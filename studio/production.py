"""Production artifact validation and pre-greenlight quality gates."""
from __future__ import annotations

import json
import re
import importlib.resources
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .failure_intelligence import evaluate_candidate
from .format_strategy import format_strategy, premise_text_for_format_inference
from .channel_contracts import evaluate_channel_fit
from .production_economics import estimate_video_budget
from .shot_pipeline import build_shot_plan
from .title_intelligence import critique_title, generate_title_candidates
from .dialogue_craft import evaluate_scenes_dialogue
from .agency_intelligence import evaluate_agency
from .sound_design import evaluate_sound_design
from .meaning_carrier import evaluate_meaning_carrier
from .relational_contract import evaluate_relational_contract
from .spatial_status import evaluate_spatial_status
from .closure_integrity import evaluate_closure_integrity
from .compressed_survival_integrity import evaluate_compressed_survival_integrity
from .transformation_romance_integrity import evaluate_transformation_romance_integrity
from .compound_expansion import evaluate_compound_expansion_readiness
from .creature_pacing import evaluate_creature_pacing
from .romance_deception_integrity import evaluate_romance_deception_integrity
from .zero_to_hero_integrity import evaluate_zero_to_hero_integrity
from .prohibition_scifi_integrity import evaluate_prohibition_scifi_integrity
from .family_exit_integrity import evaluate_family_exit_integrity
from .animal_guise_consent import evaluate_animal_guise_consent
from .visual_causality import evaluate_visual_causality
from .hidden_identity_integrity import evaluate_hidden_identity_integrity
from .scale_community_integrity import evaluate_scale_community_integrity
from .thumbnail_concepts import generate_concepts, critique_concept
from .storyboard import validate_storyboard_file

REPO_SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"
SCHEMA_DIR = REPO_SCHEMA_DIR if REPO_SCHEMA_DIR.exists() else importlib.resources.files("studio") / "package_data" / "schemas"


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


