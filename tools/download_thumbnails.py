"""Download highest-available YouTube thumbnails and build a metadata index."""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from studio.thumbnail_intelligence import analyze_thumbnail, write_index

UA = {"User-Agent": "Mozilla/5.0 longform-animation-studio research"}


def safe_filename_component(value: str, fallback: str = "unknown") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", str(value)).strip("_")[:80]
    return cleaned or fallback


def valid_video_id(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_-]{6,40}", str(value or "")))


def fetch(url: str, timeout: int = 30) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def download_one(video_id: str, out_dir: Path) -> tuple[Path | None, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    for quality in ("maxresdefault", "sddefault", "hqdefault"):
        path = out_dir / f"{video_id}.{quality}.jpg"
        if path.exists() and path.stat().st_size > 1000:
            return path, quality
        url = f"https://i.ytimg.com/vi/{video_id}/{quality}.jpg"
        try:
            data = fetch(url)
        except Exception:
            continue
        # hqdefault can be a 120x90 placeholder; maxres missing often returns a tiny placeholder.
        if len(data) < 5000 and quality != "hqdefault":
            continue
        path.write_bytes(data)
        return path, quality
    return None, "failed"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="JSON/JSONL rows containing video_id; optional metadata fields")
    parser.add_argument("--output-root", default="thumbnails/reference")
    parser.add_argument("--index", default="thumbnails/index.jsonl")
    args = parser.parse_args()
    source = Path(args.input)
    if source.suffix == ".jsonl":
        rows = [json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        rows = json.loads(source.read_text(encoding="utf-8"))
    out = []
    for row in rows:
        vid = row.get("video_id") or row.get("id")
        if not vid:
            continue
        if not valid_video_id(vid):
            record = dict(row)
            record["video_id"] = vid
            record["download_error"] = "invalid unsafe video id"
            out.append(record)
            continue
        channel = safe_filename_component((row.get("channel") or row.get("channel_title") or row.get("uploader") or "unknown").lower())
        path, quality = download_one(vid, Path(args.output_root) / channel)
        record = dict(row)
        record["video_id"] = vid
        record["channel_key"] = channel
        record["thumbnail_quality"] = quality
        record["downloaded_at_unix"] = int(time.time())
        if path:
            record["thumbnail_path"] = str(path).replace("\\", "/")
            try:
                record["visual_metrics"] = analyze_thumbnail(path)
            except Exception as exc:
                record["analysis_error"] = repr(exc)
        else:
            record["download_error"] = "no usable thumbnail variant"
        out.append(record)
        print(json.dumps({"video_id": vid, "quality": quality, "ok": bool(path)}), flush=True)
    write_index(out, Path(args.index))
    print(json.dumps({"indexed": len(out), "index": args.index}))


if __name__ == "__main__":
    main()
