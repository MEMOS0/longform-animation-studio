"""Consent-aware patronage/transformation melodrama integrity checks.

These heuristics encode the Kukua Asante doctrine: patronage romance is ethical
only when dependency, transfer of control, procedural competence, collapse, and
free re-choice are structurally visible. They are craft warnings, not hit predictions.
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


def evaluate_patronage_consent_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    ordered = "\n".join([architecture_text, scenes_text, premise_text])

    patronage_term = bool(re.search(r"billionaire|wealthy|rich benefactor|patron|sponsor|mentor|ceo|philanthropist", full))
    transformation_term = bool(re.search(r"transformation|model|modeling|fashion|education|training|mentorship|opportunity|international contract|career", full))
    dependency_term = bool(re.search(r"village girl|poor|humble|depends? on|indebted|owe(?:s)?|rescue|help(?:s|ed)? her|pay(?:s|ing)? for|sponsor", full))
    applies = patronage_term and transformation_term and dependency_term
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    worth_pos = _pos(r"serv(?:es?|ing)|work(?:s|ing)?|help(?:s|ing)? (?:the )?(?:women|village|family|others)|mend|repair|care(?:s|d)? for|labor", ordered)
    transformation_pos = _pos(r"transformation|school|education|model|fashion|training|runway|contract", ordered)
    collapse_pos = _pos(r"loses? everything|arrest|convict|freeze|frozen|bankrupt|downfall|prison|jail|scandal", ordered)
    choice_pos = _pos(r"marry me|she proposes|publicly asks|stand beside|return(?:s|ed)? to him|won.?t abandon|choose him|choice is him|rechoice", ordered)
    ending_text = ordered[-max(1, len(ordered) // 3):]

    checks = {
        "operational_worth_before_transformation": worth_pos is not None and transformation_pos is not None and worth_pos < transformation_pos,
        "concrete_economic_or_care_education_wound": bool(re.search(r"debt|father died|mother died|funeral expenses|school fees|couldn.?t afford|blocked education|poverty|work(?:s|ing)? to support|economic interruption", full)),
        "patronage_begins_with_consent_design": bool(re.search(r"no pressure|without pressure|private(?:ly)? decide|time to (?:talk|decide)|key is yours|boundar|accommodation|transparent|ask(?:s|ing)? consent|respect(?:s|ed)? refusal", full)),
        "transformation_is_procedural_labor": bool(re.search(r"school|education|coach|practice|rehears|training|lesson|feedback|first attempt|keeps? trying|driving lesson|voice|craft|portfolio|internship", full)),
        "dependency_suppresses_romantic_pressure": bool(re.search(r"depends? on me|cost her everything|would cost her|not ask(?:ing)? her to belong|doesn.?t want her feeling indebted|no pressure|accept refusal|saying no", full)),
        "financial_and_contract_control_transfers": bool(re.search(r"passwords?|her accounts?|control of|lawyer review|contract review|negotiat|travel arrangements|earnings|own money|paid her|professional support", full)),
        "independent_alternative_or_refusal_tests_desire": bool(re.search(r"turns? down|refus(?:es?|al)|another proposal|comfortable life|security without love|not what.*need from marriage|choose freely|free choice", full)),
        "benefactor_collapse_inverts_power_before_choice": collapse_pos is not None and choice_pos is not None and collapse_pos < choice_pos,
        "justice_or_repair_is_procedural": bool(re.search(r"evidence|lawyer|case file|appeal|bail|acquitt|signature|document|record|testimony|audit|court|original submission", full)),
        "success_returns_as_communal_consequence": bool(re.search(r"village|community|drainage|roof|school|clinic|road|local capacity|rebuild|give back|remembered where", ending_text)),
    }

    labels = {
        "operational_worth_before_transformation": "heroine is not shown serving/working/caring before beauty or career transformation",
        "concrete_economic_or_care_education_wound": "transformation lacks a concrete economic/educational wound that explains why patronage matters",
        "patronage_begins_with_consent_design": "patronage offer lacks pressure-free decision structure, boundaries, transparency, or respect for refusal",
        "transformation_is_procedural_labor": "transformation is not earned through visible training, practice, feedback, craft, or education",
        "dependency_suppresses_romantic_pressure": "the benefactor does not recognize dependency or actively suppress romantic pressure while the heroine relies on him",
        "financial_and_contract_control_transfers": "the heroine never receives meaningful control over accounts, earnings, contracts, legal review, travel, or professional support",
        "independent_alternative_or_refusal_tests_desire": "desire is never tested against an independent alternative, secure offer, or explicit refusal",
        "benefactor_collapse_inverts_power_before_choice": "the benefactor does not lose leverage before the heroine chooses him, so loyalty can read as debt repayment",
        "justice_or_repair_is_procedural": "downfall/repair lacks procedural evidence such as documents, lawyers, appeal, testimony, records, or audit",
        "success_returns_as_communal_consequence": "ending keeps success private instead of returning capacity, repair, infrastructure, or care to the community that formed her",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Patronage transformation romance works when operational worth precedes beauty, consent design mitigates dependency, control transfers before romance, collapse inverts leverage, justice remains procedural, and success returns as communal consequence.",
    }
