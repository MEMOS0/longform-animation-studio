"""Serialized patronage/art-longing integrity checks.

Derived from Beluluga NOCTURNE hit/episode comparison. Transparent creative
warnings, not performance predictions. Applies when a period queer or otherwise
socially constrained romance uses art/music and patronage as the only socially
legible form of intimacy.
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


def _segments(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"[.!?\n]", text) if part.strip()]


def _has_coercive_intimacy(text: str) -> bool:
    for sentence in _segments(text):
        if re.search(r"kiss\w*[^.\n]{0,80}without (?:his |her |their )?(?:asking|consent|permission)", sentence) and not re.search(r"\b(?:refuses?|won.?t)\s+to\s+kiss\w*", sentence):
            return True
        if re.search(r"forced (?:kiss|intimacy)|not free to leave|owns? (?:him|her|them)", sentence):
            return True
    return False


def evaluate_serialized_patronage_art_longing_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    constrained_romance = bool(re.search(r"\bbl\b|male-male|queer|gay|his husband|two men|forbidden romance|secret romance|\bromance\b|\blovers?\b|intimacy|in love|love affair", full))
    period_power = bool(re.search(r"period|regency|duke|duchess|grand duke|empress|emperor|lord|lady|aristocr|crown|court|imperial|nobility|patron", full))
    art_object = bool(re.search(r"piano|pianist|music|musician|nocturne|composition|composer|sonata|movement|bar\b|melody|painting|portrait|poem|manuscript|performance|recital|artist", full))
    if not (constrained_romance and period_power and art_object):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    architecture_text = _text(architecture).lower()
    final_scene_text = _text(scenes[-1]).lower() if scenes else ""
    ending_parts: list[str] = []
    if isinstance(architecture, dict):
        for key, value in architecture.items():
            if re.search(r"ending|final|closing|resolution|epilogue|payoff", str(key).lower()):
                ending_parts.append(_text(value).lower())
        sequences = architecture.get("sequences") or architecture.get("sequence")
        if isinstance(sequences, list) and sequences:
            ending_parts.append(_text(sequences[-1]).lower())
    ending_text = "\n".join(ending_parts + [final_scene_text]) or (architecture_text[-max(1, len(architecture_text) // 3):] if architecture_text else full[-max(1, len(full) // 4):])

    coercion = _has_coercive_intimacy(full)
    affirmative_consent = bool(re.search(r"tell me to stop|may i|you can stay|choice|choose|permission|consent|if you don't want|explicit permission|asked (?:his|her|their|for) permission|invited|optional", full))
    objective_closure = bool(re.search(r"\b(?:finished|completed|performed|played|held|resolved|answered|accepted|signed|ended|delivered|returned)\b|choice (?:is )?made|boundary (?:is )?set", full))
    forced_end_dependence = bool(re.search(r"forced? to work for (?:him|her|the patron)|must work for (?:him|her|the patron)|patron owns|no choice but to work|cannot leave", ending_text))
    checks = {
        "artist_has_independent_craft_goal_before_attachment": bool(re.search(r"recital|performance|compose|composition|practice|rehears|concert|imperial hall|exhibition|commission|career|work", full)),
        "art_object_is_relational_language_not_decor": bool(re.search(r"wrote it for you|closest .*asking|unfinished|unresolved|third bar|second movement|listen(?:ed|ing)?|hear|melody|manuscript|music .*say|piece .*mean", full)),
        "patronage_is_both_material_care_and_dependence": bool(re.search(r"patronage|patron|gave me a home|somewhere to (?:play|work|paint)|sponsor|dependent|livelihood|support", full)) and bool(re.search(r"end my patronage|only thing .*name|dependence|cannot leave|took so long to leave|obligation|indebted", full)),
        "rank_or_naming_makes_power_asymmetry_explicit": bool(re.search(r"your grace|your majesty|lord|title|rank|call me|name|unnamed|no name|what are we|as what", full)),
        "intimacy_preserves_micro_consent_and_refusal_rights": affirmative_consent and not coercion,
        "rival_or_alternative_attachment_is_differentiated_by_listening_not_possession": bool(re.search(r"i listened|listening|noticed|noticing things|understood|hear(?:s|d)? the rest|rescue|defend|protect", full)) and not bool(re.search(r"rival .*owns|alternative .*possess", full)),
        "duty_has_material_political_or_family_cost": bool(re.search(r"army|crown|country|house|succession|betrothal|marriage alliance|politic|regiment|war|front|heir|family command", full)),
        "artistic_body_or_capacity_has_cost": bool(re.search(r"hand|finger|voice|hearing|sight|cannot play|can't play|cannot perform|losing|fails?|injur|illness|tremor", full)),
        "social_barrier_is_institutional_not_cartoon_villainy": bool(re.search(r"society|nobility|court|reputation|scandal|law|church|family|empress|crown|class|public", full)),
        "episodes_close_intimacy_or_professional_micro_objectives": objective_closure,
        "ending_preserves_independent_home_craft_or_choice": bool(re.search(r"new home|own home|own studio|second movement|continue composing|still writing|invitation remains open|free to choose|choice|independent|practice|ready to play|earns? (?:her|his|their) own", ending_text)) and not forced_end_dependence,
        "continuation_hook_is_specific_institutional_or_creative": bool(re.search(r"outpost|war|mother|letter|invitation|second movement|unanswered|evidence|court|performance|attack|arrival|missing|specific threat", ending_text + "\n" + full[-max(1, len(full) // 4):])),
    }
    labels = {
        "artist_has_independent_craft_goal_before_attachment": "the artist/patronized protagonist lacks an independent performance, composition, exhibition, or craft goal before attachment",
        "art_object_is_relational_language_not_decor": "the art object is decorative rather than a repeatable language for proposal, listening, refusal, memory, or recognition",
        "patronage_is_both_material_care_and_dependence": "patronage is not shown as both sincere material care and a dependence trap",
        "rank_or_naming_makes_power_asymmetry_explicit": "rank, title, naming, or the lack of a social name for the bond is left implicit",
        "intimacy_preserves_micro_consent_and_refusal_rights": "intimacy lacks micro-consent, refusal rights, or permission to remain/leave",
        "rival_or_alternative_attachment_is_differentiated_by_listening_not_possession": "the alternative attachment is not differentiated through listening, noticing, defense, or non-possessive care",
        "duty_has_material_political_or_family_cost": "duty is a vague excuse rather than material military, Crown, house, succession, or family cost",
        "artistic_body_or_capacity_has_cost": "the protagonist's artistic body/capacity carries no loss, injury, deterioration, or performance risk",
        "social_barrier_is_institutional_not_cartoon_villainy": "the barrier is cartoon villainy rather than institutional class, court, family, reputation, or law",
        "episodes_close_intimacy_or_professional_micro_objectives": "serialized chapters do not close concrete intimacy/professional units before hooks",
        "ending_preserves_independent_home_craft_or_choice": "the ending resolves into possession/couple status without preserving independent home, craft, or choice",
        "continuation_hook_is_specific_institutional_or_creative": "continuation is generic rather than a specific institutional, family, war, evidence, or creative hook",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Serialized patronage art-longing works when a recurring art object carries the intimacy that society refuses to name, patronage is both sincere care and dependence, rank and social form are explicit, intimacy preserves refusal rights, duty has material cost, the artist's body/craft is at risk, episodes close concrete units, and the ending preserves independent home/craft/choice with a specific institutional or creative continuation hook.",
    }
