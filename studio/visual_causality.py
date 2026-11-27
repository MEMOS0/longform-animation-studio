"""Muted-intelligibility and visual causality heuristics.

Epicverse evidence showed that a silent visual chain can carry a breakout. This
module does not measure beauty; it checks whether scene scaffolds contain visible
actors, actions, objects, and consequence images rather than abstract emotion only.
"""
from __future__ import annotations

import re
from typing import Any

ACTION_RE = re.compile(r"\b(?:cross(?:es|ing)?|kneel(?:s|ing)?|hid(?:e|es|ing)|feed(?:s|ing)?|open(?:s|ing)?|carr(?:y|ies|ying)|protect(?:s|ing)?|touch(?:es|ing)?|run(?:s|ning)?|enter(?:s|ing)?|build(?:s|ing)?|repair(?:s|ing)?|share(?:s|ing)?|return(?:s|ing)?|throw(?:s|ing)?|break(?:s|ing)?|heal(?:s|ing)?|cook(?:s|ing)?|warm(?:s|ing)?|shelter(?:s|ing)?|escape(?:s|ing)?|confront(?:s|ing)?|lower(?:s|ing)?|lift(?:s|ing)?|plac(?:e|es|ing)|clos(?:e|es|ing)|lock(?:s|ing)?|unlock(?:s|ing)?|chain(?:s|ing)?|forc(?:e|es|ing)|shield(?:s|ing)?|fall(?:s|ing)?|lay(?:s|ing)?|step(?:s|ping)?|reach(?:es|ing)?|flee(?:s|ing)?|crawl(?:s|ing)?|climb(?:s|ing)?|trap(?:s|ping)?|free(?:s|ing)?|lure(?:s|ing)?|operate(?:s|ing)?|brace(?:s|ing)?|emerge(?:s|ing)?|fill(?:s|ing)?|tremble(?:s|ing)?|withdraw(?:s|ing)?|turn(?:s|ing)?|count(?:s|ing)?|work(?:s|ing)?|test(?:s|ing)?|hold(?:s|ing)?|guid(?:e|es|ing))\b", re.I)
CONCRETE_RE = re.compile(r"\b(?:child|creature|giant|woman|man|mother|father|guard|soldier|customer|neighbor|hand|face|body|scar|door|gate|window|floor|table|pump|oven|cart|vial|key|fire|water|food|bread|ledger|proof|cage|chain|stone|roof|bed|boat|forest|snow|cave|room|train|tunnel|vehicle|wreck|predator|insect|spider|centipede|moth|crab|turtle|animal|pigeon|bird|light|wire|panel|engine|lighthouse|foghorn)\b", re.I)
VAGUE_RE = re.compile(r"\b(?:power shifts?|emotional shift|status space under pressure|controlled attention|theme|meaning|dignity|resolve)\b", re.I)


def flatten(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(flatten(v) for v in value)
    return str(value or "")


def evaluate_visual_causality(scenes: list[dict[str, Any]] | None) -> dict[str, Any]:
    scenes = scenes or []
    if not scenes:
        return {"score_0_to_1": 0.0, "warnings": ["no scenes supplied"], "scene_scores": [], "doctrine": "Every scene should remain broadly intelligible when muted."}
    scene_scores = []
    warnings = []
    for scene in scenes:
        visual = scene.get("visual_action") or {}
        first = str(visual.get("first_image") or "")
        final = str(visual.get("final_image") or "")
        combined = flatten(visual)
        scene_id = scene.get("scene_id", "?")
        score = 0.2
        first_action = bool(ACTION_RE.search(first))
        final_action = bool(ACTION_RE.search(final))
        concrete = bool(CONCRETE_RE.search(combined))
        callback = bool(final.strip()) and final.strip().lower() != first.strip().lower()
        vague_only = bool(VAGUE_RE.search(combined)) and not concrete
        score += 0.2 if first_action else 0.0
        score += 0.2 if final_action else 0.0
        score += 0.2 if concrete else 0.0
        score += 0.2 if callback else 0.0
        if vague_only:
            score -= 0.15
        scene_scores.append({"scene_id": scene_id, "score_0_to_1": round(max(0.0, min(1.0, score)), 3), "first_action": first_action, "final_action": final_action, "concrete_image": concrete, "final_image_changes": callback})
        missing = []
        if not first_action:
            missing.append("entry image lacks a readable physical action")
        if not final_action:
            missing.append("exit/consequence image lacks a readable physical action")
        if not concrete:
            missing.append("visual action lacks concrete bodies/objects/spaces")
        if vague_only:
            missing.append("visual description is abstract rather than filmable")
        if missing:
            warnings.append(f"{scene_id}: " + "; ".join(missing))
    mean = sum(row["score_0_to_1"] for row in scene_scores) / len(scene_scores)
    return {
        "score_0_to_1": round(mean, 3),
        "scene_scores": scene_scores,
        "warnings": warnings,
        "doctrine": "Every scene should remain broadly intelligible when muted: visible protector/protected relation, physical action, object/space consequence, and a final image changed by the turn.",
    }
