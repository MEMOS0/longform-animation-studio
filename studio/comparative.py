"""Comparative success/failure analysis for a single-channel archive.

Methodological stance:
- Public views are noisy cumulative outcomes, not retention or CTR.
- Age control is mandatory but imperfect because older videos compound recommendations.
- Small samples produce unstable theme effects; therefore outputs report effect direction,
  uncertainty, evidence tier, and alternative explanations rather than false certainty.
"""
from __future__ import annotations

import json
import math
import random
import statistics
from datetime import date, datetime
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .features import THEME_PATTERNS, flatten_theme

SNAPSHOT_DATE = date(2026, 11, 26)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [json.loads(line) for line in handle.readlines() if line.strip()]


def parse_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None


def infer_snapshot_date(rows: list[dict[str, Any]]) -> date:
    scraped = []
    for row in rows:
        value = row.get("page_evidence", {}).get("scraped_at")
        if value:
            try:
                scraped.append(datetime.fromisoformat(value.replace("Z", "+00:00")).date())
            except ValueError:
                pass
    if scraped:
        return max(scraped)
    raise ValueError("snapshot date is not inferable from archive scrape timestamps; pass snapshot_date explicitly")


def add_outcomes(rows: list[dict[str, Any]], snapshot_date: date | None = None) -> list[dict[str, Any]]:
    snapshot_date = snapshot_date or infer_snapshot_date(rows)
    for row in rows:
        published = parse_iso_date(row.get("published_date") or row.get("uploadDate"))
        age_days = (snapshot_date - published).days + 1 if published else None
        if age_days is not None and age_days < 1:
            age_days = None
        views = row.get("exact_view_count") or row.get("views") or row.get("rounded_view_count") or 0
        duration = row.get("duration_seconds") or row.get("duration") or 0
        row["analysis"] = {
            "views": int(views),
            "published_date": published.isoformat() if published else None,
            "age_days_at_snapshot": age_days,
            "views_per_day": views / age_days if age_days else None,
            "log_views_per_day": math.log1p(views / age_days) if age_days else None,
            "duration_minutes": duration / 60 if duration else None,
            "snapshot_date": snapshot_date.isoformat(),
        }
    valid = [r for r in rows if r["analysis"].get("log_views_per_day") is not None]
    values = sorted(r["analysis"]["log_views_per_day"] for r in valid)
    if values:
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        median = float(np.median(values))
        for row in valid:
            value = row["analysis"]["log_views_per_day"]
            if value >= q3:
                cohort = "outperforming"
            elif value <= q1:
                cohort = "underperforming"
            else:
                cohort = "middle"
            row["analysis"].update({"cohort_by_age_adjusted_views": cohort, "archive_log_vpd_median": median, "q1": float(q1), "q3": float(q3)})
    return rows


def binary_feature(row: dict[str, Any], feature: str) -> bool:
    cf = row.get("creative_features", {})
    if feature in THEME_PATTERNS:
        return flatten_theme(row, feature)
    if feature == "female_protagonist":
        return cf.get("protagonist_gender") == "female"
    if feature == "male_protagonist":
        return cf.get("protagonist_gender") == "male"
    if feature == "ambiguous_protagonist":
        return cf.get("protagonist_gender") == "ambiguous"
    if feature in ("victimization", "hidden_identity_or_secret", "status_reversal", "kinship_rescue"):
        return bool(cf.get(feature, {}).get("present"))
    return bool(cf.get("title_structure", {}).get(feature))


def permutation_test(values_a: list[float], values_b: list[float], iterations: int = 5000, seed: int = 13) -> dict[str, float]:
    if len(values_a) < 2 or len(values_b) < 2:
        return {"effect": float("nan"), "p": float("nan")}
    rng = random.Random(seed)
    observed = statistics.mean(values_a) - statistics.mean(values_b)
    combined = values_a + values_b
    count = 0
    for _ in range(iterations):
        rng.shuffle(combined)
        sample_a = combined[: len(values_a)]
        sample_b = combined[len(values_a) :]
        if abs(statistics.mean(sample_a) - statistics.mean(sample_b)) >= abs(observed):
            count += 1
    return {"effect": observed, "p": (count + 1) / (iterations + 1)}


