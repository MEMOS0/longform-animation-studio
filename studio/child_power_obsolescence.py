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
    ordered = "\n".join([_text(architecture), _text(scenes), _text(premise)]).lower()
    child_term = bool(re.search(r"\bchild\b|\bgirl\b|\bdaughter\b|\bkid\b|\borphan\b", full))
    power_term = bool(re.search(r"precognition|premonition|super strength|superpower|sees? .*before", full)) or bool(re.search(r"(?:her|his|their) powers?|(?:child|girl|daughter|kid).{0,20}(?:vision|countdown|powers?)|(?:vision|countdown|powers?).{0,20}(?:child|girl|daughter|kid)", full))
    family_term = bool(re.search(r"\bdad\b|\bfather\b|\bmommy\b|paternity|biological|birth mother|real dad|birth father", full))
    applies = child_term and power_term and family_term
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    power_demo_pos = _pos(r"countdown|you.?re going to die|saves?|rescue|danger|explosion|protect", ordered)
    explanation_pos = _pos(r"i see|visions?|in my head|predict|power|super strength|superpower", ordered)
    care_pos = _pos(r"defend|protect|take that word back|care|bandage|treat|comfort|hug|cake", ordered)
    proof_pos = _pos(r"dna|paternity|biological|birth record|birth certificate|proof|test result", ordered)
    power_loss_pos = _pos(r"power.*(?:gone|lost|unstable)|(?:gone|lost|unstable).*power|super strength.*gone|normal (?:six|six-year-old|child|kid)|no longer need.*visions?|don.?t need.*visions?", ordered)
    closure_pos = _pos(r"someone will come|now i know you will|that.?s what home is|goes home|returns home|home with (?:her|his|their) (?:dad|father|mom|mother|family)|ordinary child|normal (?:six|six-year-old|child|kid)|family is home|wedding", ordered)
    sequel_pos = _pos(r"another weird kid|sequel|next child|new case|to be continued", ordered)

    seqs = architecture.get("sequences", []) if isinstance(architecture, dict) else []
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else {}
    structured_finale = "\n".join([_text(seqs[-2:]), _text(ending_payoff), _text(scenes[-5:])]).strip().lower()
    premise_finale = "\n".join([_ending_keyed_text(premise), _text(premise.get("ending_payoff", {}))]).strip().lower()
    architecture_has_ending = bool(seqs[-2:] or ending_payoff)
    if len(scenes) < 5 and not architecture_has_ending and premise.get("logline"):
        logline = str(premise.get("logline")).lower()
        clauses = re.split(r"[.!?;]\s*", logline)
        ending_clauses = [clause for clause in clauses if re.search(r"in the end|at the end|final(?:ly)?|aftermath|epilogue", clause) and re.search(r"home|family|ordinary|normal|cake|school|wedding|someone will", clause)]
        premise_finale = "\n".join([premise_finale, *ending_clauses]).strip()
    finale_text = ("\n".join([structured_finale, premise_finale]).strip() if len(scenes) < 5 else structured_finale or premise_finale)

    child_investigation = any(
        phrase in full
        for phrase in (
            "child investigates", "child searches", "child finds out", "child tracks", "child demands", "child tests", "child asks", "child organizes",
            "girl investigates", "girl searches", "girl finds out", "daughter investigates", "daughter searches", "kid investigates",
            "i will investigate", "i'll investigate", "i can investigate", "i will search", "i'll search", "i will find out", "i'll find out",
            "no acting alone",
        )
    )

    checks = {
        "power_demonstrated_before_explanation": power_demo_pos is not None and explanation_pos is not None and power_demo_pos < explanation_pos,
        "protective_bond_before_biological_proof": care_pos is not None and proof_pos is not None and care_pos < proof_pos,
        "procedural_identity_evidence": bool(re.search(r"dna|paternity|lab|birth record|hospital record|death certificate|legal|witness|sealed|chain of custody|report", full)),
        "child_agency_investigation": child_investigation,
        "power_has_social_or_bodily_cost": bool(re.search(r"monster|dangerous|afraid|privacy|secret|unstable|weak|risk|bullet|hurt|collapse|dizzy", full)),
        "power_destabilized_or_removed_before_resolution": bool(power_loss_pos is not None and (closure_pos is None or power_loss_pos < closure_pos)) or bool(re.search(r"power.*(?:gone|lost|unstable)|super strength.*gone|normal (?:six|six-year-old|child|kid)|don.?t need.*visions?", finale_text)),
        "love_not_payment_for_power": bool(re.search(r"not (?:my )?bodyguard|don.?t love you because|love .*not .*save|our turn to protect|we.*protect you|you.?re my daughter", full)),
        "ordinary_belonging_closure": bool(re.search(r"home|someone will|now i know you will|normal|ordinary|cake|school|family|wedding|come when.*afraid", finale_text)),
        "sequel_hook_after_belonging_closure": not sequel_pos or (closure_pos is not None and closure_pos < sequel_pos),
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
