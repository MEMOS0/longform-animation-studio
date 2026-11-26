"""Relational-contract validation for creature romance/protection, social tests, and power-asymmetric bonds."""
from __future__ import annotations

from typing import Any

REQUIRED_FIELDS = [
    "power_asymmetry",
    "safety_or_kindness_before_power",
    "costly_protagonist_action",
    "consent_or_personhood_repair",
    "payoff_image",
]


def evaluate_relational_contract(premise: dict[str, Any]) -> dict[str, Any]:
    raw_explicit = premise.get("relational_contract") or {}
    warnings: list[str] = []
    if raw_explicit and not isinstance(raw_explicit, dict):
        return {
            "score_0_to_1": 0.0,
            "warnings": ["relational_contract must be an object; malformed premise section was not evaluated"],
            "craft_rule": "Power-asymmetric relationships are strongest when safety or costly kindness precedes power, and the ending repairs consent/personhood rather than rewarding coercion.",
        }
    explicit = raw_explicit
    if not explicit:
        return {
            "score_0_to_1": 0.0,
            "warnings": ["premise does not declare relational_contract: power asymmetry, safety/kindness before power, costly action, consent/personhood repair, and payoff image must be explicit"],
            "craft_rule": "Power-asymmetric relationships are strongest when safety or costly kindness precedes power, and the ending repairs consent/personhood rather than rewarding coercion.",
        }
    missing = [field for field in REQUIRED_FIELDS if not explicit.get(field)]
    if missing:
        warnings.append("relational_contract missing fields: " + ", ".join(missing))
    safety = str(explicit.get("safety_or_kindness_before_power", "")).lower()
    repair = str(explicit.get("consent_or_personhood_repair", "")).lower()
    payoff = str(explicit.get("payoff_image", "")).lower()
    if safety and not any(term in safety for term in ["before", "first", "without knowing", "before knowing", "prior to", "initially", "unaware"]):
        warnings.append("safety/kindness before power is not temporally explicit")
    denial_terms = ["no choice", "not free", "never free", "cannot choose", "can't choose", "denied choice", "without choice", "no agency", "not allowed to choose"]
    if repair and any(term in repair for term in denial_terms):
        warnings.append("consent/personhood repair explicitly denies choice or freedom")
    elif repair and not any(term in repair for term in ["choice", "choose", "consent", "person", "personhood", "free", "freedom", "name", "agency", "trust", "release"]):
        warnings.append("consent/personhood repair does not clearly restore choice, freedom, identity, or trust")
    if payoff and any(term in payoff for term in ["marry him", "rescued by", "becomes rich", "wealthy wife", "powerful husband"]):
        warnings.append("payoff may reward status/romance without repaired agency")
    return {
        "score_0_to_1": max(0.0, round(1.0 - 0.2 * len(warnings), 2)),
        "fields": {field: explicit.get(field) for field in REQUIRED_FIELDS},
        "warnings": warnings,
        "craft_rule": "Power-asymmetric relationships are strongest when safety or costly kindness precedes power, and the ending repairs consent/personhood rather than rewarding coercion.",
    }
