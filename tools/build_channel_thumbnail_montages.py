"""Build deduplicated hit/middle/failure thumbnail montages per channel."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


def load_index(path: Path) -> dict[str, dict]:
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows[row["video_id"]] = row
    return rows


def cohort_rows(comparison_path: Path, index: dict[str, dict]) -> dict[str, list[dict]]:
    data = json.loads(comparison_path.read_text(encoding="utf-8"))
    out = {"outperforming": [], "middle": [], "underperforming": []}
    for row in data.get("videos", []):
        thumb = index.get(row.get("video_id"), {})
        if not thumb.get("thumbnail_path"):
            continue
        merged = {**thumb, **row}
        cohort = row.get("within_channel_cohort", "middle")
        out.setdefault(cohort, out["middle"]).append(merged)
    return out


def pick_unique(rows: list[dict], count: int) -> list[dict]:
    picked = []
    seen = set()
    for row in rows:
        vid = row.get("video_id")
        if vid and vid not in seen:
            picked.append(row)
            seen.add(vid)
        if len(picked) >= count:
            break
    return picked


def montage(channel_key: str, cohorts: dict[str, list[dict]], output: Path, thumb_size=(256, 144)) -> Path | None:
    groups = [("HIT", cohorts.get("outperforming", [])), ("MIDDLE", cohorts.get("middle", [])), ("LOW", cohorts.get("underperforming", []))]
    n = max((len(v) for _, v in groups), default=0)
    if not n:
        return None
    per = min(3, n)
    w, h = thumb_size
    label_h = 30
    canvas = Image.new("RGB", (w * per, (h + label_h) * len(groups) + 44), "#111111")
    draw = ImageDraw.Draw(canvas)
    draw.text((8, 8), channel_key.replace("_", " ").upper(), fill="white")
    y = 40
    for label, rows in groups:
        draw.rectangle((0, y, canvas.width, y + label_h), fill="#222222")
        draw.text((8, y + 7), label, fill="white")
        for x, row in enumerate(pick_unique(rows, per)):
            path = Path(row["thumbnail_path"])
            if not path.exists():
                continue
            im = Image.open(path).convert("RGB")
            im.thumbnail((w, h))
            tile = Image.new("RGB", (w, h), "black")
            tile.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
            canvas.paste(tile, (x * w, y + label_h))
            caption = f"{row.get('views_per_day', 0):.0f}/d | {row.get('video_id', '')}"
            draw.text((x * w + 5, y + label_h + h - 15), caption, fill="white")
        y += h + label_h
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, quality=90)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="thumbnails/priority_channels_index.jsonl")
    parser.add_argument("--comparisons", default="data/processed/channel_comparisons")
    parser.add_argument("--out", default="thumbnails/channel_cohort_montages")
    args = parser.parse_args()
    index = load_index(Path(args.index))
    outputs = []
    for path in sorted(Path(args.comparisons).glob("*.json")):
        if path.name == "summary.json":
            continue
        result = montage(path.stem, cohort_rows(path, index), Path(args.out) / f"{path.stem}.jpg")
        if result:
            outputs.append(str(result))
    print(json.dumps({"montages": outputs}, indent=2))


if __name__ == "__main__":
    main()
