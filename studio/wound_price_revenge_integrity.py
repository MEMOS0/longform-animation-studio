"""Wound-and-price dark-fantasy revenge integrity checks."""
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


def _final_narrative_text(architecture: dict[str, Any], scenes: list[dict[str, Any]], fallback: str) -> str:
    if scenes:
        return _text(scenes[-max(1, min(5, len(scenes))):]).lower()
    if isinstance(architecture, dict) and isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
        return _text(architecture["sequences"][-max(1, min(3, len(architecture["sequences"]))):]).lower()
    return fallback[-max(1, len(fallback) // 3):]


def evaluate_wound_price_revenge_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    dark_creature = bool(re.search(r"demon|fiend|monster|creature|troll|beast|supernatural|dark fantasy|nightstalker", full))
    revenge = bool(re.search(r"revenge|avenge|vengeance|murdered|kill the one|hunt(?:er|ing)? .*killer|mother.*murder", full))
    if not (dark_creature and revenge):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    ending = _final_narrative_text(architecture, scenes, full)
    motif_source = bool(re.search(r"count(?:ing|s|ed)?|carv(?:ing|es|ed)?|song|whistle|token|wooden|figurine|ritual|promise|keepsake|listening wolf", full))
    motif_end = bool(re.search(r"count(?:ing|s|ed)?|carv(?:ing|es|ed)?|song|whistle|token|wooden|figurine|ritual|promise|keepsake|listening wolf|boy who counted", ending))

    checks = {
        "intimate_wound_before_dark_spectacle": bool(re.search(r"mother|father|family|child|home|cottage|protect(?:ed|ing)? (?:her|his|the) child", full)),
        "wound_becomes_portable_behavioral_motif": motif_source,
        "motif_returns_as_climax_identity": motif_source and motif_end,
        "mentor_care_has_cost_or_penance": bool(re.search(r"mentor|teacher|master|hunter.{0,80}(?:train|teach|protect)|six winters|penance|someone should have done|sacrific", full)),
        "competence_rules_precede_power": bool(re.search(r"weakness|first rule|rule|train|training|six winters|never hunt|learn|drill|study", full)),
        "power_or_revenge_has_irreversible_price": bool(re.search(r"soul|life|death|die|price|cost|sacrific|never return|lose yourself|irreversible", full)),
        "revenge_conflicts_with_protective_rule": bool(re.search(r"never hunt angry|do not go alone|promise me you will not|revenge.{0,80}(?:cost|consume|destroy)|anger.{0,80}(?:rule|danger|cost)", full)),
        "antagonist_weaponizes_original_wound": bool(re.search(r"your mother|murdered your mother|before i took her|i will remember you|smell of a child|knows? (?:your|the) fear|weaponizes?", full)),
        "alliance_or_care_outlives_revenge_utility": bool(re.search(r"companion|friend|healer|not alone|come with me|help people|protect|care|trust", full)),
        "ending_pays_price_and_closes_grief": bool(re.search(r"soul|death|dies|it is done|mama|mother|memorial|grief|mourning|accept|price|cost|never beg|no crown|home", ending)),
    }
    labels = {
        "intimate_wound_before_dark_spectacle": "dark-fantasy revenge begins with lore/spectacle rather than an intimate relational wound",
        "wound_becomes_portable_behavioral_motif": "the wound remains backstory instead of becoming a portable behavior, object, counting ritual, song, token, or promise",
        "motif_returns_as_climax_identity": "the opening wound-motif does not return transformed in the climax as identity, method, or counter-power",
        "mentor_care_has_cost_or_penance": "the mentor exists only to explain lore rather than paying care/penance costs over time",
        "competence_rules_precede_power": "the protagonist receives power or wins before craft rules, weaknesses, and training establish competence",
        "power_or_revenge_has_irreversible_price": "supernatural revenge power is effectively free instead of carrying an irreversible soul, life, identity, or relationship price",
        "revenge_conflicts_with_protective_rule": "revenge never tests a protective rule such as not hunting angry or not going alone, so there is no moral self-betrayal",
        "antagonist_weaponizes_original_wound": "the antagonist is generic evil rather than someone who recognizes and weaponizes the original wound",
        "alliance_or_care_outlives_revenge_utility": "relationships exist only as revenge tools rather than care/alliance that persists beyond utility",
        "ending_pays_price_and_closes_grief": "ending resets or rewards the hero without paying the established price or closing the original grief",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Dark-fantasy revenge works when an intimate wound becomes a portable behavior/object, competence is learned before power, the antagonist weaponizes that wound, supernatural help exacts an irreversible price, and the ending pays the price while transforming the original motif into identity rather than reset spectacle.",
    }
