"""Child-power obsolescence / family-security integrity checks."""
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


def _pos(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return match.start() if match else None


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


def evaluate_child_power_obsolescence(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    child_term = bool(re.search(r"\bchild\b|\bgirl\b|\bdaughter\b|\bkid\b|\borphan\b", full))
    power_term = bool(re.search(r"precognition|premonition|vision|countdown|super strength|superpower|powers?|sees? .*before|predict", full))
    family_term = bool(re.search(r"dad|father|mommy|paternity|biological|birth mother|real dad|birth father", full))
    applies = child_term and power_term and family_term
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    power_demo_pos = _pos(r"countdown|you.?re going to die|saves?|rescue|danger|explosion|protect", full)
    explanation_pos = _pos(r"i see|visions?|in my head|predict|power|super strength|superpower", full)
    care_pos = _pos(r"defend|protect|take that word back|care|bandage|treat|comfort|hug|cake", full)
    proof_pos = _pos(r"dna|paternity|biological|birth record|birth certificate|proof|test result", full)
    power_loss_pos = _pos(r"power.*(?:gone|lost|unstable)|(?:gone|lost|unstable).*power|super strength.*gone|normal (?:six|six-year-old|child|kid)|no longer need.*visions?|don.?t need.*visions?", full)
    closure_pos = _pos(r"home|someone will|now i know you will|ordinary|normal|family|wedding|cake", full)
    sequel_pos = _pos(r"another weird kid|sequel|next child|new case|to be continued", full)

    seqs = architecture.get("sequences", []) if isinstance(architecture, dict) else []
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else {}
    finale_text = "\n".join([_text(seqs[-2:]), _text(ending_payoff), _text(scenes[-5:])]).strip().lower()
    if not finale_text:
        finale_text = "\n".join([_ending_keyed_text(premise), _text(premise.get("ending_payoff", {})), _text(premise.get("logline", ""))]).strip().lower()

    checks = {
        "power_demonstrated_before_explanation": power_demo_pos is not None and explanation_pos is not None and power_demo_pos < explanation_pos,
        "protective_bond_before_biological_proof": care_pos is not None and proof_pos is not None and care_pos < proof_pos,
        "procedural_identity_evidence": bool(re.search(r"dna|paternity|lab|birth record|hospital record|death certificate|legal|witness|sealed|chain of custody|report", full)),
        "child_agency_investigation": bool(re.search(r"investigate|search|find out|track|record|no acting alone|together|ask|demand|test", full)),
        "power_has_social_or_bodily_cost": bool(re.search(r"monster|dangerous|afraid|privacy|secret|unstable|weak|risk|bullet|hurt|collapse|dizzy", full)),
        "power_destabilized_or_removed_before_resolution": bool(power_loss_pos is not None and (closure_pos is None or power_loss_pos < closure_pos)) or bool(re.search(r"power.*(?:gone|lost|unstable)|super strength.*gone|normal (?:six|six-year-old|child|kid)|don.?t need.*visions?", finale_text)),
        "love_not_payment_for_power": bool(re.search(r"not (?:my )?bodyguard|don.?t love you because|love .*not .*save|our turn to protect|we.*protect you|you.?re my daughter", full)),
        "ordinary_belonging_closure": bool(re.search(r"home|someone will|now i know you will|normal|ordinary|cake|school|family|wedding|come when.*afraid", finale_text)),
        "sequel_hook_after_belonging_closure": not sequel_pos or closure_pos is not None and closure_pos < sequel_pos,
    }
    labels = {
        "power_demonstrated_before_explanation": "child power is explained before it is demonstrated through concrete danger/rescue",
        "protective_bond_before_biological_proof": "protective love appears only after legal/biological proof instead of before it",
        "procedural_identity_evidence": "identity/family truth lacks procedural evidence such as records, tests, witnesses, or chain-of-custody",
        "child_agency_investigation": "child remains a passive victim rather than helping organize investigation/action",
        "power_has_social_or_bodily_cost": "power is consequence-free and never socially disruptive, dangerous, unstable, or bodily costly",
        "power_destabilized_or_removed_before_resolution": "ending never tests whether love remains when the power weakens or disappears",
        "love_not_payment_for_power": "family love still reads as payment for usefulness rather than independent of rescue power",
        "ordinary_belonging_closure": "resolution lacks ordinary home/belonging security after spectacle",
        "sequel_hook_after_belonging_closure": "sequel hook arrives before relational/home closure",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Child-power family melodrama works when the power is first demonstrated as protection, love forms before proof, identity is procedurally investigated, and the ending makes the power unnecessary by replacing it with reliable ordinary care.",
    }
