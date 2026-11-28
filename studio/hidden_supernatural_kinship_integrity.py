"""Hidden supernatural kinship integrity checks.

Derived from Heart Flush hit/medium/low comparison. Transparent creative
warnings, not performance predictions. Applies when hidden or disputed children
with supernatural lineage drive family reunion, custody fear, class/status
conflict, and romance.
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


def evaluate_hidden_supernatural_kinship_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    child = bool(re.search(r"\b(?:child|children|kid|kids|son|daughter|pup|pups|cub|cubs|quintuplet\w*|triplet\w*|offspring)\b", full))
    supernatural = bool(re.search(r"\b(?:werewolf|wolf king|alpha|luna|shifter|shift(?:ing|ed|s)?\b|dragon|vampire|magic bloodline|moon mark|pack)\b", full))
    hidden_kinship = bool(re.search(r"hid(?:e|es|den)|secret|missing family|unknown father|never told|didn.?t know they existed|another man.?s child|disputed child|not your child|conceal", full)) and bool(re.search(r"father|mother|parent|grand(?:mother|father|child)|bloodline|biological", full))
    if not (child and supernatural and hidden_kinship):
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

    progressive_markers = set(re.findall(r"first|another|third|fourth|oldest|for now|not yet|doesn.?t know yet|gradually|progressive|piece by piece|secretly", full))
    evidence_markers = set(re.findall(r"birthmark|moon mark|dna|paternity|blood test|bloodline", full))
    single_dump = bool(re.search(r"reveals? all|tells? (?:him|her|them) everything|one speech|single exposition", full))
    refused_test = bool(re.search(r"refus\w*[^.\n]{0,40}(?:dna|paternity|blood test)|(?:dna|paternity|blood test)[^.\n]{0,40}refus\w*", full))
    unopposed_seizure = bool(re.search(r"wins? custody|granted custody|takes? (?:the )?(?:kids|children)[^.\n]{0,40}(?:without|unopposed)|no choice", full))
    no_choice = bool(re.search(r"no choice|don.?t have a choice|forced|not consensual", full))

    checks = {
        "children_open_with_concrete_material_or_social_mission": bool(re.search(r"sell|earn|work|mission|money|rent|food|school|peddle|mall|market|job|bully|humiliat|danger|grab|kidnap", full)),
        "child_agency_has_rules_limits_and_consequences": bool(re.search(r"plan|hide|protect mommy|help|care|rub|oldest|look after|secret|no shifting|don.?t shift|stay hidden|sneak|warned|dangerous", full)) and bool(re.search(r"no shifting|public|expos|discover|caught|consequence|dangerous|rule|warned|not allowed|must not", full)),
        "kinship_reveal_is_progressive_not_single_exposition_dump": (not single_dump) and (len(progressive_markers) >= 2 or (progressive_markers and len(evidence_markers) >= 1) or bool(re.search(r"gradually|progressive|piece by piece|staged reveal", full))),
        "kinship_claims_are_verified_by_independent_evidence": (not refused_test) and bool(re.search(r"confirmed|positive|proves?|matched|camera|footage|record|ledger|proof|evidence|witness|physician|doctor", full)) and bool(re.search(r"dna|paternity|blood test|bloodline|birthmark|moon mark", full)),
        "concealment_is_motivated_by_credible_custody_or_safety_fear": bool(re.search(r"custody|take (?:the )?(?:kids|children)|lose (?:all|the|my)|afraid|scared|protect the other|court|pup ?nap|kidnap|danger|safety|not safe", full)),
        "wealth_or_parental_power_cannot_simply_seize_the_children": (not unopposed_seizure) and bool(re.search(r"not selling|won.?t (?:allow|hand)|nobody.?s taking|children are not property|can.?t buy|money.*not|consent|choose|resist|refus", full)),
        "caregiver_has_independent_competence_beyond_family_role": bool(re.search(r"design|work|job|assistant|fashion|competition|initials|craft|skill|business|earn|profession|draw|talent", full)),
        "supernatural_power_has_public_rules_cost_or_exposure_risk": bool(re.search(r"no shifting in public|shift back|expos|human|pack law|bloodline pressure|moon mark|secret|reveal|rule|cost|risk", full)),
        "status_or_family_judgment_is_answered_with_material_truth": bool(re.search(r"camera|footage|evidence|proof|record|ledger|witness|admit|truth|lie|lying|slander|investigat|test", full)),
        "romance_or_family_reunion_is_chosen_not_forced_by_children": (not no_choice) and bool(re.search(r"freely|not forcing|never used .*children|pursue|only if|want to marry|no more contracts|consent|chooses?|choice", re.sub(r"no choice|don.?t have a choice|forced|not consensual", " ", full))),
        "antagonist_or_false_claimant_receives_accountable_consequence": bool(re.search(r"arrest(?:ed)?|police (?:take|arrest)|canceled engagement|fired|stripped of (?:the )?position|court|prison|legal consequences|exposed publicly|caught and (?:arrested|punished)", full)),
        "ending_restores_secure_family_belonging_not_only_status": bool(re.search(r"together|family|home|won.?t have to be apart|stay|always|safe|protect|ordinary|care|sister|baby|belong", ending_text)),
    }
    labels = {
        "children_open_with_concrete_material_or_social_mission": "the children begin as cute accessories rather than participants in a concrete material or social mission",
        "child_agency_has_rules_limits_and_consequences": "child agency is unlimited cuteness rather than bounded planning with supernatural/public consequences",
        "kinship_reveal_is_progressive_not_single_exposition_dump": "the hidden kinship is exposed in one explanatory dump instead of progressive discovery",
        "kinship_claims_are_verified_by_independent_evidence": "kinship claims rely on assertion rather than birthmarks, bloodline evidence, tests, records, witnesses, or footage",
        "concealment_is_motivated_by_credible_custody_or_safety_fear": "the caregiver hides children for arbitrary misunderstanding rather than credible custody or safety fear",
        "wealth_or_parental_power_cannot_simply_seize_the_children": "wealth or biological parental power threatens to override the caregiver and children without resistance or consent boundaries",
        "caregiver_has_independent_competence_beyond_family_role": "the caregiver lacks independent work, craft, professional competence, or economic agency beyond being a parent/romantic object",
        "supernatural_power_has_public_rules_cost_or_exposure_risk": "supernatural shifting/power is decorative rather than governed by exposure rules, cost, or risk",
        "status_or_family_judgment_is_answered_with_material_truth": "family/status judgment is settled by shouting rather than material truth, records, footage, admissions, or evidence",
        "romance_or_family_reunion_is_chosen_not_forced_by_children": "children or kinship are used to force romance/family rather than chosen commitment",
        "antagonist_or_false_claimant_receives_accountable_consequence": "the antagonist/false claimant faces no credible social, legal, or economic consequence",
        "ending_restores_secure_family_belonging_not_only_status": "the ending restores status or marriage without secure family belonging, care, safety, or ordinary togetherness",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Hidden supernatural kinship works when children open with a concrete mission, child agency has rules and consequences, kinship revelation escalates progressively, concealment is motivated by credible custody/safety fear, evidence verifies lineage, wealth cannot simply seize children, caregivers retain independent competence, supernatural power has exposure risk, status judgment is answered with material truth, romance/family reunion remains chosen, antagonists face accountability, and the ending restores secure belonging rather than mere status.",
    }
