"""Appearance-capital transformation integrity checks from EchoDrama evidence."""
from __future__ import annotations

import re
from typing import Any


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(_text(item) for item in value.values())
    if isinstance(value, list):
        return "\n".join(_text(item) for item in value)
    return ""


def evaluate_appearance_capital_transformation_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    appearance = bool(re.search(r"ugly|fat|hidden beauty|masked revenge|new face|beauty|beautiful|girl in the mirror|mocked[^.\n]{0,50}(?:face|appearance)|(?:face|appearance)[^.\n]{0,50}mocked", full))
    social = bool(re.search(r"mocked|laughed|humiliat|bully|shame|reject|school|wedding|public|everyone", full))
    transform = bool(re.search(r"transform|new face|masked|hidden beauty|become|returned with a new face|makeover", full))
    if not (appearance and social and transform):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    ending_parts: list[str] = []
    if isinstance(architecture, dict):
        for key, value in architecture.items():
            if re.search(r"ending|final|closing|resolution|epilogue|payoff", str(key).lower()):
                ending_parts.append(_text(value).lower())
        sequences = architecture.get("sequences") or architecture.get("sequence")
        if isinstance(sequences, list) and sequences:
            ending_parts.append(_text(sequences[-1]).lower())
    architecture_text = _text(architecture).lower()
    end = "\n".join(ending_parts + ([_text(scenes[-1]).lower()] if scenes else [])) or (architecture_text[-max(1, len(architecture_text) // 3):] if architecture_text else full[-max(1, len(full) // 4):])

    checks = {
        "opening_establishes_social_cost_without_making_stigma_the_only_engine": bool(re.search(r"mocked|laughed|humiliat|pig|ugly|fat|reject", full)) and bool(re.search(r"uncle|family|school|role|work|dream|love|father|shares|career", full)),
        "transformation_has_specific_practice_cost_or_time": bool(re.search(r"10 years|ten years|training|practice|film|role|weight loss|surgery|hospital|checkup|project|study|learns?|work", full)),
        "inner_capability_or_relational_memory_survives_the_new_face": bool(re.search(r"voice|talent|role|drawing|kind|saved|remember|recognized|promise|love letter|letter|career|project", full)),
        "powerful_or_desired_character_must_rerecognize_not merely_desire": bool(re.search(r"recogniz|remember|know who|look at me|not interested|save me again|who are you really|identity", full)),
        "revenge_does_not_depend_on_body_shaming_or_erasing_the_original_self": not bool(re.search(r"stay fat|pig|deserved because fat|ugly people deserve", end)) and bool(re.search(r"not the sophia|girl in the mirror|this is my face|original self|i am|identity|name", full)),
        "transformation_carries_physical_emotional_or_ethical_cost": bool(re.search(r"collapse|hospital|hurt|scared|not enough time|risk|cost|left side|fall|assault|weapon|sacrifice", full)),
        "truth_is_exposed_through_evidence_or_witnessed_action": bool(re.search(r"evidence|document|handwriting|witness|police|law|submitted|signed|camera|report|proof", full)),
        "ending_converts_status_into_reciprocal_choice_or_material_justice": bool(re.search(r"deal|choice|your turn|congratulations|graduated|law can handle|evidence has been submitted|proud|found you|apolog", end)),
        "romance_is_not_reward_for_becoming_acceptably_beautiful": bool(re.search(r"save me|proud|found you|love before|recognized|choice|deal|trust", end)) and not bool(re.search(r"loves? her only because she is beautiful|deserves love now that she is thin", full)),
    }
    labels = {
        "opening_establishes_social_cost_without_making_stigma_the_only_engine": "the opening uses stigma but gives no family/work/dream engine beyond humiliation",
        "transformation_has_specific_practice_cost_or_time": "the transformation is instantaneous or vague rather than practiced, costly, or time-bound",
        "inner_capability_or_relational_memory_survives_the_new_face": "the new appearance replaces rather than reveals durable capability, memory, or relational history",
        "powerful_or_desired_character_must_rerecognize_not merely_desire": "the desired/powerful character only desires the transformed surface and never re-recognizes the person",
        "revenge_does_not_depend_on_body_shaming_or_erasing_the_original_self": "the revenge logic reproduces body-shaming or erases the original self instead of indicting the gaze",
        "transformation_carries_physical_emotional_or_ethical_cost": "the transformation has no physical, emotional, ethical, or relational cost",
        "truth_is_exposed_through_evidence_or_witnessed_action": "exposure happens by assertion rather than documents, witnesses, law, or observed action",
        "ending_converts_status_into_reciprocal_choice_or_material_justice": "the ending is only status/romance reward rather than reciprocal choice, graduation/recognition, or legal/material justice",
        "romance_is_not_reward_for_becoming_acceptably_beautiful": "romance functions as a prize for acceptable beauty rather than recognition, trust, or chosen care",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Appearance-capital transformation works when social stigma is answered by durable capability, costly transformation, re-recognition, evidence or witnessed truth, and reciprocal/material justice; it fails when the new face is merely a beauty prize or the story reproduces body-shaming.",
    }
