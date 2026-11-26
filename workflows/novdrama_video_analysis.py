import asyncio
import json
from pathlib import Path

BRANCH = "devin/1764170700-failure-intelligence-foundation"
REPO = "MEMOS0/longform-animation-studio"

ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "video_id": {"type": "string"},
        "evidence_quality": {"type": "string"},
        "one_sentence_verdict": {"type": "string"},
        "opening_30_seconds": {"type": "string"},
        "first_5_minutes": {"type": "string"},
        "full_story_structure": {"type": "string"},
        "character_psychology": {"type": "string"},
        "direction_visual_audio": {"type": "string"},
        "success_mechanisms": {"type": "array", "items": {"type": "string"}},
        "failure_mechanisms": {"type": "array", "items": {"type": "string"}},
        "counterintuitive_findings": {"type": "array", "items": {"type": "string"}},
        "timestamped_evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "time": {"type": "string"},
                    "observation": {"type": "string"},
                    "interpretation": {"type": "string"},
                },
                "required": ["time", "observation", "interpretation"],
            },
        },
        "production_lessons": {"type": "array", "items": {"type": "string"}},
        "uncertainties": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "video_id", "evidence_quality", "one_sentence_verdict", "opening_30_seconds", "first_5_minutes",
        "full_story_structure", "character_psychology", "direction_visual_audio", "success_mechanisms",
        "failure_mechanisms", "counterintuitive_findings", "timestamped_evidence", "production_lessons", "uncertainties",
    ],
}


def select_videos():
    rows = json.loads(Path("C:/Users/Administrator/repos/longform-animation-studio/data/processed/novdrama_analysis_rows.json").read_text(encoding="utf-8"))
    by_id = {row["video_id"]: row for row in rows}
    # User-named references plus outcome-stratified/theme-diverse examples.
    ids = [
        "vYNuKn6GiaE",  # largest hit: dragon babies / betrayal
        "v03oauoFveU",  # major hit: hidden dragon daughter
        "ULJ7-z1zm6M",  # major hit: orphan adopted by dragon family
        "jRa3_WZYDdY",  # hit: pet is wolf king / true love
        "0ofXaXWcfi0",  # recent hit: male lead rescued by mermaid
        "NnPZaWSGYuc",  # failure: cursed witch / dragon queen
        "KsxgWoFS50I",  # user-cited failure: sacrificed girl becomes goddess
        "rtTbEcFdnZQ",  # user-cited failure: beggar is supreme dragon king
        "_I5I1l7DP3E",  # failure: magic mirror / wolf king kiss
        "ZhAYjMLvlqc",  # failure despite dragon prince/children surface elements
        "xJUN_KOCnME",  # failure/outlier: racing championship
        "Prsthri0ktA",  # oldest failure: hybrid wolf ancestor
    ]
    return [(video_id, by_id.get(video_id, {})) for video_id in ids]


def prompt_for(video_id, row):
    title = row.get("exact_title") or row.get("archive_title") or "unknown"
    analysis = row.get("analysis", {})
    cohort = analysis.get("cohort_by_age_adjusted_views", "unknown")
    vpd = analysis.get("views_per_day")
    views = analysis.get("views")
    return f'''You are one specialist analyst inside a comparative long-form animation study. Analyze exactly one Nov Drama video end-to-end and report reusable creative mechanisms. Do not edit the repo, do not open a PR, and do not stop early.

Video: {video_id}
Title: {title}
Public outcome at snapshot: {views} views, {vpd} views/day, cohort={cohort}. Treat this as observational only.

Repository: {REPO}. It is cloned for you. Immediately run:
1. git fetch origin {BRANCH}
2. git checkout {BRANCH}
3. git pull origin {BRANCH}
4. python -m pip install -e . pytest

Then obtain actual audiovisual evidence:
- Use `python tools/download_piped_archive.py --ids {video_id} --workers 1 --media-dir <local media dir> --raw-dir data/raw/piped` to download the public low-resolution progressive stream and subtitles through the configured Piped-compatible API.
- If the default API fails, investigate public Piped instances or metadata endpoints. Do not use credentials, do not bypass access controls, and do not pretend you watched media you could not obtain.
- Run `python -m studio.media_analysis <media> --subtitle <ttml> --output-dir data/processed/media/{video_id} --video-id {video_id}`.

Mandatory analysis standard:
- Inspect ALL generated contact sheets visually, not only the first one. The videos are often vertical/mobile-native; do not treat stretched thumbnails as accurate.
- Read the timestamped timeline/second-level measurements and subtitle alignment, but do not reduce the analysis to transcript.
- If useful, extract additional short clips/frames/audio measurements with ffmpeg/Python.
- Watch/inspect the video as closely as your tools allow from beginning to end. Explicitly state any coverage gaps.
- Analyze first 30 seconds, first 5 minutes, middle escalation, final emotional payoff, dialogue, character psychology, visual direction, sound/music, editing rhythm, and mobile readability.
- Focus on why the storytelling works or fails, not merely what happens.
- Compare against this hypothesis set: (a) child/family/belonging outperforms cold revenge, (b) hidden identity only works when it escalates, (c) dense mythology can overwhelm, (d) adult sexualized coercion may narrow audience, (e) fantasy spectacle must be tied to emotional stakes, (f) title/thumbnail mismatch may explain failure better than script quality.
- Actively seek evidence AGAINST those hypotheses. Report counterintuitive findings.
- Use only short quotation fragments when needed; do not reproduce large transcript sections.
- Return at least 12 timestamped evidence items spread across the whole runtime, each with observation + interpretation.
- Production lessons must be actionable for original films, not instructions to copy this plot.

Structured output: fill every schema field honestly. Set evidence_quality to explain exactly what media coverage was achieved.'''


async def analyze_one(item):
    video_id, row = item
    return await agent(
        prompt_for(video_id, row),
        phase="analyze-videos",
        schema=ANALYSIS_SCHEMA,
        label=video_id,
        repos=[REPO],
        mode="normal",
        soft_time_limit_minutes=45,
    )


async def main():
    videos = select_videos()
    await register_workflow({
        "name": "novdrama-comparative-video-analysis",
        "description": "End-to-end visual/audio/narrative analysis of representative Nov Drama hits and failures",
        "soft_time_limit_minutes": 45,
        "phases": [
            {
                "title": "analyze-videos",
                "detail": "One specialist agent per representative video; every agent inspects the actual media evidence end-to-end",
                "count": len(videos),
                "labels": [video_id for video_id, _ in videos],
                "soft_time_limit_minutes": 45,
            }
        ],
    })
    log(f"Starting {len(videos)} video-analysis agents")
    results = await parallel([(lambda item=item: analyze_one(item)) for item in videos])
    for result in results:
        log(f"{result['video_id']}: {result['one_sentence_verdict']}")
    log("COMPARATIVE_VIDEO_ANALYSIS_RESULTS=" + json.dumps(results, ensure_ascii=False))


asyncio.run(main())
