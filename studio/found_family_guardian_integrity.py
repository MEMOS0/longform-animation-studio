"""Compressed found-family guardian integrity checks."""
from __future__ import annotations

import re
from typing import Any


def _text(value: Any) -> str:
    if isinstance(value, str): return value
    if isinstance(value, dict): return "\n".join(_text(v) for v in value.values())
    if isinstance(value, list): return "\n".join(_text(v) for v in value)
    return ""


def _pos(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return match.start() if match else None


def _last_pos(pattern: str, text: str) -> int | None:
    matches = list(re.finditer(pattern, text))
    return matches[-1].start() if matches else None


def _ending_keyed_text(value: Any) -> str:
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            key_text = str(key).lower()
            if re.search(r"ending|finale|resolution|epilogue|payoff|final_sequence_use|closing_reversal", key_text):
                parts.append(_text(item))
            elif isinstance(item, (dict, list)):
                parts.append(_ending_keyed_text(item))
        return "\n".join(parts)
    if isinstance(value, list):
        return "\n".join(_ending_keyed_text(item) for item in value)
    return ""


def evaluate_found_family_guardian_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    guardian_core = bool(re.search(r"\bgiant\b|creature parent|nonhuman parent|adoptive parent|adoptive mother|adoptive father", full))
    personal_guardian_patterns = [
        r"guardian\s+(?:of|for|to)\s+(?:the\s+|a\s+|an\s+)?(?:child|children|daughter|infant|baby|orphan)\b",
        r"guardian.{0,40}(?:raises?\b|feeds?\b|shelters?\b|protects\b)",
        r"(?:child|daughter|infant|baby|orphan)\b.{0,80}(?:becomes?|as)\s+(?:her|his|their)\s+guardian",
        r"(?:raises?|adopts?|takes? in).{0,80}guardian",
    ]
    personal_guardian = False
    for pattern in personal_guardian_patterns:
        explicit_child_object = pattern.startswith("guardian\\s")
        for match in re.finditer(pattern, full):
            window = full[max(0, match.start() - 30):match.end() + 30]
            if re.search(r"guardian\s+(?:of|for|to)\s+(?:the\s+|a\s+|an\s+)?orphanage\b", window):
                continue
            if not explicit_child_object and re.search(r"\bcity(?:'s)?\b|\bpublic\b|\bkingdom\b|\bpeople\b", window):
                continue
            personal_guardian = True
            break
        if personal_guardian:
            break
    child = bool(re.search(r"daughter|child|children|infant|baby|orphan", full))
    applies = child and (guardian_core or personal_guardian)
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    care_pos = _pos(r"feed|warm|teach|train|hunt|protect|raise|shelter|fire|blanket", full)
    rupture_positions = [m.start() for m in re.finditer(r"argument|rupture|leaves|departure|run(?:s)? away", full)]
    rupture_pos = next((pos for pos in rupture_positions if care_pos is None or pos > care_pos), None)
    rescue_pos = _last_pos(r"rescue|save|carries|carry|crossbow|army|final confrontation", full)
    seqs = architecture.get("sequences", []) if isinstance(architecture, dict) else []
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else {}
    premise_end = _ending_keyed_text(premise)
    architecture_has_ending = bool(seqs[-2:] or ending_payoff)
    if len(scenes) < 5 and not architecture_has_ending and premise.get("logline"):
        logline = str(premise.get("logline")).lower()
        clauses = re.split(r"[.!?;]\s*", logline)
        ending_clauses = [clause for clause in clauses if re.search(r"in the end|at the end|final(?:ly)?|aftermath|epilogue", clause) and re.search(r"home(?:coming)?|rebuild|reunit|carries|carry", clause)]
        premise_end = "\n".join([premise_end, *ending_clauses]).strip()
    finale_text = "\n".join([_text(seqs[-2:]), _text(ending_payoff), _text(scenes[-5:]), premise_end]).strip().lower()
    care_categories = {
        "feeding": bool(re.search(r"\bfeed(?:s|ing)?\b|\bfood\b|\bbread\b|\bmilk\b|\beat(?:s|ing)?\b", full)),
        "warmth": bool(re.search(r"\bwarm(?:s|ed|th)?\b|\bfire\b|\bblanket\b|\bshelter(?:s|ed|ing)?\b", full)),
        "teaching": bool(re.search(r"\bteach(?:es|ing)?\b|\btrain(?:s|ed|ing)?\b|\blearn(?:s|ed|ing)?\b", full)),
        "survival": bool(re.search(r"\bhunt(?:s|ed|ing)?\b|\btrack(?:s|ed|ing)?\b|\bbow\b|\bsurvive(?:s|d)?\b", full)),
        "protection": bool(re.search(r"\bprotect(?:s|ed|ing)?\b|\bshield(?:s|ed)?\b|\bhide(?:s|n|ing)?\b|\bsave(?:s|d)?\b", full)),
        "rest": bool(re.search(r"\bsleep(?:s|ing)?\b|\brest(?:s|ed|ing)?\b|\bbed\b", full)),
        "carrying": bool(re.search(r"\bcarry\b|\bcarries\b|\bcarried\b|\bshoulder\b", full)),
    }

    checks = {
        "origin_endangerment_before_exposition": bool(re.search(r"pursu|chase|flee|danger|serpent|wolf|attack|birth|infant|newborn", full[:2000])),
        "rescue_transfer_into_guardian_custody": bool(re.search(r"rescues?|saves?|adopt|raises?|takes? (?:her|him|the child)|bursts? through", full)),
        "repeated_operational_care": sum(care_categories.values()) >= 2 or (any(care_categories.values()) and bool(re.search(r"years pass|as the years pass|montage|grows? up|over time", full))),
        "child_gains_agency_or_competence": bool(re.search(r"learns?|hunt|survive|bow|arrow|track|choose|leaves|journey", full)),
        "relational_rupture_before_external_rescue": care_pos is not None and rupture_pos is not None and rescue_pos is not None and care_pos < rupture_pos < rescue_pos,
        "guardian_misread_as_property_or_monster": bool(re.search(r"fortune|captured?|monster|beast|property|army|ruthless lord|crossbow|trap", full)),
        "public_trap_or_impossible_odds": bool(re.search(r"city square|public|army|crossbow|trap|gate|prison|imprisoned", full)),
        "physical_custody_or_carrying_closure": bool(re.search(r"carries|carry|on his back|shoulder|home|reunit|embrace|holds? .*close", finale_text)),
    }
    labels = {
        "origin_endangerment_before_exposition": "story lacks immediate origin endangerment before fantasy exposition",
        "rescue_transfer_into_guardian_custody": "child is not transferred into guardian custody through rescue/care",
        "repeated_operational_care": "guardian bond lacks repeated operational care across time",
        "child_gains_agency_or_competence": "child remains passive and gains no agency/competence",
        "relational_rupture_before_external_rescue": "rescue lacks a prior care -> rupture -> rescue emotional chain",
        "guardian_misread_as_property_or_monster": "outsiders do not misread/exploit the guardian as monster, property, or fortune",
        "public_trap_or_impossible_odds": "climax lacks public trap or impossible odds",
        "physical_custody_or_carrying_closure": "ending does not physically restore custody/contact/home",
    }
    warnings=[label for key,label in labels.items() if not checks[key]]
    return {"applies":True,"score_0_to_1":round(sum(checks.values())/len(checks),3),"warnings":warnings,"checks":checks,"craft_rule":"Compressed guardian fantasy works when scale serves care: origin danger transfers a child into nonhuman custody, repeated care and competence build attachment, rupture precedes external rescue, and the climax physically restores custody rather than merely defeating enemies."}
