"""Reference-informed thumbnail concept generation and critique.

The system learns visual mechanics from reference thumbnails. It must not copy the images.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def classify_reference(row: dict[str, Any]) -> str:
    text = ((row.get("title") or "") + " " + (row.get("exact_title") or "") + " " + (row.get("archive_title") or "")).lower()
    if any(k in text for k in ("sinbad", "aladdin", "odyssey", "jason", "argonaut", "voyage", "arabian")):
        return "mythic_adventure"
    if any(k in text for k in ("reborn", "beautiful", "reincarnated")):
        return "transformation_rebirth"
    if any(k in text for k in ("dragon", "wolf", "mermaid", "monster", "beast", "pet")):
        return "creature_power_bond"
    if any(k in text for k in ("divorce", "wife", "husband", "bride", "wedding", "married", "fiancé", "fiance")):
        return "romantic_family_betrayal"
    if any(k in text for k in ("planet", "sci-fi", "war", "pilot", "air force")):
        return "science_fiction_spectacle"
    if any(k in text for k in ("orc", "demon", "hunter")):
        return "dark_creature_threat"
    if any(k in text for k in ("saas", "bahu", "ghareeb", "humsafar", "aseer")):
        return "localized_family_melodrama"
    return "general_emotional_drama"


def load_index(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def reference_library(index_paths: list[Path]) -> dict[str, list[dict[str, Any]]]:
    library: dict[str, list[dict[str, Any]]] = {}
    for path in index_paths:
        for row in load_index(path):
            category = classify_reference(row)
            row["reference_category"] = category
            library.setdefault(category, []).append(row)
    return library


def generate_concepts(premise: dict[str, Any], library: dict[str, list[dict[str, Any]]] | None = None) -> list[dict[str, Any]]:
    """Generate original thumbnail concepts from story mechanics.

    Expected premise keys are intentionally flexible: title/working_title, genre, wound,
    transformation, creature_or_child_anchor, protector, betrayal, setting, and emotional_promise.
    """
    title = premise.get("title") or premise.get("working_title") or "Untitled"
    genre = (premise.get("genre") or "emotional fantasy drama").lower()
    creature = premise.get("creature_or_child_anchor") or premise.get("child_anchor") or ""
    transformation = premise.get("transformation") or ""
    protector = premise.get("protector") or ""
    wound = premise.get("wound") or "visible injustice"
    promise = premise.get("emotional_promise") or "reversal and belonging"

    concepts: list[dict[str, Any]] = []
    if creature or any(k in genre for k in ("fantasy", "dragon", "wolf", "mermaid")):
        concepts.append({
            "concept_id": "vulnerable_bond_scale",
            "category": "creature_power_bond",
            "core_mechanic": "small vulnerable being in front, protector/power presence looming behind",
            "composition": "protagonist and vulnerable creature/child occupy the lower-center third; protector or transformed creature fills the upper/background third; eyes or energy connect them",
            "emotion": "fear turning into trust; protector intensity without sexualized coercion",
            "palette": "warm gold/cyan or warm gold/ice-blue contrast; luminous subject separation from darker background",
            "text_direction": "short concrete promise, 2–5 words maximum if text is used; do not restate a long title",
            "mobile_test": "at 160px wide, viewer must still identify the small creature/child, protagonist emotion, and protector silhouette",
            "reference_categories_to_study": ["creature_power_bond"],
        })
    if transformation or "rebirth" in genre or "beauty" in title.lower():
        concepts.append({
            "concept_id": "transformation_split",
            "category": "transformation_rebirth",
            "core_mechanic": "before/after or wound/power contrast in one instantly readable frame",
            "composition": "protagonist split across an asymmetrical diagonal or central mirror axis; wounded version smaller/less polished, transformed version dominant but still emotionally expressive",
            "emotion": "shame becoming agency, not empty glamour",
            "palette": "high-key clean background with one saturated accent; avoid muddy midtones",
            "text_direction": "one transformation word or short reversal phrase; avoid clutter",
            "mobile_test": "before/after difference must remain visible at feed size",
            "reference_categories_to_study": ["transformation_rebirth"],
        })
    if any(k in genre for k in ("romance", "family", "drama", "modern")) or premise.get("betrayal"):
        concepts.append({
            "concept_id": "relational_pressure_triangle",
            "category": "romantic_family_betrayal",
            "core_mechanic": "two or three people arranged so loyalty, betrayal, or protection is readable before any text",
            "composition": "vulnerable protagonist largest or most emotionally exposed; betrayer/protector positioned behind or opposite; use eyelines and distance rather than random crowd clutter",
            "emotion": "hurt, suspicion, longing, defiance, or protective resolve",
            "palette": "warm intimate skin tones against cooler social environment; luxury can frame status conflict",
            "text_direction": "title-thumbnail division of labor: title carries plot twist, thumbnail carries emotion/relationship",
            "mobile_test": "viewer can identify who is hurt, who has power, and what relationship tension matters",
            "reference_categories_to_study": ["romantic_family_betrayal", "localized_family_melodrama"],
        })
    contract = (premise.get("channel_contract") or "").lower()
    if contract == "mythic_adventure":
        concepts.append({
            "concept_id": "mythic_survival_scale",
            "category": "mythic_adventure",
            "core_mechanic": "recognizable mythic environment plus bodily survival threat",
            "composition": "small human figure or emotionally readable hero against a giant creature/environment; danger must be physically legible rather than abstract lore",
            "emotion": "awe mixed with immediate survival fear",
            "palette": "golden mythic warmth against deep blue/green danger",
            "text_direction": "use familiar mythic name or voyage promise if available; avoid invented lore terms",
            "mobile_test": "giant-vs-human scale contrast and hero expression survive shrinkage",
            "reference_categories_to_study": ["mythic_adventure", "creature_power_bond"],
        })
    if contract == "serialized_creature_franchise":
        concepts.append({
            "concept_id": "arena_monster_injustice",
            "category": "serialized_creature_franchise",
            "core_mechanic": "enslaved or hunted protagonist facing monster/power system with completion value",
            "composition": "protagonist and creature in direct confrontation; crowd/power figures pushed to background; packaging should communicate complete arc or season value",
            "emotion": "bodily vulnerability plus defiant survival",
            "palette": "dirty arena earth tones pierced by creature glow or blood-red power accents",
            "text_direction": "favor complete/season/movie language over episode-number-first fragmentation",
            "mobile_test": "viewer must read who is trapped and what monster/power threatens them",
            "reference_categories_to_study": ["creature_power_bond", "dark_creature_threat"],
        })
    if contract == "korean_niche_microdrama":
        concepts.append({
            "concept_id": "niche_face_tension",
            "category": "korean_niche_microdrama",
            "core_mechanic": "large attractive faces carrying niche relational tension, secrecy, regression, or power imbalance",
            "composition": "one or two faces dominate the frame; object/trope cue (pendant, uniform, crown, contract, phone) small but readable",
            "emotion": "yearning, suspicion, control, betrayal, or forbidden intimacy",
            "palette": "clean glossy beauty lighting with one saturated trope accent",
            "text_direction": "short trope declaration or intimate confrontation phrase; subtitles/title carry specifics",
            "mobile_test": "eye contact and trope object remain readable at vertical feed size",
            "reference_categories_to_study": ["romantic_family_betrayal", "general_emotional_drama"],
        })
    if not concepts:
        concepts.append({
            "concept_id": "single_question_closeup",
            "category": "general_emotional_drama",
            "core_mechanic": "one dominant emotional face plus one object or silhouetted threat that creates the central question",
            "composition": "face on one vertical third, object/threat on the opposite third, clean negative space for optional text",
            "emotion": "the exact wound or moral pressure of the premise",
            "palette": "controlled two-color contrast with one warm emotional accent",
            "text_direction": "no more than one short curiosity phrase",
            "mobile_test": "face expression and object meaning survive shrinkage",
            "reference_categories_to_study": ["general_emotional_drama"],
        })
    for concept in concepts:
        concept["source_promise"] = promise
        concept["source_wound"] = wound
        concept["protector"] = protector
        concept["do_not_copy"] = "Use reference images only for mechanics: hierarchy, contrast, emotion, and readability. Generate original characters, layout, typography, and world details."
    return concepts


def critique_concept(concept: dict[str, Any]) -> dict[str, Any]:
    """Transparent heuristic critique for a proposed thumbnail concept."""
    strengths = []
    risks = []
    comp = (concept.get("composition") or "").lower()
    emotion = (concept.get("emotion") or "").lower()
    palette = (concept.get("palette") or "").lower()
    text = (concept.get("text_direction") or "").lower()
    if any(k in comp for k in ("center", "third", "dominant", "protagonist")):
        strengths.append("clear focal hierarchy")
    else:
        risks.append("focal hierarchy underspecified")
    if any(k in emotion for k in ("fear", "trust", "hurt", "shame", "longing", "defiance", "resolve", "tenderness")):
        strengths.append("specific emotion")
    else:
        risks.append("emotion too generic")
    if any(k in palette for k in ("contrast", "warm", "cyan", "gold", "high-key")):
        strengths.append("controlled color contrast")
    if "2–5" in text or "short" in text or "one " in text:
        strengths.append("text restraint")
    else:
        risks.append("possible text clutter")
    if any(k in comp for k in ("crowd", "many", "ensemble")):
        risks.append("crowd complexity may reduce mobile readability")
    if any(k in emotion for k in ("empty glamour", "generic")):
        risks.append("emotion may not carry story promise")
    score = 0.45 + 0.12 * len(strengths) - 0.09 * len(risks)
    return {
        "score_0_to_1": max(0.0, min(1.0, score)),
        "strengths": strengths,
        "risks": risks,
        "required_mobile_check": concept.get("mobile_test", "inspect at actual feed size"),
        "ctr_caveat": "This is a design-quality critique, not a CTR prediction. Validate with YouTube Test & Compare when available.",
    }
