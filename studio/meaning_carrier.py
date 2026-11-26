"""Meaning-carrier validation: physical objects/spaces should change meaning across the film."""
from __future__ import annotations

import re
from typing import Any

OBJECT_TERMS = [
    "net", "bread", "floor", "mat", "ring", "scar", "moon", "compass", "contract", "patent", "key", "mirror",
    "mask", "letter", "locket", "knife", "cup", "plate", "door", "gate", "window", "lullaby", "song", "light",
    "stormglass", "cloth", "table", "gate", "bed", "crown", "collar", "chain", "cage", "map", "photograph",
]


def flatten(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(flatten(v) for v in value.values())
    if isinstance(value, list):
        return "\n".join(flatten(v) for v in value)
    return ""


def object_hits(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in OBJECT_TERMS if re.search(rf"\b{re.escape(term)}\b", lowered)]


def final_sequence_text(architecture: dict[str, Any]) -> str:
    sequences = architecture.get("sequences") or []
    return flatten(sequences[-2:])


def evaluate_meaning_carrier(premise: dict[str, Any], architecture: dict[str, Any] | None = None) -> dict[str, Any]:
    architecture = architecture or {}
    explicit = premise.get("meaning_carrier") or {}
    warnings: list[str] = []
    mode = "explicit" if explicit else "inferred"

    if explicit:
        required = ["object_or_space", "opening_meaning", "closing_reversal", "final_sequence_use"]
        missing = [key for key in required if not explicit.get(key)]
        if missing:
            warnings.append("meaning_carrier missing fields: " + ", ".join(missing))
        opening = str(explicit.get("opening_meaning", "")).strip().lower()
        closing = str(explicit.get("closing_reversal", "")).strip().lower()
        if opening and closing and opening == closing:
            warnings.append("meaning carrier does not change meaning between opening and ending")
        final_text = final_sequence_text(architecture).lower()
        carrier_text = str(explicit.get("object_or_space", "")).lower()
        carrier_tokens = [token for token in re.findall(r"[a-z]{5,}", carrier_text) if token not in {"their", "there", "between"}]
        final_match = any(token in final_text for token in carrier_tokens) or bool(explicit.get("final_sequence_use"))
        if not final_match:
            warnings.append("meaning carrier is not visibly connected to the final two architecture sequences")
        return {
            "mode": mode,
            "object_or_space": explicit.get("object_or_space"),
            "opening_meaning": explicit.get("opening_meaning"),
            "closing_reversal": explicit.get("closing_reversal"),
            "final_sequence_use": explicit.get("final_sequence_use"),
            "score_0_to_1": max(0.0, round(1.0 - 0.25 * len(warnings), 2)),
            "warnings": warnings,
            "craft_rule": "A physical object, space, sound-object, or ritual should carry the wound in the opening and return with changed meaning in the payoff.",
        }

    opening_text = flatten(premise.get("opening_event", {}))
    final_text = final_sequence_text(architecture)
    opening_hits = object_hits(opening_text)
    final_hits = object_hits(final_text)
    shared = sorted(set(opening_hits) & set(final_hits))
    if not opening_hits:
        warnings.append("no concrete physical/spatial meaning carrier detected in the opening")
    if opening_hits and not shared:
        warnings.append("opening object/space does not detectably return in the final sequences")
    if not opening_hits and final_hits:
        warnings.append("ending has concrete imagery but the opening does not seed it")
    return {
        "mode": mode,
        "opening_object_hits": opening_hits,
        "final_object_hits": final_hits,
        "shared_objects": shared,
        "score_0_to_1": 1.0 if shared else (0.5 if opening_hits or final_hits else 0.0),
        "warnings": warnings,
        "craft_rule": "A physical object, space, sound-object, or ritual should carry the wound in the opening and return with changed meaning in the payoff.",
    }
