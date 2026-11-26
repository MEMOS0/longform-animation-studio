"""YouTube public-archive ingestion utilities.

The collector intentionally separates three evidence tiers:
1. channel-list metadata (cheap, complete ordering/duration/rounded views),
2. watch-page metadata (exact public views/date/likes when exposed), and
3. media-level evidence (only when a local media file was lawfully obtained).

No tier is allowed to masquerade as a stronger tier downstream.
"""
from __future__ import annotations

import concurrent.futures
import json
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131 Safari/537.36"


@dataclass
class FetchResult:
    video_id: str
    ok: bool
    data: dict[str, Any] | None = None
    error: str | None = None


def fetch_url(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    return urllib.request.urlopen(req, timeout=timeout).read()


def extract_json_object(source: str, variable_name: str) -> dict[str, Any] | None:
    match = re.search(re.escape(variable_name) + r"\s*=\s*({)", source)
    if not match:
        return None
    start = match.start(1)
    depth = 0
    in_string = False
    escaped = False
    backslash = chr(92)
    for index, char in enumerate(source[start:], start):
        if in_string:
            if escaped:
                escaped = False
            elif char == backslash:
                escaped = True
            elif char == '"':
                in_string = False
        else:
            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(source[start : index + 1])
    return None


def walk_objects(node: Any, key: str) -> list[Any]:
    hits: list[Any] = []
    if isinstance(node, dict):
        for child_key, value in node.items():
            if child_key == key:
                hits.append(value)
            hits.extend(walk_objects(value, key))
    elif isinstance(node, list):
        for value in node:
            hits.extend(walk_objects(value, key))
    return hits


def text_runs(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if "simpleText" in value:
            return str(value["simpleText"])
        if "runs" in value:
            return "".join(str(run.get("text", "")) for run in value.get("runs", []))
        if "content" in value:
            return str(value["content"])
    return str(value)


def parse_published_date(text: str) -> str | None:
    clean = text.replace("Premiered", "").replace("Streamed live on", "").strip()
    for fmt in ("%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(clean, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def parse_watch_page(video_id: str, html: str) -> dict[str, Any]:
    initial = extract_json_object(html, "ytInitialData") or {}
    primary_hits = walk_objects(initial, "videoPrimaryInfoRenderer")
    secondary_hits = walk_objects(initial, "videoSecondaryInfoRenderer")
    primary = primary_hits[0] if primary_hits else {}
    secondary = secondary_hits[0] if secondary_hits else {}

    view_renderer = primary.get("viewCount", {}).get("videoViewCountRenderer", {})
    exact_views = view_renderer.get("originalViewCount")
    date_text = text_runs(primary.get("dateText"))
    title = text_runs(primary.get("title"))

    description = ""
    desc_hits = walk_objects(secondary, "attributedDescriptionBodyText") or walk_objects(secondary, "descriptionBodyText")
    if desc_hits:
        description = text_runs(desc_hits[0])

    like_count = None
    like_hits = walk_objects(primary, "likeCount")
    if like_hits:
        try:
            like_count = int(str(like_hits[0]).replace(",", ""))
        except (TypeError, ValueError):
            like_count = None

    return {
        "video_id": video_id,
        "watch_url": f"https://www.youtube.com/watch?v={video_id}",
        "exact_title": title or None,
        "exact_view_count": int(exact_views) if exact_views and str(exact_views).isdigit() else None,
        "published_text": date_text or None,
        "published_date": parse_published_date(date_text) if date_text else None,
        "like_count": like_count,
        "description": description or None,
        "page_evidence": {
            "primary_renderer_found": bool(primary),
            "secondary_renderer_found": bool(secondary),
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        },
    }


def fetch_watch_metadata(video_id: str) -> FetchResult:
    try:
        html = fetch_url(f"https://www.youtube.com/watch?v={video_id}").decode("utf-8", "ignore")
        return FetchResult(video_id=video_id, ok=True, data=parse_watch_page(video_id, html))
    except Exception as exc:  # network/source instability is data, not a hidden success
        return FetchResult(video_id=video_id, ok=False, error=repr(exc))


def load_channel_flat(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def download_thumbnail(video_id: str, output_dir: Path) -> str | None:
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / f"{video_id}.jpg"
    if target.exists() and target.stat().st_size > 10_000:
        return str(target)
    for quality in ("maxresdefault", "hq720", "sddefault", "hqdefault"):
        url = f"https://i.ytimg.com/vi/{video_id}/{quality}.jpg"
        try:
            payload = fetch_url(url, timeout=20)
            if len(payload) > 10_000:
                target.write_bytes(payload)
                return str(target)
        except Exception:
            continue
    return None


def parse_rss(xml_path: Path) -> dict[str, dict[str, str]]:
    if not xml_path.exists():
        return {}
    root = ET.fromstring(xml_path.read_bytes())
    ns = {"atom": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
    result = {}
    for entry in root.findall("atom:entry", ns):
        video_id = entry.findtext("yt:videoId", namespaces=ns)
        published = entry.findtext("atom:published", namespaces=ns)
        updated = entry.findtext("atom:updated", namespaces=ns)
        if video_id:
            result[video_id] = {"rss_published": published or "", "rss_updated": updated or ""}
    return result


def collect(channel_json_path: Path, output_dir: Path, thumbnail_dir: Path, workers: int = 6) -> Path:
    """Merge channel-list, watch-page, RSS, and thumbnail evidence into one JSONL file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    channel = load_channel_flat(channel_json_path)
    entries = channel.get("entries", [])
    rss = parse_rss(Path("C:/Users/Administrator/novdrama_rss.xml"))

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        watch_results = list(pool.map(fetch_watch_metadata, [entry["id"] for entry in entries]))

    watch_by_id = {result.video_id: result for result in watch_results}
    output_path = output_dir / "novdrama_archive.jsonl"
    with output_path.open("w", encoding="utf-8") as handle:
        for recency_rank, entry in enumerate(entries, start=1):
            video_id = entry["id"]
            watch_result = watch_by_id.get(video_id)
            watch = watch_result.data if watch_result and watch_result.ok and watch_result.data else {}
            thumb_path = download_thumbnail(video_id, thumbnail_dir)
            record = {
                "video_id": video_id,
                "url": entry.get("url"),
                "channel_id": channel.get("channel_id") or channel.get("id"),
                "channel_title": channel.get("channel") or channel.get("title"),
                "archive_recency_rank": recency_rank,
                "archive_title": entry.get("title"),
                "duration_seconds": entry.get("duration"),
                "rounded_view_count": entry.get("view_count"),
                "thumbnail_path": thumb_path,
                "watch_scrape_ok": bool(watch_result and watch_result.ok),
                "watch_scrape_error": watch_result.error if watch_result else "missing",
                **rss.get(video_id, {}),
                **watch,
            }
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        time.sleep(0)
    return output_path


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--channel-json", default="C:/Users/Administrator/novdrama_channel.json")
    parser.add_argument("--output-dir", default="data/raw")
    parser.add_argument("--thumbnail-dir", default="data/raw/thumbnails")
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    path = collect(Path(args.channel_json), Path(args.output_dir), Path(args.thumbnail_dir), args.workers)
    print(path)


if __name__ == "__main__":
    main()
