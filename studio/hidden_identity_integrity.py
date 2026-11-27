"""Transparent hidden-identity melodrama integrity checks.

These heuristics encode hidden-status craft doctrine: competence and love precede
the reveal, deception creates a trust cost, power is used prosocially, and the
ending subordinates status to chosen love/family. Royal variants additionally
require material ritual consequences, post-reveal heroine agency, and explicit
status-invariant re-choice. These are warnings for creative review, not oracle
predictions.
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


DISCLOSURE_PATTERN = (
    r"identity reveal|"
    r"reveal(?:s|ed)? (?:his|her|their)? ?(?:identity|wealth|status)|"
    r"true identity|billionaire heir|"
    r"tells? .{0,40}(?:she|he) is (?:the )?(?:king.?s daughter|queen.?s son|princess|prince)|"
    r"(?:admits?|confesses?|discloses?) (?:her identity|his identity|their identity)(?!\s+is\s+(?:still\s+)?(?:a\s+)?(?:mystery|secret|unknown|hidden))|"
    r"(?:admits?|confesses?|discloses?) (?:being|that(?: she| he| they)? is|(?:she|he|they) is) "
    r"(?:a |the )?(?:princess|prince|royal|heir|heiress|king.?s daughter)|"
    r"introduces? .{0,60}(?:daughter|heiress|heir|princess|prince)"
)


def evaluate_hidden_identity_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])

    status_hidden = bool(re.search(
        r"hidden (?:identity|heir|heiress|billionaire|wealth|status)|"
        r"secret(?:ly)? (?:rich|wealthy|heir|billionaire)|"
        r"poor (?:student|worker|mechanic|student)|true identity|"
        r"not knowing he was|not knowing she was|"
        r"secret(?:ly)? (?:a )?(?:princess|prince|royal)|"
        r"hidden (?:princess|prince|royal identity)|"
        r"(?:keeps?|kept|conceals?|hides?) (?:her|his|their) (?:rank|identity|royal identity|status|true identity) secret|"
        r"(?:her|his|their) (?:rank|identity|royal identity|status|true identity) (?:is|remains|stays) secret|"
        r"(?:princess|prince|countess|count|duke|duchess|royal)s?.{0,25}disguis|"
        r"escaped? .*palace.*disguise",
        full,
    ))
    occupational_disguise = bool(re.search(
        r"disguis(?:ed|es|ing)?(?: herself| himself| themselves)? as (?:a )?(?:maid|village girl|commoner|servant|beggar)|"
        r"poses? as (?:a )?(?:maid|village girl|commoner|servant|beggar)",
        full,
    ))
    rank_tokens = set(re.findall(r"[a-z]+", full))
    rank_vocabulary = {
        "princess", "princesses", "prince", "princes", "royal", "royals", "palace", "kingdom", "crown", "king", "kings", "queen", "queens",
        "heir", "heiress", "countess", "countesses", "duke", "duchess", "lord", "lady",
        "billionaire", "wealth",
    }
    concealed_rank_context = bool(rank_vocabulary & rank_tokens)
    hidden = status_hidden or (occupational_disguise and concealed_rank_context)
    if not hidden:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    reveal = bool(re.search(DISCLOSURE_PATTERN, full))
    competence = bool(re.search(r"competence|corrects?|valuation|solves?|repairs?|work(?:s|ed)?|craft|skill|earns?|proves?|intellectual|publicly validates?", full))
    ordinary_bond = bool(re.search(r"before (?:status|wealth)|ordinary kindness|coffee|study|library|meal|work together|kindness|care|love(?:d)? before|non-status", full))
    trust_cost = bool(re.search(r"trust wound|lie|lied|hiding the truth|apolog|needs time|informed choice|wrong to hide|trust (?:is|was) (?:damaged|broken)", full))
    prosocial_power = bool(re.search(r"protect(?:s|ed)?|save(?:s|d)?|rescue(?:s|d)?|university|school|hospital|workers?|students?|community|family|foundation|institution|vulnerable", full))
    belonging_closure = bool(re.search(r"chosen love|family|belonging|home|proposal|wedding|greatest treasure|love (?:before|not because)|subordinat", full[-max(2000, len(full) // 3):]))

    checks = {
        "reveal_present": reveal,
        "competence_or_kindness_before_status": competence,
        "ordinary_non_status_bond": ordinary_bond,
        "lie_has_trust_cost": trust_cost,
        "power_used_prosocially": prosocial_power,
        "wealth_subordinated_to_belonging": belonging_closure,
    }
    labels = {
        "reveal_present": "hidden-identity premise never clearly stages the reveal",
        "competence_or_kindness_before_status": "hidden identity lacks competence/kindness proof independent of status",
        "ordinary_non_status_bond": "love/loyalty is not clearly formed through ordinary non-status behavior before the reveal",
        "lie_has_trust_cost": "hidden identity reveal does not treat deception as a relational trust wound requiring repair",
        "power_used_prosocially": "hidden wealth/power is not clearly used to protect people or institutions the audience cares about",
        "wealth_subordinated_to_belonging": "ending does not clearly subordinate wealth/status to chosen love, family, home, or belonging",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]

    accountability = {
        "intelligent_deceived_party_evidence": bool(re.search(r"evidence|facts|records|documents|invoice|timeline|audit|investigat", full)),
        "post_reveal_spatial_boundary": bool(re.search(r"separate homes|no gifts|no persuasion|get out|post[- ]reveal boundar|relationship boundar|enforc(?:e|ed|ing)[^\n]{0,40}space|space after (?:the )?reveal", full)),
        "procedural_full_disclosure": bool(re.search(r"full disclosure|every document|supporting documents|written record|original record|complete record", full)),
        "consent_based_help_rules": bool(re.search(r"help requires consent|no tests|no surveillance|questions replace traps|unless .*safety|say yes", full)),
        "repeat_inconvenient_compliance": bool(re.search(r"when inconvenient|following them|prove it when|10 days|ten days|therapy|\bdates\b", full)),
        "truthful_rechoice": bool(re.search(r"choose me again|choose each other|full truth|with conditions|restart the marriage", full)),
    }

    ordered = "\n".join([architecture_text, scenes_text, premise_text])
    reveal_match = re.search(DISCLOSURE_PATTERN, ordered)
    post_reveal_text = ordered[reveal_match.end():] if reveal_match else ""
    royal_variant = bool({"princess", "princesses", "prince", "princes", "royal", "royals", "palace", "kingdom", "crown", "countess", "countesses", "duke", "duchess"} & rank_tokens)
    royal_extensions = {
        "ritual_or_object_has_material_consequence": bool(re.search(r"rose|ring|token|ritual|law|ceremony|crown|object", full)) and bool(re.search(r"house|home|hut|palace|marry|marriage|heir|kingdom|inherit|live in|public", full)),
        "agency_retained_after_reveal": bool(re.search(r"she (?:exposes?|interrupts?|saves?|investigates?|chooses?|protects?)|heroine (?:exposes?|saves?|chooses?)|her evidence|she brings proof|female protagonist.*(?:evidence|proof|save|expose)", post_reveal_text)),
        "truthful_status_invariant_rechoice": bool(re.search(r"choose .*palace .*hut|choose .*hut .*palace|choose .*every day|choose me again|choose each other|love .*without (?:crown|status|wealth)", post_reveal_text)),
    }
    royal_missing = [key for key, ok in royal_extensions.items() if not ok]
    accountability_missing = [key for key, ok in accountability.items() if not ok]
    if hidden and accountability_missing:
        warnings.append("QueenFlix accountability extensions incomplete: " + ", ".join(accountability_missing))
    if royal_variant and royal_missing:
        warnings.append("Golden Rose royal extensions incomplete: " + ", ".join(royal_missing))

    base_score = sum(checks.values()) / len(checks)
    accountability_score = sum(accountability.values()) / len(accountability)
    score = 0.7 * base_score + 0.3 * accountability_score
    if royal_variant:
        checks.update(royal_extensions)
    return {
        "applies": True,
        "score_0_to_1": round(score, 3),
        "base_score_0_to_1": round(base_score, 3),
        "accountability_score_0_to_1": round(accountability_score, 3),
        "warnings": warnings,
        "checks": checks,
        "queenflix_accountability": accountability,
        "golden_rose_extensions": royal_extensions,
    }
