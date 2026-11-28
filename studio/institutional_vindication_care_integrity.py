"""Institutional vindication through caregiving evidence integrity checks.

Derived from Fantasy Empire hit/medium/low evidence. Transparent creative
warnings, not performance predictions. Applies when a protagonist is materially
or legally condemned by an institution, re-enters through useful care/competence,
and wins restoration through evidence, procedure, autonomy, and changed conduct.
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


def evaluate_institutional_vindication_care_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    injustice = bool(re.search(r"framed|false accus|wrongful|never stole|didn.?t steal|convicted|prison|exile|court|sentence|trespass order", full))
    institution = bool(re.search(r"court|palace|royal|crown|prince|princess|council|police|hearing|judge|archive|guard|elder", full))
    care = bool(re.search(r"child|daughter|son|baby|governess|tutor|therapy|medical|healing|caregiver|protect", full))
    if not (injustice and institution and care):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    architecture_text = _text(architecture).lower()
    final_scene_text = _text(scenes[-1]).lower() if scenes else ""
    ending_parts: list[str] = []
    if isinstance(architecture, dict):
        for key, value in architecture.items():
            if re.search(r"ending|final|closing|resolution|epilogue|payoff", str(key).lower()):
                ending_parts.append(_text(value).lower())
        sequences = architecture.get("sequences") or architecture.get("sequence")
        if isinstance(sequences, list) and sequences:
            ending_parts.append(_text(sequences[-1]).lower())
    ending_text = "\n".join(ending_parts + [final_scene_text]) or (architecture_text[-max(1, len(architecture_text) // 3):] if architecture_text else full[-max(1, len(full) // 4):])

    checks = {
        "accusation_has_concrete_object_sentence_or_family_cost": bool(re.search(r"jewel|necklace|relic|receipt|signature|camera|five years|prison|sentence|baby|daughter|son|family separation|exile", full)),
        "caregiving_competence_reenters_before_status_or_romance": bool(re.search(r"governess|tutor|therapy plan|medical record|healing|adrenaline|pulse|protect|comfort|clean|caregiver|child psychology|one step at a time", full)),
        "bond_is_behaviorally_earned_not_automatic_reward": bool(re.search(r"afraid|terrified|sleep|attached|dependent|trust|breathe|safe|comfort|listen|care|protect.*before|stayed when", full)),
        "institutional_suspicion_is_procedural_not_only_villainy": bool(re.search(r"court|camera|receipt|signature|archive|medical record|guard|trespass|hearing|police|investigation|warning|procedure", full)),
        "protagonist_remains_investigative_and_sets_autonomy_boundaries": bool(re.search(r"i need the original|search|archive|records|not your cage|your choice|own feet|choose the distance|won.?t block it|not abandonment|my choice|investigate|find.*paper", full)),
        "evidence_chain_uses_documents_witnesses_or_preserved_procedure": bool(re.search(r"original transfer|paper|signature|receipt|witness|testimony|archive|medical record|police|preserve|chain of custody|black channel", full)),
        "reversal_includes_retraction_accountability_or_changed_conduct": bool(re.search(r"retract|cleared|innocent|i was wrong|sorry|apolog|conduct must change|earn it|cancel.*engagement|consequences|justice|hearing waits", ending_text)),
        "ending_restores_name_family_agency_before_status": bool(re.search(r"cleared.*name|family complete|mother|daughter|choice is mine|own name|truth is mine|no .* define|before.*crown|walk.*own feet|caregiver", ending_text)),
    }
    labels = {
        "accusation_has_concrete_object_sentence_or_family_cost": "the injustice remains vague rather than attaching to a concrete object, sentence, record, or family separation",
        "caregiving_competence_reenters_before_status_or_romance": "the protagonist re-enters through disguise or romance rather than visible care, medical, therapeutic, educational, or protective competence",
        "bond_is_behaviorally_earned_not_automatic_reward": "attachment or trust is asserted rather than built through fear, sleep, safety, listening, protection, or repeated care",
        "institutional_suspicion_is_procedural_not_only_villainy": "institutions oppose the protagonist only through villainy rather than records, courts, guards, archives, investigations, or procedure",
        "protagonist_remains_investigative_and_sets_autonomy_boundaries": "the protagonist is passively protected or rescued instead of investigating and setting explicit boundaries against protective control",
        "evidence_chain_uses_documents_witnesses_or_preserved_procedure": "truth depends on confession or confrontation rather than documents, witnesses, testimony, records, or preserved procedure",
        "reversal_includes_retraction_accountability_or_changed_conduct": "exposure is emotional only; no retraction, accountability, hearing, apology, or behavioral change follows",
        "ending_restores_name_family_agency_before_status": "the ending rewards crown/status/romance before restoring name, family, truth, or the protagonist's chosen agency",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Institutional vindication works when a concrete accusation is answered through caregiving competence, behaviorally earned attachment, procedural suspicion, investigative agency, autonomy boundaries, document/witness evidence, accountable institutional reversal, and restored name/family/agency before status.",
    }
