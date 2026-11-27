"""Serial relational-anchor integrity checks.

Derived from MoistenAI Codename J channel-format evidence. These are creative
warnings for serialized action/thriller storytelling, not performance prediction.
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


def evaluate_serial_relational_anchor_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    serial = bool(re.search(r"\b(?:season|episode|chapter|serial|series)\b", full))
    action_world = bool(re.search(r"assassin|spy|agent|mission|crime|organization|mafia|underworld|mercenary|thriller", full))
    if not (serial and action_world):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    opening_text = full[:max(1, len(full) // 4)]
    if scenes:
        ending_units = scenes[-2:]
    elif isinstance(architecture, dict) and isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
        ending_units = architecture["sequences"][-2:]
    else:
        ending_units = [full[-max(1, len(full) // 4):]]
    ending_extra = []
    if isinstance(architecture, dict):
        for key in ("ending", "ending_payoff", "resolution", "final_act"):
            if key in architecture:
                ending_extra.append(architecture[key])
    ending_text = (_text(ending_units) + "\n" + _text(ending_extra)).lower()

    relational = re.compile(r"friend|family|sister|brother|daughter|son|mother|father|mentor|lover|bond|promise|home")
    attachment_threat = re.compile(r"hostage|abduct|kidnap|bait|blackmail|manipulat|threaten|target|kill .*(?:friend|family|sister|brother|daughter|son|mother|father|lover)|loose end")
    third = max(1, len(full) // 3)
    relational_positions = [match.start() for match in relational.finditer(full)]
    relational_across_parts = bool(
        any(pos < third for pos in relational_positions)
        and any(third <= pos < third * 2 for pos in relational_positions)
        and any(pos >= third * 2 for pos in relational_positions)
    )
    checks = {
        "intimate_anchor_exists_beyond_the_mission": bool(relational.search(full)),
        "ordinary_civilian_life_has_stakes": bool(re.search(r"civilian|ordinary life|school|work|home|birthday|promise|friendship|family dinner|chosen family", full)),
        "opening_carries_relational_consequence_not_only_action": bool(relational.search(opening_text) and re.search(r"return|left|goodbye|promise|betray|grief|guilt|stranger|separat|abandon|lost|disappear", opening_text)),
        "institutional_plot_threatens_the_anchor": bool(attachment_threat.search(full) and re.search(r"organization|agency|deputy|mission|assassin|syndicate|mafia|mercenary|operation", full)),
        "antagonist_weaponizes_attachment": bool(re.search(r"kill the people .*(?:care|love)|use .* as bait|manipulat.*(?:fear|love|family|attachment)|threaten.*(?:friend|family|sister|civilian)|hostage", full)),
        "chapter_ends_on_active_turn_or_cliffhanger": bool(re.search(r"abduct|kidnap|hostage|reveal|betray|attack|choice|choose|disappear|arrest|shot|you're mine|cliffhanger|returns?|arrives?", ending_text)),
        "relational_throughline_survives_exposition": relational_across_parts,
        "operational_exposition_has_personal_cost": bool(re.search(r"guilt|grief|promise|choice|family|friend|civilian|home|ordinary life|trust|betray", full) and re.search(r"mission|operation|target|intelligence|organization|syndicate|mercenary", full)),
    }
    labels = {
        "intimate_anchor_exists_beyond_the_mission": "the serial has missions but no durable intimate anchor beyond them",
        "ordinary_civilian_life_has_stakes": "ordinary civilian life is absent, so institutional danger has no human cost",
        "opening_carries_relational_consequence_not_only_action": "the opening starts with plot/action rather than relational consequence, absence, guilt, return, or broken promise",
        "institutional_plot_threatens_the_anchor": "the institutional conspiracy does not concretely threaten the intimate/civilian anchor",
        "antagonist_weaponizes_attachment": "the antagonist attacks the protagonist directly instead of weaponizing attachment, care, or belonging",
        "chapter_ends_on_active_turn_or_cliffhanger": "the chapter/season unit ends without an active turn, revelation, abduction, choice, or cliffhanger",
        "relational_throughline_survives_exposition": "the relational throughline appears only in one section and disappears during exposition/action",
        "operational_exposition_has_personal_cost": "operational or political exposition lacks an immediate personal cost",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Serialized action works when missions are anchored in a durable intimate bond, ordinary civilian life has stakes, the opening carries relational consequence, institutional plots threaten that bond, antagonists weaponize attachment, operational exposition has personal cost, and each chapter ends on an active relational or strategic turn.",
    }
