"""Incognito moral-test integrity checks.

Derived from Heart Secrets hit/medium/low evidence. These are transparent
creative warnings, not performance predictions. Applies when a powerful person
uses a low-status disguise to test how others treat powerless people.
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


def _segments(text: str) -> list[str]:
    normalized = re.sub(r"\.\.\.+", "…", text)
    return [part.strip() for part in re.split(r"[.!?\n]", normalized) if part.strip()]


def _affirmative(pattern: str, text: str) -> bool:
    negation = re.compile(r"\b(?:never|no longer|not|without|fails? to|doesn['’]?t|don['’]?t|didn['’]?t)\b")
    return any(re.search(pattern, segment) and not negation.search(segment) for segment in _segments(text))


def evaluate_incognito_moral_test_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    powerful = bool(re.search(r"billionaire|governor|ceo|mother|father|parent|owner|magnate|rich|powerful|chairman|heir", full))
    disguise = bool(re.search(r"pretend|disguis|incognito|poses? as|dressed as|hidden identity|secretly|uniform|maid|cleaner|gateman|driver|homeless|stranger", full))
    moral_test = bool(re.search(r"\btest(?:s|ed|ing)?\b|how (?:she|he|they) treat|see how|moral|kindness|cruel|humiliat", full))
    low_status = bool(re.search(r"maid|cleaner|servant|worker|clerk|gateman|driver|cook|homeless|poor|unpaid|staff|employee", full))
    if not (powerful and disguise and moral_test and low_status):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    status_object = bool(re.search(
        r"gown|dress|bead|shoe|floor|room|key|pot|soup|meal|rent|wage|salary|debt|contract|motel|hotel|office|uniform|shelter|rain|storm|bill|receipt",
        full,
    ))
    powerless_conduct = bool(re.search(
        r"how (?:she|he|they) treat|treats? (?:the )?(?:maid|cleaner|worker|clerk|poor|homeless|stranger|staff)|threw (?:her|him|them) out|slap|humiliat|mock|laugh|bully|open(?:ed)? the door|shelter|fed|cover(?:ed)? the cost",
        full,
    ))
    costly_kindness = bool(re.search(
        r"out of (?:her|his|their) pay|open(?:ed)? the door|share(?:d|s)? (?:her|his|their) (?:food|meal|soup)|gave (?:her|him|them) (?:a room|shelter|food)|paid bail|bus fare|risk(?:ed|s)? (?:her|his|their) job|lost (?:her|his|their) job|cover(?:ed)? the rest|keep one room",
        full,
    ))
    material_cruelty = bool(re.search(
        r"rain|storm|slap|fired|wage|salary|debt|hospital|injur|arrest|handcuff|thrown out|locked outside|public humiliation|evict|starv|unpaid",
        full,
    ))
    test_contested = _affirmative(
        r"not your exam|never asked me|testing (?:her|him|them) was wrong|that test cost|test(?:s|ed|ing)?.{0,80}(?:wrong|cruel|manipulat|cost|ashamed|sorry|apolog)|apolog\w*.{0,80}test",
        full,
    ) or bool(re.search(r"object(?:s|ed)? to the test|son confront|daughter confront|ethics of the test", full))
    procedural_reveal = bool(re.search(
        r"label|tag|receipt|contract|key|records?|witness|evidence|timeline|invoice|bill|camera|recording|documents?|proof|tailor|rental|hired|signatures?",
        full,
    ))
    independent_restoration = bool(re.search(
        r"own (?:business|restaurant|shop|motel|company)|independent income|salary|wage|manager|promotion|repaid|account|school|training|counter at .* price|livelihood|career|voice|choice|free to refuse",
        full,
    ))
    central_engine_dominant = not bool(re.search(
        r"corporate fraud|hostile takeover|murder mystery|serial killer|alien invasion|war crimes|international conspiracy|multiple assassins|guardianship trial|police conspiracy",
        full,
    )) or bool(re.search(r"moral test|kindness|worker dignity|treats? the powerless|shelter|service labor", full))

    checks = {
        "status_object_before_test": status_object,
        "test_targets_powerless_conduct": powerless_conduct,
        "kindness_is_active_and_costly_before_reward": costly_kindness,
        "cruelty_has_material_consequences": material_cruelty,
        "covert_test_is_ethically_contested": test_contested,
        "reveal_uses_procedure_or_evidence_not_wealth_alone": procedural_reveal,
        "ending_restores_independent_dignity_and_livelihood": independent_restoration,
        "moral_test_engine_remains_dominant": central_engine_dominant,
    }
    labels = {
        "status_object_before_test": "the moral test lacks a concrete priced/labor/status object or arena before the hidden identity is exposed",
        "test_targets_powerless_conduct": "the premise tests romance/status loyalty rather than how characters treat powerless workers or strangers",
        "kindness_is_active_and_costly_before_reward": "the sympathetic character is merely nice instead of paying a visible cost before any reward",
        "cruelty_has_material_consequences": "cruelty remains verbal or symbolic rather than causing weather exposure, wage/job risk, injury, debt, arrest, or public consequences",
        "covert_test_is_ethically_contested": "covert testing is framed as automatically wise instead of being challenged as manipulative and emotionally costly",
        "reveal_uses_procedure_or_evidence_not_wealth_alone": "the reveal depends on unexplained wealth/status rather than objects, records, witnesses, timelines, contracts, or other procedure",
        "ending_restores_independent_dignity_and_livelihood": "the ending rewards the kind person with romance/wealth while leaving livelihood, voice, and independent choice unresolved",
        "moral_test_engine_remains_dominant": "corporate/legal/crime machinery overwhelms the original moral-test engine instead of serving it",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Incognito moral-test drama works when hidden power enters a vulnerable low-status role, conduct toward the powerless is tested through costly kindness and material cruelty, the covert test is ethically contested, exposure is procedural, and the ending restores independent dignity rather than merely transferring wealth or romance.",
    }
