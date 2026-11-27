"""Zero-to-hero high-fantasy integrity checks.

Derived from ReelQuest evidence. These heuristics separate a legible
class/power progression engine from generic power fantasy. They are warnings,
not performance predictions.
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


def evaluate_zero_to_hero_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    applies = bool(re.search(r"zero to hero|underdog|awaken|bloodline|soul ?blood|battle academy|power progression|commoner", full))
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    checks = {
        "relational_rescue_goal": bool(re.search(r"father|mother|family|village|rescue|save|find him|bring him home|protect", full)),
        "systemic_class_gatekeeping": bool(re.search(r"commoner|noble|lowborn|caste|class|rules changed|gatekeeping|born right|way up|elite", full)),
        "courage_before_power": bool(re.search(r"turned|could have run|fear is.*instinct|courage|protect.*before|saved.*before|stood.*before", full)),
        "power_cost_or_container_limit": bool(re.search(r"cost|die|burst|lifespan|clash|container|poison|burning|pain|sacrifice|risk", full)),
        "legible_power_rules": bool(re.search(r"rank|ladder|crystal|bloodline|soul ?blood|fusion|fuse|level|rules|weakness|energy", full)),
        "institution_adapts_to_exclude": bool(re.search(r"rules changed|moved the bar|sealing off|targeting|permanently revoked|convicted|blame|buri", full)),
        "allies_have_agency_or_price": bool(re.search(r"mentor|teacher|student|ally|companion|deal|condition|exchange|report|guide|friend", full)),
        "ending_closure_or_explicit_serial_contract": bool(re.search(r"complete|resolution|home|reunited|saved|rebuild|belonging", full[-2500:])) or premise.get("release_format") in {"serial_episode", "series_premiere", "compilation_or_complete_season"},
    }
    labels = {
        "relational_rescue_goal": "power progression lacks a relational rescue/protection goal beyond becoming strong",
        "systemic_class_gatekeeping": "zero-to-hero conflict is not systemic class/institutional gatekeeping",
        "courage_before_power": "protagonist lacks a behavioral courage/protection proof before power escalation",
        "power_cost_or_container_limit": "power progression lacks bodily cost, limit, or failure risk",
        "legible_power_rules": "power system is not legible through rules, ranks, resources, energy limits, or fusion constraints",
        "institution_adapts_to_exclude": "institution does not adapt rules/narratives to preserve exclusion after the protagonist proves competence",
        "allies_have_agency_or_price": "allies/mentors are passive helpers rather than agents with price, agenda, or reciprocal obligation",
        "ending_closure_or_explicit_serial_contract": "standalone ending appears unresolved; if this is serial/compound packaging, classify and design it explicitly",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    score = sum(checks.values()) / len(checks)
    return {
        "applies": True,
        "score_0_to_1": round(score, 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Zero-to-hero works when class gatekeeping adapts systemically, courage precedes power, power has cost/rules/limits, allies exact prices, and the protagonist's strength remains subordinate to rescue/protection.",
    }
