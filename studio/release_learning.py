"""Post-release learning loop for self-improving studio decisions.

Public outcomes remain observational. The loop compares release evidence with
pre-release warnings and produces explicit revision rules rather than pretending
to know CTR/retention causality.
"""
from __future__ import annotations

from typing import Any


def percentile_rank(values: list[float], value: float) -> float | None:
    vals = sorted(v for v in values if v is not None)
    if not vals:
        return None
    return round(sum(v <= value for v in vals) / len(vals), 3)


def release_postmortem(
    release: dict[str, Any],
    preproduction: dict[str, Any] | None = None,
    cohort_rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    views = float(release.get("views") or 0)
    age_days = max(0.25, float(release.get("age_days") or 1))
    vpd = views / age_days
    cohort_rows = cohort_rows or []
    cohort_vpds = [float(r.get("views_per_day") or r.get("views_per_day_estimate") or 0) for r in cohort_rows]
    pct = percentile_rank(cohort_vpds, vpd)
    pre = preproduction or {}
    warnings = []
    for section in ("format_strategy", "opening_conversion_quality", "channel_contract_fit"):
        value = pre.get(section, {})
        warnings.extend(f"{section}: {w}" for w in value.get("warnings", []))
    failure = pre.get("failure_intelligence", {})
    matched = failure.get("matched_patterns", [])
    title_risks = []
    for row in pre.get("title_packaging", {}).get("existing_title_critiques", []):
        title_risks.extend(row.get("critique", {}).get("risks", []))
    outcome = "insufficient_data"
    if pct is not None:
        if pct >= 0.75:
            outcome = "outperforming_cohort"
        elif pct <= 0.25:
            outcome = "underperforming_cohort"
        else:
            outcome = "middle_cohort"
    hypotheses = []
    revisions = []
    if outcome == "underperforming_cohort":
        if warnings:
            hypotheses.append("pre-release warnings may have identified real structural/packaging risks")
            revisions.append("do not greenlight similar projects until the same warning classes are resolved or deliberately tested")
        if matched:
            hypotheses.append("matched failure-intelligence patterns may have repeated past failure mechanics")
            revisions.append("increase penalty weight for repeated matched patterns in future evaluations")
        if title_risks:
            hypotheses.append("title packaging may have obscured the vulnerable/relational hook")
            revisions.append("test one title exposing the core wound/protector relationship more directly")
        if not (warnings or matched or title_risks):
            hypotheses.append("underperformance despite clean pre-release gates; investigate packaging mismatch, topic demand, channel fit, upload timing, or execution quality")
            revisions.append("create a falsification review comparing first minute, first five minutes, thumbnail, and title against same-channel hits")
    elif outcome == "outperforming_cohort":
        hypotheses.append("the release may validate the selected emotional engine/channel contract, but not prove causality")
        revisions.append("extract the minimal reusable mechanism and test whether it repeats in a different surface world")
    else:
        hypotheses.append("available evidence is not yet sufficient for a strong hit/failure interpretation")
        revisions.append("collect more age-matched data, audience comments, CTR/impressions, and retention before revising rules")
    return {
        "video_id": release.get("video_id"),
        "title": release.get("title"),
        "views": views,
        "age_days": age_days,
        "views_per_day": round(vpd, 2),
        "cohort_percentile_views_per_day": pct,
        "outcome_vs_cohort": outcome,
        "preproduction_warnings": warnings,
        "matched_failure_patterns": [m.get("id", str(m)) if isinstance(m, dict) else str(m) for m in matched],
        "failure_hypotheses": hypotheses,
        "revision_rules": revisions,
        "required_private_metrics": ["impressions", "CTR by surface", "average percentage viewed", "retention curve", "traffic sources", "subscriber gain"],
        "causal_boundary": "Public views/day cannot isolate title, thumbnail, story, execution, or recommendation effects.",
    }
