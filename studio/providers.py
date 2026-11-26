"""Provider inventory contracts for AI-assisted production.

This module deliberately separates capability inventory from artifact validation. A provider
being reachable is not evidence that it can produce usable long-form animation.
"""
from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ProviderSpec:
    provider: str
    modality: str
    models: tuple[str, ...]
    env_required: tuple[str, ...]
    validation_status: str
    evidence_path: str = ""
    operational_notes: tuple[str, ...] = field(default_factory=tuple)


PROVIDERS: tuple[ProviderSpec, ...] = (
    ProviderSpec(
        provider="cloudflare_workers_ai",
        modality="text_generation",
        models=("@cf/openai/gpt-oss-20b", "@cf/mistralai/mistral-small-3.1-24b-instruct", "@cf/meta/llama-4-scout-17b-16e-instruct"),
        env_required=("CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN"),
        validation_status="smoke_passed_2026-11-26",
        evidence_path="knowledge/production/ai-provider-inventory.md",
        operational_notes=("llama-3.2 vision model requires explicit license acceptance; do not accept on user's behalf",),
    ),
    ProviderSpec(
        provider="cloudflare_workers_ai",
        modality="text_to_image",
        models=("@cf/black-forest-labs/flux-1-schnell", "@cf/black-forest-labs/flux-2-klein-4b", "@cf/leonardo/phoenix-1.0"),
        env_required=("CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN"),
        validation_status="flux-1-schnell smoke passed through temporary worker binding; production QA not complete",
        evidence_path="knowledge/production/ai-provider-inventory.md",
        operational_notes=("Cloudflare MCP execute bridge does not directly run binary-generation models",),
    ),
    ProviderSpec(
        provider="cloudflare_workers_ai",
        modality="text_to_speech",
        models=("@cf/deepgram/aura-2-en", "@cf/deepgram/aura-1"),
        env_required=("CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN"),
        validation_status="aura-2-en smoke passed through temporary worker binding; production voice QA not complete",
        evidence_path="knowledge/production/ai-provider-inventory.md",
        operational_notes=("omit container when encoding=mp3",),
    ),
    ProviderSpec(
        provider="cloudflare_workers_ai",
        modality="video_generation",
        models=(),
        env_required=("CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN"),
        validation_status="no video-generation model visible in catalog audit on 2026-11-26",
        evidence_path="knowledge/production/ai-provider-inventory.md",
    ),
    ProviderSpec(
        provider="elevenlabs_browser_session",
        modality="voice_generation",
        models=("Dan / Eleven v4 browser-session workflow",),
        env_required=(),
        validation_status="historically validated on user's PC, unavailable in this VM-only session",
        operational_notes=("do not use local PC unless the user explicitly re-enables local access",),
    ),
)


def inventory() -> list[dict[str, Any]]:
    rows = []
    for spec in PROVIDERS:
        missing = [name for name in spec.env_required if not os.environ.get(name)]
        rows.append({
            "provider": spec.provider,
            "modality": spec.modality,
            "models": list(spec.models),
            "env_required": list(spec.env_required),
            "env_missing": missing,
            "credential_state": "missing" if missing and spec.env_required else ("not_required_or_external_session" if not spec.env_required else "present"),
            "validation_status": spec.validation_status,
            "evidence_path": spec.evidence_path,
            "operational_notes": list(spec.operational_notes),
        })
    return rows


def cloudflare_request(path: str, method: str = "GET", body: dict[str, Any] | None = None, timeout: int = 120) -> dict[str, Any]:
    """Minimal direct Cloudflare API client for environments with explicit credentials.

    The current Devin session may authenticate through MCP without exposing a token to the
    shell; in that case this client correctly reports missing credentials rather than pretending
    they exist. Never log token values.
    """
    account = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not account or not token:
        raise RuntimeError("missing CLOUDFLARE_ACCOUNT_ID or CLOUDFLARE_API_TOKEN in shell environment")
    url = f"https://api.cloudflare.com/client/v4/accounts/{account}/{path.lstrip('/')}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "User-Agent": "longform-animation-studio/0.1"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


def render_inventory(rows: list[dict[str, Any]]) -> str:
    lines = ["# AI provider inventory", "", "| provider | modality | credential state | validation |", "|---|---|---|---|"]
    for row in rows:
        lines.append(f"| `{row['provider']}` | {row['modality']} | {row['credential_state']} | {row['validation_status']} |")
    lines.extend(["", "Credential state only says whether shell environment variables exist; it never prints secret values.", "See `knowledge/production/ai-provider-inventory.md` for audited smoke-test evidence and caveats."])
    return "\n".join(lines) + "\n"


def write_inventory(output_json: Path, output_md: Path) -> list[dict[str, Any]]:
    rows = inventory()
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps({"providers": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(render_inventory(rows), encoding="utf-8")
    return rows
