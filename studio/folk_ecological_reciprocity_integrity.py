"""Creative warnings for folk/ecological reciprocity legends.

This is not a performance predictor. It checks whether a culturally grounded
legend uses supernatural presence as a reciprocal ecological/communal relation
rather than a mascot, treasure, or generic war spectacle.
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


def evaluate_folk_ecological_reciprocity_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    arch = _text(architecture).lower()
    end = arch[-max(1, len(arch) // 3):] + "\n" + (_text(scenes[-1]).lower() if scenes else "")

    folk = bool(re.search(r"legend|folk|myth|spirit|serpent|giant|beast|dragon|queen|guardian|mountain|forest|village", full))
    ecology = bool(re.search(r"oak|forest|mountain|water|spring|river|slope|soil|herb|honey|harvest|land|sea|ecosystem|village|commons", full))
    reciprocal = bool(re.search(r"oath|promise|heal|cure|protect|share|trade|help|remember|steward|care|warm|feed|save", full))
    extraction = bool(re.search(r"cut\w*[^.\n]{0,50}(?:oak|forest|tree|slope)|strip\w*[^.\n]{0,50}(?:slope|land|forest)|steal|theft|poison|gold|immortal|heart|cage|capture|hunt\w*|land grab|buy\w*[^.\n]{0,40}(?:land|plot|water)|enclos|mine|profit|charcoal", full))
    if not (folk and ecology and reciprocal and extraction):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    generic_war = bool(re.search(r"army|warrior army|battlefield|siege|conquer|war band", full)) and not bool(re.search(r"water|oak|herb|honey|spring|slope|land|forest|mountain|village", full))

    checks = {
        "opening_grounds_legend_in_ordinary_labor_and_material_culture": bool(re.search(r"charcoal|bread|eggs|honey|rope|harvest|rice|shepherd|farm|weav\w*|fish\w*|market|craft|work|door|hearth", full)),
        "supernatural_entity_is_tied_to_ecological_or_communal_function": bool(re.search(r"stones?|wall|boundary|water|spring|river|mountain|forest|oak|healing|medicine|herb|warm\w*|protect\w*|cure\w*", full)),
        "central_conflict_is_extraction_enclosure_or_broken_reciprocity": extraction,
        "human_mediator_uses_oath_care_or_local_knowledge_not_domination": bool(re.search(r"oath|promise|swear|heal|cure|carry|help|remember|teach|share|protect|keep\w* secret|never tell", full)) and not bool(re.search(r"captur\w*[^.\n]{0,40}(?:creature|serpent|beast|giant)|cage\w*[^.\n]{0,40}(?:creature|serpent|beast|giant)", end)),
        "betrayal_or_secret_has_visible_social_or_ecological_cost": bool(re.search(r"hunters?|mother pays|slope|slide|washing away|poison|trust|betray|secret|men know|die|death|leave|gone because", full)),
        "ecological_consequences_are_physical_and_material": bool(re.search(r"slope|slide|washing away|water|drought|spring|mountain comes down|roots hold|flood|fire|soil|forest gone|poison", full)),
        "ordinary_evidence_or_witnesses_expose_the_violation": bool(re.search(r"proof|witness|saw|tells?|admits?|confess|records?|tracks?|nails|ditch|sleeve|black root|poisoned|orders?|testimony", full)),
        "community_participates_in_survival_or_restoration": bool(re.search(r"village|barrio|neighbors?|everyone|wake the village|community|people|doors|homes", full)),
        "supernatural_entity_retains_autonomy_home_and_nonownership": bool(re.search(r"my home|under the mountain|went home|not yours|release|free|stay[^.\n]{0,30}(?:mountain|forest|home)|refus\w* palace|never tell where i live", full + "\n" + end)),
        "ending_restores_commons_memory_or_seasonal_continuity": bool(re.search(r"remember|forget me not|spring|dawn|wall|water|home|carrying him home|doors warm|commons|village|mountain|thank you", end)),
        "conflict_is_not_substituted_by_generic_war_spectacle": not generic_war,
        "cultural_specificity_is_material_practice_not_costume_only": bool(re.search(r"basque|anatolian|visayan|oak|charcoal|honey|herb|water mint|silver leaf|rice|shepherd|barrio|mountain|door|hearth|spring", full)),
    }
    missing = [k for k, v in checks.items() if not v]
    score = round(sum(1 for v in checks.values() if v) / len(checks), 3)
    warnings = []
    if missing:
        warnings.append("Folk/ecological reciprocity risks weakening: " + ", ".join(missing[:6]))
    if generic_war:
        warnings.append("Do not replace the ecological/relational contract with generic fantasy war spectacle.")
    return {"applies": True, "score_0_to_1": score, "warnings": warnings, "checks": checks}
