"""Format-aware creative strategy derived from cross-channel evidence.

These are decision aids, not causal rules: public evidence cannot separate CTR,
retention, algorithmic distribution, and execution quality.
"""
from __future__ import annotations

import re
from typing import Any


def duration_class(minutes: float | int | None, compilation: bool = False) -> str:
    if compilation:
        return "compilation_or_complete_season"
    if minutes is None:
        return "unspecified"
    m = float(minutes)
    if m <= 2:
        return "teaser_or_hook_short"
    if m <= 12:
        return "microdrama_episode"
    if m <= 30:
        return "short_feature"
    if m <= 60:
        return "mid_length_feature"
    if m <= 130:
        return "long_feature"
    return "extended_compilation"


BASE_RULES = {
    "teaser_or_hook_short": [
        "State the core trope visually in the first 3 seconds.",
        "Do not treat the asset as evidence for long-form retention.",
    ],
    "microdrama_episode": [
        "Declare the niche trope almost immediately; target viewers already trained in the genre.",
        "Use face-dense emotion, direct dialogue/subtitles, and one dominant relational question.",
        "Every episode still needs one self-contained wound/goal/protection problem and one meaningful payoff before the cliffhanger.",
        "Do not compare episode performance directly with complete 60-120 minute films.",
    ],
    "short_feature": [
        "Create legible injustice or danger within the first 90 seconds.",
        "Pay the title/thumbnail fantasy visually by minute 5.",
        "Keep lore subordinate to a visible victim/protector relationship.",
        "End with emotional belonging or safety, not only procedural victory.",
    ],
    "mid_length_feature": [
        "Open with embodied stakes before world scale or mythology.",
        "Use 8-12 minute escalation blocks; each block must change capability, alliance, secret pressure, or cost.",
        "Deliver a major promise payoff before the midpoint and a deeper relational payoff near the end.",
    ],
    "long_feature": [
        "Provide early proof of the advertised fantasy, then escalate cost rather than repeating setup.",
        "Track audience retention risk across long dialogue/low-motion valleys; insert visual or emotional turns without relying on noise.",
        "The finale must answer the original wound with belonging, home, safety, chosen love, or transformed identity.",
    ],
    "compilation_or_complete_season": [
        "Open with the strongest self-contained episode hook, not recap or franchise lore.",
        "Package completeness as value: clear season/complete-story expectation, normalized audio, clean episode transitions.",
        "Do not use the success of a compilation to claim individual fragmented episodes would perform equally.",
    ],
    "extended_compilation": [
        "Assume binge value and franchise trust are part of performance; separate packaging effects from story quality.",
        "Audit openings/endings of internal episodes individually before generalizing.",
    ],
    "unspecified": ["Specify duration and release format before greenlighting."],
}


def infer_format_flags(text: str) -> dict[str, bool]:
    low = text.lower()
    return {
        "episodic": bool(re.search(r"\b(episode|ep\.?|part)\s*\d+\b|to be continued|cliffhanger", low)),
        "compilation": bool(re.search(r"complete|compilation|full season|season\s*\d+|all episodes|movie marathon", low)),
        "serialized": bool(re.search(r"serial|series|episode|part|chapter|season", low)),
        "continuation_hook": bool(re.search(r"to be continued|cliffhanger|next episode|season\s*2", low)),
    }


def format_strategy(target_minutes: float | int | None = None, premise_text: str = "", explicit_format: str = "") -> dict[str, Any]:
    flags = infer_format_flags(premise_text + " " + explicit_format)
    cls = explicit_format if explicit_format in BASE_RULES else duration_class(target_minutes, flags["compilation"])
    warnings: list[str] = []
    recommendations = list(BASE_RULES.get(cls, BASE_RULES["unspecified"]))
    if cls in {"microdrama_episode"} and not flags["serialized"]:
        warnings.append("short duration but no serial/episode packaging detected; decide whether this is a microdrama episode or compressed short feature")
    if flags["episodic"] and cls not in {"microdrama_episode", "compilation_or_complete_season"}:
        warnings.append("episodic labeling on a longer asset may reduce self-contained discovery value; prove the first episode can stand alone")
    if flags["compilation"] and cls not in {"compilation_or_complete_season", "extended_compilation"}:
        warnings.append("compilation language detected without matching duration; clarify packaging")
    if cls in {"long_feature", "mid_length_feature", "short_feature"} and flags["continuation_hook"]:
        recommendations.append("A continuation hook is acceptable only after the current film/episode pays off a major promise; do not use it as a substitute for resolution.")
    if cls in {"short_feature", "mid_length_feature", "long_feature"} and not re.search(r"child|creature|dragon|wolf|mother|father|family|lover|protector|baby|heir", premise_text.lower()):
        warnings.append("no explicit relational/vulnerable anchor detected in surface premise; broad cinematic formats currently depend on such anchors more than abstract scale")
    return {
        "format_class": cls,
        "inferred_flags": flags,
        "recommendations": recommendations,
        "warnings": warnings,
        "causal_boundary": "Duration/format guidance is observational and channel-dependent; it is not proof of retention or CTR causality.",
    }
