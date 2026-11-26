# longform-animation-studio

Evidence-driven intelligence and production infrastructure for original long-form animated films.

This repository is not a prompt collection. It is a reusable studio system for learning from real market evidence, detecting failure patterns before production, designing original stories, and carrying those stories through screenplay, direction, audio, edit, QA, release, and post-release learning.

## Core principles

1. **Evidence before taste.** Public outcomes are noisy, but they are still useful evidence when compared carefully inside a controlled channel cohort.
2. **Failure intelligence is first-class.** Knowing what not to repeat is as valuable as imitating hits.
3. **No causal overclaiming.** Without CTR, impressions, retention curves, and traffic-source data, every conclusion must be labeled observational, inferential, or hypothetical.
4. **Audience psychology over surface tropes.** Dragons, royalty, and hidden identities are not magic ingredients; they work when they create vulnerability, belonging, power reversal, curiosity, and emotional payoff.
5. **Story decisions propagate.** A premise affects title, thumbnail, character design, scene order, dialogue, sound, edit rhythm, and production cost. The system keeps those dependencies explicit.
6. **Originality with market awareness.** We learn mechanisms, not plots to copy.

## Repository map

- `studio/` — reusable Python package
  - `youtube_archive.py` — public channel metadata/thumbnail ingestion with provenance tiers
  - `features.py` — auditable title/theme/thumbnail feature extraction
  - `comparative.py` — age-adjusted cohort comparison, hypothesis tables, montage evidence
  - `media_analysis.py` — second-resolution visual/audio/subtitle timeline extraction
  - `story_signals.py` — transparent wound/care/justice/lore/threat signal extraction
  - `dialogue_analysis.py` — sentence-shape, exposition, pressure, care, question-ratio analysis
  - `failure_intelligence.py` — transparent failure-pattern matching for future ideas/scripts
  - `format_strategy.py` — duration/episode/compilation-aware release-format guidance
  - `channel_contracts.py` — machine-readable audience/channel fit checks
  - `production.py` — schema validation and pre-greenlight gates for premise/architecture/scene artifacts
  - `production_economics.py` — documented per-second generation cost scenarios and iteration-adjusted budget planning
  - `shot_pipeline.py` — draft/mid/hero key-shot decomposition, continuity dependencies, and generation-ratio discipline
  - `providers.py` — validated/documented AI generation provider inventory boundaries
  - `thumbnail_intelligence.py` / `thumbnail_concepts.py` — visual packaging metrics, reference classification, and original concept critique
  - `cli.py` — command-line entry points
- `tools/download_piped_archive.py` — provenance-preserving media/subtitle acquisition through a configurable Piped-compatible public API
- `tools/batch_media_analysis.py` — archive-wide timestamped media analysis
- `tools/build_casebooks.py` — per-video timestamped audiovisual/narrative casebooks
- `tools/compare_casebooks.py` — hit/middle/failure cohort comparison across casebook metrics
- `tools/compare_dialogue.py` — cohort comparison of subtitle sentence shape and exposition density
- `tools/repair_audio_metrics.py` — fast correction of cached audio silence/RMS evidence
- `data/` — local evidence outputs; raw media should generally stay out of git
- `knowledge/` — durable research findings, craft notes, thumbnail intelligence, and channel-specific evidence interpretations
- `thumbnails/` — persistent thumbnail reference archive, indices, and comparative montages
- `schemas/` — data contracts for handoff between agents and production stages
- `.devin/skills/longform-animation-studio/SKILL.md` — operating discipline for AI agents using this repository
- `tests/` — regression tests for core logic

## Evidence tiers

Every analysis must state which tier it uses:

| Tier | Evidence | Allowed use |
|---|---|---|
| 0 | Public title, thumbnail, upload date, duration, cumulative views | market-pattern hypotheses only |
| 1 | Exact watch-page/API metadata, comments, likes when available | stronger audience-demand hypotheses, still not causal |
| 2 | Timestamped subtitle/dialogue aligned to video | narrative-structure evidence, not visual evidence by itself |
| 3 | Second-resolution visual frames, shot/motion/color/composition evidence, audio features | audiovisual craft analysis |
| 4 | Human/agent-reviewed scene interpretation with timestamped evidence | creative-mechanism conclusions |
| 5 | Private retention, CTR, impressions, traffic-source data | causal-adjacent performance diagnosis when available |

Never present lower-tier inference as higher-tier fact.

## Quickstart

```bash
python -m pip install -e .
python -m pytest -q
```

Typical analysis flow:

