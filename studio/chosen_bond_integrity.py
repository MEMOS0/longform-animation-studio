"""Anti-fate chosen-bond re-choice integrity checks.

Derived from Lotus Crown dHdkaKb3_S8 evidence. These are creative heuristics,
not performance predictions: they distinguish chosen devotion and accountability
from copied fated-mate mythology or status-upgrade romance.
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


def _opening_text(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    if isinstance(premise, dict):
        for key, value in premise.items():
            lowered = str(key).lower()
            if "opening" in lowered or lowered.startswith("first_") or lowered in {"inciting_event", "prologue"}:
                parts.append(_text(value))
    sequences = architecture.get("sequences") if isinstance(architecture, dict) else None
    if isinstance(sequences, list) and sequences:
        count = max(1, (len(sequences) + 2) // 3)
        parts.extend(_text(sequence) for sequence in sequences[:count])
    if scenes:
        count = max(1, (len(scenes) + 2) // 3)
        parts.extend(_text(scene) for scene in scenes[:count])
    return "\n".join(parts).lower()


def _ending_tail(text: str) -> str:
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    if len(sentences) > 1:
        return "\n".join(sentences[-max(1, (len(sentences) + 2) // 3):])
    words = text.split()
    return " ".join(words[-max(1, len(words) // 3):]) if words else ""


def _first(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return match.start() if match else None


def _segment_has_opening_betrayal(segment: str) -> bool:
    public = bool(re.search(r"wedding|ceremony|crowd|public|banquet|clan|pack|court", segment))
    betrayal = bool(re.search(r"cheat|betray|another woman|another mate|humiliat|share|stolen crown| crowns? another", segment))
    delayed = bool(re.search(r"betrayal (?:arrives|comes|happens).{0,25}later|years later", segment))
    return public and betrayal and not delayed


def evaluate_chosen_bond_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    chronology = chr(10).join([architecture_text, scenes_text]) if (architecture_text + scenes_text).strip() else premise_text
    flat = re.sub(r"\s+", " ", full)
    opening_raw = _opening_text(premise, architecture, scenes)
    opening = re.sub(r"\s+", " ", opening_raw)
    ending = _ending_tail(chronology)

    destiny_system = bool(re.search(r"fated mate|fate\b|destiny|destined|soul bond|mate bond|bonding ceremony|imprint|chosen bond", flat))
    romantic_bond = bool(re.search(r"mate|marry|marriage|wedding|bride|fianc|queen|king|partner|vow|romance|betrothal", flat))
    betrayal_or_rechoice = bool(
        re.search(r"(?:mate|husband|wife|fiance|partner|spouse|bond).{0,100}(?:cheat|betray|humiliat|abandon|reject|share|chooses? another)|(?:cheat|betray|humiliat|abandon|reject|share|chooses? another).{0,100}(?:mate|husband|wife|fiance|partner|spouse|bond)", flat)
        or re.search(r"re-choice|rechoose|chooses? (?:a |the )?(?:new|alternative|chosen) (?:mate|partner|bond)", flat)
    )
    applies = destiny_system and romantic_bond and betrayal_or_rechoice
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    sacrifice_terms = bool(re.search(r"blood essence|blood magic|life force|power core|healing labor|elixir|medicine|magic|energy|resources?|money|sacrifice", flat))
    system_value = bool(re.search(r"sustain|support|keep.*at bay|suppress|heal|restore|save|protect|maintain|power.*(?:clan|family|house|pack)|succession|position|status", flat))
    refusal_pattern = r"\bi (?:will not|won.?t|refuse|do not accept)|\bshe (?:refuses|rejects|walks away|chooses? to leave|says? no)|\bprotagonist (?:refuses|rejects|walks away)|\bheroine (?:refuses|rejects|walks away)"
    upgrade_pattern = r"new partner|chosen partner|chosen bond|alternative (?:mate|partner)|better partner|elf king|new queen|accepts? (?:the|a) (?:king|queen|partner|mate)|marries? (?:the|a) (?:king|queen|partner)"
    refusal_pos = _first(refusal_pattern, chronology)
    upgrade_pos = _first(upgrade_pattern, chronology)
    alternative_care_pattern = r"\b(?:he|chosen partner|new partner|alternative partner|elf king|king)\b\s+(?:cares?|heals?|restores?|protects?|tends?|feeds?|shelters?|comforts?|waits?|supports?)"
    care_pos = (upgrade_pos + _first(alternative_care_pattern, chronology[upgrade_pos:])) if upgrade_pos is not None and _first(alternative_care_pattern, chronology[upgrade_pos:]) is not None else None
    reciprocity_pos = _first(r"she believes|she trusts|she reciprocates|she chooses him|she accepts|mutual vow|returns? (?:his|their) (?:love|loyalty)|i do\b", chronology)

    exposure_categories = sum(bool(re.search(pattern, flat)) for pattern in [
        r"witness|public|crowd|banquet|ceremony|guests?",
        r"mark|scar|body|blood|resonat|heartbeat|physical proof",
        r"letter|ring|document|record|potion|object|physical evidence|forensic proof",
        r"testimony|confess|admits?|investigation|questioning",
        r"mechanism|how the potion|formula|spell|resonance rule|blood rule",
    ])

    repentance = bool(re.search(r"repent|sorry|apolog|regret|begs? (?:for )?(?:forgiveness|another chance)|win (?:her|him|them) back|come back to me", flat))
    repentance_rejected = bool(re.search(r"refus(?:es|ed) (?:reconciliation|forgiveness|to return|to go back)|rejects? (?:his|her|their) (?:apology|repentance|regret)|does not forgive|won.?t forgive|no reconciliation|not enough to repair|regret is not repair|you chose power", flat))
    forgiveness_pressure = bool(re.search(r"forced to forgive|must forgive|pressure(?:d|s)? .*forgive|family makes? (?:her|him|them) forgive", flat))

    coercive_new_bond = bool(re.search(r"force(?:s|d)? (?:her|him|them)? ?to marry|forced marriage|(?:marry|marries) (?:her|him|them) against (?:her|his|their) will|no choice but to marry|coerc(?:es?|ed|ion).{0,40}(?:marry|marriage|mate|bond)", chronology))
    consent_language = bool(re.search(r"explicit consent|free consent|freely chosen|choose freely|chosen (?:partner|bond|mate)|consent|no pressure|need not force|won.?t bind|doesn.?t bind|asks? (?:for )?(?:her |his |their )?(?:consent|permission)|waits? (?:for )?(?:her |his |their )?(?:answer|choice)|patient", chronology))

    checks = {
        "public_betrayal_opening": any(
            _segment_has_opening_betrayal(segment)
            for segment in re.split(r"[.!?]", opening_raw.lower().replace(chr(10), ".")) if segment.strip()
        ),
        "sacrificial_labor_has_system_value": sacrifice_terms and system_value,
        "fate_functions_as_excuse": bool(re.search(r"fate.*(?:excuse|can't resist|cannot resist|inevitable|made me|forces? us|means? we must)|destiny.*(?:excuse|inevitable|can't resist)|so-called fate|curse we can.?t resist|supposed to share", flat)),
        "protagonist_refuses_before_upgrade": refusal_pos is not None and upgrade_pos is not None and refusal_pos < upgrade_pos,
        "alternative_bond_is_chosen_and_consenting": consent_language and bool(re.search(r"bond|vow|mate|partner|queen|king|marriage", chronology)) and not coercive_new_bond,
        "care_precedes_romantic_reciprocity": care_pos is not None and reciprocity_pos is not None and care_pos < reciprocity_pos,
        "late_repentance_is_not_rewarded": (not repentance) or repentance_rejected,
        "exposure_is_layered_evidence": exposure_categories >= 3,
        "institutional_consequence_matches_institutional_theft": bool(re.search(r"council|court|law|elders?|publicly strips?|stripped of|title revoked|banish|revoke|resources revoked|succession removed|accountability|restitution|loses? (?:the )?(?:title|crown|succession|position)", flat)),
        "closure_reclassifies_home_or_chosen_family": bool(re.search(r"home|chosen family|family|belonging|peace|sanctuary|freely chosen|chosen bond|mutual vow", ending)),
        "forgiveness_is_not_coerced": not forgiveness_pressure and (repentance_rejected or not re.search(r"forgiv", flat) or bool(re.search(r"freely choos(?:es?|ing) to forgive|forgives? only after (?:truth|repair|accountability)", flat))),
    }
    labels = {
        "public_betrayal_opening": "destiny-bond betrayal is not public, concrete, and legible in the opening",
        "sacrificial_labor_has_system_value": "protagonist sacrifice/care does not materially sustain the betrayer, family, or power system",
        "fate_functions_as_excuse": "fate/destiny is decorative lore rather than an ideology used to excuse choice and entitlement",
        "protagonist_refuses_before_upgrade": "higher-status alternative appears before the protagonist has meaningfully refused the humiliating bond",
        "alternative_bond_is_chosen_and_consenting": "new bond is not framed through chosen, patient, consenting devotion rather than ownership or destiny",
        "care_precedes_romantic_reciprocity": "romantic reciprocity happens before concrete care, healing, protection, or consent-preserving patience",
        "late_repentance_is_not_rewarded": "self-centered late repentance or regret is treated as sufficient repair",
        "exposure_is_layered_evidence": "truth exposure lacks layered public, physical, object, testimony, mechanism, or procedural evidence",
        "institutional_consequence_matches_institutional_theft": "institutional exploitation is answered only by emotion or spectacle rather than titles/resources/legal/public consequences",
        "closure_reclassifies_home_or_chosen_family": "ending does not transform belonging/home/family order around chosen nonpossessive bonds",
        "forgiveness_is_not_coerced": "forgiveness/reconciliation is pressured or treated as obligatory rather than free and consequence-aware",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Chosen-bond fantasy romance works when public betrayal exposes fate as an excuse, the protagonist refuses before any upgrade, sacrificial care collapses the exploiter's system, the alternative bond is patient and consenting, truth is exposed through layered evidence, institutions remove stolen power, and closure rebuilds home through free choice rather than forced forgiveness.",
    }
