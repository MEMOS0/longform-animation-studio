"""Scale-bridge stewardship integrity checks from Drakenhart tiny-kingdom evidence."""
from __future__ import annotations

import re
from typing import Any


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(_text(item) for item in value.values())
    if isinstance(value, list):
        return "\n".join(_text(item) for item in value)
    return ""


def evaluate_scale_bridge_stewardship_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    scale_world = bool(re.search(r"tiny kingdom|tiny people|tiny civilization|miniature|small folk|little people|micro-?world|root kingdom", full))
    scale_gap = bool(re.search(r"giant|shrinks?|scale|surface world|tiny people|tiny kingdom|small folk|little people", full))
    stewardship = bool(re.search(r"flood|ecosystem|village|kingdom|protect|promise|build|repair|home|guard|map|steward", full))
    if not (scale_world and scale_gap and stewardship):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    ending_parts: list[str] = []
    if isinstance(architecture, dict):
        for key, value in architecture.items():
            if re.search(r"ending|final|closing|resolution|epilogue|payoff", str(key).lower()):
                ending_parts.append(_text(value).lower())
        sequences = architecture.get("sequences") or architecture.get("sequence")
        if isinstance(sequences, list) and sequences:
            ending_parts.append(_text(sequences[-1]).lower())
    architecture_text = _text(architecture).lower()
    end = "\n".join(ending_parts + ([_text(scenes[-1]).lower()] if scenes else [])) or (architecture_text[-max(1, len(architecture_text) // 3):] if architecture_text else "")

    extractive_abandonment = bool(re.search(r"steal\w*|stolen|leav\w*[^.\n]{0,60}(?:kingdom|world|them|village|people)[^.\n]{0,40}for good|never returns?", full))

    checks = {
        "scale_gap_is_physical_spatial_and_social_not_only_visual_spectacle": bool(re.search(r"cave|roots?|tiny|giant|small|large|high ground|drill|bottle caps?|scale", full)) and bool(re.search(r"kingdom|village|people|guard|queen|community|they|them", full)),
        "human_arrival_has_material_ecological_consequences": bool(re.search(r"flood|giants bring floods|drill|damage|collapse|destroy|threat|invasion|invasive|resource", full)),
        "micro_civilization_has_labor_infrastructure_and_rules": bool(re.search(r"build|guard|farming|village|kingdom|council|queen|map|bottle caps?|high ground|refuge|infrastructure|work", full)),
        "outsider_uses_expertise_but_does_not_become_instant_savior": bool(re.search(r"scientist|explorer|map|report|research|knowledge|help|promise|learn", full)) and not bool(re.search(r"single-handedly saves|instantly worshipped as a god|chosen one solves everything", full)),
        "reciprocal_exchange_changes_both_worlds": bool(re.search(r"bottle caps?|knowledge|promise|home|trade|teach|learn|build smarter|finish the maps|swap\w* maps?|share[sd]? knowledge", full)) and not extractive_abandonment,
        "scale_power_creates_specific_risks_and_limits": bool(re.search(r"one use|limited|might not bring me back|flood|crush|giant|small|fragile|risk|cost", full)),
        "return_or_stay_decision_is_motivated_by_relationship_and_duty": bool(re.search(r"because i promised|you came back|home now|every sunrise|i will return|i.?ll return|i choose to stay|stays? (?:here|there|for good)|to be with (?:her|his|their )?family|duty|promise|guard\w*[^.\n]{0,60}together", end + "\n" + full[-max(1, len(full) // 3):])) and not extractive_abandonment,
        "ending_rebuilds_shared_infrastructure_or_ongoing_stewardship": bool(re.search(r"no more floods|build smarter|built this with us|finish the maps|home now|every sunrise|protect|repair|steward|guard\w*[^.\n]{0,60}(?:levee|dam|village|kingdom|together)|repairs? (?:the )?(?:dam|levee)", end)) and not extractive_abandonment,
        "wonder_is_grounded_in_tactile_objects_and_systems": bool(re.search(r"bottle caps?|map|report|drill|helmet|light|book|tool|door|bridge|root|leaf|seed", full)),
    }
    labels = {
        "scale_gap_is_physical_spatial_and_social_not_only_visual_spectacle": "the scale gap is visual spectacle without physical/social consequences",
        "human_arrival_has_material_ecological_consequences": "the outsider's arrival lacks material ecological or infrastructural consequences",
        "micro_civilization_has_labor_infrastructure_and_rules": "the miniature civilization lacks labor, infrastructure, governance, or rules",
        "outsider_uses_expertise_but_does_not_become_instant_savior": "the outsider is either useless or an instant savior rather than a limited expert participant",
        "reciprocal_exchange_changes_both_worlds": "exchange is one-way rescue rather than reciprocal knowledge/objects/practices changing both worlds",
        "scale_power_creates_specific_risks_and_limits": "scale/power lacks concrete risks, costs, or limits",
        "return_or_stay_decision_is_motivated_by_relationship_and_duty": "the return/stay choice is logistical rather than relational and duty-driven",
        "ending_rebuilds_shared_infrastructure_or_ongoing_stewardship": "the ending escapes the world without rebuilding shared infrastructure or ongoing stewardship",
        "wonder_is_grounded_in_tactile_objects_and_systems": "wonder is abstract spectacle rather than tactile objects and systems",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "A scale-bridge story works when size difference creates material ecological/social consequences, the micro-civilization has labor and rules, outsider expertise is limited and reciprocal, both worlds exchange knowledge/objects, power has scale-specific costs, and the ending rebuilds shared infrastructure or ongoing stewardship.",
    }
