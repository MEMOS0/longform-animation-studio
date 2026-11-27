"""Compressed wish/creature-family integrity checks.

Derived from Fableheart evidence. These heuristics test whether a short
fantasy wish is an ethical object chain rather than a vending-machine reward.
They are warnings, not performance predictions.
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


def evaluate_compressed_wish_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    magic_signal = bool(re.search(r"christmas star|magic(?:al)? object|tail|mermaid|creature baby|wishing star|magic", full))
    applies = magic_signal and bool(re.search(r"wish|child|son|daughter|family|mother|father|creature|mermaid|fantasy", full))
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    def first_pos(pattern: str) -> int:
        match = re.search(pattern, full)
        return match.start() if match else -1
    reward_pos = first_pos(r"got my wish|wish comes true|wish is granted|tail appears|in the sea.*tail|transformation")
    sacrifice_pos = first_pos(r"gave.*away|give.*back|sacrifice|let go|release|for you")
    ritual_pos = first_pos(r"give a present|something you love|christmas|ritual|rule|tradition|gift")

    checks = {
        "physical_constraint_or_cost": bool(re.search(r"one breath|breath|cost|risk|danger|slow|too far|vulnerable|limited|cannot|can't|sacrifice", full)),
        "bodily_belonging_motivation": bool(re.search(r"tail|legs|belong|left behind|too slow|body|fit in|fast like|looks more at|two worlds", full)),
        "moral_or_ritual_rule_planted": ritual_pos >= 0 and (reward_pos < 0 or ritual_pos < reward_pos),
        "protagonist_caused_pursuit": bool(re.search(r"went after|follow|chase|ran after|chose to|because.*wish|it fell for me|now i get mine", full)),
        "wish_carrier_is_vulnerable_or_personlike": bool(re.search(r"creature baby|baby|alone and scared|tears|child|person|alive|mother.*baby|her baby|vulnerable", full)),
        "possession_reframed_as_attachment": bool(re.search(r"that's her baby|not my|give it back|someone else's|belongs to|mother.*baby|kidnap|took it", full)),
        "sacrifice_before_reward": sacrifice_pos >= 0 and (reward_pos < 0 or sacrifice_pos < reward_pos),
        "adult_prejudice_or_blame_repair": bool(re.search(r"blamed you|afraid.*stories|brought him home|grandpa|stood between|apolog|repair|wrong about", full)),
        "transformation_integrates_identity": bool(re.search(r"in the sea.*tail|on land.*legs|both|integrat|never be left behind|hybrid|two worlds|choose both", full)),
        "ritual_or_object_meaning_closes": bool(re.search(r"merry christmas|gift|gave my star|got my wish|star went home|tree|ritual|meaning", full[-2500:])),
    }
    labels = {
        "physical_constraint_or_cost": "compressed wish fantasy lacks a physical constraint, cost, or danger that makes magic consequential",
        "bodily_belonging_motivation": "wish lacks bodily/belonging motivation beyond arbitrary desire",
        "moral_or_ritual_rule_planted": "moral or seasonal ritual rule is not planted before the magical reward",
        "protagonist_caused_pursuit": "protagonist does not cause the magical pursuit through a legible choice",
        "wish_carrier_is_vulnerable_or_personlike": "wish carrier remains a vending-machine object rather than vulnerable or personlike",
        "possession_reframed_as_attachment": "the story never reframes possessing the wish object as attachment/kinship or another's loss",
        "sacrifice_before_reward": "reward arrives without surrender, release, or sacrifice first",
        "adult_prejudice_or_blame_repair": "adult blame/prejudice is not repaired through witnessed evidence",
        "transformation_integrates_identity": "transformation erases one identity instead of integrating mixed belonging",
        "ritual_or_object_meaning_closes": "ending does not close the original ritual/object meaning",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Compressed wish fantasy works when a bodily belonging wound drives a protagonist-caused pursuit, the magical carrier becomes vulnerable/personlike, possession is ethically reframed, sacrifice precedes reward, adult prejudice is repaired by evidence, and transformation integrates rather than erases identity.",
    }
