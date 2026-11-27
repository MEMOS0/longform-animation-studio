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


def _affirmative_match(pattern: str, text: str) -> bool:
    for clause in re.split(r"[.!?;]", text):
        for match in re.finditer(pattern, clause):
            before = clause[:match.start()]
            if re.search(r"(?:nobody|no one|never)\s+(?:\w+\s+){0,8}$", before):
                continue
            return True
    return False


def _ending_keyed_text(value: Any) -> str:
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            key_text = str(key).lower()
            if re.search(r"ending|finale|resolution|epilogue|payoff", key_text):
                parts.append(_text(item))
            elif isinstance(item, (dict, list)):
                parts.append(_ending_keyed_text(item))
        return "\n".join(parts)
    if isinstance(value, list):
        return "\n".join(_ending_keyed_text(item) for item in value)
    return ""


def evaluate_supernatural_child_witness(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])

    child_term = bool(re.search(r"(?<![a-z])(?:child|boy|son|daughter|girl|kid)(?![a-z])", full))
    supernatural_witness = bool(re.search(
        r"supernatural|psychic|(?<![a-z])visions?(?![a-z])|past life|reincarnation|divine light|child of light|knows? secrets?|memories? (?:of|from) (?:a )?(?:dead|missing)|remembers? (?:a )?(?:dead|missing)|impossible knowledge",
        full,
    ))
    investigation_term = bool(re.search(
        r"missing|cold case|murder|disappearance|disappeared|detective|sheriff|police|officer|investigat|witness|crime|mafia|gangster|cover.?up|body|killer",
        full,
    ))
    applies = child_term and supernatural_witness and investigation_term
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    seqs = architecture.get("sequences", []) if isinstance(architecture, dict) else []
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else {}
    sequence_text = _text(seqs).lower()
    if seqs:
        ordered = "\n".join([sequence_text, scenes_text, premise_text])
    else:
        ordered = "\n".join([architecture_text, scenes_text, premise_text])

    care_pos = _pos(
        r"hospital|holds? (?:his|her) hand|comfort(?:s|ed|ing)?|care(?:s|d)? for|protect(?:s|ed|ing)?|bedside|grief|bereav|keeps? .*safe|stay(?:s|ed)? with|tucks? in|feeds?",
        ordered,
    )
    knowledge_pos = _pos(
        r"(?<![a-z])visions?(?![a-z])|knows?|remembers?|names?|secret|missing|cold case|past life|reincarnation|divine light",
        ordered,
    )

    structured_finale = "\n".join([_text(seqs[-2:]), _text(ending_payoff), _text(scenes[-3:])]).strip().lower()
    premise_finale = "\n".join([_ending_keyed_text(premise), _text(premise.get("ending_payoff", {}))]).strip().lower()
    if not structured_finale and premise.get("logline"):
        logline = str(premise.get("logline")).lower()
        clauses = re.split(r"[.!?;]\s*", logline)
        ending_clauses = [clause for clause in clauses if re.search(r"in the end|at the end|final(?:ly)?|aftermath|epilogue", clause) and re.search(r"home|safe|ordinary|family|truth|confess|together", clause)]
        premise_finale = "\n".join([premise_finale, *ending_clauses]).strip()
    fallback_finale = ordered[-max(1, len(ordered) // 3):]
    finale_text = "\n".join([structured_finale, premise_finale]).strip() or fallback_finale

    spiritual_explanation = bool(re.search(r"supernatural|psychic|(?<![a-z])visions?(?![a-z])|past life|reincarnation|divine|spiritual", full))
    natural_alternative = bool(re.search(r"trauma|imagination|grief|mental|fraud|hoax|false memory|dream", full))
    explicit_skepticism = bool(re.search(r"skeptic|doubt|not helping|doesn.?t believe|do not believe|rejects?|refuses? to believe", full))
    evidence_object = _affirmative_match(r"records?|documents?|photographs?|photos?|case file|chain of custody|testimony|witness statement|map|route|physical evidence", full)
    procedural_action = _affirmative_match(r"verify|verifies|verified|compare|review|examine|search|interview|locate|walk.*memory|follow.*(?:route|map)|check", full)

    checks = {
        "care_before_knowledge_extraction": care_pos is not None and knowledge_pos is not None and care_pos < knowledge_pos,
        "knowledge_is_socially_or_physically_dangerous": bool(re.search(r"danger|dangerous|threat|afraid|risk|hurt|kill|warning|not safe|publicly identify|expose(?:s|d)? the child|child.*(?:target|danger)|protect.*(?:child|boy|son|daughter)", full)),
        "competing_explanations_for_child_knowledge": spiritual_explanation and (natural_alternative or explicit_skepticism),
        "supernatural_clues_converted_into_procedure": evidence_object and procedural_action,
        "institutional_or_local_power_resistance": bool(re.search(r"cover.?up|powerful family|local power|mafia|gangster|institution.*(?:resist|block|protect)|authority.*(?:resist|block|protect)|town.*(?:afraid|silence|protect)|(?:sheriff|chief|department|precinct).{0,80}(?:refus|warn|block|dismiss|cover|stay out|leave .*alone)|(?:refus|warn|block|dismiss).{0,80}(?:sheriff|chief|department|precinct)", full)),
        "child_exposure_has_cost": bool(re.search(r"publicly identify|forced to identify|testify|confront|kidnap|abduct|target|afraid|scared|hurt|danger|threat|breaks down|shaking|trauma", full)),
        "confession_or_moral_truth_payoff": bool(re.search(r"confess|admit(?:s|ted)?|truth|i loved|i tried|cover.?up|what really happened|moral truth|motive|confession", finale_text)),
        "ordinary_safety_reestablished_after_mystery": bool(re.search(r"home|safe|fine|okay|ordinary|protected|leave together|go together|sleep|breakfast|with (?:his|her|their) family|family (?:home|together|reunited)", finale_text)),
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
