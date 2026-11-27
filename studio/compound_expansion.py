"""Compound serial-expansion planning and integrity checks.

WUFO evidence suggests a compressed creature film can later be expanded with a
prequel/continuation block and reused as a longer compound asset. This is a
packaging doctrine, not duration causality: the original film must still close
emotionally and infrastructurally enough to stand alone.
"""
from __future__ import annotations

from typing import Any


def _flat(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(_flat(v) for v in value.values())
    if isinstance(value, list):
        return "\n".join(_flat(v) for v in value)
    return ""


CLOSURE_TERMS = [
    "home", "belong", "safe", "safety", "family", "recognition", "chosen", "love",
    "community repair", "rebuilding", "return", "embrace", "protection",
]
UNRESOLVED_SYSTEM_TERMS = [
    "water", "food", "coal", "heat", "power", "safety", "infrastructure", "community", "ration", "fuel",
]


def evaluate_compound_expansion_readiness(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    combined = "\n".join([_flat(premise), _flat(architecture), _flat(scenes)]).lower()
    creature_like = any(term in combined for term in ["creature", "dragon", "wolf", "monster", "animal", "beast"])
    sequences = architecture.get("sequences", []) if isinstance(architecture, dict) else []
    final_text = _flat(sequences[-2:] if len(sequences) >= 2 else sequences).lower()
    if architecture.get("ending_payoff"):
        final_text += "\n" + _flat(architecture.get("ending_payoff")).lower()
    final_scenes = scenes[-2:] if len(scenes) >= 2 else scenes
    final_text += "\n" + _flat(final_scenes).lower()

    relational_closure = any(term in final_text for term in CLOSURE_TERMS)
    unresolved_system = (
        any(term in combined for term in UNRESOLVED_SYSTEM_TERMS)
        and any(term in combined for term in ["collapse", "destroy", "seize", "ration", "monopoly", "deprivation"])
        and not any(term in final_text for term in ["rebuild", "repair", "restore", "replacement", "community survives", "water access", "heat access", "food access", "power restored"])
    )
    ambiguous_tail = any(term in final_text for term in ["ambiguous", "mystery remains", "perhaps", "departure alone", "disappears"])

    warnings: list[str] = []
    if creature_like and not relational_closure:
        warnings.append("compound reuse is premature: the standalone creature film needs relational/home/protection closure in its final movement")
    if unresolved_system:
        warnings.append("do not use unresolved heat/water/food/community survival as an artificial expansion hook; show replacement or rebuilding consequence in the standalone asset")
    if ambiguous_tail and not relational_closure:
        warnings.append("ambiguous departure/rebirth imagery alone is not enough closure for ethical creature-family reuse")

    expected_scene_count = len(sequences)
    scene_keys = []
    for index, scene in enumerate(scenes):
        key = scene.get("scene_id") or scene.get("sequence") or scene.get("time_range") or index
        scene_keys.append(str(key))
    scene_coverage_ratio = min(len(set(scene_keys)) / expected_scene_count, 1.0) if expected_scene_count and scenes else 1.0
    if expected_scene_count and scenes and scene_coverage_ratio < 1.0:
        warnings.append("compound expansion readiness cannot treat a partial scene draft as ending-complete; the last supplied scene is not necessarily the ending")

    target = float(premise.get("target_minutes") or 0)
    expansion_floor = round(target * 0.5, 1) if target else None
    expansion_ceiling = round(target * 0.95, 1) if target else None
    score = 1.0 if creature_like and relational_closure and not unresolved_system else max(0.0, 1.0 - 0.35 * len(warnings)) if creature_like else 0.0
    if expected_scene_count and scenes and scene_coverage_ratio < 1.0:
        score = min(score, 0.65 * scene_coverage_ratio)
    return {
        "applicable": creature_like,
        "score_0_to_1": round(score, 2),
        "warnings": warnings,
        "scene_coverage_ratio": round(scene_coverage_ratio, 3),
        "packaging_boundary": "Compound expansion is packaging evidence, not proof that longer runtime caused stronger performance.",
        "recommended_plan": {
            "standalone_asset": "finish the emotional wound and show material/community consequence before any reuse",
            "prequel_window_minutes": [expansion_floor, expansion_ceiling] if target else None,
            "prequel_material": "show the economic/world system before the opening wound, but end the inserted block on a handoff that makes the original opening more painful rather than redundant",
            "reuse_rule": "preserve the original care-before-power chain; do not re-edit the reused film so spectacle appears before the first care act",
            "tail_rule": "after reused footage, add only a short epilogue if it clarifies home/nest/community consequence; do not append a sequel tease that displaces closure",
        },
    }
