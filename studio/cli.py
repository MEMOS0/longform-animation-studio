"""Command line interface for the long-form animation studio intelligence system."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from .comparative import analyze as comparative_analyze
from .failure_intelligence import evaluate_candidate, render_report
from .features import enrich_records
from .media_analysis import analyze_video
from .production import evaluate_project
from .release_learning import release_postmortem
from .storyboard_production import export_manifest
from .premise_generator import generate_and_write
from .storyboard_seed import write_seed_boards
from .youtube_archive import collect


def main() -> None:
    parser = argparse.ArgumentParser(prog="studio")
    sub = parser.add_subparsers(dest="command", required=True)

    collect_p = sub.add_parser("collect-archive")
    collect_p.add_argument("--channel-json", required=True)
    collect_p.add_argument("--output-dir", default="data/raw")
    collect_p.add_argument("--thumbnail-dir", default="data/raw/thumbnails")

    enrich_p = sub.add_parser("enrich-archive")
    enrich_p.add_argument("input")
    enrich_p.add_argument("output")

    compare_p = sub.add_parser("compare")
    compare_p.add_argument("input")
    compare_p.add_argument("output_dir")
    compare_p.add_argument("--snapshot-date", default="", help="YYYY-MM-DD snapshot for archives without scrape timestamps")

    media_p = sub.add_parser("analyze-media")
    media_p.add_argument("video")
    media_p.add_argument("--subtitle", default="")
    media_p.add_argument("--output-dir", required=True)
    media_p.add_argument("--video-id", required=True)

    risk_p = sub.add_parser("evaluate-idea")
    risk_p.add_argument("--archive", default="data/processed/novdrama_analysis_rows.json")
    risk_p.add_argument("--candidate", required=True)
    risk_p.add_argument("--script-file", default="")
    risk_p.add_argument("--output", default="data/processed/failure_intelligence_evaluation.md")

    project_p = sub.add_parser("evaluate-project")
    project_p.add_argument("--premise", required=True)
    project_p.add_argument("--architecture", default="")
    project_p.add_argument("--scenes", default="")
    project_p.add_argument("--storyboards", default="")
    project_p.add_argument("--archive", default="data/processed/novdrama_analysis_rows.json")
    project_p.add_argument("--output", required=True)

    gen_p = sub.add_parser("generate-premises")
    gen_p.add_argument("--output-dir", required=True)
    gen_p.add_argument("--count", type=int, default=3)
    gen_p.add_argument("--contract", default="social_test_melodrama")
    gen_p.add_argument("--target-minutes", type=float, default=42)
    gen_p.add_argument("--archive", default="data/processed/novdrama_analysis_rows.json")

    prompts_p = sub.add_parser("export-production-prompts")
    prompts_p.add_argument("--storyboards", required=True)
    prompts_p.add_argument("--output-dir", required=True)
    prompts_p.add_argument("--project-id", default="project")

    seed_p = sub.add_parser("seed-storyboards")
    seed_p.add_argument("--scenes", required=True)
    seed_p.add_argument("--output-dir", required=True)

    post_p = sub.add_parser("release-postmortem")
    post_p.add_argument("--release", required=True, help="release metadata JSON with video_id,title,views,age_days")
    post_p.add_argument("--preproduction", default="")
    post_p.add_argument("--cohort", default="")
    post_p.add_argument("--output", required=True)

    args = parser.parse_args()
    if args.command == "collect-archive":
        print(collect(Path(args.channel_json), Path(args.output_dir), Path(args.thumbnail_dir)))
    elif args.command == "enrich-archive":
        print(enrich_records(Path(args.input), Path(args.output)))
    elif args.command == "compare":
        snapshot = date.fromisoformat(args.snapshot_date) if args.snapshot_date else None
        print(json.dumps({k: str(v) for k, v in comparative_analyze(Path(args.input), Path(args.output_dir), snapshot).items()}, indent=2))
    elif args.command == "analyze-media":
        result = analyze_video(Path(args.video), Path(args.subtitle) if args.subtitle else None, Path(args.output_dir), args.video_id)
        print(json.dumps({k: str(v) for k, v in result.items()}, indent=2))
    elif args.command == "evaluate-idea":
        rows = json.loads(Path(args.archive).read_text(encoding="utf-8"))
        script_text = Path(args.script_file).read_text(encoding="utf-8") if args.script_file else ""
        result = evaluate_candidate(args.candidate, rows, script_text)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_report(result), encoding="utf-8")
        output.with_suffix(".json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(output)
    elif args.command == "evaluate-project":
        rows = json.loads(Path(args.archive).read_text(encoding="utf-8"))
        result = evaluate_project(Path(args.premise), Path(args.architecture) if args.architecture else None, Path(args.scenes) if args.scenes else None, rows, Path(args.storyboards) if args.storyboards else None)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(output)
    elif args.command == "generate-premises":
        rows = json.loads(Path(args.archive).read_text(encoding="utf-8"))
        result = generate_and_write(Path(args.output_dir), args.count, args.target_minutes, rows, args.contract)
        print(json.dumps({"count": result["count"], "premise_ids": [row["premise_id"] for row in result["premises"]]}, indent=2))
    elif args.command == "export-production-prompts":
        result = export_manifest(Path(args.storyboards), Path(args.output_dir), args.project_id)
        print(json.dumps({"output": str(Path(args.output_dir) / "production_manifest.json"), "shot_count": result["shot_count"], "scene_count": result["scene_count"]}, indent=2))
    elif args.command == "seed-storyboards":
        result = write_seed_boards(Path(args.scenes), Path(args.output_dir))
        print(json.dumps({"output_dir": args.output_dir, "scene_count": result["scene_count"], "shot_count": sum(row["shot_count"] for row in result["boards"])}, indent=2))
    elif args.command == "release-postmortem":
        release = json.loads(Path(args.release).read_text(encoding="utf-8"))
        pre = json.loads(Path(args.preproduction).read_text(encoding="utf-8")) if args.preproduction else None
        cohort = json.loads(Path(args.cohort).read_text(encoding="utf-8")) if args.cohort else []
        result = release_postmortem(release, pre, cohort)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(output)


if __name__ == "__main__":
    main()
