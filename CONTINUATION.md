# Continuation checkpoint — read first after context rollover

Updated: 2026-11-26 after commit `3c2c6b1` plus pending Epic evidence commit (“Compare Epic hit and failure thumbnails”). PR: https://github.com/MEMOS0/longform-animation-studio/pull/1, branch `devin/1764170700-failure-intelligence-foundation`, local repo `C:/Users/Administrator/repos/longform-animation-studio`.

## Immutable user mandate

Build a reusable professional AI-assisted long-form animation studio system, not merely a Nov Drama report. Another AI agent must be able to use the repo to plan/write/direct/produce original high-quality long-form animated films. Analyze successful and failed videos genuinely audiovisually where possible; never pretend inaccessible videos were watched. Record evidence with timestamps. Nov Drama is only the start. Deeply integrate screenplay, character psychology, dialogue, direction, sound, retention, thumbnail intelligence, market/format analysis, and failure intelligence. Keep working until the user says stop; use no subagents and do not treat subagent output as done.

## Current completed state

- Nov archive: 48 videos metadata; 47 mp4s analyzed with second-resolution timelines; casebooks/dialogue cohort analysis in repo.
- AI provider inventory: Cloudflare Workers AI smoke-tested for text/image/TTS; no video model found.
- Thumbnail Intelligence foundation exists: persistent reference archive, montages, metrics, concepts/critique module.
- Priority channel archives committed: Epic 81, FablePop 9, Ironcrest 4, RIFTBORN 11, The Next Show 56.
- Ironcrest complete 4-video deep dive committed at `knowledge/market/ironcrest-deep-dive.md`. Key finding: child/creature protection beats adult crown/competence spectacle; all videos ~27–32m so runtime is controlled.
- `tools/download_piped_archive.py` subtitle-selection bug fixed and committed; English is now preferred rather than blindly taking first subtitle. Corrected Ironcrest English subtitles exist locally/repo for relevant IDs.
- Genre classification improved with `mythic_adventure` and `transformation_melodrama`; channel comparisons regenerated.
- Future Frame: original YouTube account is terminated. Direct yt-dlp says unavailable because account terminated; Piped endpoints fail. A 13-title partial catalog preserved from Hollywood.ai in `knowledge/market/future-frame-catalog.md` + `data/raw/future_frame_hollywood_catalog.json`. Most thumbnails are gone upstream; only one low-res thumbnail downloaded. Do not claim media analysis.
- Epic official site analyzed in `knowledge/market/epic-ai-films-site-analysis.md`. Key evidence: recent “Five Baby Dragons” (~149k/day) and “Mother of Dragons” (~90k/day) strongly cross-validate vulnerable creature/child protection; disaster one-offs underperform inside the channel; site confirms one-filmmaker studio/world-franchise strategy.
- External sources audited in `knowledge/market/data-source-and-format-audit.md`. Crateh exposes a very different Korean serial ecosystem: 1,052 works; 814 series vs only 6 feature films; genres dominated by drama/romance/fantasy/action/historical. Do not compare microdrama episodes directly with 60–120m films. MetaMovies blocked by verification interstitial.
- Tests currently pass: 5 passed.

## Important caveats

- Contact-sheet review is sampled full-runtime visual inspection, not continuous frame-by-frame human watching.
- `Aa0l5km5Jl4` (Ironcrest Son of Wolves) has no English subtitle track; analysis is visual-first and lower confidence.
- Public views/day is not CTR or retention.
- Montage generator may duplicate rows for small archives; fix pending. Epic thumbnail comparison committed at `knowledge/thumbnails/epic-thumbnail-comparison.md`: relational creature scale contrast and face emotion beat trailers/AI-meta/off-format imagery; lows are often different product types.
- Some earlier cross-channel interpretation may have been affected by Arabic subtitle contamination; revisit before treating as final.
- Devin Review CI oscillates pending/failed. No actionable new review findings are visible in PR comments as of checkpoint; inspect review UI/comments if notification arrives.

## Immediate next steps, in order

1. Fix montage overlap for small archives and regenerate montages if cheap.
2. Epic deep-dive media job is running in background shell `epicdeep2`: downloading `_VqQezjbLes` Five Baby Dragons, `46mo0VFuYoM` Mother of Dragons, `gc6nfjiklRQ` Earthquake, `6-w0gu5NR_A` One Last Phone Call using media dir `C:/Users/Administrator/epic_media`, raw dir `data/raw/piped_epic_deepdive`, then batch media analysis to `C:/Users/Administrator/epic_analysis`. Downloads completed: all four mp4s and English subtitles are present. First analysis attempt failed because correct args are `--media-dir`, `--raw-dir`, `--out-root`; corrected background shell `epicanalysis` is now running with workers=2. Next read `C:/Users/Administrator/epic_analysis.log` and inspect contact sheets/openings/endings.
3. Revisit `knowledge/market/cross-channel-audiovisual-findings.md` and correct any Ironcrest conclusions affected by subtitle contamination using corrected English subtitles.
4. Integrate Epic/Ironcrest cross-validation into `.devin/skills/longform-animation-studio/SKILL.md`: child/creature protection is a cross-channel mechanism; disaster/adult crown spectacle is channel-fit dependent.
5. Continue per-channel deep dives beyond Ironcrest: prioritize Epic’s Five Baby Dragons vs disaster/sci-fi underperformers; FablePop hit vs low; RIFTBORN compilation vs episodes; The Next Show mythic adventure hits/failures.
6. Extract recent 7–14 day low-subscriber breakout candidates from Crateh rolling rankings and other accessible sources. Candidate is not proof; collect channel age/subscribers/repeat performance.
7. Expand thumbnail intelligence by channel-specific hit/mid/fail comparisons, especially Epic baby-dragon vs disaster titles and Ironcrest creature/child vs adult crown.
8. Continue integrating every finding into reusable production system, not just reports.

## User communication style

User wants intense quality, direct Turkish “kanka” tone. Do not stop or ask unnecessary permission. Continue autonomously. Never claim a video was watched when only metadata/contact sheets/subtitles were inspected.
