"""Production artifact validation and pre-greenlight quality gates."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .failure_intelligence import evaluate_candidate
from .format_strategy import format_strategy
from .channel_contracts import evaluate_channel_fit

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_artifact(path: Path, schema_name: str) -> list[str]:
    schema = load_json(SCHEMA_DIR / schema_name)
    artifact = load_json(path)
    validator = Draft202012Validator(schema)
    return ["/".join(str(p) for p in error.absolute_path) + ": " + error.message for error in sorted(validator.iter_errors(artifact), key=lambda e: list(e.absolute_path))]


def load_scenes(path: Path | None) -> tuple[list[dict[str, Any]], list[str]]:
    if path is None:
        return [], []
    errors: list[str] = []
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]
    scenes: list[dict[str, Any]] = []
    schema = load_json(SCHEMA_DIR / "scene-screenplay.schema.json")
    validator = Draft202012Validator(schema)
    for file in files:
        data = load_json(file)
        candidates = data if isinstance(data, list) else [data]
        for scene in candidates:
            scene_errors = ["/".join(str(p) for p in e.absolute_path) + ": " + e.message for e in validator.iter_errors(scene)]
            if scene_errors:
                errors.extend(f"{file.name}: {error}" for error in scene_errors)
            scenes.append(scene)
    return scenes, errors


def minutes_range(value: str) -> tuple[float, float] | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)", value)
    if not match:
        return None
    return float(match.group(1)), float(match.group(2))


def scene_quality(scenes: list[dict[str, Any]]) -> dict[str, Any]:
    missing: dict[str, list[str]] = {
        "power_change": [],
        "protagonist_decision": [],
        "failure_checks": [],
        "negative_space_sound": [],
    }
    ranges: list[tuple[float, float, str]] = []
    for scene in scenes:
        sid = scene.get("scene_id", "<missing>")
        if scene.get("power_position_start") == scene.get("power_position_end"):
            missing["power_change"].append(sid)
        if not scene.get("protagonist_decision"):
            missing["protagonist_decision"].append(sid)
        if len(scene.get("failure_checks", [])) < 2:
            missing["failure_checks"].append(sid)
        sound = scene.get("sound_design", {})
        if not sound.get("silence_or_negative_space"):
            missing["negative_space_sound"].append(sid)
        parsed = minutes_range(str(scene.get("time_range", "")))
        if parsed:
            ranges.append((parsed[0], parsed[1], sid))
    ranges.sort()
    overlaps = []
    for previous, current in zip(ranges, ranges[1:]):
        if current[0] < previous[1]:
            overlaps.append(f"{previous[2]} overlaps {current[2]}")
    covered = sum(end - start for start, end, _ in ranges)
    return {
        "scene_count": len(scenes),
        "covered_minutes_estimate": round(covered, 2),
        "missing": missing,
        "time_overlaps": overlaps,
    }


def architecture_quality(architecture: dict[str, Any]) -> dict[str, Any]:
    sequences = architecture.get("sequences", [])
    warnings: list[str] = []
    if architecture.get("target_minutes") and len(sequences) < max(8, int(architecture["target_minutes"] / 10)):
        warnings.append("sequence density may be too low for target duration")
    repeated_turns = len({s.get("turn", "").strip().lower() for s in sequences}) < len(sequences)
    if repeated_turns:
        warnings.append("some sequence turns repeat exactly; verify that escalation is not repetitive")
    missing_capability = [str(s.get("sequence")) for s in sequences if not s.get("new_capability_or_clue") and not s.get("ally_or_relationship_change") and not s.get("secret_reveal_escalation")]
    if missing_capability:
        warnings.append("sequences without capability/clue/relationship/secret progression: " + ", ".join(missing_capability))
    return {"sequence_count": len(sequences), "warnings": warnings}


def flatten_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(flatten_text(v) for v in value.values())
    if isinstance(value, list):
        return "\n".join(flatten_text(v) for v in value)
    return ""


def gate_report(schema_errors: dict[str, list[str]], failure: dict[str, Any], scenes: dict[str, Any], architecture: dict[str, Any]) -> dict[str, Any]:
    return {
        "A_premise": "pass" if not schema_errors.get("premise") and failure["risk_score_0_to_1"] < 0.5 else "attention",
        "B_architecture": "pass" if not schema_errors.get("architecture") and not architecture.get("warnings") else "attention",
        "C_screenplay": "pass" if not schema_errors.get("scenes") and not any(scenes.get("missing", {}).values()) else "attention",
        "D_direction_storyboard": "unknown_until_storyboard_frames_exist",
        "E_production": "unknown_until_generated_media_exists",
        "F_release_learning": "unknown_until_release_metadata_exists",
    }


def evaluate_project(premise_path: Path, architecture_path: Path | None, scenes_path: Path | None, archive_rows: list[dict[str, Any]]) -> dict[str, Any]:
    schema_errors: dict[str, list[str]] = {"premise": validate_artifact(premise_path, "premise-packet.schema.json")}
    premise = load_json(premise_path)
    architecture = load_json(architecture_path) if architecture_path else {}
    if architecture_path:
        schema_errors["architecture"] = validate_artifact(architecture_path, "story-architecture.schema.json")
    scenes, scene_errors = load_scenes(scenes_path)
    schema_errors["scenes"] = scene_errors
    combined = "\n".join([flatten_text(premise), flatten_text(architecture), flatten_text(scenes)])
    candidate = premise.get("title_candidates", [premise.get("premise_id", "untitled")])[0]
    failure = evaluate_candidate(candidate, archive_rows, combined)
    scene_report = scene_quality(scenes)
    architecture_report = architecture_quality(architecture)
    return {
        "premise_id": premise.get("premise_id"),
        "schema_errors": schema_errors,
        "failure_intelligence": failure,
        "scene_quality": scene_report,
        "architecture_quality": architecture_report,
        "format_strategy": format_strategy(premise.get("target_minutes"), combined, premise.get("release_format", "")),
        "channel_contract_fit": evaluate_channel_fit(combined, premise.get("channel_contract", "")),
        "gates": gate_report(schema_errors, failure, scene_report, architecture_report),
    }
