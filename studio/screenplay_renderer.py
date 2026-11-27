"""Render structured scene units into annotated screenplay drafts.

These are professional working drafts for rewriting/directing, not final production
scripts. They make action, speaker, pressure, sound, image consequences, and edit
hooks legible in a screenplay-like reading order while preserving evidence-backed
scene causality.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def speaker_label(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", str(name or "VOICE")).strip()
    special = {
        "land trust": "LAND TRUST OFFICER",
        "coal guild": "COAL GUILD OFFICER",
        "customer witness": "CUSTOMER",
        "care network witness": "CARE NETWORK WITNESS",
        "her grandmother": "GRANDMOTHER",
        "the caregiver": "CAREGIVER",
    }
    return special.get(cleaned.lower(), cleaned.upper())


def sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    if not text:
        return ""
    return text[:1].upper() + text[1:] + ("" if text.endswith((".", "!", "?")) else ".")


def parenthetical(turn: dict[str, Any]) -> str:
    delivery = str(turn.get("delivery") or "").split(";")[0]
    parts = [part.strip() for part in delivery.split(",") if part.strip()]
    if not parts:
        return ""
    return ", ".join(parts[:2])


def render_scene(scene: dict[str, Any]) -> str:
    scene_id = scene.get("scene_id", "SCENE")
    dialogue = scene.get("dialogue_design", {})
    visual = scene.get("visual_action", {})
    sound = scene.get("sound_design", {})
    lines = [
        f"## {scene_id} — {scene.get('time_range', '')}",
        "",
        f"OBJECTIVE: {scene.get('objective', '')}",
        f"POWER SHIFT: {scene.get('power_position_start', '')} → {scene.get('power_position_end', '')}",
        f"SCENE SUBTEXT: {scene.get('subtext', '')}",
        f"RHYTHM: {dialogue.get('scene_rhythm', '')}",
        "",
        sentence(visual.get("first_image", "")),
        "",
    ]
    exchange = dialogue.get("spoken_exchange") or []
    if not exchange and dialogue.get("key_lines"):
        lines.extend(["KEY DIALOGUE", ""])
        for key_line in dialogue.get("key_lines") or []:
            lines.extend([f"- {key_line}", ""])
    for turn in exchange:
        action = sentence(turn.get("action", ""))
        if action:
            lines.extend([action, ""])
        lines.append(speaker_label(turn.get("speaker", "VOICE")))
        note = parenthetical(turn)
        if note:
            lines.append(f"({note})")
        lines.extend([str(turn.get("line", "")).strip(), ""])
        room_sound = sentence(turn.get("room_sound", ""))
        if room_sound:
            lines.extend(["SOUND — " + room_sound, ""])
    final_image = sentence(visual.get("final_image", ""))
    if final_image:
        lines.extend(["FINAL IMAGE — " + final_image, ""])
    negative = sentence(sound.get("silence_or_negative_space", ""))
    if negative:
        lines.extend(["SOUND SPACE — " + negative, ""])
    lines.extend([
        f"EXIT HOOK: {scene.get('edit_hook', {}).get('exit_hook', '')}",
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def render_screenplay(premise: dict[str, Any], scenes: list[dict[str, Any]]) -> str:
    title = (premise.get("title_candidates") or ["Untitled"])[0]
    parts = [
        f"# Annotated Screenplay Draft — {title}",
        "",
        "Status: evidence-informed professional working draft. Rewrite for voice, casting, culture, and production constraints before shooting; preserve the power turns, objections, proof chain, sound negative space, and image consequences.",
        "",
        f"Target minutes: {premise.get('target_minutes', '')}",
        f"Premise id: {premise.get('premise_id', '')}",
        "",
        "GLOBAL REWRITE RULES: keep turns interruptible; answer concrete pressure rather than restating theme; let hands, objects, thresholds, witnesses, and creature behavior carry psychology; avoid naming feelings the action already proves.",
        "",
    ]
    parts.extend(render_scene(scene).rstrip() for scene in scenes)
    return "\n\n".join(part for part in parts if part is not None).rstrip() + "\n"


def write_screenplay(premise: dict[str, Any], scenes: list[dict[str, Any]], output_path: Path) -> Path:
    output_path.write_text(render_screenplay(premise, scenes), encoding="utf-8")
    return output_path
