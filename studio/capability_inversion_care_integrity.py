"""Capability-inversion care-romance integrity checks.

Derived from VistaVerse hit/low evidence. Transparent creative warnings, not
performance prediction. Applies when a stigmatized physical capability becomes
care/protection labor for a disabled or injured powerful person.
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
    negation = re.compile(r"\b(?:never|no longer|not|without|fails? to|doesn['’]?t|don['’]?t|didn['’]?t|forced)\b|\bno\s+choice\b")
    return any(re.search(pattern, segment) and not negation.search(segment) for segment in _segments(text))


CAPABILITY_PATTERN = re.compile(
    r"superhuman strength|freakishly strong|extraordinary strength|unnatural strength|inhuman strength|super strength|"
    r"strength (?:of|to) (?:ten|10)|knock(?:s|ing)? out .*pigs|powerful body|enhanced body|extraordinary physical power"
)
STIGMA_PATTERN = re.compile(r"freak|monster|abnormal|can't control|cannot control|damage|destroy|liabil|reject|mock|stigma|labeled")


def _has_stigmatized_capability(text: str) -> bool:
    segments = _segments(text)
    for index, segment in enumerate(segments):
        window = " ".join(segments[max(0, index - 1):index + 2])
        if CAPABILITY_PATTERN.search(window) and STIGMA_PATTERN.search(window):
            return True
    return False


def evaluate_capability_inversion_care_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    capability = bool(CAPABILITY_PATTERN.search(full))
    stigma = _has_stigmatized_capability(full)
    disability_or_injury = bool(re.search(r"wheelchair|disabled|paralyz|broken leg|injur|illness|blind|cannot walk|can't walk", full))
    care_or_romance = bool(re.search(r"bodyguard|caregiver|caretaker|protect|romance|fall\w* in love|girlfriend|boyfriend|wife|husband", full))
    if not (capability and stigma and disability_or_injury and care_or_romance):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    if scenes:
        ending_units = scenes[-2:]
    elif isinstance(architecture, dict) and isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
        ending_units = architecture["sequences"][-2:]
    else:
        ending_units = [full[-max(1, len(full) // 4):]]
    ending_extra = []
    if isinstance(architecture, dict):
        for key in ("ending", "ending_payoff", "resolution", "final_act"):
            if key in architecture:
                ending_extra.append(architecture[key])
    ending_text = (_text(ending_units) + "\n" + _text(ending_extra)).lower()

    checks = {
        "ability_is_costly_before_it_is_valuable": bool(re.search(r"freak|can't control|cannot control|damage|insurance|no job|fired|trouble|mock|rejected|labeled", full)),
        "labor_revalues_ability_as_protection_not_domination": bool(re.search(r"bodyguard|protect|security assistant|hired|care assistance|keep .* safe|escort", full)),
        "care_restores_agency_rather_than_infantilizing": bool(re.search(r"not.*only be taken care|do it yourself|your legs.*decide|practice|tool|agency|you can|stand.*own|independent", full)),
        "disabled_person_retains_desire_competence_and_interiority": bool(re.search(r"cook|plan|business|work|decide|want|feel|confess|choice|protect|support|not.*object", full)),
        "caregiver_has_independent_labor_dignity": bool(re.search(r"farm|pig|butcher|parents|clean and honest|earn .* money|own two hands|home|labor|work", full)),
        "class_or_gender_inversion_creates_mutual_learning": bool(re.search(r"wealthy|estate|city|country|farm|street food|class|rich|poor|rural|homemade|local market", full)),
        "intimacy_is_renegotiated_beyond_the_job": _affirmative(r"job.*done|reason to stay|leave|bodyguard.*girlfriend|girlfriend|boyfriend|confess|like you|choice", ending_text),
        "consent_pressure_is_named_or_avoided": _affirmative(r"consent|permission|uncomfortable|reject|choice|if you don't want|hide .*feelings|asks? first|respect", full),
        "ending_preserves_independent_livelihood_or_work_choice": _affirmative(r"earn .* money|own money|job|work|career|bodyguard|choose|choice", ending_text),
    }
    labels = {
        "ability_is_costly_before_it_is_valuable": "the ability is immediately useful rather than first carrying social, bodily, or economic cost",
        "labor_revalues_ability_as_protection_not_domination": "the ability is not revalued through credible protection/care labor",
        "care_restores_agency_rather_than_infantilizing": "care treats the disabled/injured person as a dependent object instead of rebuilding agency and choice",
        "disabled_person_retains_desire_competence_and_interiority": "the disabled/injured person lacks desire, competence, plans, or interiority beyond being rescued",
        "caregiver_has_independent_labor_dignity": "the caregiver has no independent labor, family, home, or economic dignity outside the powerful person",
        "class_or_gender_inversion_creates_mutual_learning": "the inversion is decorative rather than forcing both people to learn across class, labor, gender, or environment",
        "intimacy_is_renegotiated_beyond_the_job": "the romance never distinguishes love from the employment/care arrangement",
        "consent_pressure_is_named_or_avoided": "romantic or sexual pressure is not named as a choice/consent problem",
        "ending_preserves_independent_livelihood_or_work_choice": "the ending collapses the caregiver into dependency instead of preserving work or livelihood choice",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Capability-inversion care romance works when stigmatized ability is first costly, protection labor revalues it without making the caregiver a servant, care restores agency rather than infantilizing, the disabled person retains competence/desire/interiority, both people learn across class or gender inversion, and intimacy is renegotiated as consenting choice beyond the job.",
    }
