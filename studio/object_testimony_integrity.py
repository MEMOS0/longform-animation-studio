"""Object-testimony and provenance-restoration integrity checks."""
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


def _affirmative_match(pattern: str, text: str) -> bool:
    for clause in re.split(r"[.!?;]|\bbut\b|\band\b", text):
        for match in re.finditer(pattern, clause):
            before = clause[:match.start()]
            if re.search(r"(?:(?:nobody|no one|never|without|not|no|doesn.?t)\s+(?:\w+\s+){0,8}|refus(?:es|ed)?\s+to\s+(?:\w+\s+){0,8}|cancel(?:s|led)?\s+(?:\w+\s+){0,4})$", before):
                continue
            return True
    return False


def evaluate_object_testimony_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    ending_source = "\n".join([architecture_text, scenes_text])
    ending = ending_source[-max(1, len(ending_source) // 3):] if ending_source else ""

    object_terms = bool(re.search(r"relic|artifact|antique|mirror|clock|watch|jewel|stone|museum object|golden eye", full))
    object_voice = bool(re.search(r"(?:objects?|relics?|artifacts?|antiques?|mirrors?|clocks?|watch(?:es)?|jewels?|stones?)\s+(?:speaks?\b(?!\s+volumes\b)|talks?|remembers?|recounts?|testif(?:y|ies)|whispers?|warns?|asks?|begs?)\b|hear(?:s|ing)?(?:\s+\w+){0,5}\s+(?:objects?|relics?|artifacts?|antiques?|mirrors?|clocks?|watch(?:es)?|jewels?|stones?)\s+(?:speaks?\b(?!\s+volumes\b)|talks?|remembers?|recounts?|testif(?:y|ies)|whispers?)\b|hear(?:s|ing)?(?:\s+\w+){0,5}\s+(?:objects?|relics?|artifacts?|antiques?|mirrors?|clocks?|watch(?:es)?|jewels?|stones?)\s+reveals?\s+(?:\w+\s+){0,5}aloud\b|whispering relics|golden eye", full))
    objects_speak = object_terms and object_voice
    testimony = bool(re.search(r"voice|whisper|speak|remember|testimony|history|memory|says|tells? (?:her|him|them)", full))
    provenance = bool(re.search(r"provenance|authentic|fake|apprais|artifact|relic|antique|museum|cultural|auction|restoration|stolen", full))
    applies = objects_speak and provenance
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    checks = {
        "object_testimony_is_limited_not_omniscient": bool(re.search(r"doesn.?t know|limited (?:memory|knowledge|testimony)|only (?:saw|heard|remembers?)|remembers? only fragments?|(?:memory|testimony) fragments?|fragments? of (?:memory|testimony|the theft|the event)|fragmented (?:memory|testimony)|partial (?:memory|testimony|knowledge)|hypothesis|lead|clue|not proof|must verify|needs? verification", full)),
        "objects_have_history_or_personhood": bool(re.search(r"(?:objects?|relics?|artifacts?|antiques?|mirrors?|clocks?|watch(?:es)?|jewels?|stones?)\s+(?:speaks?\b(?!\s+volumes\b)|remembers?|asks?|begs?|warns?|recounts?|testif(?:y|ies))\b|voice|whisper|don.?t (?:melt|smash|break|touch)|history|memory|belong", full)),
        "craft_or_labor_precedes_power": bool(re.search(r"apprais|craft|work|labor|owed|paycheck|job|competence|inspection|negotiat|expert|professional", full)),
        "magic_produces_leads_not_verdicts": _affirmative_match(r"scan|\btests?\b|\blab(?:oratory)?\b|\bct\b|fracture|x[- ]?ray|verify|independent (?:test|lab|laboratory|verification|witness|expert|chemical analysis|analysis)|chemical analysis|forensic analysis|material analysis|evidence|proof|record|document|inspect|hash|chain of custody", full),
        "verification_is_procedural": _affirmative_match(r"scan|\btests?\b|\blab(?:oratory)?\b|\bct\b|fracture|independent (?:test|lab|laboratory|verification|witness|expert|chemical analysis|analysis)|chemical analysis|forensic analysis|material analysis|police|court|lawyer|warrant|customs|task force|record|log|payment trail|chain of custody|sealed", full),
        "ownership_control_is_interrogated": bool(re.search(r"own|ownership|control|leash|gift|obedience|salary|voting rights|shares|name|independence|permission|allowance", full)),
        "protagonist_refuses_identity_absorption": bool(re.search(r"name stays|keeps? .*name|not changing .*name|independent|my own life|don.?t own me|not yours|refus|leaves? control|blood.*doesn.?t decide", full)),
        "cultural_memory_or_restoration_matters": bool(re.search(r"museum|cultural property|provenance|recovered|return(?:ed|s)?|restore(?:d|s)?|restitution|stolen .*recover|relics? .*return|artifacts? .*recover|cultural memory", full)),
        "power_creates_exploitation_risk": bool(re.search(r"wants? .*power|useful|threat|exploit|price stolen|use .*ability|target|bait|criminal|black market|smuggl", full)),
        "romance_or_family_does_not_own_future": bool(re.search(r"don.?t want .*shares|share .*future|not own|won.?t belong|independent|forgiveness|honest|choose|condition|stays", ending)),
    }
    labels = {
        "object_testimony_is_limited_not_omniscient": "object testimony is omniscient or instantly conclusive instead of limited memory/leads requiring verification",
        "objects_have_history_or_personhood": "objects are inert clues rather than history-bearing voices with vulnerability, memory, or belonging",
        "craft_or_labor_precedes_power": "supernatural ability replaces professional craft/labor instead of amplifying it",
        "magic_produces_leads_not_verdicts": "magic functions as verdict rather than producing hypotheses that material tests must verify",
        "verification_is_procedural": "public/family/legal truth lacks scans, labs, records, logs, police, custody, independent verification, or procedure",
        "ownership_control_is_interrogated": "gifts, salary, family recognition, shares, or protection are not interrogated as control structures",
        "protagonist_refuses_identity_absorption": "protagonist is absorbed into blood family, employer, romance, or institution instead of retaining chosen identity",
        "cultural_memory_or_restoration_matters": "objects remain treasure/props rather than cultural memory requiring provenance, return, recovery, or restoration",
        "power_creates_exploitation_risk": "the power has no exploitation/criminal-use risk or coercive demand",
        "romance_or_family_does_not_own_future": "ending lets romance/family own the protagonist's future rather than sharing it conditionally and freely",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Object-testimony fantasy works when objects are limited history-bearers whose voices generate leads, material/procedural verification carries public truth, craft precedes power, ownership and provenance are interrogated, and family or romance cannot absorb the protagonist's chosen identity.",
    }
