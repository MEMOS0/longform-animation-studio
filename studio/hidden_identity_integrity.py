"""Transparent hidden-identity melodrama integrity checks.

These heuristics encode the Lioren breakout finding: hidden wealth/status works best
when competence and love precede the reveal, the lie creates a trust cost, power is
used prosocially, and the ending subordinates status to chosen love or family.
They are warnings for creative review, not oracle predictions.
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


def evaluate_hidden_identity_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    hidden = bool(re.search(r"hidden (?:identity|heir|heiress|billionaire|wealth|status)|secret(?:ly)? (?:rich|wealthy|heir|billionaire)|poor (?:student|worker|mechanic|student)|true identity|not knowing he was|not knowing she was", full))
    if not hidden:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    reveal = bool(re.search(r"identity reveal|reveal(?:s|ed)? (?:his|her|their)? ?(?:identity|wealth|status)|true identity|billionaire heir|heiress", full))
    competence = bool(re.search(r"competence|corrects?|valuation|solves?|repairs?|work(?:s|ed)?|craft|skill|earns?|proves?|intellectual|publicly validates?", full))
    ordinary_bond = bool(re.search(r"before (?:status|wealth)|ordinary kindness|coffee|study|library|meal|work together|kindness|care|love(?:d)? before|non-status", full))
    trust_cost = bool(re.search(r"trust wound|lie|lied|hiding the truth|apolog|needs time|informed choice|wrong to hide|trust (?:is|was) (?:damaged|broken)", full))
    prosocial_power = bool(re.search(r"protect(?:s|ed)?|save(?:s|d)?|rescue(?:s|d)?|university|school|hospital|workers?|students?|community|family|foundation|institution|vulnerable", full))
    belonging_closure = bool(re.search(r"chosen love|family|belonging|home|proposal|wedding|greatest treasure|love (?:before|not because)|subordinat", full[-max(2000, len(full) // 3):]))

    checks = {
        "reveal_present": reveal,
        "competence_or_kindness_before_status": competence,
        "ordinary_non_status_bond": ordinary_bond,
        "lie_has_trust_cost": trust_cost,
        "power_used_prosocially": prosocial_power,
        "wealth_subordinated_to_belonging": belonging_closure,
    }
    labels = {
        "reveal_present": "hidden-identity premise never clearly stages the reveal",
        "competence_or_kindness_before_status": "hidden identity lacks competence/kindness proof independent of status",
        "ordinary_non_status_bond": "love/loyalty is not clearly formed through ordinary non-status behavior before the reveal",
        "lie_has_trust_cost": "hidden identity reveal does not treat deception as a relational trust wound requiring repair",
        "power_used_prosocially": "hidden wealth/power is not clearly used to protect people or institutions the audience cares about",
        "wealth_subordinated_to_belonging": "ending does not clearly subordinate wealth/status to chosen love, family, home, or belonging",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]

    accountability = {
        "intelligent_deceived_party_evidence": bool(re.search(r"evidence|facts|records|documents|invoice|timeline|audit|investigat", full)),
        "post_reveal_spatial_boundary": bool(re.search(r"separate homes|no gifts|no persuasion|get out|post[- ]reveal boundar|relationship boundar|enforc(?:e|ed|ing)[^\n]{0,40}space|space after (?:the )?reveal", full)),
        "procedural_full_disclosure": bool(re.search(r"full disclosure|every document|supporting documents|written record|original record|complete record", full)),
        "consent_based_help_rules": bool(re.search(r"help requires consent|no tests|no surveillance|questions replace traps|unless .*safety|say yes", full)),
        "repeat_inconvenient_compliance": bool(re.search(r"when inconvenient|following them|prove it when|10 days|ten days|therapy|\bdates\b", full)),
        "truthful_rechoice": bool(re.search(r"choose me again|choose each other|full truth|with conditions|restart the marriage", full)),
    }
    accountability_missing = [key for key, ok in accountability.items() if not ok]
    if hidden and accountability_missing:
        warnings.append("QueenFlix accountability extensions incomplete: " + ", ".join(accountability_missing))
    base_score = sum(checks.values()) / len(checks)
    accountability_score = sum(accountability.values()) / len(accountability)
    score = 0.7 * base_score + 0.3 * accountability_score
    return {"applies": True, "score_0_to_1": round(score, 3), "base_score_0_to_1": round(base_score, 3), "accountability_score_0_to_1": round(accountability_score, 3), "warnings": warnings, "checks": checks, "queenflix_accountability": accountability}
