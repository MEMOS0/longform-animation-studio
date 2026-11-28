"""Retributive romance reversal integrity checks.

Derived from Payback Stories hit/medium/low evidence. Transparent creative
warnings, not performance predictions. Applies when a betrayed partner uses
rebirth, exit, evidence, or relational reversal to escape a controlling or
deprioritizing romantic system.
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


def evaluate_retributive_romance_reversal_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    romance = bool(re.search(r"wife|husband|fianc|marriage|married|bride|groom|mistress|lover|wedding|spouse", full))
    betrayal = bool(re.search(r"mistress|stepsister|another woman|chose|abducted|kidnapped|controlling|control|cage|gps|tracker|sent .*100|ignored|left me|betray|cheat|ruined my life|begged", full))
    reversal = bool(re.search(r"reborn|second chance|walked away|walks? away|leav(?:e|ing)|divorce|destroy|payback|revenge|took everything|cancel(?:ed)?|gifted.*stepsister|never trust him|new life", full))
    if not (romance and betrayal and reversal):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    architecture_text = _text(architecture).lower()
    final_scene_text = _text(scenes[-1]).lower() if scenes else ""
    ending_parts: list[str] = []
    if isinstance(architecture, dict):
        for key, value in architecture.items():
            if re.search(r"ending|final|closing|resolution|epilogue|payoff", str(key).lower()):
                ending_parts.append(_text(value).lower())
        sequences = architecture.get("sequences") or architecture.get("sequence")
        if isinstance(sequences, list) and sequences:
            ending_parts.append(_text(sequences[-1]).lower())
    ending_text = "\n".join(ending_parts + [final_scene_text]) or (architecture_text[-max(1, len(architecture_text) // 3):] if architecture_text else full[-max(1, len(full) // 4):])

    checks = {
        "betrayal_is_concrete_coercive_or_materially_costly": bool(re.search(r"gps|tracker|froze|passport|cut off|abducted|kidnapped|bullet|hospital|surgery|baby|sent .*100|withheld|drug trials|died|death|faked amnesia|no leaving|no being alone|black card", full)),
        "boundary_is_decisive_and_behavioral": bool(re.search(r"call off|cancel(?:ed)?|walked away|walks? away|packing|leav(?:e|ing)|divorce|moved.*passport|never trust|turned around|did not choose|no longer welcome|cutting ties", full)),
        "reversal_uses_evidence_institutions_or_competence_not_only cruelty": bool(re.search(r"evidence|lawyer|police|prison|recording|trial|court|trust|shares|company|career|destroyed|exposed|transfers|documents|publicly|media", full)),
        "late_regret_or_sacrifice_does_not_restore_access": bool(re.search(r"no love left|no hatred left|removed himself|lost the privilege|doesn\'t run after|too late|not forgiveness|zero credit|never trust|felt nothing|does not restore|walked away", full)),
        "new_intimacy_is_behaviorally_careful_and_consensual": bool(re.search(r"neither pressuring|waits patiently|choice|freedom to decide|doesn\'t interrupt|check if.*healing|treasures|protects you|protective|wide open sky|courage to love|careful|gentlemanly", full)),
        "ending_preserves_freedom_or_noncoercive_chosen_love": bool(re.search(r"free|freedom|wide open sky|courage to love|peaceful|new life|never look back|chose herself|independent|protects you|marry me|yes|walked away|brand new", ending_text)),
        "self_destruction_is_not_used_as_romantic_justice": not bool(re.search(r"pressed the barrel|suicide|kill(?:ed|ing)? himself|die to atone|i\'ll be there soon.*pistol|service pistol.*temple", full)),
    }
    labels = {
        "betrayal_is_concrete_coercive_or_materially_costly": "the betrayal is vague romantic neglect rather than coercive control, medical/financial abandonment, violence, or repeated material cost",
        "boundary_is_decisive_and_behavioral": "the protagonist threatens revenge but never cancels, leaves, divorces, hides access, or behaviorally exits the abusive arrangement",
        "reversal_uses_evidence_institutions_or_competence_not_only cruelty": "payback is only cruelty or spectacle rather than evidence, law, institutional consequences, financial control, or competent exposure",
        "late_regret_or_sacrifice_does_not_restore_access": "the abuser's regret, injury, sacrifice, or suffering magically reopens romantic access instead of remaining separate from consent",
        "new_intimacy_is_behaviorally_careful_and_consensual": "replacement romance is instant possession rather than careful attention, patience, choice, and respect for trauma",
        "ending_preserves_freedom_or_noncoercive_chosen_love": "the ending rewards the coercive ex or leaves only punishment instead of freedom, peace, self-rule, or freely chosen noncoercive love",
        "self_destruction_is_not_used_as_romantic_justice": "self-destruction is framed as romantic atonement or satisfying justice; use consequences, repair, refusal, or institutional accountability instead",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {"applies": True, "score_0_to_1": round(sum(checks.values()) / len(checks), 3), "warnings": warnings, "checks": checks, "craft_rule": "Retributive romance reversal works when coercive/material betrayal is concrete, the protagonist behaviorally exits, payback uses evidence or institutions, regret or sacrifice does not purchase access, new intimacy is patient and consensual, self-destruction is not romantic justice, and the ending preserves freedom or noncoercive chosen love."}
