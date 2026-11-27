"""Evidentiary withdrawal rebirth integrity checks.

Derived from NeoDrama hit/low evidence. Transparent creative warnings, not
performance prediction. Applies to rebirth/second-chance stories whose central
wound is manipulated information inside a consent-boundary or shared-space
conflict.
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


def evaluate_evidentiary_withdrawal_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    rebirth = bool(re.search(r"reborn|rebirth|past life|second chance|this time around|back on the day", full))
    shared_space = bool(re.search(r"roommate|shared (?:home|apartment|space)|lease|landlord|dormitory|co-op|communal|tenant", full))
    epistemic_wound = bool(re.search(r"edited (?:recording|clip|audio)|spliced|posted it online|spread rumors|defam|frame[ds]?\b|fake photos?|face swap|evidence", full))
    if not (rebirth and shared_space and epistemic_wound):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    evidence_sources = sum(bool(re.search(pattern, full)) for pattern in [
        r"lease|contract|rental agreement",
        r"security footage|hallway footage|camera|cctv",
        r"full recording|recorder|raw audio|original recording",
        r"screenshot|chat record|message",
        r"witness|testimony|testif",
        r"photo|metadata|timestamp",
        r"police|officer|legal|lawsuit|court",
    ])
    checks = {
        "past_wound_is_epistemic_not_only_violent": epistemic_wound,
        "rebirth_choice_is_strategic_withdrawal": bool(re.search(r"won['’]?t (?:meddle|argue|shield|save)|move out|won['’]?t rent|leave|withdraw|walk away|not my problem", full)),
        "withdrawal_does_not_mean_consent": bool(re.search(r"do(?:es)? not consent|don['’]?t consent|doesn['’]?t mean i agree|object to|without every tenant['’]?s consent|boundary", full)),
        "boundary_is_principled_not_class_contempt": bool(re.search(r"income|hometown|job status|not about money|consent|shared space|safety|women-only|tenant", full)),
        "evidence_is_multi_source_and_material": evidence_sources >= 3,
        "antagonists_self_expose_through_escalation": bool(re.search(r"show all their cards|fake photos?|hidden camera|planted|spy|debt|blackmail|kidnap|traffic|framing|confession", full)),
        "witness_network_changes_with_information": bool(re.search(r"coworker|landlord|building staff|roommates?|community safety|witness|several women|manager|neighbors?", full)),
        "prepared_code_or_survival_system_pays_off": bool(re.search(r"code|safe word|call the police|raw footage|timestamp|backup|recorder|prepared|plan", full)),
        "no_obligatory_rescue_or_forgiveness": bool(re.search(r"didn['’]?t save anyone|won['’]?t shield|not forgive|don['’]?t forgive|your choice|own it|path she chose|no reconciliation", full)),
        "closure_is_autonomy_infrastructure": bool(re.search(r"door i could close|changed the locks|new locks|long-term lease|cameras installed|rent|move back\?.*no|safe(?:r)? home|control access", full)),
    }
    labels = {
        "past_wound_is_epistemic_not_only_violent": "the past-life wound is only physical harm or generic betrayal rather than manipulated information/public belief",
        "rebirth_choice_is_strategic_withdrawal": "the reborn protagonist repeats direct confrontation instead of withdrawing from the harmful arrangement",
        "withdrawal_does_not_mean_consent": "leaving is visually/morally ambiguous because the protagonist never explicitly refuses consent to the violating arrangement",
        "boundary_is_principled_not_class_contempt": "the boundary reads as class prejudice because consent, shared-space safety, or tenant stakes are not articulated",
        "evidence_is_multi_source_and_material": "the reversal depends on one convenient recording instead of corroborating material/witness/institutional evidence",
        "antagonists_self_expose_through_escalation": "guilt is asserted or discovered externally rather than escalated into self-exposing fabrication/coercion",
        "witness_network_changes_with_information": "allies remain static or convert through speeches rather than changed information and evidence",
        "prepared_code_or_survival_system_pays_off": "rebirth knowledge stays omniscient commentary instead of becoming concrete preparedness that pays off under pressure",
        "no_obligatory_rescue_or_forgiveness": "the ending forces rescue/forgiveness of complicit people instead of letting consequences and boundaries stand",
        "closure_is_autonomy_infrastructure": "the ending stops at punishment rather than building changed access, safety, work, housing, or control over the protagonist's life",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Evidentiary withdrawal rebirth works when a protagonist destroyed by manipulated information uses the second life to withdraw without consenting, defend a principled boundary, build multi-source proof and witness infrastructure, let antagonists self-expose, refuse obligatory forgiveness, and end with control over access to her own life.",
    }
