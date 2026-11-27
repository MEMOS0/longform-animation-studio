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


def _cooccurs_with_reference(text: str, first_pattern: str, second_pattern: str) -> bool:
    segments = [segment for segment in re.split(r"[.!?\n]", text) if segment.strip()]
    reference = r"\b(?:it|this|that)\b|\bthe (?:machine|weapon|money|payment|reward)\b"
    for index, segment in enumerate(segments):
        if re.search(first_pattern, segment) and re.search(second_pattern, segment):
            return True
        if index + 1 < len(segments):
            following = segments[index + 1]
            if re.search(first_pattern, segment) and re.search(reference, following) and re.search(second_pattern, following):
                return True
    return False


def _first_non_negated(pattern: str, text: str) -> int | None:
    for match in re.finditer(pattern, text):
        sentence_start = max(
            text.rfind(".", 0, match.start()),
            text.rfind("!", 0, match.start()),
            text.rfind("?", 0, match.start()),
            text.rfind("\n", 0, match.start()),
        ) + 1
        prefix = text[sentence_start:match.start()]
        affirmative_exception = r"\bnot only\b|\bwithout (?:assistance|help)\b"
        negated_in_match = re.search(r"\b(?:never|not|no|without|refus\w*)\b", match.group(0)) and not re.search(affirmative_exception, match.group(0))
        negated_prefix = re.search(r"\b(?:never|not|no|without|refus\w*)\b(?:\s+\w+){0,3}\s*$", prefix) and not re.search(affirmative_exception + r"\s*$", prefix)
        if not negated_in_match and not negated_prefix:
            return match.start()
    return None


def evaluate_constructive_restoration_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    narrative = "\n".join([_text(architecture), _text(scenes)]).lower()
    object_words = r"machine|robot|vehicle|ship|station|engine"
    repair_words = r"\b(?:repair(?:s|ed|ing)?|fix(?:es|ing)?|restore(?:s|d)?)\b"
    object_directed_repair = any(
        re.search(repair_words, segment) and re.search(object_words, segment)
        for segment in re.split(r"[.!?\n]", full)
    )
    repair_core = bool(re.search(r"mechanic|workshop|engineer|salvage|rebuild|restoration", full) or object_directed_repair)
    speculative_object = bool(re.search(r"\b(?:robot|android|machine|ship|starship|spaceship|station|city|drone|fleet)\b|\bai\b|war machine", full))
    applies = repair_core and speculative_object
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    small_repair = r"(?:repairs?|fixes|restores?)[^.!?\n]{0,90}(?:small object|lamp|circuit|tool|toy|radio|servo|motor)"
    mid_repair = r"(?:repairs?|fixes|restores?)[^.!?\n]{0,90}(?:robots?|vehicles?|bikes?|machines?)"
    big_repair = r"(?:repairs?|fixes|restores?)[^.!?\n]{0,90}(?:ships?|starships?|spaceships?|stations?|power grid|infrastructure)"
    def repaired_object_positions(object_pattern: str) -> list[int]:
        positions = []
        for match in re.finditer(object_pattern, narrative):
            sentence_start = max(narrative.rfind(".", 0, match.start()), narrative.rfind("!", 0, match.start()), narrative.rfind("?", 0, match.start()), narrative.rfind("\n", 0, match.start())) + 1
            segment = narrative[sentence_start:match.start()]
            action_pattern = r"\b(?:repairs?|repaired|repairing|fixes|fixed|fixing|restores?|restored|restoring)\b"
            actions = list(re.finditer(action_pattern, segment))
            if actions:
                span = segment[actions[-1].end():]
                if not re.search(r"\b(?:while|but|although|though|because|which|who)\b", span):
                    positions.append(match.start())
        return positions

    small_positions = repaired_object_positions(r"small object|lamp|circuit|tool|toy|radio|servo|motor")
    mid_positions = repaired_object_positions(r"\b(?:robots?|vehicles?|bikes?|machines?)\b")
    big_positions = repaired_object_positions(r"\b(?:ships?|starships?|spaceships?|stations?|cities)\b|power grid|infrastructure")
    object_ladder = False
    for small_pos in small_positions:
        mid_pos = next((pos for pos in mid_positions if pos > small_pos), None)
        big_pos = next((pos for pos in big_positions if mid_pos is not None and pos > mid_pos), None)
        if mid_pos is not None and big_pos is not None:
            object_ladder = True
            break
    learner_work = _first_non_negated(r"\b(?:she|he|they|learner|apprentice|protagonist)\s+(?:\w+\s+){0,2}(?:repairs?|fixes|solders?|wires?|tests?|builds?|diagnoses?|installs?)|(?:she|he|they|learner|apprentice)\s+(?:\w+\s+){0,2}(?:does|performs)\s+(?:the\s+)?(?:repair|work)", narrative) is not None
    restitution_language = bool(re.search(r"restitution|reparations?|make amends|repair the damage|rebuild what|help rebuild|compensat|accountab", full))
    weapon_pattern = r"war machine|combat unit|weapon|military robot|battle machine"
    care_use_pattern = r"repurpos|convert|care|farm|shelter|clinic|workshop|infrastructure|cook|serve|protect"
    repurposed_weapon = _cooccurs_with_reference(full, weapon_pattern, care_use_pattern)
    money_pattern = r"money|payment|paid|wages?|reward|wealth|sale|profit"
    capacity_pattern = r"parts?|tools?|workshop|repair|supplies|crew|infrastructure|production|build"
    production_capacity = _cooccurs_with_reference(full, money_pattern, capacity_pattern)
    wonder_infrastructure = bool(re.search(r"wonder|ancient|miracle|alien|advanced|hidden", full) and re.search(r"power|water|transport|ship|station|network|grid|home|shelter|repair bay|engine", full))
    mentorship_cycle = bool(re.search(r"teach(?:es|ing)?|mentor|apprentice|learns?", full) and re.search(r"robot child|childlike robot|small robot|young robot|child analogue|new apprentice|teaches? (?:the )?(?:robot|child)", full))
    seqs = architecture.get("sequences", []) if isinstance(architecture, dict) else []
    finale_text = "\n".join([_text(seqs[-2:]), _text(architecture.get("ending_payoff") if isinstance(architecture, dict) else {}), _text(scenes[-5:])]).lower()
    tested_finale = bool(re.search(r"(?<!without )(?<!no )(?<!not )\b(?:re)?tests?(?:ed|ing)?\b|diagnostic|trial run|systems check|launch|maiden flight|flight test", finale_text))

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
