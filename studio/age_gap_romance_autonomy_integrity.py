"""Age-gap romance autonomy integrity checks.

Transparent creative warnings derived from Tales By Amy evidence. Not a
performance predictor. Applies to adult intergenerational romance under
family/social judgment.
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


def evaluate_age_gap_romance_autonomy_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    age_gap = bool(re.search(r"age[- ]gap|age difference|older (?:man|woman|widower|widow)|younger (?:man|woman)|old (?:man|woman|widower|billionaire)|young (?:woman|man|girl)|\b\d{2}[- ]year age|too old|too young|birth certificate", full))
    romance = bool(re.search(r"romance|love|marry|marriage|wife|husband|couple|partner", full))
    judgment = bool(re.search(r"societ|judg|gossip|family opposition|children object|scandal|gold[- ]?digger|shame|public opinion", full))
    if not (age_gap and romance and judgment):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    checks = {
        "both_partners_are_unambiguously_adults": bool(re.search(r"adult|grown woman|grown man|never too young to choose|not a child|both adults|of legal age", full)),
        "financial_power_asymmetry_is_named": bool(re.search(r"money|wealth|billionaire|rich|gold[- ]?digger|refus\w+ money|keep your money|financial|pay|account|transfer", full)),
        "younger_partner_has_refusal_rights_and_independence": bool(re.search(r"refus\w+|can leave|free to leave|choice|chose|choose|independent|own (?:shop|business|career|work)|not for money|walk away", full)),
        "love_is_behavioral_not_wealth_spectacle": bool(re.search(r"patience|respect|honest|trust|apolog|listen|care|sacrifice|showing up|learn\w* (?:their|her|his) habits|communication", full)),
        "family_opposition_has_legitimate_grief_or_protection": bool(re.search(r"griev\w+|lost (?:his|her) (?:wife|husband)|replace your mother|protect (?:him|her)|afraid|worried|children", full)),
        "accusations_are_resolved_procedurally": bool(re.search(r"transfer record|account access|receipt|evidence|witness|timeline|documents?|confession|police|proof|records?", full)),
        "consent_and_repair_continue_after_commitment": bool(re.search(r"after marriage|married life|talk honestly|communicat|apolog|repair|safe|choice|consent|boundary|respect", full)),
        "ending_preserves_identity_beyond_public_approval": bool(re.search(r"own (?:shop|business|career|work)|independent|ordinary|family|work|studio|chosen|self[- ]worth|identity", full)),
    }
    labels = {
        "both_partners_are_unambiguously_adults": "the age-gap framing is ambiguous about adulthood or infantilizes the younger partner",
        "financial_power_asymmetry_is_named": "wealth/age power asymmetry is decorative rather than named as a real consent and judgment condition",
        "younger_partner_has_refusal_rights_and_independence": "the younger partner lacks visible refusal rights, independent judgment, work, or ability to leave",
        "love_is_behavioral_not_wealth_spectacle": "love is proven through wealth/status rather than patience, respect, honesty, listening, and repair",
        "family_opposition_has_legitimate_grief_or_protection": "family opposition is flat prejudice instead of a mixture of grief, protection, and social judgment that must be answered",
        "accusations_are_resolved_procedurally": "gold-digger or betrayal accusations resolve by declaration rather than records, witnesses, timelines, documents, or confession",
        "consent_and_repair_continue_after_commitment": "the story treats marriage/commitment as the end of consent, communication, and power negotiation",
        "ending_preserves_identity_beyond_public_approval": "the ending substitutes public approval/pregnancy/romance for the younger partner's continuing independent identity",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Adult age-gap romance works when financial/power asymmetry is explicit, the younger partner has independence and refusal rights, family opposition includes real grief/protection, accusations resolve procedurally, behavioral love outweighs spectacle, consent/repair continue after commitment, and the ending preserves identity beyond public approval.",
    }
