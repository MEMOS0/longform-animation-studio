"""Compressed found-family guardian integrity checks."""
from __future__ import annotations

import re
from typing import Any


def _text(value: Any) -> str:
    if isinstance(value, str): return value
    if isinstance(value, dict): return "\n".join(_text(v) for v in value.values())
    if isinstance(value, list): return "\n".join(_text(v) for v in value)
    return ""


def _pos(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return match.start() if match else None


def _last_pos(pattern: str, text: str) -> int | None:
    matches = list(re.finditer(pattern, text))
    return matches[-1].start() if matches else None


def evaluate_found_family_guardian_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    guardian = bool(re.search(r"giant|guardian|creature parent|nonhuman parent|adoptive|found family", full))
    child = bool(re.search(r"daughter|child|infant|baby|orphan", full))
    applies = guardian and child
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    care_pos = _pos(r"feed|warm|teach|train|hunt|protect|raise|shelter|fire|blanket", full)
    rupture_pos = _pos(r"argument|rupture|leaves|departure|run(?:s)? away|conflict", full)
    rescue_pos = _last_pos(r"rescue|save|carries|carry|crossbow|army|final confrontation", full)

    checks = {
        "origin_endangerment_before_exposition": bool(re.search(r"pursu|chase|flee|danger|serpent|wolf|attack|birth|infant|newborn", full[:2000])),
        "rescue_transfer_into_guardian_custody": bool(re.search(r"rescues?|saves?|adopt|raises?|takes? (?:her|him|the child)|bursts? through", full)),
        "repeated_operational_care": len(re.findall(r"feed|warm|teach|train|hunt|fire|shelter|protect|sleep|carry|blanket", full)) >= 3,
        "child_gains_agency_or_competence": bool(re.search(r"learns?|hunt|survive|bow|arrow|track|choose|leaves|journey", full)),
        "relational_rupture_before_external_rescue": care_pos is not None and rupture_pos is not None and rescue_pos is not None and care_pos < rupture_pos < rescue_pos,
        "guardian_misread_as_property_or_monster": bool(re.search(r"fortune|captured?|monster|beast|property|army|ruthless lord|crossbow|trap", full)),
        "public_trap_or_impossible_odds": bool(re.search(r"city square|public|army|crossbow|trap|gate|prison|imprisoned", full)),
        "physical_custody_or_carrying_closure": bool(re.search(r"carries|carry|on his back|shoulder|home|reunit|embrace|holds? .*close", full[-2500:])),
    }
    labels = {
        "origin_endangerment_before_exposition": "story lacks immediate origin endangerment before fantasy exposition",
        "rescue_transfer_into_guardian_custody": "child is not transferred into guardian custody through rescue/care",
        "repeated_operational_care": "guardian bond lacks repeated operational care across time",
        "child_gains_agency_or_competence": "child remains passive and gains no agency/competence",
        "relational_rupture_before_external_rescue": "rescue lacks a prior care -> rupture -> rescue emotional chain",
        "guardian_misread_as_property_or_monster": "outsiders do not misread/exploit the guardian as monster, property, or fortune",
        "public_trap_or_impossible_odds": "climax lacks public trap or impossible odds",
        "physical_custody_or_carrying_closure": "ending does not physically restore custody/contact/home",
    }
    warnings=[label for key,label in labels.items() if not checks[key]]
    return {"applies":True,"score_0_to_1":round(sum(checks.values())/len(checks),3),"warnings":warnings,"checks":checks,"craft_rule":"Compressed guardian fantasy works when scale serves care: origin danger transfers a child into nonhuman custody, repeated care and competence build attachment, rupture precedes external rescue, and the climax physically restores custody rather than merely defeating enemies."}
