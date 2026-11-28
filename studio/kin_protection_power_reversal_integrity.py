"""Kin-protection power-reversal integrity checks.

Derived from Legendary Story House hit/medium/low evidence. Transparent
creative warnings, not performance prediction.
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


def evaluate_kin_protection_power_reversal_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    kin = bool(re.search(r"sisters?|brothers?|mother|father|parents?|wife|daughter|son|family|sibling", full))
    power = bool(re.search(r"king|warden|commander|underworld|mafia|archmage|god|supreme|hidden power|legendary|sovereign|military|special operations", full))
    protection = bool(re.search(r"protect|save|avenge|revenge|bully|bullied|humiliat|threat|murder|attack|harm", full))
    if not (kin and power and protection):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    opening = full[:max(1, len(full) // 4)]
    ending_units = scenes[-max(1, min(4, len(scenes))):] if scenes else []
    if isinstance(architecture, dict):
        for key in ("ending", "ending_payoff", "resolution", "final_act"):
            if key in architecture:
                ending_units.append(architecture[key])
        if not scenes and isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
            ending_units.extend(architecture["sequences"][-max(1, min(3, len(architecture["sequences"]))):])
    ending = (_text(ending_units) or full[-max(1, len(full) // 3):]).lower()

    checks = {
        "protector_has_specific_loss_oath_or_secret_duty": bool(re.search(r"murdered|killed|oath|secret mission|top secret|years ago|disappeared|missing|imprisoned|convict|war|border|trained|found .*snow", opening)),
        "protected_kin_have_independent_roles_or_competence": bool(re.search(r"professor|doctor|ceo|director|singer|tour|pilot|financial audit|audit|knights|family .*leader|mother .*protect|wife .*help|sisters? .*stand", full)),
        "kin_threat_is_material_and_specific": bool(re.search(r"bully|bullied|humiliat|kill|murder|poison|land|debt|pension|assault|kidnap|fractures|coma|jump|captive|ransom|threat", full)),
        "protection_uses_procedure_or_verification_not_only_violence": bool(re.search(r"surveillance|evidence|records|audit|investigation|digital signature|payment records|police|backup|witness|proof|documents|verify|verified|seal off", full)),
        "kin_reciprocate_or_share_agency_in_the_fight": bool(re.search(r"sisters? .*stand in front|mother .*protect|wife .*help|let mom help|take care of you|protect .*you|we .*return safely|i won't become .*chain|children .*nothing to do", full)),
        "hidden_power_is_verified_through_public_objects_or_authority": bool(re.search(r"ring|badge|card|signet|pendant|hammer|title|commander|warden|kingpin|patriarch|national guard|state police|oracle|kneel", full)),
        "violence_is_bounded_by_a_code_or_innocence_constraint": bool(re.search(r"innocent|spare .*family|won't let anything happen|not one inmate|control your power|don't touch my family|protect all of you|won't cross|no killing .*innocent|only .*guilty", full)),
        "taboo_or_quasi_familial_intimacy_is_acknowledged_and_bounded": bool(not re.search(r"sisters? .*flirt|three against one|join us|non.?blood sisters? .*love|sister .*rest of my life", full) or re.search(r"not related by blood|not blood|boundar|consent|respect|sibling not romance|family not lover", full)),
        "antagonist_power_is_traced_to_network_or_motive": bool(re.search(r"client|paid|payment records|backer|marcus|dorian|family .*position|money|pension|insurance|contract|organization|foreign agents|land", full)),
        "ending_restores_family_safety_or_truth_before_next_hook": bool(re.search(r"free|safe|truth|verified|forgive|family again|protect|home|eliminated|evidence|arrest|return safely|never come for you", ending)),
    }
    labels = {
        "protector_has_specific_loss_oath_or_secret_duty": "the protector lacks a concrete loss, oath, secret duty, disappearance, or training debt motivating return",
        "protected_kin_have_independent_roles_or_competence": "protected relatives are helpless props rather than people with professions, judgment, combat, financial, familial, or moral competence",
        "kin_threat_is_material_and_specific": "the threat to kin is generic villainy rather than bodily, financial, territorial, legal, sexual, or custodial harm",
        "protection_uses_procedure_or_verification_not_only_violence": "protection is only force; it lacks surveillance, evidence, records, audits, investigation, witnesses, documents, or verification",
        "kin_reciprocate_or_share_agency_in_the_fight": "kin never reciprocate, protect, investigate, care, sacrifice, or share agency; they only wait to be saved",
        "hidden_power_is_verified_through_public_objects_or_authority": "hidden power is asserted rather than verified through badges, rings, cards, titles, weapons, officials, kneeling networks, or public authority",
        "violence_is_bounded_by_a_code_or_innocence_constraint": "violent power has no innocence constraint, control rule, proportionality, or protective code",
        "taboo_or_quasi_familial_intimacy_is_acknowledged_and_bounded": "quasi-familial sexualization or sibling-flirtation is used as bait without explicit non-blood status, boundaries, consent, or ethical acknowledgment",
        "antagonist_power_is_traced_to_network_or_motive": "the antagonist is a lone evil figure rather than a network with money, contracts, succession, pensions, land, clients, or institutional motive",
        "ending_restores_family_safety_or_truth_before_next_hook": "the ending escalates revenge without first restoring a concrete measure of family safety, truth, freedom, evidence, or reconciliation",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Kin-protection power reversal works when the protector returns with a specific loss/oath/secret duty, protected kin retain independent competence and reciprocal agency, threats are materially specific, hidden power is verified publicly, violence is bounded by innocence/control rules, evidence and institutions matter alongside force, antagonist networks have traceable motives, taboo family-adjacent intimacy is explicitly bounded, and each ending restores safety or truth before the next revenge hook.",
    }
