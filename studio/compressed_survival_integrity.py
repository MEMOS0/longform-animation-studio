"""Compressed creature-survival doctrine validation.

Checks whether a short visual-first survival package preserves the mechanisms
identified in the Neural Pictures deep dive. Transparent craft heuristics, not a
retention predictor.
"""
from __future__ import annotations

import re
from typing import Any


def flatten(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(flatten(v) for v in value)
    return str(value or "")


def evaluate_compressed_survival_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = flatten(premise).lower()
    arch_text = flatten(architecture).lower()
    scene_text = flatten(scenes).lower()
    full = "\n".join([premise_text, arch_text, scene_text])
    applies = premise.get("channel_contract") == "compressed_creature_survival" or bool(re.search(r"compressed creature.survival|creature.survival|giant predator|survival movie", full))
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    opening = flatten(premise.get("opening_event", {})).lower()
    sequences = architecture.get("sequences") or []
    middle_end = flatten(sequences[3:]).lower() if len(sequences) >= 5 else arch_text
    final = flatten(sequences[-2:]).lower() if sequences else arch_text
    scene_visuals = flatten([scene.get("visual_action", {}) for scene in scenes]).lower()
    scene_sound = flatten([scene.get("sound_design", {}) for scene in scenes]).lower()

    checks = {
        "early_role_creature_location_payoff": bool(re.search(r"wreck|crash|breaks? apart|derail|disaster|predator|giant|creature|threat", opening)),
        "occupational_competence_becomes_plan": bool(re.search(r"conductor|operator|mechanic|pilot|captain|engineer|professional|occupation", full) and re.search(r"panel|wire|brake|horn|lens|foghorn|engine|tool|mechanism|trap|vehicle|station", middle_end)),
        "predator_and_innocent_or_ally_are_differentiated": bool(re.search(r"predator", full) and re.search(r"innocent animal|small animal|creature ally|allied creature|ally_creature", full)),
        "quiet_animal_care_hinge": bool(re.search(r"quiet|lowest-density|music withdraws|small animal|animal vocalization|protects? .*animal|care", scene_sound + " " + arch_text)),
        "escape_converts_to_reciprocal_rescue": bool(re.search(r"escape.*rescue|turns? back|rescue obligation|captives|survivors.*trapped|free captives|reciprocal rescue", middle_end + " " + premise_text)),
        "opening_vehicle_or_object_reused_in_climax": bool(re.search(r"vehicle|station|train|lighthouse|ferry|object|lens|key", final) and re.search(r"trap|mechanism|rescue|light|sound|gate|engine|foghorn", final)),
        "contact_or_recognition_closure": bool(re.search(r"contact|recognition|free|freed|return|home|belonging|apolog", final)),
        "muted_visual_intelligibility": bool(re.search(r"visual objective|sound off|muted|first_image|final_image", full) and len(scene_visuals) > 300),
    }
    warnings = []
    labels = {
        "early_role_creature_location_payoff": "opening does not pay the role/creature/location survival contract early",
        "occupational_competence_becomes_plan": "occupational identity does not become a concrete survival/trap plan",
        "predator_and_innocent_or_ally_are_differentiated": "creature ecosystem is not morally differentiated",
        "quiet_animal_care_hinge": "no quiet animal/creature-care hinge after spectacle",
        "escape_converts_to_reciprocal_rescue": "escape does not convert into reciprocal rescue",
        "opening_vehicle_or_object_reused_in_climax": "opening vehicle/station/object is not reused as climax machinery",
        "contact_or_recognition_closure": "ending does not close through contact, recognition, freedom, or return",
        "muted_visual_intelligibility": "scene package does not demonstrate muted visual intelligibility",
    }
    for key, ok in checks.items():
        if not ok:
            warnings.append(labels[key])
    score = sum(checks.values()) / len(checks)
    return {
        "applies": True,
        "score_0_to_1": round(score, 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Compressed creature survival should pay a legible role/creature/location contract early, build muted visual objectives, differentiate predator from vulnerable/cooperative life, use occupational competence as climax machinery, convert escape into reciprocal rescue, and close through recognition/contact rather than explosion alone.",
    }
