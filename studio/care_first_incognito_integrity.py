"""Care-first incognito integrity checks.

Derived from Gracie/HeartTale hit/medium/low evidence. Transparent creative
warnings, not performance predictions. Applies when a romance begins through
care/rescue of a stranger whose status or identity is concealed.
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


def evaluate_care_first_incognito_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    care = bool(re.search(r"save|rescue|bandage|wound|injur|medical|nurse|care|shelter|feed|protect", full))
    stranger = bool(re.search(r"stranger|unknown man|unknown woman|mysterious|incognito|hidden identity|secretly|real identity|disguise|not knowing", full))
    romance = bool(re.search(r"romance|wife|husband|marriage|married|marry|bride|groom|fianc", full))
    status = bool(re.search(r"\b(?:billionaire|heir|ceo|boss|tycoon|prince|king|syndicate|mafia|wealthy|empire|powerful)\b", full))
    if not (care and stranger and romance and status):
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

    opening_parts: list[str] = []
    if isinstance(architecture, dict):
        for key, value in architecture.items():
            if re.search(r"opening|inciting|setup|first", str(key).lower()):
                opening_parts.append(_text(value).lower())
    opening_text = "\n".join([_text(premise).lower()] + opening_parts) or full[:max(1, len(full) // 4)]
    later_text = _text(scenes[1:]).lower() if len(scenes) > 1 else (architecture_text or full[len(full) // 3:])
    coercion_detected = bool(re.search(r"never see your|you don.?t have a choice|forced (?:you |her |him |them )?(?:into )?marr|forced marriage|threaten\w*[^.]{0,50}(?:marr|choice)|bought.*without.*discuss|didn.?t discuss it with me", full))
    repair_scan = re.sub(r"without discuss\w*|didn.?t discuss[^.]*", " ", ending_text)
    consent_scan = re.sub(r"without discuss\w*|didn.?t discuss[^.]*", " ", full)
    repair_language = bool(re.search(r"consent|freely|discuss|asked|permission|apolog|repair|no coercion|won.?t force|respect|mutual choice", repair_scan))
    consent_language = bool(re.search(r"consent|choice|freely|discuss|asked|permission|apolog|repair|no coercion|won.?t force|respect", consent_scan))

    checks = {
        "pre_romance_objective_has_material_or_moral_urgency": bool(re.search(r"surgery|medical money|rent|debt|grandmother|grandfather|mother|child|family|job|work|survive|escape|save.*before|needs \$\d|needs money", opening_text)),
        "care_act_is_visible_costly_and_before_status_revelation": bool(re.search(r"bandage|wound|blood|rescue|save[sd]? (?:him|her|them)|shelter|feed|medical skills|not knowing|before.*identity|stranger", full)),
        "identity_revelation_creates_dramatic_irony_or_recontextualizes_care": bool(re.search(r"not knowing|turns out|actually|real identity|secretly|reveal|discover|finds out|incognito|hidden identity|the same (?:man|woman)|false claim", full)),
        "protagonist_competence_repeats_beyond_initial_rescue": bool(re.search(r"medical|nurse|design|cook|sing|opera|harp|craft|investigat|work|job|skill|speech|build|repair|negotiat", later_text)),
        "protagonist_has_active_loyalty_or_agency_test": bool(re.search(r"refuse|rejects|tears? up|face to face|choice|choose|won.?t cooperate|won.?t conspire|sets? a boundary|tells? him|tells? her|leave him|leave her", full)),
        "wealth_or_power_does_not_substitute_for_consent_or_repair": consent_language and (not coercion_detected or repair_language),
        "class_dignity_is_not_only_status_adjacency": bool(re.search(r"labor|workers|farmers|builders|seamstress|community|ordinary|not ashamed|honor|dignity|competence|earned|foundation", full)),
        "ending_preserves_independent_life_vocation_family_or_freely_chosen_commitment": bool(re.search(r"independent|vocation|dream|studio|work|research|build|family|freely|choice|chosen|mutual|face to face|own name|own studio", ending_text)),
    }
    labels = {
        "pre_romance_objective_has_material_or_moral_urgency": "the opening lacks a concrete material or moral objective before the romance",
        "care_act_is_visible_costly_and_before_status_revelation": "the incognito romance is not anchored in a visible costly care/rescue act performed before status revelation",
        "identity_revelation_creates_dramatic_irony_or_recontextualizes_care": "hidden identity is label-only rather than a revelation that recontextualizes the original care or creates dramatic irony",
        "protagonist_competence_repeats_beyond_initial_rescue": "the protagonist has competence only in the inciting rescue rather than repeated craft, work, investigation, performance, or public capability",
        "protagonist_has_active_loyalty_or_agency_test": "the protagonist is protected or transferred without a meaningful loyalty, boundary, refusal, or direct agency test",
        "wealth_or_power_does_not_substitute_for_consent_or_repair": "wealth, force, capture, or unilateral gifts substitute for consent, discussion, apology, or repair",
        "class_dignity_is_not_only_status_adjacency": "class ascent merely attaches the protagonist to power instead of dignifying labor, community, competence, or ordinary people",
        "ending_preserves_independent_life_vocation_family_or_freely_chosen_commitment": "the ending is only status/wedding spectacle and does not preserve independent work, family repair, vocation, or freely chosen commitment",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Care-first incognito works when a materially urgent protagonist performs visible costly care before status revelation, the reveal recontextualizes that care through dramatic irony, competence repeats beyond rescue, agency is actively tested, wealth/power never replaces consent or repair, class dignity extends beyond status adjacency, and the ending preserves independent life or freely chosen commitment.",
    }
