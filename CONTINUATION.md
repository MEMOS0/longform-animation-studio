# Continuation checkpoint — read first after context rollover

Updated: 2026-11-26 after breakout media deep-dive work. Latest pushed commit at last verified push was `6cd9ba3` (“Verify recent breakout channel histories”), and then `d1aad52` (“Add exploration and survival channel contracts”). PR: https://github.com/MEMOS0/longform-animation-studio/pull/1, branch `devin/1764170700-failure-intelligence-foundation`, local repo `C:/Users/Administrator/repos/longform-animation-studio`.

## Immutable user mandate

Build a reusable professional AI-assisted long-form animation studio system, not merely a Nov Drama report. Another AI agent must be able to use the repo to plan/write/direct/produce original high-quality long-form animated films. Analyze successful and failed videos genuinely audiovisually where possible; never pretend inaccessible videos were watched. Record timestamped/concrete evidence. Nov Drama is only the start. Deeply integrate screenplay, character psychology, dialogue, direction, sound, retention, thumbnail intelligence, market/format analysis, and failure intelligence. Keep working until the user says stop; use no subagents and do not treat subagent output as done. User wants direct Turkish “kanka” tone and no unnecessary questions.

## Current completed state

- Tests: **10 passed** locally after production economics/channel-contract/thumbnail tests.
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
- Machine-readable channel contracts added at `knowledge/market/channel_contracts.json` and wired through `studio/channel_contracts.py` into production evaluation; premise schema accepts `channel_contract`.

- Example end-to-end original project: `examples/stormglass_keepers/` has premise, architecture, scenes, thumbnail concepts, and production evaluation. Gates A/B/C pass; risk 0.356; no matched failure patterns; format/channel warnings clean.
- Machine-readable channel contracts exist and are wired into production evaluation. Production economics estimator exists and is integrated.
- External video-generation provider audit: `knowledge/production/video-generation-provider-audit.md`. Runway Dev aggregation, Google Gemini Omni, Luma Ray 3.2, Pika, Kling direct documented; Sora/Videos API and Gemini Veo 3.1 Preview are unavailable/shut down. No paid smoke tests.
- Advanced craft playbook: `knowledge/craft/advanced-screenplay-direction-retention.md` covers emotional machine, protagonist psychology, scene power transitions, dialogue/subtext, retention horizons, direction, sound, edit, endings.
- Recent breakout discovery: `tools/discover_recent_breakouts.py` found 35 last-14-day leads, 26 strong low/mid-subscriber leads. Report `knowledge/market/recent-breakout-candidates.md`; thumbnails downloaded under `thumbnails/reference/recent_breakouts/`; montage `thumbnails/recent_breakouts_top24_montage.jpg`; synthesis `knowledge/market/recent-breakout-synthesis.md`.
- Recent breakout channel-history verification: `knowledge/market/recent-breakout-channel-verification.md`. Veylorn compilation is repeat/franchise amplification, EchoDrama is the cleanest low-base melodrama breakout, Drakenhart/VNDL are high-priority tiny-channel creature-fantasy performers, Neural is not a low-subscriber breakout.
- `exploration_wonder_feature` and `hostile_survival_spectacle` channel contracts added to `knowledge/market/channel_contracts.json`; thumbnail concept generation now has `hidden_world_scale` and `ordinary_human_vs_impossible_threat` branches; tests still 10 passed.
- Recent breakout media deep dive: `knowledge/market/recent-breakout-media-deep-dive.md`. All five selected videos downloaded locally. Quick opening/ending sheets are in `C:/Users/Administrator/breakout_quick_sheets/`; Tiny Kingdom has completed machine analysis in `C:/Users/Administrator/breakout_analysis/1Nv2aGUgIG4/`; batch analysis for other videos may still be incomplete if the process was killed. Key lessons: creature stories split into protection/belonging vs hostile survival; exploration/wonder works when it becomes care/capture/social stakes early; Hidden Beauty validates coercive-protection/body-shame inversion; chosen-one myth should follow vulnerability/loss/protection.
- Crateh 14d endpoint appears to return the same rows as 7d; do not treat it as independent evidence.
- `.gitattributes` added marking `data/**`, `thumbnails/**`, `*.ttml`, and `*.casebook.json` as `linguist-generated` because Devin Review docs say these do not count toward review diff-size limits. This is the current CI/Review fix hypothesis.

