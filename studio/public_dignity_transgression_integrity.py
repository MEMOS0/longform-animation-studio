"""Public dignity-transgression integrity checks.

Derived from HeartScene hit/medium/low comparison. Transparent creative
warnings, not performance predictions. Applies when a public slap, humiliation,
or status-based misjudgment detonates a contemporary social/family/business
arena and the story is about verification, dignity, proportionate consequence,
and aftermath rather than simple revenge spectacle.
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


def evaluate_public_dignity_transgression_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    transgression = bool(re.search(r"\b(?:slap(?:ped|s|ping)?|hit|struck|strike|assault(?:ed)?|humiliat\w*|insult\w*)\b", full))
    public_arena = bool(re.search(r"\b(?:public|engagement|party|wedding|guests?|crowd|ballroom|venue|ceremony|family event|workplace)\b", full))
    status_misread = bool(re.search(r"beneath|dress|appearance|impostor|liar|thief|class|status|respect|dignity|look(?:s|ed)? like|pretend", full))
    consequence = bool(re.search(r"consequence|fired|engagement (?:is )?over|complaint|footage|evidence|truth|verify|investigat|legal", full))
    if not transgression or sum([public_arena, status_misread, consequence]) < 2:
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

    cruel_revenge = bool(re.search(r"enjoys? (?:her|his|their) suffering|laughs? while (?:she|he|they) suffer|destroy (?:her|his|their) life for fun|revenge is enough", full))
    checks = {
        "transgression_is_public_status_violence_not_random_action": bool(re.search(r"(?:slap\w*|hit|struck|assault\w*|humiliat\w*|insult\w*)[^.\n]{0,180}(?:public|guests?|crowd|engagement|party|ballroom|beneath|dress|class|respect|dignity)|(?:public|guests?|crowd|engagement|party|ballroom|beneath|dress|class|respect|dignity)[^.\n]{0,180}(?:slap\w*|hit|struck|assault\w*|humiliat\w*|insult\w*)", full)),
        "target_offers_explanation_or_verification_before_escalation": bool(re.search(r"offered? (?:an )?explanation|call (?:my |your |the )?(?:son|daughter|husband|wife|manager)|contact|verify|proof|invitation|establish the facts|confirm(?:ing)? who", full)),
        "authority_judges_values_not_status_or_appearance": bool(re.search(r"not when you are wrong|values|basic respect|beneath|way (?:she|he|they) (?:was|is) dressed|dignity|unworthy|judg\w+ .*appearance|values i no longer trust", full)),
        "bystanders_and_enablers_are_confronted": bool(re.search(r"rest of you|not one of you|everyone (?:watched|staring)|bystander|joined (?:a )?public humiliation|afraid to disagree|tolerate .*behavior|guests? watched", full)),
        "victim_gets_safety_care_documentation_and_choice": bool(re.search(r"checked|safe|medical|formal complaint|documented|security footage|appropriate authorities|offering you a choice|if you wish|payment for .*work|not obligated", full)),
        "helper_or_witness_has_material_cost_and_moral_agency": bool(re.search(r"fired|lost (?:the )?job|payment|work|money|business|dream|cost|punish\w* .*doing what is right|telling the truth|helping may cost", full)) and bool(re.search(r"truth|help|defend|choice|brave|fear does not|stubborn heart", full)),
        "power_response_is_proportionate_boundary_not_revenge": (not cruel_revenge) and bool(re.search(r"engagement is over|ending an engagement|refus\w* to marry|formal complaint|authorities|documented|legal|provide .*footage|will not be punished|does not have the authority", full)),
        "independent_evidence_controls_truth": bool(re.search(r"security footage|venue cameras|camera|footage|record|documents?|verify|evidence|witness|call .* establish|facts", full)),
        "transgressor_faces_relational_social_or_procedural_consequence": bool(re.search(r"engagement is over|ended the engagement|lost .*job|fired|public humiliation|people are talking|complaint|authorities|court|review|sponsor|contract.*(?:review|withdraw|lost)|consequences", full)),
        "aftermath_explores_fear_cost_and_values": bool(re.search(r"frightened|fear does not|worried about money|punish you for doing what is right|what a person is willing to sacrifice|another person.?s dignity|proud of you|dream is not dead", full)),
        "serial_hook_is_specific_not_generic": bool(re.search(r"security footage|venue cameras|compliance records|financial disclosures|contract review|unanswered call|find out|formal complaint|documentation|subcontractors", full)),
        "chapter_or_film_closes_a_micro_objective": bool(re.search(r"engagement is over|truth|documented|payment|will not be punished|choice|safe|complaint|answers?|established", ending_text + "\n" + full[-max(1, len(full) // 4):])),
    }
    labels = {
        "transgression_is_public_status_violence_not_random_action": "the inciting violence/humiliation is not clearly public and status/dignity-based",
        "target_offers_explanation_or_verification_before_escalation": "the target is not given a chance to explain or verify before escalation",
        "authority_judges_values_not_status_or_appearance": "the authority response does not explicitly reject status/appearance as a measure of dignity",
        "bystanders_and_enablers_are_confronted": "the story isolates blame in one villain without confronting bystanders/enablers",
        "victim_gets_safety_care_documentation_and_choice": "the victim does not receive safety, care, documentation, payment, or meaningful choice",
        "helper_or_witness_has_material_cost_and_moral_agency": "helping/truth-telling has no material cost or moral agency",
        "power_response_is_proportionate_boundary_not_revenge": "power responds through revenge spectacle rather than proportionate boundaries, procedure, or refusal",
        "independent_evidence_controls_truth": "truth is controlled by assertion/status rather than independent evidence",
        "transgressor_faces_relational_social_or_procedural_consequence": "the transgressor lacks relational, social, or procedural consequence",
        "aftermath_explores_fear_cost_and_values": "the aftermath skips the victim/helper's fear, economic cost, and values",
        "serial_hook_is_specific_not_generic": "continuation relies on a generic cliffhanger rather than a specific evidence/procedure hook",
        "chapter_or_film_closes_a_micro_objective": "the chapter/film does not close a micro-objective before any continuation hook",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "A public dignity transgression works when status-based violence is met with verification, victim care and choice, proportionate boundaries, independent evidence, confrontation of enablers, material cost for helpers, and a specific procedural continuation hook after a micro-objective closes.",
    }
