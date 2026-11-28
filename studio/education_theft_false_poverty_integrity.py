"""Creative warnings for education-theft and false-poverty family exploitation stories.

Transparent heuristic, not a performance predictor.
"""

from typing import Any
import re


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(str(k) + " " + _text(v) for k, v in value.items())
    if isinstance(value, list):
        return "\n".join(_text(v) for v in value)
    return "" if value is None else str(value)


def evaluate_education_theft_false_poverty_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    arch = _text(architecture).lower()
    end = arch[-max(1, len(arch) // 3):] + "\n" + (_text(scenes[-1]).lower() if scenes else "")

    education = bool(re.search(r"school|college|university|tuition|student|exam|gaokao|education|thesis|graduate|scholarship", full))
    family = bool(re.search(r"parent|mother|father|mom|dad|sister|brother|family|daughter|son", full))
    poverty = bool(re.search(r"pretend\w*[^.\n]{0,30}poor|false poverty|act poor|poor act|scrap|recycling|can't afford|cannot afford|tuition|debt|bankrupt", full))
    coercion = bool(re.search(r"quit school|drop\w* out|forced? to work|work at the (?:scrap|recycling)|child labor|steal\w*[^.\n]{0,30}(?:education|future)|exploit\w*|made me quit", full))
    if not (education and family and poverty and coercion):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    reconciliation = bool(re.search(r"forgiv\w*[^.\n]{0,50}(?:parents?|mother|father|family)|reunit\w*[^.\n]{0,50}(?:parents?|mother|father|family)|reconcil\w*[^.\n]{0,50}(?:parents?|mother|father|family)", end))

    checks = {
        "opening_makes_education_coercion_and_refusal_immediately_specific": bool(re.search(r"quit school|dropping out|not quitting school|pay my own tuition|college entrance exams", full)),
        "economic_exploitation_is_material_and_procedural": bool(re.search(r"tuition|scrapyard|recycling yard|child labor|wages?|pay\w*[^.\n]{0,30}(?:family|parents?)|labor bureau|contract|sign\w*|living expenses", full)),
        "false_poverty_is_contradicted_by_hidden_assets_or_luxury": bool(re.search(r"pretend\w*[^.\n]{0,30}poor|act poor|luxury store|designer|chanel|storefronts?|fully paid|assets|hidden money|rich family", full)),
        "favoritism_allocates_family_resources_to_another_child": bool(re.search(r"sister|brother|younger daughter|all meant for|favored|elite school|study abroad|assets are all meant", full)),
        "protagonist_resists_through_work_study_law_and_competence": bool(re.search(r"pay my own tuition|work\w*[^.\n]{0,30}(?:supermarket|job|study)|scores?|exam|labor bureau|police|teacher|scholarship|top scorer|university", full)),
        "institutional_or_community_witnesses_interrupt_family_coercion": bool(re.search(r"teacher|school|boss|police|labor bureau|security|admissions team|court|media|everyone|witness", full)),
        "filial_piety_public_shaming_is_named_and_challenged": bool(re.search(r"ungrateful|unfilial|shameless|family business|driving.*parents|own mother|heartless|conscience|respect", full)),
        "identity_or_recorded_evidence_exposes_the_false_poverty": bool(re.search(r"evidence|recording|doctored|fake|designer|chanel|storefronts?|assets|luxury store|witness|public", full)),
        "achievement_compounds_education_into_independent_capability": bool(re.search(r"university|college|degree|graduate|thesis|company|founder|chairwoman|career|profession|technical|AI|empire of your own", full + "\n" + end)),
        "sibling_appropriation_or_counterfeit_identity_is_confronted": bool(re.search(r"pretend\w*[^.\n]{0,40}(?:me|her|zhao)|admissions team|top scorer|stole my future|your sister|sister.*sign|change your clothes", full)),
        "material_consequences_match_the_extraction": bool(re.search(r"bankrupt|asset seizure|court|lawsuit|clients|funding|debt|scavenging|collect scrap|lost everything|arrest|sentenced", end + "\n" + full[-max(1, len(full) // 3):])),
        "ending_sets_boundary_without_reconciliation_or_gratuitous_cruelty": bool(re.search(r"market rate|every cent|doesn't care|no need to go out of your way|get out|boundary|own way|not doing this to get back|not because she pities", end)) and not reconciliation,
        "education_or_self_defined_future_survives_after_revenge": bool(re.search(r"graduate|thesis|studies|school|alma mater|career|knowledge|future|partner in life|signing ceremony|empire", end)),
        "false_poverty_is_not_romanticized_without_accountability": bool(re.search(r"pretending|pretend|fake|wrong|apolog|sorry|test|truth|expose|shameless|two-faced|live with the part", full)),
    }
    missing = [k for k, v in checks.items() if not v]
    score = round(sum(1 for v in checks.values() if v) / len(checks), 3)
    warnings = []
    if missing:
        warnings.append("Education-theft/false-poverty contract risks weakening: " + ", ".join(missing[:6]))
    if reconciliation:
        warnings.append("Do not restore exploitative parents through unearned reconciliation; education autonomy requires durable boundaries.")
    return {"applies": True, "score_0_to_1": score, "warnings": warnings, "checks": checks}
