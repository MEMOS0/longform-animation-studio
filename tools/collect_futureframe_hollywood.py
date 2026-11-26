"""Collect the public Future Frame Movies catalog mirrored by Hollywood.ai.

The original YouTube channel appears terminated as of 2026-11-26, so this is a
partial preservation catalog, not a complete performance archive.
"""

import html
import json
import re
import urllib.request
from pathlib import Path

SOURCE = "https://hollywood.ai/creators/future-frame-movies"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "future_frame_hollywood_catalog.json"
MD = ROOT / "knowledge" / "market" / "future-frame-catalog.md"


def clean(text: str) -> str:
    return html.unescape(re.sub(r"<.*?>", "", text)).strip()


def collect() -> list[dict]:
    req = urllib.request.Request(SOURCE, headers={"User-Agent": "Mozilla/5.0"})
    page = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    rows = []
    seen = set()
    pattern = re.compile(
        r"i\.ytimg\.com%2Fvi%2F(?P<video_id>[A-Za-z0-9_-]{6,20}).{0,5000}?"
        r"(?P<duration>\d+:\d{2}(?::\d{2})?)</span>.{0,1800}?"
        r"<h3[^>]+title=\"(?P<title>[^\"]+)\"",
        re.S,
    )
    matches = list(pattern.finditer(page))
    hero_pattern = re.compile(
        r"i\.ytimg\.com%2Fvi%2F(?P<video_id>[A-Za-z0-9_-]{6,20}).{0,2200}?"
        r'creator-profile-module__[^\"]*duration">' r"(?P<duration>\d+:\d{2}(?::\d{2})?)</span>.*?"
        r"<h2>(?P<title>.*?)</h2>",
        re.S,
    )
    matches.extend(hero_pattern.finditer(page))
    for match in matches:
        vid = match.group("video_id")
        if vid in seen:
            continue
        seen.add(vid)
        rows.append(
            {
                "video_id": vid,
                "title": clean(match.group("title")),
                "duration_text": match.group("duration"),
                "youtube_url": f"https://www.youtube.com/watch?v={vid}",
                "thumbnail_url": f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg",
                "source": SOURCE,
                "availability_note": "Original YouTube account reported terminated; media unavailable through tested public endpoints.",
            }
        )
    return rows


def main() -> None:
    rows = collect()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Future Frame Movies partial catalog",
        "",
        "Source: Hollywood.ai creator page. The original YouTube channel appears terminated as of 2026-11-26; direct yt-dlp says the account was terminated, and tested Piped-compatible endpoints failed. This catalog preserves titles/durations/thumbnails but cannot supply reliable public view counts or full-media analysis.",
        "",
        "| video | duration | title |",
        "|---|---:|---|",
    ]
    for row in rows:
        lines.append(f"| `{row['video_id']}` | {row['duration_text']} | {row['title']} |")
    MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} rows")


if __name__ == "__main__":
    main()
