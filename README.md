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
  - `failure_intelligence.py` — transparent failure-pattern matching for future ideas/scripts
  - `cli.py` — command-line entry points
- `tools/download_piped_archive.py` — provenance-preserving media/subtitle acquisition through a configurable Piped-compatible public API
- `data/` — local evidence outputs; raw media should generally stay out of git
- `knowledge/` — durable research findings, craft notes, and channel-specific evidence interpretations
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

# 5. Stress-test a new idea against failure intelligence
python -m studio.cli evaluate-idea \
  --candidate "They abandoned the forbidden child, unaware she was the dragon heir" \
  --script-file drafts/premise.md
```

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

The initial archive contains 48 public videos. Metadata, thumbnails, exact dates/views, subtitles, and local low-resolution audiovisual copies are being converted into timestamped evidence. Preliminary archive-level patterns are already visible, but they remain observational until validated against scene-level analysis and additional channels.

Important early caveat: cumulative public views are strongly age- and recommendation-dependent. Use `views_per_day` only as a discovery metric, not as truth about retention or CTR.

## Contributing discipline

- Add mechanisms, not superficial tropes.
- Every creative rule must link to evidence or be labeled a hypothesis.
- Prefer transparent heuristics over fake precision.
- Make adapters replaceable; do not hard-wire the studio to one video generator, voice provider, or data source.
- Do not commit downloaded copyrighted media or secrets. Commit analysis artifacts, schemas, code, and evidence summaries instead.
