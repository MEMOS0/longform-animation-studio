"""Parse Crateh landing-page rolling ranking cards into structured evidence."""

import html
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw" / "crateh_7d_rankings.json"
MD = ROOT / "knowledge" / "market" / "crateh-breakout-candidates.md"
URL = "https://crateh.com/ko?period=7d"


def strip_tags(value: str) -> str:
    return html.unescape(re.sub(r"<.*?>", "", value)).strip()


def parse(page: str) -> list[dict]:
    rows = []
    ranked_start = page.find('<div class="ranked-sections">')
    ranked_end = page.find('<h2 class="sec-title', ranked_start)
    if ranked_end < 0:
        ranked_end = page.find('최신 작품', ranked_start)
    ranked_page = page[ranked_start:ranked_end if ranked_end > ranked_start else len(page)]
    sections = re.split(r'<h2 class="ranked-section-title">', ranked_page)
    for section in sections[1:]:
        format_name = strip_tags(section.split("</h2>", 1)[0])
        for card in re.findall(r"<article class=\"video-card.*?</article>", section, re.S):
            rank_m = re.search(r'video-card-rank num">(\d+)<', card)
            link_m = re.search(r'href="/ko/watch/youtube%3A([A-Za-z0-9_-]{6,20})', card)
            duration_m = re.search(r'video-duration num">([^<]+)</span>', card)
            category_m = re.search(r'video-card-category">(.*?)</p>', card, re.S)
            title_m = re.search(r'video-card-title[^>]*>(.*?)</h3>', card, re.S)
            creator_m = re.search(r'video-card-creator">(.*?)</p>', card, re.S)
            meta_m = re.search(r'video-card-meta num">(.*?)</p>', card, re.S)
            if not link_m or not title_m:
                continue
            creator_bits = [strip_tags(x) for x in re.split(r"<!--\s*-->\s*·\s*<!--\s*-->", creator_m.group(1))] if creator_m else []
            meta_text = strip_tags(meta_m.group(1)) if meta_m else ""
            views_m = re.search(r"조회수\s*([^Y]+?)\s*YouTube", meta_text)
            rows.append(
                {
                    "format_section": format_name,
                    "rank": int(rank_m.group(1)) if rank_m else None,
                    "video_id": link_m.group(1),
                    "duration_text": duration_m.group(1) if duration_m else "",
                    "category": strip_tags(category_m.group(1)) if category_m else "",
                    "title": strip_tags(title_m.group(1)),
                    "creator": creator_bits[0] if creator_bits else "",
                    "genre_text": creator_bits[1] if len(creator_bits) > 1 else "",
                    "views_text": views_m.group(1).strip() if views_m else "",
                    "source_url": URL,
                }
            )
    unique = []
    seen = set()
    for row in rows:
        key = (row["format_section"], row["video_id"])
        if key not in seen:
            seen.add(key)
            unique.append(row)
    return unique


def main() -> None:
    page = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode("utf-8", "ignore")
    rows = parse(page)
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Crateh 7-day ranking candidates",
        "",
        "Collected 2026-11-26 from `https://crateh.com/ko?period=7d`. These are rolling 7-day ranking candidates in the Korean AI-film ecosystem, not verified breakout proof. Channel age, subscriber count, upload date, and repeat performance still require direct validation.",
        "",
        "| section | rank | video | duration | creator | genre | views | title |",
        "|---|---:|---|---:|---|---|---:|---|",
    ]
    for r in rows:
        lines.append(f"| {r['format_section']} | {r['rank']} | `{r['video_id']}` | {r['duration_text']} | {r['creator']} | {r['genre_text']} | {r['views_text']} | {r['title']} |")
    MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} rows")


if __name__ == "__main__":
    main()
