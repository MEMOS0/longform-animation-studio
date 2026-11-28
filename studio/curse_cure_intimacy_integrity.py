"""Cursed-touch cure/caregiver romance integrity checks.

Derived from Vintage Verse hit/medium/low evidence. Transparent creative
warnings, not performance prediction. Applies when romance develops around a
dangerous magical touch, transformation, or curse that one person can soothe.
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
    return [part.strip() for part in re.split(r"[.!?\n]", text) if part.strip()]


def _affirmative(pattern: str, text: str) -> bool:
    negation = re.compile(r"\b(?:never|not|no longer|without|fails? to|doesn['’]?t|didn['’]?t|don['’]?t)\b")
    return any(re.search(pattern, part) and not negation.search(part) for part in _segments(text))


def _has_nonconsensual_intimacy(text: str) -> bool:
    patterns = (
        r"(?:kiss(?:es|ed)?|touch(?:es|ed)?|takes?|forces?|presses?).{0,40}without (?:asking|permission|consent)",
        r"without (?:asking|permission|consent).{0,15}(?:kiss|touch|force|bed|sex)",
        r"never asks? permission before (?:kissing|touching)",
        r"(?:kiss|touch).{0,60}never asks? permission|never asks? permission.{0,60}(?:kiss|touch)",
        r"no consent",
    )
    refusal = re.compile(r"refus|avoid|stop|prevent|won['’]?t|wouldn['’]?t|not allowed|must not")
    for sentence in _segments(text):
        for pattern in patterns:
            for match in re.finditer(pattern, sentence):
                before = sentence[max(0, match.start() - 35):match.start()]
                if not refusal.search(before):
                    return True
    return False


def evaluate_curse_cure_intimacy_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    curse = bool(re.search(r"curse|cursed|burns? at .*touch|petrif|turn to stone|lose control|rampage|shift|venom|touch (?:kills|burns|hurts)|dangerous touch", full))
    creature_or_royal = bool(re.search(r"dragon|medusa|werewolf|wolf|beast|monster|serpent|snakes?|king|prince|queen|royal|alpha", full))
    intimacy = bool(re.search(r"romance|romantic|lover|boyfriend|girlfriend|wife|husband|bride|kiss|caregiver|massage|mate|marri|wedding|falls? in love|in love", full))
    if not (curse and creature_or_royal and intimacy):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    opening = full[:max(1, len(full) // 4)]
    ending_units = scenes[-max(1, min(3, len(scenes))):] if scenes else []
    if isinstance(architecture, dict):
        for key in ("ending", "ending_payoff", "resolution", "final_act"):
            if key in architecture:
                ending_units.append(architecture[key])
        if not scenes and isinstance(architecture.get("sequences"), list) and architecture.get("sequences"):
            ending_units.extend(architecture["sequences"][-max(1, min(2, len(architecture["sequences"]))):])
    ending = (_text(ending_units) or full[-max(1, len(full) // 3):]).lower()

    checks = {
        "dangerous_touch_has_rules_and_cost": bool(re.search(r"no one can (?:get near|touch)|burns? at .*touch|can't control|cannot control|hurt you|petrif|turn .* stone|die from the curse|curse.{0,60}(?:six months|death|kill|cost)|dangerous", full)),
        "cure_person_has_independent_need_or_identity": bool(re.search(r"mother|mom|mum|family|money|salary|job|profession|studio|archives|identity|who i really am|necklace|rent|contract|home", opening)),
        "intimacy_progresses_by_consent_and_pacing": bool(re.search(r"no rush|wait until|not ready|don't be afraid|permission|choice|you choose|your choice|ask|consent|ready|stop", full) and not _has_nonconsensual_intimacy(full)),
        "control_or_cure_is_procedural_not_instant": bool(re.search(r"one breath|again|training|test|verification|medicine|control the shift|practice|results|witness|restore|ritual|seal|learn|procedur|treatment", full)),
        "instrumental_origin_is_confessed_or_revised": bool(re.search(r"using me|just .*cure|that's how it started|different now|truth|confess|not just|real|liar|contract", full)),
        "antagonist_weaponizes_curse_or_intimacy": bool(re.search(r"spread.*lies|drive you apart|tamper|poison|amplify the curse|lure .* away|trap|compel|control source|false oracle|curse.*weapon|use.*curse|forced my hand", full)),
        "love_is_proven_when_utility_is_questioned": bool(re.search(r"risk .*life|die for|protect|save|not just .*cure|if .*cure.*why|still needs|face it together|when i won't be there|i love|choice", full)),
        "caregiver_or_cure_retains_agency_after_intimacy": bool(re.search(r"queen|rule|host|archives|investigate|verify|decide|studio|own .*business|work|job|choice|i choose|leave|stay", full)),
        "ending_restores_autonomy_or_shared_life_beyond_curse": _affirmative(r"home|family|baby|child|married|choose|stay|free|own .*studio|together|rule|livelihood|mother", ending),
    }
    labels = {
        "dangerous_touch_has_rules_and_cost": "the dangerous touch/curse lacks a clear rule, cost, deadline, or bodily risk",
        "cure_person_has_independent_need_or_identity": "the cure/caregiver exists only as the magical solution, without family, money, work, identity, or independent motive",
        "intimacy_progresses_by_consent_and_pacing": "physical intimacy is instant or pressured instead of paced through readiness, permission, stop/choice, or consent",
        "control_or_cure_is_procedural_not_instant": "the cure/control works by instant touch rather than breath, training, verification, ritual, medicine, or repeatable procedure",
        "instrumental_origin_is_confessed_or_revised": "the story never confronts that the beloved began as a cure, contract, tool, or transaction",
        "antagonist_weaponizes_curse_or_intimacy": "the antagonist does not exploit the curse, touch rules, medicine, rumors, or intimacy as a weapon",
        "love_is_proven_when_utility_is_questioned": "love is not tested when the cure becomes useless, dangerous, false, or no longer necessary",
        "caregiver_or_cure_retains_agency_after_intimacy": "the caregiver/cure loses independent agency once romance begins",
        "ending_restores_autonomy_or_shared_life_beyond_curse": "the ending merely removes the curse without building autonomy, livelihood, family, home, or chosen shared life",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Cursed-touch cure romance works when the curse has rules and cost, the cure person has independent need or identity, intimacy is paced through consent, control is procedural rather than instant, instrumental origins are confessed and revised, antagonists weaponize curse or intimacy, love survives loss of utility, and the ending builds autonomous shared life beyond the curse.",
    }
