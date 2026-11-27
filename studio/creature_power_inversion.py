"""Creature power-inversion integrity checks."""
from __future__ import annotations

import re
from typing import Any


def _text(value: Any) -> str:
    if isinstance(value, str): return value
    if isinstance(value, dict): return "\n".join(_text(v) for v in value.values())
    if isinstance(value, list): return "\n".join(_text(v) for v in value)
    return ""


def evaluate_creature_power_inversion(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    applies = bool(re.search(r"power inversion|not fire|freez|frost|cold.*dragon|dragon.*cold|ice.*creature|creature.*ice", full))
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}
    checks = {
        "material_survival_stakes_before_spectacle": bool(re.search(r"cold|freez|coal|heat|warm|food|stable|poor|winter|resource", full)),
        "difference_shown_behaviorally": bool(re.search(r"not fire|freezes?|frost|ice|different|broken|defect", full)),
        "institution_mislabels_difference": bool(re.search(r"monster|cursed|weakness|beast|threw|burn.*before|abandoned", full)),
        "care_costs_before_power": bool(re.search(r"feed|warm|name|blanket|help|look after|pulled .*out|not letting go|steal|coal", full)),
        "public_execution_or_trap_convergence": bool(re.search(r"execution|burn|stake|trap|bait|king|soldier|crowd", full)),
        "inverted_power_protects": bool(re.search(r"protect|save|shield|rescue|counter|stop|frost.*fire|freez.*fire", full)),
        "recognition_contact_closure": bool(re.search(r"recognition|contact|touch|forehead|embrace|not letting go|eye", full[-3500:])),
        "communal_consequence": bool(re.search(r"thaw|green|village|community|people|snow.*melt|melt.*snow|rebuild|proclaim|order changes", full[-3500:])),
    }
    labels = {
        "material_survival_stakes_before_spectacle": "creature inversion lacks material/environmental survival stakes",
        "difference_shown_behaviorally": "creature difference is explained rather than shown behaviorally",
        "institution_mislabels_difference": "institution does not mislabel the difference as defect/monstrosity",
        "care_costs_before_power": "care does not cost resources/safety/status before power payoff",
        "public_execution_or_trap_convergence": "resource monopoly and scapegoating do not converge into public execution/trap stakes",
        "inverted_power_protects": "inverted power is not used protectively",
        "recognition_contact_closure": "ending lacks recognition/contact after spectacle",
        "communal_consequence": "ending lacks visible communal or environmental consequence",
    }
    warnings=[label for key,label in labels.items() if not checks[key]]
    return {"applies":True,"score_0_to_1":round(sum(checks.values())/len(checks),3),"warnings":warnings,"checks":checks,"craft_rule":"Creature inversion works when material survival stakes precede spectacle, the institution misreads difference as defect, costly care precedes power, and the inverted power protects through recognition plus visible communal consequence."}
