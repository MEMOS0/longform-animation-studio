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


def evaluate_labor_romance_power_balance_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    labor_role = bool(re.search(r"maid|assistant|servant|employee|worker|secretary|driver|cook|nanny|apprentice|crew|staff", full))
    power_holder = bool(re.search(r"billionaire|ceo|heir|boss|employer|president|rich|powerful|mafia|prince", full))
    romance = bool(re.search(r"romance|girlfriend|boyfriend|fall\w* in love|date|wife|husband|marry|marriage", full))
    hierarchy_or_concealment = bool(re.search(r"disguise|pretend|secretly|hidden identity|conceal|lied to get|male applicants|class|poor|debt|loan|contract", full))
    if not (labor_role and power_holder and romance and hierarchy_or_concealment):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    checks = {
        "entry_is_economic_necessity_not_romantic_scheme": bool(re.search(r"debt|loan|three jobs|need(?:ed)? (?:this|the)? ?job|pay(?:s)? well|rent|bills|survival|afford", full)),
        "concealment_or_class_cost_is_material": bool(re.search(r"chest|gauze|uniform|shared room|medical|hospital|injur|scar|privacy|lied to get|male applicants|exclusion|can['’]?t afford", full)),
        "employment_is_not_ownership": bool(re.search(r"don['’]?t own (?:you|her|him|them)|not (?:a|your) possession|off duty|own thing|you don['’]?t get to decide|not your job|not property", full)),
        "consent_pressure_is_named_not_romanticized": bool(re.search(r"without asking|uncomfortable|ask me first|permission|consent|don['’]?t do this|give .* space|apolog|repair|take responsibility", full)),
        "care_uses_labor_time_before_wealth": bool(re.search(r"handmade|cooked|meal|schedule|part-time job|practice|time with|shared|helping|work(?:ed)? together|gift", full)),
        "wealth_pressure_tests_autonomy": bool(re.search(r"quit.*hire|i['’]?ll hire you|buy|money|pay.*back| repayment|business deal|after your money|gold[- ]?digger|rich rival", full)),
        "protagonist_accounts_for_deception_without_class_stigma": bool(re.search(r"take responsibility|lied to get|earned (?:my|her) pay|not for money|wasn['’]?t for money|not after your money|won['’]?t admit to something i didn['’]?t do", full)),
        "ending_separates_romance_from_employment_debt": bool(re.search(r"end the contract|no penalty|separate repayment|quit.*assistant|part-time job|keep paying|own company|career|employment.*relationship|no longer.*employee", full[-5000:])),
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
