"""Compare dialogue/narration sentence-shape metrics across outcome cohorts."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from studio.dialogue_analysis import analyze_cues
from studio.media_analysis import parse_ttml


def mean(values):
    values = [float(v) for v in values if isinstance(v, (int, float)) and not math.isnan(float(v))]
    return sum(values) / len(values) if values else None


def compare(raw_dir: Path, outcomes_path: Path, output_json: Path, output_md: Path) -> dict:
    outcomes = {row["video_id"]: row for row in json.loads(outcomes_path.read_text(encoding="utf-8"))}
    rows = []
    for path in sorted(raw_dir.glob("*.en.ttml")):
        video_id = path.name.removesuffix(".en.ttml")
        outcome = outcomes.get(video_id, {}).get("analysis", {})
        if not outcome.get("cohort_by_age_adjusted_views"):
            continue
        analysis = analyze_cues(parse_ttml(path))
        row = {"video_id": video_id, "title": outcomes[video_id].get("exact_title") or outcomes[video_id].get("archive_title"), "cohort": outcome["cohort_by_age_adjusted_views"], "views_per_day": outcome.get("views_per_day")}
        for section in ("opening_5min", "middle", "final_10min", "full"):
            for key, value in analysis[section].items():
                if isinstance(value, (int, float)):
                    row[f"{section}_{key}"] = value
        rows.append(row)
    keys = sorted({key for row in rows for key in row if key not in {"video_id", "title", "cohort"}})
    cohorts = {}
    for cohort in sorted({row["cohort"] for row in rows}):
        group = [row for row in rows if row["cohort"] == cohort]
        cohorts[cohort] = {"n": len(group)} | {key: mean([row.get(key) for row in group]) for key in keys}
    result = {"n": len(rows), "rows": rows, "cohort_summary": cohorts, "methodological_boundary": "Subtitle-derived sentence-shape proxies; they do not measure acting, subtext, or visual emotion."}
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    interesting = [
        "opening_5min_word_count", "opening_5min_avg_sentence_words", "opening_5min_long_sentence_ratio",
        "opening_5min_exposition_marker_per_1000_words", "opening_5min_pressure_marker_per_1000_words",
        "opening_5min_care_marker_per_1000_words", "opening_5min_question_ratio",
        "final_10min_pressure_marker_per_1000_words", "final_10min_care_marker_per_1000_words",
    ]
    lines = ["# Dialogue/narration cohort comparison", "", result["methodological_boundary"], "", f"Videos analyzed: {len(rows)}", "", "| metric | outperforming | middle | underperforming |", "|---|---:|---:|---:|"]
    for key in interesting:
        vals = [cohorts.get(c, {}).get(key) for c in ("outperforming", "middle", "underperforming")]
        lines.append(f"| `{key}` | " + " | ".join("—" if v is None else f"{v:.2f}" for v in vals) + " |")
    lines.extend(["", "## Rows", "", "| video | cohort | views/day | opening words | avg sentence | exposition/1k | pressure/1k | care/1k |", "|---|---|---:|---:|---:|---:|---:|---:|"])
    for row in sorted(rows, key=lambda r: r.get("views_per_day") or 0, reverse=True):
        lines.append(f"| {row['video_id']} | {row['cohort']} | {row.get('views_per_day') or 0:.1f} | {row.get('opening_5min_word_count') or 0:.0f} | {row.get('opening_5min_avg_sentence_words') or 0:.1f} | {row.get('opening_5min_exposition_marker_per_1000_words') or 0:.1f} | {row.get('opening_5min_pressure_marker_per_1000_words') or 0:.1f} | {row.get('opening_5min_care_marker_per_1000_words') or 0:.1f} |")
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", default="data/raw/piped")
    parser.add_argument("--outcomes", default="data/processed/novdrama_analysis_rows.json")
    parser.add_argument("--output-json", default="data/processed/dialogue_cohort_comparison.json")
    parser.add_argument("--output-md", default="data/processed/dialogue_cohort_comparison.md")
    args = parser.parse_args()
    result = compare(Path(args.raw_dir), Path(args.outcomes), Path(args.output_json), Path(args.output_md))
    print(json.dumps({"videos": result["n"], "output": args.output_md}, indent=2))


if __name__ == "__main__":
    main()
