"""Collect public channel video rows through a Piped-compatible endpoint."""
from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 longform-animation-studio research"}


def get_json(url: str):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())


def collect(base: str, channel_id: str, max_pages: int = 10) -> dict:
    rows = []
    seen = set()
    channel_meta = {}
    nextpage = None
    for _ in range(max_pages):
        if nextpage:
            url = f"{base}/nextpage/channel/{channel_id}?nextpage=" + urllib.parse.quote(str(nextpage), safe="")
        else:
            url = f"{base}/channel/{channel_id}"
        data = get_json(url)
        if not channel_meta:
            channel_meta = {k: data.get(k) for k in ("id", "name", "description", "subscriberCount", "verified", "tabs")}
        items = data.get("relatedStreams") or []
        for item in items:
            vid = ""
            match = re.search(r"[?&]v=([A-Za-z0-9_-]+)", item.get("url") or "")
            if match:
                vid = match.group(1)
            if not vid or vid in seen:
                continue
            seen.add(vid)
            rows.append({
                "video_id": vid,
                "title": item.get("title"),
                "channel": item.get("uploaderName") or channel_meta.get("name"),
                "channel_id": channel_id,
                "channel_subscriber_count": channel_meta.get("subscriberCount"),
                "duration_seconds": item.get("duration"),
                "views": item.get("views"),
                "uploaded_ms": item.get("uploaded"),
                "uploaded_text": item.get("uploadedDate"),
                "is_short": item.get("isShort"),
                "piped_thumbnail": item.get("thumbnail"),
                "url": "https://www.youtube.com/watch?v=" + vid,
            })
        nextpage = data.get("nextpage")
        if not nextpage or not items:
            break
    return {"channel": channel_meta, "videos": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="https://maxtube-api.lawrie.co.nz")
    parser.add_argument("--channel-id", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--max-pages", type=int, default=10)
    args = parser.parse_args()
    data = collect(args.base.rstrip("/"), args.channel_id, args.max_pages)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"channel": data["channel"].get("name"), "videos": len(data["videos"])}))


if __name__ == "__main__":
    main()
