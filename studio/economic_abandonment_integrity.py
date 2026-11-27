"""Economic-abandonment mutual-aid repair integrity checks."""
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


def _affirmative_match(pattern: str, text: str) -> bool:
    for clause in re.split(r"[.!?;]", text):
        for match in re.finditer(pattern, clause):
            before = clause[:match.start()]
            if re.search(r"(?:nobody|no one|never|without)\s+(?:\w+\s+){0,8}$", before):
                continue
            return True
    return False


def evaluate_economic_abandonment_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    ending_source = "\n".join([architecture_text, scenes_text])
    ending = ending_source[-max(1, len(ending_source) // 3):] if ending_source else ""

    abandonment = bool(re.search(r"left (?:her|him|them)|walked away|letter|train station|don.?t belong|betray(?:ed|al)?|stole everything|took everything|abandoned (?:his|her|their) (?:wife|husband|fiance|partner|family)", full))
    economic = bool(re.search(r"money|wallet|id\b|debt|loan|orchard|property|business|contract|fraud|invoice|bank|assets", full))
    romance_or_family = bool(re.search(r"husband|wife|wedding|marriage|fianc|romance|mother|family|daughter", full))
    applies = abandonment and economic and romance_or_family
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    checks = {
        "abandonment_strips_identity_infrastructure": bool(re.search(r"purse|phone|wallet|id\b|ring|home|money|suitcase|letter|job|credit", full)),
        "first_repair_is_mutual_aid_and_work": bool(re.search(r"caf|job|work|room upstairs|shelter|meal|food|mutual aid|not charity|earn|labor|broom", full)),
        "competence_precedes_romantic_security": bool(re.search(r"invoice|price|financial|bookkeeping|contract|notices?|figures? out|lawyer|ledger|evidence|competence", full)),
        "purchased_rescue_or_class_bribe_is_refused": bool(re.search(r"leave (?:town|chicago)|\$?\d+[,.]?\d*.*leave|pay your way|buy.*out|bribe|check|purchased rescue|not what.*thinks|refus", full)),
        "financial_truth_is_procedural": bool(re.search(r"invoice|financials|power of attorney|notar|revocation|bank|loan|purchase agreement|court|judge|prosecutor|records?|signature|proof|evidence", full)),
        "restitution_is_measurable": _affirmative_match(r"\$\d[,.\d]*|default is cured|auction is canceled|pays? back|repay|transfer|in (?:her|his|their) name|loan.*paid|debt.*paid|restitution", full),
        "romance_cannot_require_abandoning_rescuer": bool(re.search(r"maggie|rescuer|wherever i live|our home is her home|chosen family|not by blood|mother|mom", full)),
        "final_acceptance_is_conditional_and_free": bool(re.search(r"before i answer|need to know|wherever i live|choose|choice|yes|our home|no more hiding|free", ending)),
        "ending_repairs_threshold_into_owned_belonging": bool(re.search(r"door of (?:her|his|their) own|business|home|wedding|family|orchard|caf|own name|belong|mom", ending)),
    }
    labels = {
        "abandonment_strips_identity_infrastructure": "abandonment is emotional rather than materially stripping money, ID, phone, home, documents, objects, or credit",
        "first_repair_is_mutual_aid_and_work": "first repair is romantic/charity rescue instead of mutual aid, work, food, shelter, or labor dignity",
        "competence_precedes_romantic_security": "heroine/hero lacks financial, legal, operational, or investigative competence before romantic security",
        "purchased_rescue_or_class_bribe_is_refused": "story does not refuse class bribery or purchased rescue that repeats the original exclusion",
        "financial_truth_is_procedural": "financial betrayal is asserted without invoices, contracts, POA, bank/loan records, signatures, court, or evidence chains",
        "restitution_is_measurable": "repair lacks measurable repayment, debt cure, asset transfer, ownership, loan payment, or restitution",
        "romance_cannot_require_abandoning_rescuer": "new romance does not account for the person/community that first provided shelter and care",
        "final_acceptance_is_conditional_and_free": "final romantic acceptance is not conditional, informed, and free",
        "ending_repairs_threshold_into_owned_belonging": "ending does not transform the abandonment threshold into owned home, business, family, or belonging",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Economic abandonment melodrama works when first repair is mutual-aid labor, competence precedes romantic security, purchased rescue is refused, financial truth is procedural, restitution is measurable, and final love includes the rescuer/chosen family inside a freely chosen belonging structure.",
    }
