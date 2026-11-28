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
        return _text(scenes[-max(1, min(5, (len(scenes) + 2) // 3)):]).lower()
    if isinstance(architecture, dict) and isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
        return _text(architecture["sequences"][-max(1, min(3, (len(architecture["sequences"]) + 2) // 3)):]).lower()
    return fallback[-max(1, len(fallback) // 3):]



def _setup_narrative_text(architecture: dict[str, Any], scenes: list[dict[str, Any]], fallback: str) -> str:
    if scenes:
        count = max(1, min(5, (len(scenes) + 2) // 3))
        return _text(scenes[:-count] or scenes[:1]).lower()
    if isinstance(architecture, dict) and isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
        count = max(1, min(3, (len(architecture["sequences"]) + 2) // 3))
        return _text(architecture["sequences"][:-count] or architecture["sequences"][:1]).lower()
    return fallback[:max(1, len(fallback) // 2)]


def _has_active_revenge_intent(text: str) -> bool:
    direct_cues = bool(re.search(r"avenge|murdered|kill the one|hunt(?:er|ing)? .*killer|mother.*murder", text))
    if direct_cues:
        return True
    for match in re.finditer(r"revenge|vengeance", text):
        window = text[max(0, match.start() - 100):match.start()]
        negated = re.search(r"(^|[^a-z])(over|instead of|rather than|rejects?|renounces?|refuses?)([^a-z]|$)", window)
        if not negated:
            return True
    return False


def evaluate_wound_price_revenge_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    dark_creature = bool(re.search(r"demon|fiend|monster|creature|troll|beast|supernatural|dark fantasy|nightstalker", full))
    revenge = _has_active_revenge_intent(full)
    if not (dark_creature and revenge):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    ending = _final_narrative_text(architecture, scenes, full)
    motif_patterns = {
        "counting": r"count(?:ing|s|ed)?|boy who counted",
        "carving": r"carv(?:ing|es|ed)?|wooden|figurine|listening wolf",
        "song": r"song|whistle",
        "token": r"token|keepsake",
        "ritual_promise": r"ritual|promise",
    }
    setup_text = _setup_narrative_text(architecture, scenes, full)
    setup_motifs = {name for name, pattern in motif_patterns.items() if re.search(pattern, setup_text)}
    ending_motifs = {name for name, pattern in motif_patterns.items() if re.search(pattern, ending)}
    motif_source = bool(setup_motifs)
    motif_end = bool(setup_motifs & ending_motifs)

    checks = {
        "intimate_wound_before_dark_spectacle": bool(re.search(r"mother|father|family|child|home|cottage|protect(?:ed|ing)? (?:her|his|the) child", full)),
        "wound_becomes_portable_behavioral_motif": motif_source,
        "motif_returns_as_climax_identity": motif_source and motif_end,
        "mentor_care_has_cost_or_penance": bool(re.search(r"mentor|teacher|master|hunter.{0,80}(?:train|teach|protect)|six winters|penance|someone should have done|sacrific", full)),
        "competence_rules_precede_power": bool(re.search(r"weakness|first rule|rule|train|training|six winters|never hunt|learn|drill|study", full)),
        "power_or_revenge_has_irreversible_price": bool(re.search(r"accepts?.{0,80}(?:soul|price|cost|bargain)|pays?.{0,80}(?:soul|price|cost)|in exchange for|gives? up.{0,80}(?:life|soul|future|memory)|never return|lose yourself|irreversible.{0,80}(?:price|cost)|sacrific(?:e|es|ed).{0,80}(?:life|soul|self|future)", full)),
        "revenge_conflicts_with_protective_rule": bool(re.search(r"never hunt angry|do not go alone|promise me you will not|revenge.{0,80}(?:cost|consume|destroy)|anger.{0,80}(?:rule|danger|cost)", full)),
        "antagonist_weaponizes_original_wound": bool(re.search(r"your mother|murdered your mother|before i took her|i will remember you|smell of a child|knows? (?:your|the) fear|weaponizes?", full)),
        "alliance_or_care_outlives_revenge_utility": bool(re.search(r"companion|friend|healer|not alone|come with me|help people|protect|care|trust", full)),
        "ending_pays_price_and_closes_grief": bool(re.search(r"mama|mother|memorial|grief|mourning|it is done", ending) and re.search(r"soul|death|dies|accepts?.{0,80}(?:price|cost)|pays?.{0,80}(?:price|cost)|never beg|irreversible|sacrific", ending)),
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
