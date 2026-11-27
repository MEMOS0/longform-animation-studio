"""Restitution-pact accountability integrity checks.

Derived from Mini Series Drama yA_UfmmVAG0 evidence. These heuristics are
creative warnings, not performance predictors: they test whether a supernatural
sacrifice story turns betrayal, restored perception, bodily extraction, and
late repentance into a legible moral contract rather than decorative lore.
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


def evaluate_restitution_pact_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    chronology = "\n".join([architecture_text, scenes_text]) if (architecture_text + scenes_text).strip() else premise_text
    full = "\n".join([premise_text, architecture_text, scenes_text])
    flat = re.sub(r"\s+", " ", full)
    chronology_flat = re.sub(r"\s+", " ", chronology)

    bodily_cost = bool(re.search(r"eyes?|sight|blind|vision|blood|heart|voice|hearing|memory|memories|body|life force|healing labor", flat))
    sacrifice = bool(re.search(r"sacrific|trade[sd]?|gave up|give up|offers?|price|cost|pact|bargain|in exchange", flat))
    supernatural_contract = bool(re.search(r"pact|curse|demon|vow|oath|magic bargain|magical bargain|supernatural bargain|rebound|restitution|restores? (?:her|his|their )?(?:eyes|sight|vision|voice|memory)", flat))
    betrayal_or_extraction = bool(re.search(r"betray|unfaithful|cheat|false victim|frame[sd]?|took|drain|extract|cut out|steal|exploit|abandon", flat))
    applies = bodily_cost and sacrifice and supernatural_contract and betrayal_or_extraction
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    vow_pos = _first(r"protect (?:her|him|them|you) forever|never let anyone hurt|swear|vow|oath|promise to protect", chronology)
    betrayal_pattern = r"betray|unfaithful|cheat|chose not to turn around|abandon|false victim|frame[sd]?|took (?:her|his|their) blood|cut out"
    betrayal_pos = None
    for betrayal_match in re.finditer(betrayal_pattern, chronology):
        sentence_start = max(
            chronology.rfind(".", 0, betrayal_match.start()),
            chronology.rfind("!", 0, betrayal_match.start()),
            chronology.rfind("?", 0, betrayal_match.start()),
            chronology.rfind("\n", 0, betrayal_match.start()),
        ) + 1
        prefix = chronology[sentence_start:betrayal_match.start()]
        conditional_marker = re.search(r"\b(?:if|unless)\b[^.!?]{0,30}$", prefix)
        previous_lines = chronology[:sentence_start].rstrip().splitlines()
        if previous_lines and re.search(r"(?<!not )(?<!no )\b(?:if|unless)\s*$", previous_lines[-1].strip()):
            conditional_marker = True
        sentence_ends = [pos for pos in [
            chronology.find(".", betrayal_match.end()),
            chronology.find("!", betrayal_match.end()),
            chronology.find("?", betrayal_match.end()),
            chronology.find("\n", betrayal_match.end()),
        ] if pos != -1]
        sentence_end = min(sentence_ends) if sentence_ends else len(chronology)
        betrayal_sentence = chronology[sentence_start:sentence_end]
        temporal_pact_marker = bool(
            re.search(r"\b(?:when|whenever)\b[^.!?]{0,30}$", prefix)
            and re.search(r"pact|curse|rebound|returns?|restores?", betrayal_sentence)
            and (
                re.search(r"\bwhenever\b[^.!?]{0,30}$", prefix)
                or re.search(r"rule|terms|states?|explains?|according to|would|will|were to|should", betrayal_sentence)
            )
        )
        if conditional_marker or temporal_pact_marker:
            continue
        betrayal_pos = betrayal_match.start()
        break
    restitution_pos = _first(r"eyes? (?:are )?returned|sight returns?|restores? (?:her|his|their )?(?:eyes|sight|vision)|can see again|awakened|red eyes", chronology)
    reveal_pos = _first(r"they (?:find out|learn|discover)|he finds out|she finds out|publicly reveal|identity is revealed|truth is exposed", chronology)
    extraction_positions = [
        pos for pos in [
            _first(r"eyes?|sight|vision", chronology),
            _first(r"blood|drain", chronology),
            _first(r"heart|cut out", chronology),
        ]
        if pos is not None
    ]
    extraction_escalates = len(set(extraction_positions)) >= 2 and extraction_positions == sorted(extraction_positions)

    care_pos = _first(r"alternative partner|chosen partner|new partner|butler|healer|protector|he (?:cares|heals|protects|tends|waits|respects)|she (?:cares|heals|protects|tends|waits|respects)", chronology)
    status_pos = _first(r"king|queen|lord|powerful|rich|wealthy|high status|head of|identity reveal|you.?re .{0,20}(?:king|lord)", chronology)
    refusal_or_exit_pos = _first(r"she (?:refuses|rejects|chooses to leave|wants? to end)|he (?:refuses|rejects|chooses to leave|wants? to end)|free to leave|end (?:the |our )?engagement|let her go", chronology)
    identity_reveal_pos = _first(r"you.?re (?:the )?(?:king|lord|[A-Z][a-z]+)?|identity reveal|reveals? (?:his|her) identity|hidden identity", chronology)
    mutual_closure = bool(re.search(r"mutual vow|only husband|only wife|chosen family|home|belonging|reciprocal|if you live|if you die|freely chosen", chronology[-max(1, len(chronology) // 3):]))

    checks = {
        "explicit_bodily_sacrifice_cost": bodily_cost and bool(re.search(r"sacrific|trade[sd]?|gave up|offers?|price|cost|in exchange", full)),
        "conditional_accountability_mechanism": bool(re.search(r"if .{0,80}(?:betray|hurt|harm).{0,100}(?:return|restore|rebound|curse|consequence)|betrayal .{0,60}(?:returns?|restores?|triggers?|rebounds?)|the deeper they hurt", chronology_flat)),
        "beneficiaries_vow_protection_before_betrayal": vow_pos is not None and betrayal_pos is not None and vow_pos < betrayal_pos,
        "restored_perception_creates_hidden_irony": restitution_pos is not None and bool(re.search(r"can.?t let them know|must hide|hides? (?:her|his|their) (?:sight|vision|knowledge|power)|pretends? to still be blind|secretly sees|dramatic irony", chronology_flat)) and (reveal_pos is None or restitution_pos < reveal_pos),
        "bodily_extraction_escalates_through_entitlement": extraction_escalates and bool(re.search(r"dead weight|useful|useless|blood bag|owes? us|always wanted to help|it.?ll grow back|not actually trying to kill|resilience|can survive", chronology_flat)),
        "caretaker_history_is_inverted_into_resource_ownership": bool(re.search(r"saved (?:them|us|him)|protected (?:them|us)|healed (?:them|us)", flat) and re.search(r"owes?|useful|resource|blood bag|dead weight|property|belongs? to us|guard(?:ing)? a", chronology_flat)),
        "public_forced_choice_reveals_real_hierarchy": bool(re.search(r"pick one|choose one|forced choice|on this side|on that side|in front of (?:everyone|the crowd)|public test|choose (?:her|him|them) or", chronology_flat)),
        "consequence_is_visible_moral_ledger": bool(re.search(r"curse rebounds?|become(?:s)? (?:true )?(?:monsters?|bat|beast)|monstrous consequence|visible consequence|transformation .{0,50}(?:betrayal|curse|moral)|permanent", chronology_flat)),
        "instrumental_repentance_is_not_rewarded": bool(re.search(r"apolog|repent|regret|sorry|forgive", chronology_flat)) and bool(re.search(r"only (?:to|so they can|so he can) break|to break the curse|never forgive|does not forgive|won.?t forgive|regret is not repair|too late|gave you chances", chronology_flat)),
        "alternative_partner_proves_care_before_status": care_pos is not None and status_pos is not None and care_pos < status_pos,
        "consent_or_exit_choice_precedes_identity_reward": refusal_or_exit_pos is not None and identity_reveal_pos is not None and refusal_or_exit_pos < identity_reveal_pos,
        "closure_is_mutual_not_forced_forgiveness": mutual_closure and not bool(re.search(r"forced to forgive|must forgive them|owes? them forgiveness", chronology_flat)),
    }
    labels = {
        "explicit_bodily_sacrifice_cost": "bodily/sensory sacrifice is implicit rather than a concrete price the protagonist pays",
        "conditional_accountability_mechanism": "supernatural pact/curse is decorative because betrayal does not trigger explicit restitution or consequence",
        "beneficiaries_vow_protection_before_betrayal": "beneficiaries do not make a protection vow before violating it, weakening contractual accountability",
        "restored_perception_creates_hidden_irony": "restored perception immediately becomes safety/exposition instead of hidden dramatic irony",
        "bodily_extraction_escalates_through_entitlement": "bodily extraction does not escalate through entitlement excuses such as usefulness, resilience, or reversible harm",
        "caretaker_history_is_inverted_into_resource_ownership": "prior care is not inverted into resource ownership, so the antagonists' entitlement remains abstract",
        "public_forced_choice_reveals_real_hierarchy": "story lacks a public forced-choice test that reveals whom the betrayers instinctively value",
        "consequence_is_visible_moral_ledger": "consequence is random spectacle rather than a visible moral ledger tied to the pact",
        "instrumental_repentance_is_not_rewarded": "late repentance is rewarded even when motivated by curse-breaking, fear, or self-preservation",
        "alternative_partner_proves_care_before_status": "alternative partner's status appears before concrete care, making the romance read as upgrade rather than trust",
        "consent_or_exit_choice_precedes_identity_reward": "identity/status reveal happens before the protagonist can refuse, leave, or choose freely",
        "closure_is_mutual_not_forced_forgiveness": "closure forces forgiveness or possession instead of mutual chosen witness",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Restitution-pact melodrama works when bodily sacrifice creates a conditional moral contract, betrayal restores perception as hidden dramatic irony, caretaker history is inverted into extraction, public choice reveals the betrayers' real hierarchy, consequences visualize the moral ledger, self-preserving repentance fails, and the alternative bond earns trust through care and consent before status.",
    }
