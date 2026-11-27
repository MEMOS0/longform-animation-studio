"""Adversarial co-parent incognito integrity checks.

Derived from Celine Drama TV hit/low evidence. These are creative warning
heuristics, not performance predictors. The pattern applies when romantic or
family intimacy forms while both partners hide adversarial institutional
identities behind ordinary work, especially where children or dependents
catalyze the bond.
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


def _pos(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return match.start() if match else None


def _affirmative(pattern: str, text: str) -> bool:
    for segment in re.split(r"[.!?\n]", text):
        if re.search(pattern, segment) and not re.search(r"no one|never|not |without|fails? to|doesn['’]?t|don['’]?t", segment):
            return True
    return False


def evaluate_adversarial_coparent_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    narrative = "\n".join([_text(architecture), _text(scenes)]).lower()
    full = "\n".join([_text(premise), narrative]).lower()

    law_enforcement = bool(re.search(r"fbi|police|detective|investigator|agent|undercover cop|special agent", full))
    criminal_power = bool(re.search(r"mafia|mob|crime family|godfather|cartel|assassin|criminal empire|underworld", full))
    romance_family = bool(re.search(r"husband|wife|married|marriage|romance|fall(?:ing)? in love|family", full))
    dependent = bool(re.search(r"child|children|kid|son|daughter|dependent|apprentice|student", full))
    cover_terms = len(set(re.findall(r"security guard|debt collector|driver|assistant|ordinary (?:guy|man|woman|job)|night shift|regular job|bodyguard|nanny|maid", full)))
    if not (law_enforcement and criminal_power and romance_family and dependent and cover_terms):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    reveal_pos = _pos(r"identity reveal|real identity|who you actually married|i['’]?m (?:with )?(?:the )?(?:fbi|mafia)|truth comes out", narrative)
    if reveal_pos is None:
        reveal_pos = 10**9
    early_text = narrative[:reveal_pos]

    checks = {
        "dual_cover_is_ordinary_labor": cover_terms >= 2 or bool(re.search(r"ordinary (?:guy|man|woman|job)", full)),
        "children_catalyze_but_do_not_own_adult_choice": bool(re.search(r"child\w*|son|daughter", full)) and _affirmative(r"free will|own choices?|adult decision|children only introduced|only introduced us", full),
        "material_care_precedes_status_reward": bool(re.search(r"steady (?:pay|job)|dinner|bedtime stor|rent|bills|shared (?:cost|home)|toys|school|meal|not baggage", early_text)),
        "adversarial_institutions_create_real_stakes": law_enforcement and criminal_power and bool(re.search(r"hunt\w*|investigat\w*|target\w*|arrest|surveillance|expose\w*|enemy|rival", full)),
        "concealment_creates_named_epistemic_debt": bool(re.search(r"deciding when to tell|how much else did you decide|no more secrets|making decisions on each other['’]?s behalf|full disclosure|information asymmetry|couldn['’]?t tell|hide things forever", full)),
        "evidence_is_procedural_multi_source": sum(bool(re.search(pattern, full)) for pattern in [r"ledger|personnel record", r"security footage|surveillance", r"witness statement", r"financial record", r"communication", r"confession.*tape|recorded confession"]) >= 2,
        "climax_converts_no_more_secrets_into_joint_behavior": bool(re.search(r"no more secrets", full) and re.search(r"together|backup|tactical team|joint|share (?:the )?(?:video|evidence|information)|we figure it out", full)),
        "children_are_not_secret_keepers_or_family_glue": bool(re.search(r"children carry our secrets|make them cover|grown-up problems are for grown-ups|settle it ourselves|not make.*keep secrets|did nothing wrong", full)),
        "ending_is_informed_adult_rechoice": bool(re.search(r"choose me again|proper proposal|second wedding|this time.*choice|full identity|respect (?:her|his|their) choices|always be honest|marry.*free will", full[-5000:])),
        "institutional_accountability_survives_romance": bool(re.search(r"conflict of interest|handover|other agents|investigation|arrest|secured.*records|cleared review|not innocent", full[-6000:])),
    }
    labels = {
        "dual_cover_is_ordinary_labor": "one or both adversarial leads use status/wealth/power openly instead of ordinary-labor cover that can be tested relationally",
        "children_catalyze_but_do_not_own_adult_choice": "children or dependents appear to force romantic consent rather than merely catalyzing a choice adults explicitly own",
        "material_care_precedes_status_reward": "bond forms through status revelation or spending before concrete labor/domestic care proves who the lovers are without power",
        "adversarial_institutions_create_real_stakes": "hidden identities are cosmetic because the institutions cannot genuinely investigate, expose, or endanger each other",
        "concealment_creates_named_epistemic_debt": "lying is treated as a generic secret rather than control over the information under which the other person chose intimacy",
        "evidence_is_procedural_multi_source": "institutional guilt/innocence is settled by assertion or romance rather than multiple procedural evidence sources",
        "climax_converts_no_more_secrets_into_joint_behavior": "the climax repeats solo heroics or hidden rescue instead of visibly converting no-more-secrets into shared operational behavior",
        "children_are_not_secret_keepers_or_family_glue": "children carry adult secrets, blame, or emotional responsibility instead of being released from adult conflict",
        "ending_is_informed_adult_rechoice": "the first marriage/romance simply continues instead of being consciously re-chosen after full identity disclosure",
        "institutional_accountability_survives_romance": "romantic reconciliation erases investigation, conflict-of-interest handling, or accountability for institutional harm",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Adversarial co-parent incognito works when ordinary-labor cover is tested through material care, children catalyze without owning adult consent, institutional conflict is real, concealment becomes named epistemic debt, post-reveal trust turns procedural and joint, children stop carrying secrets, and the ending is an informed adult re-choice that preserves accountability.",
    }
