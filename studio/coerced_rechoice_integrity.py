"""Coerced-origin hidden-identity free re-choice integrity checks."""
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


def _immediate_negation_before(text: str, start: int) -> bool:
    before = text[max(0, start - 70):start]
    return bool(re.search(r"(?:will not|won.?t|does not|doesn.?t|do not|don.?t|never)\s+(?:\w+\s+){0,2}$", before))


def _positions(pattern: str, text: str) -> list[int]:
    return [match.start() for match in re.finditer(pattern, text)]


def _unnegated_positions(pattern: str, text: str) -> list[int]:
    return [match.start() for match in re.finditer(pattern, text) if not _immediate_negation_before(text, match.start())]


def evaluate_coerced_rechoice_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    ending_source = "\n".join([architecture_text, scenes_text])
    ending = ending_source[-max(1, len(ending_source) // 3):] if ending_source else ""

    marriage = bool(re.search(r"marry|marriage|husband|wife|bride|wedding", full))
    coercion = bool(re.search(r"forced|coerce|blackmail|in exchange|leverage|threat|took .*children|missing (?:twins|children)|no choice|contract marriage|fake marriage|arranged marriage|marri(?:ed|age).*contract", full))
    hidden_status = bool(re.search(r"hidden identity|secretly rich|billionaire|trillionaire|ceo|poor single dad|disguise|scar|driver|hiding who|amnesiac heiress|secret heiress|true heiress|lost heiress|imposter|impostor", full))
    applies = marriage and coercion and hidden_status
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    pressure_strong_positions = _positions(
        r"stand(?:s)? with (?:you|her|the victim|the wife|nora)|accept(?:s|ed)? (?:her|your) refusal|respect(?:s|ed)? (?:her|your) refusal|family approval.*not.*consent|mother.*not.*consent|board.*not.*consent|pressure.*not.*consent|choice.*not.*family",
        full,
    )
    pressure_weak_positions = _positions(r"won.?t pressure|don.?t pressure|no one can force|free to refuse", full)
    pressure_adverse_positions = _unnegated_positions(
        r"stand(?:s)? with (?:him|the ceo|ceo|the husband)|insist(?:s|ed)?\s+(?:\w+\s+){0,4}stay married|pressure(?:s|d)?\s+(?:\w+\s+){0,4}stay married|(?:force(?:s|d)?|compel(?:s|led)?|coerce(?:s|d)?|blackmail(?:s|ed)?)\s+(?:\w+\s+){0,5}(?:stay married|marry|marriage)",
        full,
    )
    pressure_positive_positions = pressure_strong_positions + pressure_weak_positions
    pressure_is_bounded = bool(pressure_positive_positions) and (
        not pressure_adverse_positions
        or any(position > max(pressure_adverse_positions) for position in pressure_strong_positions)
    )

    retaliation_positive_positions = _positions(
        r"doesn.?t owe|not owe|deal stands|no retaliation|won.?t (?:pull|withdraw|weaponize)|will not (?:pull|withdraw|weaponize)|continue(?:s|d)? support|business is business|support.*despite rejection",
        full,
    )
    retaliation_adverse_positions = _unnegated_positions(
        r"(?:cuts?|pulls?|withdraws?|weaponizes?|cancels?)\s+(?:\w+\s+){0,4}(?:funding|support|technology|consultants|deal|business contract)|after rejection.{0,80}(?:cuts?|pulls?|withdraws?|weaponizes?|cancels?).{0,40}(?:funding|support|technology|consultants|deal|business contract)",
        full,
    )
    power_is_bounded = bool(retaliation_positive_positions) and (
        not retaliation_adverse_positions
        or any(position > max(retaliation_adverse_positions) for position in retaliation_positive_positions)
    )

    checks = {
        "coercion_has_concrete_leverage": bool(re.search(r"missing (?:twins|children)|children.*force|in exchange|blackmail|leverage|threat|tuition|debt|custody", full)),
        "disguise_has_survival_or_trauma_function": bool(re.search(r"scar|assault|protect|afraid|test|trust|hide|hiding|survive|safety", full)),
        "attachment_forms_before_status_reveal": bool(re.search(r"before (?:he|she) knows|doesn.?t know|unaware|ordinary|poor|broke|package deal|partnership|children|twins|bedtime|work", full)),
        "procedural_evidence_and_accountability": bool(re.search(r"evidence|footage|complaint|attorney|lawyer|police|investigation|records?|test|verification|arrest|court|clinic", full)),
        "money_is_not_accepted_as_substitute_repair": bool(re.search(r"money was never the wound|not signing away|property|assets|fortune|wealth.*not|can.?t buy|not a bribe", full)),
        "anger_or_coercion_is_not_erased": bool(re.search(r"anger|coercion|forced|lie was|betrayal|not forgive|trust wound|no more lies", full)),
        "agency_or_control_is_restored": bool(re.search(r"marital assets|control|choice|choose|decide|decision|consent|without consent|sign|contract|documents?", full)),
        "explicit_truth_before_final_choice": bool(re.search(r"tell me the truth|deserve the truth|no more lies|no more hiding|truth", full)),
        "transactional_intimacy_is_bounded": bool(re.search(r"sell.*skills.*not.*body|not.*selling.*body|no sex|sexual boundary|boundar|separate room|professional|consent|not.*owe.*body", full)),
        "pressure_is_not_consent_substitute": pressure_is_bounded,
        "power_is_not_weaponized_after_rejection": power_is_bounded,
        "final_choice_is_partnership_not_rescue": bool(re.search(r"partner, not (?:my )?rescuer|choose you|freely choose|may i|ask|no force|not my rescuer|rechoice|when you are ready", ending)),
    }
    labels = {
        "coercion_has_concrete_leverage": "coerced relationship lacks concrete leverage such as children, debt, tuition, custody, blackmail, or threat",
        "disguise_has_survival_or_trauma_function": "hidden-identity disguise has no survival, trust-testing, trauma, or safety function beyond author convenience",
        "attachment_forms_before_status_reveal": "relationship does not form around ordinary care/partnership before wealth or status revelation",
        "procedural_evidence_and_accountability": "truth and consequences are asserted without evidence, investigation, records, legal procedure, or accountability",
        "money_is_not_accepted_as_substitute_repair": "money/property risks becoming a substitute apology rather than one component of restored agency",
        "anger_or_coercion_is_not_erased": "the story erases anger or the original coercion once romance/wealth is revealed",
        "agency_or_control_is_restored": "the coerced partner does not regain meaningful choice, control, documents, assets, or decision rights",
        "explicit_truth_before_final_choice": "final romantic choice occurs without explicit truth and no-more-lies conditions",
        "transactional_intimacy_is_bounded": "transactional or contracted intimacy lacks explicit body/sex/professional boundaries",
        "pressure_is_not_consent_substitute": "family, board, or social pressure is treated as consent instead of being bounded by the affected person's free refusal",
        "power_is_not_weaponized_after_rejection": "the powerful partner does not prove that romantic rejection will not trigger withdrawal, retaliation, or leverage",
        "final_choice_is_partnership_not_rescue": "ending does not convert the coerced relationship into an explicit free partnership/re-choice",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Coerced hidden-identity romance becomes durable when the original coercion remains a wound, truth is procedurally proven, money does not erase anger, agency/control is restored, transactional intimacy is bounded, rejection does not trigger retaliation, and the ending is a free partnership re-choice rather than rescue absorption.",
    }
