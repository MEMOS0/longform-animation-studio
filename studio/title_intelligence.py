"""Evidence-informed title generation and critique.

Titles are packaging artifacts. The system learns mechanisms from market evidence
but must not copy exact high-performing titles or use deceptive duplicate-title
trend-jacking.
"""
from __future__ import annotations

import re
from typing import Any


def flatten_premise_text(premise: dict[str, Any]) -> str:
    parts = [premise.get("logline", ""), premise.get("audience_promise", "")]
    for key in ("emotional_engine", "protagonist", "opening_event", "theme_lane"):
        value = premise.get(key, {})
        if isinstance(value, dict):
            parts.extend(str(v) for v in value.values())
    return " ".join(str(p) for p in parts if p).lower()


def critique_title(title: str, premise: dict[str, Any] | None = None) -> dict[str, Any]:
    low = title.lower()
    strengths: list[str] = []
    risks: list[str] = []
    vulnerable_terms = ["child", "baby", "mother", "father", "daughter", "son", "girl", "boy", "creature", "dragon", "wolf", "mermaid", "orphan", "heir"]
    conflict_terms = ["hunted", "betrayed", "rejected", "mocked", "abandoned", "hidden", "secret", "stole", "kill", "curse", "enemy", "war", "threat", "disgraced"]
    transformation_terms = ["until", "then", "now", "became", "returned", "reborn", "transformed", "revealed", "exposed", "chose"]
    relational_terms = ["mother", "father", "daughter", "son", "family", "keeper", "protector", "bride", "wife", "husband", "lover", "child"]
    if any(term in low for term in vulnerable_terms):
        strengths.append("vulnerable or relational anchor visible")
    else:
        risks.append("no vulnerable/relational anchor visible")
    if any(term in low for term in conflict_terms):
        strengths.append("conflict or injustice legible")
    else:
        risks.append("conflict/injustice not legible")
    if any(term in low for term in transformation_terms):
        strengths.append("turn or transformation promise present")
    else:
        risks.append("no clear turn/transformation promise")
    if any(term in low for term in relational_terms):
        strengths.append("relationship role present")
    if len(title) > 110:
        risks.append("too long for mobile scanning")
    elif len(title) > 80:
        risks.append("long; verify mobile truncation")
    if low.count("…") + low.count("...") > 1:
        risks.append("multiple ellipsis beats may feel cluttered")
    if re.search(r"\b(full movie|4k|episode\s*\d+|part\s*\d+)\b", low):
        risks.append("packaging tokens may crowd story promise unless they are intentionally part of release format")
    if premise:
        text = flatten_premise_text(premise)
        contract = premise.get("channel_contract", "")
        anchor_terms = [term for term in vulnerable_terms if term in text]
        if anchor_terms and not any(term in low for term in anchor_terms[:4]):
            risks.append("title may not expose the premise's clearest vulnerable anchor")
        if contract == "creature_protection_feature" and not any(term in low for term in ["child", "baby", "dragon", "creature", "wolf", "protect", "keeper", "mother"]):
            risks.append("creature-protection contract not readable in title")
    score = 0.42 + 0.12 * len(strengths) - 0.08 * len(risks)
    return {
        "score_0_to_1": max(0.0, min(1.0, score)),
        "strengths": strengths,
        "risks": risks,
        "mobile_length": len(title),
        "ethical_boundary": "Do not reuse another channel's exact hit title or create deceptive duplicate packaging; learn the demand mechanism instead.",
    }


def generate_title_candidates(premise: dict[str, Any]) -> list[dict[str, Any]]:
    engine = premise.get("emotional_engine", {})
    protagonist = premise.get("protagonist", {})
    identity = protagonist.get("identity", "the protagonist")
    wound = engine.get("wound", "a visible wound")
    injustice = engine.get("injustice", "a powerful injustice")
    protector = engine.get("protective_counterforce", "a protector")
    payoff = engine.get("belonging_payoff", "belonging")
    contract = premise.get("channel_contract", "")
    if contract == "creature_protection_feature":
        raw = [
            f"They Hunted the Last Creature Child… Until {identity.split(',')[0]} Chose to Protect It",
            f"The Child Everyone Feared Trusts the Protector Everyone Else Condemned",
            f"A Hunted Creature Child. A Disgraced Protector. One Home They Must Save.",
        ]
    elif contract == "transformation_melodrama":
        raw = [
            "They Taught Her to Hide Her Beauty… Until One Person Saw the Girl Beneath the Shame",
            "The Girl They Mocked Is About to Become the Woman They Cannot Erase",
            "She Was Hidden for Her Own Safety… Then the Truth Made Her Visible",
        ]
    elif contract == "exploration_wonder_feature":
        raw = [
            "She Found a Hidden World Beneath the Roots… Then Became Its Only Giant Protector",
            "The Tiny Kingdom Feared Her Size… Until She Learned How Not to Be Dangerous",
            "A Lost Explorer. A Hidden Kingdom. One Choice That Could Save Them Both.",
        ]
    elif contract == "hostile_survival_spectacle":
        raw = [
            "Her Plane Crashed on an Island Where the Insects Were Waiting",
            "One Survivor. One Impossible Island. No Way Out Before Nightfall.",
            "She Survived the Crash… Then the Island Started Hunting Her",
        ]
    else:
        raw = [
            f"They Created {wound}… Until {protector} Changed Everything",
            f"When {injustice} Threatens Everything, One Choice Leads to {payoff}",
            "A Wound They Cannot Hide. A Protector They Did Not Expect. A Home Worth Fighting For.",
        ]
    return [{"title": title, "critique": critique_title(title, premise)} for title in raw]
