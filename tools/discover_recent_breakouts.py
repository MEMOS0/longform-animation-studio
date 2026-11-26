"""Discover recent low/mid-subscriber AI-film breakout candidates through Piped search.

Search visibility is biased by YouTube/Piped indexing; candidates are leads, not proof.
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://maxtube-api.lawrie.co.nz"
ROOT = Path(__file__).resolve().parents[1]
QUERIES = [
    "AI drama full movie",
    "AI movie full movie fantasy",
    "AI animation movie",
    "dragon full movie AI",
    "mermaid full movie AI",
    "reborn full movie AI drama",
    "werewolf full movie AI drama",
]


def get_json(path: str, timeout=25):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


def video_id(url: str) -> str:
    return url.rsplit("v=", 1)[-1] if "v=" in url else url.rsplit("/", 1)[-1]


def search(query: str) -> list[dict]:
    data = get_json("/search?q=" + urllib.parse.quote(query) + "&filter=videos")
    return data.get("items", [])


def enrich(vid: str) -> dict:
    data = get_json("/streams/" + vid)
    uploaded = data.get("uploaded")
    upload_date = None
    if isinstance(uploaded, (int, float)):
        upload_date = datetime.fromtimestamp(uploaded / 1000, tz=timezone.utc).date().isoformat()
    elif isinstance(uploaded, str):
        upload_date = uploaded[:10]
    return {
        "total_views": data.get("views"),
        "upload_date": upload_date,
        "channel_id": (data.get("uploaderUrl") or "").rsplit("/", 1)[-1],
        "subscriber_count": data.get("uploaderSubscriberCount"),
        "like_count": data.get("likes"),
        "duration_seconds": data.get("duration"),
        "exact_title": data.get("title"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=14)
    parser.add_argument("--max-enrich", type=int, default=35)
    parser.add_argument("--queries", default="", help="comma-separated query override")
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    cutoff = now.timestamp() - args.days * 86400
    found = {}
    queries = [q.strip() for q in args.queries.split(",") if q.strip()] or QUERIES
    for query in queries:
        try:
            rows = search(query)
        except Exception as exc:
            print(json.dumps({"query": query, "error": str(exc)}))
            continue
        for row in rows:
            uploaded_ms = row.get("uploaded") if isinstance(row.get("uploaded"), (int, float)) else row.get("uploadedDate")
            if not isinstance(uploaded_ms, (int, float)) or uploaded_ms / 1000 < cutoff or row.get("isShort"):
                continue
            vid = video_id(row.get("url", ""))
            duration = row.get("duration") or 0
            if duration < 300:
                continue
            item = found.setdefault(vid, {"video_id": vid, "queries": [], "search_title": row.get("title"), "channel": row.get("uploaderName"), "search_views": row.get("views"), "duration_seconds_search": duration, "uploaded_ms": uploaded_ms})
            item["queries"].append(query)
        time.sleep(0.2)
    candidates = sorted(found.values(), key=lambda x: -(x.get("search_views") or 0))[: args.max_enrich]
    enriched = []
    for row in candidates:
        try:
            row.update(enrich(row["video_id"]))
        except Exception as exc:
            row["enrich_error"] = str(exc)
        age_days = max(0.25, (now.timestamp() - row["uploaded_ms"] / 1000) / 86400)
        row["age_days_at_collection"] = round(age_days, 2)
        views = row.get("total_views") or row.get("search_views") or 0
        row["views_per_day_estimate"] = round(views / age_days, 1)
        subs = row.get("subscriber_count")
        row["low_mid_subscriber_flag"] = bool(subs is not None and subs < 100000)
        row["candidate_strength"] = "strong_lead" if row["low_mid_subscriber_flag"] and row["views_per_day_estimate"] > 10000 else ("watchlist" if row["low_mid_subscriber_flag"] else "large_channel_or_unknown")
        enriched.append(row)
        time.sleep(0.2)
    out = ROOT / "data" / "processed" / "recent_breakout_candidates.json"
    out.write_text(json.dumps({"collected_at": now.isoformat(), "days": args.days, "candidates": enriched}, ensure_ascii=False, indent=2), encoding="utf-8")
    md = ROOT / "knowledge" / "market" / "recent-breakout-candidates.md"
    lines = [
        "# Recent AI-film breakout candidates",
        "",
        f"Collected {now.date().isoformat()} through Piped public search for videos uploaded in the last {args.days} days. These are leads, not proof: search indexing/recommendation bias is significant, subscriber counts are current rather than at upload, and public views are not retention/CTR.",
        "",
        "| strength | video | channel | subs | age d | views | views/day | duration | queries | title |",
        "|---|---|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for r in enriched:
        dur = (r.get("duration_seconds") or r.get("duration_seconds_search") or 0) / 60
        lines.append(f"| {r['candidate_strength']} | `{r['video_id']}` | {r.get('channel') or ''} | {r.get('subscriber_count')} | {r['age_days_at_collection']:.1f} | {r.get('total_views') or r.get('search_views')} | {r['views_per_day_estimate']:.0f} | {dur:.0f}m | {', '.join(r['queries'])[:45]} | {(r.get('exact_title') or r.get('search_title') or '').replace('|','/')} |")
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"candidates": len(enriched), "queries": queries, "strong": sum(r["candidate_strength"] == "strong_lead" for r in enriched), "output": str(out)}))


if __name__ == "__main__":
    main()
