"""Closure integrity: sequel hooks must not replace relational/home payoff."""
from __future__ import annotations

from typing import Any

CLOSURE_TERMS = [
    "home", "belong", "safe", "recognition", "remember", "family", "community", "chosen", "choose",
    "love", "repair", "apolog", "dignity", "partnership", "garden", "table", "meal", "sanctuary", "healing",
]
SEQUEL_TERMS = [
    "another", "new disturbance", "star abyss", "stories are just beginning", "story is just beginning", "war coming",
    "not over", "returns", "wakes", "sequel", "next enemy", "elsewhere", "beyond the stars",
]
INFRASTRUCTURE_TERMS = ["water", "food", "storm", "shield", "power", "array", "infrastructure", "harbor", "valves"]
COMMUNITY_CONSEQUENCE_TERMS = ["survive", "rebuild", "replace", "ration", "share", "community", "village", "town", "people are safe", "new system", "restored"]


def flatten(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(flatten(v) for v in value.values())
    if isinstance(value, list):
        return "\n".join(flatten(v) for v in value)
    return ""


def _hits(text: str, terms: list[str]) -> list[str]:
    lowered = text.lower()
    return [term for term in terms if term in lowered]


def evaluate_closure_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    scenes = scenes or []
    sequences = architecture.get("sequences") or []
    warnings: list[str] = []
    rows = []
    for index, seq in enumerate(sequences):
        text = flatten(seq).lower()
        rows.append({
            "sequence": seq.get("sequence", index + 1),
            "closure_hits": _hits(text, CLOSURE_TERMS),
            "sequel_hits": _hits(text, SEQUEL_TERMS),
            "infrastructure_hits": _hits(text, INFRASTRUCTURE_TERMS),
            "community_consequence_hits": _hits(text, COMMUNITY_CONSEQUENCE_TERMS),
        })
    first_sequel = next((row for row in rows if row["sequel_hits"]), None)
    if first_sequel:
        earlier_closure = any(row["closure_hits"] for row in rows[: rows.index(first_sequel)])
        if not earlier_closure:
            warnings.append("sequel expansion appears before a relational/home closure beat lands")
    final_text = flatten(sequences[-2:] if len(sequences) >= 2 else sequences) + "\n" + flatten(scenes[-2:] if len(scenes) >= 2 else scenes) + "\n" + flatten(premise.get("relational_contract", {}))
    final_closure = _hits(final_text, CLOSURE_TERMS)
    if sequences and not final_closure:
        warnings.append("final movement lacks a clear relational/home/belonging closure signal")
    infrastructure = _hits(flatten(architecture) + "\n" + flatten(scenes), INFRASTRUCTURE_TERMS)
    consequence = _hits(final_text, COMMUNITY_CONSEQUENCE_TERMS)
    if infrastructure and any(term in flatten(sequences[-2:] if len(sequences) >= 2 else sequences).lower() for term in ["destroy", "collapse", "self-destruct", "fails", "dark"]):
        if not consequence:
            warnings.append("infrastructure/system collapse is not followed by visible community survival, replacement, or rebuilding consequence")
    score = max(0.0, round(1.0 - 0.28 * len(warnings), 2))
    return {
        "score_0_to_1": score,
        "rows": rows,
        "final_closure_hits": final_closure,
        "warnings": warnings,
        "craft_rule": "A plot sequel hook may remain, but only after the promised recognition, home, belonging, and community consequence have landed.",
    }
