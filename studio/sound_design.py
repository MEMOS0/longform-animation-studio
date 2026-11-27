"""Sound-design quality gates for long-form animated films."""
from __future__ import annotations

from typing import Any

REQUIRED_KEYS = ["dialogue_priority", "music_function", "silence_or_negative_space", "motif"]
WEAK_TERMS = ["constant music", "wallpaper", "loud throughout", "generic epic"]
GENERIC_MOTIFS = {"a restrained tactile sound motif", "restrained tactile motif", "sound motif"}
SOUND_SOURCE_TERMS = ["breath", "water", "fire", "paper", "stone", "metal", "glass", "cloth", "footstep", "chain", "coin", "crowd", "labor", "wind", "rain", "creature", "wing", "fin", "oven", "pump", "heartbeat", "room tone", "ledger", "object", "witness", "measurement", "scratch", "whisper", "repair", "mechanic", "murmur", "assembly"]
MUSICAL_STRUCTURE_TERMS = ["note", "melody", "chord", "theme", "instrument", "motif", "harmony", "rhythm"]


def evaluate_sound_design(scenes: list[dict[str, Any]]) -> dict[str, Any]:
    scene_reports = []
    warnings = []
    strengths = []
    for scene in scenes:
        sid = scene.get("scene_id", "scene")
        sound = scene.get("sound_design", {})
        missing = [key for key in REQUIRED_KEYS if not sound.get(key)]
        joined = " ".join(str(sound.get(k, "")) for k in REQUIRED_KEYS).lower()
        scene_warnings = [f"{sid}: missing {key}" for key in missing]
        if missing:
            scene_warnings.append(f"{sid}: sound design is not yet production-actionable")
        negated = any(marker in joined for marker in ("rather than", "not constant", "no constant", "avoid constant", "instead of constant"))
        if any(term in joined for term in WEAK_TERMS) and not negated:
            scene_warnings.append(f"{sid}: music/sound described as constant or generic rather than structural")
        motif_text = str(sound.get("motif", "")).strip().lower()
        negative_text = str(sound.get("silence_or_negative_space", "")).lower()
        if motif_text in GENERIC_MOTIFS:
            scene_warnings.append(f"{sid}: motif is generic; tie it to object, creature, labor, or environment materials")
        elif motif_text and not any(term in motif_text for term in SOUND_SOURCE_TERMS) and not any(term in motif_text for term in MUSICAL_STRUCTURE_TERMS):
            scene_warnings.append(f"{sid}: motif lacks concrete sound-source materials")
        if negative_text and not any(term in negative_text for term in SOUND_SOURCE_TERMS + ["silence", "drop", "thin"]):
            scene_warnings.append(f"{sid}: negative space is abstract rather than a audible transition")
        if "silence" in joined or "drop" in joined or "negative space" in joined:
            strengths.append(f"{sid}: uses silence/negative space as an emotional transition")
        if "dialogue" in joined and "intelligible" in joined:
            strengths.append(f"{sid}: dialogue intelligibility is explicit")
        if "motif" in joined and any(term in joined for term in ("evolve", "answer", "fragment", "return")):
            strengths.append(f"{sid}: motif has narrative evolution rather than wallpaper repetition")
        scene_reports.append({"scene_id": sid, "warnings": scene_warnings, "sound_design_keys_present": sorted(sound.keys())})
        warnings.extend(scene_warnings)
    score = 1.0 if scenes else 0.0
    if scenes:
        score = max(0.0, 1.0 - len(warnings) / max(1, len(scenes) * 2))
    return {"score_0_to_1": round(score, 2), "scene_reports": scene_reports, "warnings": warnings, "strengths": sorted(set(strengths)), "craft_rule": "Sound must mark power transitions: dialogue clarity first, motif evolution second, silence/negative space before bonding or revelation."}
