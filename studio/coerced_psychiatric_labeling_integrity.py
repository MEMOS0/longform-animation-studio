"""Coerced psychiatric-labeling integrity checks from Sienna Brooks evidence."""
from __future__ import annotations

import re
from typing import Any


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(_text(item) for item in value.values())
    if isinstance(value, list):
        return "\n".join(_text(item) for item in value)
    return ""


def evaluate_coerced_psychiatric_labeling_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    psychiatric = bool(re.search(r"mental hospital|psychiatric|schizophreni|mania|false diagnosis|mentally ill|lunatic|insane asylum|psychiatric hospital", full))
    coercion = bool(re.search(r"lock(?:ed|s)? (?:her|him|them)|confined|false imprisonment|restraint|injection|forced treatment|sign(?:ed)? (?:the )?(?:document|stake|shares)|forged signature", full))
    power = bool(re.search(r"heiress|billionaire|empire|company|group|shares|stake|assets|fortune|wealth|president|ceo", full))
    if not (psychiatric and coercion and power):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    ending_parts: list[str] = []
    if isinstance(architecture, dict):
        for key, value in architecture.items():
            if re.search(r"ending|final|closing|resolution|epilogue|payoff", str(key).lower()):
                ending_parts.append(_text(value).lower())
        sequences = architecture.get("sequences") or architecture.get("sequence")
        if isinstance(sequences, list) and sequences:
            ending_parts.append(_text(sequences[-1]).lower())
    architecture_text = _text(architecture).lower()
    end = "\n".join(ending_parts + ([_text(scenes[-1]).lower()] if scenes else [])) or (architecture_text[-max(1, len(architecture_text) // 3):] if architecture_text else "")

    checks = {
        "opening_establishes_sacrificed_labor_or_love_before_betrayal": bool(re.search(r"5 years|five years|gave up|behind the scenes|built .*line by line|helped .*build|sacrific|inheritance", full)),
        "false_diagnosis_is_publicly_weaponized_not_private_backstory": bool(re.search(r"diagnosed|announc|public|party|wedding|everyone|psychiatric expert|mental patient", full)),
        "confinement_is_linked_to_asset_or_legal_control": bool(re.search(r"30%|stake|shares|assets|sign|document|spouse|husband by law|trust fund|company|control", full)),
        "protagonist_asserts_sanity_and_legal_personhood": bool(re.search(r"i'm not sick|i am not sick|don't believe him|want to make a phone call|want to see a lawyer|lawyer|legal channels|false imprisonment", full)),
        "institutional_coercion_has_specific_material_mechanisms": bool(re.search(r"needles|restraints|no food|injections|private psychiatric hospital|room \d+|seal this place|starve|lock me up|new arrivals", full)),
        "escape_or_rescue_uses_procedure_counterpower_not_magic": bool(re.search(r"lawyers|legal channels|seal this place|find .*fast|trust fund documents|will|evidence|police|court", full)),
        "hidden_competence_is_reclaimed_through_systems_not_status_alone": bool(re.search(r"financial genius|built this system|line by line|proposal|system|wall street|president|vice president|money flows|monitoring", full)),
        "evidence_is_specific_financial_or_documentary": bool(re.search(r"money laundering|shell companies|forged signatures?|transfer records|account key|evidence|charging documents|patent theft|fraud", full)),
        "antagonist_escalation_is_material_and_accountable": bool(re.search(r"false imprisonment|money laundering|fraud|attempted murder|murder for hire|kill|eliminate|die there|court|sentenced|prison", full)),
        "restitution_includes_assets_legal_consequence_and_public_truth": bool(re.search(r"assets liquidated|surrendered|confiscated|recovered|donated|sentenced|prison|court|convictions?|charges?", end + "\n" + full[-max(1, len(full) // 3):])),
        "ending_rejects_reconciliation_and_rebuilds_self_owned_power": bool(re.search(r"didn't come .*save you|let it all go|love isn't infinite|moved on|own hands|empire|walk this road with you|not save you", end)),
        "mental_illness_is_not_used_as inherent_violence_or_comic_stigma": not bool(re.search(r"crazy people are dangerous|lunatics are violent|mental patients are monsters|hysterical woman", full)),
    }
    labels = {
        "opening_establishes_sacrificed_labor_or_love_before_betrayal": "the betrayal lacks a concrete history of sacrificed labor, love, inheritance, or invisible work",
        "false_diagnosis_is_publicly_weaponized_not_private_backstory": "the false diagnosis is private backstory rather than a public weapon that changes social reality",
        "confinement_is_linked_to_asset_or_legal_control": "confinement is cruelty without a clear asset, signature, marriage, or legal-control motive",
        "protagonist_asserts_sanity_and_legal_personhood": "the protagonist never asserts sanity, communication rights, counsel, or legal personhood",
        "institutional_coercion_has_specific_material_mechanisms": "psychiatric coercion is abstract rather than specific institutional force, restraint, medication, isolation, or hunger",
        "escape_or_rescue_uses_procedure_counterpower_not_magic": "escape/rescue happens by fiat rather than procedure, lawyers, documents, counterpower, or planned force",
        "hidden_competence_is_reclaimed_through_systems_not_status_alone": "hidden competence is a status label rather than demonstrated systems, finance, proposals, or operational skill",
        "evidence_is_specific_financial_or_documentary": "exposure relies on accusation rather than specific financial/documentary evidence",
        "antagonist_escalation_is_material_and_accountable": "antagonist escalation lacks material criminal stakes and accountability",
        "restitution_includes_assets_legal_consequence_and_public_truth": "restitution omits assets, legal consequences, or public truth",
        "ending_rejects_reconciliation_and_rebuilds_self_owned_power": "the ending rewards the abuser with reconciliation or leaves power unowned rather than self-built",
        "mental_illness_is_not_used_as inherent_violence_or_comic_stigma": "the story treats mental illness itself as inherently violent, monstrous, or comic rather than focusing on false labeling and coercive control",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "A coerced psychiatric-labeling revenge story works when false diagnosis publicly strips legal personhood to seize assets, institutional coercion is specific, the protagonist asserts sanity and counsel, escape uses procedure/counterpower, hidden competence is operationally reclaimed, exposure relies on documentary evidence, consequences are legal/material, and the ending rejects reconciliation while rebuilding self-owned power without treating mental illness itself as violence or comedy.",
    }
