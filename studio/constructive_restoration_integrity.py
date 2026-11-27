"""Constructive-restoration science-fiction integrity checks.

Encodes the NEXORA mechanic doctrine as transparent creative review heuristics:
technical wonder should be earned through care, repair labor, learner agency,
economic independence, restitution, and tested infrastructure rather than lore
spectacle or effortless wish fulfillment. This validator is a warning system,
not a performance predictor.
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


def _ordered(text: str, first_pattern: str, second_pattern: str) -> bool:
    first = _pos(first_pattern, text)
    second = _pos(second_pattern, text)
    return first is not None and second is not None and first < second


def _cooccurs_in_segment(text: str, first_pattern: str, second_pattern: str) -> bool:
    return any(
        re.search(first_pattern, segment) and re.search(second_pattern, segment)
        for segment in re.split(r"[.!?\n]", text)
    )


def evaluate_constructive_restoration_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    narrative = "\n".join([_text(architecture), _text(scenes)]).lower()
    repair_core = bool(re.search(r"mechanic|workshop|engineer|salvage|rebuild|restoration|(?:repair(?:s|ed|ing)?|fix(?:es|ing)?|restore(?:s|d)?)\W{0,30}(?:machine|robot|vehicle|ship|station|engine)|(?:machine|robot|vehicle|ship|station|engine)\W{0,30}(?:repair(?:s|ed|ing)?|fix(?:es|ing)?|restore(?:s|d)?)", full))
    speculative_object = bool(re.search(r"\b(?:robot|android|machine|ship|starship|spaceship|station|city|drone|fleet)\b|\bai\b|war machine", full))
    applies = repair_core and speculative_object
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    object_ladder = _ordered(narrative, r"small object|lamp|circuit|tool|toy|radio|servo|motor", r"\b(?:robot|vehicle|bike|machine)\b") and _ordered(narrative, r"\b(?:robot|vehicle|bike|machine)\b", r"\b(?:ship|starship|spaceship|station|city)\b|infrastructure|power grid")
    learner_work = bool(re.search(r"\b(?:she|he|they|learner|apprentice|protagonist)\s+(?:repairs?|fixes|solders?|wires?|tests?|builds?|diagnoses?|installs?)|(?:she|he|they|learner|apprentice)\s+(?:does|performs)\s+(?:the\s+)?(?:repair|work)", narrative))
    restitution_language = bool(re.search(r"restitution|reparations?|make amends|repair the damage|rebuild what|help rebuild|compensat|accountab", full))
    weapon_pattern = r"war machine|combat unit|weapon|military robot|battle machine"
    care_use_pattern = r"repurpos|convert|care|farm|shelter|clinic|workshop|infrastructure|cook|serve|protect"
    repurposed_weapon = _cooccurs_in_segment(full, weapon_pattern, care_use_pattern)
    money_pattern = r"money|payment|paid|wages?|reward|wealth|sale|profit"
    capacity_pattern = r"parts?|tools?|workshop|repair|supplies|crew|infrastructure|production|build"
    production_capacity = _cooccurs_in_segment(full, money_pattern, capacity_pattern)
    wonder_infrastructure = bool(re.search(r"wonder|ancient|miracle|alien|advanced|hidden", full) and re.search(r"power|water|transport|ship|station|network|grid|home|shelter|repair bay|engine", full))
    mentorship_cycle = bool(re.search(r"teach(?:es|ing)?|mentor|apprentice|learns?", full) and re.search(r"robot child|childlike robot|small robot|young robot|child analogue|new apprentice|teaches? (?:the )?(?:robot|child)", full))
    seqs = architecture.get("sequences", []) if isinstance(architecture, dict) else []
    finale_text = "\n".join([_text(seqs[-2:]), _text(scenes[-5:])]).lower()
    tested_finale = bool(re.search(r"(?<!without )(?<!no )(?<!not )test(?:s|ed|ing)?|diagnostic|trial run|systems check|launch|maiden flight|flight test", finale_text))

    checks = {
        "nontransactional_shelter_or_care_in_origin": bool(re.search(r"orphan|runaway|homeless|abandoned|exile|precarious", full[:2500]) and re.search(r"shelter|food|meal|care|takes? (?:her|him|them) in|welcom", full[:3500])),
        "repair_object_competence_ladder": object_ladder,
        "learner_performs_repair_under_mentorship": learner_work,
        "skill_becomes_economic_independence": bool(re.search(r"paid|fair pay|wages?|earns?|independent workshop|own shop|commission|sells? repaired", full)),
        "belonging_is_operational_capacity": bool(re.search(r"crew needs|relies? on (?:her|him|them)|only (?:she|he|they) can|trusted mechanic|belong|place on the crew", full)),
        "war_conflict_carries_restitution_ethic": bool(re.search(r"war|invasion|battle|occupation|corporate extraction", full) and restitution_language),
        "weapon_is_repurposed_into_care_or_work_infrastructure": repurposed_weapon,
        "wealth_is_converted_into_repair_capacity": production_capacity,
        "wonder_object_becomes_usable_infrastructure": wonder_infrastructure,
        "childlike_robot_or_apprentice_completes_mentorship_cycle": mentorship_cycle,
        "finale_demonstrates_capability_through_tested_systems": tested_finale,
    }
    labels = {
        "nontransactional_shelter_or_care_in_origin": "origin lacks nontransactional shelter/care before lore, spectacle, or employment",
        "repair_object_competence_ladder": "competence is asserted rather than earned through a small-object -> machine/vehicle -> infrastructure/ship ladder",
        "learner_performs_repair_under_mentorship": "mentor solves the work or learner agency is not visible in hands-on repair",
        "skill_becomes_economic_independence": "repair skill does not become paid work or material independence",
        "belonging_is_operational_capacity": "belonging is sentimentally declared rather than operational reliance on the protagonist's capacity",
        "war_conflict_carries_restitution_ethic": "war/extraction conflict lacks restitution or repair accountability",
        "weapon_is_repurposed_into_care_or_work_infrastructure": "war machinery is spectacle rather than repurposed care/work infrastructure",
        "wealth_is_converted_into_repair_capacity": "money is terminal reward rather than converted into tools, parts, crew, or repair capacity",
        "wonder_object_becomes_usable_infrastructure": "advanced wonder remains lore/visual spectacle instead of usable infrastructure",
        "childlike_robot_or_apprentice_completes_mentorship_cycle": "mentorship cycle is not completed through a childlike robot/apprentice analogue",
        "finale_demonstrates_capability_through_tested_systems": "finale lacks tested systems, diagnostics, trial run, or demonstrated operational capability",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Constructive-restoration sci-fi works when care precedes lore, competence is earned through an escalating object ladder, mentorship preserves learner agency, wealth becomes production capacity, war is answered through restitution, and the finale proves capability through tested infrastructure rather than mere spectacle.",
    }
