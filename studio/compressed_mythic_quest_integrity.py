"""Compressed mythic quest integrity checks.

Derived from Moon Outlaw short-form fantasy comparison. Transparent creative
warnings, not performance predictions. Applies to compact fantasy quest or
rescue films, especially 10-30 minute pieces with serialized continuation hooks.
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


def evaluate_compressed_mythic_quest_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    fantasy = bool(re.search(r"fantasy|quest|kingdom|queen|king|dragon|orc|magic|immortal|creature|swamp|warrior|mythic|slaver|beast", full))
    quest = bool(re.search(r"quest|search|find|rescue|save|retrieve|journey|hunt|war|mission|bring back|looking for", full))
    if not (fantasy and quest):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    architecture_text = _text(architecture).lower()
    final_scene_text = _text(scenes[-1]).lower() if scenes else ""
    ending_parts: list[str] = []
    opening_parts: list[str] = []
    if isinstance(architecture, dict):
        for key, value in architecture.items():
            key_text = str(key).lower()
            if re.search(r"ending|final|closing|resolution|epilogue|payoff", key_text):
                ending_parts.append(_text(value).lower())
            if re.search(r"opening|inciting|setup|first", key_text):
                opening_parts.append(_text(value).lower())
        sequences = architecture.get("sequences") or architecture.get("sequence")
        if isinstance(sequences, list) and sequences:
            ending_parts.append(_text(sequences[-1]).lower())
            opening_parts.append(_text(sequences[0]).lower())
    ending_text = "\n".join(ending_parts + [final_scene_text]) or (architecture_text[-max(1, len(architecture_text) // 3):] if architecture_text else full[-max(1, len(full) // 4):])
    opening_text = "\n".join([_text(premise).lower()] + opening_parts) or full[:max(1, len(full) // 4)]

    checks = {
        "quest_objective_is_immediate_concrete_and_personally_staked": bool(re.search(r"find|search|rescue|save|daughter|child|flower|immortality|kingdom|home|revenge|protect|stop|destroy", opening_text)),
        "companions_have_complementary_roles_and_relationship_friction": bool(re.search(r"brother|friend|companion|partner|beast|dragon|general|mentor|rival|banter|argu|promise|loyal|protects? (?:him|her|them)", full)),
        "obstacles_escalate_and_reveal_world_or_character": bool(re.search(r"creature|orc|lizard|fire|army|dragon|slaver|trap|fog|portal|battle|enemy|trial|threshold|complication|escalat", full)),
        "spectacle_is_tied_to_choice_cost_or_protection": bool(re.search(r"protect|sacrifice|choice|cost|save|defend|innocent|people|daughter|kingdom|refus|risk|wound|death", full)),
        "lore_carries_moral_or_material_cost": bool(re.search(r"immortal|lifespan|blood|fallen|extinct|sacrifice|curse|price|cost|stolen|chains|slavery|war|destroyed|took everything", full)),
        "tonal_contract_is_explicit_for_comedy_spectacle_or_genre_mix": bool(re.search(r"tonal contract|tone:|comic relief|grounded humor|dark comic|epic adventure|genre blend|genre-mix|dramatic irony|mythic adventure", full)),
        "micro_objective_closes_before_any_series_hook": bool(re.search(r"escape|defeat|rescue|recover|return|win|survive|complete|close|answer|truth|reunite|defeated|secured|saved", ending_text)),
        "continuation_hook_is_specific_not_generic_cta": bool(re.search(r"island|next|war|queen|slaver|enemy|arrive|destination|mission|promise|unanswered|door|army|reign", ending_text)) and not bool(re.search(r"subscribe|like and follow|next episode on", ending_text)),
        "ending_changes_power_knowledge_or_relationship_state": bool(re.search(r"learn|know|truth|alliance|relationship|power|crown|queen|king|daughter|home|war|defeat|rescue|choose|choice|promise|changed", ending_text)),
    }
    labels = {
        "quest_objective_is_immediate_concrete_and_personally_staked": "the compressed quest does not establish a concrete personally staked objective immediately",
        "companions_have_complementary_roles_and_relationship_friction": "companions are interchangeable bodies rather than complementary roles with friction, loyalty, skill contrast, or banter",
        "obstacles_escalate_and_reveal_world_or_character": "obstacles feel interchangeable rather than escalating while revealing world, power rules, or character",
        "spectacle_is_tied_to_choice_cost_or_protection": "spectacle is decorative rather than tied to protection, sacrifice, choice, cost, or consequence",
        "lore_carries_moral_or_material_cost": "the lore object/world rule lacks a moral, material, or emotional cost",
        "tonal_contract_is_explicit_for_comedy_spectacle_or_genre_mix": "the architecture lacks an explicit tonal contract governing comedy, spectacle, and any genre mixture",
        "micro_objective_closes_before_any_series_hook": "the compressed film ends before closing a micro-objective, functioning only as a prologue",
        "continuation_hook_is_specific_not_generic_cta": "the continuation hook is missing, generic, or reduced to a channel call-to-action rather than a specific story question",
        "ending_changes_power_knowledge_or_relationship_state": "the ending does not change what the characters know, owe, control, or mean to each other",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Compressed mythic quests need an immediate concrete objective, complementary companions, escalating obstacles that reveal world/character, spectacle tied to cost or protection, lore with moral/material stakes, an explicit tonal contract, closure of a micro-objective before any series hook, a specific continuation question rather than a generic CTA, and an ending that changes power, knowledge, or relationship state.",
    }
