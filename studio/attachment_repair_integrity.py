"""Parentification-free attachment repair integrity checks.

These heuristics encode the Poppy doctrine: a child may catalyze grief repair,
but custody, emotional regulation, reliability, and healing must be carried by
adults and systems rather than the child. Transparent craft warnings only.
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


def evaluate_attachment_repair_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    ending_source = "\n".join([architecture_text, scenes_text])
    ending_text = ending_source[-max(1, len(ending_source) // 3):] if ending_source else ""

    child_family = bool(re.search(r"child|daughter|son|girl|boy|kid", full)) and bool(re.search(r"daddy|dad\b|father|mommy|mother|parent", full))
    reunion_or_loss = bool(re.search(r"(?<![a-z])(?:dead|died|death|lost|missing)(?![a-z])|records? (?:were )?wrong|dna|custody|children.?s home|orphanage|came home|long[- ]lost|reunion", full))
    grief_or_attachment = bool(re.search(r"grie(?:f|ving)|sad|scared|afraid|abandon|forgot|come back|attachment|broken heart|happiness", full))
    applies = child_family and reunion_or_loss and grief_or_attachment
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    checks = {
        "living_child_contradicts_fixed_loss_belief": bool(re.search(r"not dead|still alive|she.?s alive|he.?s alive|came home|records? (?:were )?wrong|error in the records|long[- ]lost", full)),
        "custody_or_reunion_is_procedurally_safeguarded": bool(re.search(r"dna|records?|home assessment|custody|guardianship|social worker|children.?s home|court|judge|approval|placement|visits?", full)),
        "parent_publicly_claims_without_hiding_child": bool(re.search(r"won.?t make .*hide|not hide|press conference|publicly (?:claim|acknowledge|recognize)|my daughter|my son|claim her|claim him", full)),
        "care_is_small_repeated_and_embodied": bool(re.search(r"eat|meal|breakfast|dinner|shoes?|bedtime|cook|drawing|draw|hug|backpack|toy|frog|hand|tuck|bath|lunch", full)),
        "adult_grief_regulation_and_support": bool(re.search(r"therap|counselor|nora|support group|adults? for help|ask for help|doctor|breathing|rest|consultation", full)),
        "reliability_has_measurable_repair_protocol": bool(re.search(r"\d+[: ]?(?:sharp|o.?clock)|call .*late|if .*delayed|reminder|showing up|keeps? .*promise|i.?ll call|apolog|forgive", full)),
        "parentification_is_explicitly_corrected": bool(re.search(r"didn.?t have to cure|don.?t have to (?:cure|fix|take care)|not your job|adults? (?:will|can|should) help|you can love me and still|go play|not your fault|you did nothing wrong", full)),
        "dead_parent_memory_differentiates_child": bool(re.search(r"not (?:a )?replacement|i see you|you.?re not (?:your )?(?:mother|mom|mommy)|like (?:your )?(?:mother|mom|mommy).*but|remember .*mother|mommy died|mother died", full)),
        "child_fear_is_named_and_repaired": bool(re.search(r"scared|afraid|forgot me|won.?t come back|leave me|abandon", full)) and bool(re.search(r"listen|apolog|forgive|not your fault|call|i.?m here|promise", full)),
        "ending_proves_ordinary_safety_systems": bool(re.search(r"teacher|uniformed helper|staff|safe|calm|home|school|therap|reminder|meal|together|play", ending_text)),
    }

    labels = {
        "living_child_contradicts_fixed_loss_belief": "reunion lacks a strong contradiction of the parent's fixed loss/death belief",
        "custody_or_reunion_is_procedurally_safeguarded": "custody/reunion happens without DNA, records, assessment, guardianship, court, or social-worker safeguarding",
        "parent_publicly_claims_without_hiding_child": "parent does not publicly claim or protect the child's identity instead of hiding her/him",
        "care_is_small_repeated_and_embodied": "care remains abstract instead of repeated embodied acts such as food, shoes, bedtime, drawing, touch, toys, or shared meals",
        "adult_grief_regulation_and_support": "grief regulation is placed on the child rather than therapy, breathing, rest, adult help, or professional support",
        "reliability_has_measurable_repair_protocol": "parental reliability is not measurable through time promises, call protocols, reminders, apologies, or repeated compliance",
        "parentification_is_explicitly_corrected": "the story never explicitly corrects the child's belief that they must cure/fix/care for the parent",
        "dead_parent_memory_differentiates_child": "the child is treated as a replacement for the dead parent rather than a distinct person with partial resemblance",
        "child_fear_is_named_and_repaired": "child abandonment fear is missing or not answered with listening, apology, truth, and behavioral repair",
        "ending_proves_ordinary_safety_systems": "ending does not prove ordinary safety systems after the reunion high",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Child-reunion grief melodrama works when procedural safeguarding and adult support surround the reunion, reliability is behaviorally repaired, and the child is free to love without being responsible for curing the parent.",
    }
