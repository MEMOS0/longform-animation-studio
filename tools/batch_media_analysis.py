"""Run timestamped media analysis for every locally downloaded archive video."""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from studio.media_analysis import analyze_video


def one(video: Path, raw_dir: Path, out_root: Path) -> dict:
    video_id = video.stem
    if (out_root / video_id / f"{video_id}.media_summary.json").exists():
        return {"video_id": video_id, "ok": True, "skipped_existing": True}
    try:
        result = analyze_video(video, raw_dir / f"{video_id}.en.ttml", out_root / video_id, video_id)
        return {"video_id": video_id, "ok": True, "summary": str(result["summary"])}
    except Exception as exc:
        return {"video_id": video_id, "ok": False, "error": repr(exc), "traceback": traceback.format_exc()[-2000:]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--media-dir", default="C:/Users/Administrator/novdrama_media")
    parser.add_argument("--raw-dir", default="data/raw/piped")
    parser.add_argument("--out-root", default="data/processed/media_batch")
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    videos = sorted(Path(args.media_dir).glob("*.mp4"))
    out_root = Path(args.out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    results_path = out_root / "batch_results.jsonl"
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(one, video, Path(args.raw_dir), out_root) for video in videos]
        with results_path.open("a", encoding="utf-8") as handle:
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                handle.write(json.dumps(result, ensure_ascii=False) + "\n")
                handle.flush()
                print(json.dumps({k: v for k, v in result.items() if k != "traceback"}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
