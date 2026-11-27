"""Hidden-mastery competence-cascade integrity checks.

Derived from Jasmine Drama evidence. These heuristics separate a serialized
hidden-competence revenge engine from random power inflation or genre hopping.
They are warnings, not performance predictions.
"""
from __future__ import annotations

import re
from typing import Any


def _is_checklist_key(key: Any) -> bool:
    markers = ("anti_pattern", "anti-patterns", "warnings", "validation", "craft_rule", "checklist")
    return any(marker in str(key).lower() for marker in markers)


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        checklist_markers = ("anti_pattern", "anti-patterns", "warnings", "validation", "craft_rule", "checklist")
        return "\n".join(_text(v) for k, v in value.items() if not any(marker in str(k).lower() for marker in checklist_markers))
    if isinstance(value, list):
        return "\n".join(_text(v) for v in value)
    return ""


def _count_any(text: str, groups: dict[str, str]) -> int:
    return sum(1 for pattern in groups.values() if re.search(pattern, text))


def _early_story_text(architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    sequences = architecture.get("sequences") if isinstance(architecture, dict) else None
    if isinstance(sequences, list) and sequences:
        count = max(1, (len(sequences) + 2) // 3)
        parts.extend(_text(sequence).lower() for sequence in sequences[:count])
    elif architecture:
        text = _text(architecture).lower()
        parts.append(text[:max(1, len(text) // 3)])
    if scenes:
        count = max(1, (len(scenes) + 2) // 3)
        parts.extend(_text(scene).lower() for scene in scenes[:count])
    return "\n".join(parts)


def _ordered_architecture_text(architecture: dict[str, Any]) -> str:
    parts: list[str] = []
    sequences = architecture.get("sequences") if isinstance(architecture, dict) else None
    if isinstance(sequences, list):
        parts.extend(_text(sequence).lower() for sequence in sequences)
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else None
    if ending_payoff:
        parts.append(_text(ending_payoff).lower())
    return "\n".join(parts)


def _ordered_scene_text(scenes: list[dict[str, Any]]) -> str:
    return "\n".join(_text(scene).lower() for scene in scenes)


def _closure_before_hook_in_ordered_text(text: str) -> bool:
    if not text:
        return False
    hook_match = re.search(r"new mission|top-level mission|return to the team|sequel hook|next mission|ordered to|called away", text)
    closure_match = re.search(r"justice|law|court|police|family|reunited|marriage|belonging|instructor|new identity|special agent|peace|home", text)
    return bool(closure_match) and (not hook_match or closure_match.start() < hook_match.start())


def _has_coercive_intimacy(text: str) -> bool:
    text = re.sub(r"\bnoo+\b", "no", text)
    coercion_patterns = [
        r"no right to refuse",
        r"can.?t refuse",
        r"won.?t take no",
        r"forced? .*?(?:bed|sex|kiss|intimacy)",
        r"(?:ignores|ignored|ignoring).{0,35}(?:no|refusal|stop)",
        r"(?:said|says|asked|begged).{0,30}\b(?:no|stop)\b.{0,50}(?:keeps|kept|continues|continued|doesn.?t stop)",
        r"(?:keeps|kept|continues|continued).{0,30}(?:kissing|touching|undressing).{0,45}after.{0,35}(?:she|he|they).{0,12}(?:says?|said).{0,8}\b(?:no|stop)\b",
        r"belong completely to me",
        r"you are mine now",
    ]
    intimacy_pattern = re.compile(r"kiss|sex|sexual|bed|bedroom|intimate|intimacy|romance|romantic|touch|undress|wedding night|belong|mine")
    for pattern in coercion_patterns:
        for match in re.finditer(pattern, text):
            window = text[max(0, match.start() - 140):match.end() + 140]
            if intimacy_pattern.search(window):
                return True
    return False


def _artifact_units(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> list[str]:
    units = [_text(premise).lower()]
    sequences = architecture.get("sequences") if isinstance(architecture, dict) else None
    if isinstance(sequences, list):
        units.extend(_text(sequence).lower() for sequence in sequences)
        for key, value in architecture.items():
            if key not in {"sequences", "ending_payoff"} and not _is_checklist_key(key):
                units.append(_text(value).lower())
    elif architecture:
        units.append(_text(architecture).lower())
    ending_payoff = architecture.get("ending_payoff") if isinstance(architecture, dict) else None
    if ending_payoff:
        units.append(_text(ending_payoff).lower())
    units.extend(_text(scene).lower() for scene in scenes)
    return [unit for unit in units if unit]


def _positive_hidden_master_identity(text: str) -> bool:
    for match in re.finditer(r"prodigy|genius|master hacker|secretly skilled|hidden mastery", text):
        prefix = text[max(0, match.start() - 35):match.start()]
        if not re.search(r"(?:no|not|without|lacks|never)(?:\s+\w+){0,3}\s*$", prefix):
            return True
    return False


def evaluate_competence_cascade_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    premise_text = _text(premise).lower()
    architecture_text = _text(architecture).lower()
    scenes_text = _text(scenes).lower()
    full = "\n".join([premise_text, architecture_text, scenes_text])
    opening = _early_story_text(architecture, scenes)

    mastery_terms = r"assassin|special agent|mercenary|elite operative|master hacker|top assassin|king of killers|prodigy|genius|expert"
    hidden_mastery = bool(
        re.search(r"(?:reborn|transmigrated|secretly|hidden|undercover|disguised|concealed).{0,90}(?:" + mastery_terms + r")", full)
        or re.search(r"(?:" + mastery_terms + r").{0,90}(?:hidden identity|secret identity|double life|concealed|reborn|transmigrated)", full)
        or _positive_hidden_master_identity(full)
    )
    humiliation_reversal = bool(re.search(r"bully|bullied|humiliat|shame|diary|debt collector|looked down|power inversion|revenge|reborn|transmigrat|new body", full))
    applies = hidden_mastery and humiliation_reversal
    if not applies:
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    competence_domains = {
        "combat": r"combat|fight|martial|assassin|shoot|marksman|weapon|tactical",
        "mobility": r"race|racing|drive|driving|chase|parkour|pilot",
        "knowledge": r"math|language|academic|genius|scholar|memory|code|cipher",
        "investigation": r"hack|investigate|evidence|surveillance|camera|trace|records|forensic",
        "resources": r"money|assets|fund|company|account|prize money|wealth",
        "leadership": r"lead|command|instructor|mentor|team|legion|protect subordinate",
    }
    arenas = {
        "school": r"school|academy|classroom|principal|teacher|campus",
        "home_family": r"home|family|mother|father|brother|sister|dinner",
        "medical": r"hospital|clinic|doctor|nurse",
        "street_crime": r"street|debt collector|gang|underground|brothel|kidney",
        "race": r"race|racing|track|car",
        "military": r"military|army|special forces|mercenary|training camp|shooting",
        "elite_social": r"banquet|party|gala|noble|elite|chamber",
        "arena": r"arena|duel|gladiator|fight club",
        "procedure": r"police|court|judge|lawyer|law|military tribunal",
    }

    hook_pattern = r"new mission|top-level mission|return to the team|sequel hook|next mission|new case|fresh case|assigned to investigate|assignment to investigate|orders? (?:her|him|them) to investigate|called away"
    closure_pattern = r"justice (?:is )?(?:served|done|delivered)|police (?:close|solve|arrest|deliver justice)|close[sd]? the conspiracy|conspiracy (?:is )?(?:closed|exposed|resolved)|case (?:is )?(?:closed|solved)|family (?:is )?(?:reunited|restored|safe)|reunited with (?:her|his|their) family|belonging (?:lands|is restored)|peace (?:is )?restored|public apology|community is safe|safe at home|earns? (?:her|his|their) (?:new )?(?:role|place|identity)|finds? acceptance|accepted as|steps? into (?:her|his|their) new role|new identity is accepted"
    def actual_closure_match(text: str):
        for match in re.finditer(closure_pattern, text):
            prefix = text[max(0, match.start() - 35):match.start()]
            if re.search(r"\b(?:before|until|unless|if)\b[^.!?]{0,35}$", prefix):
                continue
            return match
        return None
    def closure_order(text: str) -> str:
        hook_match = re.search(hook_pattern, text)
        closure_match = actual_closure_match(text)
        if closure_match and hook_match:
            return "positive" if closure_match.start() < hook_match.start() else "negative"
        if closure_match:
            return "closure_only"
        if hook_match:
            return "hook_only"
        return "neutral"

    def explicit_order(text: str) -> str:
        normalized = re.sub(r"\s+", " ", text.lower())
        closure_terms = r"(?:closure|reunion|justice is served|justice is delivered|case(?: is)? closed|conspiracy(?: is)? closed|family reunion|acceptance|new role|victory epilogue)"
        hook_terms = r"(?:mission|new mission|next mission|new case|fresh case|assignment|teaser|sequel)"
        if re.search(hook_terms + r"[^.!?]{0,80}\bbefore\b[^.!?]{0,80}" + closure_terms, normalized):
            return "negative"
        if re.search(closure_terms + r"[^.!?]{0,80}\bbefore\b[^.!?]{0,80}" + hook_terms, normalized):
            return "positive"
        if re.search(r"\bafter\b[^.!?]{0,60}" + closure_terms + r"[^.!?]{0,80}" + hook_terms, normalized):
            return "positive"
        if re.search(closure_terms + r".{0,120}(?:and )?only then.{0,120}" + hook_terms, normalized):
            return "positive"
        if re.search(r"\bafter\b[^.!?]{0,60}" + closure_terms + r"[^.!?]{0,80}" + hook_terms, normalized):
            return "positive"
        return "neutral"

    scene_order = "neutral"
    if scenes:
        scene_texts = [_text(scene).lower() for scene in scenes]
        if len(scene_texts) == 1:
            scene_order = explicit_order(scene_texts[0])
        first_hook = None
        first_closure = None
        offset = 0
        for index, text in enumerate(scene_texts):
            hook_match = re.search(hook_pattern, text)
            closure_match = actual_closure_match(text)
            if first_hook is None and hook_match:
                weak_assignment = bool(re.search(r"new case|fresh case|assigned to investigate|assignment to investigate|orders? (?:her|him|them) to investigate", text)) and not re.search(r"new mission|next mission|sequel|return to the team|called away|another case", text)
                closure_before_here = bool(closure_match and closure_match.start() < hook_match.start())
                explicit_premature = bool(re.search(r"before (?:the )?(?:current )?(?:case|conspiracy|mission).{0,35}(?:is )?(?:closed|closure|resolved|solved)", text))
                if not (weak_assignment and index == 0 and len(scenes) > 1 and not closure_before_here and not explicit_premature):
                    first_hook = (index, hook_match.start(), hook_match.end())
            if first_closure is None and closure_match:
                first_closure = (index, closure_match.start(), closure_match.end())
            offset += len(text) + 1
        if scene_order == "neutral":
            if first_hook is not None and first_closure is not None:
                hook_key = (first_hook[0], first_hook[1])
                closure_key = (first_closure[0], first_closure[1])
                scene_order = "positive" if closure_key < hook_key else "negative"
            elif first_hook is not None:
                scene_order = "hook_only"
            elif first_closure is not None and first_closure[0] >= max(1, (2 * len(scenes)) // 3):
                scene_order = "closure_only"

    architecture_units: list[str] = []
    if isinstance(architecture, dict):
        sequences = architecture.get("sequences")
        if isinstance(sequences, list) and sequences:
            architecture_units.append(_text(sequences[-1]).lower())
        if architecture.get("ending_payoff"):
            architecture_units.append(_text(architecture.get("ending_payoff")).lower())
    architecture_states = [explicit_order(unit) if explicit_order(unit) != "neutral" else closure_order(unit) for unit in architecture_units]
    architecture_positive = "positive" in architecture_states
    architecture_negative = "negative" in architecture_states
    if len(architecture_states) >= 2:
        payoff_recap_hook = bool(architecture_units and re.search(r"new mission|top-level mission|return to the team|sequel hook|next mission|ordered to|called away", architecture_units[-1]) and re.search(r"recap|previously|earlier|had already|before the finale|before the final|before the closure|before she resolves|before he resolves", architecture_units[-1]))
        if payoff_recap_hook:
            architecture_negative = True
        elif architecture_states[0] == "closure_only" and architecture_states[-1] == "hook_only":
            architecture_positive = True
        if architecture_states[0] == "hook_only" and architecture_states[-1] == "closure_only":
            architecture_negative = True
    architecture_has_closure = any(state in {"positive", "closure_only"} for state in architecture_states)
    architecture_has_hook = any(state in {"positive", "negative", "hook_only"} for state in architecture_states)

    ending_payoff_text = _text(architecture.get("ending_payoff", "")).lower() if isinstance(architecture, dict) else ""
    unresolved_original = False
    for payoff_line in ending_payoff_text.splitlines():
        for segment in re.split(r"[.!?;]", payoff_line):
            if not re.search(r"unresolved|remains open|no closure", segment):
                continue
            sequel_context = bool(re.search(r"new mission|next mission|new case|next case|fresh case|sequel hook|another city|ordered to|called away", segment))
            original_marker = bool(re.search(r"\boriginal\b|\bmain\b|\bcentral\b|\bcore\b|\bcurrent\b", segment))
            object_marker = bool(re.search(r"conspiracy|conflict|case|mystery|original wound", segment))
            if original_marker or (object_marker and not sequel_context):
                unresolved_original = True
                break
    explicit_unresolved = unresolved_original
    if explicit_unresolved:
        closure_before_hook = False
    elif scene_order == "positive":
        closure_before_hook = True
    elif scene_order == "negative":
        closure_before_hook = False
    elif architecture_negative:
        closure_before_hook = False
    elif scene_order == "hook_only" and architecture_has_closure:
        scene_text_joined = " ".join(scene_texts) if scenes else ""
        explicit_sequel_excerpt = len(scenes) == 1 and bool(re.search(r"sequel excerpt|sequel scene|after the main case|following the closure", scene_text_joined))
        closure_before_hook = explicit_sequel_excerpt
    elif architecture_positive:
        closure_before_hook = True
    elif scene_order == "closure_only" and not architecture_has_hook:
        closure_before_hook = True
    elif architecture_has_closure and not architecture_has_hook and scene_order != "hook_only":
        closure_before_hook = True
    else:
        closure_before_hook = False

    checks = {
        "intimate_public_violation": bool(re.search(r"diary|private|read aloud|publicly humiliat|bully|bullied|shame|mock|debt collector|threaten|frame|false accusation", full)),
        "care_or_family_economic_anchor": bool(re.search(r"mother|father|brother|sister|family|child", full) and re.search(r"care|warmth|sacrifice|gave up|hospital|medical|debt|unpaid|protect|save|meal|home", full)),
        "hidden_competence_is_proven_early": bool(re.search(r"race|fight|win|evidence|skill|competence|defeat|solve|prove|demonstrate|counterattack", opening)),
        "distinct_competence_domains": _count_any(full, competence_domains) >= 3,
        "institutional_arena_rotation": _count_any(full, arenas) >= 4,
        "ethical_loyalty_test": bool(re.search(r"abandon|comrade|loyal|share risk|stay behind|protect subordinate|won.?t leave|no one leaves|shield|save.*team|not abandon", full)),
        "provenance_and_procedural_accountability": bool(re.search(r"prize money|clean money|source of money|evidence|video|records|investigation|police|law|judge|court|according to law|public apology", full)),
        "ally_supports_without_owning_revenge": bool(re.search(r"support|stand with|help|ally|partner|not alone|won.?t let.*alone|respect|choice|let her|she decides|without taking over", full)),
        "romance_or_intimacy_respects_refusal": not any(_has_coercive_intimacy(unit) for unit in _artifact_units(premise, architecture, scenes)),
        "closure_before_mission_hook": closure_before_hook,
    }
    labels = {
        "intimate_public_violation": "competence-cascade revenge lacks a specific intimate/public violation that creates moral debt",
        "care_or_family_economic_anchor": "hidden mastery is not anchored in care, family, economic sacrifice, or protection before power display",
        "hidden_competence_is_proven_early": "hidden competence is asserted but not proven early through a legible outcome",
        "distinct_competence_domains": "competence repeats one proof type instead of cascading across distinct domains",
        "institutional_arena_rotation": "long-form escalation does not rotate enough institutional arenas to renew the power test",
        "ethical_loyalty_test": "power is never ethically tested through loyalty, shared risk, or refusal to abandon vulnerable people",
        "provenance_and_procedural_accountability": "money/power/revenge lacks provenance, evidence, or procedural accountability",
        "ally_supports_without_owning_revenge": "ally support risks owning or replacing the victim/protagonist's authored revenge",
        "romance_or_intimacy_respects_refusal": "romance or intimacy contains coercive refusal-overriding language/framing",
        "closure_before_mission_hook": "the sequel/next-mission hook arrives before justice, family, identity, or belonging closure",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Hidden-mastery revenge sustains long runtime when an intimate wound and care anchor lead to early proof, distinct competence domains, rotating institutions, ethical loyalty tests, accountable evidence/procedure, non-owning allies, explicit consent, and closure before any sequel mission hook.",
    }
