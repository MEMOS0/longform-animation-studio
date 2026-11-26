"""Build auditable, timestamped story casebooks from media-analysis timelines."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from studio.media_analysis import parse_ttml
from studio.story_signals import read_jsonl, summarize_story_signals


def load_outcomes(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    rows = json.loads(path.read_text(encoding="utf-8"))
    return {row["video_id"]: row for row in rows}


def render_casebook(casebook: dict, outcome: dict | None) -> str:
    lines = [f"# Video casebook: {casebook['video_id']}", ""]
    if outcome:
        analysis = outcome.get("analysis", {})
        lines.extend(
            [
                f"Title: {outcome.get('exact_title') or outcome.get('archive_title')}",
                f"Outcome: {analysis.get('views')} views; {analysis.get('views_per_day')} views/day; cohort `{analysis.get('cohort_by_age_adjusted_views')}`",
                "",
            ]
        )
    lines.extend(
        [
            "## First explicit story signals",
            "",
        ]
    )
    for category, item in casebook["first_signal_occurrences"].items():
        if item:
            lines.append(f"- `{category}` at {item['time']:.1f}s: “{item['text']}”")
        else:
            lines.append(f"- `{category}`: no explicit marker found")
    lines.extend(["", "## Five-minute audiovisual/narrative windows", ""])
    for window in casebook["windows"]:
        counts = ", ".join(f"{k}={v}" for k, v in window["signal_counts"].items() if v)
        visual = window["visual"]
        audio = window["audio"]
        lines.append(f"### {window['start']//60:02d}:{window['start']%60:02d}–{window['end']//60:02d}:{window['end']%60:02d}")
        lines.append(f"- Signals: {counts or 'none detected'}")
        lines.append(
            "- Proxies: "
            f"brightness={visual['brightness']:.3f}, motion={visual['motion']:.3f}, "
            f"rms={audio['rms_mean']:.3f}, silence={audio['silence_ratio']:.3f}, "
            f"dialogue_words={window['dialogue_words']}, shot_boundaries={window['shot_boundaries']}"
            if visual["brightness"] is not None and audio["rms_mean"] is not None else "- Proxies unavailable"
        )
        for snippet in window["evidence_snippets"]:
            lines.append(f"- Evidence {snippet['time']}s: “{snippet['quote']}”")
        lines.append("")
    lines.extend(["## Boundaries", ""])
    lines.extend(f"- {item}" for item in casebook["interpretation_boundaries"])
    lines.append("")
    return "\n".join(lines)


def build(media_root: Path, output_root: Path, outcomes_path: Path, subtitle_raw_dir: Path = Path("data/raw/piped")) -> list[Path]:
    output_root.mkdir(parents=True, exist_ok=True)
    outcomes = load_outcomes(outcomes_path)
    written = []
    for video_dir in sorted(path for path in media_root.iterdir() if path.is_dir()):
        timelines = list(video_dir.glob("*.timeline.jsonl"))
        if not timelines:
            continue
        video_id = video_dir.name
        timeline_rows = read_jsonl(timelines[0])
        subtitle = subtitle_raw_dir / f"{video_id}.en.ttml"
        cues = parse_ttml(subtitle) if subtitle.exists() else []
        casebook = summarize_story_signals(video_id, timeline_rows, cues)
        casebook["outcome"] = outcomes.get(video_id, {}).get("analysis")
        json_path = output_root / f"{video_id}.casebook.json"
        md_path = output_root / f"{video_id}.casebook.md"
        json_path.write_text(json.dumps(casebook, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path.write_text(render_casebook(casebook, outcomes.get(video_id)), encoding="utf-8")
        written.extend([json_path, md_path])
    return written


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--media-root", default="data/processed/media_batch")
    parser.add_argument("--output-root", default="data/processed/casebooks")
    parser.add_argument("--outcomes", default="data/processed/novdrama_analysis_rows.json")
    parser.add_argument("--subtitle-raw-dir", default="data/raw/piped")
    args = parser.parse_args()
    written = build(Path(args.media_root), Path(args.output_root), Path(args.outcomes), Path(args.subtitle_raw_dir))
    print(json.dumps({"casebooks_written": len(written) // 2, "files": len(written)}, indent=2))


if __name__ == "__main__":
    main()
