"""Maternal-professional sovereignty doctrine validation for coercive pregnancy-leverage melodrama."""

import re
from typing import Any


def _text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_text(item) for item in value)
    return str(value or "")


def _first(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    return match.start() if match else None


def evaluate_maternal_sovereignty_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    """Warn when pregnancy/custody leverage, professional competence, or consent repair is decorative."""
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    chronology = re.sub(r"\s+", " ", "\n".join([architecture_text, scenes_text])).strip()
    flat = re.sub(r"\s+", " ", " ".join([premise_text, architecture_text, scenes_text])).strip()

    pregnancy_or_heir = bool(re.search(r"\b(?:pregnan\w*|baby|child|children|heir|heiress|miscarriage)\b", flat))
    coercive_status_romance = bool(re.search(r"contract marriage|secret wife|forced marriage|arranged marriage|custody|divorce|fated mate|mate bond|alpha husband|werewolf husband|lycan husband", flat))
    betrayal_or_power_gap = bool(re.search(r"betray|abandon|humiliat|reject|coerc|unwanted|hidden identity|princess|royal", flat))
    applies = pregnancy_or_heir and coercive_status_romance and betrayal_or_power_gap
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    opening = re.sub(r"\s+", " ", " ".join([premise_text, architecture_text[:1200], scenes_text[:1200]])).strip()
    repair_window = chronology[-4500:] if len(chronology) > 4500 else chronology
    checks = {
        "opening_betrayal_endangers_dependent_not_only_pride": bool(
            re.search(r"pregnan|baby|child|heir|bleed|save (?:our|the) baby|medical emergency", opening)
            and re.search(r"abandon|betray|first love|mistress|another woman|leaves? (?:her|them)|prioritizes", opening)
        ),
        "economic_sacrifice_protects_vulnerable_dependent": bool(re.search(r"contract money|money to save|surgery|protect (?:him|her|them|friend|brother|sister)|vulnerable dependent|economic sacrifice|safety", flat)),
        "contract_terms_expose_control_precisely": bool(re.search(r"clause|custody|full custody|belongs? to him|whenever he wants|no choice|control|divorce papers", flat)),
        "child_functions_as_legal_or_political_leverage": bool(re.search(r"custody|heir|succession|political leverage|steal the baby|take the baby|birth during the contract|bloodline|throne", flat)),
        "pregnancy_concealment_is_protective_and_costly": bool(re.search(r"lies? (?:that )?(?:the )?baby (?:died|is dead)|hide[sd]? (?:the )?(?:live )?pregnan|conceal[sd]? (?:the )?pregnan|secret pregnan|miscarriage lie", flat) and re.search(r"cost|isolat|risk|steal|custody|afraid|danger|lose|threat", flat)),
        "professional_competence_is_independent_of_hidden_status": bool(re.search(r"chief healer|doctor|scientific|medical|healing demonstration|research|breakthrough|resume|without nepotism|professional competence|earned craft|hospital", flat)),
        "institutional_public_proof_carries_truth": bool(re.search(r"medical board|security footage|examination|report|evidence|board|investor|election|endorsement|hospital examination|public demonstration", flat)),
        "trust_failure_is_named_beyond_rival_exposure": bool(re.search(r"never trusted|never really wanted|problem is not just|trust failure|emotional abandonment|you did not trust", flat)),
        "male_repair_requires_material_cost_not_only_apology": bool(re.search(r"gives? up (?:the )?(?:campaign|election|power|throne)|abandons? (?:the )?(?:campaign|election)|material sacrifice|injur|loses? power|loses? wealth|sacrifices? (?:his )?(?:career|position|title)", repair_window)),
        "release_of_control_precedes_reunion": (lambda release_pos, reunion_pos: release_pos is not None and reunion_pos is not None and release_pos < reunion_pos)(
            _first(r"signs? (?:the )?divorce papers|lets? go|release[sd]? control|free to leave|no obligation|she can refuse", chronology),
            _first(r"says? yes|remarr|marry me again|reunit|reconcil", chronology),
        ),
        "re_choice_is_informed_and_not_coerced": (lambda truth_pos, reunion_pos: truth_pos is not None and reunion_pos is not None and truth_pos < reunion_pos and not re.search(r"force[sd]? her to (?:marry|return)|no choice but to remarry", repair_window))(
            _first(r"truth is revealed|truth comes out|revealed|exposed|knows? (?:the )?(?:truth|reason)|learns? why|informed", chronology),
            _first(r"says? yes|remarr|marry me again|reunit|reconcil", chronology),
        ),
        "final_status_preserves_craft_and_sovereignty": bool(re.search(r"healer princess|professional|chief healer|strongest woman|sovereign|craft|first and only|chosen partner", repair_window)),
    }
    passed=sum(1 for value in checks.values() if value)
    score=round(passed/len(checks),3)
    labels={
        "opening_betrayal_endangers_dependent_not_only_pride":"the opening betrayal does not clearly endanger a dependent",
        "economic_sacrifice_protects_vulnerable_dependent":"the original economic sacrifice is not anchored in protecting a vulnerable dependent",
        "contract_terms_expose_control_precisely":"contract or custody control is vague rather than materially specific",
        "child_functions_as_legal_or_political_leverage":"the pregnancy/child does not function as real legal or political leverage",
        "pregnancy_concealment_is_protective_and_costly":"pregnancy concealment is missing, unmotivated, or cost-free",
        "professional_competence_is_independent_of_hidden_status":"hidden status substitutes for independent professional competence",
        "institutional_public_proof_carries_truth":"truth remains private reassurance instead of institutional/public proof",
        "trust_failure_is_named_beyond_rival_exposure":"rival exposure is allowed to substitute for diagnosing the partner's trust failure",
        "male_repair_requires_material_cost_not_only_apology":"male repair relies on apology/gifts rather than material cost or relinquished power",
        "release_of_control_precedes_reunion":"reunion occurs before control is released",
        "re_choice_is_informed_and_not_coerced":"the final yes is uninformed, compressed, or coerced",
        "final_status_preserves_craft_and_sovereignty":"closure reduces the heroine to wife/mate instead of preserving craft and sovereignty",
    }
    return {
        "applies": True,
        "score_0_to_1": score,
        "warnings": ["maternal_sovereignty_integrity: "+labels[key] for key,value in checks.items() if not value],
        "checks": checks,
        "craft_rule": "Maternal-professional sovereignty melodrama works when pregnancy/heir leverage creates real institutional stakes, concealment is protective and costly, independent craft outranks hidden status, public proof exposes truth, the partner's trust failure is named, repair requires material sacrifice and release of control, and final re-choice preserves the heroine's sovereignty.",
    }
