"""Epistemic-intimacy integrity checks.

Derived from Purple Grape thought-hearing hit/medium/low evidence. Transparent
creative warnings, not performance predictions. Applies when one character can
hear another character's thoughts or inner voice inside a romance, care,
employment, family, or power relationship.
"""
from __future__ import annotations

import re
from typing import Any


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(_text(v) for v in value.values())
    if isinstance(value, list):
        return "\n".join(_text(v) for v in value)
    return ""


def evaluate_epistemic_intimacy_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    thought_access = bool(re.search(r"hear(?:s|ing)?(?:\s+\w+){0,3}\s+(?:inner\s+)?thoughts|inner voice|mind[- ]reading|read(?:s|ing)?(?:\s+\w+){0,3}\s+mind|hear(?:s|ing)?(?:\s+\w+){0,2}\s+voice", full))
    relationship = bool(re.search(r"romance|love|wife|husband|marriage|fianc|ceo|warlord|nanny|maid|butler|family|spouse|bride|groom", full))
    power_stakes = bool(re.search(r"mute|secret|hidden|scheme|plot|expose|test|suspect|system|mission|villain|force|contract|divorce|danger", full))
    if not (thought_access and relationship and power_stakes):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    architecture_text = _text(architecture).lower()
    final_scene_text = _text(scenes[-1]).lower() if scenes else ""
    ending_parts: list[str] = []
    if isinstance(architecture, dict):
        for key, value in architecture.items():
            if re.search(r"ending|final|closing|resolution|epilogue|payoff", str(key).lower()):
                ending_parts.append(_text(value).lower())
        sequences = architecture.get("sequences") or architecture.get("sequence")
        if isinstance(sequences, list) and sequences:
            ending_parts.append(_text(sequences[-1]).lower())
    ending_text = "\n".join(ending_parts + [final_scene_text]) or (architecture_text[-max(1, len(architecture_text) // 3):] if architecture_text else full[-max(1, len(full) // 4):])

    checks = {
        "access_has_rules_uncertainty_or_cost": bool(re.search(r"lost mind|unable to confirm|observe personally|why can|can.?t hear|no inner voice|clearer|intermittent|test whether|am i hearing|can you hear|if you can hear", full)),
        "interior_exterior_contradiction_drives_irony": bool(re.search(r"mute|can actually talk|cold|pretend|fake|outer|inside|inner resistance|secretly|thoughts.*expressions|says.*but thinks|performance", full)),
        "knowledge_creates_suspicion_exposure_or_privacy_risk": bool(re.search(r"can.?t keep her|suspect|testing me|i know you can hear|expose|privacy|secret|if he heard|done for|retaliation|danger|careful what you think", full)),
        "protagonist_has_competence_independent_of_mindreading": bool(re.search(r"cook|recipe|maid|butler|gun|shoot|medicine|scientist|research|invent|investigat|negotiat|work|job|skill|protect|save", full)),
        "care_is_behavioral_not_only_overheard_affection": bool(re.search(r"made dessert|cook|taking care|risk.*life|save|protect|shield|support|help|stay|one step at a time|care", full)),
        "consent_privacy_disclosure_or_uncertainty_is_addressed": bool(re.search(r"can you hear|you can hear my thoughts|testing|disclose|tell me what|privacy|secret|choose|choice|consent|don.?t think|clear your mind|if you can hear", full)),
        "power_is_not_used_as_ownership_or_capture": not bool(re.search(r"capture progress|target.*one hundred percent|own(?:s|ing)? her|possess|property|he owns her|trapped forever|no choice but to stay", full)),
        "ending_preserves_independent_life_vocation_or_chosen_proximity": bool(re.search(r"research institute|dream|stable job|chosen|choice|support her|independent|family can finally|long time no see|come find you|own feet|work for you|mutual", ending_text)),
    }
    labels = {
        "access_has_rules_uncertainty_or_cost": "thought access is omniscient convenience rather than a bounded, uncertain, costly, or testable ability",
        "interior_exterior_contradiction_drives_irony": "the premise mentions mind-reading but does not exploit the gap between outward behavior and interior truth",
        "knowledge_creates_suspicion_exposure_or_privacy_risk": "secret knowledge has no consequences, suspicion, exposure, testing, or privacy danger",
        "protagonist_has_competence_independent_of_mindreading": "the protagonist has no independent labor, craft, investigation, care, protection, or professional competence beyond the power",
        "care_is_behavioral_not_only_overheard_affection": "intimacy is only overheard sentiment rather than visible care, protection, support, or sacrifice",
        "consent_privacy_disclosure_or_uncertainty_is_addressed": "the story treats invasive access as neutral instead of addressing disclosure, uncertainty, consent, privacy, or mental boundaries",
        "power_is_not_used_as_ownership_or_capture": "the power or system turns love into capture, ownership, possession, or trap completion rather than chosen attachment",
        "ending_preserves_independent_life_vocation_or_chosen_proximity": "the ending does not preserve independent work/vocation/family repair or freely chosen proximity",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Epistemic intimacy works when thought access has rules and uncertainty, exposes the gap between exterior and interior truth, creates privacy/suspicion consequences, coexists with independent competence and behavioral care, addresses consent/disclosure, avoids capture or ownership logic, and ends in chosen proximity plus an independent life.",
    }
