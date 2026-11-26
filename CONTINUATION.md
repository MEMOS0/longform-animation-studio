# Continuation checkpoint — Nov Drama / longform-animation-studio

Updated: 2026-11-26 session `9b820e85797b4edfba99232f657790bb`

## User intent (do not lose)

- Build `MEMOS0/longform-animation-studio` into a reusable professional long-form animation production system, not just a Nov Drama report.
- Analyze as much of the Nov Drama archive as possible, comparing successful, average, and failed videos inside the same channel.
- Do not rely only on titles/transcripts/screenshots: use real audiovisual evidence end-to-end where possible.
- Record timestamped concrete evidence in the repository so conclusions can be audited.
- Deepen especially in scenario writing, character psychology, story development, dialogue, directing, sound design, and retention.
- Learn what not to repeat from failures as much as what to imitate from successes.
- Keep working continuously until the user explicitly says stop; quality over speed; do not stop merely because context is full.

## Current repo/PR

- Repo: https://github.com/MEMOS0/longform-animation-studio
- Branch: `devin/1764170700-failure-intelligence-foundation`
- PR: https://github.com/MEMOS0/longform-animation-studio/pull/1
- Initial commit: `fd1e5e7` — comparative failure intelligence foundation.

## Working system already built

- `studio/youtube_archive.py`: full channel archive metadata extraction from flat yt-dlp channel JSON + YouTube watch pages + thumbnails.
- `studio/features.py`: auditable title/theme/thumbnail feature extraction.
- `studio/comparative.py`: age-adjusted views/day cohort comparison, permutation tests, thumbnail montage.
- `studio/media_analysis.py`: downloads/uses real media to extract second-resolution visual features, shot boundaries, contact sheets, audio features, subtitle alignment, narrative markers.
- `studio/failure_intelligence.py`: transparent failure-pattern matching for future ideas/scripts.
- `tools/download_piped_archive.py`: uses public Piped API `https://maxtube-api.lawrie.co.nz/streams/<video_id>` and parallel Range downloads; this works even though direct YouTube/yt-dlp is bot-blocked on the VM.
- `tools/fetch_comments.py`: first-page public comments via `https://maxtube-api.lawrie.co.nz/comments/<video_id>`.
- `.devin/skills/longform-animation-studio/SKILL.md`: extensive studio operating discipline.
- `knowledge/craft/story-retention-direction-sound.md`: external craft/research synthesis.
- Tests passed before the batch script bug: `3 passed`.

## Data state on this VM

- Channel archive JSON: `C:/Users/Administrator/novdrama_channel.json` (48 videos).
- Archive table committed: `data/raw/novdrama_archive.jsonl`.
- Comparative outputs committed: `data/processed/novdrama_analysis_rows.json`, `novdrama_comparative_results.json`, `novdrama_comparative_report.md`.
- Thumbnail montage local: `data/processed/novdrama_thumbnail_montage.jpg` (not committed due copyright).
- Local media directory: `C:/Users/Administrator/novdrama_media`.
- At last check 18/48 mp4s downloaded, including:
  `0ofXaXWcfi0, 1OXQh5I8m6Y, 3C4Chi9g1d8, KsxgWoFS50I, LEc_nNFoi-g, NnPZaWSGYuc, ULJ7-z1zm6M, _I5I1l7DP3E, ajI2gST2O5I, bI0uHNOVewI, egF-DbUQp2k, j3U5JsLvbLg, jW-gZtvP9Oo, rtTbEcFdnZQ, sepLtaMfPcA, u9acebqxR-8, v03oauoFveU, vYNuKn6GiaE`.
- Background download shell was `e86429` (`data/raw/download_all.log`).
- Priority download shell was `a1ca67` (`data/raw/download_priority.log`).
- Comments fetched into local ignored raw dir; aggregate committed candidate: `data/processed/novdrama_comment_signals.json`.

## Important command issue discovered

