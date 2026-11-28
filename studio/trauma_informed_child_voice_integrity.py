"""Trauma-informed child voice/care integrity checks.

Derived from Story Vault Unlimited's silent-child hit/medium/low comparison.
Transparent creative warnings, not performance predictions. Applies when a
grieving or selectively silent child, care labor, communication beyond speech,
and institutional misreading drive the story.
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


def evaluate_trauma_informed_child_voice_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    child = bool(re.search(r"\b(?:child|daughter|girl|boy|kid|six-year-old|orphan|niece)\b", full))
    silence_terms = r"silent|silence|hasn.?t (?:spoken|talked|made a sound)|selective mut|nonverbal|grieving|trauma|since (?:her|his|their) mother.?s funeral|broken"
    child_terms = r"child|daughter|girl|boy|kid|orphan|niece"
    silence_or_trauma = bool(re.search(rf"(?:{child_terms})[^.\n]{{0,90}}(?:{silence_terms})|(?:{silence_terms})[^.\n]{{0,90}}(?:{child_terms})", full))
    care_labor = bool(re.search(r"nanny|maid|braid\w*|hair|comb|bedtime|school pickup|feeding|care work|caregiving", full))
    if not (child and silence_or_trauma and care_labor):
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

    forced_cure = bool(re.search(r"forces? (?:her|him|them) to speak|cure[sd]? (?:her|him|them) overnight|miracle cure|speech returns instantly without cause", full))
    checks = {
        "opening_quantifies_care_failure_and_institutional_threat": bool(re.search(r"\b(?:\d+|twelve|12)\b[^.\n]{0,80}(?:nannies|caregivers)|(?:nannies|caregivers)[^.\n]{0,80}\b(?:\d+|twelve|12)\b", full)) and bool(re.search(r"switzerland|program|send(?:ing)? (?:her|him|them) away|doctor|report|institution|trust|court|seat", full)),
        "care_is_specific_sensory_cultural_routine_not_generic_kindness": bool(re.search(r"braid\w*|cornrow|beads?|comb|hair|three strands|story|song|ritual|recipe|sign language|texture|blanket|hand", full)),
        "child_communicates_before_speech_through_multiple_channels": bool(re.search(r"laugh|laughter|point|spell|beads?|write|writing|letters?|draw|sign|gesture|chooses? (?:her|his|their) own words", full)),
        "adults_do_not_force_speech_or_treat_child_as_broken": (not forced_cure) and bool(re.search(r"not broken|never once asked|doesn.?t force|wait|ready|not one day before|let (?:her|him|them) speak|ask if (?:she|he|they) could write|choice", full)),
        "caregiver_has_independent_work_economic_cost_and_community": bool(re.search(r"maid|nanny|job|pay|wage|salon|shop|grandmother|two buses|rent|landlord|community|chair|earned|work", full)),
        "powerful_parent_moves_from_delegation_to_practiced_presence": bool(re.search(r"hired every name|signed whatever|back to the office|delegat|absent|couldn.?t walk through", full)) and bool(re.search(r"sitting on the floor|right here|not going anywhere|every saturday|learns?|practice|breakfast|bedtime|presence|stays?", full)),
        "antagonist_has_material_custody_money_or_control_motive": bool(re.search(r"trust|shares|loan|debt|money|trustee|vote|company|property|custody|control|power", full)),
        "false_evidence_is_detected_through_procedural_detail": bool(re.search(r"same sentence|same words|comma|letters?|report|doctor|witness|camera|footage|record|proof|evidence|writing|signature|false police report", full)),
        "child_testimony_or_chosen_communication_is_pivotal": bool(re.search(r"(?:she|he|they) (?:saw|wrote|spelled|said)|i saw|i'm not broken|testif|chooses? to speak|speaks? in public|puts? .*in .*hand", full)),
        "restitution_is_material_not_charity_or forgiveness": bool(re.search(r"back rent|lease|pay|wage|earned|not charity|trust|returned|withdrawn|charge.*dropped|apolog|lease|owned|receipts", full)),
        "romance_or_family_bond_remains_subordinate_to_child_safety": bool(re.search(r"not as your boss|dinner|friday|choice|consent|child|daughter|safety|care|home", full)) and not bool(re.search(r"romance (?:cures|fixes) (?:the )?child|love instantly heals", full)),
        "ending_transforms_house_or_institutional_culture": bool(re.search(r"welcome to the house|hard house once|isn.?t anymore|nobody .*tell you where to put your eyes|breakfast|new maid|set the table|home|staff kitchen|safe", ending_text)),
    }
    labels = {
        "opening_quantifies_care_failure_and_institutional_threat": "the opening does not quantify caregiver failure or establish a concrete institutional/custody threat",
        "care_is_specific_sensory_cultural_routine_not_generic_kindness": "care is generic kindness rather than a specific sensory/cultural routine the child can recognize",
        "child_communicates_before_speech_through_multiple_channels": "the child is treated as voiceless instead of communicating through laughter, gesture, writing, objects, signs, or choices",
        "adults_do_not_force_speech_or_treat_child_as_broken": "adults force speech/cure or accept the broken-child frame instead of preserving readiness and agency",
        "caregiver_has_independent_work_economic_cost_and_community": "the caregiver lacks independent labor, economic cost, community, or competence beyond the plot",
        "powerful_parent_moves_from_delegation_to_practiced_presence": "the powerful parent never moves from delegated authority to practiced daily presence",
        "antagonist_has_material_custody_money_or_control_motive": "the antagonist lacks a material custody/money/control motive",
        "false_evidence_is_detected_through_procedural_detail": "fabricated evidence is exposed by assertion rather than procedural detail, documents, witnesses, writing, or records",
        "child_testimony_or_chosen_communication_is_pivotal": "the child's chosen communication/testimony is not pivotal to truth or justice",
        "restitution_is_material_not_charity_or forgiveness": "restitution is charity/forgiveness rather than earned pay, returned property, dropped charges, apology, lease, or material repair",
        "romance_or_family_bond_remains_subordinate_to_child_safety": "romance or adult reconciliation overrides child safety, consent, and care",
        "ending_transforms_house_or_institutional_culture": "the ending restores romance/status without transforming the house or institutional culture that harmed the child",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "A trauma-informed child-voice story works when care failure and institutional threat are quantified, care is a specific sensory/cultural routine, the child communicates before speech through multiple channels, adults refuse the broken-child frame, the caregiver has independent economic/community reality, the powerful parent learns practiced presence, antagonism has material motive, false evidence is procedurally exposed, child-chosen communication is pivotal, restitution is material rather than charity, and the ending transforms the household culture.",
    }
