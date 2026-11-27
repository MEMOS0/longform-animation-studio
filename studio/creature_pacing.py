"""Creature-fantasy pacing integrity from fresh breakout evidence.

The goal is not universal fast cutting. Atmospheric creature fantasy can use
slow composed shots, but spectacle should build into contact/recognition and
the ending should return to quieter relational/material resolution.
"""
from __future__ import annotations

from typing import Any

from .compound_expansion import _flat

CREATURE_TERMS = ["creature", "dragon", "wolf", "monster", "animal", "beast"]
SPECTACLE_TERMS = ["battle", "attack", "execution", "fire", "flight", "war", "chains", "crowd", "roar", "scale", "spectacle"]
QUIET_TERMS = ["silence", "quiet", "breath", "contact", "touch", "embrace", "nest", "home", "recognition", "negative space", "room tone", "wind", "snow", "water"]
LOUD_CONSTANT_TERMS = ["constant music", "loud throughout", "wallpaper", "generic epic"]


def evaluate_creature_pacing(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    combined = "\n".join([_flat(premise), _flat(architecture), _flat(scenes)]).lower()
    applicable = any(term in combined for term in CREATURE_TERMS)
    if not applicable or not scenes:
        return {"applicable": applicable, "score_0_to_1": 0.0 if applicable else 1.0, "warnings": [] if not applicable else ["creature pacing cannot be evaluated without scenes"], "strengths": []}

    def minute_mid(scene: dict[str, Any]) -> float:
        import re
        match = re.search(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)", str(scene.get("time_range", "")))
        return (float(match.group(1)) + float(match.group(2))) / 2 if match else 0.0

    ordered = sorted(scenes, key=minute_mid)
    total_mid = minute_mid(ordered[-1])
    spectacle_scenes = [s for s in ordered if any(term in _flat(s).lower() for term in SPECTACLE_TERMS)]
    final = ordered[-1]
    final_text = _flat(final).lower()
    warnings: list[str] = []
    strengths: list[str] = []

    first = ordered[0]
    first_text = _flat(first).lower()
    if not any(term in first_text for term in ["care", "feed", "warm", "hide", "protect", "touch", "creature", "labor", "cold", "heat"]):
        warnings.append(f"{first.get('scene_id')}: opening does not establish creature care/vulnerability or material cold-heat stakes early")
    else:
        strengths.append("opening grounds creature spectacle in care/vulnerability or material stakes")

    if spectacle_scenes:
        last_spectacle = spectacle_scenes[-1]
        if minute_mid(last_spectacle) >= total_mid and not any(term in final_text for term in QUIET_TERMS):
            warnings.append("spectacle occupies the ending without a quiet relational/material resolution tail")
        else:
            strengths.append("spectacle is followed by a resolution movement")
    else:
        warnings.append("no legible creature spectacle/escalation block detected")

    if not any(term in final_text for term in QUIET_TERMS):
        warnings.append(f"{final.get('scene_id')}: final scene lacks quiet contact, breath, nest/home, recognition, or negative-space sound planning")
    else:
        strengths.append("final scene plans quiet contact/recognition/negative-space resolution")

    if any(term in final_text for term in LOUD_CONSTANT_TERMS):
        warnings.append(f"{final.get('scene_id')}: final sound design remains loud/generic rather than returning to breath/room tone/recognition")

    score = max(0.0, 1.0 - 0.25 * len(warnings))
    return {
        "applicable": True,
        "score_0_to_1": round(score, 2),
        "warnings": warnings,
        "strengths": sorted(set(strengths)),
        "craft_rule": "Creature fantasy may use slow composed shots; the required rhythm is care/material stakes -> staged spectacle -> quiet contact/recognition/home resolution, not uniformly fast cutting.",
    }