`python tools/batch_media_analysis.py` failed with `ModuleNotFoundError: No module named 'studio'` because running a script by path puts `tools/` on `sys.path`, not repo root. Fix by inserting repo root into `sys.path` in that script or run with `PYTHONPATH=.`. Then run batch analysis.

## Key empirical findings so far (preliminary, not causal)

1. Archive metadata:
   - 48 videos, mostly ~48–122 minutes.
   - Views/day leaderboard: `v03oauoFveU` ~115k/day, `vYNuKn6GiaE` ~112k/day, `ULJ7-z1zm6M` ~102k/day.
   - Strongest preliminary binary signal: `family_child` +1.50 mean log views/day, exploratory permutation p≈0.013.
   - `hidden_identity_or_secret` positive (+1.01), `dragon` positive (+1.08), `setup_then_reversal` positive (+0.84), but not statistically reliable.
   - `revenge_retribution` negative (-0.95), `modern_wealth_power` negative (-0.51), `wolf_werewolf` negative (-0.53), but confounded/small sample.
   - Thumbnail brightness rank-correlates positively with outcome (~0.40); saturation slightly negative.
2. Thumbnail montage visual read:
   - Top cohort skews luminous gold/blue fantasy, family/children/creature/protector, clear transformation/belonging promise.
   - Bottom cohort skews dark/red seduction/violence, generic couple intimacy, sports/racing, or visually confusing/generic promises.
3. Format discovery:
   - Nov Drama videos are vertical/mobile-native (ULJ stream 202x360), not widescreen films. The first contact-sheet implementation accidentally stretched them; fixed in `media_analysis.py`.
4. ULJ hit opening evidence:
   - 0:00 crying orphan clutching bunny; emotional wound visible immediately.
   - 1:20 extreme close-up of dragon eye: fantasy promise appears very early.
   - 1:40–2:20 public humiliation/rejection (“Who would want you?” mechanism).
   - 2:40–3:00 boy kindness and adoption/belonging choice.
   - 3:20 castle/world transition.
   - 4:40 warm welcome/family.
   - 6:20 noble/dragon family member introduces new social tension.
   - Interpretation: rapid alternation of wound → kindness → spectacle → belonging → new tension; faces dominate vertical framing.
5. NnPZ failure opening evidence:
   - 0:00–2:00 starts with mother’s bones dug from corpse pit, coercion into slavery, clan genocide, mask threat.
   - 2:00–4:00 protagonist kills escort, sexual/violent bond/soul-mark material, complex mythology.
   - 4:00–8:00 repeated humiliation, trial, execution threats, Elder Council, pureblood politics.
   - 8:00–10:00 War King protects her but through violent spectacle/scale tearing.
   - Interpretation: not “badly produced”; visually rich and fast, but cognitively dense, dark, sexually coercive, proper-noun heavy, and emotionally unrelenting. Less universal/protective warmth than hit opening.
6. Comments:
   - ULJ top comments praise good/non-evil stepsister and lack of unnecessary sister drama; differentiation from trope fatigue matters.
   - vYNu top comments praise revenge being dealt with within 10 minutes, not delayed to the end. Important counter-hypothesis: revenge can work when it is satisfying early and then story escalates; failure is not revenge itself but cold/repetitive/unsatisfying revenge.
   - rtTb has a complaint about censorship/clouds/pixels over cleavage breaking immersion.
   - Ksxg comments show viewers like kitty/wolf/dragon and brother betrayals, yet performance is weak: surface topic demand is insufficient.

## Dynamic workflow / subagent state

- Tried workflow `novdrama-comparative-video-analysis`.
- First failed from script bug; fixed.
- Second failed because org session creation returned `out_of_quota`; no agents consumed ACU.
- Do not keep retrying child sessions unless quota returns. Per user memory, compensate with rigorous multi-pass self-audit and local computational analysis.
- Workflow file remains `workflows/novdrama_video_analysis.py` for future use.

