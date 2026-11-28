"""Deprioritized-spouse power-reversal integrity checks.

Derived from Tempting Dramas hit/medium/low evidence. Transparent creative
warnings, not performance predictions. Applies when a spouse/partner repeatedly
prioritizes another woman or family obligation until the devalued partner exits
and builds independent power.
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


def evaluate_deprioritized_spouse_power_reversal_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    spouse = bool(re.search(r"wife|husband|fianc|marriage|married|bride|groom|spouse", full))
    deprioritized = bool(re.search(r"chose|priorit|another woman|mistress|first love|best friend|adopted sister|sister|surrogate|widow|protect(?:ed|ing)? her|left me|divorce|secret wife|stand-in", full))
    boundary = bool(re.search(r"walked away|leave|left|divorce|cancel(?:ed)? the wedding|disappear|cutting ties|no second chances|done playing|took his empire|power reversal|consigliere|hellcat", full))
    if not (spouse and deprioritized and boundary):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    ending_text = "\n".join([_text(architecture).lower(), _text(scenes[-1]).lower() if scenes else ""])
    checks = {
        "deprioritization_is_repeated_or_materially_costly": bool(re.search(r"seven times|eight times|again|always chose|every time|premature|hospital|ambush|life jacket|wedding|banquet|ring|empire|postponed|ignored|blisters|blood", full)),
        "rival_power_is_personal_or_structural_not_random": bool(re.search(r"adopted sister|best friend|mistress|first love|surrogate|widow|father gave his life|debt|family obligation|looks just like|stand-in|saintess", full)),
        "protagonist_boundary_is_decisive_and_behavioral": bool(re.search(r"walked away|cutting ties|done playing|cook it yourself|canceled|divorce papers|disappeared|threw.*ring|no second chances|never blow backward", full)),
        "power_reversal_comes_through_competence_position_or_alliance": bool(re.search(r"authority|power|consigliere|empire|mafia princess|commission|commercial|alliance|earned the respect|guns|fight back|protect(?:s|ed)? the kids|family business", full)),
        "late_male_regret_does_not_automatically_restore_access": bool(re.search(r"too late|no second chances|maybe|regretted everything|desperate whispers|couldn't be bothered|never meant to last|felt nothing", full)),
        "consequences_are_material_or_institutional": bool(re.search(r"empire|divorce|cutting ties|half the .* family|authority|commission|war|bankrupt|lost|position|respect|commercial empire|cost him", full)),
        "ending_preserves_self_rule_or_chosen_family_beyond_romance": bool(re.search(r"rule|authority|power|respect|chosen|children|family|real couple|happily together|no longer anyone's wife|own name|independent|safe", ending_text or full[-max(1,len(full)//4):])),
    }
    labels = {
        "deprioritization_is_repeated_or_materially_costly": "the spouse's deprioritization is a single vague slight rather than repeated or materially costly choices",
        "rival_power_is_personal_or_structural_not_random": "the rival is a random jealousy object rather than someone with personal history, debt, family obligation, resemblance, or structural leverage",
        "protagonist_boundary_is_decisive_and_behavioral": "the protagonist complains but does not enact a decisive walk-away/divorce/cancellation/no-contact boundary",
        "power_reversal_comes_through_competence_position_or_alliance": "the reversal is unexplained wealth/status rather than competence, institutional position, alliance, protection, or earned authority",
        "late_male_regret_does_not_automatically_restore_access": "the husband's regret magically reopens access instead of arriving too late or remaining uncertain",
        "consequences_are_material_or_institutional": "the fallout stays emotional rather than affecting empire, position, family power, war, money, or institutional authority",
        "ending_preserves_self_rule_or_chosen_family_beyond_romance": "the ending collapses back into romance rather than preserving self-rule, institutional identity, or freely chosen family",
    }
    warnings=[label for key,label in labels.items() if not checks[key]]
    return {"applies":True,"score_0_to_1":round(sum(checks.values())/len(checks),3),"warnings":warnings,"checks":checks,"craft_rule":"Deprioritized-spouse power reversal works when the partner repeatedly makes costly choices for a structurally powerful rival, the protagonist enacts a decisive boundary, power returns through competence/position/alliance, regret arrives without automatic access, consequences alter institutions/material power, and the ending preserves self-rule or chosen family beyond romantic reconciliation."}
