"""Community/scale-fantasy repair integrity checks.

Encodes the Drakenhart tiny-kingdom breakout doctrine as transparent creative
review heuristics: scale should alter infrastructure/economics, outsider trust
should be historically costly, competence should protect the community early,
extraction should be stopped through proof where possible, and endings should
show sustained rebuilding/chosen home.
"""
from __future__ import annotations

import re
from typing import Any


def flatten(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(flatten(v) for v in value.values())
    if isinstance(value, list):
        return "\n".join(flatten(v) for v in value)
    return ""


def evaluate_scale_community_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = flatten(premise).lower()
    arch_text = flatten(architecture).lower()
    scene_text = flatten(scenes).lower()
    full = "\n".join([premise_text, arch_text, scene_text])
    applies = bool(re.search(r"tiny|small kingdom|hidden kingdom|underground|scale|miniature|root city|hidden city|village|community", full))
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    checks = {
        "scale_changes_material_economics": bool(re.search(r"junk|bottle caps?|roof|infrastructure|building materials?|repair|rebuild|water|food|tools?|work|labor|shelter|shared", full)),
        "early_practical_competence_save": bool(re.search(r"save|protect|repair|holds?|arch|build|fix|rescue", full[: max(2500, len(full) // 2)])),
        "outsider_trust_has_historical_cost": bool(re.search(r"guilty|guilt|blame|distrust|floods?|caused|signing them away|institutional|company|report|betray|trust .*(?:giant|outsider)|make it right", full)),
        "proof_or_persuasion_stops_extraction": bool(re.search(r"map|proof|evidence|show them|make them listen|shut it down|stop(?:s|ped)? drilling|pack it up|persuad", full)),
        "sustained_repair_or_chosen_home": bool(re.search(r"rebuild|build smarter|chosen home|this is my home|every sunrise|community|shared|belonging|stay(?:s|ed)?|return(?:s|ed)?", full[-max(2500, len(full) // 2):])),
    }
    labels = {
        "scale_changes_material_economics": "scale/community fantasy does not yet make size materially economic through infrastructure, labor, objects, or survival systems",
        "early_practical_competence_save": "outsider competence is not clearly proven through an early practical community-protecting action",
        "outsider_trust_has_historical_cost": "community trust lacks a rational historical or institutional cost",
        "proof_or_persuasion_stops_extraction": "extraction/threat is not clearly stopped through proof, knowledge, or persuasion; check whether violence is substituting for infrastructure causality",
        "sustained_repair_or_chosen_home": "ending lacks sustained rebuilding, shared repair, return, or chosen-home evidence",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    score = round(sum(checks.values()) / len(checks), 3)
    return {"applies": True, "score_0_to_1": score, "warnings": warnings, "checks": checks}