## 2026-11-26 late-session state update

- PR branch is pushed through `bb2a2cb` (“Deepen hit and failure case evidence”). Earlier commit `926b2aa` added the timestamped casebook intelligence system.
- Devin Review findings through commit `fde6bd6` were triaged/resolved; new pushes may trigger new review rounds.
- Initial batch media analysis completed for 24 videos. 47/48 mp4s were downloaded at last check; only `jRa3_WZYDdY` remained missing because the Piped stream endpoint errored. A second batch (`media_batch2`) is analyzing the newly downloaded videos and skips existing summaries.
- `vYNuKn6GiaE` is the crucial revenge counterexample: visual contact-sheet evidence shows dragon hatching/power awakening in the first minutes, dragon-baby/child promise visibly paid by roughly 11:20, and public enemy consequences by roughly 11:40–13:00. Therefore failure is not “revenge” itself but delayed/cold/unembodied revenge.
- `v03oauoFveU` opening interleaves dragon royalty/egg mystery, child vulnerability, mother reassurance, creature care, and bruised-child stakes within the first 6 minutes.
- `rtTbEcFdnZQ` failure shows polished court spectacle but adult sexualized ceremony/politics plus repeated censorship artifacts; ending warmth exists but is insufficient.
- `BeX5LHLqOEI` and `KsxgWoFS50I` both have warm payoff imagery yet underperform: payoff is necessary but not sufficient. Opening clarity and middle momentum matter.
- Key refined rule: lore is dangerous when abstract/procedural, but not when embodied in creatures, children, objects, visible costs, and action.
- `studio/media_analysis.py` was fixed after initial outputs: shot-id assignment is now linear and silence_ratio uses a file-level reference floor rather than a per-window self-percentile. Existing early outputs may still contain the old nearly constant silence artifact; repair/recompute before relying on silence ratios.
- `knowledge/nov-drama/comparative-findings.md` contains the current interpretive hypothesis ledger and timestamped evidence.
- Child workflow sessions remain blocked by organization `out_of_quota`; continue locally/self-audited unless quota returns.

## 2026-11-26 pre-context-rotation checkpoint

- All 47 downloadable Nov Drama mp4s now have media-analysis timelines in `data/processed/media_batch`; only `jRa3_WZYDdY` remains unavailable because the Piped stream endpoint repeatedly failed.
- Audio metrics are being repaired with `tools/repair_audio_metrics.py`; after it finishes, rerun `python tools/build_casebooks.py` and `python tools/compare_casebooks.py` and commit the refreshed casebooks/comparison.
- `studio/production.py` and `python -m studio.cli evaluate-project` now validate premise/architecture/scene JSON artifacts against schemas, run failure intelligence, check scene coverage, and report gates A–F.
- `examples/stormglass_project/` contains the first machine-readable original-project self-test; current evaluation has schema errors empty, gates A–C pass, risk 0.218, no architecture warnings, and no scene-quality missing fields. Gates D–F correctly remain unknown until boards/media/release exist.
- Devin Review findings at commit `aacfead` were fixed in `0f7b3ca`, `a8060de`, and `23d881f`; triage ended and a newer review is running.
- Next high-value work: commit/push production evaluator + example + all refreshed casebooks; update README; inspect the full 47-video comparison for counterexamples; deepen scene psychology/dialogue/directing/sound annotations beyond lexical proxies; expand to at least one comparison channel.

## Immediate next steps

1. Fix `tools/batch_media_analysis.py` import bug and run batch analysis for all downloaded mp4s.
2. Continue monitoring/finishing all 48 downloads with `tools/download_piped_archive.py`; do not overload Piped server.
3. Analyze key hits/failures locally from contact sheets + aligned transcript + quantitative media summaries:
   - Hits: `vYNuKn6GiaE`, `v03oauoFveU`, `jRa3_WZYDdY`, `0ofXaXWcfi0`, `gkRXl9lDReY`, `u1RoW_083xM`.
   - Failures: `NnPZaWSGYuc`, `KsxgWoFS50I`, `rtTbEcFdnZQ`, `_I5I1l7DP3E`, `ZhAYjMLvlqc`, `xJUN_KOCnME`, `Prsthri0ktA`.
