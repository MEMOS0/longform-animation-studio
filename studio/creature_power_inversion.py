"""Creature power-inversion integrity checks."""
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


def _ending_keyed_text(value: Any) -> str:
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            key_text = str(key).lower()
            if re.search(r"ending|finale|resolution|epilogue|payoff|final_sequence_use|closing_reversal", key_text):
                parts.append(_text(item))
            elif isinstance(item, (dict, list)):
                parts.append(_ending_keyed_text(item))
        return "\n".join(parts)
    if isinstance(value, list):
        return "\n".join(_ending_keyed_text(item) for item in value)
    return ""


def evaluate_creature_power_inversion(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    creature_term = bool(re.search(r"\bdragon\b|\bcreature\b|\bbeast\b|\bmonster\b", full))
    inversion_term = bool(re.search(r"power inversion|not fire|fire.{0,80}(?:frost|freez|ice)|(?:frost|freez|ice).{0,80}fire|ice breath|cold fire", full))
    applies = bool(re.search(r"power inversion|(?:frost|ice|cold)[- ](?:dragon|creature|beast)|(?:dragon|creature|beast)[- ](?:frost|ice|cold)", full)) or (creature_term and inversion_term)
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    seqs = architecture.get("sequences", []) if isinstance(architecture, dict) else []
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else {}
    finale_text = "\n".join([_text(seqs[-2:]), _text(ending_payoff), _text(scenes[-5:]), _ending_keyed_text(premise)]).strip().lower()

    care_pos = _pos(r"feed|warm|name|blanket|help|look after|pulled .*out|not letting go|steal|coal", full)
    power_pos = _pos(r"power payoff|inverted power|protective power|shield|counterattack|saves? (?:her|them|the village)|protects? (?:her|them|the village)", full)
    stakes_pos = _pos(r"cold|freez|coal|heat|warm|food|stable|poor|winter|resource", full)
    spectacle_pos = _pos(r"execution|burn|stake|trap|bait|king|soldier|crowd|battle|power payoff|protective power", full)

    care_before_power = care_pos is not None and (power_pos is None or care_pos < power_pos)
    stakes_before_spectacle = stakes_pos is not None and (spectacle_pos is None or stakes_pos < spectacle_pos)
    inversion_words = r"frost|freez|ice|cold"
    protective_words = r"protect|save|shield|rescue|counter|stop"

    checks = {
        "material_survival_stakes_before_spectacle": stakes_before_spectacle,
        "difference_shown_behaviorally": bool(re.search(r"not fire|freezes?|frost|ice|different|broken|defect", full)),
        "institution_mislabels_difference": bool(re.search(r"monster|cursed|weakness|beast|threw|burn.*before|abandoned", full)),
        "care_costs_before_power": care_before_power and bool(re.search(r"feed|warm|name|blanket|help|look after|pulled .*out|not letting go|steal|coal", full)),
        "public_execution_or_trap_convergence": bool(re.search(r"execution|burn|stake|trap|bait|king|soldier|crowd", full)),
        "inverted_power_protects": bool(re.search(rf"(?:{inversion_words}).{{0,100}}(?:protects?|saves?|shields?|stops?|counters?)|(?:protects?|saves?|shields?|stops?|counters?).{{0,100}}(?:with|using|through|by).{{0,50}}(?:{inversion_words})", full)),
        "recognition_contact_closure": bool(re.search(r"recognition|contact|touch|forehead|embrace|not letting go|eye", finale_text)),
        "communal_consequence": bool(re.search(r"thaw|green|village|community|people|snow.*melt|melt.*snow|rebuild|proclaim|order changes", finale_text)),
    }
    labels = {
        "material_survival_stakes_before_spectacle": "creature inversion lacks material/environmental survival stakes before spectacle",
        "difference_shown_behaviorally": "creature difference is explained rather than shown behaviorally",
        "institution_mislabels_difference": "institution does not mislabel the difference as defect/monstrosity",
        "care_costs_before_power": "care does not cost resources/safety/status before power payoff",
        "public_execution_or_trap_convergence": "resource monopoly and scapegoating do not converge into public execution/trap stakes",
        "inverted_power_protects": "inverted power is not used protectively",
        "recognition_contact_closure": "ending lacks recognition/contact after spectacle",
        "communal_consequence": "ending lacks visible communal or environmental consequence",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {"applies": True, "score_0_to_1": round(sum(checks.values()) / len(checks), 3), "warnings": warnings, "checks": checks, "craft_rule": "Creature inversion works when material survival stakes precede spectacle, the institution misreads difference as defect, costly care precedes power, and the inverted power protects through recognition plus visible communal consequence."}
