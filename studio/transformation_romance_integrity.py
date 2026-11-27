"""Transformation-romance doctrine validation.

Transparent craft checks derived from the EchoDrama Hidden Beauty deep dive.
These are not predictions of CTR or retention.
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


def evaluate_transformation_romance_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = flatten(premise).lower()
    arch_text = flatten(architecture).lower()
    scene_text = flatten(scenes).lower()
    full = "\n".join([premise_text, arch_text, scene_text])
    applies = premise.get("channel_contract") == "transformation_romance" or bool(re.search(r"transformation romance|hidden beauty|pre.transformation witness|gaze inversion", full))
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    sequences = architecture.get("sequences") or []
    expected_scene_count = len(sequences)
    scene_keys = []
    for index, scene in enumerate(scenes):
        scene_keys.append(str(scene.get("scene_id") or scene.get("sequence") or scene.get("time_range") or index))
    unique_scene_count = len(set(scene_keys))
    scene_coverage_ratio = min(unique_scene_count / expected_scene_count, 1.0) if expected_scene_count else 0.0

    checks = {
        "pre_transformation_witness": bool(re.search(r"before (?:the )?(?:visible )?transformation|before anyone (?:knew|admired|clapped)|pre.transformation|before the world", full)),
        "protection_system_creates_wound": bool(re.search(r"family|caregiver|mother|father|aunt", full) and re.search(r"protection|protective|hiding|hide|visibility is dangerous|taught .*hide", full) and re.search(r"wound|cost|harm|accountability|admit", full)),
        "behavioral_transformation_cost": bool(re.search(r"practice|training|certification|workshop|exercise|movement|speech|breath|threshold.crossing|behavioral cost", full)),
        "gaze_inversion_is_morally_suspect": bool(re.search(r"crowd|phones|public|attention|admires|approval", full) and re.search(r"not proof|shallow|does not equal recognition|without recognizing|suspect", full)),
        "second_performance_engine": bool(re.search(r"second performance|second engine|film|documentary|production|rehearsal|rescue drill|student film|performance arena", full)),
        "consent_violation_by_allies_is_real": bool(re.search(r"agreed|arranged|enter(?:ed)?|decided", full) and re.search(r"without asking|consent|ask me|choice|boundaries", full)),
        "reciprocal_memory_debt": bool(re.search(r"remembered|reciprocal memory|protected me|she protected him|before status|before beauty|never gratitude", full)),
        "public_space_closure": bool(re.search(r"same .*space|original .*space|public.space|staircase|pool gallery|hallway", full) and re.search(r"closure|transformed|chosen visibility|applaud|author|leader", full)),
        "no_cheap_self_harm_trigger": not bool(re.search(r"suicide|self[- ]?harm|overdose", full)),
        "complete_scene_coverage": bool(expected_scene_count and scene_coverage_ratio >= 1.0),
    }
    labels = {
        "pre_transformation_witness": "love/recognition is not proven before transformation",
        "protection_system_creates_wound": "family or caregiver protection does not causally create and then account for the hiding wound",
        "behavioral_transformation_cost": "transformation lacks behavioral practice/cost and risks becoming cosmetic reward",
        "gaze_inversion_is_morally_suspect": "public admiration is not treated as morally suspect recognition",
        "second_performance_engine": "the long-form package lacks a second professional/performance engine after the first reveal",
        "consent_violation_by_allies_is_real": "allies arranging visibility without consent is absent or not treated as a real violation",
        "reciprocal_memory_debt": "romance lacks reciprocal pre-transformation memory debt",
        "public_space_closure": "the original public humiliation geometry does not return transformed",
        "no_cheap_self_harm_trigger": "the package uses self-harm/suicide as a transformation shortcut",
        "complete_scene_coverage": "scene package is incomplete or duplicates scenes; transformation integrity cannot be confirmed from outline alone",
    }
    warnings = [labels[key] for key, ok in checks.items() if not ok]
    score = sum(checks.values()) / len(checks)
    if expected_scene_count and scene_coverage_ratio < 1.0:
        score = min(score, 0.65 * scene_coverage_ratio)
    return {
        "applies": True,
        "score_0_to_1": round(score, 3),
        "warnings": warnings,
        "checks": checks,
        "scene_coverage_ratio": round(scene_coverage_ratio, 3),
        "unique_scene_count": unique_scene_count,
        "craft_rule": "Transformation romance should prove recognition before beauty/status reversal, make protective systems accountable, give transformation behavioral cost, distrust the shallow crowd reversal, open a second performance engine, honor consent, repay reciprocal memory, and close the original public-space wound through chosen visibility.",
    }
