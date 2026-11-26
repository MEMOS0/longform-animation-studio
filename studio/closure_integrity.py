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


def _positions(text: str, terms: list[str]) -> dict[str, int]:
    lowered = text.lower()
    found: dict[str, int] = {}
    for term in terms:
        position = lowered.find(term)
        if position >= 0:
            found[term] = position
    return found


def _row(sequence: str | int, text: str) -> dict[str, Any]:
    closure = _positions(text, CLOSURE_TERMS)
    sequel = _positions(text, SEQUEL_TERMS)
    return {
        "sequence": sequence,
        "text": text.lower(),
        "closure_positions": closure,
        "sequel_positions": sequel,
        "closure_hits": list(closure),
        "sequel_hits": list(sequel),
        "infrastructure_hits": list(_positions(text, INFRASTRUCTURE_TERMS)),
        "community_consequence_hits": list(_positions(text, COMMUNITY_CONSEQUENCE_TERMS)),
    }


def evaluate_closure_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Evaluate delivered payoff, not merely the premise's promised payoff.

    Only architecture/scene evidence counts as delivered closure. A premise can
    promise home or recognition, but that promise is not evidence the ending
    dramatized it. Sequel expansion is evaluated in the payoff zone (the final
    two sequences plus explicit ending_payoff); earlier sequel words may be
    ordinary foreshadowing rather than an ending substitute.
    """
    scenes = scenes or []
    sequences = architecture.get("sequences") or []
    rows = [_row(seq.get("sequence", index + 1), flatten(seq)) for index, seq in enumerate(sequences)]
    if architecture.get("ending_payoff"):
        rows.append(_row("ending_payoff", flatten(architecture.get("ending_payoff"))))

    warnings: list[str] = []
    payoff_start = max(0, len(rows) - 2)
    payoff_rows = rows[payoff_start:]
    for row_index, row in enumerate(rows):
        if row_index < payoff_start or not row["sequel_positions"]:
            continue
        sequel_position = min(row["sequel_positions"].values())
        closure_before = False
        for prior in rows[payoff_start:row_index]:
            if prior["closure_positions"]:
                closure_before = True
                break
        if not closure_before:
            same_row_closure = [position for position in row["closure_positions"].values() if position < sequel_position]
            closure_before = bool(same_row_closure)
        if not closure_before:
            warnings.append("sequel expansion appears before a relational/home closure beat lands")
            break

    final_architecture_text = "\n".join(row["text"] for row in payoff_rows)
    final_scene_text = flatten(scenes[-2:] if len(scenes) >= 2 else scenes).lower()
    final_text = final_architecture_text + "\n" + final_scene_text
    final_closure = list(_positions(final_text, CLOSURE_TERMS))
    if rows and not final_closure:
        warnings.append("final movement lacks a clear relational/home/belonging closure signal")

    infrastructure = list(_positions(flatten(architecture) + "\n" + flatten(scenes), INFRASTRUCTURE_TERMS))
    consequence = list(_positions(final_text, COMMUNITY_CONSEQUENCE_TERMS))
    collapse_text = final_architecture_text
    if infrastructure and any(term in collapse_text for term in ["destroy", "collapse", "self-destruct", "fails", "dark"]):
        if not consequence:
            warnings.append("infrastructure/system collapse is not followed by visible community survival, replacement, or rebuilding consequence")
    score = max(0.0, round(1.0 - 0.28 * len(warnings), 2))
    public_rows = []
    for row in rows:
        public_rows.append({
            "sequence": row["sequence"],
            "closure_hits": row["closure_hits"],
            "sequel_hits": row["sequel_hits"],
            "infrastructure_hits": row["infrastructure_hits"],
            "community_consequence_hits": row["community_consequence_hits"],
        })
    return {
        "score_0_to_1": score,
        "rows": public_rows,
        "final_closure_hits": final_closure,
        "warnings": warnings,
        "craft_rule": "A plot sequel hook may remain, but only after the promised recognition, home, belonging, and community consequence have landed.",
    }
