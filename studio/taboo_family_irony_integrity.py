"""Integrity checks for forbidden-family romance driven by dramatic irony.

Derived from DramaShine XL0d9SmAA1M evidence. These are creative heuristics,
not performance predictions: they separate a durable superior-knowledge engine
from copied coercion, possessiveness, or mafia power fantasy.
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


def evaluate_taboo_family_irony_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    opening_source = "\n".join([premise_text, architecture_text[: max(1, len(architecture_text) // 3)], scenes_text[: max(1, len(scenes_text) // 3)]])

    family_taboo = bool(re.search(r"best friend.?s (?:dad|father|mom|mother)|stepmom|stepmother|stepfather|guardian|father.?in.?law|mother.?in.?law|family friend", full))
    romantic_power = bool(re.search(r"mafia|mob|godfather|don\b|ceo|billionaire|older man|age gap|powerful|boss", full))
    hidden_relation = bool(re.search(r"secret|hidden identity|doesn.?t know|unaware|mistaken|wrong (?:man|woman|person)|lies|lying|truth", full))
    applies = family_taboo and romantic_power and hidden_relation
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    arena_terms = {
        "home": r"home|mansion|estate|breakfast|kitchen|bedroom|bathroom",
        "commerce": r"boutique|shop|mall|store|card|couture",
        "school": r"school|campus|college|class|principal",
        "sport_public": r"hockey|arena|game|finals|party|gala|dance",
        "crime_institution": r"mafia|crew|police|court|contract|business|operation",
    }
    arena_count = sum(1 for pattern in arena_terms.values() if re.search(pattern, full))
    coercion_unrepaired = bool(re.search(r"drunk(?:en)? marriage|mistake(?:n)? marriage|forced marriage|blackmail|no right to refuse|won.?t take no|cut .*internet|ship .*away|surveillance|possessive|you are mine", full)) and not bool(re.search(r"flaw|wrong|apolog|repair|consent|free choice|can leave|reject|done with|boundar|truth|no more lies", full))

    checks = {
        "compounded_impossibility_early": sum(bool(re.search(pattern, opening_source)) for pattern in [r"wrong (?:man|person)|mistaken", r"marry|married|wife|husband|bride", r"best friend|stepmom|father|dad", r"mafia|godfather|boss|older man|powerful"]) >= 3,
        "audience_has_superior_knowledge": bool(re.search(r"audience|viewer|dramatic irony|doesn.?t know|unaware|only .*knows|secret identity|hidden identity", full)),
        "protective_misdirector_active": bool(re.search(r"best friend|sister|brother|father|mother|guardian", full) and re.search(r"protect|warn|save|rescue|hide|cover|scheme|investigate|track|private investigator", full)),
        "social_arena_rotation": arena_count >= 4,
        "public_shame_or_class_wound": bool(re.search(r"publicly humiliat|shame|gold.?digger|class|poor|student loans|scholarship|slut|whore|cheap|beggar|sidepiece", full)),
        "power_acquires_rules_or_accountability": bool(re.search(r"rules|by the books|police|court|law|evidence|investigation|accountability|consequences|don.?t touch civilians|procedural", full)),
        "protagonist_can_reject_power": bool(re.search(r"we are done|reject|refuse|stay away|can leave|free to leave|choice|chooses|decides|no more lies|tell me the truth", full)),
        "possessiveness_is_flaw_not_reward": not coercion_unrepaired,
        "family_reclassification_hook": bool(re.search(r"stepmom|stepmother|best friend or|call you now|family order|bloodline|part of the family|reclassif", full[-max(1, len(full)//2):])),
        "truth_and_consent_repair": bool(re.search(r"truth|no more lies|consent|free choice|choose freely|apolog|repair|boundar|can leave", full)),
    }
    labels = {
        "compounded_impossibility_early": "taboo-family premise is not compounded and legible in the opening",
        "audience_has_superior_knowledge": "story relies on surprise instead of giving the audience superior knowledge",
        "protective_misdirector_active": "no active friend/family protector misdirects and intensifies the secret",
        "social_arena_rotation": "relationship power is not tested across enough distinct social arenas",
        "public_shame_or_class_wound": "wealth/status fantasy lacks a concrete public shame or class wound",
        "power_acquires_rules_or_accountability": "protective power remains consequence-free force rather than acquiring rules or accountability",
        "protagonist_can_reject_power": "protagonist cannot meaningfully reject the powerful partner after truth exposure",
        "possessiveness_is_flaw_not_reward": "coercive/possessive behavior is present without being named, bounded, or repaired",
        "family_reclassification_hook": "ending does not convert romance revelation into a family-order reclassification hook",
        "truth_and_consent_repair": "original deception/coercion lacks explicit truth, consent, boundary, or agency repair",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Forbidden-family romance works through audience-superior dramatic irony, protective misdirection, rotating social arenas, and family reclassification; coercion and possessiveness must become repaired flaws, never proof of love.",
    }