4. Write `knowledge/nov-drama/comparative-findings.md` with timestamped evidence, counterexamples, hypothesis status, and causal boundaries.
5. Extend Failure Intelligence patterns using validated findings, especially:
   - immediate satisfying justice vs delayed misery,
   - warmth/belonging contrast vs unrelenting darkness,
   - mythology/proper-noun overload,
   - adult sexualized coercion narrowing audience,
   - trope fatigue vs differentiated good characters,
   - spectacle without emotional causality,
   - packaging/content mismatch.
6. Build schemas/templates for premise, story architecture, screenplay, scene, direction, sound, edit, QA, postmortem.
7. Implement candidate comparison CLI and test it on one original premise.
8. Commit and push updates to PR #1.
9. Update environment blueprint with verified setup commands at the end.
10. If context nears limit again, reread this file first and continue without stopping.

## 2026-11-26 late continuation — expanded cross-channel + thumbnail mandate

The user explicitly added a new long-running requirement after the first cross-channel sample:

- Focus especially on Ironcrest Pictures, FablePop, RIFTBORN CINEMA, Future Frame Movies, Epic AI Films, and add “The Next Show | Stories That Feel Like Movies”.
- Inspect Epic AI Films’ site: https://epicaifilms.com/
- Use data sources: https://openmicrodrama.com/ai-dramas, https://crateh.com/, https://metamovies.ai/ai-movies/
- Do not lump all channels together: separately analyze fantasy cinema, romantic drama, animation, science fiction, emotional stories, and series formats.
- Compare hit/middle/failure videos inside each channel before cross-channel generalization.
- Distinguish 15–30 minute films from 60–120 minute films, and standalone films from episode/series formats.
- Keep looking for recently breakout small-subscriber channels in the last 7–14 days.
- Integrate all findings into the repository skill and production decision system.

The user also explicitly requires a separate Thumbnail Intelligence specialty:

- Download highest-available-resolution thumbnails for hit/middle/failure videos across all researched channels.
- Store persistent visual references in the repository and link each image to title/date/views/duration/subscriber count/performance snapshot.
- Actually visually inspect thumbnails: palette, contrast, composition, character positions, expressions/emotions, lighting, background, hierarchy, mobile readability, curiosity gap.
- Compare hit vs failure thumbnails within the same channel and decode title-thumbnail relationships.
- Build a categorized reference library, comparative analysis, failure archive, and future system that can generate/critique original thumbnail concepts without copying references.
- Research professional YouTube thumbnail design, visual perception, attention psychology, click behavior, and A/B testing sources and integrate them into the main skill.
- Do not present guesses as proven CTR effects without real CTR data.

Current cross-channel evidence state before continuation rollover:

- OpenMicroDrama top-20 structured items committed at `data/processed/openmicrodrama_top50_items.json` (despite filename, currently 20 schema items).
- Cross-channel market baseline committed at `knowledge/market/cross-channel-ai-drama.md`.
- First audiovisual mechanism findings committed at `knowledge/market/cross-channel-audiovisual-findings.md`.
- Downloaded and fully media-analyzed locally: `PyZn_Y62Cw4`, `bHCI5XUSppM`, `2YkJl0KV3gs`, `Nglk1Ji_SNI`, `LU74Q4y3-Jk`.
- `rIyeW1cJGSs` mp4/subtitles downloaded; batch media analysis was still in progress when the second batch began.
- `q_CnGWFO788` and `2Sbr4jpoiaQ` failed through the current Piped endpoint with HTTP 500; retry with alternate endpoints or later.
- Do not trust any subagent output as completed; user explicitly rejected subagent fan-out.

