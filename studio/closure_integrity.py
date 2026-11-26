"""Closure integrity: sequel hooks must not replace relational/home payoff."""
from __future__ import annotations

import re
from typing import Any

CLOSURE_TERMS = [
    "home", "belong", "safe", "recognition", "remember", "family", "community", "chosen", "choose",
    "love", "repair", "apolog", "dignity", "partnership", "garden", "table", "meal", "sanctuary", "healing",
]
SEQUEL_TERMS = [
    "another", "new disturbance", "star abyss", "stories are just beginning", "story is just beginning", "war coming",
    "not over", "returns", "wakes", "sequel", "next enemy", "elsewhere", "beyond the stars",
]
INFRASTRUCTURE_TERMS = ["water", "food", "storm", "shield", "power", "array", "infrastructure", "harbor", "valves"]
COMMUNITY_CONSEQUENCE_TERMS = [
    "survive", "survives", "survived", "people are safe", "new system", "restore", "restores", "restored",
    "rebuild", "rebuilds", "rebuilt", "replace", "replaces", "replaced", "repair", "repairs", "repaired",
    "ration", "rations", "rationed", "redistribute", "redistributed", "communal", "shared water", "shared food",
    "share their remaining", "share supplies", "shared supplies", "shares supplies", "keep everyone fed", "keeps everyone fed",
    "feed everyone", "feeds everyone", "food is shared", "water is shared",
]
COLLAPSE_PATTERNS = [
    r"self-destruct\w*",
    r"(?:array|system|infrastructure|shield(?:\s+nodes)?|power grid|harbor|valves?)\s+(?:is|are|was|were)?\s*(?:destroyed|collapsing|collapses|collapsed|fails|failing|shutting down|going dark|goes dark|go dark|went dark)",
    r"(?:destroy(?:s|ed)?|disable(?:s|d)?|shut(?:s|ting)? down|collapse(?:s|d)?)\s+(?:the\s+)?(?:water\s+|power\s+|storm\s+|holy-light\s+)?(?:array|system|infrastructure|shield(?:\s+nodes)?|power grid|harbor|valves?)",
    r"(?:array|system|infrastructure|shield(?:\s+nodes)?|power grid|harbor|valves?)\s+(?:goes|go|went)\s+dark",
]
CONDITION_RE = re.compile(r"\b(?:if|whether|unless)\b")
MODAL_RE = re.compile(r"\b(?:will|would|could|can|may|might|shall)\s+(?:[\w'-]+\s+){0,3}$")
INTENT_RE = re.compile(r"\b(?:threaten\w* to|plan\w* to|try\w* to|want\w* to|choose\w* to|intend\w* to|plot\w* to|prepare\w* to)\s+(?:[\w'-]+\s+){0,7}(?:and\s+)?$")
NEGATION_RE = re.compile(r"\b(?:no|not|never|does not|did not|didn't|do not|don't|won't|avoids?|prevents?|fails? to|refuses? to)\s+(?:[\w'-]+\s+){0,5}$")


