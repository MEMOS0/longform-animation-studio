"""Compare timestamped story casebooks across success cohorts."""
from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any


def mean(values: list[float]) -> float | None:
    clean = [float(v) for v in values if v is not None and not math.isnan(float(v))]
    return sum(clean) / len(clean) if clean else None


def first_time(casebook: dict[str, Any], category: str) -> float | None:
    item = casebook.get("first_signal_occurrences", {}).get(category) or {}
    return item.get("time")


def windows_in(casebook: dict[str, Any], start: float, end: float) -> list[dict[str, Any]]:
    return [w for w in casebook.get("windows", []) if w.get("start", 0) < end and w.get("end", 0) > start]


def aggregate_window(windows: list[dict[str, Any]]) -> dict[str, Any]:
    if not windows:
        return {}
    signal_totals: dict[str, int] = {}
    for window in windows:
        for key, value in window.get("signal_counts", {}).items():
            signal_totals[key] = signal_totals.get(key, 0) + int(value)
    return {
        "signal_counts": signal_totals,
        "brightness": mean([(w.get("visual") or {}).get("brightness") for w in windows]),
        "motion": mean([(w.get("visual") or {}).get("motion") for w in windows]),
        "rms": mean([(w.get("audio") or {}).get("rms_mean") for w in windows]),
        "silence": mean([(w.get("audio") or {}).get("silence_ratio") for w in windows]),
        "dialogue_words": sum(int(w.get("dialogue_words") or 0) for w in windows),
        "shot_boundaries": sum(int(w.get("shot_boundaries") or 0) for w in windows),
    }


def rate(count: int | float | None, minutes: float) -> float | None:
    return (float(count) / minutes) if count is not None and minutes else None


def extract_metrics(casebook: dict[str, Any]) -> dict[str, Any]:
    duration = float(casebook.get("duration_seconds") or 0)
    hours = duration / 3600 if duration else 0
    total = casebook.get("total_signal_counts", {})
    final = casebook.get("final_10_minutes_signal_counts", {})
    opening = aggregate_window(windows_in(casebook, 0, 300))
    ending_start = max(duration - 600, 0)
    ending = aggregate_window(windows_in(casebook, ending_start, duration + 1))
    metrics: dict[str, Any] = {
        "video_id": casebook["video_id"],
        "cohort": (casebook.get("outcome") or {}).get("cohort_by_age_adjusted_views"),
        "views_per_day": (casebook.get("outcome") or {}).get("views_per_day"),
        "duration_minutes": duration / 60 if duration else None,
    }
    for category, count in total.items():
        metrics[f"{category}_per_hour"] = rate(count, hours)
        metrics[f"first_{category}_seconds"] = first_time(casebook, category)
        metrics[f"final10_{category}_count"] = final.get(category, 0)
    metrics.update(
        {
            "opening_brightness": opening.get("brightness"),
            "opening_motion": opening.get("motion"),
            "opening_rms": opening.get("rms"),
            "opening_silence": opening.get("silence"),
            "opening_dialogue_words": opening.get("dialogue_words"),
            "opening_shot_boundaries": opening.get("shot_boundaries"),
            "ending_brightness": ending.get("brightness"),
            "ending_motion": ending.get("motion"),
            "ending_rms": ending.get("rms"),
            "ending_silence": ending.get("silence"),
            "ending_dialogue_words": ending.get("dialogue_words"),
            "ending_shot_boundaries": ending.get("shot_boundaries"),
            "care_minus_wound_per_hour": (total.get("care_belonging_protection", 0) - total.get("wound_or_humiliation", 0)) / hours if hours else None,
            "lore_to_care_ratio": total.get("lore_mythology_density", 0) / max(total.get("care_belonging_protection", 0), 1),
            "threat_to_care_ratio": total.get("threat_or_violence", 0) / max(total.get("care_belonging_protection", 0), 1),
        }
    )
    return metrics


def cohort_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    keys = sorted({key for row in rows for key in row if key not in {"video_id", "cohort"}})
    cohorts: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        cohorts.setdefault(row.get("cohort") or "unknown", []).append(row)
    output = {}
    for cohort, group in cohorts.items():
        output[cohort] = {"n": len(group)}
        for key in keys:
            output[cohort][key] = mean([row.get(key) for row in group if isinstance(row.get(key), (int, float))])
    return output


def compare(casebook_root: Path, output_json: Path, output_md: Path) -> dict[str, Any]:
    rows = []
    for path in sorted(casebook_root.glob("*.casebook.json")):
        rows.append(extract_metrics(json.loads(path.read_text(encoding="utf-8"))))
    rows = [row for row in rows if row.get("cohort")]
    summary = cohort_summary(rows)
    result = {"n": len(rows), "rows": rows, "cohort_summary": summary, "methodological_boundary": "Exploratory small-sample evidence; not retention/CTR causality."}
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    interesting = [
        "lore_mythology_density_per_hour", "threat_or_violence_per_hour", "care_belonging_protection_per_hour",
        "lore_to_care_ratio", "threat_to_care_ratio", "final10_wound_or_humiliation_count",
        "final10_care_belonging_protection_count", "first_wound_or_humiliation_seconds", "first_care_belonging_protection_seconds", "first_justice_reversal_payoff_seconds", "first_lore_mythology_density_seconds", "opening_brightness", "ending_brightness", "opening_rms", "opening_silence", "ending_silence",
    ]
    lines = ["# Casebook cohort comparison", "", result["methodological_boundary"], "", f"Videos analyzed: {len(rows)}", "", "| metric | outperforming | middle | underperforming |", "|---|---:|---:|---:|"]
    for key in interesting:
        values = [summary.get(c, {}).get(key) for c in ("outperforming", "middle", "underperforming")]
        lines.append(f"| `{key}` | " + " | ".join("—" if v is None else f"{v:.2f}" for v in values) + " |")
    lines.extend(["", "## Rows", "", "| video | cohort | views/day | lore/hr | threat/hr | care/hr | final wound | final care |", "|---|---|---:|---:|---:|---:|---:|---:|"])
    for row in sorted(rows, key=lambda r: r.get("views_per_day") or 0, reverse=True):
        lines.append(
            f"| {row['video_id']} | {row['cohort']} | {(row.get('views_per_day') or 0):.1f} | "
            f"{row.get('lore_mythology_density_per_hour') or 0:.1f} | {row.get('threat_or_violence_per_hour') or 0:.1f} | "
            f"{row.get('care_belonging_protection_per_hour') or 0:.1f} | {row.get('final10_wound_or_humiliation_count') or 0} | {row.get('final10_care_belonging_protection_count') or 0} |"
        )
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--casebooks", default="data/processed/casebooks")
    parser.add_argument("--output-json", default="data/processed/casebook_cohort_comparison.json")
    parser.add_argument("--output-md", default="data/processed/casebook_cohort_comparison.md")
    args = parser.parse_args()
    result = compare(Path(args.casebooks), Path(args.output_json), Path(args.output_md))
    print(json.dumps({"videos": result["n"], "output": args.output_md}, indent=2))


if __name__ == "__main__":
    main()