```bash
# 1. Build/refresh archive metadata and thumbnails
python -m studio.cli collect-archive --channel-json /path/to/channel.json

# 2. Extract title/theme/thumbnail features
python -m studio.cli enrich-archive data/raw/novdrama_archive.jsonl data/processed/novdrama_enriched.jsonl

# 3. Compare age-adjusted cohorts and produce evidence tables/montage
python -m studio.cli compare data/processed/novdrama_enriched.jsonl data/processed

# 4. Extract a timestamped audiovisual timeline for one downloaded video
python -m studio.cli analyze-media /path/to/video.mp4 \
  --subtitle /path/to/subtitles.ttml \
  --output-dir data/processed/media/VIDEO_ID \
  --video-id VIDEO_ID

# 5. Build archive-wide casebooks after batch media analysis
python tools/batch_media_analysis.py --media-dir /path/to/downloaded-videos
python tools/build_casebooks.py
python tools/compare_casebooks.py
python tools/compare_dialogue.py

# 6. Stress-test a new idea against failure intelligence
python -m studio.cli evaluate-idea \
  --candidate "They abandoned the forbidden child, unaware she was the dragon heir" \
  --script-file drafts/premise.md

# 8. Close the learning loop after release
python -m studio.cli release-postmortem \n  --release release.json \n  --preproduction evaluation.json \n  --cohort cohort_rows.json \n  --output postmortem.json

# 7. Validate machine-readable production artifacts before greenlight
python -m studio.cli evaluate-project \
  --premise examples/stormglass_keepers/premise.json \
  --architecture examples/stormglass_keepers/architecture.json \
  --scenes examples/stormglass_keepers/scenes \
  --output examples/stormglass_keepers/evaluation.json
```

## Expanded market evidence status

The system now extends beyond Nov Drama into Epic AI Films, Ironcrest, FablePop, RIFTBORN, The Next Show, Korean/Crateh microdrama, and recent low-subscriber breakout channels. Durable entry points:

- `knowledge/market/ironcrest-deep-dive.md`
- `knowledge/market/epic-deep-dive.md`
- `knowledge/market/cross-channel-hit-failure-deep-dives.md`
- `knowledge/market/recent-breakout-media-deep-dive.md`
- `knowledge/market/breakout-within-channel-media-comparison.md`
- `knowledge/market/format-duration-performance.md`
- `knowledge/thumbnails/breakout-within-channel-thumbnail-comparison.md`
- `knowledge/production/video-generation-provider-audit.md`
- `knowledge/craft/advanced-screenplay-direction-retention.md`
- `knowledge/craft/scene-writing-laboratory.md`

Key correction from recent comparisons: strong openings are not sufficient. Minutes 1–5 must convert the hook into wound/vulnerability + protective counterforce + antagonistic pressure + payoff promise. Production evaluation machine-checks this as `opening_conversion_quality`.

## Example end-to-end project

`examples/stormglass_keepers/` contains an original creature-protection feature concept generated through the studio system: premise packet, 8-sequence architecture, 8 scene-screenplay units, and `production_evaluation.json`. At the current checkpoint it passes schema validation, Failure Intelligence, opening conversion, format strategy, and channel-contract fit with zero structural warnings, and now includes a draft/mid/hero shot-pipeline plan. It is a proof-of-work example for handoff, not a finished film.

## What the system is for

Before any film is produced, an agent should be able to answer:

- Why would a viewer click this rather than another fantasy melodrama?
- Why would they keep watching after 30 seconds, 5 minutes, 30 minutes, and 80 minutes?
- Which emotional promise is being made, and is it visible in the thumbnail/title/first scene?
- Which past failures does this resemble structurally rather than superficially?
- What specific evidence supports the chosen theme, protagonist, transformation, and ending?
- Which scenes are expensive but narratively weak?
- What can fail in character consistency, lip sync, emotional continuity, sound, pacing, or edit comprehension?

## Current Nov Drama evidence status

The initial archive contains 48 public videos. At the current checkpoint, 47 downloadable videos have second-resolution audiovisual timelines; 46 scored videos have archive-wide casebook and dialogue cohort comparisons. The repository commits aggregate cohort outputs plus representative hit/failure sample casebooks (`vYNuKn6GiaE`, `a2pydTch_Tg`); the other generated per-video casebooks are reproducible locally with `tools/build_casebooks.py` and are intentionally not committed as bulk generated artifacts. Representative hit/failure videos have direct timestamped visual audit notes in `knowledge/nov-drama/comparative-findings.md`. One video (`jRa3_WZYDdY`) remains inaccessible through the current public Piped-compatible endpoint and must not be treated as watched.

Important early caveat: cumulative public views are strongly age- and recommendation-dependent. Use `views_per_day` only as a discovery metric, not as truth about retention or CTR.

## Contributing discipline

- Add mechanisms, not superficial tropes.
- Every creative rule must link to evidence or be labeled a hypothesis.
- Prefer transparent heuristics over fake precision.
- Make adapters replaceable; do not hard-wire the studio to one video generator, voice provider, or data source.
- Do not commit downloaded copyrighted media or secrets. Commit analysis artifacts, schemas, code, and evidence summaries instead.
