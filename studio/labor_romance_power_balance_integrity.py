"""Labor-romance power-balance integrity checks.

Derived from StarKiss hit/low evidence. Transparent creative warnings, not
performance prediction. Applies when intimacy develops inside employment,
debt, disguise, or class hierarchy.
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
    return [segment.strip() for segment in re.split(r"[.!?\n]", text) if segment.strip()]


def _affirmative(pattern: str, text: str) -> bool:
    negation = re.compile(r"\b(?:never|no|not|without|fails? to|doesn['’]?t|don['’]?t|didn['’]?t)\b")
    return any(re.search(pattern, segment) and not negation.search(segment) for segment in _segments(text))


def _has_consent_objection(text: str) -> bool:
    direct = re.compile(r"uncomfortable|don['’]?t do this|do not do this|refus(?:es|ed)|you (?:don['’]?t|do not) get to decide|not your job|\bstop\b")
    object_pattern = re.compile(r"\bobject(?:s|ed)?\b")
    object_negation = re.compile(r"\b(?:nobody|no one|never|without)\b")
    for segment in _segments(text):
        if direct.search(segment):
            return True
        if object_pattern.search(segment) and not object_negation.search(segment):
            return True
    return False


def evaluate_labor_romance_power_balance_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    labor_role = bool(re.search(r"\b(?:maid|assistant|servant|employee|worker|secretary|driver|cook|nanny|apprentice|crew|staff)\b", full))
    power_holder = bool(re.search(r"\b(?:billionaire|ceo|heir|boss|employer|president|rich|powerful|mafia|prince)\b", full))
    romance = bool(re.search(r"\b(?:romance|girlfriend|boyfriend|wife|husband|marriage)\b|fall\w* in love|\bmarry\b|\bdates?\b|\bdating\b", full))
    hierarchy_or_concealment = bool(re.search(r"disguise|pretend|secretly|hidden identity|conceal|lied to get|male applicants|class|poor|debt|loan|contract", full))
    if not (labor_role and power_holder and romance and hierarchy_or_concealment):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    consent_violation = bool(re.search(r"without asking|forced kiss|kiss(?:es|ed)? (?:her|him|them|the worker)|grab(?:bed|s)?|experiment on|possessive", full))
    consent_objection = _has_consent_objection(full)
    consent_repair = _affirmative(r"apolog|permission|consent|ask me first|changed behavior|consequence|repair|take responsibility|give .* space", full)
    affirmative_consent = _affirmative(r"ask(?:s|ed)? (?:for )?permission|consent(?:s|ed)?|ask me first|respect(?:s|ed)? (?:her|his|their) (?:answer|boundary|refusal)", full)

    if scenes:
        ending_text = _text(scenes[-1]).lower()
    else:
        sequences = architecture.get("sequences") if isinstance(architecture, dict) else None
        if isinstance(sequences, list) and sequences:
            ending_text = _text(sequences[-1]).lower()
        elif architecture:
            arch_text = _text(architecture).lower()
            ending_text = arch_text[-max(1, len(arch_text) // 4):]
        else:
            ending_text = full[-max(1, len(full) // 4):]
    employment_transition = bool(re.search(r"end(?:s|ed)? the contract|contract (?:is )?end(?:s|ed)|no penalty|quit(?:s|ting)? (?:the )?(?:assistant|job|employment)|no longer (?:his|her|their )?(?:assistant|employee)|employment ends|free to resign", ending_text))
    independent_livelihood = bool(re.search(r"separate repayment|repayment plan|part-time job|new job|own company|independent income|career|business", ending_text))
    romance_choice = bool(re.search(r"\b(?:girlfriend|boyfriend|relationship|romance|wife|husband)\b|\bdates?\b|\bdating\b|\bmarry\b|cho(?:ose|oses|sen)", ending_text))

    checks = {
        "entry_is_economic_necessity_not_romantic_scheme": bool(re.search(r"debt|loan|three jobs|need(?:ed)? (?:this|the)? ?job|pay(?:s)? well|rent|bills|survival|afford", full)),
        "concealment_or_class_cost_is_material": bool(re.search(r"chest|gauze|uniform|shared room|medical|hospital|injur|scar|privacy|lied to get|male applicants|exclusion|can['’]?t afford", full)),
        "employment_is_not_ownership": bool(re.search(r"(?:don['’]?t|do(?:es)? not) own (?:you|her|him|them)|not (?:a|your) possession|off duty|own thing|you (?:don['’]?t|do not) get to decide|not your job|not property", full)),
        "consent_pressure_is_named_not_romanticized": affirmative_consent or (consent_violation and consent_objection and consent_repair),
        "care_uses_labor_time_before_wealth": bool(re.search(r"handmade|cooked|meal|schedule|part-time job|practice|time with|shared|helping|work(?:ed)? together|gift", full)),
        "wealth_pressure_tests_autonomy": bool(re.search(r"quit.*hire|i['’]?ll hire you|buy|money|pay.*back| repayment|business deal|after your money|gold[- ]?digger|rich rival", full)),
        "protagonist_accounts_for_deception_without_class_stigma": bool(re.search(r"take responsibility|lied to get|earned (?:my|her) pay|not for money|wasn['’]?t for money|not after your money|won['’]?t admit to something i didn['’]?t do", full)),
        "ending_separates_romance_from_employment_debt": employment_transition and independent_livelihood and romance_choice,
    }
    labels = {
        "entry_is_economic_necessity_not_romantic_scheme": "the worker enters the labor arrangement as a romantic scheme rather than credible economic necessity",
        "concealment_or_class_cost_is_material": "disguise/class difference is a label rather than embodied privacy, safety, medical, housing, or work cost",
        "employment_is_not_ownership": "the power holder's control over labor is allowed to become ownership of body, time, dating, or affection",
        "consent_pressure_is_named_not_romanticized": "coercive kisses, grabbing, hiring pressure, or possessiveness are romanticized without objection/repair",
        "care_uses_labor_time_before_wealth": "the bond is proven through gifts/spending before labor, time, and ordinary care",
        "wealth_pressure_tests_autonomy": "wealth is only spectacle rather than a pressure test on whether the worker can choose freely",
        "protagonist_accounts_for_deception_without_class_stigma": "necessary deception is either excused completely or treated as proof of gold-digging rather than separated from labor dignity",
        "ending_separates_romance_from_employment_debt": "romance remains fused to employment/debt dependency instead of becoming a separate informed choice",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Concealed-labor romance works when economic necessity makes the job credible, employment never becomes ownership, consent pressure is named and repaired, care is labor/time before wealth, deception is accountable without class stigma, and the ending separates romance from employment/debt dependency.",
    }
