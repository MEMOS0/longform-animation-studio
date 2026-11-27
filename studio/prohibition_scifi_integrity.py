"""Integrity checks for sensory-prohibition post-apocalyptic sci-fi.

Derived from FANTASY MOVIE KINGDOM evidence. These checks evaluate a
"don't look up" style rule as a story engine, not as a surface gimmick.
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


def evaluate_prohibition_scifi_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    applies = bool(re.search(r"don'?t look up|look up|sensory prohibition|post[- ]apocalyptic|collector|eden|meridian|ai(?:\s+machine)?", full))
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}
    checks = {
        "rule_has_behavioral_cost": bool(re.search(r"don'?t look up|face down|eyes on me|count to|practice|carried off|taken|wipe", full)),
        "rescue_countdown": bool(re.search(r"72 hours|three days|one day left|hours left|before.*wipe|deadline|countdown", full)),
        "companion_trust_arc": bool(re.search(r"robot|machine|companion|friend|not a thing|trust you|you gave me a name", full)),
        "scapegoat_reversal": bool(re.search(r"machine (?:didn'?t|did not)|said no|refused to launch|blamed a machine|human|a man did|scapegoat", full)),
        "false_paradise_exposed": bool(re.search(r"paradise.*mines|mines|erased|memory|wipe|don'?t remember|collar|control", full)),
        "rule_inversion_payoff": bool(re.search(r"look up.*safe|can look up now|look at its eyes|no one has to hide their face|what the sky looked like", full)),
        "relational_memory_closure": bool(re.search(r"remember for both|compass|find your way back|father|dad|family|home", full[-2500:])),
        "sequel_hook_after_closure": bool(re.search(r"another eden|sequel|next|new threat", full[-1200:])) and bool(re.search(r"safe now|remember for both|build a world|home|free", full[-2500:])),
    }
    labels = {
        "rule_has_behavioral_cost": "sensory prohibition is exposition rather than rehearsed behavior with consequence",
        "rescue_countdown": "rescue lacks a time pressure or irreversible deadline",
        "companion_trust_arc": "machine/creature companion lacks a distrust-to-personhood/friendship arc",
        "scapegoat_reversal": "machine-as-monster premise lacks evidence-driven scapegoat reversal",
        "false_paradise_exposed": "utopian/Eden promise is not materially exposed as coercive memory/labor control",
        "rule_inversion_payoff": "the central prohibition is not inverted into a visual/thematic final payoff",
        "relational_memory_closure": "ending lacks relational memory/home recognition closure",
        "sequel_hook_after_closure": "sequel hook arrives before relational and spatial closure",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "A sensory prohibition works as a story engine when rehearsed behavior has cost, rescue has a deadline, the feared machine/person is re-evidenced, the false paradise is materially exposed, and the ending visually invert the rule before any sequel hook.",
    }
