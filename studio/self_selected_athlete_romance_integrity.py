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
    sport = bool(re.search(r"basketball|gymnast(?:ics)?|athlete|athletic|sport|team captain|tournament|beam routine|floor routine|dance|ballet|audition|esports|martial arts|track and field|swimming|soccer|football|tennis", full))
    romance = bool(re.search(r"romance|boyfriend|girlfriend|ex\b|lover|kiss|marry|relationship|captain.*(?:love|romance)|love|cheerleader|gets? the girl", full))
    if not (sport and romance):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    opening = full[:max(1, len(full) // 4)]
    ending_units = []
    if scenes:
        ending_units.extend(scenes[-max(1, min(5, (len(scenes) + 2) // 3)):])
    elif isinstance(architecture, dict):
        for key in ("ending", "ending_payoff", "resolution", "final_act"):
            if key in architecture:
                ending_units.append(architecture[key])
        if isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
            ending_units.extend(architecture["sequences"][-max(1, min(3, (len(architecture["sequences"]) + 2) // 3)):])
    ending = (_text(ending_units) or full[-max(1, len(full) // 3):]).lower()
    penalty_erased = bool(re.search(r"erases? (?:the )?(?:report|suspension|penalty|consequence)|(?:report|suspension|penalty|consequence).{0,60}(?:erased|dropped|forgotten|cleared)", full))
    instant_recovery = bool(re.search(r"heals? overnight|instantly healed|miraculously recovered|fully recovered the next day|no recovery time", full))
    ambition_abandoned = bool(re.search(r"abandons? (?:her |his |their )?career for (?:love|romance)|gives? up (?:her |his |their )?(?:career|competition|dream) for (?:love|romance)", full))
    checks = {
        "public_humiliation_becomes_immediate_boundary": bool(re.search(r"humiliat|embarrass|push|slap|mock|bully|betray", opening) and re.search(r"breakup|break up|we're done|leave|refuse|boundary|get out|not yours|stop", opening)),
        "romantic_choice_is_not_a_trophy_or_bet": bool(re.search(r"don't get to bet|do not get to bet|not a prize|already chosen|she chose|he chose|i choose|you don't get a vote|can't win me|not yours", full)),
        "competence_is_procedural_and_visible": bool(re.search(r"tryout|training|practice|coach|score|trial|competition|routine|landing|selection|showcase|medical clearance", full)),
        "sabotage_or_injury_has_institutional_consequence": bool(re.search(r"incident report|suspension|suspended|signed statement|medical staff|investigation|disqualified|report stays|evidence|rules", full)),
        "ambition_is_not_sacrificed_for_romance": bool((not ambition_abandoned) and re.search(r"both|career|competition|showcase|camp|rehab|training|own ambition|i want this chance|don't skip|not his excuse|picked me|choose myself", full)),
        "injury_or_comeback_has_physical_cost": bool((not instant_recovery) and re.search(r"sprain|fracture|scan|rehab|medical clearance|eight weeks|recovery|surgery|can't lift|physical cost|injur.{0,80}(?:scan|rehab|clearance|weeks|recovery|surgery)", full)),
        "partner_supports_without_control": bool(re.search(r"support|watching|help|listen|ask|respect|not keeping me|not his excuse|won't be his excuse|let her|you choose|your choice|i'll wait", full)),
        "rival_accountability_does_not_erase_consequence": bool((not penalty_erased) and (re.search(r"report stays|suspension stands|leaving the team|consequences? (?:remain|stand|stay)|signed statement", full) or (re.search(r"apolog|confess|admit", full) and re.search(r"report|suspension|consequence|penalty", full)))),
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
