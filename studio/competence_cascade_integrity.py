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


def _early_story_text(architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    sequences = architecture.get("sequences") if isinstance(architecture, dict) else None
    if isinstance(sequences, list) and sequences:
        count = max(1, (len(sequences) + 2) // 3)
        parts.extend(_text(sequence).lower() for sequence in sequences[:count])
    elif architecture:
        text = _text(architecture).lower()
        parts.append(text[:max(1, len(text) // 3)])
    if scenes:
        count = max(1, (len(scenes) + 2) // 3)
        parts.extend(_text(scene).lower() for scene in scenes[:count])
    return "\n".join(parts)


def _ordered_architecture_text(architecture: dict[str, Any]) -> str:
    parts: list[str] = []
    sequences = architecture.get("sequences") if isinstance(architecture, dict) else None
    if isinstance(sequences, list):
        parts.extend(_text(sequence).lower() for sequence in sequences)
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else None
    if ending_payoff:
        parts.append(_text(ending_payoff).lower())
    return "\n".join(parts)


def _ordered_scene_text(scenes: list[dict[str, Any]]) -> str:
    return "\n".join(_text(scene).lower() for scene in scenes)


def _closure_before_hook_in_ordered_text(text: str) -> bool:
    if not text:
        return False
    hook_match = re.search(r"new mission|top-level mission|return to the team|sequel hook|next mission|ordered to|called away", text)
    closure_match = re.search(r"justice|law|court|police|family|reunited|marriage|belonging|instructor|new identity|special agent|peace|home", text)
    return bool(closure_match) and (not hook_match or closure_match.start() < hook_match.start())


def _has_coercive_intimacy(text: str) -> bool:
    coercion_patterns = [
        r"no right to refuse",
        r"can.?t refuse",
        r"won.?t take no",
        r"forced? .*?(?:bed|sex|kiss|intimacy)",
        r"(?:ignores|ignored|ignoring).{0,35}(?:no|refusal|stop)",
        r"(?:said|says|asked|begged).{0,30}(?:no|stop).{0,50}(?:keeps|kept|continues|continued|doesn.?t stop)",
        r"belong completely to me",
        r"you are mine now",
    ]
    intimacy_pattern = re.compile(r"kiss|sex|sexual|bed|bedroom|intimate|intimacy|romance|romantic|touch|undress|wedding night|belong|mine")
    for pattern in coercion_patterns:
        for match in re.finditer(pattern, text):
            window = text[max(0, match.start() - 140):match.end() + 140]
            if intimacy_pattern.search(window):
                return True
    return False


def _artifact_units(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> list[str]:
    units = [_text(premise).lower()]
    sequences = architecture.get("sequences") if isinstance(architecture, dict) else None
    if isinstance(sequences, list):
        units.extend(_text(sequence).lower() for sequence in sequences)
        for key, value in architecture.items():
            if key not in {"sequences", "ending_payoff"}:
                units.append(_text(value).lower())
    elif architecture:
        units.append(_text(architecture).lower())
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else None
    if ending_payoff:
        units.append(_text(ending_payoff).lower())
    units.extend(_text(scene).lower() for scene in scenes)
    return [unit for unit in units if unit]


def _positive_hidden_master_identity(text: str) -> bool:
    for match in re.finditer(r"prodigy|genius|master hacker|secretly skilled|hidden mastery", text):
        prefix = text[max(0, match.start() - 35):match.start()]
        if not re.search(r"(?:no|not|without|lacks|never)(?:\s+\w+){0,3}\s*$", prefix):
            return True
    return False


def evaluate_competence_cascade_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    opening = _early_story_text(architecture, scenes)

    mastery_terms = r"assassin|special agent|mercenary|elite operative|master hacker|top assassin|king of killers|prodigy|genius|expert"
    hidden_mastery = bool(
        re.search(r"(?:reborn|transmigrated|secretly|hidden|undercover|disguised|concealed).{0,90}(?:" + mastery_terms + r")", full)
        or re.search(r"(?:" + mastery_terms + r").{0,90}(?:hidden identity|secret identity|double life|concealed|reborn|transmigrated)", full)
        or _positive_hidden_master_identity(full)
    )
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

    hook_pattern = r"new mission|top-level mission|return to the team|sequel hook|next mission|ordered to|called away"
    closure_pattern = r"justice|law|court|police|family|reunited|marriage|belonging|instructor|new identity|special agent|peace|home"
    ending_units: list[str] = []
    if isinstance(architecture, dict):
        ending_payoff = architecture.get("ending_payoff")
        if ending_payoff:
            ending_units.append(_text(ending_payoff).lower())
        sequences = architecture.get("sequences")
        if isinstance(sequences, list) and sequences:
            ending_units.append(_text(sequences[-1]).lower())
    if scenes:
        ending_units.extend(_text(scene).lower() for scene in scenes[-min(2, len(scenes)):])

    positive_closure = False
    explicit_hook_before_closure = False
    ordered_groups = []
    if isinstance(architecture, dict):
        architecture_units = []
        sequences = architecture.get("sequences")
        if isinstance(sequences, list) and sequences:
            architecture_units.append(_text(sequences[-1]).lower())
        if architecture.get("ending_payoff"):
            architecture_units.append(_text(architecture.get("ending_payoff")).lower())
        ordered_groups.append("\n".join(architecture_units))
    if scenes:
        ordered_groups.append("\n".join(_text(scene).lower() for scene in scenes))
    for ordered_text in ordered_groups:
        hook_match = re.search(hook_pattern, ordered_text)
        closure_match = re.search(closure_pattern, ordered_text)
        if closure_match and (not hook_match or closure_match.start() < hook_match.start()):
            positive_closure = True
        if hook_match and closure_match and hook_match.start() < closure_match.start():
            explicit_hook_before_closure = True
    closure_before_hook = positive_closure and not explicit_hook_before_closure

    checks = {
        "intimate_public_violation": bool(re.search(r"diary|private|read aloud|publicly humiliat|bully|bullied|shame|mock|debt collector|threaten|frame|false accusation", full)),
        "care_or_family_economic_anchor": bool(re.search(r"mother|father|brother|sister|family|child", full) and re.search(r"care|warmth|sacrifice|gave up|hospital|medical|debt|unpaid|protect|save|meal|home", full)),
        "hidden_competence_is_proven_early": bool(re.search(r"race|fight|win|evidence|skill|competence|defeat|solve|prove|demonstrate|counterattack", opening)),
        "distinct_competence_domains": _count_any(full, competence_domains) >= 3,
        "institutional_arena_rotation": _count_any(full, arenas) >= 4,
        "ethical_loyalty_test": bool(re.search(r"abandon|comrade|loyal|share risk|stay behind|protect subordinate|won.?t leave|no one leaves|shield|save.*team|not abandon", full)),
        "provenance_and_procedural_accountability": bool(re.search(r"prize money|clean money|source of money|evidence|video|records|investigation|police|law|judge|court|according to law|public apology", full)),
        "ally_supports_without_owning_revenge": bool(re.search(r"support|stand with|help|ally|partner|not alone|won.?t let.*alone|respect|choice|let her|she decides|without taking over", full)),
        "romance_or_intimacy_respects_refusal": not any(_has_coercive_intimacy(unit) for unit in _artifact_units(premise, architecture, scenes)),
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
