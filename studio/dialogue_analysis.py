"""Transparent dialogue/narration style metrics from aligned subtitles.

These metrics describe sentence shape and explicit language only. They do not measure
performance quality, subtext, or emotional truth by themselves.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Any

WORD_RE = re.compile(r"[A-Za-z']+")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]+|[^.!?]+$")
EXPOSITION_MARKERS = (
    "because", "since", "as you know", "it is said", "legend", "kingdom", "clan", "bloodline",
    "centuries", "ancient", "prophecy", "chosen", "royal family", "council", "rule", "law",
)
PRESSURE_MARKERS = ("don't", "stop", "never", "shut up", "get out", "kneel", "die", "kill", "worthless", "filthy", "pathetic")
CARE_MARKERS = ("sorry", "thank you", "stay", "home", "family", "protect", "safe", "love", "care", "don't cry", "it's okay")


def sentences(text: str) -> list[str]:
    return [part.strip() for part in SENTENCE_RE.findall(text) if part.strip()]


def words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def window_text(cues: list[dict[str, Any]], start: float, end: float) -> str:
    return " ".join(cue["text"] for cue in cues if cue["start"] < end and cue["end"] > start)


def analyze_text(text: str) -> dict[str, Any]:
    units = sentences(text)
    lengths = [len(words(unit)) for unit in units]
    starts = Counter(" ".join(words(unit)[:3]) for unit in units if len(words(unit)) >= 3)
    lower = text.lower()
    word_count = sum(lengths)
    return {
        "word_count": word_count,
        "sentence_count": len(units),
        "avg_sentence_words": (sum(lengths) / len(lengths)) if lengths else 0,
        "long_sentence_ratio": sum(1 for length in lengths if length >= 22) / max(len(lengths), 1),
        "question_ratio": sum(1 for unit in units if "?" in unit) / max(len(units), 1),
        "exclamation_ratio": sum(1 for unit in units if "!" in unit) / max(len(units), 1),
        "exposition_marker_per_1000_words": sum(lower.count(marker) for marker in EXPOSITION_MARKERS) * 1000 / max(word_count, 1),
        "pressure_marker_per_1000_words": sum(lower.count(marker) for marker in PRESSURE_MARKERS) * 1000 / max(word_count, 1),
        "care_marker_per_1000_words": sum(lower.count(marker) for marker in CARE_MARKERS) * 1000 / max(word_count, 1),
        "repeated_sentence_starts": [
            {"start": start, "count": count} for start, count in starts.most_common(5) if count > 1
        ],
    }


def analyze_cues(cues: list[dict[str, Any]]) -> dict[str, Any]:
    duration = max((cue["end"] for cue in cues), default=0)
    opening = analyze_text(window_text(cues, 0, min(300, duration)))
    middle = analyze_text(window_text(cues, 300, max(duration - 600, 300)))
    ending = analyze_text(window_text(cues, max(duration - 600, 0), duration + 1))
    full = analyze_text(" ".join(cue["text"] for cue in cues))
    return {"duration_seconds": duration, "opening_5min": opening, "middle": middle, "final_10min": ending, "full": full}