def load_storyboards(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    files = sorted(path.glob("*_storyboard.json")) if path.is_dir() else [path]
    boards: dict[str, dict[str, Any]] = {}
    for file in files:
        try:
            data = load_json(file)
            validation = validate_storyboard_file(file)
        except Exception as exc:  # malformed artifact should be reported, not crash evaluation
            data = {"scene_id": file.stem.replace("_storyboard", ""), "duration_seconds": 0}
            validation = {"valid": False, "errors": [str(exc)], "warnings": []}
        boards[str(data.get("scene_id") or file.stem.replace("_storyboard", ""))] = {"path": str(file), "data": data, "validation": validation}
    return boards


def storyboard_coverage(scenes: list[dict[str, Any]], boards: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows = []
    missing = []
    invalid = []
    duration_mismatch = []
    for scene in scenes:
        sid = str(scene.get("scene_id") or "")
        board = boards.get(sid)
        if not board:
            missing.append(sid)
            continue
        validation = board["validation"]
        expected = None
        parsed = minutes_range(str(scene.get("time_range", "")))
        if parsed:
            expected = round((parsed[1] - parsed[0]) * 60.0, 2)
        actual = round(float(board["data"].get("duration_seconds") or 0), 2)
        if validation.get("errors"):
            invalid.append(sid)
        if expected is not None and abs(actual - expected) > 0.5:
            duration_mismatch.append({"scene_id": sid, "expected_seconds": expected, "actual_seconds": actual})
        rows.append({"scene_id": sid, "expected_seconds": expected, "actual_seconds": actual, "valid": validation.get("valid"), "warnings": validation.get("warnings", []), "shot_count": validation.get("shot_count", 0)})
    complete = bool(scenes) and not missing and not invalid and not duration_mismatch
    warnings = []
    if missing:
        warnings.append("missing exact storyboards for scenes: " + ", ".join(missing))
    if invalid:
        warnings.append("invalid exact storyboards for scenes: " + ", ".join(invalid))
    if duration_mismatch:
        warnings.append("storyboard duration mismatch for scenes: " + ", ".join(row["scene_id"] for row in duration_mismatch))
    return {"complete_exact_coverage": complete, "rows": rows, "missing": missing, "invalid": invalid, "duration_mismatch": duration_mismatch, "warnings": warnings}


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
    required_fields = ["turn", "protagonist_choice", "emotional_shift", "visual_setpiece", "sound_design_intent", "retention_hook"]
    for seq in sequences:
        missing = [field for field in required_fields if not seq.get(field)]
        if missing:
            warnings.append(f"sequence {seq.get('sequence')}: missing retention architecture fields: {', '.join(missing)}")
    cursor = 0.0
    coverage_gaps = []
    for seq in sequences:
        match = re.search(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)", str(seq.get("time_range", "")))
        if not match:
            warnings.append(f"sequence {seq.get('sequence')}: missing parseable time_range")
            continue
        start, end = float(match.group(1)), float(match.group(2))
        if abs(start - cursor) > 0.05:
            coverage_gaps.append(f"sequence {seq.get('sequence')}: expected start {cursor:g}, got {start:g}")
        if end <= start:
            warnings.append(f"sequence {seq.get('sequence')}: non-positive duration")
        elif end - start > 8:
            warnings.append(f"sequence {seq.get('sequence')}: longer than 8 minutes without a new sequence-level turn")
        cursor = end
    warnings.extend(coverage_gaps)
    target = architecture.get("target_minutes")
    if target and sequences and abs(cursor - float(target)) > 0.5:
        warnings.append(f"sequence coverage ends at {cursor:g} minutes, target is {target}")
    return {"sequence_count": len(sequences), "coverage_end_minutes": cursor, "warnings": warnings}


def flatten_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(flatten_text(v) for v in value.values())
    if isinstance(value, list):
        return "\n".join(flatten_text(v) for v in value)
    return ""


def opening_conversion_quality(premise: dict[str, Any]) -> dict[str, Any]:
    opening = premise.get("opening_event", {})
    text = " ".join(str(opening.get(key, "")) for key in ("first_10_seconds", "first_60_seconds", "first_5_minutes", "dramatic_question")).lower()
    groups = {
        "wound_or_vulnerability": ["wound", "hurt", "shame", "fear", "afraid", "abandon", "loss", "vulnerable", "child", "creature", "bully", "threat", "betray", "captive", "poor", "ugly", "hidden", "mock"],
        "protective_counterforce": ["protect", "shield", "save", "help", "care", "mother", "father", "ally", "companion", "bond", "rescue", "defend", "shelter", "choose"],
        "antagonistic_pressure": ["bully", "hunter", "king", "villain", "rival", "threat", "attack", "mob", "guards", "police", "society", "family", "husband", "wife", "army", "soldier", "admiral", "hunter", "enemy", "corporation", "crown"],
        "progression_or_payoff_promise": ["transform", "reveal", "escape", "justice", "belonging", "public", "restore", "secret", "power", "choice", "truth", "identity", "payoff", "expose", "proving", "cost", "danger"],
    }
    matched = {name: [term for term in terms if term in text] for name, terms in groups.items()}
    present = [name for name, hits in matched.items() if hits]
    warnings: list[str] = []
    if len(present) < 3:
        warnings.append("opening hook does not yet convert into a legible emotional system across wound/protection/pressure/payoff")
    admin_terms = ["verify", "prove", "proof", "record", "file", "contract", "inspect", "investigate", "documents", "records"]
    emotional_terms = sum(len(matched[name]) for name in ("wound_or_vulnerability", "protective_counterforce", "antagonistic_pressure"))
    admin_hits = [term for term in admin_terms if term in text]
    if len(admin_hits) >= 2 and emotional_terms < 4:
        warnings.append("opening may stall in proof/verification/administrative negotiation instead of escalating injustice or protection")
    ordinary_anchor_terms = ["water", "well", "food", "bread", "potato", "debt", "rent", "wage", "work", "chore", "home", "shop", "oven", "mill", "bucket", "pump", "shelter", "animal", "beast", "customer", "door"]
    ordinary_hits = [term for term in ordinary_anchor_terms if re.search(r"\b" + re.escape(term) + r"\b", text)]
    fantasyish = any(term in ((premise.get("channel_contract") or "") + " " + (premise.get("genre") or "") + " " + " ".join(premise.get("title_candidates") or [])).lower() for term in ("fantasy", "creature", "dragon", "monster", "mythic", "dark", "magic"))
    if fantasyish and not ordinary_hits:
        warnings.append("fantasy opening lacks an ordinary survival/labor/resource anchor; spectacle may not explain what the community stands to lose")
    return {"mechanism_groups_present": present, "matched_terms": matched, "administrative_terms": admin_hits, "ordinary_anchor_terms": ordinary_hits, "warnings": warnings}


def gate_report(schema_errors: dict[str, list[str]], failure: dict[str, Any], scenes: dict[str, Any], architecture: dict[str, Any], architecture_reviewed: bool = True, scenes_reviewed: bool = True, storyboards: dict[str, Any] | None = None) -> dict[str, Any]:
    storyboards = storyboards or {}
    if storyboards.get("complete_exact_coverage"):
        direction_gate = "pass"
    elif storyboards.get("rows"):
        direction_gate = "attention"
    else:
        direction_gate = "missing"
    return {
        "A_premise": "pass" if not schema_errors.get("premise") and failure["risk_score_0_to_1"] < 0.5 else "attention",
        "B_architecture": ("pass" if not schema_errors.get("architecture") and not architecture.get("warnings") else "attention") if architecture_reviewed else "missing",
        "C_screenplay": ("pass" if not schema_errors.get("scenes") and not any(scenes.get("missing", {}).values()) else "attention") if scenes_reviewed else "missing",
        "D_direction_storyboard": direction_gate,
        "E_production": "unknown_until_generated_media_exists",
        "F_release_learning": "unknown_until_release_metadata_exists",
    }


def evaluate_project(premise_path: Path, architecture_path: Path | None, scenes_path: Path | None, archive_rows: list[dict[str, Any]], storyboards_path: Path | None = None) -> dict[str, Any]:
    schema_errors: dict[str, list[str]] = {"premise": validate_artifact(premise_path, "premise-packet.schema.json")}
    premise = load_json(premise_path)
    architecture = load_json(architecture_path) if architecture_path else {}
    if architecture_path:
        schema_errors["architecture"] = validate_artifact(architecture_path, "story-architecture.schema.json")
    scenes, scene_errors = load_scenes(scenes_path)
    schema_errors["scenes"] = scene_errors
    combined = "\n".join([flatten_text(premise), flatten_text(architecture), flatten_text(scenes)])
    title_candidates = premise.get("title_candidates") or []
    candidate = title_candidates[0] if title_candidates else str(premise.get("premise_id") or "untitled")
    failure = evaluate_candidate(candidate, archive_rows, combined)
    scene_report = scene_quality(scenes)
    architecture_report = architecture_quality(architecture)
    if storyboards_path is None and scenes_path is not None:
        candidate_board_dir = scenes_path.parent / "storyboards" if scenes_path.is_dir() else scenes_path.parent / "storyboards"
        storyboards_path = candidate_board_dir if candidate_board_dir.exists() else None
    boards = load_storyboards(storyboards_path)
    board_report = storyboard_coverage(scenes, boards)
    shot_pipeline = build_shot_plan(scenes, premise.get("target_minutes")) if scenes else {"shot_count": 0, "warnings": ["no scenes supplied"]}
    if board_report["complete_exact_coverage"]:
        shot_pipeline["warnings"] = ["exact continuous storyboards cover the scaffold; validate generated frames, continuity assets, and edit timing before paid production"]
        shot_pipeline["coverage_scope"] = "exact_storyboard_coverage_validated_over_scaffold"
    return {
        "premise_id": premise.get("premise_id"),
        "schema_errors": schema_errors,
        "failure_intelligence": failure,
        "scene_quality": scene_report,
        "architecture_quality": architecture_report,
        "format_strategy": format_strategy(premise.get("target_minutes"), "\n".join([premise_text_for_format_inference(premise), flatten_text(architecture), flatten_text(scenes)]), premise.get("release_format", "")),
        "opening_conversion_quality": opening_conversion_quality(premise),
        "title_packaging": {"existing_title_critiques": [{"title": title, "critique": critique_title(title, premise)} for title in premise.get("title_candidates", [])], "generated_alternatives": generate_title_candidates(premise)},
        "thumbnail_concepts": [{"concept": concept, "critique": critique_concept(concept)} for concept in generate_concepts(premise)],
        "channel_contract_fit": evaluate_channel_fit(combined, premise.get("channel_contract", "")),
        "production_economics": estimate_video_budget(premise.get("target_minutes")),
        "shot_pipeline": shot_pipeline,
        "storyboard_coverage": board_report,
        "dialogue_craft": evaluate_scenes_dialogue(scenes),
        "agency_intelligence": evaluate_agency(premise, scenes),
        "sound_design_quality": evaluate_sound_design(scenes),
        "meaning_carrier_intelligence": evaluate_meaning_carrier(premise, architecture),
        "relational_contract_intelligence": evaluate_relational_contract(premise),
        "spatial_status_intelligence": evaluate_spatial_status(premise, architecture, scenes),
        "closure_integrity": evaluate_closure_integrity(premise, architecture, scenes),
        "visual_causality": evaluate_visual_causality(scenes),
        "hidden_identity_integrity": evaluate_hidden_identity_integrity(premise, architecture, scenes),
        "scale_community_integrity": evaluate_scale_community_integrity(premise, architecture, scenes),
        "compressed_survival_integrity": evaluate_compressed_survival_integrity(premise, architecture, scenes),
        "transformation_romance_integrity": evaluate_transformation_romance_integrity(premise, architecture, scenes),
        "compound_expansion_readiness": evaluate_compound_expansion_readiness(premise, architecture, scenes),
        "creature_pacing_integrity": evaluate_creature_pacing(premise, architecture, scenes),
        "romance_deception_integrity": evaluate_romance_deception_integrity(premise, architecture, scenes),
        "zero_to_hero_integrity": evaluate_zero_to_hero_integrity(premise, architecture, scenes),
        "prohibition_scifi_integrity": evaluate_prohibition_scifi_integrity(premise, architecture, scenes),
        "family_exit_integrity": evaluate_family_exit_integrity(premise, architecture, scenes),
        "animal_guise_consent": evaluate_animal_guise_consent(premise, architecture, scenes),
        "artifact_presence": {"architecture": bool(architecture), "scenes": bool(scenes), "storyboards": len(boards)},
        "gates": gate_report(schema_errors, failure, scene_report, architecture_report, bool(architecture), bool(scenes), board_report),
    }
