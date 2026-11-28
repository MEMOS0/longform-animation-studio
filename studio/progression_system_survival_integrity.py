"""Progression-system survival integrity checks.

Derived from Xixi Drama Studio hit/medium/low evidence. Transparent creative
warnings, not performance prediction.
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


def evaluate_progression_system_survival_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    system = bool(re.search(r"system|quest|talent|stat|level|upgrade|reward|panel|interface|check[- ]?in|island coins|choice", full))
    survival = bool(re.search(r"survival|survive|island|shipwreck|marooned|raft|apocalypse|wilderness|ocean|deserted|stranded|resource", full))
    progression = bool(re.search(r"progress|level|upgrade|evolve|reward|talent|skill|craft|build|territory|kingdom|empire", full))
    if not (system and survival and progression):
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
        "system_is_triggered_by_social_or_survival_injustice": bool(re.search(r"kicked? out|falsely accused|betray|exile|abandon|humiliat|mocked|expel|no choice|trap|stranded|shipwreck|marooned", opening)),
        "system_rules_have_quantified_limits_and_costs": bool(re.search(r"\b\d+\s*(?:times?|minutes?|hours?|days?|hooks?|uses?|coins?|points?|slots?|%|percent)\b|cooldown|stamina|hp|corruption|curse|risk|cost|penalty|deadline|consequences", full)),
        "survival_needs_are_concrete_and_recurrent": bool(re.search(r"water|food|hunger|thirst|shelter|medicine|fire|warm|cold|injur|wound|stamina|safe|sleep", full)),
        "resources_are_gathered_crafted_or_traded_procedurally": bool(re.search(r"fish|catch|craft|build|gather|scavenge|trade|cook|repair|materials?|ore|wood|tool|inventory|recipe", full)),
        "information_or_cheat_advantage_is_bounded": bool(re.search(r"only .*times?|three times?|limited|small chance|hint|warning|risk|cost|cannot|can't|immune only|limited uses|once per day|daily", full)),
        "group_politics_create_present_tense_feedback": bool(re.search(r"kicked? out|pool .*supplies|ration|share|leader|follow orders|team|camp|trade|beg|threat|spy|join|loyal|protect|community|classmates?", full)),
        "power_growth_creates_obligations_not_only_domination": bool(re.search(r"keep .*alive|protect|shelter|feed|share|rescue|responsib|depend|followers|community|subjects|allies|build .*for|help", full)),
        "threats_escalate_through_ecology_or_institutions": bool(re.search(r"storm|beast|snake|crocodile|cannibal|cult|curse|night demon|system announcement|penalty|elimination|predator|deity|tribe|wild beast", full)),
        "sexual_or_gendered_coercion_is_not_rewarded_as_romance": bool(not re.search(r"take your pick of .*women|women .*deserve|girl pays in labor|sexual favor|sleep with me .*food|force .*women|coerce .*women", full) or re.search(r"illegal|stop|consequence|punish|protect|rescue|not consent|threat", full)),
        "ending_closes_a_local_loop_before_the_next_hook": bool(re.search(r"enough|supplies|shelter|camp|reward|unlock|plan|deal|alliance|cure|lift|escape|protect|community|safe|built|food|water|fish|quest complete|level", ending)),
    }
    labels = {
        "system_is_triggered_by_social_or_survival_injustice": "the system appears as arbitrary power fantasy rather than an answer to expulsion, false accusation, betrayal, stranding, or survival injustice",
        "system_rules_have_quantified_limits_and_costs": "the system lacks countable uses, resources, stamina, corruption, deadlines, penalties, or other constraining costs",
        "survival_needs_are_concrete_and_recurrent": "survival is abstract rather than recurring water, food, shelter, medicine, warmth, injury, stamina, or sleep pressure",
        "resources_are_gathered_crafted_or_traded_procedurally": "resources arrive by declaration instead of fishing, crafting, gathering, scavenging, cooking, trading, building, or material procedure",
        "information_or_cheat_advantage_is_bounded": "the cheat/information advantage is unlimited and therefore drains uncertainty instead of creating bounded tactical choices",
        "group_politics_create_present_tense_feedback": "the cast is decorative because rationing, expulsion, loyalty, leadership, trade, camp politics, or communal feedback do not alter survival choices",
        "power_growth_creates_obligations_not_only_domination": "power growth only dominates others instead of creating protection, feeding, sheltering, rescue, responsibility, or community obligations",
        "threats_escalate_through_ecology_or_institutions": "threats do not escalate through weather, beasts, curses, tribes, cults, system penalties, or institutional pressure",
        "sexual_or_gendered_coercion_is_not_rewarded_as_romance": "gendered survival leverage or sexual coercion is framed as reward/romance rather than violation, threat, or conduct with consequences",
        "ending_closes_a_local_loop_before_the_next_hook": "the ending only teases escalation without first closing a local resource, threat, alliance, cure, shelter, or quest loop",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Progression-system survival works when system power answers a concrete social/survival injustice, rules have quantified limits and costs, water/food/shelter/medicine pressures recur, resources are procedurally gathered or traded, cheat knowledge is bounded, group politics feeds back into survival, power creates obligations, threats escalate ecologically or institutionally, gendered coercion is not rewarded, and each phase closes a local resource/threat/relationship loop before opening the next escalation hook.",
    }
