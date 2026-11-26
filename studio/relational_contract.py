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

DENIAL_TERMS = ["not free to choose", "no choice", "not free", "never free", "cannot choose", "can't choose", "denied choice", "without choice", "no agency", "not allowed to choose"]
REPAIR_TERMS = ["choice", "choose", "chosen", "consent", "person", "personhood", "free", "freedom", "name", "agency", "trust", "release"]
PAST_MARKERS = ["once", "at first", "at the start", "opening", "before", "previously", "used to", "initially", "earlier", "originally", "back then", "in the past"]
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


def mask_denials(text: str) -> str:
    masked = list(text)
    for term in sorted(DENIAL_TERMS, key=len, reverse=True):
        position = text.find(term)
        while position >= 0:
            for index in range(position, position + len(term)):
                masked[index] = " "
            position = text.find(term, position + 1)
    return "".join(masked)


def positive_outside_denials(text: str) -> bool:
    stripped = mask_denials(text)
    return any(positive in stripped for positive in REPAIR_TERMS)


def clause_bounds(text: str, start: int, end: int) -> tuple[int, int]:
    boundary_pattern = re.compile(r"[.;]|\bbut\b|\bhowever\b|\byet\b|\bthen\b|\blater\b|\bfinally\b|\bultimately\b|\bnow\b|\bthis time\b")
    local_start = 0
    local_end = len(text)
    for match in boundary_pattern.finditer(text):
        if match.end() <= start:
            local_start = match.end()
        elif match.start() >= end:
            local_end = match.start()
            break
    return local_start, local_end


def clause_texts(text: str) -> list[str]:
    boundary_pattern = re.compile(r"[.;]|\bbut\b|\bhowever\b|\byet\b|\bthen\b|\blater\b|\bfinally\b|\bultimately\b|\bnow\b|\bthis time\b")
    parts: list[str] = []
    cursor = 0
    for match in boundary_pattern.finditer(text):
        parts.append(text[cursor:match.start()])
        cursor = match.end()
    parts.append(text[cursor:])
    return [part.strip() for part in parts if part.strip()]


def positive_clause_is_flashback(clause: str, positive_position: int) -> bool:
    strong_markers = {"once", "at first", "at the start", "opening", "previously", "used to", "initially", "earlier", "originally", "back then", "in the past"}
    leading = clause.lstrip()
    if any(leading.startswith(marker) for marker in strong_markers):
        return True
    for marker in PAST_MARKERS:
        marker_position = clause.find(marker)
        if marker_position < 0:
            continue
        if marker_position < positive_position:
            return True
        if marker in {"at first", "at the start", "previously", "originally", "back then", "in the past"}:
            return True
    return False


def positive_repair_after(text: str) -> bool:
    for clause in clause_texts(text):
        stripped = mask_denials(clause)
        positive_positions = [stripped.find(positive) for positive in REPAIR_TERMS if stripped.find(positive) >= 0]
        if not positive_positions:
            continue
        if positive_clause_is_flashback(clause, min(positive_positions)):
            continue
        return True
    return False


def denial_is_unresolved(text: str) -> bool:
    """Evaluate denial occurrences in temporal order using local clause context.

    Past-tense framing only applies inside the clause containing the denial. A later
    flashback cannot soften a present payoff denial, unrelated "no longer" phrases do
    not count as agency repair, and an explicit lifting of a denial clears the earlier
    unresolved state.
    """
    occurrences: list[tuple[int, int]] = []
    for term in DENIAL_TERMS:
        position = text.find(term)
        while position >= 0:
            occurrences.append((position, position + len(term)))
            position = text.find(term, position + 1)
    if not occurrences:
        return False

    unresolved = False
    for start, end in sorted(set(occurrences)):
        local_start, local_end = clause_bounds(text, start, end)
        local = text[local_start:local_end]
        prefix = text[local_start:start]
        suffix = text[end:]
        occurrence_offset = start - local_start
        marker_positions = [(marker, local.find(marker)) for marker in PAST_MARKERS if local.find(marker) >= 0]
        past_before = any(position < occurrence_offset for _, position in marker_positions)
        trailing_past = any(marker in local[occurrence_offset:] for marker in ["at first", "at the start", "previously", "originally", "back then", "in the past"])
        denial_lifted = re.search(r"no longer\s+(?:\w+\s+){0,3}$", prefix) is not None or re.search(r"no more\s+(?:\w+\s+){0,3}$", prefix) is not None
        trailing_before = "before" in local[occurrence_offset:] and not denial_lifted
        explicitly_past = past_before or trailing_past or trailing_before
        if explicitly_past:
            continue
        if denial_lifted:
            unresolved = False
        elif positive_repair_after(suffix):
            unresolved = False
        else:
            unresolved = True
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
