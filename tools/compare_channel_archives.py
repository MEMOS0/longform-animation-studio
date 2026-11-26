"""Build per-channel hit/middle/failure comparisons from collected Piped rows."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def classify_format(row):
    title = (row.get("title") or "").lower()
    duration = row.get("duration_seconds") or 0
    if row.get("is_short") or duration < 240:
        return "short_or_teaser"
    if any(k in title for k in ("season", "episode", "part")):
        return "series_or_part"
    return "standalone_film"


def classify_genre(row):
    title = (row.get("title") or "").lower()
    if any(k in title for k in ("sinbad", "aladdin", "jason", "argonaut", "odyssey", "thor", "persia", "babylon", "arabian night")):
        return "mythic_adventure"
    if any(k in title for k in ("reborn", "beautiful", "changed", "pretended", "maid", "frog")):
        return "transformation_melodrama"
    if any(k in title for k in ("dragon", "mermaid", "siren", "werewolf", "wolf", "vampire", "kingdom")):
        return "fantasy_creature"
    if any(k in title for k in ("alien", "sci-fi", "planet", "space", "war", "pilot")):
        return "science_fiction"
    if any(k in title for k in ("wife", "husband", "bride", "divorce", "married", "love")):
        return "romantic_family_drama"
    if any(k in title for k in ("monster", "demon", "horror", "curse", "tomb")):
        return "monster_horror"
    return "general_emotional_drama"


def duration_bucket(row):
    minutes = (row.get("duration_seconds") or 0) / 60
    if minutes < 15:
        return "under_15m"
    if minutes < 30:
        return "15_30m"
    if minutes < 60:
        return "30_60m"
    if minutes <= 130:
        return "60_120m"
    return "over_130m"


def analyze_file(path: Path, snapshot: datetime) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for row in data.get("videos", []):
        if not row.get("uploaded_ms") or row.get("views") is None:
            continue
        published = datetime.fromtimestamp(row["uploaded_ms"] / 1000, tz=timezone.utc)
        age = max(0.25, (snapshot - published).total_seconds() / 86400)
        enriched = dict(row)
        enriched["published_date"] = published.date().isoformat()
        enriched["age_days"] = age
        enriched["views_per_day"] = row["views"] / age
        enriched["duration_minutes"] = (row.get("duration_seconds") or 0) / 60
        enriched["format"] = classify_format(row)
        enriched["genre"] = classify_genre(row)
        enriched["duration_bucket"] = duration_bucket(row)
        rows.append(enriched)
    rows.sort(key=lambda x: x["views_per_day"], reverse=True)
    n = len(rows)
    for i, row in enumerate(rows):
        row["rank_by_views_per_day"] = i + 1
        row["within_channel_cohort"] = "outperforming" if i < max(1, n // 3) else ("underperforming" if i >= n - max(1, n // 3) else "middle")
    return {"channel": data.get("channel", {}), "videos": rows, "snapshot_date": snapshot.date().isoformat()}


def render(report: dict) -> str:
    ch = report["channel"]
    lines = [f"# {ch.get('name')} — within-channel comparison", "", f"Snapshot: {report['snapshot_date']}; subscribers at collection: {ch.get('subscriberCount')}", "", "| rank | cohort | views/day | views | age d | length | format | genre | title |", "|---:|---|---:|---:|---:|---:|---|---|---|"]
    for r in report["videos"]:
        lines.append(f"| {r['rank_by_views_per_day']} | {r['within_channel_cohort']} | {r['views_per_day']:.0f} | {r['views']} | {r['age_days']:.1f} | {r['duration_minutes']:.0f}m | {r['format']} | {r['genre']} | {(r.get('title') or '').replace('|','/')} |")
    lines.append("\nPublic views are discovery evidence only; this is not CTR or retention causality.\n")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/raw/channels")
    parser.add_argument("--output-dir", default="data/processed/channel_comparisons")
    args = parser.parse_args()
    snapshot = datetime.now(timezone.utc)
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    summary = []
    for path in sorted(Path(args.input_dir).glob("*.json")):
        report = analyze_file(path, snapshot)
        stem = path.stem
        (outdir / f"{stem}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        (outdir / f"{stem}.md").write_text(render(report), encoding="utf-8")
        summary.append({"channel": report["channel"].get("name"), "videos": len(report["videos"]), "subscribers": report["channel"].get("subscriberCount"), "file": f"{stem}.md"})
    (outdir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"channels": len(summary), "videos": sum(x["videos"] for x in summary)}))


if __name__ == "__main__":
    main()
