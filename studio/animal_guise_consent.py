"""Animal-guise hidden-spouse consent integrity checks.

Derived from MythicTwist evidence. These checks treat animal disguise intimacy
as a consent/trust problem, not a cute trick.
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


def _first_pos(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return match.start() if match else None


def evaluate_animal_guise_consent(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    animal_terms = bool(re.search(r"\banimal guise\b|\bwolf form\b|\bwerewolf\b|\balpha king\b|\badog\b|\bdog\b|\bshapeshift(?:er|s|ing)?\b|\bluna\b", full))
    hidden_partner_terms = bool(re.search(r"\bhusband\b|\bmate\b|\bromance\b|\bbride\b|\bmarriage\b|\bmarry\b", full))
    applies = bool(re.search(r"animal guise|wolf form|husband.*dog|dog.*husband", full)) or (animal_terms and hidden_partner_terms)
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    reveal_positions = [
        pos for pos in [
            _first_pos(r"\breveal(?:s|ed)?\b", full),
            _first_pos(r"truth", full),
            _first_pos(r"hate being lied", full),
            _first_pos(r"from the very first day", full),
            _first_pos(r"turns? back into", full),
        ] if pos is not None
    ]
    reveal_pos = min(reveal_positions) if reveal_positions else len(full) // 2
    pre_reveal = full[:reveal_pos]
    post_reveal = full[reveal_pos:]

    restitution_object = r"estate|deeds|orchard|mother.?s house|gold|rent ledgers|inheritance|property"
    checks = {
        "protagonist_has_preexisting_agency": bool(re.search(r"conditions|inheritance|deeds|gold|taking what.*mine|choose my own life|bastard|no say", full)),
        "care_before_reveal": bool(re.search(r"care|bandage|teach|button|protect|good boy|look after|feed|dance", pre_reveal)),
        "deception_named_as_trust_wound": bool(re.search(r"hate being lied|liar|lied to you|don't know what to believe|trust|deceiv|faking", post_reveal)),
        "post_reveal_spatial_boundary": bool(re.search(r"separate rooms|not sharing a bed|don't touch|stay right there|leaving|sleeping in separate", post_reveal)),
        "animal_form_manipulation_named": bool(re.search(r"used? (?:that|the) form|turn into him|make me forgive|destroyed|lowest|manipulat", post_reveal)) or not bool(re.search(r"cuddl|bed|sex dream|intimate|kiss", pre_reveal)),
        "material_agency_restored": bool(re.search(rf"(?:return|restore|recover|give back|hand back|gives? (?:her|him|them) back|hands? (?:her|him|them) back).{{0,100}}(?:{restitution_object})|(?:{restitution_object}).{{0,100}}(?:returned|restored|recovered|given back|handed back)", post_reveal)),
        "free_exit_no_force": bool(re.search(r"stay or leave|won't force|will not force|free to leave|choice|ask you myself|no one asked you", post_reveal)),
        "explicit_rechoice_after_truth": bool(re.search(r"my choice|choose me|will you|choose each other|share responsibility|stand beside me", post_reveal)),
        "coercive_actors_accountable": bool(re.search(r"found guilty|sentenced|imprisoned|arrested|held accountable|stripped of|banished|executed", post_reveal)),
    }
    labels = {
        "protagonist_has_preexisting_agency": "heroine lacks agency/material claims before the animal-guise romance begins",
        "care_before_reveal": "romance lacks care/protection/teaching before reveal, making the bond only a trick or status fantasy",
        "deception_named_as_trust_wound": "hidden sentient animal identity is not named as a trust wound",
        "post_reveal_spatial_boundary": "reveal lacks immediate spatial/bodily boundaries",
        "animal_form_manipulation_named": "animal-form intimacy or manipulation is used cutely without being ethically named",
        "material_agency_restored": "restoration does not return concrete property/agency stolen from the heroine",
        "free_exit_no_force": "the deceiver does not offer a real no-force exit after the truth",
        "explicit_rechoice_after_truth": "ending lacks explicit re-choice after truth and freedom",
        "coercive_actors_accountable": "overt kidnapping/forced marriage/coercive actors are not held accountable",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Animal-guise romance is ethical only when care precedes revelation, disguise intimacy is treated as a consent wound, boundaries follow the reveal, agency/property is restored, and the final bond is explicitly re-chosen without force.",
    }
