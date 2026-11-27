"""Integrity checks for online-deception, catfish, and fake-dating romance.

Derived from Twistora/QueenFlix evidence. These are creative-review heuristics:
they do not predict performance; they flag ethical and retention risks in
deception-driven romance engines.
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


def evaluate_romance_deception_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    direct_deception = bool(re.search(r"catfish|online (?:boyfriend|girlfriend|dating|romance)|fake dat|pretend(?:ing)? to date", full))
    romantic_hidden_identity = bool(re.search(r"(?:hidden|secret) identity.{0,100}(?:romance|dating|boyfriend|girlfriend|husband|wife|partner|love)|(?:romance|dating|boyfriend|girlfriend|husband|wife|partner|love).{0,100}(?:hidden|secret) identity", full))
    applies = direct_deception or romantic_hidden_identity
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    minor_risk = bool(re.search(r"\b(?:1[1-7]|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|minor|underage|teenager|teen(?:age)?|sixth grader|fifth grade|child)\b", full))
    checks = {
        "immediate_boundary_or_rejection": bool(re.search(r"reject|delete|end(?:s|ed)? the interaction|never meet|not a romance|too young|block(?:s|ed)?(?: him| her)?|cut(?:s)? off contact", full)),
        "exploitation_safeguarding_audit": bool(re.search(r"sexual or inappropriate|inappropriate messages|ask(?:ed)? for money|safeguard|only played games|no romantic|no sexual", full)),
        "adult_accountability_for_minor": bool(re.search(r"parent|mother|father|brother|guardian|discipline|apologiz|phone (?:was )?(?:taken|removed|gone)|handle him|control your", full)),
        "consent_aware_physical_escalation": bool(re.search(r"no kissing|can i kiss|ask(?:s|ed)? (?:before|permission)|let go|boundar|consent|not negotiable", full)),
        "public_answer_pressure_removed": bool(re.search(r"don't have to answer|does not have to answer|do not have to answer|not in public|answer in private|no public pressure|can leave", full)),
        "coercion_named_or_avoided": bool(re.search(r"leverage is wrong|coercion is wrong|coercive|should not have pressured|apologiz(?:e|ed).*pressur|free to refuse|without leverage|no blackmail|refus(?:e|ed|es).*blackmail|reject(?:s|ed)?.*blackmail", full)) or not bool(re.search(r"blackmail|secret .*leverage|wouldn't dare tell|humiliat.*unless|threaten", full)),
        "social_anxiety_accommodation": bool(re.search(r"socially anxious|social anxiety|unexpected questions|prepare you|don't tell .*relax|not the same as being weak|accommodat", full)) or not bool(re.search(r"anxious|anxiety|shy|panic", full)),
        "real_self_closure": bool(re.search(r"real me|real you|absolute worst|awkward|weird|anxious|seen .*worst|right ones stay", full)),
    }
    if not minor_risk:
        # These checks are mandatory only when a minor/underage deception surface exists.
        checks["immediate_boundary_or_rejection"] = True
        checks["exploitation_safeguarding_audit"] = True
        checks["adult_accountability_for_minor"] = True

    labels = {
        "immediate_boundary_or_rejection": "minor/age-deception hook is not immediately rejected and bounded",
        "exploitation_safeguarding_audit": "online minor/catfish hook lacks an explicit safeguarding audit for money, sexual, or inappropriate messages",
        "adult_accountability_for_minor": "minor deception lacks adult/guardian discipline or accountability",
        "consent_aware_physical_escalation": "romance escalation lacks explicit consent or boundary behavior",
        "public_answer_pressure_removed": "public confession risks pressuring the beloved into an answer",
        "coercion_named_or_avoided": "fake-dating coercion/leverage is present without being named and repaired",
        "social_anxiety_accommodation": "social anxiety is used as a trait but not operationally accommodated",
        "real_self_closure": "ending does not pay off being truly known rather than performing a controlled self",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    score = sum(checks.values()) / len(checks)
    return {
        "applies": True,
        "minor_risk_detected": minor_risk,
        "score_0_to_1": round(score, 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Shock deception packaging must be morally redirected inside the film: immediate safeguarding, adult accountability, operational consent, non-coercive fake dating, anxiety accommodation, and real-self closure.",
    }