## Important caveats

- Contact-sheet review is sampled full-runtime visual inspection, not continuous frame-by-frame human watching.
- Public views/day is not CTR or retention. Korean “rolling views” are not total 7-day increments.
- `Aa0l5km5Jl4` lacks English subtitles; visual-first. RIFTBORN comparison videos lack subtitles. Some Korean tracks are Korean-only.
- Earlier cross-channel interpretation may include subtitle contamination; do not treat old broad findings as final without rechecking.
- Devin Review repeatedly skipped/failed because PR diff was huge. `.gitattributes` fix changed status to `running` at least once, so the diff-size hypothesis is promising; wait for completion notifications rather than polling obsessively. Local tests pass.
- Downloaded full mp4/contact-sheet media are intentionally local only, not committed. Thumbnail reference images are committed because user explicitly requested persistent visual references; never copy them as production artwork.

## Immediate next steps, in order

1. If Devin Review still skips/fails after `.gitattributes`, inspect exact status once, then split generated evidence into separate branch/PR or further exclude generated artifacts. Do not bypass review settings.
2. `knowledge/market/cross-channel-audiovisual-findings.md` has been re-reviewed after subtitle correction and explicitly marked usable within evidence limits. Continue deeper rechecks only when a production decision depends on exact dialogue.
3. Finish full machine media-analysis casebooks for `6pbhGtHRTwA`, `icsZH4sDwTM`, `NHAHR3v9La8`, and `lBhjowuJURw` if needed; initial audiovisual deep dive already exists in `knowledge/market/recent-breakout-media-deep-dive.md`, and quick sheets/media are local. Use `python tools/batch_media_analysis.py --media-dir C:/Users/Administrator/breakout_media --raw-dir data/raw/piped_recent_breakout --out-root C:/Users/Administrator/breakout_analysis --workers 2` only if fuller timelines are worth the compute.
4. Duplicate `THE LOST KIND` issue resolved at metadata/subtitle-fingerprint level: Everflame appears to reuse the hit title for a different dragon-bond story, not the same film/reupload. Optional next refinement: compare visual assets if full Everflame media is later downloaded.
5. Within-channel thumbnail comparison completed at `knowledge/thumbnails/breakout-within-channel-thumbnail-comparison.md`; continue media comparison of recent breakouts: EchoDrama hit `lBhjowuJURw` vs lows `hchpYZaYFfU`/`SeQcIQBO7sQ`; Drakenhart hit `1Nv2aGUgIG4` vs lower `L5Xau3CAto0`/`hiyRGA1WbNs`. Within-channel media comparison completed in `knowledge/market/breakout-within-channel-media-comparison.md`. Key correction: low performers can have strong hooks; Hidden Beauty wins because minutes 1-5 convert wound into public humiliation + protective romance + payoff contract, while Mermaid becomes proof/administrative verification and My Name becomes cerebral contract negotiation. `opening_conversion_quality` machine check added to production evaluation; tests now 11 passed.
6. Analyze recent breakout thumbnails in detail from `thumbnails/recent_breakouts_top24_montage.jpg` and per-image files. Initial synthesis is in `knowledge/market/recent-breakout-synthesis.md`.
7. Format-duration quantitative segmentation completed in `knowledge/market/format-duration-performance.md`; use it to refine future target-duration defaults.
8. Validate production economics and provider docs before any paid generation; never spend without explicit approval.
9. Continue integrating research into production decision-making, not just reports.

## Key creative synthesis to preserve

Most portable mechanism: legible injustice/danger + specific vulnerable child/creature/person + credible protection + early visual payoff. Strong but channel-fit dependent: hidden royal identity, transformation/rebirth, familiar mythic adventure, revenge/reversal, creature spectacle, regression romance, BL intimacy/power, disaster survival, sci-fi mystery. Usually insufficient alone: scale, lore, armies, crowns, visual polish, franchise continuity, attractive actors, continuation hooks.
