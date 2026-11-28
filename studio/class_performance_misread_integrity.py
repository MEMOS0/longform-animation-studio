"""Class-performance misread integrity checks.

Derived from QueenDrama hit/medium/low evidence. These are transparent creative
warnings, not performance predictions. Applies when rebirth lets a protagonist
stop performing wealth/status and other people misread that non-performance as
old-money pedigree.
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


def evaluate_class_performance_misread_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    rebirth = bool(re.search(r"reborn|rebirth|second life|past life|first life|years? earlier|lived once before", full))
    class_arena = bool(re.search(r"old money|wealthy|rich|heiress|socialite|elite|aristocrat|countess|manor|invitation|exclusive|designer|pedigree|dynasty|high society|status", full))
    misread = bool(re.search(r"misread|mistaken for|believe(?:s|d)? (?:she|he|they)|assume(?:s|d)?|suspect(?:s|ed)?|think(?:s|ing)? (?:she|he|they)|appears? to be|looks? like|convinc(?:ed|ing)|family explanation|secret dynasty|powerful family", full))
    nonperformance = bool(re.search(r"stop(?:s|ped)? performing|done performing|no longer pretends?|not auditioning|refus\w+|turns? down|ordinary|unbothered|does not need (?:status|approval)|likes? (?:herself|himself|themselves)|being herself|authentic", full))
    if not (rebirth and class_arena and misread and nonperformance):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    final_scene_text = _text(scenes[-1]).lower() if scenes else ""
    ending_text = "\n".join([
        premise_text,
        architecture_text[-max(1, len(architecture_text) // 3):] if architecture_text else "",
        final_scene_text,
    ])
    real_dynasty_confirm = bool(re.search(
        r"confirmed? (?:as|that) (?:old money|a real dynasty|the heir)|secret dynasty is real|really is (?:old money|a billionaire heir|from a powerful family)|revealed? as (?:old money|a real heir|a powerful family)|guessed correctly",
        ending_text + "\n" + full[-max(1, len(full) // 4):],
    ))
    projection_evidence = bool(re.search(
        r"no secret dynasty|no powerful family|not actually (?:old money|rich)|projection|family explanation|habit, not (?:her|his|their) secret|she actually doesn't need|only old money could be so unbothered",
        full,
    ))

    checks = {
        "prior_life_performance_has_material_cost": bool(re.search(
            r"first life.{0,180}(?:debt|spent|inheritance|humiliat|exposed|entertainment|mocked|fatal)|past life.{0,180}(?:debt|spent|inheritance|humiliat|exposed|entertainment|mocked|died)|spending money (?:she|he|they) should|buy(?:ing)? (?:her|his|their) way into belonging",
            full,
        )),
        "rebirth_change_is_behavioral_not_new_identity": bool(re.search(
            r"stop(?:s|ped)? (?:performing|pretending|chasing)|puts? (?:her|his|their) bag wherever|turns? down|refus\w+|no longer audition|ordinary for a while|does not need (?:status|approval)|can ask a basic question|change (?:her|his|their) mind",
            full,
        )),
        "misread_comes_from_autonomous_taste_boundaries_or_generosity": bool(re.search(
            r"taste|boundary|refus\w+|generos\w+|help(?:s|ed)? (?:a roommate|someone|them)|save face|invest(?:s|ed|ment)?|bought early|unbothered|public speech|judgment|independent panel|not the family behind them",
            full,
        )),
        "audience_knows_status_is_projection_not_secret_dynasty": projection_evidence and not real_dynasty_confirm,
        "misreading_changes_social_power_and_access": bool(re.search(
            r"invitation|membership|private dinner|collector|foundation|president|social access|connections|black card|non-public collections|influential|gossip|who are (?:her|his|their) parents",
            full,
        )),
        "relationships_shift_from_status_competition_to_reciprocal_friendship": bool(re.search(
            r"no more making you compete|just be (?:her|his|their) friend|apolog|thank you|helped without making me feel stupid|if it's your problem, it's mine|you can change how you treat people|be decent to the people around you",
            full,
        )),
        "opportunity_is_gated_by_work_disclosure_or_procedure": bool(re.search(
            r"requirements|review process|independent panel|disclose|won't take part in reviewing|asked about the work before the title|doing the work|qualified to read|records|agreement|contract|evidence",
            full,
        )),
        "ending_preserves_ordinary_selfhood_beyond_status": bool(re.search(
            r"ordinary|same person|actually built|not a role|own name|be herself|being herself|does not need (?:status|approval)|self-worth|independent|choice|choose what comes next",
            ending_text,
        )),
    }
    labels = {
        "prior_life_performance_has_material_cost": "the prior life does not show that class performance cost money, dignity, safety, or belonging",
        "rebirth_change_is_behavioral_not_new_identity": "the rebirth improvement is a new disguise or wealth upgrade rather than visibly changed everyday behavior",
        "misread_comes_from_autonomous_taste_boundaries_or_generosity": "the old-money misreading is asserted rather than produced by specific taste, boundaries, judgment, or generosity",
        "audience_knows_status_is_projection_not_secret_dynasty": "the story does not preserve the dramatic irony that the status reading is projection rather than a real hidden dynasty",
        "misreading_changes_social_power_and_access": "the misreading has no concrete effect on invitations, institutions, collectors, gatekeepers, or social power",
        "relationships_shift_from_status_competition_to_reciprocal_friendship": "relationships remain status competition instead of becoming reciprocal friendship through apology, help, and changed treatment",
        "opportunity_is_gated_by_work_disclosure_or_procedure": "opportunities arrive as pure status rewards instead of work, disclosure, independent review, contracts, or procedure",
        "ending_preserves_ordinary_selfhood_beyond_status": "the ending validates pedigree instead of ordinary selfhood, named work, independence, and freedom from approval-seeking",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Class-performance rebirth drama works when performing status has already cost the protagonist materially, rebirth changes behavior rather than supplying a better disguise, others project old-money meaning onto autonomous taste/boundaries/generosity, the audience knows the dynasty is not real, institutions convert the misreading into access, relationships become reciprocal, opportunity stays procedural, and the ending protects ordinary selfhood rather than pedigree.",
    }
