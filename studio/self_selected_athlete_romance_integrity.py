"""Self-selected athlete/performance romance integrity checks.

Derived from ElowenTale hit/medium/low evidence. Transparent creative warnings,
not performance prediction.
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


def evaluate_self_selected_athlete_romance_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    sport = bool(re.search(r"basketball|gymnast(?:ics)?|athlete|athletic|sport|team captain|competition|tournament|vault|beam|floor routine|score|coach", full))
    romance = bool(re.search(r"romance|boyfriend|girlfriend|ex\b|lover|kiss|marry|relationship|captain.*(?:love|romance)|love|cheerleader|gets? the girl", full))
    if not (sport and romance):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    opening = full[:max(1, len(full) // 4)]
    ending = full[-max(1, len(full) // 3):]
    checks = {
        "public_humiliation_becomes_immediate_boundary": bool(re.search(r"humiliat|embarrass|push|slap|mock|bully|betray", opening) and re.search(r"breakup|break up|we're done|leave|refuse|boundary|get out|not yours|stop", opening)),
        "romantic_choice_is_not_a_trophy_or_bet": bool(re.search(r"don't get to bet|do not get to bet|not a prize|already chosen|she chose|he chose|i choose|you don't get a vote|can't win me|not yours", full)),
        "competence_is_procedural_and_visible": bool(re.search(r"tryout|training|practice|coach|score|trial|competition|routine|landing|selection|showcase|medical clearance", full)),
        "sabotage_or_injury_has_institutional_consequence": bool(re.search(r"incident report|suspension|suspended|signed statement|medical staff|investigation|disqualified|report stays|evidence|rules", full)),
        "ambition_is_not_sacrificed_for_romance": bool(re.search(r"both|career|competition|showcase|camp|rehab|training|own ambition|i want this chance|don't skip|not his excuse|picked me|choose myself", full)),
        "injury_or_comeback_has_physical_cost": bool(re.search(r"injur|sprain|fracture|scan|rehab|medical clearance|eight weeks|recovery|surgery|can't lift|physical cost", full)),
        "partner_supports_without_control": bool(re.search(r"support|watching|help|listen|ask|respect|not keeping me|not his excuse|won't be his excuse|let her|you choose|your choice|i'll wait", full)),
        "rival_accountability_does_not_erase_consequence": bool(re.search(r"apolog|confess|admit|signed statement|report stays|leaving the team|suspension stands|consequence", full)),
        "climax_is_decided_by_visible_skill": bool(re.search(r"score|landing|routine|podium|trial|competition|first place|win|winning|performance", ending)),
        "ending_self_selection_precedes_or_frames_romance": bool(re.search(r"picked me|choose myself|chose myself|my own|i won|earned|not given|you can keep up|partner|together", ending)),
    }
    labels = {
        "public_humiliation_becomes_immediate_boundary": "opening humiliation does not become an immediate boundary or changed relational terms",
        "romantic_choice_is_not_a_trophy_or_bet": "the romance can be won, bet on, or possessed rather than remaining a present-tense choice",
        "competence_is_procedural_and_visible": "athletic/performance competence is asserted rather than procedurally trained, scored, reviewed, or selected",
        "sabotage_or_injury_has_institutional_consequence": "sabotage or injury lacks reports, medical review, suspension, evidence, or institutional consequence",
        "ambition_is_not_sacrificed_for_romance": "one person's ambition is treated as something to sacrifice for romance rather than a parallel stake",
        "injury_or_comeback_has_physical_cost": "injury or comeback lacks scans, rehabilitation, clearance, time, or physical cost",
        "partner_supports_without_control": "the partner controls, excuses, or rescues instead of supporting agency and choice",
        "rival_accountability_does_not_erase_consequence": "rival apology/confession erases consequences instead of coexisting with reports, suspension, or loss",
        "climax_is_decided_by_visible_skill": "the climax is social explanation rather than visible scored skill/performance",
        "ending_self_selection_precedes_or_frames_romance": "the ending rewards romance without first confirming self-selection, earned competence, or mutual independence",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Athlete/performance romance works when public humiliation creates immediate boundaries, romantic choice is never a trophy or bet, competence is visibly procedural, sabotage and injury carry institutional/medical costs, ambition is not sacrificed for love, partners support without control, rival accountability preserves consequences, and the climax is won through visible skill before self-selected romance.",
    }
