# Longform Animation Studio

A reusable evidence-driven production system for planning, writing, directing, packaging, and reviewing long-form animated films. This is **not** a prompt collection and not merely a Nov Drama report. The repository is designed so another AI agent can inherit the accumulated market research, failure intelligence, craft rules, machine checks, thumbnail references, and production discipline.

## Start here

1. Read `.devin/skills/longform-animation-studio/SKILL.md` first. It is the operating manual for an AI agent acting as a small studio.
2. Read `CONTINUATION.md` for the latest research state, evidence boundaries, and next actions.
3. Inspect `examples/stormglass_keepers/` for the current original example project: premise, architecture, scenes, exact storyboards, thumbnail concepts, and machine evaluation.
4. Run tests and the example evaluation before trusting local changes:

```bash
python -m pytest -q
python -m studio.cli evaluate-project \
  --premise examples/stormglass_keepers/premise.json \
  --architecture examples/stormglass_keepers/architecture.json \
  --scenes examples/stormglass_keepers/scenes \
  --output examples/stormglass_keepers/production_evaluation.json
```

## What the system contains

- `studio/`: reusable Python intelligence modules for comparative failure analysis, premise evaluation, format strategy, production economics, thumbnail concept generation, dialogue craft, meaning-carrier validation, relational-contract validation, and project gates.
- `knowledge/market/`: channel-specific and cross-channel market research. Start with `ironcrest-deep-dive.md`, `format-duration-performance.md`, `third-pass-breakout-media-deep-dive.md`, and `fourth-pass-breakout-media-deep-dive.md`.
- `knowledge/nov-drama/`: Nov Drama comparative findings and failure/hit analysis.
- `knowledge/craft/`: screenplay, direction, retention, sound, and scene-writing craft distilled from evidence.
- `knowledge/thumbnails/`: thumbnail taxonomy, comparative analysis, professional research synthesis, and design protocol.
- `knowledge/production/`: AI-provider inventory, generation economics, and production constraints.
- `evidence/research/`: persistent derived audiovisual evidence copied out of the analysis machine: contact sheets, timeline/second-resolution metrics, audio-analysis clips, and batch outputs. `evidence_manifest.json` records provenance and checksums.
- `data/raw/` and `data/processed/`: source metadata, subtitle files, archive tables, cohort comparisons, and machine-generated analysis outputs.
- `thumbnails/reference/`: persistent thumbnail reference archive organized for hit/middle/failure comparison.
- `examples/stormglass_keepers/`: original production example showing how research becomes a validated film package.

## Evidence policy

Public views are **not** proof of CTR or retention. Every serious claim must carry an evidence label and tier:

- Tier 0: public title/thumbnail/date/duration/views
- Tier 1: exact metadata/comments/likes
- Tier 2: timestamped subtitles aligned to video
- Tier 3: second-resolution visual/audio measurements
- Tier 4: agent-reviewed timestamped interpretation
- Tier 5: private CTR/retention/impressions/traffic data

Full copyrighted video files are not committed. The repository preserves derived evidence: subtitles, metadata, contact sheets, compressed timeline/second metrics, selected audio-analysis clips, and written timestamped interpretation. Contact-sheet interpretation is sampled full-runtime visual inspection, not a claim of continuous frame-by-frame human viewing.

## Core creative doctrine

The most portable audience engine found so far is:

> legible injustice or danger + a specific vulnerable child/creature/person + credible protection + early visual payoff + costly protagonist agency + belonging/personhood repair.

Usually insufficient alone: dragons, royalty, lore, scale, visual polish, army battles, revenge labels, franchise continuity, or “movie-like” packaging.

Strong films convert objects into meaning: an egg becomes a child/protector bond; tea becomes measurable competence; a train becomes autonomy; a ring becomes family memory and proof. The system therefore validates both a **meaning carrier** and a **relational contract** instead of judging a premise by genre ingredients.

## Current validated machine gates

The example evaluation currently checks, among other things:

- opening conversion and early promise payment
- title/packaging alignment
- retention architecture coverage
- exact storyboard continuity
- dialogue and agency craft
- shot-pipeline production economics
- sound-design intent
- meaning-carrier recurrence and transformation
- relational-contract timing, consent, personhood, and payoff

These are advisory studio gates, not oracle predictions. Read warnings and counterexamples rather than treating a score as a black box.

## Current research status

Implemented and evidenced:

- Nov Drama archive collection and hit/middle/failure cohort analysis
- Ironcrest complete four-video catalog deep dive
- Epic/FablePop/RIFTBORN/The Next Show/cross-channel hit-failure analysis
- Korean/breakout microdrama investigation
- first/second/third/fourth-pass recent breakout analysis
- duplicate-title forensic comparison using subtitle fingerprints and opening visuals
- thumbnail reference archive and taxonomy
- sound-design evidence for power shifts, care transitions, and negative space
- original Stormglass Keepers example package and machine evaluation

Still active research:

- deeper continuous visual review beyond sampled contact sheets
- more exact director-level storyboards
- additional weekly breakout discovery
- validated paid video-generation providers (no spending or license acceptance without explicit approval)

## Contribution / continuation rule

Do not strip evidence to make the repository look clean. If generated evidence is large, compress it, index it, and document provenance instead. Every new research pass should end by updating:

1. the relevant `knowledge/` file,
2. machine-readable contracts or evaluators when the lesson is repeatable,
3. `CONTINUATION.md`,
4. tests or example evaluation when logic changes.
