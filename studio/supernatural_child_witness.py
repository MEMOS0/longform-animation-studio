"""Supernatural child-witness investigation integrity checks.

These heuristics encode the Beyond the Night doctrine: supernatural child
knowledge should function as evidence-pressure inside a protected family/procedural
investigation, not as an oracle shortcut or spectacle power. They are transparent
creative warnings, not audience predictions.
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


def _pos(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return match.start() if match else None


def evaluate_supernatural_child_witness(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    ordered = "\n".join([architecture_text, scenes_text, premise_text])

    child_term = bool(re.search(r"child|boy|son|daughter|girl|kid", full))
    supernatural_witness = bool(re.search(
        r"supernatural|psychic|visions?|past life|reincarnation|divine light|child of light|knows? secrets?|memories? (?:of|from) (?:a )?(?:dead|missing)|remembers? (?:a )?(?:dead|missing)|impossible knowledge",
        full,
    ))
    investigation_term = bool(re.search(
        r"missing|cold case|murder|disappearance|disappeared|detective|sheriff|police|officer|investigat|witness|crime|mafia|gangster|cover.?up|body|killer",
        full,
    ))
    applies = child_term and supernatural_witness and investigation_term
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    care_pos = _pos(r"hospital|holds? (?:his|her) hand|comfort|care|protect|bedside|parent|father|mother|family|grief|bereav", ordered)
    knowledge_pos = _pos(r"visions?|knows?|remembers?|names?|secret|missing|cold case|past life|reincarnation|divine light", ordered)
    ending_text = full[-max(2000, len(full) // 3):]

    checks = {
        "care_before_knowledge_extraction": care_pos is not None and knowledge_pos is not None and care_pos < knowledge_pos,
        "knowledge_is_socially_or_physically_dangerous": bool(re.search(r"danger|dangerous|threat|afraid|risk|hurt|kill|warning|not safe|publicly identify|expose(?:s|d)? the child|child.*(?:target|danger)|protect.*(?:child|boy|son|daughter)", full)),
        "competing_explanations_for_child_knowledge": bool(re.search(r"trauma|imagination|grief|mental|fraud|reincarnation|past life|spiritual|skeptic|not helping|divine", full)) and bool(re.search(r"evidence|proof|investigat|verify|records?|test|document", full)),
        "supernatural_clues_converted_into_procedure": bool(re.search(r"records?|documents?|photographs?|photos?|map|route|witness|testimony|location|evidence|verify|search|walk.*memory|chain of custody|case file", full)),
        "institutional_or_local_power_resistance": bool(re.search(r"sheriff|chief|department|precinct|mafia|gangster|powerful family|town.*(?:afraid|silence|protect)|cover.?up|institution|authority|local power|stay out|leave .*alone", full)),
        "child_exposure_has_cost": bool(re.search(r"publicly identify|forced to identify|testify|confront|kidnap|abduct|target|afraid|scared|hurt|danger|threat|breaks down|shaking|trauma", full)),
        "confession_or_moral_truth_payoff": bool(re.search(r"confess|admit(?:s|ted)?|truth|i loved|i tried|cover.?up|what really happened|moral truth|motive|confession", full)),
        "ordinary_safety_reestablished_after_mystery": bool(re.search(r"home|safe|fine|okay|family|father|dad|ordinary|protected|stay|leave together|go together|sleep|breakfast", ending_text)),
        "adult_protection_not_oracle_exploitation": bool(re.search(r"protect(?:s|ed|ing)?|care(?:s|d)? for|comfort(?:s|ed)?|no acting alone|not alone|stay with|keep .*safe|adult.*(?:investigat|verify|protect)|father.*protect", full)),
    }

    labels = {
        "care_before_knowledge_extraction": "adult care/family protection is not established before the child's supernatural knowledge becomes useful",
        "knowledge_is_socially_or_physically_dangerous": "the child's knowledge is not treated as socially or physically dangerous",
        "competing_explanations_for_child_knowledge": "the story accepts the supernatural claim too quickly without trauma/skepticism/spiritual/evidence conflict",
        "supernatural_clues_converted_into_procedure": "visions or impossible knowledge are not converted into records, routes, witnesses, photographs, or verifiable evidence",
        "institutional_or_local_power_resistance": "investigation lacks institutional, criminal, or local-power resistance that prevents easy resolution",
        "child_exposure_has_cost": "the child can expose truth without fear, public exposure, bodily risk, or traumatic cost",
        "confession_or_moral_truth_payoff": "climax lacks confession or relational/moral truth behind the crime rather than only action defeat",
        "ordinary_safety_reestablished_after_mystery": "ending fails to re-establish ordinary safety/care after supernatural usefulness",
        "adult_protection_not_oracle_exploitation": "adults use the child as an oracle rather than visibly protecting and verifying around them",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Supernatural child-witness thrillers work when care precedes knowledge, knowledge creates danger, adults test competing explanations, clues become procedure, institutions resist, exposure costs the child, and the ending restores ordinary safety after moral truth.",
    }
