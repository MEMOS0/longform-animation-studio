"""Dialogue craft heuristics derived from cohort evidence.

Transparent writing-quality checks, not acting/subtext measurement. The goal is
to flag exposition-heavy or powerless lines before production.
"""
from __future__ import annotations

import re
from typing import Any

EXPOSITION_MARKERS = [
    "as you know", "remember when", "years ago", "long ago", "the prophecy", "our world", "the kingdom", "let me explain", "you see", "i have to tell you", "it is written", "legend says",
]
POWER_ACTION_MARKERS = [
    "choose", "refuse", "promise", "hide", "protect", "expose", "leave", "stay", "trust", "prove", "save", "give", "take", "stop", "help", "fight", "let", "won't", "can't",
]
CARE_PRESSURE_MARKERS = [
    "afraid", "hurt", "safe", "sorry", "hate", "love", "child", "mother", "father", "kill", "threat", "protect", "save", "shame", "mock", "trust",
]


def critique_lines(lines: list[str], max_exposition_sentences: int | None = None) -> dict[str, Any]:
    rows = []
    exposition_count = 0
    action_count = 0
    long_count = 0
    for line in lines:
        low = line.lower()
        words = re.findall(r"[\w']+", low)
        exposition_hits = [m for m in EXPOSITION_MARKERS if m in low]
        action_hits = [m for m in POWER_ACTION_MARKERS if re.search(r"\b" + re.escape(m) + r"\b", low)]
        care_hits = [m for m in CARE_PRESSURE_MARKERS if m in low]
        long = len(words) > 18
        exposition_count += bool(exposition_hits)
        action_count += bool(action_hits)
        long_count += long
        rows.append({
            "line": line,
            "word_count": len(words),
            "exposition_markers": exposition_hits,
            "power_action_markers": action_hits,
            "care_pressure_markers": care_hits,
            "risks": (["long line may reduce microdrama/mobile clarity"] if long else []) + (["explicit exposition marker"] if exposition_hits else []),
        })
    warnings: list[str] = []
    if lines and action_count == 0:
        warnings.append("sampled key lines contain no clear power/action verb")
    if lines and exposition_count >= max(2, len(lines) // 2):
        warnings.append("sampled key lines are exposition-heavy")
    if max_exposition_sentences is not None and exposition_count > max_exposition_sentences:
        warnings.append("explicit exposition count exceeds scene allowance")
    if lines and long_count == len(lines) and len(lines) > 1:
        warnings.append("all sampled key lines are long; add short power-turn lines")
    return {
        "line_count": len(lines),
        "exposition_line_count": exposition_count,
        "power_action_line_count": action_count,
        "long_line_count": long_count,
        "lines": rows,
        "warnings": warnings,
        "evidence_boundary": "These are sentence-shape heuristics; they cannot measure performance, subtext, acting, or visual emotion.",
    }


def evaluate_scenes_dialogue(scenes: list[dict[str, Any]]) -> dict[str, Any]:
    scene_rows = []
    all_warnings: dict[str, list[str]] = {}
    for scene in scenes:
        design = scene.get("dialogue_design", {})
        result = critique_lines(design.get("key_lines", []), design.get("max_exposition_sentences"))
        beats = design.get("opposition_beats") or []
        beat_names = {beat.get("beat") for beat in beats if isinstance(beat, dict)}
        missing_beats = [name for name in ("external_pressure", "witness_objection", "protagonist_decision", "evidence_or_cost") if name not in beat_names]
        if missing_beats:
            result["warnings"] = list(result["warnings"]) + ["dialogue opposition scaffold missing beats: " + ", ".join(missing_beats)]
        scene_rows.append({"scene_id": scene.get("scene_id"), "opposition_beat_count": len(beats), **{k: result[k] for k in ("line_count", "exposition_line_count", "power_action_line_count", "long_line_count", "warnings")}})
        if result["warnings"]:
            all_warnings[scene.get("scene_id", "<missing>")] = result["warnings"]
    return {"scenes": scene_rows, "warnings_by_scene": all_warnings}
