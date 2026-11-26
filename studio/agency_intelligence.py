"""Protagonist-agency and competence-inversion checks.

Evidence-informed correction from transformation/wealth breakouts: suffering and
rescue alone are weaker than a wounded protagonist who actively tests, chooses,
builds, protects, or converts hidden competence into public authority.
"""
from __future__ import annotations

from typing import Any

AGENCY_TERMS = ["choose", "chooses", "chose", "decide", "designs", "test", "refuse", "cut", "protect", "offers", "plan", "build", "lead", "risks", "destroys", "rescues", "gives up", "returns", "teaches", "funds", "creates"]
COMPETENCE_TERMS = ["technical", "professional", "combat", "assassin", "research", "invention", "strategy", "medicine", "engineering", "beastkeeper", "knowledge", "skill", "competence", "authority", "cto", "architect", "leader", "expert"]
PASSIVE_TERMS = ["abandoned", "rejected", "humiliated", "bullied", "orphan", "poor", "ugly", "victim", "mocked", "betrayed", "captive"]
RESCUE_TERMS = ["rescued", "saved", "protected", "chosen", "married", "billionaire", "ceo", "king", "dragon", "guardian"]
CIRCULAR_PAYOFF_TERMS = ["gives back", "protects others", "funds", "mentors", "open-source", "open source", "home", "children", "community", "villagers", "restores", "belonging"]


def flatten_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten_text(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(flatten_text(v) for v in value)
    return str(value)


def evaluate_agency(premise: dict[str, Any], scenes: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    premise_text = flatten_text(premise).lower()
    scene_text = flatten_text(scenes or []).lower()
    text = premise_text + " " + scene_text
    early_text = flatten_text(premise.get("opening_event", {})).lower() + " " + flatten_text((scenes or [])[:2]).lower()
    counts = {
        "agency_actions": sum(term in text for term in AGENCY_TERMS),
        "competence_markers": sum(term in text for term in COMPETENCE_TERMS),
        "passive_wound_markers": sum(term in premise_text for term in PASSIVE_TERMS),
        "rescue_markers": sum(term in text for term in RESCUE_TERMS),
        "circular_payoff_markers": sum(term in text for term in CIRCULAR_PAYOFF_TERMS),
        "early_agency_actions": sum(term in early_text for term in AGENCY_TERMS),
    }
    warnings: list[str] = []
    strengths: list[str] = []
    if counts["agency_actions"] >= 3:
        strengths.append("protagonist has repeated visible choices/actions rather than only suffering")
    else:
        warnings.append("protagonist agency is thin; add an active test, plan, refusal, protection choice, or competence inversion")
    if counts["early_agency_actions"] >= 1:
        strengths.append("agency appears in the opening conversion zone")
    else:
        warnings.append("opening does not yet show protagonist agency; wound/rescue may play passive")
    if counts["competence_markers"] >= 1:
        strengths.append("competence/professional capability can become public authority")
    elif counts["rescue_markers"] >= 2:
        warnings.append("rescue/protection fantasy lacks a clear protagonist competence that can become public authority")
    if counts["circular_payoff_markers"] >= 1:
        strengths.append("payoff can become circular generosity/community restoration rather than private victory only")
    else:
        warnings.append("ending lacks circular payoff; consider protagonist using gained power to protect or restore a vulnerable community")
    score = 0.2
    score += 0.2 if counts["agency_actions"] >= 3 else 0
    score += 0.2 if counts["early_agency_actions"] >= 1 else 0
    score += 0.2 if counts["competence_markers"] >= 1 else 0
    score += 0.2 if counts["circular_payoff_markers"] >= 1 else 0
    return {"score_0_to_1": round(score, 2), "counts": counts, "strengths": strengths, "warnings": warnings, "evidence_basis": "Nana child-designed social test, Reborn Assassin competence transplantation, AI Sweet professional authority/circular generosity, Stormglass protective choices"}
