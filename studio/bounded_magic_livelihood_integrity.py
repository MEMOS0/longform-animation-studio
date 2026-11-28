"""Bounded-magic livelihood restoration integrity checks.

Derived from Theatre of Dawn hit/medium/low evidence. Transparent creative
warnings, not performance predictions. Applies when supernatural power is used
to restore livelihood, business, land, trade, or productive infrastructure.
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


def evaluate_bounded_magic_livelihood_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    magic = bool(re.search(r"genie|magic|magical|wish|serum|portal|magic system|golden eye|talking objects|objects talk|dragon|spell|potion", full))
    livelihood = bool(re.search(r"farm|crops?|plant|store|shop|business|debt|wages|market|restaurant|trade|water|livelihood|empire|work|labor", full))
    restoration = bool(re.search(r"broke|debt|steal|stolen|dispossess|barren|ruin|restore|comeback|take back|rebuild|starv|precari|evict|failing business|lose[^.]{0,30}business|save[^.]{0,30}business", full))
    if not (magic and livelihood and restoration):
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
        "magic_has_explicit_limits_costs_or_prohibitions": bool(re.search(r"three wishes|one refill|refills? once|midnight|limited supply|serum is limited|no taking|no conjuring money|no messing|cannot|can.?t|interest|loan|scarce|scarcity|costs? (?:a|one|her|his|their)? ?(?:year|years|life|memory|blood|lifespan)|year of life", full)),
        "precarity_or_dispossession_is_concrete": bool(re.search(r"debt|wages|unpaid|stole|stolen|take everything|barren|barren farm|hungry|starv|rent|eviction|water|estate|embezzle|fraud", full)),
        "magic_creates_inputs_not_final_wealth": bool(re.search(r"spring water|serum|seed|plant|crop|inventory|tool|bracer|ingredient|input|refill|recipe|productive access|opportunity", full)),
        "labor_operations_and_learning_remain_necessary": bool(re.search(r"farm|plant|watering|sell|stall|market|restaurant|supply|transport|negotiat|work|labor|build|grow|harvest|deliver|trade", full)),
        "resource_conflict_uses_documents_rights_or_procedure": bool(re.search(r"deed|record|filing|water rights|contract|audit|auditor|evidence|files|fbi|police|court|procedure|verify|bank statement", full)),
        "scaling_uses_quality_scarcity_reputation_or_alliances": bool(re.search(r"quality|taste|premium|limited supply|reputation|restaurant|clients|alliance|logistics|trade empire|partners|network|supply will be very limited", full)),
        "restoration_benefits_family_community_or_dependents": bool(re.search(r"child|son|daughter|family|friends|neighbors|community|people are dying|feed|workers|clan|village|brings? water|protect", full)),
        "accountability_uses_evidence_or_institutions_not_magic_alone": bool(re.search(r"audit|auditor|arrest|fbi|police|court|evidence|files|fraud|embezzlement|vote|board|verification|law", full)),
        "ending_refuses_infinite_accumulation_and_proves_stewardship_or_self_sufficiency": bool(re.search(r"refus|turning down|not tempted|already got back|grew it (?:yourself|himself|herself)|without (?:the )?(?:serum|magic)|plain water|steward|community|independent|self-sufficient", ending_text)),
    }
    labels = {
        "magic_has_explicit_limits_costs_or_prohibitions": "magic is unbounded wish fulfillment rather than limited by rules, scarcity, cost, or prohibition",
        "precarity_or_dispossession_is_concrete": "the economic problem is generic rather than concrete debt, wage theft, dispossession, hunger, water access, fraud, or barrenness",
        "magic_creates_inputs_not_final_wealth": "magic directly conjures outcomes instead of creating inputs, access, tools, or opportunities that still require work",
        "labor_operations_and_learning_remain_necessary": "the story skips labor, operations, logistics, selling, growing, negotiation, or learning after the magical inciting event",
        "resource_conflict_uses_documents_rights_or_procedure": "resource conflict is solved by force or magic rather than rights, records, contracts, audits, evidence, or procedure",
        "scaling_uses_quality_scarcity_reputation_or_alliances": "growth is only more magic or money rather than quality, scarcity, reputation, logistics, relationships, or alliances",
        "restoration_benefits_family_community_or_dependents": "restoration enriches only the protagonist instead of protecting family, dependents, workers, community, or hungry people",
        "accountability_uses_evidence_or_institutions_not_magic_alone": "wrongdoing is punished by spectacle or magic rather than evidence, audit, law, board procedure, or institutional accountability",
        "ending_refuses_infinite_accumulation_and_proves_stewardship_or_self_sufficiency": "the ending rewards infinite accumulation rather than proving stewardship, self-sufficiency, community repair, or freedom from dependence on magic",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Bounded-magic livelihood restoration works when magic is explicitly limited, precarity is concrete, magic creates inputs rather than final wealth, labor and operations remain necessary, resource conflicts use rights/evidence/procedure, scaling comes through quality/scarcity/reputation/alliances, restoration benefits dependents/community, accountability uses institutions, and the ending refuses infinite accumulation by proving stewardship or self-sufficiency.",
    }
