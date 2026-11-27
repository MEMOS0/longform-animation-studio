"""Cozy disaster-shelter integrity checks.

Derived from Ghibli Cozy Journey hit/low evidence. Transparent creative
warnings, not performance prediction. Applies to family/community survival
stories organized around shelter during a natural disaster.
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


def evaluate_cozy_disaster_shelter_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    disaster = bool(re.search(r"\b(?:typhoon|flood\w*|storm|blizzard|sandstorm|hurricane|wildfire|earthquake)\b", full))
    shelter = bool(re.search(r"\b(?:shelter|home|house|upstairs|fortress|cave|cottage|boat|cabin)\b", full))
    community = bool(re.search(r"\b(?:family|father|mother|grandmother|grandfather|child|son|daughter|village|community)\b", full))
    direct_rescue = re.search(r"rescue\w*\s+(?:the|a|her|his|their)?\s*(?:family|mother|father|child|son|daughter|girl|boy|villagers?|people|them|him|her)\b|(?:family|mother|father|child|son|daughter|girl|boy|villagers?|people|they|he|she)\b[^.!?]{0,60}\b(?:is|are|was|were|gets?|got)\s+rescued", full)
    survival = bool(re.search(r"\bsurviv\w*|\brising water\b|\bfood\b|drinking water|water supply|\bration\w*|storm passes", full) or direct_rescue)
    if not (disaster and shelter and community and survival):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    sequences = architecture.get("sequences") if isinstance(architecture, dict) else None
    if scenes:
        ordered_units = scenes
    elif isinstance(sequences, list) and sequences:
        ordered_units = sequences
    else:
        ordered_units = []
    labor_pattern = re.compile(r"farm|harvest|cook|clean|repair|prepare|gather|chop|fetch|work(?:ing)? the fields|daily life")
    disaster_pattern = re.compile(r"\b(?:typhoon|flood\w*|storm|blizzard|sandstorm|hurricane|wildfire|earthquake)\b|rising water|water (?:rushes?|floods?|enters?|comes?)\s+(?:in|into|indoors)\s+(?:(?:their|the|a|her|his|our)\s+)?(?:house|home|room|cabin|shelter|living room)|water (?:rushes?|floods?|enters?|comes?) indoors|floodwaters")
    if ordered_units:
        cursor = 0
        labor_positions = []
        first_disaster_position = None
        for unit in ordered_units:
            unit_text = _text(unit).lower() + "\n"
            labor_positions.extend(cursor + match.start() for match in labor_pattern.finditer(unit_text))
            if first_disaster_position is None:
                for disaster_match in disaster_pattern.finditer(unit_text):
                    newline = chr(10)
                    sentence_start = max(unit_text.rfind(".", 0, disaster_match.start()), unit_text.rfind("!", 0, disaster_match.start()), unit_text.rfind("?", 0, disaster_match.start()), unit_text.rfind(newline, 0, disaster_match.start())) + 1
                    sentence_end_candidates = [pos for pos in (unit_text.find(".", disaster_match.end()), unit_text.find("!", disaster_match.end()), unit_text.find("?", disaster_match.end()), unit_text.find(newline, disaster_match.end())) if pos != -1]
                    sentence_end = min(sentence_end_candidates) if sentence_end_candidates else len(unit_text)
                    sentence = unit_text[sentence_start:sentence_end]
                    ordinary_water = re.search(r"pipe|plumbing|tap|faucet|sink|hose", sentence)
                    disaster_context = re.search(r"storm|flood|typhoon|hurricane|blizzard|sandstorm|wildfire|earthquake|rising water", sentence)
                    if ordinary_water and not disaster_context:
                        continue
                    first_disaster_position = cursor + disaster_match.start()
                    break
            cursor += len(unit_text)
        ordinary_before_disaster = bool(labor_positions and (first_disaster_position is None or min(labor_positions) < first_disaster_position))
    else:
        opening_text = full[:max(1, len(full) // 4)]
        ordinary = labor_pattern.search(opening_text)
        opening_disaster = disaster_pattern.search(opening_text)
        ordinary_before_disaster = bool(ordinary and (not opening_disaster or ordinary.start() < opening_disaster.start()))

    if ordered_units:
        ending_text = _text(ordered_units[-2:]).lower()
    else:
        ending_text = full[-max(1, len(full) // 4):]

    checks = {
        "ordinary_labor_establishes_world_before_disaster": ordinary_before_disaster,
        "specific_place_and_people_anchor_the_stakes": bool(re.search(r"\b(?:1960|village|riverside|japanese|faroe|family home|wooden home|farming family|named|grandmother|shiba|dog)\b", full)),
        "shelter_is_transformed_meaningful_place": bool(re.search(r"upper floor|upstairs|home becomes|wooden home|family home|abandoned .* shelter|fortress|cave house|hollow|boat", full)),
        "inside_outside_contrast_is_sustained": bool(re.search(r"inside.*(?:warm|safe|light|dry)|outside.*(?:storm|flood|wind|sand|snow)|window|door|lantern|fire|darkness", full)),
        "resources_are_inventoried_and_scarce": bool(re.search(r"little rice|limited food|drinking water|water bucket|well|ration|remaining|scarce|precious", full)),
        "preparation_turns_into_active_protection": bool(re.search(r"board|seal|repair|protect|shutter|brace|sacrifice|fight to protect|hold.*shut", full)),
        "sacrifice_object_has_prior_meaning": bool(re.search(r"precious .*tray|wooden boat|copper .*tray|copper pot|sacrific|heirloom|handmade| treasured", full)),
        "quiet_care_beats_interrupt_threat": bool(re.search(r"warm meal|dinner|blanket|lantern|shared food|cooking|comfort|sleeping|small kindness|quiet moments", full)),
        "children_or_animals_are_participants_not_only_burdens": bool(re.search(r"young son|child .*help|girl .*help|boy .*help|dog|shiba|donkey|feed|comfort(?:s|ed)?", full)),
        "resolution_rebuilds_or_restores_connection": bool(re.search(r"new beginning|rebuild|repair|return home|reunion|helps? .* home|hopeful new|(?:after|following).{0,80}(?:storm|flood|sandstorm|blizzard).{0,80}(?:shared meal|warm meal|dinner)|(?:shared meal|warm meal|dinner).{0,80}(?:after the storm|storm passes|sunrise)", ending_text)),
        "cultural_setting_is_specific_not_decorative": bool(re.search(r"1960|japanese|faroe|sahara|desert|village|riverside|farming|wooden house|copper|thatched|mud house|turf-roof", full)),
    }
    labels = {
        "ordinary_labor_establishes_world_before_disaster": "the disaster starts before ordinary labor and relationships make the world worth saving",
        "specific_place_and_people_anchor_the_stakes": "the family/community is generic rather than anchored in a specific household, place, animal, or historical texture",
        "shelter_is_transformed_meaningful_place": "the shelter is only a convenient location rather than a meaningful home/place transformed by necessity",
        "inside_outside_contrast_is_sustained": "the visual/emotional contrast between dangerous outside and fragile warmth inside is not sustained",
        "resources_are_inventoried_and_scarce": "survival lacks concrete food/water/material scarcity and inventory decisions",
        "preparation_turns_into_active_protection": "characters wait out the disaster instead of actively protecting the shelter",
        "sacrifice_object_has_prior_meaning": "the sacrifice is unspecified instead of losing an object already charged with care, labor, or memory",
        "quiet_care_beats_interrupt_threat": "the story is continuous danger spectacle without meals, warmth, sleep, or small kindness that make survival meaningful",
        "children_or_animals_are_participants_not_only_burdens": "children/animals are only vulnerable props rather than participants in care and survival",
        "resolution_rebuilds_or_restores_connection": "the ending stops at survival instead of rebuilding, reunion, return, or restored connection",
        "cultural_setting_is_specific_not_decorative": "the cultural/historical setting is decorative rather than materially informing labor, shelter, food, and survival practice",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Cozy disaster survival works when ordinary labor establishes a specific household, disaster transforms a meaningful shelter, inside/outside contrast is sustained, scarce resources force concrete choices, protection requires meaningful sacrifice, quiet care interrupts threat, children/animals participate, and resolution rebuilds connection rather than merely surviving.",
    }
