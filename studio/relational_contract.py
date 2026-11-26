"""Relational-contract validation for creature romance/protection, social tests, and power-asymmetric bonds."""
from __future__ import annotations

import re
from typing import Any

REQUIRED_FIELDS = [
    "power_asymmetry",
    "safety_or_kindness_before_power",
    "costly_protagonist_action",
    "consent_or_personhood_repair",
    "payoff_image",
]

DENIAL_TERMS = ["no choice", "not free", "never free", "cannot choose", "can't choose", "denied choice", "without choice", "no agency", "not allowed to choose"]
REPAIR_TERMS = ["choice", "choose", "chosen", "consent", "person", "personhood", "free", "freedom", "name", "agency", "trust", "release"]
PAST_MARKERS = ["once", "at first", "opening", "before", "previously", "used to", "initially"]
CONTRAST_MARKERS = ["but", "however", "then", "later", "finally", "ultimately", "now", "becomes", "restores", "restored", "this time"]



AFTER_REVEAL_PATTERNS = [
    "after learning", "after discovering", "after knowing", "after the reveal", "after his power is revealed",
    "after her power is revealed", "after their power is revealed", "once she knows", "once he knows",
    "once they know", "when she learns", "when he learns", "when they learn",
]
BEFORE_REVEAL_PATTERNS = [
    "before knowing", "before learning", "before discovering", "before she knows", "before he knows",
    "before they know", "before the reveal", "before his power", "before her power", "before their power",
    "without knowing", "unaware", "not knowing", "prior to knowing", "prior to learning", "prior to discovering", "prior to the reveal",
    "only afterward does she learn", "only afterward does he learn", "only afterward do they learn",
    "only afterward she learns", "only afterward he learns", "only afterward they learn",
    "only afterward is his identity revealed", "only afterward is her identity revealed", "only afterward is the identity revealed",
]


def kindness_is_after_reveal(text: str) -> bool:
    return any(pattern in text for pattern in AFTER_REVEAL_PATTERNS)


def kindness_is_before_power(text: str) -> bool:
    return any(pattern in text for pattern in BEFORE_REVEAL_PATTERNS)


def denial_is_unresolved(text: str) -> bool:
    """Track the final state of choice/freedom across ordered clauses.

    Positive words inside denial phrases ("no choice", "not free") are stripped before
    repair detection, while explicit past denials only count as repaired when a later
    clause restores agency. A later or current denial therefore overrides earlier freedom.
    """
    clauses = [
        clause.strip()
        for clause in re.split(r"[.;]|but|however|yet|then|later|finally|ultimately|now|this time", text)
        if clause.strip()
    ]
    unresolved = False
    for clause in clauses:
        stripped = clause
        for term in sorted(DENIAL_TERMS, key=len, reverse=True):
            stripped = stripped.replace(term, " ")
        has_denial = any(term in clause for term in DENIAL_TERMS)
        has_repair = any(positive in stripped for positive in REPAIR_TERMS)
        explicitly_past = any(marker in clause for marker in PAST_MARKERS)
        no_longer_denied = "no longer" in clause or "no more" in clause
        if has_denial and not explicitly_past and not no_longer_denied:
            unresolved = True
        if has_repair or no_longer_denied:
            unresolved = False
    return unresolved


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
    if safety and kindness_is_after_reveal(safety):
        warnings.append("safety/kindness happens after the power or identity reveal")
    elif safety and not kindness_is_before_power(safety):
        warnings.append("safety/kindness before power is not temporally explicit")
    if repair and denial_is_unresolved(repair):
        warnings.append("consent/personhood repair explicitly denies choice or freedom")
    elif repair and not any(term in repair for term in REPAIR_TERMS):
        warnings.append("consent/personhood repair does not clearly restore choice, freedom, identity, or trust")
    if payoff and any(term in payoff for term in ["marry him", "rescued by", "becomes rich", "wealthy wife", "powerful husband"]):
        warnings.append("payoff may reward status/romance without repaired agency")
    return {
        "score_0_to_1": max(0.0, round(1.0 - 0.2 * len(warnings), 2)),
        "fields": {field: explicit.get(field) for field in REQUIRED_FIELDS},
        "warnings": warnings,
        "craft_rule": "Power-asymmetric relationships are strongest when safety or costly kindness precedes power, and the ending repairs consent/personhood rather than rewarding coercion.",
    }
