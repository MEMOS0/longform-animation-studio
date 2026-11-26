"""Thumbnail evidence extraction for comparative packaging analysis."""
from __future__ import annotations

import colorsys
import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image


def image_metrics(path: Path) -> dict[str, Any]:
    img = Image.open(path).convert("RGB")
    arr = np.asarray(img)
    h, w = arr.shape[:2]
    rgb = arr.astype(np.float32) / 255.0
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)
    brightness = float(gray.mean())
    contrast = float(gray.std())
    saturation = float((hsv[:, :, 1] / 255.0).mean())
    # colorfulness metric (Hasler/Süsstrunk opponent-channel dispersion)
    rg = rgb[:, :, 0] - rgb[:, :, 1]
    yb = 0.5 * (rgb[:, :, 0] + rgb[:, :, 1]) - rgb[:, :, 2]
    colorfulness = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    lap = cv2.Laplacian((gray * 255).astype(np.uint8), cv2.CV_64F)
    edge_density = float((np.abs(lap) > 20).mean())
    # Rule-of-thirds central/subject saliency proxy: center contrast vs edges.
    cy0, cy1 = int(h * 0.25), int(h * 0.75)
    cx0, cx1 = int(w * 0.25), int(w * 0.75)
    center = gray[cy0:cy1, cx0:cx1]
    center_salience = float(center.std() - gray.std() * 0.5)
    faces = []
    try:
        cascade_path = str(Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml")
        cascade = cv2.CascadeClassifier(cascade_path)
        detected = cascade.detectMultiScale((gray * 255).astype(np.uint8), scaleFactor=1.1, minNeighbors=4, minSize=(max(12, w // 20), max(12, h // 20)))
        faces = [{"x": int(x), "y": int(y), "w": int(fw), "h": int(fh), "center_x": float((x + fw / 2) / w), "center_y": float((y + fh / 2) / h), "area_ratio": float((fw * fh) / (w * h))} for x, y, fw, fh in detected[:8]]
    except Exception:
        faces = []
    small = img.copy()
    small.thumbnail((160, 90))
    mobile_pixels = np.asarray(small).astype(np.float32) / 255.0
    mobile_gray = cv2.cvtColor((mobile_pixels * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    return {
        "width": w,
        "height": h,
        "aspect_ratio": round(w / h, 4),
        "brightness": brightness,
        "contrast": contrast,
        "saturation": saturation,
        "colorfulness": colorfulness,
        "edge_density": edge_density,
        "center_salience_proxy": center_salience,
        "face_count": len(faces),
        "faces": faces,
        "mobile_brightness": float(mobile_gray.mean()),
        "mobile_contrast": float(mobile_gray.std()),
    }


def dominant_palette(path: Path, colors: int = 5) -> list[dict[str, Any]]:
    img = Image.open(path).convert("RGB")
    img.thumbnail((160, 160))
    arr = np.asarray(img).reshape(-1, 3).astype(np.float32)
    if len(arr) == 0:
        return []
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(arr, colors, None, criteria, 3, cv2.KMEANS_PP_CENTERS)
    counts = np.bincount(labels.flatten(), minlength=colors)
    order = np.argsort(-counts)
    out = []
    total = max(1, len(arr))
    for idx in order:
        r, g, b = [int(x) for x in centers[idx]]
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        out.append({"rgb": [r, g, b], "hex": f"#{r:02x}{g:02x}{b:02x}", "share": float(counts[idx] / total), "hue": h * 360, "lightness": l, "saturation": s})
    return out


def analyze_thumbnail(path: Path) -> dict[str, Any]:
    result = image_metrics(path)
    result["dominant_palette"] = dominant_palette(path)
    return result


def write_index(rows: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
