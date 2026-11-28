"""Dignified-labor craft vindication integrity checks.

Derived from the Karma Keeps Score floor-dignity hit. Transparent creative
warnings, not performance predictions. Applies when a laborer is publicly
humiliated for class/status and the resolution depends on vocational craft,
evidence, boundaries, and relational repair rather than wealth display alone.
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


def evaluate_dignified_labor_craft_vindication_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    labor = bool(re.search(r"(?:maid|servant|cleaner|nanny|worker|cook|driver|assistant|staff|laborer|janitor)", full))
    humiliation = bool(re.search(r"eat on the floor|floor girl|humiliat|mock(?:ed|ing)?|insult|degrad|shame|looked down|class humiliation|status humiliation", full))
    craft = bool(re.search(r"craft|goldsmith|smith|maker|artisan|designer|tailor|carpenter|mechanic|chef|jewel|signature|maker.?s mark|tools|workshop|father taught|skill", full))
    vindication = bool(re.search(r"proof|evidence|expos|reveal|theft|stolen|inherit|vindicat|truth|signature|hallmark|fraud|justice|apolog", full))
    if not (labor and humiliation and craft and vindication):
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
        "public_humiliation_is_specific_to_labor_status": bool(re.search(r"eat on the floor|maids eat|servant|cleaner|floor girl|not at my table|mock\w* (?:her|him|them)|humiliat\w*.*(?:maid|servant|worker|poor)", full)),
        "dependent_or_child_independently_recognizes_dignity": bool(re.search(r"child|daughter|son|kid|little girl|little boy|dependent|mother|grandmother|family", full)) and bool(re.search(r"sit beside|join|came by myself|protect|defend|kind|honest|truth|chose", full)),
        "material_stakes_are_survival_or_care_not_vanity": bool(re.search(r"hospital|medicine|bill|rent|wages|pay|debt|surgery|mother|family|work|job|feed|survive", full)),
        "protagonist_sets_boundary_against_pity_or_status_payment": bool(re.search(r"pay me for my work|not for my floor|refus|boundary|won.?t accept|not charity|earned|don.?t pity|choice|leave", full)),
        "craft_lineage_repeats_as_active_expertise": bool(re.search(r"father taught|tools|workshop|signature|maker.?s mark|read gold|test|craft|skill|made it|expert|bench|profession|apprentice", full)),
        "vindication_uses_material_evidence_or_procedure": bool(re.search(r"evidence|proof|signature|hallmark|photograph|document|bank|letter|test|maker.?s mark|witness|audit|record|police|court", full)),
        "exposure_accounts_for_theft_fraud_or_prior_deception": bool(re.search(r"theft|stolen|fraud|false accus|lie|lied|deceiv|swap|replaced|fake|brass|embezzle|frame", full)),
        "power_holder_publicly_corrects_the_household_order": bool(re.search(r"publicly|in front|thank you for coming|where my daughter eats|household|family|table|apolog|confess|arrest|correct|wrong seat|wrong table", full)),
        "ending_recontextualizes_humiliating_space_as_freely_chosen_dignity": bool(re.search(r"by choice|freely|chosen|mat|floor|table|vocation|workshop|craft|tools|family|mutual|respect|not asking the maid|mothered", ending_text)),
    }
    labels = {
        "public_humiliation_is_specific_to_labor_status": "the class wound is generic rather than a specific public labor/status humiliation",
        "dependent_or_child_independently_recognizes_dignity": "no child, dependent, or vulnerable witness independently recognizes the laborer's dignity",
        "material_stakes_are_survival_or_care_not_vanity": "material stakes are vanity/status rather than wages, care, medicine, family survival, debt, or work",
        "protagonist_sets_boundary_against_pity_or_status_payment": "the protagonist accepts pity/status transfer without an explicit boundary around earned work or consent",
        "craft_lineage_repeats_as_active_expertise": "craft lineage is backstory rather than repeated active expertise, tools, tests, signatures, or professional judgment",
        "vindication_uses_material_evidence_or_procedure": "vindication relies on revelation or power rather than material evidence, provenance, records, witnesses, or procedure",
        "exposure_accounts_for_theft_fraud_or_prior_deception": "the antagonist's theft, fraud, false accusation, or deception is not accounted for",
        "power_holder_publicly_corrects_the_household_order": "the power holder does not publicly correct the household/social order that enabled humiliation",
        "ending_recontextualizes_humiliating_space_as_freely_chosen_dignity": "the ending is wealth/status spectacle rather than freely chosen dignity, vocation, family repair, or transformation of the humiliating space",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Dignified-labor craft vindication works when a specific public class humiliation is answered through independent moral witness, survival/care stakes, boundaries against pity, repeated vocational expertise, material/provenance evidence, accounting for theft or deception, public correction of the household order, and an ending that transforms the humiliating space into freely chosen dignity rather than mere wealth reversal.",
    }
