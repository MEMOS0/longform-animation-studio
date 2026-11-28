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


def _partner_numeric_ages(text: str) -> tuple[list[int], list[int]]:
    female_roles = r"she|woman|wife|bride|girl|widow|female partner"
    male_roles = r"he|man|husband|groom|chief|widower|billionaire|male partner"
    female: list[int] = []
    male: list[int] = []
    age_before_role = r"\b(\d{2})[- ]*years?[- ]old\D{0,15}?"
    aged_before_role = r"\baged?\s*(\d{2})\D{0,12}?"
    role_then_aged = r"\D{0,8}?aged?\s*(\d{2})\b"
    patterns = (
        (age_before_role + rf"\b(?:{female_roles})\b", female),
        (aged_before_role + rf"\b(?:{female_roles})\b", female),
        (rf"\b(?:{female_roles})\b" + role_then_aged, female),
        (age_before_role + rf"\b(?:{male_roles})\b", male),
        (aged_before_role + rf"\b(?:{male_roles})\b", male),
        (rf"\b(?:{male_roles})\b" + role_then_aged, male),
    )
    for pattern, target in patterns:
        for match in re.finditer(pattern, text):
            age = next((int(group) for group in match.groups() if group), None)
            if age is not None and 10 <= age <= 99:
                target.append(age)
    return female, male


def _numeric_partner_age_gap(text: str) -> bool:
    female, male = _partner_numeric_ages(text)
    return bool(female and male and max(abs(a - b) for a in female for b in male) >= 10)


def _has_age_gap_evidence(text: str) -> bool:
    explicit = re.search(r"age[- ]gap|age difference|\b\d{2}[- ]year age|too old|too young|birth certificate|half (?:his|her) age", text)
    older_term = re.search(r"older (?:man|woman|widower|widow|partner)|old (?:man|woman|widower|billionaire)", text)
    younger_term = re.search(r"younger (?:man|woman|partner)|young (?:woman|man|girl)", text)
    return bool(explicit or (older_term and younger_term) or _numeric_partner_age_gap(text))


def evaluate_age_gap_romance_autonomy_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    age_gap = _has_age_gap_evidence(full)
    romance = bool(re.search(r"romance|love|marry|marriage|wife|husband|couple|partner", full))
    judgment = bool(re.search(r"societ|judg|gossip|family opposition|children object|scandal|gold[- ]?digger|shame|public opinion", full))
    if not (age_gap and romance and judgment):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    female_ages, male_ages = _partner_numeric_ages(full)
    numeric_adults = bool(female_ages and male_ages and min(female_ages) >= 18 and min(male_ages) >= 18)
    checks = {
        "both_partners_are_unambiguously_adults": numeric_adults or bool(re.search(r"both adults|both partners are adults|grown woman|grown man|never too young to choose|not a child|of legal age|adult younger|adult older|younger partner is an adult|older partner is an adult", full)),
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
