"""Wrongful-accusation restoration integrity checks."""
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


def evaluate_wrongful_accusation_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    ending_source = "\n".join([architecture_text, scenes_text])
    ending = _ending_tail(ending_source)

    explicit_false_accusation = bool(re.search(r"wrongful|wrongfully|framed|frame-up|set up|false accusation|falsely accused|planted", full))
    exonerated_accusation = bool(re.search(r"accused|theft|stolen|expelled", full)) and bool(re.search(r"clears?|exonerat|innocent|didn.?t (?:steal|do it)|proves? .*innocent", full))
    accusation = explicit_false_accusation or exonerated_accusation
    status_wound = bool(re.search(r"homeless|expelled|fired|excluded|stigma|scholarship|reputation|career|land|estate", full))
    repair_context = bool(re.search(r"truth|evidence|investigat|court|lawyer|apology|restoration|job|work", full))
    applies = accusation and status_wound
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    checks = {
        "competence_precedes_pity": bool(re.search(r"tools?|repair|fix|work|job|groundskeeper|build|practical|competence|labor", full)),
        "stigma_has_material_consequences": bool(re.search(r"nobody hires|no job|homeless|housing|credit|expelled|scholarship|excluded|reputation|lost.*career", full)),
        "original_lie_has_material_contradiction": bool(re.search(r"still (?:wears|has)|same watch|planted|fake|copy|letter|object|contradiction|wasn.?t gone|already", full)),
        "second_frameup_exposes_original_mechanism": bool(re.search(r"again|repeats?|same trick|necklace.*bag|watch.*bag|planted.*again|frame.*again|second accusation", full)),
        "help_preserves_dignity_through_work": bool(re.search(r"job|work for|groundskeeper|earn|labor|not charity|not with your money|not for me|don.?t pay", full)),
        "love_interest_investigates_instead_of_instantly_believing": _affirmative_match(r"investigat|questions?|timeline|records?|evidence|not sure|doubt|prove|verify|chain of custody", full),
        "truth_chain_is_procedural": _affirmative_match(r"camera|footage|911|log|record|pawn|jeweler|witness|court|judge|warrant|lawyer|signature|documents?|evidence|chain of custody", full),
        "anti_payment_boundary_preserves_agency": bool(re.search(r"not with your money|not for me|don.?t pay|not charity|pay.*wins|buy.*out|refus", full)),
        "institutional_restoration_repairs_stolen_future": _affirmative_match(r"apolog|readmission|reinstat|scholarship|semester|school|degree|reputation restored|land stays|trust|career|job", ending),
        "romantic_closure_is_present_tense_consent": _affirmative_match(r"don.?t have to answer|ask|choose|yes|will you|if you still want|this time|consent", ending),
    }
    labels = {
        "competence_precedes_pity": "accused person is pitiable before being practically competent",
        "stigma_has_material_consequences": "accusation lacks material consequences such as expulsion, unemployment, homelessness, lost scholarship, housing, credit, or reputation",
        "original_lie_has_material_contradiction": "original accusation lacks a visible object/document/timeline contradiction",
        "second_frameup_exposes_original_mechanism": "plot does not use repetition of the frame-up mechanism to expose the original injustice",
        "help_preserves_dignity_through_work": "help is charity or payment rather than dignified labor/agency",
        "love_interest_investigates_instead_of_instantly_believing": "love interest simply believes because of romance rather than investigating evidence and doubt",
        "truth_chain_is_procedural": "truth is asserted without camera, records, witnesses, court, documents, logs, chain of custody, or verification",
        "anti_payment_boundary_preserves_agency": "wealthy help can buy the solution and repeat the power imbalance",
        "institutional_restoration_repairs_stolen_future": "ending punishes or romanticizes without restoring school, work, reputation, land control, or institutional apology",
        "romantic_closure_is_present_tense_consent": "romantic closure relies on the past letter/love without present-tense asking, choice, or consent",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Wrongful-accusation melodrama works when practical competence precedes pity, a repeated frame-up exposes the original mechanism, help remains dignified labor, love investigates rather than instant-believes, procedure proves truth, institutions restore the stolen future, and romance closes through present-tense consent.",
    }
