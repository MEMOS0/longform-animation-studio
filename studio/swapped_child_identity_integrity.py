"""Swapped-child identity/luck melodrama integrity checks.

Derived from Library of Premium Short-Form Dramas evidence. Transparent
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


def evaluate_swapped_child_identity_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    child_swap = bool(re.search(r"swapped at birth|baby swap|switched babies|real (?:daughter|heir|heiress)|false (?:daughter|heir|heiress)|secret child", full))
    status_or_power = bool(re.search(r"duke|duchess|heiress|heir|noble|lady|estate|lucky|luck|jinx|curse|blessing|chosen child", full))
    family = bool(re.search(r"mother|mom|father|dad|daughter|child|baby|aunt|family|parent", full))
    if not (child_swap and status_or_power and family):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    opening = full[:max(1, len(full) // 3)]
    ending_units = scenes[-max(1, min(3, len(scenes))):] if scenes else []
    if isinstance(architecture, dict):
        for key in ("ending", "ending_payoff", "resolution", "final_act"):
            if key in architecture:
                ending_units.append(architecture[key])
        if not scenes and isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
            ending_units.extend(architecture["sequences"][-max(1, min(2, len(architecture["sequences"]))):])
    ending = (_text(ending_units) or full[-max(1, len(full) // 3):]).lower()

    checks = {
        "swap_has_material_class_motive": bool(re.search(r"better life|duke|estate|real little lady|noble|inherit|wealth|class|fortune|lucky|good luck", opening)),
        "luck_or_blessing_has_rules_and_cost": bool(re.search(r"only works if|truly love|backfire|unlucky|bad omen|curse|jinx|disaster|mark", full)),
        "child_abuse_is_specific_and_material": bool(re.search(r"food|eat|hungry|leave me|abandon|hit|cruel|little jinx|not one good thing|locked|punish", full)),
        "identity_has_physical_or_object_evidence": bool(re.search(r"mark|ring|necklace|birthmark|scar|document|record|witness|proof|temple", full)),
        "false_child_is_not_used_as_simple_evil_object": bool(re.search(r"she's six|kids mess up|both .*children|love .*same|teach them|child.*not.*fault|protect .*both|false child.*choice", full)),
        "birth_family_coercion_becomes_active_blackmail": bool(re.search(r"keep your mouth shut|say one word|i can keep your secret|do two things|blackmail|threaten|get rid of|rumors?|nobody'?s going to know", full)),
        "loving_parent_builds_safety_and_reporting_structure": bool(re.search(r"tell me|no secrets|you can tell|protect|safe|don't be scared|i love you|both my children", full)),
        "truth_is_procedurally_uncovered": bool(re.search(r"investigat|proof|evidence|witness|record|mark|ring|rumor|cleared up|truth|found out|reveal", full)),
        "antagonist_faces_material_consequence": bool(re.search(r"pay|arrest|banish|expose|punish|consequence|lose|stripped|sent away|answer", ending)),
        "ending_restores_secure_belonging_not_only_rank": bool(re.search(r"home|family|love|mother|father|safe|belong|stay|protect", ending)),
    }
    labels = {
        "swap_has_material_class_motive": "the child swap lacks a concrete class/inheritance/luck motive",
        "luck_or_blessing_has_rules_and_cost": "luck/blessing is decorative rather than rule-bound and costly",
        "child_abuse_is_specific_and_material": "abuse is generic rather than food, abandonment, punishment, coercive labor, or material deprivation",
        "identity_has_physical_or_object_evidence": "identity depends on assertion rather than marks, rings, records, witnesses, or proof objects",
        "false_child_is_not_used_as_simple_evil_object": "the false child is treated as innately evil rather than a child shaped by adult manipulation",
        "birth_family_coercion_becomes_active_blackmail": "the birth-family threat remains passive instead of becoming blackmail, rumor, secrecy coercion, or active sabotage",
        "loving_parent_builds_safety_and_reporting_structure": "the loving parent rescues episodically without creating safety, no-secrets reporting, or durable protection",
        "truth_is_procedurally_uncovered": "the truth appears by coincidence rather than procedural evidence, witnesses, records, marks, or investigation",
        "antagonist_faces_material_consequence": "the antagonist is emotionally condemned but lacks material consequence",
        "ending_restores_secure_belonging_not_only_rank": "the ending restores rank without proving safe family belonging and ordinary child security",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Swapped-child identity melodrama works when the swap has material class motive, luck/blessing has rules and cost, abuse is materially specific, identity has proof objects, the false child is not reduced to evil, birth-family coercion becomes active blackmail, loving parents build reporting/protection structures, truth is procedurally uncovered, antagonists face material consequences, and the ending restores secure belonging beyond rank.",
    }
