"""Scene time-range coverage helpers for draft-completeness gates."""
from __future__ import annotations

import re
from typing import Any


def minutes_range(value: str) -> tuple[float, float] | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)", value)
    if not match:
        return None
    return float(match.group(1)), float(match.group(2))


def architecture_end_minutes(architecture: dict[str, Any]) -> float:
    ends = []
    for seq in architecture.get("sequences", []) if isinstance(architecture, dict) else []:
        parsed = minutes_range(str(seq.get("time_range", "")))
        if parsed:
            ends.append(parsed[1])
    return max(ends, default=0.0)


def scene_time_coverage(scenes: list[dict[str, Any]], expected_minutes: float) -> dict[str, Any]:
    intervals = []
    for scene in scenes:
        parsed = minutes_range(str(scene.get("time_range", "")))
        if parsed and parsed[1] > parsed[0]:
            intervals.append(parsed)
    intervals.sort()
    merged: list[list[float]] = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    covered = sum(end - start for start, end in merged)
    max_end = max((end for _, end in merged), default=0.0)
    ratio = min(covered / expected_minutes, 1.0) if expected_minutes else 1.0
    finale_covered = not expected_minutes or max_end >= expected_minutes - 0.05
    return {
        "coverage_ratio": ratio,
        "covered_minutes": round(covered, 3),
        "max_end_minutes": max_end,
        "expected_minutes": expected_minutes,
        "finale_covered": finale_covered,
        "complete": bool(expected_minutes and ratio >= 0.98 and finale_covered),
    }
