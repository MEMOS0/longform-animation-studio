"""Family-favoritism exit melodrama integrity checks."""
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


def evaluate_family_exit_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    applies = bool(re.search(r"obedient daughter|family favorit|favoritism|twin sister|dowry|left without saying goodbye|chloe.?s shadow", full))
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    premise_body = dict(premise)
    premise_body.pop("title_candidates", None)
    evidence_text = "\n".join([_text(premise_body), _text(architecture), _text(scenes)]).lower()
    seqs = architecture.get("sequences", []) if isinstance(architecture, dict) else []
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else {}
    finale_source = "\n".join([_text(seqs[-2:]), _text(ending_payoff), _text(scenes[-5:])]).strip().lower()
    finale_text = finale_source or evidence_text[-2500:]

    checks = {
        "material_inequity_evidence": bool(re.search(r"dowry|wedding dress|money|savings|jewelry|gold|card|trunk|gift", evidence_text)),
        "neglect_has_safety_cost": bool(re.search(r"hospital|blood|allerg|medical report|life[- ]threatening|doctor|illness|pain", evidence_text)),
        "chosen_family_operational_care": bool(re.search(r"mother[- ]in[- ]law|chosen family|remember(?:s|ed)? .*likes|dietary|routine|makes food|cushion|notice|care", evidence_text)),
        "quiet_procedural_exit": bool(re.search(r"leave(?:s)? the group chat|turned her phone off|left without|withdraw|no invite|deleted|missing", evidence_text)),
        "boundary_not_revenge": bool(re.search(r"not .*punish|live my own life|not in the wrong|shadow|bottom of your priorities|doing great", evidence_text)),
        "repair_not_objects_only": bool(re.search(r"i was wrong|regret|changed|wait|respect|boundar|if we have time|no longer need", finale_text)),
        "no_forced_forgiveness_reset": bool(re.search(r"feel nothing|no longer need|never be able|bounded|if we have time|not .*instantly forgive", finale_text)),
    }
    labels = {
        "material_inequity_evidence": "family favoritism is vague rather than measurable through objects/money/ritual allocation",
        "neglect_has_safety_cost": "neglect lacks a medical, safety, or irreversible cost",
        "chosen_family_operational_care": "chosen family love is asserted rather than operationalized through noticing, remembering, food, and routine",
        "quiet_procedural_exit": "exit is loud revenge rather than procedural withdrawal of access",
        "boundary_not_revenge": "protagonist does not articulate boundary as self-protection rather than punishment",
        "repair_not_objects_only": "repair relies on gifts/apology objects without changed behavior or accountability",
        "no_forced_forgiveness_reset": "ending forces emotional forgiveness instead of bounded contact inside the rebuilt life",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Family-exit melodrama works when neglect is measurable, exit withdraws access, chosen care is operational, and reconciliation remains bounded rather than a forced reset.",
    }
