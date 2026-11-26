"""Spatial-status grammar intelligence.

Stories often encode power through physical spaces: who sits, kneels, enters,
serves, is caged, or is allowed across a threshold. This module checks whether a
project establishes that grammar and whether the ending transforms its meaning.
It is a transparent heuristic, not a measure of quality by itself.
"""
from __future__ import annotations

import json
import re
from typing import Any

STATUS_SPACE_TERMS = {
    "floor", "table", "kneel", "sit", "chair", "mat", "threshold", "door", "doorway",
    "gate", "cage", "chain", "cell", "vault", "canal", "kitchen", "servant", "maid",
    "sanctuary", "arch", "crown", "platform", "bench", "counter", "cart", "hiding",
}
INVERSION_TERMS = {
    "chosen", "choose", "by choice", "free", "freed", "open", "opened", "no cages",
    "doors they can close", "sanctuary", "belonging", "home", "welcome", "sit",
    "reversible", "release", "unchained", "without chains", "crosses", "fly free",
}
POWER_TERMS = {
    "king", "queen", "royal", "crown", "billionaire", "fiancé", "fiance", "master",
    "madam", "soldier", "navy", "guard", "inspector", "hunter", "army", "lord",
    "institution", "public", "crowd", "villagers", "society",
}
VULNERABLE_TERMS = {
    "child", "maid", "servant", "creature", "dragon child", "worker", "poor", "vulnerable",
    "captive", "prisoner", "hunted", "daughter", "keeper",
}


def flatten(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(flatten(v) for v in value)
    return str(value)


def hits(text: str, terms: set[str]) -> list[str]:
    low = text.lower()
    return sorted(term for term in terms if term in low)


def final_sequences(architecture: dict[str, Any]) -> str:
    sequences = architecture.get("sequences") or []
    if not isinstance(sequences, list):
        return ""
    return flatten(sequences[-2:]) + " " + flatten(architecture.get("ending_payoff", {}))


def evaluate_spatial_status(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    scenes = scenes or []
    all_text = "\n".join([flatten(premise), flatten(architecture), flatten(scenes)]).lower()
    opening_text = flatten(premise.get("opening_event", {}))
    if architecture.get("sequences"):
        opening_text += " " + flatten((architecture.get("sequences") or [])[:1])
    ending_text = final_sequences(architecture)
    if scenes:
        ending_text += " " + flatten(scenes[-2:])

    opening_spaces = hits(opening_text, STATUS_SPACE_TERMS)
    all_spaces = hits(all_text, STATUS_SPACE_TERMS)
    ending_spaces = hits(ending_text, STATUS_SPACE_TERMS)
    inversion = hits(ending_text, INVERSION_TERMS)
    power = hits(opening_text + " " + ending_text, POWER_TERMS)
    vulnerable = hits(opening_text, VULNERABLE_TERMS)

    warnings: list[str] = []
    if len(opening_spaces) < 2:
        warnings.append("opening does not establish a legible spatial status grammar (who is caged, seated, kneeling, serving, or excluded)")
    if not vulnerable or not power:
        warnings.append("spatial grammar lacks a clear vulnerable/powered social relation")
    if not ending_spaces:
        warnings.append("ending does not visibly return to or transform the status space")
    if not inversion:
        warnings.append("ending does not clearly invert compulsion into chosen access, release, sanctuary, or belonging")
    if opening_spaces and ending_spaces and not set(opening_spaces).intersection(ending_spaces) and not inversion:
        warnings.append("opening and ending spaces do not appear related; circular spatial payoff may be absent")

    score = 0.18
    score += min(0.24, 0.08 * len(opening_spaces))
    score += 0.16 if vulnerable else 0.0
    score += 0.14 if power else 0.0
    score += min(0.18, 0.06 * len(ending_spaces))
    score += min(0.22, 0.055 * len(inversion))
    if set(opening_spaces).intersection(ending_spaces):
        score += 0.08
    score = max(0.0, min(1.0, score))
    return {
        "score_0_to_1": round(score, 3),
        "opening_status_spaces": opening_spaces,
        "ending_status_spaces": ending_spaces,
        "inversion_signals": inversion,
        "power_terms": power,
        "vulnerable_terms": vulnerable,
        "warnings": warnings,
        "doctrine": "Define who is physically forced below/outside/inside power, then make the ending transform that space into chosen access, sanctuary, or belonging. Inspired by floor/table and cage/sanctuary evidence.",
    }