## 2026-11-26 thumbnail/cross-channel implementation checkpoint

Committed through `16c5b48` (“Expand priority channel archives and thumbnail references”).

Implemented and committed:

- `studio/thumbnail_intelligence.py` — thumbnail image metrics: dimensions, brightness, contrast, saturation, colorfulness, edge density, center salience proxy, mobile-size proxies, dominant palettes. Haar face detection exists but fails on stylized art and must not be treated as evidence yet.
- `studio/thumbnail_concepts.py` — reference classification plus original concept generation/critique. It explicitly warns that critiques are not CTR predictions.
- `tools/download_thumbnails.py` — downloads maxres/sd/hq thumbnails and writes metadata-linked indexes.
- `tools/collect_piped_channel.py` — paginated Piped channel archive collector.
- `tools/compare_channel_archives.py` — per-channel age-adjusted hit/middle/failure tables plus coarse format/genre/duration classification.
- `knowledge/thumbnails/thumbnail-intelligence.md` — first professional thumbnail knowledge base, measured Nov Drama cohort metrics, direct visual comparison, cross-channel taxonomy, protocol, falsification tasks.
- `.devin/skills/longform-animation-studio/SKILL.md` — now includes Thumbnail Intelligence protocol.
- Persistent archive under `thumbnails/reference/` now includes 48 Nov Drama + 20 OpenMicroDrama top sample + 161 priority-channel videos. Total thumbnails directory ~55MB. This was explicitly requested by the user despite normal caution around copyrighted references; use internally for mechanism learning, never copy production thumbnails.
- `thumbnails/novdrama_top_bottom_montage.jpg`, `thumbnails/openmicrodrama_top20_montage.jpg`, and `thumbnails/channel_cohort_montages/*.jpg` are committed visual comparison artifacts.
- Channel archives collected and committed under `data/raw/channels/`: Ironcrest 4, FablePop 9, RIFTBORN 11, Epic AI Films 81, The Next Show 56. Per-channel comparison tables committed under `data/processed/channel_comparisons/`; aggregate in `data/processed/channel_format_genre_summary.json`.

Important discovered channel IDs/subscriber counts at collection:

- Ironcrest Pictures `UCLryKn_vFx5lm3bFpPRhgRg`, 42.3k subscribers, 4 videos.
- FablePop `UCbw9c3sH6tWOGYu_suuhmjQ`, 163k, 9 videos.
- RIFTBORN CINEMA `UCIYFNbsI6MBolwhXV7OL7AA`, 31k, 11 videos.
- Epic AI Films `UC5FCyk1QkTBLgWm-w866PGg`, 276k, 81 collected videos.
- The Next Show | Stories That Feel Like Movies `UCEbhMBucfh4N48Av0NJp2WQ`, 259k, 56 collected videos.
- Correct Future Frame Movies channel appears to be `UC9I0vMcmoJBWqFYg6O7PujA`, but maxtube `/channel/` currently returns HTTP 500 for it. Web evidence: https://www.youtube.com/channel/UC9I0vMcmoJBWqFYg6O7PujA and glu.tv/hollywood.ai listings. Retry through alternate Piped instances or YouTube page extraction.

Key early within-channel findings:

