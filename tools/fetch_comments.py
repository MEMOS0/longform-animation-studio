"""Fetch first-page public comments through a Piped-compatible API and aggregate audience signals.

Raw comments are local evidence artifacts; committed outputs should be aggregate counts or
short, necessary excerpts rather than a full redistribution of user comments.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import urllib.request
from collections import Counter
from pathlib import Path

API = "https://maxtube-api.lawrie.co.nz"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/131 Safari/537.36"

THEMES = {
    "loved_story_or_emotion": ["love it", "loved it", "good story", "best story", "cry", "cried", "emotional", "heart", "sweet", "cute"],
    "family_friendly_or wholesome": ["family can watch", "no sexual", "wholesome", "good wins", "sweet"],
    "wants_part_two": ["part 2", "part two", "sequel", "next part", "continue"],
    "character_relationship_praise": ["sister", "brother", "family", "dad", "mom", "protect", "love how", "relationship"],
    "villain_or_justice_reaction": ["evil", "villain", "karma", "revenge", "punish", "slap", "hate"],
    "confusion_or_logic_complaint": ["confused", "doesn't make sense", "plot hole", "why would", "why did", "logic"],
    "ai_or_production_artifact": ["ai ", "ai movie", "animation", "voice", "lip", "inconsisten", "artifact", "weird"],
    "pacing_or_length_complaint": ["boring", "too long", "dragged", "slow", "repetitive", "skip"],
    "sexual_content_or_coercion": ["sexual", "rape", "forced", "slave", "bed", "kiss"],
}


def fetch_comments(video_id: str) -> dict:
    url = f"{API}/comments/{video_id}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    data = json.loads(urllib.request.urlopen(req, timeout=45).read())
    comments = []
    for item in data.get("comments", []):
        text = html.unescape(item.get("commentText") or "")
        comments.append({
            "author": item.get("author"),
            "text": text,
            "likeCount": item.get("likeCount") or 0,
            "replyCount": item.get("replyCount") or 0,
            "commentedTime": item.get("commentedTime"),
            "pinned": bool(item.get("pinned")),
            "hearted": bool(item.get("hearted")),
        })
    return {"video_id": video_id, "commentCount": data.get("commentCount"), "disabled": data.get("disabled"), "comments": comments}


def aggregate(video_payloads: list[dict]) -> dict:
    videos = {}
    corpus = Counter()
    weighted = Counter()
    for payload in video_payloads:
        counts = Counter()
        likes = Counter()
        for comment in payload.get("comments", []):
            lower = comment["text"].lower()
            for theme, needles in THEMES.items():
                if any(needle in lower for needle in needles):
                    counts[theme] += 1
                    likes[theme] += int(comment.get("likeCount") or 0)
                    corpus[theme] += 1
                    weighted[theme] += int(comment.get("likeCount") or 0)
        videos[payload["video_id"]] = {
            "commentCount": payload.get("commentCount"),
            "sampled_comments": len(payload.get("comments", [])),
            "theme_comment_counts": dict(counts),
            "theme_like_weighted_counts": dict(likes),
            "top_comments_brief": [
                {"text": c["text"][:220], "likeCount": c["likeCount"]}
                for c in sorted(payload.get("comments", []), key=lambda x: -x.get("likeCount", 0))[:5]
            ],
        }
    return {"videos": videos, "archive_theme_comment_counts": dict(corpus), "archive_theme_like_weighted_counts": dict(weighted), "method_note": "First-page comments only; themes are keyword proxies and not sentiment-validated."}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-jsonl", default="data/raw/novdrama_archive.jsonl")
    parser.add_argument("--raw-dir", default="data/raw/comments")
    parser.add_argument("--output", default="data/processed/novdrama_comment_signals.json")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    rows = [json.loads(line) for line in Path(args.archive_jsonl).read_text(encoding="utf-8").splitlines() if line.strip()]
    raw_dir = Path(args.raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    payloads = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        future_map = {pool.submit(fetch_comments, row["video_id"]): row["video_id"] for row in rows}
        for future in concurrent.futures.as_completed(future_map):
            video_id = future_map[future]
            try:
                payload = future.result()
            except Exception as exc:
                payload = {"video_id": video_id, "error": repr(exc), "comments": []}
            (raw_dir / f"{video_id}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            payloads.append(payload)
            print(video_id, len(payload.get("comments", [])), payload.get("error", ""), flush=True)
    result = aggregate(payloads)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
