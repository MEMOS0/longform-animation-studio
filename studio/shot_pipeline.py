"""Shot-level production planning for long-form AI animation.

The goal is not to generate a whole film in one pass. Scenes are decomposed into
shots with draft/mid/hero lanes, explicit continuity dependencies, and a planned
generation-to-final ratio so budget and quality remain measurable.
"""
from __future__ import annotations

import re
from typing import Any


def parse_minutes_range(value: str) -> tuple[float, float] | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)", str(value))
    if not match:
        return None
    return float(match.group(1)), float(match.group(2))


def lane_for_shot(kind: str, text: str) -> str:
    low = text.lower()
    if kind in {"final_image", "memory_or_revelation"} or any(k in low for k in ("dragon", "creature", "storm", "transformation", "public", "reveal")):
        return "hero"
    if kind in {"power_transition", "dialogue_action"}:
        return "mid"
    return "draft"


def shots_for_scene(scene: dict[str, Any]) -> list[dict[str, Any]]:
    sid = scene.get("scene_id", "scene")
    visual = scene.get("visual_action", {})
    objective = scene.get("objective", "")
    conflict = scene.get("conflict", "")
    decision = scene.get("protagonist_decision", "")
    turn = scene.get("turn", "")
    base = [
        ("establishing", visual.get("first_image", objective), 4.0),
        ("face_reaction", visual.get("face_reaction", conflict), 3.0),
        ("dialogue_action", objective + " " + conflict, 6.0),
        ("power_transition", decision + " " + turn, 5.0),
        ("final_image", visual.get("final_image", turn), 4.0),
    ]
    shots = []
    for index, (kind, description, seconds) in enumerate(base, 1):
        lane = lane_for_shot(kind, str(description))
        shots.append({
            "shot_id": f"{sid}_SHOT{index:02d}",
            "scene_id": sid,
            "kind": kind,
            "duration_seconds": seconds,
            "generation_lane": lane,
            "visual_prompt_intent": str(description),
            "continuity_dependencies": continuity_dependencies(scene, kind),
            "reuse_before_generate": kind in {"establishing", "face_reaction"},
        })
    return shots


def continuity_dependencies(scene: dict[str, Any], kind: str) -> list[str]:
    text = " ".join(str(x) for x in [scene.get("objective", ""), scene.get("conflict", ""), scene.get("turn", ""), scene.get("visual_action", {})]).lower()
    deps = ["protagonist_face_and_costume", "scene_lighting_palette"]
    if any(k in text for k in ("creature", "dragon", "wolf", "monster", "child")):
        deps.append("creature_or_child_model_sheet")
    if any(k in text for k in ("storm", "fire", "ice", "water", "city", "cave", "ship", "island")):
        deps.append("environment_reference_plate")
    if kind in {"dialogue_action", "power_transition"}:
        deps.append("shot_reverse_shot_eye_line")
    return sorted(set(deps))


def build_shot_plan(scenes: list[dict[str, Any]], target_minutes: float | int | None = None) -> dict[str, Any]:
    shots = [shot for scene in scenes for shot in shots_for_scene(scene)]
    lane_counts: dict[str, int] = {}
    lane_seconds: dict[str, float] = {}
    for shot in shots:
        lane_counts[shot["generation_lane"]] = lane_counts.get(shot["generation_lane"], 0) + 1
        lane_seconds[shot["generation_lane"]] = round(lane_seconds.get(shot["generation_lane"], 0.0) + shot["duration_seconds"], 2)
    covered = 0.0
    for scene in scenes:
        parsed = parse_minutes_range(scene.get("time_range", ""))
        if parsed:
            covered += parsed[1] - parsed[0]
    final_seconds = (float(target_minutes) if target_minutes else covered) * 60.0
    planned_generated_seconds = round(sum(shot["duration_seconds"] for shot in shots), 2)
    ratio = round(planned_generated_seconds / final_seconds, 4) if final_seconds else None
    return {
        "shot_count": len(shots),
        "planned_generated_seconds": planned_generated_seconds,
        "estimated_final_seconds": round(final_seconds, 2),
        "planned_generated_to_final_ratio": ratio,
        "lane_counts": lane_counts,
        "lane_seconds": lane_seconds,
        "shots": shots,
        "coverage_scope": "key_shots_only",
        "coverage_gap_seconds": round(max(0.0, final_seconds - planned_generated_seconds), 2),
        "warnings": ["shot list covers key dramatic beats, not every final second; full pre-production must expand each scene into continuous shot coverage"] if planned_generated_seconds < final_seconds * 0.5 else [],
        "production_rules": [
            "Generate character/creature/location reference sheets before motion shots.",
            "Expand key beats into full continuous shot coverage before any paid generation.",
            "Use draft lane for blocking and reuse valid inserts/plates rather than regenerating everything.",
            "Use hero lane only for emotional payoff, creature transformation, revelation, and final-image shots.",
            "Track actual generated seconds separately; iteration ratio is a production KPI, not a creative afterthought.",
        ],
    }
