"""Period autonomy/evidence romance integrity checks.

Derived from TeawithJay/Jay Studios period-drama comparison. Transparent
creative warnings, not performance predictions. Applies to Regency/period
romances where arranged duty, class reputation, artistic or intellectual labor,
consent, and evidence-driven vindication shape the love story.
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


def _story_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        parts = []
        for key, child in value.items():
            key_text = str(key).lower()
            if re.search(r"packag|thumbnail|marketing|poster|distribution|audience_target", key_text):
                continue
            parts.append(_story_text(child))
        return "\n".join(parts)
    if isinstance(value, list):
        return "\n".join(_story_text(v) for v in value)
    return ""


def evaluate_period_autonomy_evidence_romance_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_story_text(premise), _story_text(architecture), _story_text(scenes)]).lower()
    period = bool(re.search(r"\b(?:regency|period|duk(?:e|es|edom)|duchess(?:es)?|earl(?:s|dom)?|marquess(?:es)?|princess(?:es)?|lord(?:s|ship)?|aristocr\w*|ballroom\w*|carriage\w*|dowr\w*|banns|opera|society)\b", full))
    romance = bool(re.search(r"\b(?:romance|love\w*|marri\w*|wife|wives|husband\w*|bride\w*|heart\w*|kiss\w*|suitor\w*|wedding\w*)\b", full))
    constraint = bool(re.search(r"arranged|duty|title|class|reputation|scandal|society|royal|alliance|cast out|banish|disown|honor", full))
    if not (period and romance and constraint):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    architecture_text = _story_text(architecture).lower()
    final_scene_text = _story_text(scenes[-1]).lower() if scenes else ""
    ending_parts: list[str] = []
    if isinstance(architecture, dict):
        for key, value in architecture.items():
            if re.search(r"ending|final|closing|resolution|epilogue|payoff", str(key).lower()):
                ending_parts.append(_story_text(value).lower())
        sequences = architecture.get("sequences") or architecture.get("sequence")
        if isinstance(sequences, list) and sequences:
            ending_parts.append(_story_text(sequences[-1]).lower())
    ending_text = "\n".join(ending_parts + [final_scene_text]) or (architecture_text[-max(1, len(architecture_text) // 3):] if architecture_text else full[-max(1, len(full) // 4):])
    explicit_permission = bool(re.search(r"never (?:(?:kisses?|touches?|claims?|beds?|takes?)|initiates? intimacy)[^.\n]{0,80}without (?:her |his |their )?(?:consent|permission)|only (?:kisses?|touches?|claims?|beds?)[^.\n]{0,60}(?:with|after) (?:her |his |their )?(?:consent|permission)", full))
    nonconsensual_intimacy = bool(re.search(r"kiss\w*[^.\n]{0,80}(?:as|while|when)[^.\n]{0,50}(?:pulls? away|resists?|struggles?|tries? to stop)|(?:pulls? away|resists?|struggles?|tries? to stop)[^.\n]{0,80}kiss\w*|forced (?:kiss|intimacy)|(?<!never )kiss\w*[^.\n]{0,50}without (?:her |his |their )?(?:consent|permission)", full))
    respectful_stop = bool(re.search(r"stops? (?:immediately|as soon as)|pulls? away[^.\n]{0,50}(?:stops?|respects?)|respects?[^.\n]{0,50}pulls? away", full))
    nonconsensual_intimacy = nonconsensual_intimacy and not respectful_stop
    consent_scan = re.sub(r"without (?:her |his |their )?(?:consent|permission)|didn.?t (?:ask|seek) (?:consent|permission)|no consent|not consensual|unwanted|forced", " ", full)

    checks = {
        "social_constraint_has_material_cost": bool(re.search(r"cast out|banish|allowance|dowry|inherit|ruin|scandal|blacklist|without a shilling|lose|stripped|debt|reputation|dismiss", full)),
        "heroine_refuses_or_questions_objectifying_arrangement": bool(re.search(r"refus|won.?t|will not|not sell|no intention|choose|choice|freedom|rebellion|beneath|docility|not ruled", full)),
        "artistic_or_intellectual_competence_is_independent": bool(re.search(r"sing|voice|opera|music|book|read|write|scholar|garden|physician|poison|perform|stage|craft|work|skill", full)),
        "powerful_man_confronts_his_own_duty_or_control": bool(re.search(r"duty|mother.*dictate|i command|choose my own|hollow shell|cannot offer|forgive|apolog|amends|control|title", full)),
        "rival_or_arranged_party_retains_agency": bool(re.search(r"(?:princess|rival|arranged party|arranged match)[^.\n]{0,80}(?:agrees? by choice|freely chooses?|chooses? (?:to )?(?:end|release|refuse)|ends? (?:the )?match|royal decree|refuses? the match|rejects? (?:the )?(?:betrothal|match|arrangement)|rejects? (?:the )?(?:betrothal|match|arrangement))|(?:agrees? by choice|freely chooses?|chooses? (?:to )?(?:end|release|refuse)|ends? (?:the )?match|royal decree|refuses? the match|rejects? (?:the )?(?:betrothal|match|arrangement)|rejects? (?:the )?(?:betrothal|match|arrangement))[^.\n]{0,80}(?:princess|rival|arranged party|arranged match)|blameless|deserve", full)),
        "deception_or_misunderstanding_has_consequence_before_repair": bool(re.search(r"mask|secret|lie|decep|misunderstand|played|betray|vanished|truth|forgive|apolog|amends|make peace", full)),
        "intimacy_is_explicitly_consensual_and_reversible": (not nonconsensual_intimacy) and (explicit_permission or bool(re.search(r"you will tell me if you wish|do not wish|asked|permission|choose|choice|freely|consent|only if|not asking|worthy", consent_scan))),
        "social_or_bodily_accusation_is_resolved_through_evidence": bool(re.search(r"evidence|proof|witness|physician|doctor|symptom|poison|garden|register|engraving|testimony|magistrate|investigat|examined|verified|signed letter[^.\n]{0,60}(?:clears?|proves?|confess|testif)|independent (?:witness|examination|verification|investigation|copy|testimony)", full)),
        "ending_restores_voice_choice_or_home_not_only_marriage": bool(re.search(r"voice|music|home|choose|choice|begin again|worthy|forgive|reconcil|truth|name|freedom|independent|vocation|self-sufficient|agency|repair(?:s|ed|ing)? (?:the )?(?:harm|damage|trust|relationship|wrong)", ending_text)),
    }
    labels = {
        "social_constraint_has_material_cost": "period duty/reputation is abstract rather than materially costly",
        "heroine_refuses_or_questions_objectifying_arrangement": "the heroine does not actively refuse or question objectifying arrangement/ownership logic",
        "artistic_or_intellectual_competence_is_independent": "the heroine lacks independent artistic, intellectual, professional, or evidentiary competence",
        "powerful_man_confronts_his_own_duty_or_control": "the powerful man never confronts the duty, control, or family machinery that constrains him",
        "rival_or_arranged_party_retains_agency": "the rival/arranged party is a prop rather than a person with agency and dignity",
        "deception_or_misunderstanding_has_consequence_before_repair": "deception or misunderstanding is waved away without consequence and repair",
        "intimacy_is_explicitly_consensual_and_reversible": "intimacy/commitment lacks explicit consent, reversibility, or chosenness",
        "social_or_bodily_accusation_is_resolved_through_evidence": "accusation, mystery, or social judgment is resolved by assertion rather than evidence/testimony/procedure",
        "ending_restores_voice_choice_or_home_not_only_marriage": "the ending is only marriage/status rather than restored voice, chosen home, vocation, truth, or mutual repair",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Period autonomy romance works when social constraint has material cost, the heroine actively refuses objectifying arrangement, independent artistic/intellectual competence drives the bond, powerful men confront their own duty/control, rivals retain agency, deception has consequences before repair, intimacy is consensual and reversible, accusations resolve through evidence/procedure, and the ending restores voice, choice, home, truth, or vocation rather than mere marriage.",
    }
