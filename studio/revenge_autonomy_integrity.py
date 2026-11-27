"""Revenge-autonomy integrity checks for victim-authored revenge melodrama."""
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
    for clause in re.split(r"[.!?;]|\bbut\b", text):
        for match in re.finditer(pattern, clause):
            before = clause[:match.start()]
            if re.search(r"(?:(?:nobody|no one|never|without|not|no)\s+(?:\w+\s+){0,8}|refus(?:es|ed)?\s+to\s+(?:\w+\s+){0,8})$", before):
                continue
            return True
    return False


def _ending_tail(text: str) -> str:
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    if len(sentences) == 1:
        words = text.split()
        return " ".join(words[-max(1, len(words) // 3):]) if words else ""
    if sentences:
        count = max(1, (len(sentences) + 2) // 3)
        return "\n".join(sentences[-count:])
    return text[-max(1, len(text) // 3):] if text else ""


def evaluate_revenge_autonomy_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    ending = _ending_tail("\n".join([architecture_text, scenes_text]))

    betrayal = bool(re.search(r"betray|humiliat|pushed|thrown|attempted murder|cheat|deceiv|identity fraud|switched places|twin|false identity", full))
    survival_return = bool(re.search(r"(?:presumed|believed|thought|everyone thought).*dead|drowned|near[- ]death|new identity|alias|new name|returns? (?:as|after|from)|comes back (?:as|after|from)|reborn", full))
    revenge = bool(re.search(r"revenge|avenge|destroy them|make them pay|sting|trap|expose|take .*down|reckoning", full))
    applies = betrayal and survival_return and revenge
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    checks = {
        "betrayal_is_consent_or_power_violation_not_simple_rudeness": bool(re.search(r"consent|switched places|identity fraud|false identity|forced|blackmail|threat|public humiliation|pushed|thrown|attempted murder|stolen|deceived", full)),
        "public_humiliation_creates_witnesses": bool(re.search(r"public|wedding|auction|launch|party|room|crowd|guests|filmed|witnesses|trending|spectators", full)),
        "survival_has_physical_cost": bool(re.search(r"hospital|doctor|breath|heartbeat|injur|blood|drown|water|unconscious|medical|pain|lost.*child|miscarriage|body", full)),
        "victim_authors_revenge_plan": bool(re.search(r"she plans|he plans|they plan|i plan|she decides|he decides|chooses|strategy|trap|sting|bait|weapon|orchestrat|sets? up", full)),
        "rescuer_supports_without_owning_rebirth": bool(re.search(r"only if.*want|you choose|don.?t get to decide|supports?|helps?|not.*own|consent|asks? before|doesn.?t touch|won.?t touch", full)),
        "new_identity_is_victim_chosen": bool(re.search(r"new name|alias|chooses .*name|who do you want to be|calls? herself|identity.*choice|not erase", full)),
        "objects_convert_trauma_into_evidence_or_leverage": bool(re.search(r"letter|phone|key|files?|documents?|records?|bottle|formula|perfume|object|seal|serial|camera|accounts?|ledger|evidence|proof", full)),
        "revenge_reverses_original_power_structure": bool(re.search(r"bait|public room|auction|stage|launch|same room|turns? the tables|uses? .*against|what they want|desire|ownership|predator close", full)),
        "spectacle_converts_to_procedure": bool(re.search(r"police|federal|court|lawyer|regulator|legal|accounts? frozen|evidence|files?|signature|escrow|verified|warrant|arrest|investigation|chain of custody", full)),
        "no_forced_forgiveness_or romantic_possession": _affirmative_match(r"no more favors|won.?t forgive|not forgiven|don.?t forgive|don.?t belong|won.?t belong|not yours|refus|no\b", full),
        "ending_centers_autonomy_before_romance": _affirmative_match(r"free|freedom|live|won.?t belong|don.?t belong|not belong|independent|her own|his own|their own|wait|choose|choice", ending),
        "romance_is_deferred_and_nonpossessive": bool(re.search(r"i.?ll wait|if you choose|when you.?re ready|no pressure|not yours|don.?t belong|doesn.?t claim|free choice", ending)),
    }
    labels = {
        "betrayal_is_consent_or_power_violation_not_simple_rudeness": "betrayal is ordinary conflict rather than a consent, coercion, identity, violence, or public-power violation",
        "public_humiliation_creates_witnesses": "humiliation lacks public witnesses/social spectatorship that can later be reversed",
        "survival_has_physical_cost": "survival/return skips bodily, medical, grief, or material cost",
        "victim_authors_revenge_plan": "rescuer or allies author the revenge while the victim remains passive",
        "rescuer_supports_without_owning_rebirth": "rescuer controls the transformation or treats the victim as owned",
        "new_identity_is_victim_chosen": "new identity is imposed rather than chosen by the victim",
        "objects_convert_trauma_into_evidence_or_leverage": "revenge lacks concrete objects, documents, accounts, records, or evidence/leverage",
        "revenge_reverses_original_power_structure": "revenge does not reverse the original public/power mechanism against the perpetrators",
        "spectacle_converts_to_procedure": "public exposure remains spectacle without legal, financial, regulatory, or evidentiary consequences",
        "no_forced_forgiveness_or romantic_possession": "ending pressures forgiveness or transfers the victim into romantic possession",
        "ending_centers_autonomy_before_romance": "ending centers couple formation before autonomy, freedom, or self-ownership",
        "romance_is_deferred_and_nonpossessive": "romantic closure is possessive/immediate rather than deferred, waiting, or freely chosen",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Victim-authored revenge melodrama works when survival has cost, the victim chooses the rebirth and plan, objects become evidence or leverage, public humiliation is reversed into procedural consequences, and autonomy precedes any deferred nonpossessive romance.",
    }
