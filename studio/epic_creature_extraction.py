"""Epic creature-extraction narrative integrity checks."""
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


def _pos(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return match.start() if match else None


def evaluate_epic_creature_extraction(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    creature_term = bool(re.search(r"\bcreatures?\b|\bmonsters?\b|\btalu\b|\bdragons?\b|\bgiants?\b|\btrolls?\b|\bbeasts?\b|nonhuman|winged|elder creature", full))
    extraction_term = bool(re.search(r"\bextract(?:ion|s|ed|ing)?\b|\bdrain(?:s|ed|ing)?\b|\bessence\b|\bcapture wagons?\b|souls? trapped", full))
    epic_term = bool(re.search(r"\barmy\b|\bkingdom\b|\bcapital\b|\broyal\b|\bwar\b|\bboundary\b|\bgeneral\b|\bcommander\b|\bempire\b|\bcouncil\b", full))
    applies = creature_term and extraction_term and epic_term
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    seqs = architecture.get("sequences", []) if isinstance(architecture, dict) else []
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else {}
    structured_finale = "\n".join([_text(seqs[-2:]), _text(ending_payoff), _text(scenes[-5:])]).strip().lower()
    premise_finale = "\n".join([_ending_keyed_text(premise), _text(premise.get("ending_payoff", {}))]).strip().lower()
    if not structured_finale and not premise_finale and premise.get("logline"):
        clauses = re.split(r"[.!?;]\s*", premise_text)
        premise_finale = "\n".join(c for c in clauses if re.search(r"\bin the end\b|\bat the end\b|\bfinal(?:ly)?\b|\baftermath\b|\bepilogue\b", c))
    finale_text = structured_finale or premise_finale

    proc_pos = _pos(r"archive|record|guard rotation|service passage|chain of custody|evidence|map|route|jurisdiction|inspect|infiltrat", full)
    rescue_pos = _pos(r"rescue|liberat|free(?:s|d|ing)?|escape(?:s|d)?|break(?:s|ing)? chains?", full)
    trauma_pos = _pos(r"not in that cell|can.?t stop my hands|shaking|trembl|conditioning|mind control|trauma|dissociat|still afraid|panic|flashback", full)
    destruction_pos = _pos(r"destroy|break|shatter|end(?:s|ing)? the source", full)
    cost_pos = _pos(r"souls? trapped|trapped inside|left in darkness|another way|sacrific|fallout|kingdom.*darkness|lose (?:light|power|energy)|what.*cost", full)
    closure_pos = _pos(r"rebuild|another way|peace|choose day after day|welcome.*home|community|village|valley|remember.*lost|found.*home|repair", finale_text)
    hook_pos = _pos(r"to be continued|sequel|new threat|final eye|darkness returns", full)

    third = len(full) // 3
    checks = {
        "creature_society_operational_care": bool(re.search(r"\bcreatures?\b.{0,80}(?:feed|food|shelter|heal|teach|train|protect|care|home|village|valley|community)|(?:feed|food|shelter|heal|teach|train|protect|care).{0,80}\bcreatures?\b", full)),
        "extraction_economic_incentive": bool(re.search(r"energy|power the|fuel|profit|monopoly|holy fire|essence|capture wagons?|source of (?:power|energy)|souls? trapped", full)),
        "power_use_exposure_cost": bool(re.search(r"power.{0,80}(?:reveal|expose|track|signal|attract|cost|risk)|(?:reveal|expose|track|signal|attract).{0,80}power|blood.*stone|stone.*blood", full)),
        "procedural_evidence_or_access_chain": proc_pos is not None and (proc_pos >= third or bool(re.search(r"middle|act ii|investigation|infiltration", full[:proc_pos], re.I))),
        "liberation_trauma_persists": trauma_pos is not None and (rescue_pos is not None and trauma_pos >= rescue_pos or bool(re.search(r"not in that cell|can.?t stop my hands|conditioning|mind control|after rescue|after liberation", full))),
        "source_defeat_has_moral_or_infrastructural_cost": destruction_pos is not None and cost_pos is not None,
        "communal_consequence_or_peace_maintenance": closure_pos is not None,
        "sequel_hook_after_home_closure": hook_pos is None or (closure_pos is not None and closure_pos < hook_pos),
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
