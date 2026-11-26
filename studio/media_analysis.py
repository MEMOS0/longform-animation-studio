"""Second-resolution audiovisual evidence extraction.

This module is deliberately evidence-first: it never claims a viewer reaction directly.
It produces timestamped visual, audio, subtitle, and structural observations that a later
analyst or agent can use to support or reject hypotheses.
"""
from __future__ import annotations

import argparse
import html
import re
import json
import math
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

try:
    import librosa
except Exception:  # pragma: no cover - optional at runtime
    librosa = None

FRAME_W = 160
FRAME_H = 90
FPS_SAMPLE = 1


def sample_geometry(width: int | None, height: int | None) -> tuple[int, int]:
    if width and height and height > width:
        return 90, 160
    return 160, 90


def run(cmd: list[str], timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def ffprobe(video: Path) -> dict[str, Any]:
    proc = run([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_entries", "format=duration,size:stream=codec_type,width,height,r_frame_rate", str(video)
    ])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr)
    data = json.loads(proc.stdout)
    streams = data.get("streams", [])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})
    return {
        "duration": float(data.get("format", {}).get("duration") or 0),
        "size": int(data.get("format", {}).get("size") or 0),
        "width": video_stream.get("width"),
        "height": video_stream.get("height"),
        "fps": video_stream.get("r_frame_rate"),
        "has_audio": bool(audio_stream),
    }


def parse_time(value: str) -> float:
    parts = value.split(":")
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + float(seconds)
    return float(value)


def parse_ttml(path: Path | None) -> list[dict[str, Any]]:
    if not path or not path.exists():
        return []
    raw = path.read_bytes()
    if raw.lstrip().startswith(b"WEBVTT"):
        cues = []
        text_raw = raw.decode("utf-8", errors="replace")
        blocks = re.split(r"\n\s*\n", text_raw)
        for block in blocks:
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            if not lines:
                continue
            time_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
            if time_index is None:
                continue
            begin_raw, end_raw = [part.strip().split()[0] for part in lines[time_index].split("-->", 1)]
            cue_lines = lines[time_index + 1:]
            if not cue_lines:
                continue
            clean_parts = []
            for line in cue_lines:
                line = re.sub(r"<\d{2}:\d{2}:\d{2}\.\d{3}>", " ", line)
                line = re.sub(r"</?c(?:\.[^>]*)?>", "", line)
                line = re.sub(r"<[^>]+>", "", line)
                line = html.unescape(" ".join(line.split())).strip()
                if line:
                    clean_parts.append(line)
            text = " ".join(clean_parts).strip()
            if not text:
                continue
            cues.append({"start": parse_time(begin_raw.replace(",", ".")), "end": parse_time(end_raw.replace(",", ".")), "text": text})
        ordered = sorted(cues, key=lambda cue: cue["start"])
        deduped = []
        for index, cue in enumerate(ordered):
            duration = cue["end"] - cue["start"]
            if duration <= 0.02:
                neighbors = []
                if deduped:
                    neighbors.append(deduped[-1])
                if index + 1 < len(ordered):
                    neighbors.append(ordered[index + 1])
                if cue["text"] and any(cue["text"] in neighbor.get("text", "") for neighbor in neighbors):
                    continue
            if deduped and cue["start"] == deduped[-1]["start"] and cue["text"] == deduped[-1]["text"]:
                continue
            if deduped and cue["text"] == deduped[-1]["text"] and cue["start"] < deduped[-1]["end"]:
                deduped[-1]["end"] = max(deduped[-1]["end"], cue["end"])
                continue
            cue = dict(cue)
            if deduped and cue["start"] <= deduped[-1]["end"] + 0.05:
                previous_text = deduped[-1].get("full_text", deduped[-1]["text"])
                text = cue["text"]
                overlap = len(previous_text) if text.startswith(previous_text) else 0
                if not overlap:
                    max_overlap = min(len(previous_text), len(text))
                    for size in range(max_overlap, 11, -1):
                        if text.startswith(previous_text[-size:]):
                            overlap = size
                            break
                if overlap:
                    cue["full_text"] = text
                    cue["text"] = text[overlap:].strip()
                    if not cue["text"]:
                        continue
            deduped.append(cue)
        return deduped
    root = ET.fromstring(raw)
    ns = {"tt": "http://www.w3.org/ns/ttml"}
    cues = []
    for node in root.findall(".//tt:p", ns):
        begin = node.attrib.get("begin")
        end = node.attrib.get("end")
        if not begin or not end:
            continue
        text = " ".join("".join(node.itertext()).split())
        text = html.unescape(text).replace(">>", "").strip()
        if not text:
            continue
        cues.append({"start": parse_time(begin), "end": parse_time(end), "text": text})
    cues.sort(key=lambda cue: cue["start"])
    return cues


