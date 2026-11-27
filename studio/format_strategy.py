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
        "Treat compression as a completeness constraint: every scene should advance danger, bond, cost, or reversal in at least two ways.",
        "Keep lore subordinate to a visible victim/protector relationship.",
        "End with emotional belonging or safety, not only procedural victory, unless the asset is explicitly a serialized act with a next-problem hook.",
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
    "compound_serial_expansion": [
        "Make the original compressed asset emotionally and materially complete before reusing it inside a longer package.",
        "Use prequel or continuation material to deepen the original wound/handoff, not to replace missing closure.",
        "Preserve care-before-power ordering in reused creature material; do not front-load spectacle by re-editing away the first care act.",
        "Treat performance as packaging evidence, not proof that longer duration caused the result.",
    ],
    "extended_compilation": [
        "Assume binge value and franchise trust are part of performance; separate packaging effects from story quality.",
        "Audit openings/endings of internal episodes individually before generalizing.",
    ],
    "unspecified": ["Specify duration and release format before greenlighting."],
}


def premise_text_for_format_inference(premise: dict[str, Any]) -> str:
    """Flatten premise text without optional future compound-expansion guidance.

    The expansion plan is packaging advice for a later reuse decision, not the
    current release format, so it must not trigger episodic/prequel inference.
    """
    import copy
    cleaned = copy.deepcopy(premise)
    packaging = cleaned.get("packaging")
    if isinstance(packaging, dict):
        packaging.pop("compound_expansion", None)
    def flat(value: Any) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return "\n".join(flat(v) for v in value.values())
        if isinstance(value, list):
            return "\n".join(flat(v) for v in value)
        return ""
    return flat(cleaned)


def infer_format_flags(text: str) -> dict[str, bool]:
    low = text.lower()
    episodic = bool(re.search(r"\b(episode|ep\.?|part)\s*\d+\b|to be continued|cliffhanger", low))
    return {
        "episodic": episodic,
        "compilation": bool(re.search(r"compilation|complete season|full season|season\s*\d+|all episodes|movie marathon", low)),
        "compound_expansion": bool(re.search(r"compound expansion|serial expansion|prequel|continuation material|reused footage|re-edit", low)),
        "serialized": episodic or bool(re.search(r"serial|series|episode|part|chapter|season", low)),
        "continuation_hook": bool(re.search(r"to be continued|cliffhanger|next episode|season\s*2", low)),
    }


def format_strategy(target_minutes: float | int | None = None, premise_text: str = "", explicit_format: str = "") -> dict[str, Any]:
    flags = infer_format_flags(premise_text + " " + explicit_format)
    cls = explicit_format if explicit_format in BASE_RULES else duration_class(target_minutes, flags["compilation"])
    if cls == "microdrama_episode" and target_minutes is not None and float(target_minutes) >= 8 and not flags["serialized"]:
        cls = "short_feature"
    warnings: list[str] = []
    recommendations = list(BASE_RULES.get(cls, BASE_RULES["unspecified"]))
    compressed_complete = target_minutes is not None and 10 <= float(target_minutes) <= 35.5 and not flags["serialized"]
    density_rule = "Treat compression as a completeness constraint: every scene should advance danger, bond, cost, or reversal in at least two ways."
    if compressed_complete and density_rule not in recommendations:
        recommendations.insert(2, density_rule)
    if cls in {"microdrama_episode"} and not flags["serialized"]:
        warnings.append("short duration but no serial/episode packaging detected; decide whether this is a microdrama episode or compressed short feature")
    compressed_engine_risk = compressed_complete or (cls in {"microdrama_episode", "short_feature"} and not flags["serialized"])
    if compressed_engine_risk and not re.search(r"child|creature|dragon|wolf|mother|father|family|lover|protector|baby|heir|giant|scholarship|orphan|bride", premise_text.lower()):
        warnings.append("compressed formats currently depend on ultra-legible relational/class engines; abstract or lore-first premises are high risk at short duration")
    if flags["episodic"] and cls not in {"microdrama_episode", "compilation_or_complete_season"}:
        warnings.append("episodic labeling on a longer asset may reduce self-contained discovery value; prove the first episode can stand alone")
    if flags["compilation"] and cls not in {"compilation_or_complete_season", "extended_compilation"}:
        warnings.append("compilation language detected without matching duration; clarify packaging")
    if flags.get("compound_expansion") and cls != "compound_serial_expansion":
        warnings.append("compound/serial expansion language detected; classify the release explicitly so duration is not mistaken for causal evidence")
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
