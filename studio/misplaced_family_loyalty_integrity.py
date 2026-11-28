"""Misplaced family-loyalty integrity checks.

Derived from PrimeFate hit/medium/low evidence. Transparent creative warnings,
not performance predictions. Applies when a family rewards a manipulative or
status-performing insider while rejecting the real contributor/kin.
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


def evaluate_misplaced_family_loyalty_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    family = bool(re.search(r"family|father|mother|sister|brother|\bson\b|daughter|\bheir\b|in-law|household", full))
    rejection = bool(re.search(r"cast out|disown|reject|exile|threw out|walks? away|leave|left|frame|accus|betray|dumped|family[^\n.]{0,30}abandon(?:ed|s|ing)?[^\n.]{0,15}(?:him|her|them|their son|their daughter|their child|the protagonist|their relative)|abandoned by (?:his|her|their) family", full))
    misallocated = bool(re.search(r"fake heir|impostor|favorite|favoritism|all their love|outsider|son-in-law|beloved|manipulat|credul|believes? (?:his|her|their) lies", full))
    if not (family and rejection and misallocated):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    architecture_text = _text(architecture).lower()
    final_scene_text = _text(scenes[-1]).lower() if scenes else ""
    ending_text = "\n".join([architecture_text[-max(1, len(architecture_text)//3):] if architecture_text else "", final_scene_text]) or full[-max(1, len(full) // 4):]
    ordered = "\n".join([architecture_text, _text(scenes).lower()]).strip() or full
    checks = {
        "rejected_kin_has_visible_care_or_competence_before_exile": bool(
            re.search(r"raised|care|cook|work|project|company|protect|provide|sacrifice|heal|repair|supported|devotion|life's work|wanted to make (?:him|her|them) proud", ordered)
            and re.search(r"cast out|disown|reject|exile|threw out|walks? away|leave|left|frame|accus|betray|dumped", ordered)
            and re.search(r"raised|care|cook|work|project|company|protect|provide|sacrifice|heal|repair|supported|devotion|life's work|wanted to make (?:him|her|them) proud", ordered).start()
            < re.search(r"cast out|disown|reject|exile|threw out|walks? away|leave|left|frame|accus|betray|dumped", ordered).start()
        ),
        "family_favoritism_is_dramatized_through_specific_acts": bool(re.search(
            r"all their love|basement|watch under|framed|selling (?:the )?(?:files|secrets)|stole the drive|believed? (?:his|her|their) lies|one son|play favorites|sensitive|let him have this",
            full,
        )),
        "manipulator_power_depends_on_information_asymmetry": bool(re.search(
            r"fake heir|impostor|lie|lies|frame|secret|hidden|evidence they did not see|they'd still believe me|saw you|with my own eyes|forg|deceiv|manipulat",
            full,
        )),
        "walk_away_or_exile_is_a_decisive_boundary": bool(re.search(
            r"disown|cast out|walks? away|leave|left|never come back|none of my concern|striking your name|i'm leaving|don't want any of you as my family",
            full,
        )),
        "exposure_uses_evidence_or_consequences_not_confession_alone": bool(re.search(
            r"expose|uncover|reveals?|proof|records?|camera|witness|investigation|bankrupt|arrest|prison|audit|public|timeline",
            full,
        )),
        "family_acknowledges_the_specific_misallocation": bool(re.search(
            r"we were so wrong|what if|never believed|shouldn't have treated|i'm sorry|forgive|regret|we can't afford|ruined their chance|your own actions|snobbish",
            full,
        )),
        "consequences_follow_power_money_or_survival_not_only_insults": bool(re.search(
            r"company collaps|bankrupt|prison|investigation|fire|death|debt|stock|lost everything|estate|ruin|survival|commercial mission|ceo",
            full,
        )),
        "ending_preserves_protection_identity_or_moral_choice_beyond_annihilation": bool(re.search(
            r"protect|welcome home|family|choice|choose|never let anyone hurt|goodness|repent|deeds|identity|own name|repair|love",
            ending_text,
        )),
    }
    labels = {
        "rejected_kin_has_visible_care_or_competence_before_exile": "the rejected relative is only declared worthy instead of shown caring, working, healing, protecting, or building before exile",
        "family_favoritism_is_dramatized_through_specific_acts": "family favoritism stays abstract rather than appearing through concrete acts such as framing, unequal care, theft, disbelief, or basement/exile treatment",
        "manipulator_power_depends_on_information_asymmetry": "the manipulator wins by fiat rather than exploiting secrets, forged appearances, selective witness testimony, or family credulity",
        "walk_away_or_exile_is_a_decisive_boundary": "the protagonist remains trapped in argument instead of crossing a decisive disowning, walk-away, or expulsion boundary",
        "exposure_uses_evidence_or_consequences_not_confession_alone": "exposure depends on confession or outrage rather than files, records, witnesses, investigation, bankruptcy, prison, or public consequences",
        "family_acknowledges_the_specific_misallocation": "the family never names the exact favoritism or disbelief that caused the catastrophe",
        "consequences_follow_power_money_or_survival_not_only_insults": "the fallout remains verbal rather than damaging company power, money, freedom, survival, or social position",
        "ending_preserves_protection_identity_or_moral_choice_beyond_annihilation": "the ending is only annihilation/revenge rather than protection, chosen family, identity, repair, or a moral choice",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Misplaced-family-loyalty drama works when the rejected kin's care/competence is visible before exile, favoritism is enacted through concrete asymmetric acts, the manipulator exploits information asymmetry, departure is decisive, exposure uses evidence and material consequences, the family names its exact failure, and the ending leaves protection, identity, repair, or moral choice beyond simple annihilation.",
    }