- Ironcrest: baby dragon rescue 10M / ~461k views/day, she-wolf adopted baby 4.6M / ~145k/day, Ghost Wing sci-fi 613k / ~42k/day, Son of Wolves crown sequel 878k / ~28k/day. Strong vulnerability/protection pattern, but only 4 videos.
- FablePop: transformation/rebirth/secret-family hits ~109k–227k/day; older romance betrayal middles ~27k–32k/day; short/odd animal-prince or maid president videos far lower. Transformation/agency packaging is bright, clean, before/after oriented.
- RIFTBORN: BEASTBOUND Season 1 compilation 5.4M / ~170k/day and 137 minutes; individual episodes are far lower. Compilation/complete-story availability itself is a major format effect; thumbnails are visually consistent, so packaging alone cannot explain the difference.
- Epic AI Films: AGE OF KINGDOMS/DRAGONS long standalone films dominate; 60–120 minute films median much higher than under-15 minute videos. Low performers include trailers, AI-meta/behind-the-scenes/tool demos, and generic sci-fi experiments — channel-contract mismatch, not necessarily bad thumbnails.
- The Next Show: mythic adventure IP-like stories (Sinbad, Aladdin, Jason/Odyssey/dragons) dominate; documentaries/dinosaur/off-brand shorts are low. 30–120 minute films far outperform under-15 minute pieces. Series compilations can outperform individual parts.
- Cross-duration evidence is promising but confounded by age, series compilation, genre, and channel identity. Do not make universal duration claims.

Important thumbnail visual insights:

- Nov Drama top thumbnails are typically luminous vulnerability/protection/belonging images; low thumbnails more often skew dark/red revenge, coercion, crowded triangles, or arena spectacle. Brightness cohort means: hit .397 vs middle .350 vs low .300, but this is not causal.
- Cross-channel genre contract changes packaging rules: Ironcrest creature thumbnails use scale/protection; FablePop uses clean transformation/before-after; Epic uses cinematic creature/kingdom scale; The Next Show uses mythic scale/iconic adventure; RIFTBORN uses franchise creature branding.
- Failure within a channel often reflects off-format/off-brand content (trailers, tool demos, documentary/dinosaur pieces) rather than simply inferior thumbnail craft.

Epic site/source notes:

- https://epicaifilms.com/ positions the channel as “One filmmaker. Limitless worlds. Original feature films watched by millions. Made by one person.” Site is thin/portfolio-like in static HTML; do not treat it as transparent production-process documentation.
- https://crateh.com/ is useful as a curated AI-film box-office/premise-format comparison source. It explicitly distinguishes prologue/chapter/compilation and evidence behind production claims.
- https://metamovies.ai/ai-movies/ HTML fetched to `C:/Users/Administrator/metamovies_ai.html` but not yet analyzed.

Immediate next high-value work after rollover:

1. Finish downloading/analyzing all Ironcrest remaining videos. Download process running/started with IDs `GlTDPApzNYU`, `Aa0l5km5Jl4`, `fmJUSCDP-r4` into `C:/Users/Administrator/ironcrest_media`, raw dir `data/raw/piped_ironcrest`, log `data/raw/ironcrest_download.log`. `2YkJl0KV3gs` already analyzed. User explicitly asked all Ironcrest videos deeply.
2. When mp4s finish, run `tools/batch_media_analysis.py --media-dir C:/Users/Administrator/ironcrest_media --raw-dir data/raw/piped_ironcrest --out-root C:/Users/Administrator/ironcrest_analysis --workers 2`.
3. Inspect openings/endings/contact sheets/subtitles visually and write `knowledge/market/ironcrest-deep-dive.md` with timestamped hit/middle/failure comparisons.
4. Fix `classify_genre` before relying on aggregate genre summaries: mythic adventure titles (Sinbad/Aladdin/Jason/Odyssey/Thor/etc.) are currently often misclassified as general_emotional_drama. Treat existing genre aggregate as rough only.
5. Retry Future Frame channel archive using alternate Piped instances. One probe command was launched but may not have completed before rollover; instances tested included kavin.rocks, adminforge, reallyaweso.me, private.coffee, drgns.space.
6. Analyze metamovies.ai and crateh in more detail; extract additional small breakout channels from last 7–14 days.
7. Build thumbnail hit/low comparisons specifically inside each priority channel without duplicate overlap when channel has fewer than 12 videos. Current montage generator duplicates rows for small archives because it blindly takes first+last 6; visual evidence still usable but montages should be fixed.
8. Continue integrating everything into the reusable skill/production system. Do not stop unless user explicitly says stop.
