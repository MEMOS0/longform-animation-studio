"""Repair silence ratios in existing media-analysis timelines after extractor fixes."""
from __future__ import annotations

import argparse
import json
import sys
import wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from studio.media_analysis import extract_audio
from studio.story_signals import read_jsonl


def fast_rms_profile(wav_path: Path, frame: int = 512, hop: int = 512) -> tuple[np.ndarray, int]:
    with wave.open(str(wav_path), "rb") as handle:
        rate = handle.getframerate()
        width = handle.getsampwidth()
        channels = handle.getnchannels()
        raw = handle.readframes(handle.getnframes())
    dtype = np.int16 if width == 2 else np.int32
    data = np.frombuffer(raw, dtype=dtype).astype(np.float32)
    if channels > 1:
        data = data.reshape(-1, channels).mean(axis=1)
    data /= float(np.iinfo(dtype).max)
    count = max(0, 1 + (len(data) - frame) // hop)
    if count <= 0:
        return np.array([]), rate
    frames = np.lib.stride_tricks.as_strided(data, shape=(count, frame), strides=(data.strides[0] * hop, data.strides[0]))
    return np.sqrt((frames * frames).mean(axis=1)), rate


def repair(media_root: Path, media_dir: Path) -> dict[str, int]:
    repaired = 0
    missing = 0
    for timeline_path in sorted(media_root.glob("*/*.timeline.jsonl")):
        video_dir = timeline_path.parent
        video_id = video_dir.name
        video_path = media_dir / f"{video_id}.mp4"
        rows = read_jsonl(timeline_path)
        if not rows or not video_path.exists():
            missing += 1
            continue
        wav = extract_audio(video_path, video_dir)
        if not wav:
            missing += 1
            continue
        rms, rate = fast_rms_profile(wav)
        if not len(rms):
            missing += 1
            continue
        silence_floor = max(float(np.percentile(rms, 20)), 0.002)
        fps = rate / 512.0
        changed = False
        for row in rows:
            start = int(row.get("start", 0))
            end = int(row.get("end", start + 10))
            a = int(start * fps)
            b = max(a + 1, int(end * fps))
            segment = rms[a:min(b, len(rms))]
            if len(segment):
                row["audio_silence_ratio"] = float((segment < silence_floor).mean())
                row["audio_rms_mean"] = float(segment.mean())
                row["audio_rms_std"] = float(segment.std())
                changed = True
        if changed:
            with timeline_path.open("w", encoding="utf-8") as handle:
                for row in rows:
                    handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            repaired += 1
        else:
            missing += 1
    return {"repaired": repaired, "missing_or_skipped": missing}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--media-root", default="data/processed/media_batch")
    parser.add_argument("--media-dir", default="C:/Users/Administrator/novdrama_media")
    args = parser.parse_args()
    print(json.dumps(repair(Path(args.media_root), Path(args.media_dir)), indent=2))


if __name__ == "__main__":
    main()
