"""Meaning-system agency restoration integrity checks.

Derived from preliminary LESO Studio evidence. Transparent creative warnings, not
performance predictions. Applies when faith, spirituality, philosophy, or a
communal meaning system helps a materially precarious protagonist restore
livelihood through concrete action rather than passive miracle.
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


def evaluate_meaning_system_agency_restoration_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    meaning_hits = sum(bool(re.search(pattern, full)) for pattern in [r"god|divine", r"faith|belief", r"pray|prayer", r"church|temple|monk", r"spiritual|sacred vow|ancestor", r"philosophy|creed"])
    meaning_system = meaning_hits >= 2
    precarity = bool(re.search(r"rent|food|hunger|hungry|debt|loan|job|unemploy|application|rejected|poverty|eviction|bill", full))
    restoration = bool(re.search(r"small beginning|start where you are|skill|cook|work|business|orders|job|clients|workers|restaurant|livelihood|income|craft", full))
    if not (meaning_system and precarity and restoration):
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
        "opening_wound_is_materially_specific": bool(re.search(r"rent|food|hunger|debt|loan|job|application|rejected|eviction|bill|no money|poverty", full)),
        "belief_is_costly_or_behavioral_not_decoration": bool(re.search(r"pray|church cleaning|tithe|service|kept praying|kept believing|discipline|vow|practice|ritual|honesty|community obligation", full)),
        "turning_point_instructs_concrete_agency": bool(re.search(r"start(?:s)? where (?:you|she|he|they) (?:are|is)|small beginnings|write down|skills you already have|inventory|list(?:ing)? (?:your |her |his |their )?skills|skills you already have|first job|use what you have", full)),
        "first_opportunity_is_countable_and_executable": bool(re.search(r"\b(?:one|two|three|ten|\d+) people\b|first client|first order|cook(?:ing)? for|catering|delivery|repair job|sell(?:ing)? at|market stall|commission", full)),
        "success_scales_through_competence_operations_or_witnessed_labor": bool(re.search(r"orders|workers|clients|everything is intact|need workers|hiring|staff|reputation|deliveries", full)),
        "social_repair_requires_recognition_of_wrong": bool(re.search(r"we were wrong|cast.*aside|apolog|forgive|reconcil|admit(?:ted)?|acknowledg", ending_text)),
        "ending_protects_livelihood_dignity_or_communal_participation": bool(re.search(r"business|restaurant|job|workers|livelihood|independent|dignity|community|grateful|testimony|chosen|belong|home|secure", ending_text)),
    }
    labels = {
        "opening_wound_is_materially_specific": "the suffering is vague instead of rent, food, work rejection, debt, eviction, or another material pressure",
        "belief_is_costly_or_behavioral_not_decoration": "faith/meaning appears as decoration rather than costly practice, discipline, service, honesty, or endurance",
        "turning_point_instructs_concrete_agency": "the meaning system never instructs practical action, skill inventory, small beginnings, or same-day work",
        "first_opportunity_is_countable_and_executable": "the first opportunity is abstract rather than a countable job, client, order, meal, repair, sale, or task",
        "success_scales_through_competence_operations_or_witnessed_labor": "success arrives as unexplained miracle rather than scaling through labor, execution, reputation, clients, orders, or operations",
        "social_repair_requires_recognition_of_wrong": "social repair is absent or reduced to envy/applause without acknowledgment of exclusion or wrongdoing",
        "ending_protects_livelihood_dignity_or_communal_participation": "the ending does not secure livelihood, dignity, independent work, or communal participation beyond emotional relief",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Faith or meaning-system restoration works when transcendent endurance is joined to practical agency: material precarity, costly belief, concrete skill use, countable first work, competence-driven scaling, moral social repair, and a livelihood-protecting ending. Do not let miracle replace action.",
    }
