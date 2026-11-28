"""BL power/autonomy romance integrity checks.

Derived from Smith drama-US hit/medium/low evidence. Transparent creative
warnings, not performance prediction.
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


def _segments(text: str) -> list[str]:
    normalized = re.sub(r"\.\.\.+", "…", text)
    return [part.strip() for part in re.split(r"[.!?\n]", normalized) if part.strip()]


def _has_coercive_control(text: str) -> bool:
    patterns = (
        r"(?:kiss(?:es|ed)?|touch(?:es|ed)?|forces?|takes?|presses?).{0,50}without (?:asking|permission|consent)",
        r"without (?:asking|permission|consent).{0,20}(?:kiss|touch|force|bed|sex)",
        r"not free to leave|(?:can['’]?t|cannot|not allowed) to? ?leave|keeps? .{0,25}captive|locks? .{0,25}(?:in|room)|owns? (?:him|them)|treats? .{0,25}property|no consent",
    )
    negated_ownership = re.compile(r"(?:doesn['’]?t|does not|never|no longer)\s+owns?")
    outside_romance_actor = re.compile(r"rival|villain|antagonist|kidnapper|captor|enemy")
    for sentence in _segments(text):
        if outside_romance_actor.search(sentence):
            continue
        for pattern in patterns:
            for match in re.finditer(pattern, sentence):
                if "own" in match.group(0) and re.search(r"(?:doesn['’]?t|does not|never|no longer)\s*$", sentence[max(0, match.start() - 20):match.start()]):
                    continue
                return True
    return False


def evaluate_bl_power_autonomy_romance_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    queer_or_pack = bool(re.search(r"\bbl\b|male omega|alpha|omega|werewolf|wolf king|vampire|male pregnancy|boyfriend|straight man|straight guy|male-male|\bgay\b|his husband|her wife", full))
    power = bool(re.search(r"billionaire|king|coach|boss|mafia|auction|paid|bought|save|rescued|patron|heir|prince", full))
    romance = bool(re.search(r"romance|boyfriend|husband|lover|kiss|marry|pregnant|crush|relationship|fell? for", full))
    if not (queer_or_pack and power and romance):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    opening = full[:max(1, len(full) // 3)]
    ending_units = scenes[-max(1, min(4, len(scenes))):] if scenes else []
    if isinstance(architecture, dict):
        for key in ("ending", "ending_payoff", "resolution", "final_act"):
            if key in architecture:
                ending_units.append(architecture[key])
        if not scenes and isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
            ending_units.extend(architecture["sequences"][-max(1, min(3, len(architecture["sequences"]))):])
    ending = (_text(ending_units) or full[-max(1, len(full) // 3):]).lower()

    coercive_control = _has_coercive_control(full)

    checks = {
        "protagonist_has_independent_craft_or_goal": bool(re.search(r"perfumer|formula|hockey|dance|job|career|investigat|work|practice|tryout|researcher|doctor|records|mission", opening)),
        "power_asymmetry_is_explicit": bool(re.search(r"billionaire|king|coach|boss|auction|paid|bought|chains|owns?|power|status|heir|mafia|alpha", full)),
        "bodily_or_species_rules_are_explicit": bool(re.search(r"heat|pheromone|scent|mark|omega|alpha|pregnant|wolf|werewolf|vampire|blood|shift|species|bond", full)),
        "rescue_or_payment_does_not_create_ownership": bool(re.search(r"not a bargaining chip|can't buy|cannot buy|not yours|doesn't own|no promise|contract is gone|release|free to leave|free to walk away|(?:can|may|allowed to) walk away|you can leave|not property|own answer", full) and not coercive_control),
        "intimacy_uses_micro_consent_and_refusal_rights": bool(re.search(r"you can just say no|tell me to move away|you could have told me|ask|permission|consent|trial run|won't cross the line|if you don't want|your choice|answer", full) and not coercive_control),
        "competence_or_care_is_procedural": bool(re.search(r"practice|training|formula|tryout|records|investigation|doctor|write down|pain meds|evidence|report|test|procedure|lesson", full)),
        "medical_or_care_support_preserves_agency": bool(re.search(r"doctor|hospital|memory|headache|write down|not going to promise|pain meds|food|tell me|you can be angry|care|recover", full)),
        "institutional_truth_or_justice_is_procedural": bool(re.search(r"police|records|investigation|evidence|report|documents|preservation|responsibility|contract|lawyer|both sets", full)),
        "romance_is_rechosen_after_leverage_is_questioned": bool(re.search(r"boyfriend|trial run|not telling you to forgive|isn't yours to give|choose|choice|answer|want more|not property|free to leave", full) and not coercive_control),
        "ending_preserves_future_agency_or_commitment_terms": bool(re.search(r"rest of (?:my|our) life|marriage|relationship|i can wait|won't cross the line|future|choice|choose|home|family|commitment", ending)),
    }
    labels = {
        "protagonist_has_independent_craft_or_goal": "the desired/manipulated man lacks independent craft, work, investigation, sport, or goal before attachment",
        "power_asymmetry_is_explicit": "power asymmetry is decorative rather than explicit king/coach/boss/auction/payment/status leverage",
        "bodily_or_species_rules_are_explicit": "omegaverse/supernatural body rules are used without explicit heat, scent, mark, blood, pregnancy, or transformation consequences",
        "rescue_or_payment_does_not_create_ownership": "rescue, payment, or protection is allowed to read as ownership rather than explicitly preserving freedom/refusal",
        "intimacy_uses_micro_consent_and_refusal_rights": "intimacy lacks micro-consent, refusal rights, ask/answer structure, trial boundaries, or line-crossing negotiation",
        "competence_or_care_is_procedural": "competence/care is asserted rather than practiced, documented, medically handled, investigated, or procedurally verified",
        "medical_or_care_support_preserves_agency": "caregiving overrides agency instead of preserving memory, anger, pain, food, medical choice, and self-directed recovery",
        "institutional_truth_or_justice_is_procedural": "truth/justice is emotional rather than police, records, documents, evidence, contracts, or responsibility procedure",
        "romance_is_rechosen_after_leverage_is_questioned": "romance is never explicitly rechosen after rescue, debt, status, coaching, or ownership leverage is questioned",
        "ending_preserves_future_agency_or_commitment_terms": "the ending assumes possession or marriage without future agency, explicit commitment terms, or line-respecting choice",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "BL power romance works when the desired man has independent craft or goals, power asymmetry and bodily/species rules are explicit, rescue or payment never becomes ownership, intimacy is negotiated through micro-consent and refusal rights, care and truth remain procedural, romance is rechosen after leverage is questioned, and the ending preserves future agency or explicit commitment terms.",
    }
