# Agent handoff: how to use this repository as a production skill

Read this file first if you are an AI agent asked to plan, write, direct, or produce an original long-form animated film. Your job is not to imitate surface tropes. Your job is to operate the studio system honestly and make evidence-informed creative decisions.

## Required startup sequence

1. Read `README.md` for repository structure and evidence tiers.
2. Read `.devin/skills/longform-animation-studio/SKILL.md` and follow it as operating discipline.
3. Read `knowledge/nov-drama/comparative-findings.md` before using Nov-Drama-derived rules.
4. Read `knowledge/craft/story-retention-direction-sound.md` before screenplay/directing work.
5. Read `knowledge/production/ai-provider-inventory.md` before assuming any generation API works.
6. Inspect `data/processed/casebook_cohort_comparison.md` and `data/processed/dialogue_cohort_comparison.md` for measured archive-wide patterns.
7. Treat generated per-video casebooks as reproducible artifacts. Only representative samples are committed to keep reviews readable.

## Non-negotiables

- Do not claim that a video was watched end-to-end unless you actually inspected the audiovisual evidence.
- Do not infer CTR or retention from public views. Label evidence tiers.
- Do not copy plots, character combinations, dialogue, or exact expressive content from reference videos.
- Do not greenlight a story only because it contains dragons, royalty, revenge, a child, or a hidden identity.
- Do not accept provider license terms or spend money without explicit user approval.
- Do not trust generated output merely because a provider returned a file. Validate narrative, visual, audio, and editorial usability.

## Production workflow

### 1. Research and market fit

- Build or refresh the relevant channel/market archive.
- Compare inside-channel cohorts before cross-channel conclusions.
- Write hypotheses with evidence tier, support, counterexamples, and decision implications.
- Use cross-channel evidence to broaden the search, not to replace full-video analysis.

### 2. Premise design

Create a machine-readable premise in `schemas/premise.schema.json` format. A viable premise must define the wound, want, need, secret/power asymmetry, protective counterforce, cost, status reversal, and belonging payoff. If those cannot be stated clearly, the premise is not ready.

### 3. Failure intelligence

Run:

```bash
python -m studio.cli evaluate-idea --candidate "your premise" --script-file your_notes.md
```

Read every triggered pattern. Do not optimize the score; resolve the underlying dramatic risk or document why the resemblance is superficial.

### 4. Architecture and scene design

Create architecture and scene artifacts under `schemas/`. Every scene needs change, dramatic question, power shift, protagonist choice or failure to choose, intended entry/exit emotion, and visual necessity. Long runtime is not stuffing; each scene must earn attention.

### 5. Pre-greenlight validation

Run:

```bash
python -m studio.cli evaluate-project \
  --premise path/to/premise.json \
  --architecture path/to/architecture.json \
  --scenes path/to/scenes \
  --output path/to/evaluation.json
```

Interpret the result as a gate report, not a creative oracle. Schema errors must be fixed. Failure-pattern warnings need explicit revision or rationale.

### 6. Production-provider validation

Before committing to image/voice/video generation:

- inventory exact providers and model names;
- smoke-test the smallest safe artifact;
- save evidence and failure modes;
- never assume one modality implies another modality works;
- evaluate vertical/mobile emotional readability, continuity, face integrity, voice fit, and editability.

Cloudflare Workers AI is currently a validated candidate for text/image/TTS experimentation in this repository, not a validated video pipeline.

### 7. Direction, sound, and edit

Use `knowledge/craft/story-retention-direction-sound.md` as the craft baseline. The mobile viewer must understand faces, emotional pressure, protection, danger, and reversal without needing dense exposition. Sound must shape transitions and emotional contrast; it is not wallpaper.

### 8. Post-release learning

If the film is released, collect performance evidence honestly. Private CTR, retention, traffic sources, comments, and audience segmentation outrank public-view speculation. Feed results back into `knowledge/` and revise the failure-intelligence rules.

## Current honest limitations

- The Nov Drama archive is deeply instrumented, but direct interpretive visual audits are still representative rather than exhaustive for every video.
- Cross-channel expansion has begun at market/title level; it must not be treated as audiovisually validated until the downloaded comparison videos are analyzed.
- No end-to-end video-generation provider has been validated yet.
- The system is a decision-support studio, not an automatic hit predictor.
