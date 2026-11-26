"""Structured creative-feature extraction for comparative video analysis.

The taxonomy is intentionally explicit and auditable: every inferred feature stores the
surface evidence that triggered it. These are hypotheses about audience-facing signals,
not claims of causal retention/CTR effects.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageStat

THEME_PATTERNS: dict[str, list[str]] = {
    "dragon": ["dragon"],
    "wolf_werewolf": ["wolf", "werewolf", "alpha", "omega", "lycan"],
    "vampire": ["vampire", "blood moon"],
    "sea_mermaid": ["mermaid", "sea god", "sea king", "ocean"],
    "angel_demon": ["angel", "archangel", "fallen angel", "demon"],
    "animal_child": ["puppy", "kitten", "rabbit", "pet", "cub"],
    "modern_wealth_power": ["billionaire", "ceo", "mafia", "championship", "taxi driver"],
    "royalty_status": ["king", "queen", "prince", "princess", "emperor", "empress", "royal", "supreme", "god", "goddess"],
    "romance_mate": ["love", "mate", "fianc", "married", "husband", "wife", "kiss", "true love", "boyfriend"],
    "revenge_retribution": ["revenge", "take back", "take it all back", "take it all", "destroy", "never have", "never touch", "lost everything"],
    "family_child": ["baby", "babies", "child", "children", "daughter", "son", "mom", "dad", "family", "pregnant", "unborn"],
    "rebirth_second_chance": ["reborn", "second chance", "back", "returned"],
    "sacred_special_blood": ["sacred", "blood", "half-blood", "divine power", "curse", "cursed", "magic", "witch"],
}

VICTIM_PATTERNS = [
    "abandoned", "betrayed", "humiliated", "rejected", "mocked", "dumped", "left her to die",
    "left him to die", "sacrificed", "hunted", "cursed", "poor", "orphan", "worthless", "fat",
    "stole everything", "sent her to die", "left someone", "drugged", "cheating", "hybrid",
]
HIDDEN_IDENTITY_PATTERNS = ["unaware", "secretly", "never knowing", "not knowing", "only i know", "true love", "lost princess"]
STATUS_REVERSAL_PATTERNS = ["now she", "now he", "became", "become", "returned", "rules", "made her", "walked away", "changed his fate", "changed everything"]
KINSHIP_RESCUE_PATTERNS = ["saved", "save her", "save his", "took her in", "adopted", "raised"]

FEMALE_MARKERS = ["she", "her", "girl", "wife", "woman", "mom", "mother", "princess", "queen", "empress", "goddess", "mermaid"]
MALE_MARKERS = ["he", "his", "him", "boy", "husband", "man", "dad", "father", "prince", "king", "emperor", "godfather"]


def contains_any(text: str, patterns: list[str]) -> tuple[bool, list[str]]:
    lower = text.lower()
    hits = [pattern for pattern in patterns if pattern in lower]
    return bool(hits), hits


def title_features(title: str) -> dict[str, Any]:
    lower = title.lower()
    words = re.findall(r"[A-Za-z']+", title)
    caps_words = [w for w in words if len(w) > 1 and w.upper() == w]
    female_hits = [m for m in FEMALE_MARKERS if re.search(rf"\b{re.escape(m)}\b", lower)]
    male_hits = [m for m in MALE_MARKERS if re.search(rf"\b{re.escape(m)}\b", lower)]
    protagonist_gender = "female" if len(female_hits) > len(male_hits) else "male" if len(male_hits) > len(female_hits) else "ambiguous"

    themes = {}
    for theme, patterns in THEME_PATTERNS.items():
        hit, evidence = contains_any(lower, patterns)
        themes[theme] = {"present": hit, "evidence": evidence}

    victim, victim_hits = contains_any(lower, VICTIM_PATTERNS)
    hidden, hidden_hits = contains_any(lower, HIDDEN_IDENTITY_PATTERNS)
    reversal, reversal_hits = contains_any(lower, STATUS_REVERSAL_PATTERNS)
    kinship, kinship_hits = contains_any(lower, KINSHIP_RESCUE_PATTERNS)
    if hidden and victim and any(marker in lower for marker in ("king", "queen", "prince", "princess", "heir", "daughter", "son", "empress", "emperor")):
        reversal = True
        reversal_hits = reversal_hits + ["implicit_high_status_identity_reversal"]

    pivot_positions = [pos for token in ("…", "�") for pos in [title.find(token)] if pos >= 0]
    pivot_ratio = (min(pivot_positions) / max(len(title), 1)) if pivot_positions else None
    setup_then_reversal = bool(pivot_positions and victim and reversal and pivot_ratio is not None and pivot_ratio < 0.65)

    return {
        "protagonist_gender": protagonist_gender,
        "gender_evidence": {"female": female_hits, "male": male_hits},
        "themes": themes,
        "victimization": {"present": victim, "evidence": victim_hits},
        "hidden_identity_or_secret": {"present": hidden, "evidence": hidden_hits},
        "status_reversal": {"present": reversal, "evidence": reversal_hits},
        "kinship_rescue": {"present": kinship, "evidence": kinship_hits},
        "title_structure": {
            "characters": len(title),
            "word_count": len(words),
            "ellipsis_or_separator": bool(pivot_positions),
            "pivot_ratio": pivot_ratio,
            "setup_then_reversal": setup_then_reversal,
            "caps_word_count": len(caps_words),
            "caps_words": caps_words,
            "caps_ratio": len(caps_words) / max(len(words), 1),
            "exclamation": "!" in title,
            "question": "?" in title,
        },
    }


def thumbnail_features(path: str | None) -> dict[str, Any]:
    if not path or not Path(path).exists():
        return {"available": False}
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image.resize((320, 180)), dtype=np.float32) / 255.0
    red, green, blue = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    brightness = float(arr.mean())
    maxc = arr.max(axis=2)
    minc = arr.min(axis=2)
    saturation = float(((maxc - minc) / np.maximum(maxc, 1e-5)).mean())
    colorfulness = float(np.sqrt(red.var() + green.var() + blue.var()))
    lower = arr[int(arr.shape[0] * 0.55) :, :, :]
    gray = lower.mean(axis=2)
    edge_density = float((np.abs(np.diff(gray, axis=1)).mean() + np.abs(np.diff(gray, axis=0)).mean()))
    center = arr[:, int(arr.shape[1] * 0.2) : int(arr.shape[1] * 0.8), :]
    center_brightness = float(center.mean())
    warm_ratio = float(((red > blue * 1.08) & (red > green * 0.9)).mean())
    gold_ratio = float(((red > 0.55) & (green > 0.32) & (blue < 0.28)).mean())
    blue_ratio = float(((blue > red * 1.05) & (blue > green * 0.9)).mean())
    return {
        "available": True,
        "width": image.width,
        "height": image.height,
        "brightness": brightness,
        "saturation": saturation,
        "colorfulness": colorfulness,
        "lower_half_edge_density_proxy_for_text": edge_density,
        "center_brightness": center_brightness,
        "warm_ratio": warm_ratio,
        "gold_ratio": gold_ratio,
        "blue_ratio": blue_ratio,
    }


def enrich_records(input_jsonl: Path, output_jsonl: Path) -> Path:
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with input_jsonl.open(encoding="utf-8", newline="") as source:
        lines = source.readlines()
    with output_jsonl.open("w", encoding="utf-8") as target:
        for line in lines:
            if not line.strip():
                continue
            row = json.loads(line)
            title = row.get("exact_title") or row.get("archive_title") or ""
            row["creative_features"] = title_features(title)
            row["thumbnail_features"] = thumbnail_features(row.get("thumbnail_path"))
            target.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    return output_jsonl


def flatten_theme(row: dict[str, Any], theme: str) -> bool:
    return bool(row.get("creative_features", {}).get("themes", {}).get(theme, {}).get("present"))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="data/raw/novdrama_archive.jsonl")
    parser.add_argument("output", nargs="?", default="data/processed/novdrama_enriched.jsonl")
    args = parser.parse_args()
    print(enrich_records(Path(args.input), Path(args.output)))


if __name__ == "__main__":
    main()
