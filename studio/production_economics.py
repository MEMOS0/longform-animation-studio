"""Long-form generation cost estimation.

Rates are documentation-audited snapshots, not quotes. Recheck provider docs before spending.
"""
from __future__ import annotations

from typing import Any

DOCUMENTED_USD_PER_SECOND = {
    "gemini_omni_flash_1_2_low_tier": 0.02,
    "grok_imagine_1_5_lite_low_tier": 0.02,
    "gen4_turbo": 0.05,
    "wan3_low_tier": 0.05,
    "seedance2_mini_low_tier": 0.07,
    "kling_4_flash_low_tier": 0.094,
    "gen4_5": 0.12,
    "kling_4_low_tier": 0.157,
    "aleph2": 0.28,
}

SOURCE = "knowledge/production/video-generation-provider-audit.md"


def estimate_video_budget(target_minutes: float | int | None, generation_to_final_ratio: float = 8.0) -> dict[str, Any]:
    if not target_minutes:
        return {"status": "unknown", "warnings": ["target_minutes is required for production economics"]}
    finished_seconds = float(target_minutes) * 60
    generated_seconds = finished_seconds * generation_to_final_ratio
    scenarios = []
    for model, rate in sorted(DOCUMENTED_USD_PER_SECOND.items(), key=lambda item: item[1]):
        scenarios.append({
            "model_or_lane": model,
            "documented_usd_per_second": rate,
            "finished_minutes_cost_if_single_pass": round(finished_seconds * rate, 2),
            "iteration_adjusted_cost_estimate": round(generated_seconds * rate, 2),
        })
    mixed_generated_seconds = generated_seconds
    mixed_cost = mixed_generated_seconds * (0.70 * 0.02 + 0.20 * 0.05 + 0.10 * 0.12)
    return {
        "status": "documentation_estimate_not_quote",
        "target_minutes": target_minutes,
        "generation_to_final_ratio": generation_to_final_ratio,
        "single_pass_scenarios": scenarios,
        "mixed_pipeline_example": {
            "assumption": "70% cheap draft/blocking lane at $0.02/sec, 20% mid-cost lane at $0.05/sec, 10% hero-shot lane at $0.12/sec",
            "iteration_adjusted_cost_estimate": round(mixed_cost, 2),
        },
        "warnings": [
            "iteration ratio is a planning assumption, not a measurement",
            "input/reference video billing can increase cost on some providers",
            "voice, music, edit, QA, and labor are excluded",
            "recheck exact provider pricing/terms before any spend",
        ],
        "production_rules": [
            "do not generate the full film linearly; decompose into shots",
            "validate character consistency with a cheap fixed smoke pack first",
            "use expensive models only for hero/motion-critical shots",
            "track actual generated seconds vs final seconds as a KPI",
        ],
        "evidence": SOURCE,
    }
