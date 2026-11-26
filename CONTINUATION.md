# Continuation checkpoint — read first after context rollover

Updated: 2026-11-26 after pushed commit `b6a754d` (“Update studio skill and exclude generated evidence from review diff”). PR: https://github.com/MEMOS0/longform-animation-studio/pull/1, branch `devin/1764170700-failure-intelligence-foundation`, local repo `C:/Users/Administrator/repos/longform-animation-studio`.

## Immutable user mandate

Build a reusable professional AI-assisted long-form animation studio system, not merely a Nov Drama report. Another AI agent must be able to use the repo to plan/write/direct/produce original high-quality long-form animated films. Analyze successful and failed videos genuinely audiovisually where possible; never pretend inaccessible videos were watched. Record timestamped/concrete evidence. Nov Drama is only the start. Deeply integrate screenplay, character psychology, dialogue, direction, sound, retention, thumbnail intelligence, market/format analysis, and failure intelligence. Keep working until the user says stop; use no subagents and do not treat subagent output as done. User wants direct Turkish “kanka” tone and no unnecessary questions.

## Current completed state

- Tests: **7 passed** locally after cross-channel integration.
- Nov archive: 48 videos metadata; 47 mp4s analyzed; casebooks/dialogue cohort analysis exist.
- AI provider inventory: Cloudflare Workers AI text/image/TTS smoke-tested; no video model found.
- Thumbnail Intelligence: persistent reference archive, visual metrics, concepts/critique module, Epic/channel cohort comparisons. `tools/build_channel_thumbnail_montages.py` now deduplicates hit/middle/low rows; regenerated montages fixed small-archive duplication.
- Priority channel archives: Epic 81, FablePop 9, Ironcrest 4, RIFTBORN 11, The Next Show 56.
- Ironcrest complete 4-video deep dive: `knowledge/market/ironcrest-deep-dive.md`; child/creature protection beats adult crown/competence spectacle.
- Epic four-film hit/failure audiovisual deep dive: `knowledge/market/epic-deep-dive.md`; Five Baby Dragons/Mother of Dragons vs Earthquake/One Last Phone Call. Important falsification: Phone Call has a strong rescue opening yet underperforms, supporting channel-contract mismatch rather than “failure = weak opening.”
- Cross-channel hit/failure deep dives: `knowledge/market/cross-channel-hit-failure-deep-dives.md` covers FablePop, The Next Show, RIFTBORN using downloaded media/contact sheets. Key lessons: FablePop needs wound/secret/social reversal; Next Show needs physical mythic survival before lore; RIFTBORN compilation/completeness can dominate fragmented episode craft.
- Korean recent breakout deep dive: `knowledge/market/korean-breakout-deep-dive.md`; six downloaded/analyzed candidates from Crateh. Key lessons: niche precision differs radically; BL intimacy/power/secrecy and regression/court tropes should not be pooled with broad creature fantasy.
- Future Frame YouTube account terminated; partial 13-title catalog preserved from Hollywood.ai, no media-analysis claims.
- External source/format audit exists. Do not compare microdrama episodes directly with 60–120m films.
- Cross-channel patterns integrated into code: `studio/failure_intelligence.py` now includes spectacle-without-relational-anchor, abstract quest lore, fragmented episode, delayed payoff. `studio/format_strategy.py` added and integrated into `studio/production.py`; premise schema now accepts optional `target_minutes`/`release_format`.
- Skill updated with cross-channel/format decision protocol in `.devin/skills/longform-animation-studio/SKILL.md`.
- `.gitattributes` added marking `data/**`, `thumbnails/**`, `*.ttml`, and `*.casebook.json` as `linguist-generated` because Devin Review docs say these do not count toward review diff-size limits. This is the current CI/Review fix hypothesis.

## Important caveats

- Contact-sheet review is sampled full-runtime visual inspection, not continuous frame-by-frame human watching.
- Public views/day is not CTR or retention. Korean “rolling views” are not total 7-day increments.
- `Aa0l5km5Jl4` lacks English subtitles; visual-first. RIFTBORN comparison videos lack subtitles. Some Korean tracks are Korean-only.
- Earlier cross-channel interpretation may include subtitle contamination; do not treat old broad findings as final without rechecking.
- Devin Review repeatedly skipped/failed because PR diff was huge. `.gitattributes` fix is pushed but not yet proven; wait for automatic notification/status rather than polling obsessively. Local tests pass.
- Downloaded full mp4/contact-sheet media are intentionally local only, not committed. Thumbnail reference images are committed because user explicitly requested persistent visual references; never copy them as production artwork.

## Immediate next steps, in order

1. If Devin Review still skips/fails after `.gitattributes`, inspect exact status once, then split generated evidence into separate branch/PR or further exclude generated artifacts. Do not bypass review settings.
2. Revisit `knowledge/market/cross-channel-audiovisual-findings.md` and correct subtitle-contaminated conclusions using corrected English subtitles.
3. Add a machine-readable channel-contract knowledge file (JSON/YAML) mapping Epic/Ironcrest/FablePop/Next/RIFT/Korean microdrama contracts and wire it into premise evaluation.
4. Create at least one original example premise packet + architecture + scenes that uses the full system end-to-end, then run production gates on it.
5. Expand thumbnail intelligence: compare Epic/Ironcrest/Fable/Next/RIFT hit-middle-low thumbnails visually in more detail; update thumbnail concept generator with channel-contract-aware reference classes.
6. Continue weekly/recent breakout discovery beyond Crateh top 10; collect channel age, repeat performance, format, language/market, and evidence quality.
7. Investigate accessible video-generation providers/APIs beyond Cloudflare; inventory exact model/modality/pricing/license constraints without accepting terms or spending money.
8. Continue integrating research into production decision-making, not just reports.

## Key creative synthesis to preserve

Most portable mechanism: legible injustice/danger + specific vulnerable child/creature/person + credible protection + early visual payoff. Strong but channel-fit dependent: hidden royal identity, transformation/rebirth, familiar mythic adventure, revenge/reversal, creature spectacle, regression romance, BL intimacy/power, disaster survival, sci-fi mystery. Usually insufficient alone: scale, lore, armies, crowns, visual polish, franchise continuity, attractive actors, continuation hooks.