def frame_features(frame: np.ndarray, previous: np.ndarray | None) -> dict[str, float]:
    arr = frame.astype(np.float32) / 255.0
    brightness = float(arr.mean())
    maxc = arr.max(axis=2)
    minc = arr.min(axis=2)
    saturation = float(((maxc - minc) / np.maximum(maxc, 1e-5)).mean())
    gray = arr.mean(axis=2)
    edge = float(np.abs(np.diff(gray, axis=1)).mean() + np.abs(np.diff(gray, axis=0)).mean())
    colorfulness = float(np.sqrt(arr[:, :, 0].var() + arr[:, :, 1].var() + arr[:, :, 2].var()))
    motion = float(np.mean(np.abs(arr - previous.astype(np.float32) / 255.0))) if previous is not None else 0.0
    hist = cv2.calcHist([frame], [0, 1, 2], None, [4, 4, 4], [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    hist_diff = 0.0
    if previous is not None:
        prev_hist = cv2.calcHist([previous], [0, 1, 2], None, [4, 4, 4], [0, 256, 0, 256, 0, 256])
        prev_hist = cv2.normalize(prev_hist, prev_hist).flatten()
        hist_diff = float(cv2.compareHist(hist, prev_hist, cv2.HISTCMP_BHATTACHARYYA))
    warm = float(((arr[:, :, 0] > arr[:, :, 2] * 1.08) & (arr[:, :, 0] > arr[:, :, 1] * 0.9)).mean())
    return {
        "brightness": brightness,
        "saturation": saturation,
        "edge_density": edge,
        "colorfulness": colorfulness,
        "motion_mean_abs_diff": motion,
        "histogram_diff": hist_diff,
        "warm_ratio": warm,
    }


def sample_video_frames(video: Path, output_dir: Path, contact_every: int = 20, source_width: int | None = None, source_height: int | None = None) -> tuple[list[dict[str, Any]], list[str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    frame_w, frame_h = sample_geometry(source_width, source_height)
    tile_w, tile_h = (144, 256) if frame_h > frame_w else (256, 144)
    cmd = [
        "ffmpeg", "-v", "error", "-i", str(video), "-vf", f"fps={FPS_SAMPLE},scale={frame_w}:{frame_h}",
        "-f", "rawvideo", "-pix_fmt", "bgr24", "-"
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdout is not None
    frame_size = frame_w * frame_h * 3
    rows: list[dict[str, Any]] = []
    thumbs: list[tuple[int, Image.Image]] = []
    previous = None
    second = 0
    diffs = []
    while True:
        payload = proc.stdout.read(frame_size)
        if len(payload) < frame_size:
            break
        frame = np.frombuffer(payload, dtype=np.uint8).reshape((frame_h, frame_w, 3)).copy()
        feats = frame_features(frame, previous)
        diffs.append(feats["histogram_diff"] + feats["motion_mean_abs_diff"])
        row = {"t": second, **feats}
        rows.append(row)
        if second % contact_every == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            thumbs.append((second, Image.fromarray(rgb).resize((tile_w, tile_h))))
        previous = frame
        second += 1
    stderr = proc.stderr.read().decode("utf-8", "ignore") if proc.stderr else ""
    proc.wait()
    if proc.returncode != 0 and not rows:
        raise RuntimeError(stderr)

    values = np.array([r["histogram_diff"] for r in rows[1:]], dtype=float)
    threshold = max(0.18, float(np.percentile(values, 97))) if len(values) else 0.2
    shot_id = 0
    for index, row in enumerate(rows):
        row["shot_boundary"] = bool(index and row["histogram_diff"] >= threshold)
        if row["shot_boundary"]:
            shot_id += 1
        row["shot_id"] = shot_id

    sheet_paths = []
    font = ImageFont.load_default()
    columns, rows_per_sheet = 4, 5
    per_sheet = columns * rows_per_sheet
    for sheet_index in range(math.ceil(len(thumbs) / per_sheet)):
        batch = thumbs[sheet_index * per_sheet : (sheet_index + 1) * per_sheet]
        sheet = Image.new("RGB", (columns * tile_w, rows_per_sheet * (tile_h + 20)), "black")
        draw = ImageDraw.Draw(sheet)
        for pos, (timestamp, image) in enumerate(batch):
            x, y = (pos % columns) * tile_w, (pos // columns) * (tile_h + 20)
            sheet.paste(image, (x, y))
            draw.text((x + 3, y + tile_h + 2), f"{timestamp//60:02d}:{timestamp%60:02d}", fill="white", font=font)
        path = output_dir / f"contact_{sheet_index:03d}.jpg"
        sheet.save(path, quality=88)
        sheet_paths.append(str(path))
    return rows, sheet_paths


def extract_audio(video: Path, output_dir: Path) -> Path | None:
    output_dir.mkdir(parents=True, exist_ok=True)
    wav = output_dir / "audio_16k.wav"
    if wav.exists() and wav.stat().st_size > 1000:
        return wav
    proc = run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(wav)], timeout=300)
    return wav if proc.returncode == 0 and wav.exists() else None


def audio_features(video: Path, output_dir: Path, window: int = 10) -> dict[int, dict[str, float]]:
    if librosa is None:
        return {}
    wav = extract_audio(video, output_dir)
    if not wav:
        return {}
    try:
        y, sr = librosa.load(str(wav), sr=16000, mono=True)
    except Exception:
        return {}
    result: dict[int, dict[str, float]] = {}
    reference_rms = librosa.feature.rms(y=y)[0]
    silence_floor = max(float(np.percentile(reference_rms, 20)), 0.002)
    for start in range(0, int(len(y) / sr), window):
        segment = y[start * sr : min((start + window) * sr, len(y))]
        if len(segment) < sr:
            continue
        rms = librosa.feature.rms(y=segment)[0]
        centroid = librosa.feature.spectral_centroid(y=segment, sr=sr)[0]
        zcr = librosa.feature.zero_crossing_rate(segment)[0]
        onsets = librosa.onset.onset_detect(y=segment, sr=sr, units="time")
        result[start] = {
            "rms_mean": float(rms.mean()),
            "rms_std": float(rms.std()),
            "spectral_centroid_mean": float(centroid.mean()),
            "zero_crossing_rate": float(zcr.mean()),
            "onsets_per_second": float(len(onsets) / max(len(segment) / sr, 1)),
            "silence_ratio": float((rms < silence_floor).mean()),
        }
    return result


def cue_text_in_window(cues: list[dict[str, Any]], start: float, end: float) -> str:
    texts = [cue["text"] for cue in cues if cue["start"] < end and cue["end"] > start]
    return " ".join(texts)


def narrative_markers(cues: list[dict[str, Any]]) -> dict[str, Any]:
    conflict_patterns = ["abandon", "betray", "curse", "die", "death", "kill", "poor", "orphan", "sacrifice", "humiliat", "reject", "monster", "thief", "filthy"]
    reveal_patterns = ["dragon", "king", "queen", "prince", "princess", "secret", "power", "blood", "transform", "alpha", "god", "magic"]
    care_patterns = ["sorry", "thank you", "family", "home", "save", "protect", "love", "care", "stay with"]

    def first(patterns):
        for cue in cues:
            lower = cue["text"].lower()
            if any(pattern in lower for pattern in patterns):
                return {"time": cue["start"], "text": cue["text"]}
        return None

    words_per_minute = []
    for minute in range(math.ceil((cues[-1]["end"] if cues else 0) / 60)):
        text = cue_text_in_window(cues, minute * 60, (minute + 1) * 60)
        words_per_minute.append(len(re.findall(r"[A-Za-z']+", text)))
    return {
        "first_conflict_language": first(conflict_patterns),
        "first_power_or_identity_language": first(reveal_patterns),
        "first_care_or_belonging_language": first(care_patterns),
        "dialogue_words_per_minute": words_per_minute,
        "cue_count": len(cues),
    }


def merge_timeline(visual_rows: list[dict[str, Any]], audio: dict[int, dict[str, float]], cues: list[dict[str, Any]], window: int = 10) -> list[dict[str, Any]]:
    duration = len(visual_rows)
    timeline = []
    for start in range(0, duration, window):
        end = min(start + window, duration)
        segment = visual_rows[start:end]
        if not segment:
            continue
        row: dict[str, Any] = {
            "start": start,
            "end": end,
            "shot_ids": sorted(set(int(r["shot_id"]) for r in segment)),
            "shot_boundary_count": sum(1 for r in segment if r.get("shot_boundary")),
            "visual_mean": {
                key: float(np.mean([r[key] for r in segment]))
                for key in ("brightness", "saturation", "edge_density", "colorfulness", "motion_mean_abs_diff", "warm_ratio")
            },
            "dialogue_text": cue_text_in_window(cues, start, end),
            "dialogue_word_count": len(re.findall(r"[A-Za-z']+", cue_text_in_window(cues, start, end))),
        }
        row.update({f"audio_{k}": v for k, v in audio.get(start, {}).items()})
        timeline.append(row)
    return timeline


def summarize(timeline: list[dict[str, Any]], visual_rows: list[dict[str, Any]], cues: list[dict[str, Any]]) -> dict[str, Any]:
    shot_lengths = []
    last = 0
    for row in visual_rows:
        if row.get("shot_boundary"):
            shot_lengths.append(row["t"] - last)
            last = row["t"]
    if visual_rows:
        shot_lengths.append(len(visual_rows) - last)
    return {
        "seconds_indexed": len(visual_rows),
        "shot_count": len(shot_lengths),
        "shot_length_mean_seconds": float(np.mean(shot_lengths)) if shot_lengths else None,
        "shot_length_median_seconds": float(np.median(shot_lengths)) if shot_lengths else None,
        "shot_length_p90_seconds": float(np.percentile(shot_lengths, 90)) if shot_lengths else None,
        "visual_motion_mean": float(np.mean([r["motion_mean_abs_diff"] for r in visual_rows])) if visual_rows else None,
        "visual_brightness_mean": float(np.mean([r["brightness"] for r in visual_rows])) if visual_rows else None,
        "dialogue_cues": len(cues),
        "narrative_markers": narrative_markers(cues),
    }


def analyze_video(video_path: Path, subtitle_path: Path | None, output_dir: Path, video_id: str) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    probe = ffprobe(video_path)
    visual_rows, contact_sheets = sample_video_frames(video_path, output_dir / "contact_sheets", source_width=probe.get("width"), source_height=probe.get("height"))
    cues = parse_ttml(subtitle_path)
    audio = audio_features(video_path, output_dir)
    timeline = merge_timeline(visual_rows, audio, cues)

    timeline_path = output_dir / f"{video_id}.timeline.jsonl"
    with timeline_path.open("w", encoding="utf-8") as handle:
        for row in timeline:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    seconds_path = output_dir / f"{video_id}.seconds.jsonl"
    with seconds_path.open("w", encoding="utf-8") as handle:
        for row in visual_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary = {"video_id": video_id, "probe": probe, "contact_sheets": contact_sheets, **summarize(timeline, visual_rows, cues)}
    summary_path = output_dir / f"{video_id}.media_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"timeline": timeline_path, "seconds": seconds_path, "summary": summary_path}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--video-id", required=True)
    args = parser.parse_args()
    result = analyze_video(Path(args.video), Path(args.subtitle) if args.subtitle else None, Path(args.output_dir), args.video_id)
    print(json.dumps({k: str(v) for k, v in result.items()}, indent=2))


if __name__ == "__main__":
    main()
