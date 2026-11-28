"""Bonded machine-pilot integrity checks.

Derived from HUACE GLOBAL NOVA STUDIO mecha evidence. These are transparent
creative warnings for machine-companion science fiction, not performance
prediction.
"""
from __future__ import annotations

import re
from typing import Any


def _text(value: Any, key: str = "") -> str:
    lowered_key = key.lower()
    if any(marker in lowered_key for marker in ("production", "prompt", "guidance", "failure_check", "sound_design", "dialogue_design", "generation_note", "ai_generated")):
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return chr(10).join(_text(v, str(k)) for k, v in value.items())
    if isinstance(value, list):
        return chr(10).join(_text(v) for v in value)
    return ""


def evaluate_bonded_machine_pilot_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    machine = bool(re.search(r"\b(?:mecha?|robot|android|machine|ai|artificial intelligence|drone|mechanical|war machine)\b", full))
    pilot_or_war = bool(re.search(r"pilot|cockpit|neural link|invasion|war|alien|military|weapon|battle|mech", full))
    if not (machine and pilot_or_war):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    opening = full[:max(1, len(full) // 4)]
    middle = full[max(1, len(full) // 4):max(1, len(full) * 3 // 4)]
    ending_units = []
    if scenes:
        ending_units.extend(scenes[-max(1, min(5, (len(scenes) + 2) // 3)):])
    if isinstance(architecture, dict):
        for key in ("ending", "ending_payoff", "resolution", "final_act"):
            if key in architecture:
                ending_units.append(architecture[key])
        if isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
            ending_units.extend(architecture["sequences"][-max(1, min(3, (len(architecture["sequences"]) + 2) // 3)):])
    ending = (_text(ending_units) or full[-max(1, len(full) // 3):]).lower()
    climax_units = []
    if scenes:
        climax_units.extend(scenes[-max(1, min(2, len(scenes))):])
    if isinstance(architecture, dict) and isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
        climax_units.extend(architecture["sequences"][-max(1, min(2, len(architecture["sequences"]))):])
    climax = (_text(climax_units) or ending).lower()
    machine_terms = r"(?:mecha?|robot|machine|ai|android|unit|mech|companion|zero)"
    checks = {
        "ordinary_economic_identity_before_the_call": bool(re.search(r"delivery|rent|job|worker|driver|repair|shop|shift|wage|money|insurance|debt|paycheck|ordinary life", opening)),
        "machine_bond_is_selected_or_mutual_not_assignment": bool(re.search(r"choose|chooses|chosen|connect|bond|link|sync|resonat|only (?:he|she|they) can|listens? to|follows? (?:him|her|them)", full)),
        "embodied_training_precedes_competence": bool(re.search(r"train|practice|learn|walk|balance|first steps|simulation|test run|mentor|instructor|tutorial|hands off|easy", full) and re.search(r"before|first|then|after|again|until", full)),
        "civilian_relational_anchor_survives_the_mission": bool(re.search(r"mom|mother|father|sister|brother|friend|mentor|family|home|promise|civilian|child", full) and re.search(r"call|protect|rescue|return|stay with|don't let go|come home|keep .* safe", full)),
        "machine_or_creature_has_vulnerable_agency": bool(re.search(machine_terms + r"[^.\n]{0,90}(?:hurt|damaged|afraid|disobey|choose|refuse|protect|sacrifice|help|trust|feel|listen)", full) or re.search(r"(?:hurt|damaged|afraid|disobey|choose|refuse|protect|sacrifice|help|trust|feel|listen)[^.\n]{0,90}" + machine_terms, full)),
        "institution_treats_bond_as_property_or_weapon": bool(re.search(r"military|command|orders?|unauthorized|surrender|specimen|property|weapon|experiment|test subject|control|collar|terminate|asset", full)),
        "shared_load_or_sacrifice_has_physical_cost": bool(re.search(r"share the load|take my share|damage|structural failure|sacrifice|injur|burn|overload|shutdown|lose you|one more try|can't hold|cost", middle + ending)),
        "climax_requires_cooperation_not_firepower_alone": bool(re.search(r"together|stay with me|trust me|help me|hold us steady|facing it|cooperat|listen|bond|connection|link", climax) and re.search(r"attack|fire|battle|core|kill|fight|final|climax", climax)),
        "ending_gives_machine_or_pilot_identity_beyond_utility": bool(re.search(r"my name is|real name|names? them|becomes? a|no longer (?:a )?(?:weapon|tool|unit)|person|companion|friend|family|home|free", ending)),
    }
    labels = {
        "ordinary_economic_identity_before_the_call": "the pilot lacks an ordinary economic/civilian identity before the machine call",
        "machine_bond_is_selected_or_mutual_not_assignment": "the machine bond is treated as assignment rather than selection, compatibility, or mutual trust",
        "embodied_training_precedes_competence": "the pilot becomes competent without embodied training, failure, or instruction",
        "civilian_relational_anchor_survives_the_mission": "the mission has no durable civilian/familial/mentor anchor carrying emotional stakes",
        "machine_or_creature_has_vulnerable_agency": "the machine/creature is only a tool, lacking vulnerability, fear, refusal, choice, protection, or trust",
        "institution_treats_bond_as_property_or_weapon": "the institution does not create pressure by treating the bonded being as property, specimen, weapon, or asset",
        "shared_load_or_sacrifice_has_physical_cost": "the bond never becomes shared physical load, sacrifice, damage, overload, or cost",
        "climax_requires_cooperation_not_firepower_alone": "the climax is solved by firepower instead of cooperation, trust, timing, or shared control",
        "ending_gives_machine_or_pilot_identity_beyond_utility": "the ending leaves the machine/pilot as utility rather than naming identity, personhood, freedom, family, or home",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Bonded-machine science fiction works when an economically ordinary pilot is selected into a mutual machine bond, learns through embodied failure, keeps a civilian relational anchor alive, faces an institution that treats the bonded being as property, shares physical cost, wins through cooperation rather than firepower, and ends by granting identity beyond utility.",
    }
