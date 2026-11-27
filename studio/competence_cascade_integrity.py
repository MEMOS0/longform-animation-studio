"""Hidden-mastery competence-cascade integrity checks.

Derived from Jasmine Drama evidence. These heuristics separate a serialized
hidden-competence revenge engine from random power inflation or genre hopping.
They are warnings, not performance predictions.
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


def _count_any(text: str, groups: dict[str, str]) -> int:
    return sum(1 for pattern in groups.values() if re.search(pattern, text))


def evaluate_competence_cascade_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    ending_source = "\n".join([architecture_text, scenes_text])
    ending = ending_source[-max(1, len(ending_source) // 3):] if ending_source else ""
    opening = full[:max(1, len(full) // 3)]

    hidden_mastery = bool(re.search(r"assassin|special agent|mercenary|elite operative|secretly skilled|hidden mastery|master hacker|top assassin|king of killers|reborn expert|transmigrated expert", full))
    humiliation_reversal = bool(re.search(r"bully|bullied|humiliat|shame|diary|debt collector|looked down|power inversion|revenge|reborn|transmigrat|new body", full))
    applies = hidden_mastery and humiliation_reversal
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    competence_domains = {
        "combat": r"combat|fight|martial|assassin|shoot|marksman|weapon|tactical",
        "mobility": r"race|racing|drive|driving|chase|parkour|pilot",
        "knowledge": r"math|language|academic|genius|scholar|memory|code|cipher",
        "investigation": r"hack|investigate|evidence|surveillance|camera|trace|records|forensic",
        "resources": r"money|assets|fund|company|account|prize money|wealth",
        "leadership": r"lead|command|instructor|mentor|team|legion|protect subordinate",
    }
    arenas = {
        "school": r"school|academy|classroom|principal|teacher|campus",
        "home_family": r"home|family|mother|father|brother|sister|dinner",
        "medical": r"hospital|clinic|doctor|nurse",
        "street_crime": r"street|debt collector|gang|underground|brothel|kidney",
        "race": r"race|racing|track|car",
        "military": r"military|army|special forces|mercenary|training camp|shooting",
        "elite_social": r"banquet|party|gala|noble|elite|chamber",
        "arena": r"arena|duel|gladiator|fight club",
        "procedure": r"police|court|judge|lawyer|law|military tribunal",
    }

    hook_match = re.search(r"new mission|top-level mission|return to the team|sequel hook|next mission|ordered to|called away", ending)
    closure_match = re.search(r"justice|law|court|police|family|reunited|marriage|belonging|instructor|new identity|special agent|peace|home", ending)
    closure_before_hook = bool(closure_match) and (not hook_match or closure_match.start() < hook_match.start())

    checks = {
        "intimate_public_violation": bool(re.search(r"diary|private|read aloud|publicly humiliat|bully|bullied|shame|mock|debt collector|threaten|frame|false accusation", full)),
        "care_or_family_economic_anchor": bool(re.search(r"mother|father|brother|sister|family|child", full) and re.search(r"care|warmth|sacrifice|gave up|hospital|medical|debt|unpaid|protect|save|meal|home", full)),
        "hidden_competence_is_proven_early": bool(re.search(r"race|fight|win|evidence|skill|competence|defeat|solve|prove|demonstrate|counterattack", opening)),
        "distinct_competence_domains": _count_any(full, competence_domains) >= 3,
        "institutional_arena_rotation": _count_any(full, arenas) >= 4,
        "ethical_loyalty_test": bool(re.search(r"abandon|comrade|loyal|share risk|stay behind|protect subordinate|won.?t leave|no one leaves|shield|save.*team|not abandon", full)),
        "provenance_and_procedural_accountability": bool(re.search(r"prize money|clean money|source of money|evidence|video|records|investigation|police|law|judge|court|according to law|public apology", full)),
        "ally_supports_without_owning_revenge": bool(re.search(r"support|stand with|help|ally|partner|not alone|won.?t let.*alone|respect|choice|let her|she decides|without taking over", full)),
        "romance_or_intimacy_respects_refusal": not bool(re.search(r"no right to refuse|can.?t refuse|forced? .*bed|won.?t take no|owns? you|belong completely to me|you are mine now", full)),
        "closure_before_mission_hook": closure_before_hook,
    }
    labels = {
        "intimate_public_violation": "competence-cascade revenge lacks a specific intimate/public violation that creates moral debt",
        "care_or_family_economic_anchor": "hidden mastery is not anchored in care, family, economic sacrifice, or protection before power display",
        "hidden_competence_is_proven_early": "hidden competence is asserted but not proven early through a legible outcome",
        "distinct_competence_domains": "competence repeats one proof type instead of cascading across distinct domains",
        "institutional_arena_rotation": "long-form escalation does not rotate enough institutional arenas to renew the power test",
        "ethical_loyalty_test": "power is never ethically tested through loyalty, shared risk, or refusal to abandon vulnerable people",
        "provenance_and_procedural_accountability": "money/power/revenge lacks provenance, evidence, or procedural accountability",
        "ally_supports_without_owning_revenge": "ally support risks owning or replacing the victim/protagonist's authored revenge",
        "romance_or_intimacy_respects_refusal": "romance or intimacy contains coercive refusal-overriding language/framing",
        "closure_before_mission_hook": "the sequel/next-mission hook arrives before justice, family, identity, or belonging closure",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Hidden-mastery revenge sustains long runtime when an intimate wound and care anchor lead to early proof, distinct competence domains, rotating institutions, ethical loyalty tests, accountable evidence/procedure, non-owning allies, explicit consent, and closure before any sequel mission hook.",
    }
