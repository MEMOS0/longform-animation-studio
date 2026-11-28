"""Dual-incognito workplace accountability integrity checks.

Derived from CineAI Grand Crescent evidence. These heuristics are creative
warnings for contemporary institutional melodrama, not performance predictors.
They distinguish labor-as-truth-access and consent-aware status concealment
from generic billionaire hidden-identity spectacle.
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


def _first(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return match.start() if match else None


def evaluate_dual_incognito_workplace_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    narrative = "\n".join([_text(architecture), _text(scenes)]).lower()
    full = "\n".join([_text(premise), narrative]).lower()

    workplace = bool(re.search(r"\b(?:hotel|restaurant|hospital|factor(?:y|ies)|compan(?:y|ies)|office|shop|stores?|staff|employees?|workers?|managers?|payroll|workplace)\b", full))
    hidden_power = bool(re.search(r"secret(?:ly)? (?:a )?(?:owner|billionaire|heir|heiress|ceo|executive)|hidden (?:owner|identity|wealth|status)|incognito|ordinary staff position|conceals? (?:her|his|their) (?:identity|wealth|status)", full))
    stripped_power = bool(re.search(r"lost everything|fired|removed as ceo|deposed|framed|stripped of|false(?:ly)? accused|suspended|bankrupt", full))
    labor_entry = bool(re.search(r"takes? (?:a )?(?:job|position)|applies?|\bordinary staff\b|\bassistant\b|\bcleaner\b|\bserver\b|\bworkers?\b|\bemployees?\b|\buniforms?\b|\bshifts?\b|\blabor\b", full))
    if not (workplace and labor_entry and (hidden_power or stripped_power)):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    dignity_pos = _first(r"don['’]?t humiliate|supervise\.?\s*don['’]?t humiliate|defends? .*humiliat|protects? .*dignity|stops? .*humiliat|refuses? to shame", narrative)
    intimacy_pos = _first(r"kiss(?:es|ed)?|falling in love|fall in love|romance|date|proposal|marries|marry", narrative)
    care_tokens = [
        bool(re.search(r"cake|birthday|meal|food|dessert|umbrella", narrative)),
        bool(re.search(r"injur|bleeding|bandag|treats? (?:his|her|their) hand|medical", narrative)),
        bool(re.search(r"schedule|overtime|payroll|wages?|shift|hours", narrative)),
        bool(re.search(r"complaint|afraid to speak|afraid to tell|worker safety|staff safety", narrative)),
    ]
    evidence_patterns = {
        "banking": r"bank confirmation",
        "vendor_registration": r"vendor registration",
        "maintenance": r"maintenance log|maintenance record",
        "access_control": r"access code",
        "visual_or_audio_record": r"security footage|recording",
        "testimony": r"guest testimony|witness testimony|witness statement",
        "public_correction": r"written apology|public correction",
        "payroll_or_timekeeping": r"payroll|overtime sheet",
        "financial_document": r"invoice|receipt",
        "audit_or_ledger": r"audit|ledger|original documents?|supporting documents?|written records?",
    }
    evidence_sources = sum(bool(re.search(pattern, narrative)) for pattern in evidence_patterns.values())
    transparency_terms = bool(re.search(r"transparent records|employee access|worker protection|scheduling (?:tool|system)|payroll (?:tool|system)|open records|workers? can (?:see|inspect|verify)|transparency infrastructure", narrative))

    checks = {
        "hidden_authority_enters_same_labor": hidden_power and bool(re.search(r"ordinary staff|same labor|worker|employee|assistant|uniform|shift|job|floor", full)),
        "stripped_protagonist_proves_labor_competence": stripped_power and bool(re.search(r"do(?:es)? it properly|competent|learns? the work|repairs?|serves?|cleans?|works? (?:the )?(?:shift|floor)|earns? respect", full)),
        "anti_humiliation_precedes_intimacy": dignity_pos is not None and (intimacy_pos is None or dignity_pos < intimacy_pos),
        "community_care_is_repeated_and_material": sum(care_tokens) >= 2,
        "evidence_is_procedural_and_multi_source": evidence_sources >= 3,
        "concealment_creates_named_consent_debt": bool(re.search(r"made that decision for both|wrong to hide|should have told|kept .*outside the truth|information asymmetry|without .*informed choice|right to know", full)),
        "reconciliation_preserves_time_and_choice": bool(re.search(r"needs? time|take(?:s)? time|space|without demanding forgiveness|doesn['’]?t demand forgiveness|free to choose|choice", full)),
        "career_restoration_is_not_romantic_patronage": bool(re.search(r"same terms|independent committee|merit|on the merits|refuses? (?:a )?(?:senior role|position|job)|builds? independently|not because (?:of )?(?:dating|romance)|no favoritism", full)),
        "harm_becomes_worker_facing_transparency_infrastructure": transparency_terms,
        "ending_establishes_shared_truth_rule": bool(re.search(r"no more secrets|secrets that belong to both|honest about|truth.*(?:both|together)|same information|full disclosure", full[-3000:])),
    }
    labels = {
        "hidden_authority_enters_same_labor": "hidden institutional authority inspects from a distance instead of entering the same labor system it needs to understand",
        "stripped_protagonist_proves_labor_competence": "stripped/deposed protagonist is restored by status before proving respect and competence inside ordinary labor",
        "anti_humiliation_precedes_intimacy": "romance begins before dignity protection/anti-humiliation establishes the bond's moral basis",
        "community_care_is_repeated_and_material": "workplace community is decorative; care is not repeated through concrete material acts",
        "evidence_is_procedural_and_multi_source": "corruption is exposed through a single convenient clue rather than procedural multi-source evidence",
        "concealment_creates_named_consent_debt": "hidden identity/wealth is treated as a reward without naming information-asymmetry consent debt",
        "reconciliation_preserves_time_and_choice": "reconciliation demands instant forgiveness instead of preserving time, space, and choice",
        "career_restoration_is_not_romantic_patronage": "professional restoration depends on romantic patronage rather than merit, independence, or transparent review",
        "harm_becomes_worker_facing_transparency_infrastructure": "villain punishment substitutes for converting the harm into worker-facing transparency or protection infrastructure",
        "ending_establishes_shared_truth_rule": "ending does not close the central concealment wound with a concrete shared truth/disclosure rule",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Dual-incognito workplace melodrama works when labor exposes institutional truth, dignity precedes intimacy, concealment creates repairable consent debt, evidence is procedural, and restoration preserves independence while converting harm into transparent worker protection.",
    }
