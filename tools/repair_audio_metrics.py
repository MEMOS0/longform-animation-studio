"""Repair audio fields in existing media-analysis timelines after extractor fixes."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from studio.media_analysis import audio_features
from studio.story_signals import read_jsonl


def repair(media_root: Path, media_dir: Path) -> dict[str, int]:
    repaired = 0
    missing = 0
    for timeline_path in sorted(media_root.glob("*/*.timeline.jsonl")):
        video_dir = timeline_path.parent
        video_id = video_dir.name
        video_path = media_dir / f"{video_id}.mp4"
        rows = read_jsonl(timeline_path)
        if not rows or not video_path.exists():
            missing += 1
            continue
        audio = audio_features(video_path, video_dir)
        if not audio:
            missing += 1
            continue
        for row in rows:
            for key in list(row):
                if key.startswith("audio_"):
                    row.pop(key, None)
            row.update({f"audio_{k}": v for k, v in audio.get(int(row.get("start", 0)), {}).items()})
        with timeline_path.open("w", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        repaired += 1
    return {"repaired": repaired, "missing_or_skipped": missing}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--media-root", default="data/processed/media_batch")
    parser.add_argument("--media-dir", default="C:/Users/Administrator/novdrama_media")
    args = parser.parse_args()
    print(json.dumps(repair(Path(args.media_root), Path(args.media_dir)), indent=2))


if __name__ == "__main__":
    main()
