"""Strategic romantic deception integrity checks.

Derived from Seven Clover hit/medium/low evidence. Transparent creative warnings,
not performance predictions. Applies when a romance begins through professional
sabotage, fake pregnancy/marriage, hidden identity, or strategic pretense.
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


def evaluate_strategic_romantic_deception_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    romance = bool(re.search(r"wedding|marriage|marry|wife|husband|fianc|bride|groom|romance|love", full))
    deception = bool(re.search(r"fake pregnancy|pregnancy report|chicken blood|fake marriage|pretend|pretense|ruin (?:this|a|the)? ?wedding|sabotage (?:this|a|the)? ?wedding|wedding sabotage|hidden identity|fake amnesia|imposter|impostor|contract marriage|arrangement", full))
    strategic = bool(re.search(r"paid|fifty grand|ten million|contract|arrangement|mission|job|professional|compensat|test|blind date|sabotage|ruin", full))
    if not (romance and deception and strategic):
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

    retaliation_scan = re.sub(r"(?:refus\w+|won't|wouldn't|did not|decided not|chose not)[^.]{0,50}(?:pull|withdraw|withhold)[^.]{0,30}(?:team|support|technical)?", " ", ending_text)
    coercion_retaliation = bool(re.search(r"withdraw(?:s|ing|al of)? (?:the )?(?:technical )?support|pull(?:s|ing)? (?:the )?(?:team|support|technical)|withhold(?:s|ing)? support|force(?:s|d)? (?:her|him|them)? ?(?:back|reconciliation)|punish(?:es|ing)? (?:her|him|them) for rejecting", retaliation_scan))
    pretense_scan = re.sub(r"no longer (?:has|have|had) to keep pretending|(?:doesn't|don't|do not) have to keep pretending|stop(?:ped)? pretending", " ", ending_text)
    freely_chosen = not bool(re.search(r"no choice|forced|coerced|compelled|has to keep pretending|keep pretending", pretense_scan))
    checks = {
        "deception_has_material_motive_and_visible_professional_competence": bool(re.search(r"surgery money|medical bills|paid|fifty grand|ten million|professional|mission|job|report|chicken blood|acting|resourceful|plan|evidence", full)),
        "deception_is_bounded_by_terms_exit_or_compensation": bool(re.search(r"contract|arrangement|one year|compensat|divorce|end here|mission a success|terms|deal|what\'s in it for you|keep things as they are", full)),
        "partner_is_not_a_passive_fool_and_has_agency": bool(re.search(r"see through|play along|i object|don\'t agree|co-?create|guessed|knew|suspect|test|choice|refuse|reject|doesn\'t owe|no right", full)),
        "intimacy_requires_consent_uncertainty_or_behavioral_trust": bool(re.search(r"do you like me|does she feel nothing|keep my distance|i don\'t think of you that way|brave|face my feelings|feelings|trust|not forcing|respect|choose his own marriage", full)),
        "rejection_is_not_punished_through_money_or_institutional_power": bool(re.search(r"she doesn't owe me a thing|the deal stands|collaboration will continue|not petty|business is business|won't force|respect your wishes|no coercion", full)) and not coercion_retaliation,
        "truth_and_consequences_use_evidence_or_procedure": bool(re.search(r"recording|confession|evidence|police|lawyer|death penalty|dna|board|shares|files|arrest|custody|verified|law", full)),
        "ending_replaces_pretense_with_freely_chosen_commitment_or_independent_truth": freely_chosen and bool(re.search(r"real love|real couple|wife for real|becomes real|brave|face my feelings|of course i do|freely|choose|independent|ability|not.*deal|honest|truth", ending_text)),
    }
    labels = {
        "deception_has_material_motive_and_visible_professional_competence": "the romantic deception is arbitrary lying rather than a materially motivated, professionally executed strategy",
        "deception_is_bounded_by_terms_exit_or_compensation": "the deception has no contract, compensation, time limit, exit, or other boundary and therefore reads as coercion",
        "partner_is_not_a_passive_fool_and_has_agency": "the deceived partner is merely gullible rather than seeing through, testing, refusing, or actively co-creating the arrangement",
        "intimacy_requires_consent_uncertainty_or_behavioral_trust": "attraction leaps over consent and uncertainty instead of being built through distance, testing, trust, or explicit emotional choice",
        "rejection_is_not_punished_through_money_or_institutional_power": "rejection is punished through money, business leverage, family pressure, or institutional power rather than respected",
        "truth_and_consequences_use_evidence_or_procedure": "wrongdoing resolves through melodramatic accusation rather than recordings, evidence, law, board procedure, or verified facts",
        "ending_replaces_pretense_with_freely_chosen_commitment_or_independent_truth": "the ending keeps the pretense or coercive bargain instead of converting it into freely chosen commitment or independent truth",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {"applies": True, "score_0_to_1": round(sum(checks.values()) / len(checks), 3), "warnings": warnings, "checks": checks, "craft_rule": "Strategic romantic deception works when the deception is materially motivated and professionally legible, bounded by terms or exit, met by partner agency rather than gullibility, intimacy is consented through uncertainty and trust, rejection is not punished through money or institutional power, wrongdoing is resolved through evidence, and the ending replaces pretense with freely chosen commitment or independent truth."}
