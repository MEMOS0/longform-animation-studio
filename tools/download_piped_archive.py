"""Download public video/audio/subtitle evidence through a configured Piped-compatible API.

This tool deliberately stores provenance and raw API responses beside media files. Downstream
analysis must distinguish actual audiovisual evidence from metadata-only inference.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import shutil
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

API = "https://maxtube-api.lawrie.co.nz"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131 Safari/537.36"
ALLOWED_MEDIA_HOSTS = {"maxtube-proxy.lawrie.co.nz", "www.youtube.com"}


def validate_media_url(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    allowed = host in ALLOWED_MEDIA_HOSTS or host.endswith(".googlevideo.com")
    if parsed.scheme != "https" or parsed.username or parsed.password or not allowed:
        raise ValueError(f"untrusted media URL host: {host or '<missing>'}")
    return url


def get_json(url: str, timeout: int = 45) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


def download_file(url: str, target: Path, retries: int = 3) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    part = target.with_suffix(target.suffix + ".part")
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as response, part.open("wb") as handle:
                shutil.copyfileobj(response, handle, length=1024 * 1024)
            if target.exists():
                target.unlink()
            part.rename(target)
            return target
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(3 * (attempt + 1))
    return target


def download_ranged(url: str, target: Path, content_length: int, workers: int = 8, chunk_size: int = 8 * 1024 * 1024) -> Path:
    """Parallel range download for the Piped proxy, which is much faster than one stream."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size == content_length:
        return target
    chunk_dir = target.parent / (target.name + ".chunks")
    chunk_dir.mkdir(exist_ok=True)
    ranges = []
    for start in range(0, content_length, chunk_size):
        end = min(start + chunk_size - 1, content_length - 1)
        ranges.append((start, end, chunk_dir / f"{start:012d}-{end:012d}.bin"))

    def one(item):
        start, end, path = item
        expected = end - start + 1
        if path.exists() and path.stat().st_size == expected:
            return path
        req = urllib.request.Request(url, headers={"Range": f"bytes={start}-{end}", "User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as response:
            payload = response.read()
        if len(payload) != expected:
            raise IOError(f"range {start}-{end}: got {len(payload)}, expected {expected}")
        path.write_bytes(payload)
        return path

    for attempt in range(3):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
                list(pool.map(one, ranges))
            part = target.with_suffix(target.suffix + ".part")
            with part.open("wb") as output:
                for _, _, path in ranges:
                    output.write(path.read_bytes())
            if target.exists():
                target.unlink()
            part.rename(target)
            for _, _, path in ranges:
                try:
                    path.unlink()
                except OSError:
                    pass
            try:
                chunk_dir.rmdir()
            except OSError:
                pass
            return target
        except Exception:
            if attempt == 2:
                raise
            time.sleep(4 * (attempt + 1))
    return target


def fetch_one(video_id: str, media_dir: Path, raw_dir: Path, skip_media: bool = False) -> dict:
    raw_dir.mkdir(parents=True, exist_ok=True)
    media_dir.mkdir(parents=True, exist_ok=True)
    meta_path = raw_dir / f"{video_id}.piped.json"
    try:
        data = get_json(f"{API}/streams/{video_id}")
        meta_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        result = {"video_id": video_id, "ok": True, "metadata_path": str(meta_path), "duration": data.get("duration"), "views": data.get("views")}

        subtitles = data.get("subtitles") or []
        if subtitles:
            subtitle_url = subtitles[0].get("url")
            if subtitle_url:
                sub_path = download_file(validate_media_url(subtitle_url), raw_dir / f"{video_id}.en.ttml")
                result["subtitle_path"] = str(sub_path)

        streams = data.get("videoStreams") or []
        progressive = [s for s in streams if not s.get("videoOnly") and s.get("url")]
        chosen = progressive[-1] if progressive else (streams[-1] if streams else None)
        if chosen and not skip_media:
            media_path = media_dir / f"{video_id}.mp4"
            media_url = validate_media_url(chosen["url"])
            content_length = int(chosen.get("contentLength") or 0)
            if content_length > 10_000_000:
                download_ranged(media_url, media_path, content_length)
            elif not media_path.exists() or media_path.stat().st_size < 1_000_000:
                download_file(media_url, media_path)
            result["media_path"] = str(media_path)
            result["media_bytes"] = media_path.stat().st_size if media_path.exists() else 0
            result["chosen_stream"] = {k: chosen.get(k) for k in ("quality", "format", "mimeType", "videoOnly", "bitrate")}
        return result
    except Exception as exc:
        return {"video_id": video_id, "ok": False, "error": repr(exc)}


def read_ids(args: argparse.Namespace) -> list[str]:
    ids: list[str] = []
    if args.ids:
        ids.extend(args.ids.split(","))
    if args.archive_jsonl:
        for line in Path(args.archive_jsonl).read_text(encoding="utf-8").splitlines():
            if line.strip():
                ids.append(json.loads(line)["video_id"])
    seen = set()
    unique = []
    for video_id in ids:
        video_id = video_id.strip()
        if video_id and video_id not in seen:
            seen.add(video_id)
            unique.append(video_id)
    return unique


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", default="", help="Comma-separated video IDs")
    parser.add_argument("--archive-jsonl", default="", help="Archive JSONL to read IDs from")
    parser.add_argument("--media-dir", default="data/raw/media")
    parser.add_argument("--raw-dir", default="data/raw/piped")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--skip-media", action="store_true")
    args = parser.parse_args()
    ids = read_ids(args)
    output = Path(args.raw_dir) / "download_results.jsonl"
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(fetch_one, video_id, Path(args.media_dir), Path(args.raw_dir), args.skip_media) for video_id in ids]
        with output.open("w", encoding="utf-8") as handle:
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                handle.write(json.dumps(result, ensure_ascii=False) + "\n")
                handle.flush()
                print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
