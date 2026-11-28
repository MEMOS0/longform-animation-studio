"""Animal-communication zoo/institution revival integrity checks.

Derived from King's Theater and KellyCine hit evidence plus the adjacent
King's Theater low counterexample. Transparent creative warnings, not
performance prediction.
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


def evaluate_animal_communication_zoo_revival_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    animal_talk = bool(re.search(r"understands? animals?|talks? to animals?|hear animals?|animals? talk|animal language|communicate with animals?", full))
    institution = bool(re.search(r"zoo|wildlife park|animal park|sanctuary|aquarium|shelter|circus|vet|veterinary", full))
    revival = bool(re.search(r"failing|dying|save|revive|revival|debt|bankrupt|viral|visitors?|investment|business|ticket|customers?", full))
    if not (animal_talk and institution and revival):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    opening = full[:max(1, len(full) // 4)]
    ending_units = scenes[-max(1, min(4, len(scenes))):] if scenes else []
    if isinstance(architecture, dict):
        for key in ("ending", "ending_payoff", "resolution", "final_act"):
            if key in architecture:
                ending_units.append(architecture[key])
        if not scenes and isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
            ending_units.extend(architecture["sequences"][-max(1, min(3, len(architecture["sequences"]))):])
    ending = (_text(ending_units) or full[-max(1, len(full) // 3):]).lower()

    checks = {
        "institutional_crisis_is_concrete_before_the_gift": bool(re.search(r"debt|overdue bills|cut off|water and power|failing|dying|can't afford|50,?000|bankrupt|infrastructure|feed mill|vet supply|closure", opening)),
        "animal_speech_reveals_specific_needs_or_preferences": bool(re.search(r"itch|scratch|hungry|food|depressed|sulking|famous|sunlight|pool|lawn|doesn't want|wants? to|afraid|hurt|stuck|trouble|misses|lonely|prefer", full)),
        "animals_have_distinct_personalities_not_generic_minions": bool(re.search(r"monkey|tiger|kangaroo|elephant|parrot|bird|gorilla|panda|croc|wolf|hen|animal .*act|star power|troublemaker|fighter|performer", full)),
        "communication_solves_behavior_through_understanding_not_domination": bool(re.search(r"why|real problem|cause|understand|listen|ask|favor|prefer|choice|doesn't want|if you don't want|coax|calm|trust", full)),
        "animal_autonomy_and_refusal_are_explicit": bool(re.search(r"if .*doesn't want|don't force|entirely up to|can stop|refuse|won't perform|choice|behave|i won't touch|not forcing|no schedule", full)),
        "economic_revival_is_procedural": bool(re.search(r"ticket|tourist|visitor|viral|video|media planner|investment|reservation|advertising|revenue|sales?|contract|exchange|sponsor|customers?", full)),
        "rescue_or_care_competence_precedes_spectacle": bool(re.search(r"rescue|health exam|medical|vet|transport assessment|snacks|keep .*calm|scratch|stuck|hurt|safety|care", full)),
        "animal_safety_protocols_limit_showmanship": bool(re.search(r"double.?fenc|safety|no bait|outer warehouse|limit visitors|security|surveillance|don't force|do not bang|barrier|won't lose a single hair|not approved", full)),
        "institutional_antagonist_uses_sabotage_or_exploitation": bool(re.search(r"sabotage|culprit|suspect|block.*road|plot|competitor|too good|steal|fake contract|threat|trap|poison|cut off|hostile", full)),
        "ending_restores_institution_and_animal_wellbeing": bool(re.search(r"saved|visitors?|investment|viral|safe|healthy|happy|enjoying|pool|home|reopen|reservations?|thriv|protect|succeed|contract", ending)),
    }
    labels = {
        "institutional_crisis_is_concrete_before_the_gift": "the zoo/park is not already failing through debts, utilities, infrastructure, animal feed, medical costs, or closure pressure before the gift appears",
        "animal_speech_reveals_specific_needs_or_preferences": "animal dialogue is generic comic noise rather than specific itch, hunger, fear, dignity, fame, sunlight, pool, injury, loneliness, or preference information",
        "animals_have_distinct_personalities_not_generic_minions": "animals are interchangeable helpers rather than differentiated species/characters with moods, acts, vanities, fears, and social relationships",
        "communication_solves_behavior_through_understanding_not_domination": "the protagonist uses animals as labor or spectacle without translating the cause of behavior into care, trust, negotiation, or environmental change",
        "animal_autonomy_and_refusal_are_explicit": "animal performance lacks refusal rights, choice, no-force rules, or consent-like boundaries",
        "economic_revival_is_procedural": "the zoo recovers by declaration rather than tickets, visitors, viral video, media, sponsorship, reservations, contracts, or investment mechanics",
        "rescue_or_care_competence_precedes_spectacle": "the story monetizes animal novelty before demonstrating rescue, health assessment, feeding, calming, transport, or care competence",
        "animal_safety_protocols_limit_showmanship": "viral spectacle and sabotage plots lack barriers, double-fencing, visitor limits, surveillance, no-bait rules, or welfare constraints",
        "institutional_antagonist_uses_sabotage_or_exploitation": "the opposition is vague rather than competitor sabotage, exploitative exchange, roadblocks, fake contracts, supply interference, or institutional pressure",
        "ending_restores_institution_and_animal_wellbeing": "the ending restores business viability without also restoring animal safety, health, choice, home, or wellbeing",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Animal-communication zoo revival works when a concrete institutional crisis precedes the gift, animal speech exposes specific needs and personalities, behavior is solved through understanding rather than domination, animals retain refusal/autonomy, care and safety precede spectacle, recovery is procedurally monetized through visitors/media/investment/contracts, antagonists attack the institution through sabotage or exploitation, and the ending restores both institutional viability and animal wellbeing.",
    }
