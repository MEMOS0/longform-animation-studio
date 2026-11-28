"""Protective-kinship and instrumental-marriage repair integrity checks.

Derived from the Mythora Realm `5vGUIhUlt0A` deep dive. These are creative
warnings, not performance predictors: they test whether a falsely monstrous
caregiver story turns child protection into material action, child agency,
household competence, and consent-repaired partnership rather than decorative
stepmother romance.
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


def _first(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return match.start() if match else None


def _first_non_negated(pattern: str, text: str) -> int | None:
    for match in re.finditer(pattern, text):
        sentence_start = max(
            text.rfind(".", 0, match.start()),
            text.rfind("!", 0, match.start()),
            text.rfind("?", 0, match.start()),
            text.rfind("\n", 0, match.start()),
        ) + 1
        prefix = text[sentence_start:match.start()]
        positive_completion = re.search(r"not hesitate to\s*$|without hesitation\s*$|without (?:my|your|his|her|their) permission\s*$", prefix)
        negated = re.search(r"\b(?:refus\w*|withhold\w*|without|never|not)\b(?:\s+\w+){0,3}\s*$", prefix)
        sentence_end_positions = [pos for pos in [text.find(".", match.end()), text.find("!", match.end()), text.find("?", match.end()), text.find("\n", match.end())] if pos != -1]
        sentence_end = min(sentence_end_positions) if sentence_end_positions else len(text)
        conditional_constraint = re.search(r"\bonly (?:after|if|when)\b[^.!?]{0,50}\b(?:marry\w*|marriage|permission|obligation|stay\w*|pay\w*|debt\w*|contract|servitude|earn)\b", text[match.end():sentence_end])
        if (positive_completion or not negated) and not conditional_constraint:
            return match.start()
    return None


def _order_status(text: str, before_pattern: str, after_pattern: str) -> bool | None:
    before = _first_non_negated(before_pattern, text)
    after = _first_non_negated(after_pattern, text)
    if before is None or after is None:
        return None
    return before < after


def evaluate_protective_kinship_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    chronology = "\n".join([architecture_text, scenes_text]) if (architecture_text + scenes_text).strip() else premise_text
    flat = re.sub(r"\s+", " ", full)
    chronology_flat = re.sub(r"\s+", " ", chronology)

    child_center = bool(re.search(r"\b(?:child|children|daughter|daughters|son|sons|orphan|ward|heir)\b", flat))
    kinship_or_marriage = bool(re.search(r"stepmother|stepfather|guardian|bride|wife|husband|marriage|family|kinship|chosen family", flat))
    explicit_reputation = bool(re.search(r"viper|monster|unwomanly|dangerous reputation|called (?:her|him|them) cruel|false reputation|stigmatized", flat))
    coerced_or_instrumental_marriage = bool(re.search(r"sold (?:her|him|them)|arranged marriage|contract marriage|instrumental marriage|forced marriage", flat))
    if not (child_center and kinship_or_marriage and (explicit_reputation or coerced_or_instrumental_marriage)):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    autonomy_pattern = r"(?:transfers?|gives?|hands?|grants?)[^.!?]{0,60}(?:keys|treasury|accounts|estates|revenues|money|control)|freedom to leave|material autonomy|free to leave|she can refuse"
    intimacy_pattern = r"kiss|real marriage|intimacy|wedding renewal|chooses? (?:him|her|them)|says yes"
    truth_pattern = r"admits?|confess(?:es|ed)?|tells? (?:[a-z][a-z'-]{1,28} )?the truth|truth is revealed|reveals? the truth|acknowledges?"
    rechoice_pattern = r"real marriage|chooses? (?:him|her|them)|says yes|kiss|re-choice|renewal"

    def source_order(before_pattern: str, after_pattern: str) -> bool:
        scene_status = _order_status(scenes_text, before_pattern, after_pattern) if scenes_text.strip() else None
        if scene_status is not None:
            return scene_status
        architecture_status = _order_status(architecture_text, before_pattern, after_pattern) if architecture_text.strip() else None
        if architecture_status is not None:
            return architecture_status
        return False

    autonomy_pos = _first_non_negated(autonomy_pattern, chronology)

    checks = {
        "false_monster_reputation_is_grounded_in_resistance": bool(re.search(r"viper|monster|cruel|unwomanly|dangerous", flat) and re.search(r"strike back|hit back|fought back|resist|abuse|cornered|sold", flat)),
        "child_neglect_is_materially_visible": bool(re.search(r"split shoes|broken shoes|bruise|dark circles|thin (?:nightdress|blanket|clothes)|empty wardrobe|freezing room|cold room|starv|half-starved|servants' quarters|crushed lantern", flat)),
        "caregiver_creates_reporting_and_protection_structure": bool(re.search(r"tell me immediately|report (?:harm|abuse)|if anyone hurts you|protect(?:s|ing)? (?:the )?(?:children|daughters)|defend(?:s|ing)? (?:the )?(?:children|daughters)", flat)),
        "children_receive_agency_not_only_rescue": bool(re.search(r"teach(?:es|ing)? .{0,40}(?:defend|fight|hit back)|self-defense|defend yourself|scream|run to me|refuse false apology|don.?t apologize|children choose|child agency", flat)),
        "domestic_governance_functions_as_competence": bool(re.search(r"hot water|blankets|food|breakfast|household|keys|treasury|ledger|accounts|budget|room assignments|audit|steward", flat)),
        "family_rhetoric_is_tested_by_material_care": bool(re.search(r"family protects children|blood is blood|we.?re family|inheritance|robbed them|stole from them|owe nothing", flat)),
        "authority_response_is_procedural_not_impulsive": bool(re.search(r"audit|ledger|evidence|investigate|listens? to the children|seal every exit|trial|public proof|divide the house|institutional consequence", flat)),
        "instrumental_marriage_betrayal_is_named": bool(re.search(r"used (?:me|her|him)|chose (?:me|her|him) because|needed (?:her|his) strength|without telling (?:her|him) the truth|instrumental marriage|marriage is anything but a bargain", flat)),
        "material_autonomy_transfer_precedes_intimacy": source_order(autonomy_pattern, intimacy_pattern),
        "truth_disclosure_precedes_re_choice": source_order(truth_pattern, rechoice_pattern),
        "consent_preserving_re_choice": bool(_first_non_negated(r"can refuse|can leave|free to leave|you don.?t have to|if you need time|asks? permission|permission to touch|with (?:her|his|their) permission|uncoerced|freely chosen", chronology)),
        "child_power_is_not_property": bool(
            re.search(r"child .{0,50}(?:power|gift|magic|flame|healing)|healing (?:flame|gift)|magical gift", flat)
            and (
            re.search(r"belongs? to (?:herself|himself|themselves)|not (?:a )?(?:miracle|object|property)", flat)
            or _first_non_negated(r"(?:rejects?|refuses?|challenges?|objects? to|condemns?|denounces?|opposes?)[^.!?]{0,80}children as property", flat) is not None
        )
        ),
        "exploitative_blood_family_is_rejected": bool(re.search(r"blood is blood|birth family|stepmother|father .{0,40}(?:debt|money)|family has missed you", flat) and re.search(r"owe nothing|reject|refuse|do not answer|threw .{0,30}fire|make them somewhere else", flat)),
        "closure_is_durable_chosen_family_labor": bool(re.search(r"years later|time jump|wedding renewal|breakfast|ordinary|home|children .{0,40}(?:choose|leave only when)|domestic continuity|shared nighttime labor", chronology_flat[-max(1, len(chronology_flat) // 2):])),
    }
    labels = {
        "false_monster_reputation_is_grounded_in_resistance": "the monster/viper reputation is asserted without concrete abusive cause or resistance history",
        "child_neglect_is_materially_visible": "child neglect remains emotional exposition instead of visible clothing/room/body/object evidence",
        "caregiver_creates_reporting_and_protection_structure": "the caregiver protects reactively but does not create a reporting/protection structure children can use",
        "children_receive_agency_not_only_rescue": "children are rescued but not taught agency, refusal, self-defense, or help-seeking",
        "domestic_governance_functions_as_competence": "domestic labor, accounts, food, keys, or room allocation are missing as concrete competence",
        "family_rhetoric_is_tested_by_material_care": "blood/family rhetoric is not tested against theft, neglect, inheritance, or material care",
        "authority_response_is_procedural_not_impulsive": "the authority figure instantly takes sides instead of listening, auditing, proving, and imposing consequence",
        "instrumental_marriage_betrayal_is_named": "instrumental use in the marriage is romanticized rather than named as betrayal",
        "material_autonomy_transfer_precedes_intimacy": "romance/intimacy arrives before material autonomy, keys, money, control, or exit freedom",
        "truth_disclosure_precedes_re_choice": "the partner re-chooses before learning the truth about the instrumental marriage",
        "consent_preserving_re_choice": "the renewed bond lacks explicit refusal rights, waiting, permission, or uncoerced choice",
        "child_power_is_not_property": "child power functions as a prize/property rather than the child's own agency and care capacity",
        "exploitative_blood_family_is_rejected": "abusive blood relatives receive automatic reconciliation or rescue despite returning only for exploitation",
        "closure_is_durable_chosen_family_labor": "closure stops at spectacle/status instead of proving durable chosen-family domestic labor over time",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Protective-kinship melodrama works when a false monster reputation is reframed as resistance to abuse, neglect becomes material evidence, the caregiver builds reporting/agency structures, domestic governance proves competence, family rhetoric is tested by material care, authority responds procedurally, instrumental marriage is confessed and repaired through autonomy before intimacy, child power belongs to the child, exploitative blood family is rejected, and closure proves durable chosen-family labor.",
    }
