"""Epic creature-extraction narrative integrity checks.

Derived from the VeylornStudios THE LOST KIND deep dive. The gate is intended for
feature-scale creature/dark-fantasy stories where creature bodies, essence, labor,
or energy are extracted by an institution.
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


def _ending_keyed_text(value: Any) -> str:
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            key_text = str(key).lower()
            if re.search(r"ending|finale|resolution|epilogue|payoff", key_text):
                parts.append(_text(item))
            elif isinstance(item, (dict, list)):
                parts.append(_ending_keyed_text(item))
        return "\n".join(parts)
    if isinstance(value, list):
        return "\n".join(_ending_keyed_text(item) for item in value)
    return ""


def evaluate_epic_creature_extraction(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    creature_term = bool(re.search(r"creature|monster|talu|dragon|giant|troll|beast|nonhuman|winged|elder creature", full))
    extraction_term = bool(re.search(r"extract|essence|drain|source|holy fire|capture wagons|necromanc|energy|souls? trapped|exploitation", full))
    epic_term = bool(re.search(r"army|kingdom|capital|royal|war|boundary|general|commander|empire|council", full))
    applies = creature_term and extraction_term and epic_term
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    seqs = architecture.get("sequences", []) if isinstance(architecture, dict) else []
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else {}
    structured_finale = "\n".join([_text(seqs[-2:]), _text(ending_payoff), _text(scenes[-5:])]).strip().lower()
    premise_finale = "\n".join([_ending_keyed_text(premise), _text(premise.get("ending_payoff", {}))]).strip().lower()
    finale_text = structured_finale or premise_finale or full

    checks = {
        "creature_society_operational_care": bool(re.search(r"creature.{0,80}(?:feed|food|shelter|heal|teach|train|protect|care|home|village|valley|community)|(?:feed|food|shelter|heal|teach|train|protect|care).{0,80}creature", full)),
        "extraction_economic_incentive": bool(re.search(r"extract|drain|essence|capture wagons|energy|source|power the|fuel|profit|monopoly|holy fire", full)),
        "power_use_exposure_cost": bool(re.search(r"power.{0,80}(?:reveal|expose|track|signal|attract|cost|risk)|(?:reveal|expose|track|signal|attract).{0,80}power|blood.*stone|stone.*blood", full)),
        "procedural_evidence_or_access_chain": bool(re.search(r"archive|record|guard rotation|service passage|chain of custody|evidence|map|route|jurisdiction|inspect|infiltrat", full)),
        "liberation_trauma_persists": bool(re.search(r"not in that cell|can.?t stop my hands|shaking|trembl|conditioning|mind control|trauma|dissociat|still afraid|panic|flashback", full)),
        "source_defeat_has_moral_or_infrastructural_cost": bool(re.search(r"destroy.{0,100}(?:souls?|heart|source|light|darkness|kingdom)|(?:souls?|heart|source|light|darkness|kingdom).{0,100}destroy|left in darkness|another way|trapped inside", full)),
        "communal_consequence_or_peace_maintenance": bool(re.search(r"rebuild|another way|peace|choose day after day|welcome.*home|community|village|valley|remember.*lost|found.*home|repair", finale_text)),
        "sequel_hook_after_home_closure": not bool(re.search(r"to be continued|sequel|new threat|final eye|darkness returns", full)) or bool(re.search(r"home|peace|community|rebuild|welcome", finale_text)),
    }
    labels = {
        "creature_society_operational_care": "creature society is asserted but not shown operating through food, shelter, teaching, healing, or communal care",
        "extraction_economic_incentive": "antagonist cruelty lacks a material extraction/energy incentive",
        "power_use_exposure_cost": "power use is consequence-free and does not expose or endanger the wielder/community",
        "procedural_evidence_or_access_chain": "middle lacks procedural access/evidence mechanisms and risks becoming passive lore/travel",
        "liberation_trauma_persists": "rescue treats liberation as instant recovery rather than persistent bodily/psychological trauma",
        "source_defeat_has_moral_or_infrastructural_cost": "destroying the source/system is treated as costless instead of morally or infrastructurally expensive",
        "communal_consequence_or_peace_maintenance": "ending stops at villain defeat without community consequence, rebuilding, or peace maintenance",
        "sequel_hook_after_home_closure": "sequel/darkness hook appears without first landing home/belonging closure",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Epic creature extraction works when scale still preserves operational care: creature society feeds/shelters/heals, extraction has material incentives, power exposes the wielder, investigation proceeds through access/evidence, liberation leaves trauma, system defeat carries moral/infrastructural cost, and peace is maintained by the community after the villain falls.",
    }