def flatten(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(flatten(v) for v in value.values())
    if isinstance(value, list):
        return "\n".join(flatten(v) for v in value)
    return ""


def _positions(text: str, terms: list[str]) -> dict[str, int]:
    lowered = text.lower()
    found: dict[str, int] = {}
    for term in terms:
        position = lowered.find(term)
        if position >= 0:
            found[term] = position
    return found


def _all_positions(text: str, terms: list[str]) -> dict[str, list[int]]:
    lowered = text.lower()
    found: dict[str, list[int]] = {}
    for term in terms:
        positions = [match.start() for match in re.finditer(re.escape(term), lowered)]
        if positions:
            found[term] = positions
    return found


def _positive_term_positions(text: str, terms: list[str]) -> dict[str, list[int]]:
    lowered = text.lower()
    found: dict[str, list[int]] = {}
    negation_before = re.compile(r"(?:beyond|without|no|not|never|unable to|fails? to|impossible to)\s+$")
    for term in terms:
        positions = []
        for match in re.finditer(re.escape(term), lowered):
            before = lowered[max(0, match.start() - 30):match.start()]
            if not negation_before.search(before):
                positions.append(match.start())
        if positions:
            found[term] = positions
    return found


def _sentence_bounds(text: str, position: int) -> tuple[int, int]:
    start = max(text.rfind(".", 0, position), text.rfind("!", 0, position), text.rfind("?", 0, position), text.rfind("\n", 0, position)) + 1
    endings = [idx for idx in [text.find(".", position), text.find("!", position), text.find("?", position), text.find("\n", position)] if idx >= 0]
    end = min(endings) + 1 if endings else len(text)
    return start, end


def _is_hypothetical(text: str, position: int) -> bool:
    start, end = _sentence_bounds(text, position)
    before_sentence = text[start:position]
    clause_start = max(before_sentence.rfind(","), before_sentence.rfind(";"), before_sentence.rfind(":"))
    for match in re.finditer(r"\b(?:but|however|yet)\b", before_sentence):
        clause_start = match.end()
    before = before_sentence[clause_start + 1 :] if clause_start >= 0 else before_sentence
    after = text[position:end]
    if CONDITION_RE.search(before) or CONDITION_RE.search(after):
        return True
    if re.search(r"\b(?:after|before|when|while|as)\s+(?:the\s+)?$", before):
        return False
    if MODAL_RE.search(before) or INTENT_RE.search(before) or NEGATION_RE.search(before):
        return True
    return "?" in text[start:end] and re.search(r"\b(?:will|would|could|can|what if|how|why|when)\b", before_sentence) is not None


def _collapse_events(text: str) -> list[int]:
    lowered = text.lower()
    events: set[int] = set()
    for pattern in COLLAPSE_PATTERNS:
        for match in re.finditer(pattern, lowered):
            if not _is_hypothetical(lowered, match.start()):
                events.add(match.start())
    return sorted(events)


def _row(sequence: str | int, text: str) -> dict[str, Any]:
    closure = _positions(text, CLOSURE_TERMS)
    sequel = _positions(text, SEQUEL_TERMS)
    community_positions = _positive_term_positions(text, COMMUNITY_CONSEQUENCE_TERMS)
    return {
        "sequence": sequence,
        "text": text.lower(),
        "closure_positions": closure,
        "sequel_positions": sequel,
        "community_positions": community_positions,
        "closure_hits": list(closure),
        "sequel_hits": list(sequel),
        "infrastructure_hits": list(_positions(text, INFRASTRUCTURE_TERMS)),
        "community_consequence_hits": list(community_positions),
    }


def _scene_has_later_recovery(text: str) -> bool:
    """Accept recovery evidence while rejecting generic shared/community boilerplate
    and explicitly early beats that merely precede a later collapse."""
    lowered = text.lower()
    positions = _positive_term_positions(lowered, COMMUNITY_CONSEQUENCE_TERMS)
    if not positions:
        return False
    collapse_positions = _collapse_events(lowered)
    if collapse_positions:
        earliest_collapse = collapse_positions[0]
        return _has_positions_after(positions, earliest_collapse)
    explicitly_prior = re.search(r"(?:before|prior to)\s+(?:the\s+)?(?:collapse|outage|failure|shutdown)", lowered) or re.search(r"(?:already|previously)\s+(?:rebuilt|restored|repaired)\s+before", lowered)
    if explicitly_prior:
        return False
    return True


def _has_positions_after(position_map: dict[str, list[int]], position: int) -> bool:
    return any(point > position for positions in position_map.values() for point in positions)


def evaluate_closure_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Evaluate delivered payoff, not merely the premise's promised payoff.

    Only architecture/scene evidence counts as delivered closure. A premise can
    promise home or recognition, but that promise is not evidence the ending
    dramatized it. Sequel expansion is evaluated in the payoff zone (the final
    two sequences plus explicit ending_payoff); earlier sequel words may be
    ordinary foreshadowing rather than an ending substitute.
    """
    scenes = scenes or []
    sequences = architecture.get("sequences") or []
    rows = [_row(seq.get("sequence", index + 1), flatten(seq)) for index, seq in enumerate(sequences)]
    sequence_count = len(rows)
    if architecture.get("ending_payoff"):
        rows.append(_row("ending_payoff", flatten(architecture.get("ending_payoff"))))

    warnings: list[str] = []
    payoff_start = max(0, sequence_count - 2)
    payoff_rows = rows[payoff_start:]
    for row_index, row in enumerate(rows):
        if row_index < payoff_start or not row["sequel_positions"]:
            continue
        sequel_position = min(row["sequel_positions"].values())
        closure_before = False
        for prior in rows[payoff_start:row_index]:
            if prior["closure_positions"]:
                closure_before = True
                break
        if not closure_before:
            same_row_closure = [position for position in row["closure_positions"].values() if position < sequel_position]
            closure_before = bool(same_row_closure)
        if not closure_before:
            warnings.append("sequel expansion appears before a relational/home closure beat lands")
            break

    final_architecture_text = "\n".join(row["text"] for row in payoff_rows)
    final_scene_text = flatten(scenes[-2:] if len(scenes) >= 2 else scenes).lower()
    final_text = final_architecture_text + "\n" + final_scene_text
    final_closure = list(_positions(final_text, CLOSURE_TERMS))
    if rows and not final_closure:
        warnings.append("final movement lacks a clear relational/home/belonging closure signal")

    infrastructure = list(_positions(flatten(architecture) + "\n" + flatten(scenes), INFRASTRUCTURE_TERMS))
    consequence = list(_positions(final_text, COMMUNITY_CONSEQUENCE_TERMS))
    scene_rows = [_row(scene.get("scene_id", f"scene-{index + 1}"), flatten(scene)) for index, scene in enumerate(scenes)]
    final_scene_rows = scene_rows[-2:] if len(scene_rows) >= 2 else scene_rows
    collapse_needs_followup = False
    for row_index in range(payoff_start, len(rows)):
        row = rows[row_index]
        for collapse_position in _collapse_events(row["text"]):
            same_row_after = _has_positions_after(row["community_positions"], collapse_position)
            later_rows_after = any(later["community_consequence_hits"] for later in rows[row_index + 1 :])
            screenplay_after = any(_scene_has_later_recovery(later["text"]) for later in final_scene_rows)
            if not same_row_after and not later_rows_after and not screenplay_after:
                collapse_needs_followup = True
                break
        if collapse_needs_followup:
            break
    if infrastructure and collapse_needs_followup:
        warnings.append("infrastructure/system collapse is not followed by visible community survival, replacement, or rebuilding consequence")
    score = max(0.0, round(1.0 - 0.28 * len(warnings), 2))
    public_rows = []
    for row in rows:
        public_rows.append({
            "sequence": row["sequence"],
            "closure_hits": row["closure_hits"],
            "sequel_hits": row["sequel_hits"],
            "infrastructure_hits": row["infrastructure_hits"],
            "community_consequence_hits": row["community_consequence_hits"],
        })
    return {
        "score_0_to_1": score,
        "rows": public_rows,
        "final_closure_hits": final_closure,
        "warnings": warnings,
        "craft_rule": "A plot sequel hook may remain, but only after the promised recognition, home, belonging, and community consequence have landed.",
    }
