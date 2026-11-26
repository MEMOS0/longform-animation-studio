"""Transparent story-signal extraction for audiovisual casebooks.

These lexicons are measurement aids, not proof of story quality. They are deliberately
simple and inspectable so future agents can challenge or extend them with evidence.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

WORD_RE = re.compile(r"[A-Za-z']+")

SIGNAL_PATTERNS: dict[str, tuple[str, ...]] = {
    "wound_or_humiliation": (
        "abandon", "alone", "beg", "betray", "burden", "cry", "curse", "die", "death", "filthy",
        "freak", "humiliat", "kill", "monster", "orphan", "pathetic", "poor", "reject", "slave",
        "suffer", "thief", "useless", "weak", "worthless",
    ),
    "care_belonging_protection": (
        "adopt", "belong", "care", "come with", "family", "friend", "home", "kind", "love", "protect",
        "safe", "save", "stay with", "thank you", "welcome",
    ),
    "justice_reversal_payoff": (
        "apolog", "arrest", "confess", "crown", "evidence", "expose", "guilty", "inherit", "kneel",
        "liar", "pay for", "punish", "revenge", "take back", "truth", "victory", "win",
    ),
    "romance_bond_or_coercion": (
        "bond", "bride", "claim", "crush", "fiance", "husband", "kiss", "marry", "mate", "mine",
        "romance", "wife",
    ),
    "lore_mythology_density": (
        "alpha", "bloodline", "clan", "council", "curse", "destiny", "dragon", "elder", "emperor",
        "goddess", "heir", "kingdom", "magic", "omega", "pack", "power", "prophecy", "pureblood",
        "queen", "realm", "royal", "sacred", "spell", "throne", "tribe", "warrior",
    ),
    "threat_or_violence": (
        "attack", "blood", "burn", "death", "die", "execute", "fight", "hurt", "kill", "murder",
        "pain", "punish", "slaughter", "threat", "war", "wound",
    ),
}

CATEGORIES = tuple(SIGNAL_PATTERNS)


def words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def count_signal(text: str, category: str) -> int:
    lower = text.lower()
    return sum(lower.count(pattern) for pattern in SIGNAL_PATTERNS[category])


def first_signal(cues: list[dict[str, Any]], category: str) -> dict[str, Any] | None:
    patterns = SIGNAL_PATTERNS[category]
    for cue in cues:
        lower = cue["text"].lower()
        if any(pattern in lower for pattern in patterns):
            return {"time": cue.get("start"), "text": cue.get("text", "")[:140]}
    return None


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8", newline="") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def mean(values: list[float | int | None]) -> float | None:
    clean = [float(v) for v in values if v is not None]
    return sum(clean) / len(clean) if clean else None


def window_text(rows: list[dict[str, Any]], start: float, end: float) -> str:
    return " ".join(row.get("dialogue_text") or "" for row in rows if row.get("start", 0) < end and row.get("end", 0) > start)


def short_quote(text: str, max_words: int = 12) -> str:
    tokens = re.findall(r"\S+", re.sub(r"\s+", " ", text).strip())
    return " ".join(tokens[:max_words])


def aggregate_windows(timeline_rows: list[dict[str, Any]], window_seconds: int = 300) -> list[dict[str, Any]]:
    if not timeline_rows:
        return []
    duration = max(row.get("end", 0) for row in timeline_rows)
    windows = []
    for start in range(0, int(duration), window_seconds):
        end = min(start + window_seconds, duration)
        rows = [row for row in timeline_rows if row.get("start", 0) < end and row.get("end", 0) > start]
        text = " ".join(row.get("dialogue_text") or "" for row in rows)
        counts = {category: count_signal(text, category) for category in CATEGORIES}
        snippets = []
        for row in rows:
            dialogue = (row.get("dialogue_text") or "").strip()
            if dialogue and len(snippets) < 2:
                snippets.append({"time": row.get("start"), "quote": short_quote(dialogue)})
        windows.append(
            {
                "start": start,
                "end": end,
                "signal_counts": counts,
                "dialogue_words": len(words(text)),
                "shot_boundaries": sum(int(row.get("shot_boundary_count") or 0) for row in rows),
                "visual": {
                    "brightness": mean([(row.get("visual_mean") or {}).get("brightness") for row in rows]),
                    "saturation": mean([(row.get("visual_mean") or {}).get("saturation") for row in rows]),
                    "colorfulness": mean([(row.get("visual_mean") or {}).get("colorfulness") for row in rows]),
                    "motion": mean([(row.get("visual_mean") or {}).get("motion_mean_abs_diff") for row in rows]),
                },
                "audio": {
                    "rms_mean": mean([row.get("audio_rms_mean") for row in rows]),
                    "rms_std": mean([row.get("audio_rms_std") for row in rows]),
                    "silence_ratio": mean([row.get("audio_silence_ratio") for row in rows]),
                    "onsets_per_second": mean([row.get("audio_onsets_per_second") for row in rows]),
                },
                "evidence_snippets": snippets,
            }
        )
    return windows


def summarize_story_signals(video_id: str, timeline_rows: list[dict[str, Any]], cues: list[dict[str, Any]] | None = None, window_seconds: int = 300) -> dict[str, Any]:
    cues = cues or []
    windows = aggregate_windows(timeline_rows, window_seconds)
    duration = max((row.get("end") or 0 for row in timeline_rows), default=0)
    full_text = " ".join(row.get("dialogue_text") or "" for row in timeline_rows)
    total_counts = {category: count_signal(full_text, category) for category in CATEGORIES}
    firsts = {category: first_signal(cues, category) for category in CATEGORIES}
    final_rows = [row for row in timeline_rows if row.get("start", 0) >= max(duration - 600, 0)]
    final_text = " ".join(row.get("dialogue_text") or "" for row in final_rows)
    final_counts = {category: count_signal(final_text, category) for category in CATEGORIES}

    def first_time(category: str) -> float | None:
        item = firsts.get(category) or {}
        return item.get("time")

    care_latency = None
    if first_time("care_belonging_protection") is not None and first_time("wound_or_humiliation") is not None:
        care_latency = first_time("care_belonging_protection") - first_time("wound_or_humiliation")

    return {
        "video_id": video_id,
        "duration_seconds": duration,
        "window_seconds": window_seconds,
        "total_signal_counts": total_counts,
        "first_signal_occurrences": firsts,
        "care_after_wound_latency_seconds": care_latency,
        "final_10_minutes_signal_counts": final_counts,
        "windows": windows,
        "interpretation_boundaries": [
            "Signal counts measure explicit dialogue language only; they do not prove emotional quality or causality.",
            "Evidence snippets are short orientation quotes, not a transcript substitute.",
            "Visual/audio metrics are low-resolution proxies and must be paired with direct viewing.",
        ],
    }
