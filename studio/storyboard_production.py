"""Export exact storyboards into production-ready generation manifests.

The exporter does not generate media or spend money. It turns validated director
storyboards into auditable per-shot prompts, negative prompts, audio instructions,
continuity dependencies, and QA checks so a separate generation agent/provider can
execute them consistently.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .storyboard import validate_storyboard

STYLE_ANCHOR = (
    "original cinematic animated feature film, emotionally readable faces, consistent character design, "
    "natural volumetric light, detailed but uncluttered composition, no photoreal celebrity likeness"
)
NEGATIVE_PROMPT = (
    "watermark, logo, subtitles, UI text, duplicated limbs, distorted hands, inconsistent face, "
    "random extra characters, muddy composition, copied copyrighted character design, empty spectacle"
)
ASSET_PROMPTS = {
    "mira_face_costume": "Mira reference sheet: adult woman keeper, weathered face, practical storm-blue costume, scarred palm, resolute but warm expression, front/side/three-quarter views",
    "child_face_scale_light": "stormglass dragon child reference sheet: small childlike dragon, large expressive eyes, translucent cyan-gold scales, vulnerable nonverbal expressions, front/side/three-quarter views",
    "tam_costume": "Tam reference sheet: wiry young ally, practical harbor-worker costume, copied key tools, alert expression, consistent silhouette",
    "rook_face_costume": "Rook reference sheet: controlled institutional antagonist, severe face, dark official costume, chain/control-key insignia, no cartoon villain exaggeration",
    "king_face_costume": "king reference sheet: aging ruler, layered ceremonial costume, grief and certainty readable in face, crown subdued enough for animation consistency",
    "parent_creature_design": "parent stormglass dragon reference sheet: huge protective creature, same cyan-gold scale language as child, expressive eyes, chained and free poses, scale reference beside Mira",
    "storm_vault_geography": "vertical storm vault environment plate: circular shaft, descending storm channel, gear mechanisms, chained platform, upper iris, spatial map for shot continuity",
    "stormglass_wall_continuity": "stormglass wall/network material plate: translucent cyan-gold veins, sanctuary lattice behavior, how light travels through stone",
    "memory_proof_scales": "memory-scale prop reference: small luminous scales capable of projecting memories, readable glow, consistent shape and activation state",
    "mother_call_motif": "audio motif note: three-part parent/child call that can echo, answer, distort under control, and resolve as a lullaby",
    "capital_crowd_continuity": "capital crowd reference: sailors, villagers, soldiers, workers, varied silhouettes, costume continuity, reusable crowd plates",
    "sanctuary_arch_continuity": "sunlit stormglass sanctuary arch environment plate: open coastal arch, warm restoration palette, parent and child flight path, no cage imagery",
}


def load_storyboard_files(storyboards_dir: Path) -> list[dict[str, Any]]:
    boards = []
    for path in sorted(storyboards_dir.glob("*_storyboard.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        validation = validate_storyboard(data)
        if not validation["valid"]:
            raise ValueError(f"invalid storyboard {path}: {validation['errors']}")
        data["_source_path"] = str(path)
        boards.append(data)
    return boards


def infer_assets(dependencies: list[str]) -> list[dict[str, str]]:
    assets = []
    for dep in dependencies:
        assets.append({"dependency": dep, "asset_prompt": ASSET_PROMPTS.get(dep, f"continuity reference asset for {dep}")})
    return assets


def shot_prompt(shot: dict[str, Any], scene_id: str) -> dict[str, Any]:
    visual = shot.get("visual_action", "")
    camera = shot.get("camera_intent", "")
    size = shot.get("shot_size", "")
    lane = shot.get("generation_lane", "mid")
    dependencies = list(shot.get("continuity_dependencies", []))
    visual_prompt = f"{STYLE_ANCHOR}. {size}; {camera}; {visual}. Emotional action must remain readable before spectacle."
    return {
        "shot_id": shot.get("shot_id"),
        "scene_id": scene_id,
        "timecode": shot.get("timecode"),
        "duration_seconds": shot.get("duration_seconds"),
        "generation_lane": lane,
        "visual_prompt": visual_prompt,
        "negative_prompt": NEGATIVE_PROMPT,
        "camera_intent": camera,
        "dialogue": shot.get("dialogue", ""),
        "audio_direction": shot.get("sound_design", ""),
        "director_note": shot.get("director_note", ""),
        "continuity_dependencies": dependencies,
        "required_reference_assets": infer_assets(dependencies),
        "qa_checks": [
            "character/creature faces match approved reference sheets",
            "story geography matches prior and following shots",
            "emotion and power shift remain readable at full-screen playback",
            "no text, watermark, logo, or subtitle artifact",
            "dialogue lip/performance timing reviewed before upscale or final render",
        ],
    }


def export_manifest(storyboards_dir: Path, output_dir: Path, project_id: str = "project") -> dict[str, Any]:
    boards = load_storyboard_files(storyboards_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    shots = []
    scene_rows = []
    all_dependencies: dict[str, dict[str, str]] = {}
    for board in boards:
        scene_id = str(board.get("scene_id"))
        scene_shots = [shot_prompt(shot, scene_id) for shot in board.get("shots", [])]
        shots.extend(scene_shots)
        scene_rows.append({
            "scene_id": scene_id,
            "duration_seconds": board.get("duration_seconds"),
            "shot_count": len(scene_shots),
            "source_path": board.get("_source_path"),
        })
        for shot in scene_shots:
            for asset in shot["required_reference_assets"]:
                all_dependencies[asset["dependency"]] = asset
        (output_dir / f"{scene_id}_shot_prompts.json").write_text(json.dumps(scene_shots, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lane_counts: dict[str, int] = {}
    for shot in shots:
        lane_counts[shot["generation_lane"]] = lane_counts.get(shot["generation_lane"], 0) + 1
    manifest = {
        "project_id": project_id,
        "scope": "pre_generation_prompt_manifest_not_generated_media",
        "scene_count": len(scene_rows),
        "shot_count": len(shots),
        "lane_counts": lane_counts,
        "scenes": scene_rows,
        "reference_assets": [all_dependencies[key] for key in sorted(all_dependencies)],
        "production_order": [
            "approve story and exact storyboards",
            "generate or draw reference sheets and environment plates",
            "review reference consistency before motion generation",
            "generate draft/mid shots for blocking",
            "generate hero payoff shots only after continuity assets are locked",
            "assemble edit with dialogue and sound before expensive final upscales",
            "run release postmortem and feed results back into failure intelligence",
        ],
        "spend_warning": "This manifest is a planning artifact. Do not connect it to paid generation without explicit approval and provider pricing review.",
        "shots": shots,
    }
    (output_dir / "production_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest
