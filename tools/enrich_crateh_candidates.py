"""Enrich Crateh candidates with public Piped stream metadata."""

import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "data" / "raw" / "crateh_7d_rankings.json"
OUT = ROOT / "data" / "processed" / "crateh_7d_candidates_enriched.json"
MD = ROOT / "knowledge" / "market" / "crateh-breakout-candidates.md"
BASE = "https://maxtube-api.lawrie.co.nz/streams/"


def fetch(video_id: str) -> dict:
    try:
        req = urllib.request.Request(BASE + video_id, headers={"User-Agent": "Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=20).read())
        uploaded = data.get("uploaded")
        upload_date = ""
        if isinstance(uploaded, (int, float)):
            upload_date = datetime.fromtimestamp(uploaded / 1000, tz=timezone.utc).date().isoformat()
        return {
            "total_views": data.get("views"),
            "upload_date": upload_date,
            "channel_id": (data.get("uploaderUrl") or "").rsplit("/", 1)[-1],
            "subscriber_count": data.get("uploaderSubscriberCount"),
            "piper_title": data.get("title"),
            "metadata_status": "ok",
        }
    except Exception as exc:
        return {"metadata_status": type(exc).__name__ + ": " + str(exc)[:100]}


def main() -> None:
    rows = json.loads(IN.read_text(encoding="utf-8"))
    enriched = []
    for row in rows:
        merged = dict(row)
        merged.update(fetch(row["video_id"]))
        enriched.append(merged)
        time.sleep(0.3)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Crateh 7-day ranking candidates",
        "",
        "Collected 2026-11-26 from `https://crateh.com/ko?period=7d`, enriched with public Piped stream metadata. Views in the Crateh column are rolling-window ranking figures; total views/subscribers are current public metadata. These are candidates, not proven breakouts.",
        "",
        "| rank | video | creator | subs | upload | total views | 7d rank views | duration | genre | title |",
        "|---:|---|---|---:|---|---:|---:|---:|---|---|",
    ]
    for r in enriched:
        lines.append(
            f"| {r['rank']} | `{r['video_id']}` | {r['creator']} | {r.get('subscriber_count','')} | {r.get('upload_date','')} | {r.get('total_views','')} | {r['views_text']} | {r['duration_text']} | {r['genre_text']} | {r['title']} |"
        )
    MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("enriched", len(enriched))


if __name__ == "__main__":
    main()