def compare_binary_feature(rows: list[dict[str, Any]], feature: str) -> dict[str, Any]:
    valid = [r for r in rows if r.get("analysis", {}).get("log_views_per_day") is not None]
    present = [r for r in valid if binary_feature(r, feature)]
    absent = [r for r in valid if not binary_feature(r, feature)]
    a = [r["analysis"]["log_views_per_day"] for r in present]
    b = [r["analysis"]["log_views_per_day"] for r in absent]
    test = permutation_test(a, b)
    return {
        "feature": feature,
        "present_n": len(present),
        "absent_n": len(absent),
        "present_mean_log_vpd": statistics.mean(a) if a else None,
        "absent_mean_log_vpd": statistics.mean(b) if b else None,
        "mean_difference_log_vpd": test["effect"],
        "permutation_p": test["p"],
        "top_present_examples": sorted(({"id": r["video_id"], "vpd": round(r["analysis"]["views_per_day"], 1), "title": r.get("exact_title") or r.get("archive_title")} for r in present), key=lambda x: -x["vpd"])[:5],
        "bottom_present_examples": sorted(({"id": r["video_id"], "vpd": round(r["analysis"]["views_per_day"], 1), "title": r.get("exact_title") or r.get("archive_title")} for r in present), key=lambda x: x["vpd"])[:5],
    }


def numeric_correlation(rows: list[dict[str, Any]], getter, name: str) -> dict[str, Any]:
    pairs = []
    for row in rows:
        value = getter(row)
        outcome = row.get("analysis", {}).get("log_views_per_day")
        if value is not None and outcome is not None:
            pairs.append((float(value), float(outcome), row["video_id"]))
    if len(pairs) < 4:
        return {"feature": name, "n": len(pairs), "spearman_like": None}
    x = np.array([p[0] for p in pairs])
    y = np.array([p[1] for p in pairs])
    xr = np.argsort(np.argsort(x))
    yr = np.argsort(np.argsort(y))
    corr = float(np.corrcoef(xr, yr)[0, 1])
    return {"feature": name, "n": len(pairs), "rank_correlation": corr, "min": float(x.min()), "max": float(x.max()), "mean": float(x.mean())}


