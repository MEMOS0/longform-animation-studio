"""Generate non-uniform exact-format director-seed storyboards from scene units.

These boards are pre-director scaffolds, not production-final boards. Their value
is exact continuity: every second is allocated, every beat has sound/camera/lane
intent, and pacing is deliberately varied before a human/agent director refines
staging and dialogue shot by shot.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

BEATS = [
    ("wide establishing", "slow push", "first_image", "", "negative_space", "hero", 1.20, "open on the scene image"),
    ("intimate closeup", "settle", "face_reaction", "", "breath/room tone", "mid", 0.72, "read emotion before exposition"),
    ("action wide", "lateral track", "objective", "", "environmental action foley", "draft", 0.95, "objective as visible movement"),
    ("power two-shot", "slow tightening", "conflict", "key0", "dialogue first", "mid", 1.12, "conflict through voices and positions"),
    ("pressure insert", "macro", "conflict", "", "object/room texture", "draft", 0.62, "insert pressure detail"),
    ("decision closeup", "static intimate", "protagonist_decision", "key1", "music drops before decision", "mid", 0.82, "decision must be visible"),
    ("turn wide", "reframe", "turn", "", "sound motif shifts", "hero", 1.34, "power turn in space"),
    ("vertical composition", "high or low angle", "vertical_composition", "", "negative space", "draft", 0.78, "spatial power relationship"),
    ("subtext two-shot", "slow lateral drift", "subtext", "key2", "sparse motif", "mid", 1.05, "subtext not explanation"),
    ("consequence wide", "backward track", "consequence", "", "consequence foley", "draft", 0.92, "cost becomes physical"),
    ("sensory bridge", "insert or detail", "final_image", "", "object/motif texture", "draft", 0.58, "sensory transition"),
    ("final image", "slow pull-back", "final_image", "key0", "motif unresolved", "hero", 1.46, "exit on changed power"),
]


def minutes_range(value: str) -> tuple[float, float]:
    match = re.search(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)", value or "")
    return (float(match.group(1)), float(match.group(2))) if match else (0.0, 5.0)


def distribute_duration(weights: list[float], total: float, minimum: float = 4.0, maximum: float = 32.0) -> list[float]:
    raw = [total * weight / sum(weights) for weight in weights]
    durations = [min(max(v, minimum), maximum) for v in raw]
    for _ in range(50):
        diff = total - sum(durations)
        if abs(diff) < 0.01:
            break
        adjustable = [i for i, v in enumerate(durations) if (v < maximum if diff > 0 else v > minimum)]
        if not adjustable:
            break
        step = diff / len(adjustable)
        for i in adjustable:
            durations[i] = min(max(durations[i] + step, minimum), maximum)
    correction = total - sum(durations)
    durations[-1] += correction
    return durations


def scene_value(scene: dict[str, Any], key: str) -> str:
    visual = scene.get("visual_action", {})
    if key in visual:
        return str(visual.get(key) or "")
    if key == "consequence":
        return "visible consequence of " + str(scene.get("protagonist_decision") or "the decision")
    return str(scene.get(key) or "")


def build_seed_board(scene: dict[str, Any], continuity_dependencies: list[str] | None = None) -> dict[str, Any]:
    start, end = minutes_range(str(scene.get("time_range", "")))
    duration = round((end - start) * 60.0, 2)
    shot_count = max(12, min(22, round(duration / 18)))
    keys = list((scene.get("dialogue_design") or {}).get("key_lines") or []) + ["", "", ""]
    selected = [BEATS[round(i * (len(BEATS) - 1) / max(1, shot_count - 1))] for i in range(shot_count)]
    durations = distribute_duration([beat[6] for beat in selected], duration)
    sound = scene.get("sound_design") or {}
    shots: list[dict[str, Any]] = []
    cursor = 0.0
    for i, (beat, shot_duration) in enumerate(zip(selected, durations), start=1):
        shot_end = cursor + shot_duration
        if i == shot_count:
            shot_end = duration
        size, camera, source, dialogue_key, sound_key, lane, _weight, note = beat
        dialogue = ""
        if dialogue_key:
            dialogue = keys[int(dialogue_key[-1])] if len(keys) > int(dialogue_key[-1]) else ""
        sound_text = {
            "negative_space": sound.get("silence_or_negative_space", "ambient negative space"),
            "dialogue first": sound.get("dialogue_priority", "dialogue first"),
            "sparse motif": sound.get("music_function", "sparse motif"),
            "motif unresolved": str(sound.get("motif", "motif")) + " unresolved",
        }.get(sound_key, sound_key)
        shots.append({
            "shot_id": f"{scene.get('scene_id', 'SXX')}_DS{i:03d}",
            "timecode": f"{cursor:.2f}-{shot_end:.2f}",
            "duration_seconds": round(shot_end - cursor, 2),
            "scene_id": scene.get("scene_id", "SXX"),
            "shot_size": size,
            "camera_intent": camera,
            "visual_action": scene_value(scene, source),
            "dialogue": dialogue,
            "sound_design": sound_text,
            "generation_lane": lane,
            "continuity_dependencies": continuity_dependencies or ["protagonist_face_costume", "location_geography", "relationship_continuity", "meaning_carrier_continuity", "sound_motif_continuity"],
            "director_note": "director seed generated from exact scene fields; refine staging before production: " + note,
        })
        cursor = shot_end
    return {
        "scene_id": scene.get("scene_id", "SXX"),
        "duration_seconds": duration,
        "coverage": "continuous_exact_format_director_seed",
        "shots": shots,
        "validation_rules": ["seed must be manually/directorially refined before production", "no gaps or overlaps", "sound and power transitions must remain explicit", "shot pacing must remain intentionally varied"],
    }


def write_seed_boards(scenes_dir: Path, output_dir: Path, continuity_dependencies: list[str] | None = None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(scenes_dir.glob("S*.json")):
        scene = json.loads(path.read_text(encoding="utf-8"))
        board = build_seed_board(scene, continuity_dependencies)
        out = output_dir / f"{scene.get('scene_id', path.stem)}_storyboard.json"
        out.write_text(json.dumps(board, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rows.append({"scene_id": scene.get("scene_id"), "path": str(out), "shot_count": len(board["shots"]), "duration_seconds": board["duration_seconds"]})
    return {"scene_count": len(rows), "boards": rows}
