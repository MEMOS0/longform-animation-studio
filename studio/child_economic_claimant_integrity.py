"""Child economic-claimant integrity checks.

Encodes the Lulu doctrine: a secret-child claimant can convert invisible care
into economic and evidentiary stakes, but adults must verify truth, repair
betrayal, and restore ordinary childhood rather than using the child as a cure.
Transparent craft warnings only.
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


def evaluate_child_economic_claimant_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    ending_source = "\n".join([architecture_text, scenes_text])
    ending = ending_source[-max(1, len(ending_source) // 3):] if ending_source else ""

    child = bool(re.search(r"child|daughter|son|girl|boy|kid", full))
    wealthy_parent = bool(re.search(r"billionaire|ceo|wealthy|rich|company|group|inheritance|heir", full)) and bool(re.search(r"dad|father|mom|mother|parent", full))
    economic_claim = bool(re.search(r"child support|formula money|milk money|deadbeat dad|owe|debt|pay up|hardship pay|diapers|expenses|invoice|collect", full))
    applies = child and wealthy_parent and economic_claim
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    checks = {
        "care_invoice_is_concrete": bool(re.search(r"formula|milk money|diapers|hardship pay|emotional damages|expenses|\$?\d+[,.]?\d*.*(?:formula|diapers|damages|hardship)|invoice|itemiz", full)),
        "claim_has_public_or_procedural_consequence": bool(re.search(r"company|office|lobby|public|media|press|family tree|paternity|dna|court|lawyer|scandal|security", full)),
        "child_has_self_protection_and_agency": bool(re.search(r"don.?t trust|stay back|refus|hid(?:e|es)?|ran away|overhear|observ|notice|figure[sd]? out|help(?:s|ed)? catch|protect herself|protect himself|not stupid", full)),
        "child_claims_are_adult_verified": bool(re.search(r"dna|paternity|doctor|test|camera|footage|police|lawyer|court|evidence|records?|proof|investigation|verification", full)),
        "maternal_labor_or_betrayal_is_material": bool(re.search(r"pregnant|working|sick|passing out|exile|framed|set up|didn.?t believe|disbelieved|leak|secret|abandon|wronged|labor|hardship", full)),
        "money_is_restitution_not_forgiveness": bool(re.search(r"simple sorry|sorry enough|payoff|restitution|not enough|money.*not|can.?t buy|wronged|trust", full)),
        "child_catalyzes_but_does_not_cure_adults": bool(re.search(r"adults?|parents?|mommy|daddy|protect|investigate|doctor|teacher|school|play|child.*not responsible|not your job", full)),
        "legal_or_economic_accountability_lands": bool(re.search(r"court|lawyer|arrest|police|strip(?:ped)? .*position|recover.*assets|forged evidence|fraud|consequences|answer for", full)),
        "ending_restores_ordinary_child_development": bool(re.search(r"kindergarten|school|teacher|peers?|class|rules?|play|vacation|routine|ordinary|home", ending)),
    }
    labels = {
        "care_invoice_is_concrete": "child economic claim remains vague instead of itemizing formula, diapers, hardship, damages, expenses, or care labor",
        "claim_has_public_or_procedural_consequence": "claim has no public, corporate, family-status, paternity, legal, or procedural consequence",
        "child_has_self_protection_and_agency": "child is passive cargo rather than self-protecting, observant, refusing, hiding, or investigation-capable",
        "child_claims_are_adult_verified": "child observations or identity claims are treated as proof without DNA, doctor, camera, records, lawyer, court, or evidence verification",
        "maternal_labor_or_betrayal_is_material": "mother's labor/betrayal is abstract rather than pregnancy, poverty, sickness, framing, disbelief, exile, or hardship",
        "money_is_restitution_not_forgiveness": "payment or wealth risks becoming forgiveness rather than incomplete restitution alongside trust repair",
        "child_catalyzes_but_does_not_cure_adults": "child is made responsible for adult healing instead of catalyzing adult protection, investigation, schooling, and play",
        "legal_or_economic_accountability_lands": "wrongdoing lacks legal/economic accountability such as court, lawyers, asset recovery, fraud exposure, or consequences",
        "ending_restores_ordinary_child_development": "ending does not restore ordinary childhood through school, teachers, peers, rules, play, routine, or home",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "A child economic claimant works when care labor becomes a concrete claim, child agency is protected but adult-verified, money is restitution rather than absolution, legal accountability lands, and the ending returns the child to ordinary development.",
    }