def create_thumbnail_montage(rows: list[dict[str, Any]], output: Path, thumb_size=(256, 144), cols=6) -> Path | None:
    rows = sorted(rows, key=lambda r: -(r.get("analysis", {}).get("views_per_day") or 0))
    tiles = []
    font = ImageFont.load_default()
    for row in rows:
        path = row.get("thumbnail_path")
        if not path or not Path(path).exists():
            continue
        image = Image.open(path).convert("RGB").resize(thumb_size)
        canvas = Image.new("RGB", (thumb_size[0], thumb_size[1] + 28), "black")
        canvas.paste(image, (0, 0))
        draw = ImageDraw.Draw(canvas)
        analysis = row.get("analysis", {})
        vpd = analysis.get('views_per_day') or 0
        label = f"{row['video_id']} {vpd:.0f}/d {analysis.get('cohort_by_age_adjusted_views', '?')[:4]}"
        draw.text((3, thumb_size[1] + 5), label, fill="white", font=font)
        tiles.append(canvas)
    if not tiles:
        return None
    rows_n = math.ceil(len(tiles) / cols)
    sheet = Image.new("RGB", (cols * thumb_size[0], rows_n * (thumb_size[1] + 28)), "black")
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % cols) * thumb_size[0], (index // cols) * (thumb_size[1] + 28)))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=90)
    return output


def analyze(input_jsonl: Path, output_dir: Path, snapshot_date: date | None = None) -> dict[str, Path]:
    rows = add_outcomes(load_jsonl(input_jsonl), snapshot_date)
    output_dir.mkdir(parents=True, exist_ok=True)
    enriched_path = output_dir / "novdrama_analysis_rows.json"
    enriched_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    features = list(THEME_PATTERNS) + [
        "female_protagonist", "male_protagonist", "ambiguous_protagonist", "victimization",
        "hidden_identity_or_secret", "status_reversal", "kinship_rescue", "setup_then_reversal", "exclamation",
    ]
    comparisons = [compare_binary_feature(rows, feature) for feature in features]
    numeric = [
        numeric_correlation(rows, lambda r: r.get("analysis", {}).get("duration_minutes"), "duration_minutes"),
        numeric_correlation(rows, lambda r: r.get("analysis", {}).get("age_days_at_snapshot"), "age_days"),
        numeric_correlation(rows, lambda r: r.get("creative_features", {}).get("title_structure", {}).get("characters"), "title_characters"),
        numeric_correlation(rows, lambda r: r.get("creative_features", {}).get("title_structure", {}).get("caps_ratio"), "title_caps_ratio"),
        numeric_correlation(rows, lambda r: r.get("thumbnail_features", {}).get("brightness") if r.get("thumbnail_features", {}).get("available") else None, "thumbnail_brightness"),
        numeric_correlation(rows, lambda r: r.get("thumbnail_features", {}).get("saturation") if r.get("thumbnail_features", {}).get("available") else None, "thumbnail_saturation"),
        numeric_correlation(rows, lambda r: r.get("thumbnail_features", {}).get("lower_half_edge_density_proxy_for_text") if r.get("thumbnail_features", {}).get("available") else None, "thumbnail_text_edge_proxy"),
    ]

    montage = create_thumbnail_montage(rows, output_dir / "novdrama_thumbnail_montage.jpg")
    sorted_rows = sorted(rows, key=lambda r: -(r.get("analysis", {}).get("views_per_day") or 0))
    leaderboard = [
        {
            "rank": index + 1,
            "video_id": row["video_id"],
            "title": row.get("exact_title") or row.get("archive_title"),
            "views": row["analysis"]["views"],
            "published": row["analysis"]["published_date"],
            "age_days": row["analysis"]["age_days_at_snapshot"],
            "views_per_day": round(row["analysis"]["views_per_day"], 1) if row["analysis"].get("views_per_day") is not None else None,
            "duration_minutes": round(row["analysis"]["duration_minutes"], 1) if row["analysis"].get("duration_minutes") else None,
            "cohort": row["analysis"].get("cohort_by_age_adjusted_views"),
        }
        for index, row in enumerate(sorted_rows)
    ]

    results = {
        "method_limits": [
            "Public views cannot separate CTR, retention, impressions, browse/search/suggested traffic, or external embedding.",
            "Views-per-day controls age crudely but does not remove recommendation compounding or premiere spikes.",
            "Theme labels are title-visible demand signals, not proof that the film itself executes that theme well.",
            "n=48 and many feature cells are small; permutation tests are exploratory and not multiple-comparison-corrected causal evidence.",
        ],
        "leaderboard": leaderboard,
        "binary_feature_comparisons": comparisons,
        "numeric_correlations": numeric,
        "montage": str(montage) if montage else None,
    }
    results_path = output_dir / "novdrama_comparative_results.json"
    results_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path = output_dir / "novdrama_comparative_report.md"
    report_path.write_text(render_markdown(results), encoding="utf-8")
    return {"rows": enriched_path, "results": results_path, "report": report_path, "montage": montage} if montage else {"rows": enriched_path, "results": results_path, "report": report_path}


def fmt(value: Any, digits: int = 2) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "n/a"
    if isinstance(value, (int, float)):
        return f"{value:.{digits}f}"
    return str(value)


def render_markdown(results: dict[str, Any]) -> str:
    lines = [
        "# Nov Drama comparative archive analysis",
        "",
        "Outcome metric: public cumulative views converted to views/day at the scrape snapshot. This is a discovery metric, not CTR or retention.",
        "",
        "## Method limits",
    ]
    lines += [f"- {item}" for item in results["method_limits"]]
    lines += ["", "## Age-adjusted leaderboard (top/bottom)", "", "|rank|video|views|age days|views/day|minutes|cohort|", "|---:|---|---:|---:|---:|---:|---|"]
    for row in results["leaderboard"][:12] + results["leaderboard"][-12:]:
        title = row["title"].replace("|", "/")[:95]
        lines.append(f"|{row['rank']}|[{row['video_id']}](https://www.youtube.com/watch?v={row['video_id']}) {title}|{row['views']}|{row['age_days']}|{row['views_per_day']}|{row['duration_minutes']}|{row['cohort']}|")
    lines += ["", "## Binary creative-feature comparisons", "", "Positive difference means videos with the feature have higher mean log views/day. p values are exploratory permutation tests.", "", "|feature|present n|absent n|mean diff log vpd|p|", "|---|---:|---:|---:|---:|"]
    for row in sorted(results["binary_feature_comparisons"], key=lambda x: -(x["mean_difference_log_vpd"] if x["mean_difference_log_vpd"] == x["mean_difference_log_vpd"] else -99)):
        lines.append(f"|{row['feature']}|{row['present_n']}|{row['absent_n']}|{fmt(row['mean_difference_log_vpd'])}|{fmt(row['permutation_p'], 3)}|")
    lines += ["", "## Continuous proxies", "", "|feature|n|rank correlation|range|", "|---|---:|---:|---|"]
    for row in results["numeric_correlations"]:
        lines.append(f"|{row['feature']}|{row['n']}|{fmt(row.get('rank_correlation'))}|{fmt(row.get('min'))}–{fmt(row.get('max'))}|")
    lines += ["", "See `novdrama_comparative_results.json` for examples and full rows; `novdrama_thumbnail_montage.jpg` is sorted by age-adjusted outcome.", ""]
    return "\n".join(lines)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="data/processed/novdrama_enriched.jsonl")
    parser.add_argument("output_dir", nargs="?", default="data/processed")
    args = parser.parse_args()
    print(json.dumps({k: str(v) for k, v in analyze(Path(args.input), Path(args.output_dir)).items()}, indent=2))


if __name__ == "__main__":
    main()
