"""Integrity checks for forbidden-family romance driven by dramatic irony.

Derived from DramaShine XL0d9SmAA1M evidence. These are creative heuristics,
not performance predictions: they separate a durable superior-knowledge engine
from copied coercion, possessiveness, or mafia power fantasy.
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
    elif architecture:
        text = _text(architecture)
        parts.append(text[: max(1, len(text) // 3)])
    if scenes:
        count = max(1, (len(scenes) + 2) // 3)
        parts.extend(_text(scene) for scene in scenes[:count])
    return "\n".join(parts).lower()


def _protagonist_names(value: Any) -> list[str]:
    names: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = str(key).lower()
            protagonist_key = "protagonist" in lowered or "heroine" in lowered or "main_character" in lowered
            if protagonist_key and isinstance(item, str) and len(item.split()) <= 5:
                names.append(item.lower())
                names.append(item.lower().split()[0])
            elif protagonist_key and isinstance(item, dict):
                for name_key in ("name", "identity"):
                    if isinstance(item.get(name_key), str):
                        candidate = item[name_key].lower()
                        if candidate.strip():
                            names.append(candidate)
                            names.append(candidate.split()[0])
            elif isinstance(item, (dict, list)):
                names.extend(_protagonist_names(item))
    elif isinstance(value, list):
        for item in value:
            names.extend(_protagonist_names(item))
    return names


def evaluate_taboo_family_irony_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    flat = re.sub(r"\s+", " ", full)
    opening_source = _opening_text(premise, architecture, scenes)

    family_taboo = bool(re.search(r"best(?:ie| friend).?s (?:dad|father|mom|mother|parent)|stepmom|stepmother|stepfather|father.?in.?law|mother.?in.?law|former guardian|guardian-ward", flat))
    romantic_power = bool(re.search(r"mafia|mob|godfather|don\b|ceo|billionaire|older man|age gap|boss", flat))
    romantic_relation = bool(re.search(r"marry|marries|married|marriage|husband|wife|bride|romance|lover|dating|partner|falls? in love|in love with", flat))
    hidden_relation = bool(re.search(r"secret|hidden identity|doesn.?t know|unaware|mistaken|wrong (?:man|woman|person)|lies|lying|truth", flat))
    applies = family_taboo and romantic_power and romantic_relation and hidden_relation
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    arena_terms = {
        "home": r"home|mansion|estate|breakfast|kitchen|bedroom|bathroom",
        "commerce": r"boutique|shop|mall|store|card|couture",
        "school": r"school|campus|college|class|principal",
        "sport_public": r"hockey|arena|game|finals|party|gala|dance",
        "crime_institution": r"mafia|crew|police|court|contract|business|operation",
    }
    arena_count = sum(1 for pattern in arena_terms.values() if re.search(pattern, full))

    coercion_present = bool(re.search(r"drunk(?:en)? marriage|mistake(?:n)? marriage|forced marriage|blackmail|no right to refuse|can.?t refuse|won.?t take no|cut(?:ting)? off (?:his |her |their |the )?access to (?:the )?internet|cut(?:ting)? (?:off )?(?:his |her |their |the )?internet|ship(?:ped|s)? .{0,25}away|surveillance|possessive|you are mine", flat))
    repair_behavior = bool(re.search(r"apolog|repair|explicit consent|free choice|choose freely|can leave|free to leave|respects? (?:her|his|their) (?:no|refusal|boundar)|honors? (?:her|his|their) (?:no|refusal|boundar)|asks? (?:permission|before)|no more lies|tells? the truth|truth before", flat))
    coercion_unrepaired = coercion_present and not repair_behavior

    agency_text = re.sub(r"no right to refuse|can.?t refuse|cannot refuse|won.?t take no", " ", flat)
    supporting_departure = bool(re.search(r"(?:best friend|friend|sister|mother|rival|supporting character).{0,35}chooses? to leave", agency_text))
    protagonist_names = _protagonist_names(premise)
    named_departure = any(re.search(r"\b" + re.escape(name.split()[0]) + r"\b chooses? to leave (?:him|her|them|the partner|the marriage|the relationship)", agency_text) for name in protagonist_names if name.split())
    pronoun_departure = bool(re.search(r"(?:she|he|they|protagonist|heroine) chooses? to leave (?:him|her|them|the partner|the marriage|the relationship)", agency_text))
    protagonist_agency = bool(re.search(r"we are done|she rejects|he rejects|she refuses|he refuses|stay away|can leave|free to leave|she decides|he decides|tells? (?:him|her|them) no|walks? away|asks? for (?:an )?annulment|right to refuse", agency_text) or named_departure or (pronoun_departure and not supporting_departure))
    truth_revealed = bool(re.search(r"truth|no more lies|identity is revealed|learns? who|realizes? who", flat))

    shared_reveal = bool(re.search(r"(?:audience|viewer|viewer.?s|reader).{0,50}learn.{0,30}together|(?:audience|viewer|viewer.?s|reader).{0,50}(?:same time|with the characters)|characters and (?:audience|viewers|readers) learn", flat))
    explicit_superiority = bool(re.search(r"audience knows|viewer knows|audience is aware|viewer is aware|dramatic irony|superior knowledge|only the audience|only the viewer", flat))
    asymmetric_knowledge = bool(re.search(r"while .{0,40}(?:unaware|doesn.?t know)|remains? unaware|still unaware|only .{0,25}knows", flat))
    audience_superior = explicit_superiority or (asymmetric_knowledge and not shared_reveal)

    checks = {
        "compounded_impossibility_early": sum(bool(re.search(pattern, opening_source)) for pattern in [r"wrong (?:man|person)|mistaken", r"marry|married|wife|husband|bride", r"best friend|bestie|stepmom|father|dad", r"mafia|godfather|boss|older man|powerful"]) >= 3,
        "audience_has_superior_knowledge": audience_superior,
        "protective_misdirector_active": bool(re.search(r"best friend|bestie|sister|brother|father|mother|guardian", full) and re.search(r"protect|warn|save|rescue|hide|cover|scheme|investigate|track|private investigator", full)),
        "social_arena_rotation": arena_count >= 4,
        "public_shame_or_class_wound": bool(re.search(r"publicly humiliat|shame|gold.?digger|class|poor|student loans|scholarship|slut|whore|cheap|beggar|sidepiece", full)),
        "power_acquires_rules_or_accountability": bool(re.search(r"rules|by the books|police|court|law|evidence|investigation|accountability|consequences|don.?t touch civilians|procedural", full)),
        "protagonist_can_reject_power": protagonist_agency,
        "possessiveness_is_flaw_not_reward": not coercion_unrepaired,
        "family_reclassification_hook": bool(re.search(r"stepmom|stepmother|best friend or|bestie or|call you now|family order|bloodline|part of the family|reclassif", full[-max(1, len(full)//2):])),
        "truth_and_consent_repair": truth_revealed and repair_behavior,
    }
    labels = {
        "compounded_impossibility_early": "taboo-family premise is not compounded and legible in the opening",
        "audience_has_superior_knowledge": "story relies on surprise instead of giving the audience superior knowledge",
        "protective_misdirector_active": "no active friend/family protector misdirects and intensifies the secret",
        "social_arena_rotation": "relationship power is not tested across enough distinct social arenas",
        "public_shame_or_class_wound": "wealth/status fantasy lacks a concrete public shame or class wound",
        "power_acquires_rules_or_accountability": "protective power remains consequence-free force rather than acquiring rules or accountability",
        "protagonist_can_reject_power": "protagonist cannot meaningfully reject the powerful partner after truth exposure",
        "possessiveness_is_flaw_not_reward": "coercive/possessive behavior is present without being named, bounded, or repaired",
        "family_reclassification_hook": "ending does not convert romance revelation into a family-order reclassification hook",
        "truth_and_consent_repair": "original deception/coercion lacks explicit truth plus consent/boundary/agency repair",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Forbidden-family romance works through audience-superior dramatic irony, protective misdirection, rotating social arenas, and family reclassification; coercion and possessiveness must become repaired flaws, never proof of love.",
    }
