"""Validation for exact continuous storyboard drafts."""
from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any


def parse_timecode(value: str) -> tuple[float, float]:
    start, end = value.split("-", 1)
    return float(start), float(end)


def validate_storyboard(data: dict[str, Any]) -> dict[str, Any]:
    shots = data.get("shots", [])
    errors: list[str] = []
    warnings: list[str] = []
    cursor = 0.0
    total = 0.0
    hero_count = 0
    durations: list[float] = []
    for shot in shots:
        try:
            start, end = parse_timecode(shot["timecode"])
        except Exception as exc:
            errors.append(f"{shot.get('shot_id','unknown')}: invalid timecode: {exc}")
            continue
        if abs(start - cursor) > 0.01:
            errors.append(f"{shot['shot_id']}: gap or overlap before shot (expected {cursor:.1f}, got {start:.1f})")
        if end <= start:
            errors.append(f"{shot['shot_id']}: non-positive duration")
        cursor = end
        total += end - start
        durations.append(end - start)
        if shot.get("generation_lane") not in {"draft", "mid", "hero"}:
            errors.append(f"{shot['shot_id']}: invalid generation lane")
        for field in ("shot_size", "camera_intent", "visual_action", "sound_design", "continuity_dependencies"):
            if not shot.get(field):
                errors.append(f"{shot['shot_id']}: missing {field}")
        if shot.get("generation_lane") == "hero":
            hero_count += 1
    expected = float(data.get("duration_seconds") or 0)
    if expected and abs(cursor - expected) > 0.5:
        errors.append(f"coverage ends at {cursor:.1f}s, expected {expected:.1f}s")
    if hero_count / max(1, len(shots)) > 0.55:
        warnings.append("hero lane is overused; expensive spectacle may lose contrast and budget discipline")
    if len(durations) >= 8:
        mean_duration = sum(durations) / len(durations)
        variation = statistics.pstdev(durations) / mean_duration if mean_duration else 0.0
        if variation < 0.12:
            warnings.append("shot durations are nearly uniform; pacing lacks acceleration, compression, and lingering emotional contrast")
        if min(durations) < 3.0:
            warnings.append("some shots are too short for readable emotional/action continuity")
        if max(durations) > 45.0:
            warnings.append("some shots are long enough to risk invisibility of cutting rhythm or generative drift")
    if not any("cage" in str(s.get("dialogue", "")).lower() or "trust" in str(s.get("dialogue", "")).lower() for s in shots):
        warnings.append("core protection/trust theme is not explicit in dialogue")
    return {"shot_count": len(shots), "covered_seconds": round(cursor, 2), "hero_shots": hero_count, "errors": errors, "warnings": warnings, "valid": not errors}


def validate_storyboard_file(path: str | Path) -> dict[str, Any]:
    return validate_storyboard(json.loads(Path(path).read_text(encoding="utf-8")))
