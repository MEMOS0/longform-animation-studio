"""Failure Intelligence: compare future creative decisions with observed failure modes.

The system is intentionally transparent rather than oracle-like. A high risk score means
"this candidate resembles patterns that underperformed in the evidence base and lacks
patterns that overperformed"; it does not prove the candidate will fail.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

from .comparative import load_jsonl
from .features import title_features, flatten_theme
from .story_signals import count_signal

STOPWORDS = set("the a an and or but to of in for with on she he her his their they was were is are be been now then so until unaware because as at by from it its this that who whom whose into had have has".split())

DEFAULT_PATTERNS: list[dict[str, Any]] = [
    {
        "id": "revenge_without_belonging",
        "label": "Retribution dominates the promise while belonging/care is weak",
        "signals": ["revenge_retribution", "weak_family_child"],
        "evidence_strength": "moderate_observational",
        "archive_signal": "revenge_retribution mean log views/day was lower in the first Nov Drama comparison; counterexamples exist.",
        "risk_logic": "Nov Drama's largest hits often sell rescue, family acceptance, heirs, or protective love. Pure payback can feel colder and less rewatchable.",
        "mitigation": "Keep justice, but anchor it in a character or child the audience wants to see emotionally safe; show warmth before retaliation.",
    },
    {
        "id": "dark_generic_couple_thumbnail",
        "label": "Dark seductive couple imagery without a clear child/creature/status transformation hook",
        "signals": ["dark_thumbnail", "romance_mate", "weak_family_child", "weak_animal_child"],
        "evidence_strength": "visual_observational",
        "archive_signal": "Bottom-cohort thumbnails skew dark/red, couple-centric, sports-like, or visually generic; top cohort often shows luminous creature/family transformation.",
        "risk_logic": "If the thumbnail only says 'attractive couple', the viewer lacks a concrete curiosity gap and emotional stake.",
        "mitigation": "Make the impossible promise visible: child/heir, creature form, transformation, protector, or a striking before/after contrast.",
    },
    {
        "id": "hidden_identity_as_only_engine",
        "label": "Hidden identity is used as a static secret rather than an escalating dramatic engine",
        "signals": ["hidden_identity_or_secret", "no_reveal_escalation"],
        "evidence_strength": "hypothesis_requires_media_validation",
        "archive_signal": "Hidden identity correlates positively at title level, so its absence/presence alone cannot explain failure; execution likely matters.",
        "risk_logic": "A secret that only waits for a final reveal produces repetitive middle chapters.",
        "mitigation": "Every act should change who almost discovers the secret, what it costs, and what new conflict the partial reveal creates.",
    },
    {
        "id": "modern_power_arena_mismatch",
        "label": "Modern sports/billionaire/mafia power fantasy lacks the mythic creature-family draw",
        "signals": ["modern_wealth_power", "weak_family_child", "weak_dragon", "weak_wolf_werewolf", "weak_vampire", "weak_sea_mermaid"],
        "evidence_strength": "counterexample_challenged_observational",
        "archive_signal": "Racing/championship examples sit near the bottom, but the pregnant-wife millionaire modern story is a major hit; modern arena alone is not a failure cause.",
        "risk_logic": "Modern power fantasy appears risky only when it lacks the channel's child/heir/protector emotional anchor or clear mythic promise.",
        "mitigation": "Keep the modern arena only if the first minutes create legible injustice around a vulnerable child/heir/family stake; otherwise use a mythic/kinship hook or treat it as a deliberate outlier test.",
    },
    {
        "id": "lore_politics_overload_before_emotional_grounding",
        "label": "Court/clan mythology and political terminology arrive before a simple emotional wound-rescue loop",
        "signals": ["lore_overload_opening", "weak_opening_wound_care_loop"],
        "evidence_strength": "timestamped_casebook_observational",
        "archive_signal": "Underperforming wolf/panther casebooks show much higher lore-per-hour and lore-to-care ratios than top hits; examples include 1UB6EA3L7I4, _I5I1l7DP3E, and BeX5LHLqOEI.",
        "risk_logic": "Proper nouns, councils, clans, bloodlines, and rituals create cognitive load before the audience knows whom to love or what injustice to hate.",
        "mitigation": "Open with one visually legible victim, one act of cruelty, and one act of protection; let lore emerge only as it changes those stakes.",
    },
    {
        "id": "procedural_or_expository_opening",
        "label": "The first minutes are report/ceremony/exposition rather than an immediate dramatic event",
        "signals": ["expository_opening"],
        "evidence_strength": "timestamped_casebook_observational",
        "archive_signal": "BeX5LHLqOEI opens with an urgent report/selection machinery despite appealing animal-child imagery; hits more often open with peril, rejection, rescue, or transformation already happening.",
        "risk_logic": "Vertical mobile viewers decide quickly; static explanation delays the emotional question.",
        "mitigation": "Convert exposition into an event: someone is thrown out, saved, exposed, claimed, or transformed while the necessary facts are visible.",
    },
    {
        "id": "justice_without_warm_resolution",
        "label": "The ending delivers procedural punishment but little belonging, safety, reconciliation, or communal joy",
        "signals": ["unresolved_or_procedural_ending"],
        "evidence_strength": "timestamped_casebook_observational",
        "archive_signal": "1UB6EA3L7I4 ends in banishment/royal jurisdiction and a dying apology; stronger hits end in home, family acceptance, celebration, marriage, or communal safety.",
        "risk_logic": "Revenge satisfaction alone does not repay long-form suffering unless the protagonist's original wound is emotionally answered.",
        "mitigation": "After justice, explicitly dramatize what the protagonist gains: home, family, child safety, chosen love, public acceptance, or a transformed future.",
    },
    {
        "id": "adult_betrayal_escalates_into_misery_spiral",
        "label": "Sexual betrayal, pregnancy loss, coercion, or domestic violence escalates without early protection/agency",
        "signals": ["adult_misery_opening", "no_capability_progression"],
        "evidence_strength": "hypothesis_with_counterexample",
        "archive_signal": "1UB6EA3L7I4 and KsxgWoFS50I lean into sexual/domestic cruelty and underperform; however gkRXl9lDReY proves pregnancy betrayal can succeed when the premise is simple and the victim quickly gains a path forward.",
        "risk_logic": "The problem is not mature subject matter itself but prolonged helplessness and tonal claustrophobia before rescue or agency.",
        "mitigation": "Within the first act, give the victim an ally, plan, secret asset, or active decision; do not stack sexual humiliation merely for shock.",
    },
    {
        "id": "production_artifact_immersion_break",
        "label": "Censorship blur, sudden muting, over-loud music, or visible AI continuity artifacts interrupt emotional immersion",
        "signals": ["production_artifact_risk"],
        "evidence_strength": "comment_observational",
        "archive_signal": "Public comments repeatedly criticize blurring/censorship, missing sound, loud music, sudden cuts, and on-screen reup-protection artifacts even on otherwise liked stories.",
        "risk_logic": "Viewers can forgive imperfect AI animation more easily than being reminded they are watching a broken/generated artifact.",
        "mitigation": "Add audio/visual continuity QA gates: no unexplained muting, music under dialogue, no censorship mosaics unless unavoidable, no sudden emotional-state jumps, no watermark-like overlays.",
    },
    {
        "id": "suffering_repetition_without_progress",
        "label": "The heroine suffers repeatedly but the story does not convert suffering into capability or relationships",
        "signals": ["victimization", "no_capability_progression"],
        "evidence_strength": "hypothesis_requires_media_validation",
        "archive_signal": "Victimization is present in most titles, including hits; failure cannot be explained by victimization alone.",
        "risk_logic": "Humiliation only creates engagement when it opens a measurable injustice question and the protagonist gains allies/agency.",
        "mitigation": "Track every suffering scene: it must create a new alliance, capability, clue, or active decision; otherwise compress or remove it.",
    },
]


def tokens(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-zA-Z']+", text.lower()) if len(token) > 2 and token not in STOPWORDS]


def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    numerator = sum(a[x] * b[x] for x in common)
    da = math.sqrt(sum(x * x for x in a.values()))
    db = math.sqrt(sum(x * x for x in b.values()))
    return numerator / max(da * db, 1e-9)


def archive_index(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    index = []
    for row in rows:
        title = row.get("exact_title") or row.get("archive_title") or ""
        cohort = row.get("analysis", {}).get("cohort_by_age_adjusted_views", "unknown")
        index.append({
            "video_id": row.get("video_id"),
            "title": title,
            "cohort": cohort,
            "views_per_day": row.get("analysis", {}).get("views_per_day"),
            "token_counts": Counter(tokens(title)),
            "themes": [theme for theme in row.get("creative_features", {}).get("themes", {}) if flatten_theme(row, theme)],
        })
    return index


def nearest_archive_examples(candidate_text: str, rows: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    candidate_counts = Counter(tokens(candidate_text))
    scored = []
    for row in archive_index(rows):
        scored.append({**row, "similarity": cosine(candidate_counts, row["token_counts"])})
    return sorted(scored, key=lambda x: -x["similarity"])[:limit]


def candidate_flags(candidate_text: str, script_text: str = "") -> dict[str, bool]:
    features = title_features(candidate_text)
    themes = {name for name, value in features["themes"].items() if value["present"]}
    full = (candidate_text + "\n" + script_text).lower()
    reveal_mentions = len(re.findall(r"reveal|discover|expose|learns|finds out|transform", full))
    agency_mentions = len(re.findall(r"decides|chooses|protects|saves|learns|uses|earns|leads|escapes", full))
    opening_text = script_text[: max(1200, len(script_text) // 8)] if script_text else ""
    ending_text = script_text[-max(1200, len(script_text) // 8):] if script_text else ""
    opening_words = max(len(re.findall(r"[A-Za-z']+", opening_text)), 1)
    lore_per_1000_opening = count_signal(opening_text, "lore_mythology_density") / opening_words * 1000 if opening_text else 0
    opening_wound = count_signal(opening_text, "wound_or_humiliation")
    opening_care = count_signal(opening_text, "care_belonging_protection")
    ending_wound = count_signal(ending_text, "wound_or_humiliation") + count_signal(ending_text, "threat_or_violence")
    ending_warmth = count_signal(ending_text, "care_belonging_protection") + count_signal(ending_text, "justice_reversal_payoff")
    flags = {name: name in themes for name in themes}
    flags.update({
        "hidden_identity_or_secret": bool(features["hidden_identity_or_secret"]["present"]),
        "victimization": bool(features["victimization"]["present"]),
        "status_reversal": bool(features["status_reversal"]["present"]),
        "setup_then_reversal": bool(features["title_structure"]["setup_then_reversal"]),
        "dark_thumbnail": "dark thumbnail" in full or "red black thumbnail" in full,
        "no_reveal_escalation": reveal_mentions < 3 if script_text else False,
        "no_capability_progression": agency_mentions < 4 if script_text else False,
        "lore_overload_opening": lore_per_1000_opening >= 8 if script_text else False,
        "weak_opening_wound_care_loop": bool(script_text and (opening_wound == 0 or opening_care == 0)),
        "expository_opening": bool(script_text and re.search(r"(report|council|ceremony|selection|clan council|royal court|as you know|years ago)", opening_text.lower())),
        "adult_misery_opening": bool(script_text and re.search(r"pregnan|cheat|affair|miscarriage|termination|forced|coerc|domestic|rape|sexual", opening_text.lower())),
        "unresolved_or_procedural_ending": bool(script_text and ending_wound >= max(ending_warmth + 2, 4) and not re.search(r"belonging payoff|publicly accept|family acceptance|chosen love|child safety|celebration|transformed future|home", full)),
        "production_artifact_risk": bool(re.search(r"censor|blur|mosaic|muted|missing sound|loud music|audio dropout|watermark|sudden cut|continuity error", full)),
    })
    for theme in ("family_child", "animal_child", "dragon", "wolf_werewolf", "vampire", "sea_mermaid", "romance_mate", "modern_wealth_power", "revenge_retribution"):
        flags.setdefault(theme, theme in themes)
        flags[f"weak_{theme}"] = not flags.get(theme, False)
    return flags


def evaluate_patterns(flags: dict[str, bool], patterns: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    patterns = patterns or DEFAULT_PATTERNS
    matched = []
    for pattern in patterns:
        hits = [signal for signal in pattern["signals"] if flags.get(signal)]
        if len(hits) == len(pattern["signals"]):
            matched.append({**pattern, "matched_signals": hits})
    return matched


def evaluate_candidate(candidate_text: str, rows: list[dict[str, Any]], script_text: str = "") -> dict[str, Any]:
    flags = candidate_flags(candidate_text, script_text)
    neighbors = nearest_archive_examples(candidate_text + "\n" + script_text[:4000], rows)
    matched = evaluate_patterns(flags)
    failure_neighbors = [n for n in neighbors if n["cohort"] == "underperforming"]
    success_neighbors = [n for n in neighbors if n["cohort"] == "outperforming"]
    failure_pressure = sum(n["similarity"] for n in failure_neighbors)
    success_pressure = sum(n["similarity"] for n in success_neighbors)
    pattern_pressure = len(matched) * 0.18
    risk = max(0.0, min(1.0, 0.35 + failure_pressure - 0.45 * success_pressure + pattern_pressure))
    return {
        "candidate": candidate_text,
        "risk_score_0_to_1": round(risk, 3),
        "confidence": "low_until_script_and_media-evidence comparison is complete",
        "matched_failure_patterns": matched,
        "nearest_archive_examples": [
            {k: v for k, v in neighbor.items() if k != "token_counts"} for neighbor in neighbors
        ],
        "positive_missing_or_weak": missing_positive_mechanisms(flags),
        "decision_guidance": guidance(risk, matched),
        "causal_boundary": "This is pattern-matching against public outcomes and extracted creative signals; it is not a causal predictor of CTR, retention, or audience response.",
    }


def missing_positive_mechanisms(flags: dict[str, bool]) -> list[str]:
    missing = []
    if not flags.get("hidden_identity_or_secret"):
        missing.append("No strong hidden identity/secret hook detected; Nov Drama hits often use one, though this is not mandatory.")
    if not flags.get("family_child") and not flags.get("animal_child"):
        missing.append("No child/heir/creature emotional anchor detected; this is currently one of the strongest archive-level positive signals.")
    if not flags.get("status_reversal"):
        missing.append("No explicit status reversal detected in the surface promise.")
    if not any(flags.get(theme) for theme in ("dragon", "wolf_werewolf", "vampire", "sea_mermaid")):
        missing.append("No clear mythic creature lane detected; test whether the concept matches the channel audience's demand.")
    return missing


def guidance(risk: float, matched: list[dict[str, Any]]) -> list[str]:
    actions = []
    if risk >= 0.65:
        actions.append("Do not greenlight in current form; redesign the emotional engine or run a cheap validation artifact first.")
    elif risk >= 0.45:
        actions.append("Proceed only after targeted revision; the concept has meaningful resemblance to underperforming patterns.")
    else:
        actions.append("Concept does not trigger strong archive-level failure alarms, but retention-safe execution still requires scene-level proof.")
    for pattern in matched:
        actions.append(f"Mitigate {pattern['id']}: {pattern['mitigation']}")
    return actions


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# Failure Intelligence evaluation",
        "",
        f"Candidate: {result['candidate']}",
        f"Risk score: {result['risk_score_0_to_1']} ({result['confidence']})",
        "",
        result["causal_boundary"],
        "",
        "## Matched failure patterns",
    ]
    if not result["matched_failure_patterns"]:
        lines.append("- None triggered by current transparent rules.")
    for pattern in result["matched_failure_patterns"]:
        lines += [
            f"- **{pattern['id']}** ({pattern['evidence_strength']}): {pattern['label']}",
            f"  - Archive signal: {pattern['archive_signal']}",
            f"  - Mitigation: {pattern['mitigation']}",
        ]
    lines += ["", "## Nearest archive examples", "", "|video|cohort|views/day|similarity|title|", "|---|---|---:|---:|---|"]
    for row in result["nearest_archive_examples"]:
        vpd = row.get("views_per_day")
        lines.append(f"|[{row['video_id']}](https://www.youtube.com/watch?v={row['video_id']})|{row['cohort']}|{vpd:.0f}|{row['similarity']:.2f}|{row['title'][:90].replace('|','/')}|" if isinstance(vpd, (int, float)) else f"|[{row['video_id']}](https://www.youtube.com/watch?v={row['video_id']})|{row['cohort']}|n/a|{row['similarity']:.2f}|{row['title'][:90].replace('|','/')}|")
    lines += ["", "## Positive mechanisms missing or weak"] + [f"- {x}" for x in result["positive_missing_or_weak"]]
    lines += ["", "## Decision guidance"] + [f"- {x}" for x in result["decision_guidance"]]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", default="data/processed/novdrama_enriched.jsonl")
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--script-file", default="")
    parser.add_argument("--output", default="data/processed/failure_intelligence_evaluation.md")
    args = parser.parse_args()
    rows = load_jsonl(Path(args.archive))
    # comparative analysis rows may not have been written back to JSONL; load JSON rows if needed
    if rows and "analysis" not in rows[0] and Path("data/processed/novdrama_analysis_rows.json").exists():
        rows = json.loads(Path("data/processed/novdrama_analysis_rows.json").read_text(encoding="utf-8"))
    script_text = Path(args.script_file).read_text(encoding="utf-8") if args.script_file else ""
    result = evaluate_candidate(args.candidate, rows, script_text)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(result), encoding="utf-8")
    json_output = output.with_suffix(".json")
    json_output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
