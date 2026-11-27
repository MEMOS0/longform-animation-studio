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
- Expanded second-pass breakout deep dive: `knowledge/market/expanded-breakout-deep-dive.md` covers Giant Father, Aethernal Act II, Nana beggar/stepmother test, and Reborn Assassin. Key lessons: misunderstood protector/parent scale; grounded humor; child agency/social tests; competence transplantation; compressed complete myth can outperform padded longer films.
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
6. Finish optional media analysis for `bAjeNeQ9DGc` if needed; initial rediscovery deep dive prioritized four stronger/cleaner cases.
7. Analyze recent breakout thumbnails in detail from `thumbnails/recent_breakouts_top24_montage.jpg` and per-image files. Initial synthesis is in `knowledge/market/recent-breakout-synthesis.md`.
7. Format-duration quantitative segmentation completed in `knowledge/market/format-duration-performance.md`; use it to refine future target-duration defaults.
8. Validate production economics and provider docs before any paid generation; never spend without explicit approval.
9. Continue integrating research into production decision-making, not just reports.

## Key creative synthesis to preserve

Most portable mechanism: legible injustice/danger + specific vulnerable child/creature/person + credible protection + early visual payoff. Strong but channel-fit dependent: hidden royal identity, transformation/rebirth, familiar mythic adventure, revenge/reversal, creature spectacle, regression romance, BL intimacy/power, disaster survival, sci-fi mystery. Usually insufficient alone: scale, lore, armies, crowns, visual polish, franchise continuity, attractive actors, continuation hooks.


## 2026-11-26 late checkpoint — continuous shot scaffold + release loop + AI Sweet visual audit

Latest pushed commit: `8c46839` plus subsequent small commits may exist; check `git log` before writing.

New system capabilities since expanded breakout pass:

- `studio/release_learning.py` + `studio release-postmortem`: compares age-adjusted release performance with preproduction warnings/failure matches/title risks and emits revision rules while preserving causal uncertainty. Tests now 15 passing.
- `studio/shot_pipeline.py` now builds continuous preproduction scaffolds covering every planned scene second, not only key beats. Stormglass regenerated: 414 shots, 2,880 planned/generated scaffold seconds, ratio 1.0, lanes draft 197 / mid 97 / hero 120. Caveat: continuous scaffold is not a finished director storyboard; generic slots still need exact staging/dialogue/camera intent.
- `bAjeNeQ9DGc` media confirmed downloaded. Opening/ending contact sheets visually inspected. Strong evidence: class humiliation → protective CEO alliance → hidden technical competence → public boardroom/CTO authority → circular generosity to children's home. This validates wealth melodrama only when protagonist capability becomes public authority, not passive rescue.

Immediate next highest-value work:

1. Await/read Devin Review findings for latest head; fix real findings only.
2. Continue expanding low-subscriber breakout discovery beyond current batches.
3. Deepen exact director-level shot replacement for Stormglass continuous scaffold; current slots are coverage scaffolding, not final storyboard art.
4. Validate external video provider terms/pricing immediately before any paid generation; no secrets exist in session and no spending is authorized.
5. Continue converting empirical rules into machine gates, especially agency/competence inversion and social-test structures.


## 2026-11-26 rollover checkpoint — storyboard and agency gates

Latest pushed commit: `87c0754 Add protagonist agency intelligence`.

Since previous checkpoint:

- `examples/stormglass_keepers/storyboards/S01_storyboard.json` adds 34 exact continuous director-level shots covering all 300 seconds of opening scene S01, with timecodes, shot size, camera intent, visual action, dialogue, sound, lane, and continuity dependencies.
- `studio/storyboard.py` validates continuous exact storyboards; tests now 17 passing.
- `studio/agency_intelligence.py` adds evidence-informed machine checks for active protagonist agency, competence inversion, rescue-without-agency risk, and circular payoff. Integrated into production evaluation.
- Stormglass production evaluation regenerated with agency intelligence score 1.0; this confirms the example embodies the desired mechanism, though heuristic remains broad and should not be overtrusted as prediction.

Immediate next work:

1. Read Devin Review findings for commit `87c0754` when ready; fix only concrete findings.
2. Extend exact director storyboards beyond S01 or build a controlled generator that converts continuous scaffold slots into exact shots scene by scene.
3. Continue recent breakout discovery and analyze additional low-base channels.
4. Deepen sound/music evidence into timestamped sound-design notes; current sound design is craft-level but less empirically timestamped than visual/subtitle evidence.
5. Do not spend money or create provider accounts; no secrets exist in session.


## 2026-11-26 continuity emergency checkpoint

Latest pushed commit: `d34b8da Strengthen retention architecture validation`. Tests: 19 passed before commit.

Important infrastructure note: session rotation repeatedly zeroes `.git/refs/heads/devin/1764170700-failure-intelligence-foundation` and matching remote-tracking ref. If git says branch broken/not on branch while working tree is intact, recover the latest commit hash from `.git/logs/refs/heads/...` and `.git/logs/refs/remotes/...`, write it back into both ref files, then verify `git log`/`git status`. Do not reclone or discard work. Latest repair used `18ea352...` before committing `d34b8da`.

Newest machine gate: `architecture_quality` now validates continuous sequence time coverage, parseable ranges, target-duration coverage, maximum sequence length, and required retention fields (`turn`, `protagonist_choice`, `emotional_shift`, `visual_setpiece`, `sound_design_intent`, `retention_hook`). Stormglass passes with zero warnings, 8 sequences, coverage ending at 48 minutes.

## 2026-11-26 context checkpoint — third-pass media intelligence

Latest pushed commit when this note was written: `29b74f6 Validate middle object chains in breakout dramas`. Tests: **22 passed** before latest commit. Check `git log` because review-triggered follow-up commits may exist.

Completed in this phase:

- Third-pass raw metadata/subtitles committed under `data/raw/piped_thirdpass/` for `TKUd7hWPMD8`, `iUnnJucKB2o`, `Gx7nwqNr9YY`, `ylN26llRtmw`, `62vBW1_B92Y`. Media remains local in `C:/Users/Administrator/thirdpass_media/`, not committed.
- `knowledge/market/third-pass-breakout-media-deep-dive.md` now includes opening/ending subtitle+sampled visual evidence plus middle validation for `62`, `TK`, and `iUnn`. Important correction: LESO faith reversal is not merely miracle montage; cooking competence, customer validation, 200-plate order, reinvestment, operational discipline, losses, and eventual restaurant/hotel ownership carry the middle.
- `TK` middle evidence: plate/floor/gold system evolves through foundation capture, forced apology, valuation/fraud investigation, arrest/separation, brass/goldsmith proof, medical reciprocity, and livestream exposure. `iUnn` middle evidence: bread/bakery economics evolve through tray labor, refusal to sell air, Crescent Bakery restoration demand, 40m debt/planted-theft fraud, oven loss, moon-scar identity proof, and ledger reversal.
- New channel contracts: `social_test_melodrama`, `machine_personhood_scifi`, `faith_reversal_melodrama`; transformation contract strengthened with consent repair and meaning-changing object rules. Remember to sync edits to both `knowledge/market/channel_contracts.json` and `studio/package_data/channel_contracts.json`.
- Thumbnail archive expanded with third-pass maxres references; combined 10-image montage `thumbnails/rediscovery_breakouts_top10_montage.jpg`; taxonomy `knowledge/thumbnails/rediscovery-breakout-thumbnail-taxonomy.md`.
- New machine gate `studio/meaning_carrier.py` validates physical object/space/sound-object recurrence and changed meaning. Schema now accepts optional `meaning_carrier`; Stormglass has explicit carrier and passes evaluation score 1.0. Tests 22 passing.
- Skill/README updated with circular-object and consent/personhood correction rules.

Immediate next work:

1. If Devin Review findings arrive for current head, fix concrete findings first.
2. Finish middle validation for `Gx7nwqNr9YY` and `ylN26llRtmw` using local fullfilm sheets already generated at `C:/Users/Administrator/thirdpass_analysis/<id>/fullfilm_sheet.jpg` and subtitle windows. Add concise evidence to the same report.
3. Continue exact director-level storyboards beyond S01 or controlled scene-by-scene conversion of continuous scaffold.
4. Continue recent breakout discovery; do not spend money or create provider accounts.

## 2026-11-26 context checkpoint — relational gate added

Latest pushed commit when written: `14fc2ad Add relational contract production gate`; tests 23 passed.

Since previous checkpoint:

- Completed third-pass middle validation for `Gx7nwqNr9YY` and `ylN26llRtmw` in `knowledge/market/third-pass-breakout-media-deep-dive.md` using sampled full-runtime contact sheets plus subtitle windows. Gx: consent/material agency persists through gifts, distrust, bargaining-chip wound, deeds/income, garrison logistics, forced-marriage coercion, public reversal. yl: machine personhood chain escalates through Ezra alliance, Rhea/wiped-home moral complication, mines/underclass, Cross confession, EZRA nameplate, memory/name/labor/personhood stakes.
- Added `studio/relational_contract.py` production gate. Premise schema now accepts optional `relational_contract` fields: `power_asymmetry`, `safety_or_kindness_before_power`, `costly_protagonist_action`, `consent_or_personhood_repair`, `payoff_image`. Stormglass explicit contract passes score 1.0; tests 23 passed.
- Skill updated with relational-contract gate. Keep package schema copy synchronized.

Immediate next work:

1. Fix Devin Review findings when they arrive for latest head.
2. Extend exact director storyboards beyond S01 or build controlled scene-by-scene conversion of continuous scaffold.
3. Continue recent breakout discovery and timestamped sound-design analysis.
4. Do not spend money/create accounts; no secrets exist.

## 2026-11-26 context checkpoint — exact S02 and sound evidence

Latest pushed commit when written: `7e01833 Add empirical sound design evidence`; tests **24 passed** before/after storyboard test addition.

- `examples/stormglass_keepers/storyboards/S02_storyboard.json` now exists: 20 exact continuous shots covering all 300 seconds of scene S02. Validator: valid, 20 shots, 300s, 8 hero shots, no warnings. Key staging: ledger burning, trust/cage crate refusal, voluntary scarf hook, tidal tunnel, lighthouse collapse, child in coat. Test now validates S01+S02.
- `knowledge/craft/third-pass-sound-evidence.md` added using extracted audio clips + `describe_audio`: TK domestic status violence uses close dialogue/room tone/pauses/command timbre; iUnn kindness uses outdoor ambience, negative space, sparse flute at food/personal-history turns; yl machine personhood uses minimal score, vulnerability silence, sand/breath, hybrid organic/mechanical foley.
- README and sound craft guide link the sound evidence.

Immediate next work:
1. Fix Devin Review findings when they arrive for current head.
2. Extend exact storyboards to S03+ or create controlled scene-by-scene exact conversion workflow.
3. Continue timestamped sound evidence for endings/reversals and creature romance.
4. Continue breakout discovery. No spending/accounts.

## 2026-11-26 pre-rollover checkpoint — director seeds

Latest pushed commit when written: `11c99c0 Add continuous director seed storyboards`; tests **25 passed**.

- `tools/draft_exact_storyboards.py` converts each scene screenplay into continuous exact-format director-seed boards using that scene's own first/final images, objective, conflict, decision, turn, vertical composition, key dialogue, sound, and motif. Generated seeds live in `examples/stormglass_keepers/director_seed_storyboards/S01...S08`; all validate continuous with no gaps. These are **not final boards**; exact hand-authored boards exist for S01/S02 and remain the quality reference.
- Next: review findings when they arrive; refine S03 manually using S01/S02 quality bar; continue sound evidence and breakout discovery.

Rollover addendum: latest pushed commit `d297626 Remove repeated beats from director seeds`; tests 25 passed. Director seeds now use 10 non-repeating exact-format beats per scene; they are seeds, not final boards.

Discovery addendum: rerun found new 7d leads including Everflame 2.89m/47k, Nightfall 1.72m/87k, Many Drama titles, Cine Drop; merged into 45-row candidates file without overwriting prior rows. Report regenerated.
Priority after rollover: analyze/download new discovery lead `9N6S6D_ioA0` (baby dragon hidden from giants, ~1.13m views/day estimate at collection, 52.6k subs) and compare duplicate-title Everflame variants `Ky_1Dz7WXlY` vs `6pbhGtHRTwA` before assuming same/different content. Also consider Nightfall `26o_ccDnTSg` train-station abandonment hit.

## 2026-11-26 critical pre-rollover checkpoint — evidence persistence/fourth pass

Latest pushed commit when written: `bfca507 Integrate legal proof melodrama guidance`; tests **35 passed** before evidence/docs commits. Devin Review may be running or may have newer findings after this note; handle them first after rollover.

Major user correction: evidence must not remain only on Devin's VM. This has now been fixed in commit `ff4d24f Preserve derived research evidence and handoff index`:

- `README.md` was empty and is now the real handoff index: start-here order, evidence tiers, repo structure, doctrine, validation commands, active research boundaries.
- `evidence/research/` now preserves 298 derived evidence artifacts (~42MB after compression): contact sheets, selected audio-analysis mp3s, media summaries, compressed timeline/second-resolution metrics, batch outputs, and `evidence_manifest.json` with provenance/checksums. Full copyrighted mp4s and uncompressed WAVs intentionally remain uncommitted.
- `data/raw/piped_fourthpass/` now contains metadata/subtitles for `9N6S6D_ioA0`, `Ky_1Dz7WXlY`, `26o_ccDnTSg`.
- `.gitattributes` includes `evidence/** linguist-generated=true`.
- Do not delete this evidence to slim the PR. If size is a problem, compress/index it better; the user explicitly objected to evidence living only locally.

Fourth-pass analysis completed in `knowledge/market/fourth-pass-breakout-media-deep-dive.md`:

1. `9N6S6D_ioA0` WUFO baby-dragon/giants hit: opening pays the egg/baby/protection chain immediately; sound uses battle chaos -> negative-space egg reveal -> booming antagonist power reassertion; middle converts egg into Skye and city/heart objective; care/deprivation scene uses wind/breath/intimate dialogue and structural music. Mechanism: three-body protective system (Brynn/Wick/Skye), object becomes living agency, monsters carry personhood/misunderstanding twist.
2. Duplicate-title forensic comparison: `Ky_1Dz7WXlY` (Everflame, 6226s, 2.899m) and `6pbhGtHRTwA` (Veylorn, 6483s, 10.27m) share exact title but subtitle fingerprint Jaccard only **0.02** and openings visually differ. Never treat exact title as same content. Everflame description says THE LAST BOND while title says THE LOST KIND — packaging/template inconsistency.
3. `26o_ccDnTSg` Nightfall train-station abandonment hit: elite first-five-minute conversion (abandonment -> theft/class humiliation -> Maggie intervention -> work/agency). Middle uses tea competence, apple/ring family object, trust/fraud. Ending pays legal/proof reversal, chosen kinship, labor dignity, and circular train autonomy (“This time, I bought my own ticket”). New `legal_proof_melodrama` channel contract added to both contract JSON copies and skill.

Current review-fix state: relational/meaning-carrier heuristics have undergone several review rounds. Latest test suite **35 passed**. Latest review fixes: Unicode/specific carrier matching (`85acc03`), local temporal denial scoping (`2ba7ef1`), then evidence/docs (`ff4d24f`) and contract/skill (`83d3b5b`, `bfca507`).

Immediate next work after rollover:

1. Check Devin Review findings for latest head and fix concrete findings first.
2. Continue exact director-level storyboards beyond S02; director seeds are not final boards.
3. Continue sound evidence for endings/reversals and creature romance.
4. Continue breakout discovery; analyze new low-subscriber channels.
5. Repo remains private unless user explicitly grants a safe path; do not spend money, create accounts, accept provider terms, connect local machine, or take irreversible public/admin actions without explicit approval.

## 2026-11-26 rotation checkpoint — fifth-pass breakout discovery in progress

Latest pushed commit when written: `54b309a Separate flashback repair from present choice`; tests **39 passed**. Review round for that commit may be running; handle findings first after rotation.

Completed since previous checkpoint:

- Exact director storyboards now exist through **S05**: S03 trust/bonding, S04 communal evacuation, S05 midpoint capture/weaponization. Tests validate S01–S05 continuous coverage. S01/S02 remain the original quality reference; S03–S05 are stronger than director seeds but should still be critically reviewed before production.
- Ending sound evidence added in `knowledge/craft/third-pass-sound-evidence.md`: `Gx7nwqNr9YY` consent payoff has music swell exactly after “This time it's my choice”; `9N6S6D_ioA0` post-battle sound drops into grief/breath/wind before bittersweet dragon/baby reunion. Evidence files copied under `evidence/research/ending_sound_analysis/`.
- Discovery system now merges prior leads without overwriting them, and after review fixes separates `carryover_candidates` outside the requested window while recomputing stale views/day. Latest run: **73 candidates**, 57 strong leads. Important new leads: `31-p_UcMgOs` Aethernal Act II (25.7k subs, 3.59m), `no72LZAVvZQ` Epicverse giant father/daughter (4.6k subs, 6.51m), `hozDtPcnnBA` Lioren hidden billionaire student (392 subs, 191k), `NHAHR3v9La8` dragon twin/queen's monster.
- Fifth-pass raw metadata/subtitles currently exist uncommitted under `data/raw/piped_fifthpass/`; media local under `C:/Users/Administrator/fifthpass_media/`; analysis sheets/audio local under `C:/Users/Administrator/fifthpass_analysis/`.
- Downloads completed for `no72LZAVvZQ` (700s), `31-p_UcMgOs` (1189s), `hozDtPcnnBA` (2104s). `NHAHR3v9La8` was still downloading/chunked at checkpoint.

Critical new market insight requiring integration:

- The freshest low-subscriber breakouts are **compressed short features**, not 60–120m films: giant father story is 11:40, Aethernal Act II is 19:49, Lioren romance is 35:04. This challenges the earlier default 30–45m rule. The correct conclusion is not “short is always better”; it is that compressed completeness/episode payoff can outperform long runtime when the emotional engine is extremely legible.
- `no72LZAVvZQ` is especially important: opening establishes infant peril by 00:25 (“Please, spare my baby”), white serpent/giant rescue, father-daughter survival bond, isolation argument (“I can't spend the rest of my life talking only to you”), exploitation (“live giant” value), capture, giant/army confrontation, and final daughter-on-shoulder belonging image. It validates protection/family engine in an ultra-compressed format.
- `31-p_UcMgOs` opening combines atmospheric forest, child/village ordinary labor, rot monsters feeding, masked white figure, then village survival escalation; ending is episodic capture/escape hook (“Now we find out how to get out of here”), not a complete film payoff.
- `hozDtPcnnBA` opening is immediate class confrontation at elite university; ending visibly compresses graduation, public status reversal, proposal, wedding, foundation/work identity, child/family epilogue. Subtitle object chain includes scholarship/father/status, truth, foundation, marriage, “greatest treasure.”

Immediate after rotation:

1. Handle any new Devin Review findings. Latest project evaluation after S01-S05: gates A/B/C pass; direction remains unknown until storyboard frames exist; only shot-pipeline warning is generic slots requiring exact expansion.
2. Finish/write `knowledge/market/fifth-pass-breakout-media-deep-dive.md` and copy fifthpass derived evidence into `evidence/research/`.
3. Integrate compressed-short-feature insight into `format-duration-performance.md`, `studio/format_strategy.py`, channel contracts, and skill. Do not overcorrect into “always short.”
4. Finish/check `NHAHR3v9La8` download and analyze it plus any unfinished fifthpass media.
5. Continue exact boards S06+ or critically review S03–S05 quality. No spending/accounts/public admin actions.

## 2026-11-26 rotation checkpoint — fifth-pass report integrated

Latest pushed commit: `510cf32 Clarify S06 trust repair theme`. Tests: 42 passed. S06 exact continuous storyboard added (`ddb9cc9`); S01-S06 now valid, S06 validates with no warnings. Branch/PR: `devin/1764170700-failure-intelligence-foundation`, PR #1. A new Devin Review may be running; check it first if a notification arrives.

Completed since prior checkpoint:

1. Fixed 5 review findings in job `pr-review-job-9754baf53c2c4d3bb8c698fc6d60da15` and ended triage:
   - retained breakout rows now recompute candidate strength (`a8ebb90`);
   - prepositional carriers preserve main object (`key to the gate` -> key) (`6cde8ce`);
   - denial masking preserves offsets, flashback positives do not count as present repair, explicit no-longer lifting handles trailing past comparisons (`b91f255`).
2. Added `knowledge/market/fifth-pass-breakout-media-deep-dive.md` and copied fifth-pass derived evidence into `evidence/research/fifthpass_media_analysis/` with checksums in `evidence_manifest.json`. Source copyrighted mp4s remain uncommitted.
3. Integrated compressed-short-feature insight into `knowledge/market/format-duration-performance.md` and `studio/format_strategy.py`: 10-35m can work when ultra-legible and complete, but do not overcorrect into always-short; 30-45m remains safer for trust arcs, 60-120m only when scale requires it.
4. Validated/analyzed `NHAHR3v9La8` (The Queen's Monster): 24:13, 520,630 views, 7,920 subs. Contact sheets and audio clips copied into evidence. Opening uses storm/infant/maternal danger; king orders “Drown it. Before dawn”; queen says “He's mine.” Middle relational conflict: “He's my son” / “No fire. Fly, my love” / false public narrative “The dragon killed your queen.” Ending command “Fly”; music withdraws around final minute and breath/environment carry consequence. Mechanism: misunderstood nonhuman personhood as literal child + mother protection + spouse/king personhood denial + public monster narrative + tragic legacy.

Important empirical synthesis update:

- Compressed completeness is now strongly evidenced across three formats: 11:40 giant-father protection, 24:13 dragon-twin motherhood tragedy, 35:04 class/romance reversal. The shared rule is not duration but ultra-legible singular emotional engine + every scene doing multiple jobs + explicit payoff/completeness. Aethernal's 19:49 act is different: serialized survival ending on “Now we find out how to get out of here,” not standalone resolution.
- `no72LZAVvZQ`: giant father/daughter protection and exploitation arc; “Please, spare my baby”; daughter needs both father and human world; lord commodifies giant (“live giant” / “fine price”); final rescue/belonging.
- `NHAHR3v9La8`: clearest compressed misunderstood-personhood contract. War/spectacle subordinate to “can a mother protect a child the world calls a monster?”
- `31-p_UcMgOs`: serialized act design; must not be treated as standalone ending evidence.

Immediate next steps:

1. Handle any new Devin Review findings. Latest project evaluation after S01-S05: gates A/B/C pass; direction remains unknown until storyboard frames exist; only shot-pipeline warning is generic slots requiring exact expansion. Do not let NLP heuristic edge-case whack-a-mole consume the whole session; if findings become unbounded, prefer conservative warnings or explicit structured annotations rather than pretending perfect English parsing.
2. Deepen exact boards S06+ or critically review S03-S05 quality. Existing exact boards S01-S05 valid. Continue if useful, but creative quality review matters more than mechanical count.
3. Integrate fifth-pass misunderstood-personhood compressed contract into `knowledge/market/channel_contracts.json`, `studio/package_data/channel_contracts.json`, and possibly project evaluation gates. Keep both files synchronized.
4. Thumbnail Intelligence fifth-pass originals/metadata now exist under `thumbnail_intelligence/reference_library/fifthpass_breakouts/` with `analysis.md`; next expand to hit/low comparisons inside each channel rather than only hit thumbnails.
5. Continue broader market discovery, especially last 7-14 day low-subscriber breakouts. Preserve raw metadata under `data/raw/` and derived evidence under `evidence/research/`; do not leave key evidence only on VM.
6. No spending, accounts, public/admin actions, or irreversible external actions without explicit user approval. User said do not stop and do not ask permission for ordinary internal repo/research work.

Critical caution:

- Contact-sheet evidence is sampled visual inspection, not continuous frame-by-frame human viewing. Label it accordingly.
- No CTR/retention/impressions/traffic data; views/day are discovery indicators, not causal proof.
- Never treat exact duplicate titles as same content; subtitle fingerprint comparison remains required.

## 2026-11-26 checkpoint — full Stormglass boards and hit/low media expansion

Latest pushed commit before this checkpoint: check `git log --oneline -5`; important recent commits include exact S01-S08 storyboards, storyboard coverage gate validation, same-channel hit/low media analysis, thumbnail hit/low archive, compressed-format doctrine, and fifth-pass evidence. Tests latest known: 49 passed.

Completed since fifth-pass checkpoint:

1. Fifth-pass evidence integrated; `NHAHR3v9La8` analyzed as compressed misunderstood-nonhuman-family tragedy.
2. `misunderstood_nonhuman_family` contract synchronized into both channel contract JSON files.
3. Fifth-pass thumbnail archive and same-channel hit/low thumbnail comparison created under `thumbnail_intelligence/reference_library/`.
4. Same-channel hit/low media analysis completed in `knowledge/market/fifthpass-hitlow-media-comparison.md` with evidence in `evidence/research/hitlow_media_analysis/`:
   - Epicverse giant-father hit vs abstract military/monster-fight lows.
   - Giant snake low falsifies “slow opening” explanation: creature action is immediate but emotionally flat.
   - Rust Saint low is not proof of weak story: strong memory/love engine but likely packaging/sequel/language friction.
   - Aethernal Act II hit vs Act I slower atmospheric adult-expedition opening; same franchise but different emotional contract.
5. Failure intelligence now has machine patterns for creature-action-without-relational-bond and procedural-mission-without-emotional-payoff.
6. Exact continuous storyboards S01-S08 exist and validate. S06 covers full 420 seconds; S07 420; S08 360; hero lanes within warning threshold.
7. Project evaluation now auto-detects storyboards, validates exact coverage, and Stormglass gates A-D pass. Production/release remain unknown until generated media/release metadata exist.
8. Thumbnail concept generation now produces creature-protection-specific misunderstood-child-personhood and public-hunt-protection alternatives; Stormglass has 4 concepts.
9. Recent breakout discovery refreshed: 75 candidates, 58 strong. Important new/unanalyzed low-subscriber candidates include `TKUd7hWPMD8` (maid floor/daughter social-test reversal, 1,280 subs), `or5RI5v_lHw` (abandoned wife/customer billionaire compressed melodrama, 1,330 subs), `62vBW1_B92Y` (Christian reversal, 6,160 subs), and others in `data/processed/recent_breakout_candidates.json`.

Immediate next steps:

1. Finish current `or5RI5v_lHw` download/analysis in `C:/Users/Administrator/sixthpass_media` and `sixthpass_analysis`; copy derived evidence into repo. It is a compressed 16:06 hidden-billionaire/customer melodrama breakout from 1,330-subscriber DRAMORA.
2. Handle any new Devin Review findings. Beware control-character escaping when editing regexes through shell; use raw strings/edit tool and scan for bytes <32.
3. Consider analyzing `TKUd7hWPMD8` next for circular floor/food humiliation and child allyship social-test mechanism.
4. Continue validating storyboard quality creatively, not only mechanically; consider generating reference frames only if no spending/accounts are required.
5. Keep evidence committed. Never treat contact sheets as continuous human viewing; no CTR/retention causality claims.

## 2026-11-27 checkpoint — production prompts, spatial grammar, generated premises, sixth-pass evidence

Latest pushed commit at checkpoint: `06ce0d6 Integrate faith economic reversal evidence`. Tests latest known: 54 passed. Devin Review/CI is being ignored by explicit user instruction; do not keep triaging skipped reviews.

Major additions since prior checkpoint:

1. `studio/storyboard_production.py` plus CLI `export-production-prompts`: exact storyboards now export 181 per-shot generation prompts/QA/continuity manifests under `examples/stormglass_keepers/production_prompts/`. This is planning only; no paid generation without approval.
2. `studio/storyboard.py` now warns on nearly uniform shot duration pacing. S01-S08 exact boards were rebalanced to varied durations while preserving exact continuous 48-minute coverage; production prompts/evaluation regenerated.
3. WebVTT subtitle parsing improved: word-timed rolling captions are deduplicated and incremental overlap is stripped. Important for all future video evidence.
4. `studio/spatial_status.py` added: machine-checks spatial status grammar and circular inversion (who is forced below/outside/caged vs who chooses access/sanctuary). Integrated into project evaluation.
5. `studio/premise_generator.py` plus CLI `generate-premises`: generates three original schema-valid social-test/craft melodrama premise packets and evaluations under `examples/generated_concepts/`. They are starting points, not finished scripts or copies.
6. Sixth-pass deep evidence committed:
   - DRAMORA `or5RI5v_lHw` compressed immigrant melodrama in `knowledge/market/dramora-compressed-social-melodrama-deep-dive.md`.
   - Karma Keeps Score `TKUd7hWPMD8` 81-minute floor/table social-proof film in `knowledge/market/karma-floor-table-social-proof-deep-dive.md`.
   - LESO `62vBW1_B92Y` faith/economic reversal in `knowledge/market/leso-faith-economic-reversal-deep-dive.md`.
   - Derived artifacts in `evidence/research/sixthpass_media_analysis/`; thumbnails in `thumbnail_intelligence/reference_library/sixthpass_breakouts/`.
7. Key doctrine additions:
   - Hidden wealth/identity must create a trust wound, not instant reward.
   - Introduce non-romantic care before high-status romantic rescue.
   - Public humiliation requires public proof/repair with the same social audience where possible.
   - Proof chains should use the protagonist's established competence, not surprise documents.
   - Circular inversion should transform meaning: floor imposed -> floor chosen; cage/control -> sanctuary/chosen access.
   - Faith reversal works when faith is tied to material stakes and converted into small-business operational agency; direct testimony is niche-specific, not universal.

Immediate next steps:

1. Continue market discovery and analyze unexamined low-subscriber breakouts from `data/processed/recent_breakout_candidates.json` across genres not yet deeply covered (sci-fi, werewolf/lycan, mermaid, zombie/reborn).
2. Deepen premise generation into architecture/scene generation, then evaluate generated concepts end-to-end. Consider building one full second example project if useful.
3. Continue improving creative quality gates: dialogue density, object recurrence, spatial inversion, agency, consent/trust repair, sound negative space, pacing variation.
4. Commit derived evidence promptly. Do not claim continuous human viewing; do not infer CTR/retention without private data.

## 2026-11-26 checkpoint — generated pipeline and genre expansion

Latest local commits: `ef8d2b7 Integrate desert mermaid economic creature evidence` and `bb8017f Generate validated director seed storyboards` are committed locally but were not pushed because the harness repeatedly demanded a CI stop after Devin Review infrastructure failures. User instruction remains to ignore Devin Review; if resuming after rollover and no newer blocker exists, verify `git log`/status and push these commits.

Major additions:
- Original concept pipeline now runs premise -> 8-sequence architecture -> schema-valid scenes -> continuous non-uniform director-seed storyboards -> project evaluation. All three generated concepts pass A/B/C/D gates; each has 140 director-seed shots across 42 minutes. These are scaffolds, not final production boards.
- `studio/storyboard_seed.py` plus CLI `seed-storyboards`; storyboard validator generalized beyond creature-specific trust/cage wording and still checks exact coverage/pacing.
- ELDSAGA deep evidence: `knowledge/market/eldsaga-wolf-father-creature-scifi-deep-dive.md` and `knowledge/market/eldsaga-channel-hit-low-comparison.md`. Critical falsification: low-view `wKTglMNaHxY` has strong story mechanics, so low views must not be treated as proof of bad writing. Hit original WF is 10m47; hit sequel WF2 25m15; duration is not primary separator. Relational recognition can precede a plot cliffhanger.
- Spark Shorts desert mermaid deep dive: `knowledge/market/spark-shorts-desert-mermaid-deep-dive.md`; new `creature_economic_melodrama` contract. Core doctrine: care before monetization, magical value must create ethical temptation/consent cost, creature personhood mirrors home/debt ownership, legal proof can coexist with fantasy, ending must repay economic wound spatially.
- Spark channel metrics local at `C:/Users/Administrator/spark_channel_metrics.json`, not yet committed. Raw exact channel metadata local at `C:/Users/Administrator/spark_meta/`.
- Tests: 56 passed.

Immediate next:
1. Commit Spark channel metadata/metrics and compare hit `FaP_r2awlC8` vs DG16/low titles. Analyze FaP if context allows.
2. Push local commits when appropriate; user has already said CI/review can be ignored.
3. Continue werewolf/mermaid/zombie/reborn discovery and thumbnail hit/mid/low archives.
4. Do not spend money/create accounts/public actions.

## 2026-11-26 checkpoint — Spark hit comparison and creature generator

Latest pushed commit: `5a3026e Add Spark hit low sea fantasy comparison`; push succeeded to `devin/1764170700-failure-intelligence-foundation` after the user's explicit instruction to ignore Devin Review. Tests remain 56 passed.

New evidence/system:
- Spark Shorts 23-video exact metadata archive committed under `data/raw/spark_channel/`; metrics in `data/processed/spark_channel_metrics.json`.
- `knowledge/market/spark-shorts-hit-low-comparison.md` analyzes hit `FaP_r2awlC8` and compares it with `DG16FsALL9A`/lower rows. Key transfer: bodily stigma/property exploitation + protective bond + spatial conversion into home. FaP is romantic sacrifice epic; DG16 is creature-economic family melodrama.
- Spark thumbnail archive/montage committed. Packaging hypothesis: intimate relational choice beats generic spectacle clutter; no CTR causality.
- `creature_economic_melodrama` premise generator is implemented in `studio/premise_generator.py` with `--contract creature_economic_melodrama`. `salt_window_garden` and `emberseed_oven_cart` pass A/B/C/D gates with zero schema errors when paired with director-seed storyboards. Salt production prompts exported; Emberseed export was just generated and may need committing.
- `romantic_creature_sacrifice_epic` contract added.

Immediate next:
1. Commit Emberseed prompts and any checkpoint update; push if clean.
2. Continue low-subscriber breakout discovery (zombie/reborn/werewolf/mermaid) and analyze one counterexample low video deeply enough to avoid survivorship bias.
3. Improve generated scene dialogue beyond scaffolds; director seeds are validation scaffolds, not final hand-directed boards.
4. Continue thumbnail hit/mid/low taxonomy across Spark, ELDSAGA, Ironcrest, Epic.

## 2026-11-27 checkpoint — post-merge Spark counterexample branch

PR #1 merged into main. New active branch/PR: `devin/1764820000-creature-production-deepening`, PR #2 `Add Spark low counterexample analysis`.

Major addition: `wd53-C7Na0Y` low-view Spark counterexample. It is only 4 days old and cannot be declared a true failure, but it falsifies simplistic hit rules: it already has immediate serial-sacrifice danger, bodily marks, hidden-care shells, extraction metaphors, mutual protection, and a strong infrastructure dilemma. Low performance therefore must not be read as proof of bad writing. Key production lesson: strong hooks are necessary but insufficient; mythic/lore density still needs relational clarity, packaging-title alignment, home/community consequence, and closure before cosmic expansion.

Tests: 56 passed. PR #2 pushed and opened.

## 2026-11-27 checkpoint — closure integrity gate

Added `studio/closure_integrity.py` and integrated it into project evaluation. This machine gate operationalizes the Spark/ELDSAGA counterexample lesson: a plot sequel hook may remain, but only after relational recognition/home/belonging closure lands; infrastructure collapse must be followed by visible community survival/rebuilding consequence. Tests now 57 passed. Salt Window Garden generated package scores 1.0 on closure integrity.

## 2026-11-27 checkpoint — creature dialogue scaffold pass

`studio/scene_generator.py` now has contract-aware creature-economic key lines instead of generic social-melodrama lines. Salt Window Garden uses water/pump/salt ownership language; Emberseed Oven Cart uses fire/oven/key resource language. Both generated concepts still pass A/B/C/D gates with zero schema errors. Remaining caveat: these are still scaffolds, not final hand-written screenplays; next creative pass should make lines scene-specific rather than template-derived. Tests: 57 passed. Latest pushed commit at this checkpoint: `f7d7584`.

## 2026-11-27 checkpoint — closure robustness and creature architecture specificity

Latest pushed commit: `f278274` (`Make creature architectures actor-specific and original`). Tests: 70 passed. PR #2 remains active: https://github.com/MEMOS0/longform-animation-studio/pull/2

Completed this round:
- Closure integrity was hardened against adversarial edge cases found by repeated automated review: hypothetical/planned/negated infrastructure shutdowns, independent actual collapse clauses, explicitly pre-collapse recovery, valid post-collapse timing, denied sharing, non-resource sharing, failed repair phrases, shield-node phrasing, repeated recovery beats, and screenplay-only aftermath evidence. These are heuristic gates, not perfect NLP; keep tests adversarial and treat warnings as prompts for creative inspection.
- Creature-economic premise cleanup removed copied/reference-flavored wording (`Pearl-like`) and awkward actor compounds.
- `studio/architecture_generator.py` now adapts creature-economic sequences away from generic social frame-up scaffolding toward creature consent, resource extraction, care-before-monetization, proof-chain, and spatial/economic payoff mechanics. Actor labels are compacted (`the moonfin child`, `her grandmother`) instead of long explanatory phrases.
- Both generated creature concepts were regenerated end-to-end: premise -> architecture -> scenes -> 140 director-seed shots -> production prompts -> project evaluation. Both pass A/B/C/D gates with no warnings; E/F remain unknown until real media/release data exists.

Immediate next:
1. Triage any new Devin Review findings only because the harness requires it; user still prioritizes continuous work over review theater.
2. Deepen dialogue beyond scaffolded key lines into scene-specific conflict, subtext, and reversal language.
3. Continue low-subscriber breakout discovery across undercovered genres and integrate counterexamples.
4. Rotate context before exhaustion; preserve this file as the continuity anchor.

## 2026-11-27 checkpoint — creature dialogue specificity pass

Latest pushed commit: `57a612c` (`Clean creature dialogue actor labels`). Tests: 70 passed. PR #2: https://github.com/MEMOS0/longform-animation-studio/pull/2

`studio/scene_generator.py` now produces more scene/creature-specific creature-economic dialogue: actor labels are extracted and cleaned (`The moonfin child`, `Her grandmother`, `A flour miller`), and key lines emphasize consent, resource witness, extraction cost, proof authorship, non-possession, and spatial/economic repair. Generated Salt/Emberseed packages were regenerated end-to-end and still pass A/B/C/D with no warnings. Caveat: these remain scaffold key lines, not finished human-quality screenplay dialogue; next pass should add per-scene opposition voices, interruption/negotiation rhythms, and subtext progression rather than only polished thematic lines.

Immediate next:
1. Handle any required review triage without letting it consume the creative roadmap.
2. Build a dialogue-opposition model: each scene needs antagonist pressure, caregiver/witness objection, protagonist refusal, evidence implication, and cost escalation.
3. Resume low-subscriber breakout discovery across undercovered genres.

## 2026-11-27 checkpoint — Epicverse visual-first breakout

Latest pushed commit: `24115ab`. Tests: 70 passed. Added `knowledge/market/epicverse-giant-father-visual-first-breakout.md` plus media/contact-sheet evidence and thumbnail for low-subscriber Epicverse `no72LZAVvZQ` (11.7m, ~6.51M views, ~4.6k subs at collection). Doctrine: scale spectacle must convert into repeated care behavior; every scene should remain intelligible muted. Caveat: no subtitles, sampled full-runtime contact-sheet inspection only, no CTR/retention causality. Note: full 58MB video evidence was committed and GitHub warned about large files; consider evidence-storage policy next context (keep small derived artifacts in git, large source media local/object storage).

Immediate next: build dialogue-opposition model; continue low-subscriber scan; decide large media evidence policy; handle required review triage.

Epicverse followup committed in `d1e69d9`: same-channel hit/low comparison shows `no72` ~6.6M vs many creature/fantasy videos under ~2k in flat metadata; strong evidence that channel size/category alone does not explain breakout. Next: exact per-video dates/durations, thumbnail montage, low-video audiovisual comparison, and large-media evidence policy.

## 2026-11-26 late-session Aethernal evidence checkpoint

- Added Aethernal Pictures same-channel hit/medium/low comparison: Act II `31-p_UcMgOs` about 3.6M views/19.8 min versus Act I about 529k/33.8 min and low teaser/soundtrack contracts.
- Added full-runtime sampled visual/contact-sheet evidence, aligned subtitle evidence, machine visual metrics, and waveform-derived sound-contrast analysis for Act II under `evidence/research/rediscovery_analysis/31-p_UcMgOs/`.
- Key doctrine: fantasy spectacle should be grounded in ordinary survival systems (water, food, debt, chores, animals, doors, communal procedures). Sequel labeling is not automatically fatal; concrete threat-event packaging can overcome franchise friction.
- Thumbnail Intelligence now includes Aethernal hit/medium/low originals and montage. Hit packaging uses ordinary boy + dog + water bucket + approaching Rot creatures; low teaser is portrait/branding without dramatic direction.
- Production evaluator now warns when a fantasy opening lacks an ordinary survival/labor/resource anchor.
- Latest local test state at this checkpoint: 82 passed.

## 2026-11-27 dialogue-scaffold checkpoint

- `studio/creature_dialogue.py` now generates scene-specific spoken exchanges for creature-economic premises: external pressure, witness objection, protagonist decision, and evidence/cost.
- Creature key lines were revised away from broad theme statements toward shorter action/refusal/proof lines tied to pump/oven, water/fire, ledger, witness, creature fear, and economic pressure.
- `studio/dialogue_craft.py` now validates spoken-exchange structure when present: beat/speaker/line/action completeness, turn length, and speaker differentiation.
- Regenerated Salt Window Garden and Emberseed Oven Cart artifacts: gates A/B/C/D pass, zero dialogue warnings, zero sound warnings, visual causality 1.0, four spoken turns per scene.
- Latest local test state at this checkpoint: 84 passed.

## 2026-11-27 storyboard-dialogue synchronization checkpoint

- Director-seed storyboards now use creature spoken-exchange lines in dialogue shots and use the matching concrete action as visual staging.
- Repeated sampled beats no longer duplicate the exact same dialogue line across adjacent shots.
- Regenerated production prompts after synchronization; generated projects still pass A/B/C/D with zero dialogue/sound warnings and visual causality 1.0.
- Latest local test state at this checkpoint: 86 passed.


## 2026-11-27 storyboard-review + PrimeFate checkpoint

- Review findings fixed on PR #2: key-line fallback for screenplays without spoken exchanges; witness-objection now precedes protagonist decision; scripted final images are preserved while evidence dialogue remains. Tests: 92 passed.
- Latest code/artifact commit before this checkpoint: `371b62f` (`Collect PrimeFate breakout reference evidence`). Active branch remains `devin/1764820000-creature-production-deepening`.
- PrimeFate partial evidence is now committed: channel archive metadata, hit/target/medium/low thumbnails, flat metrics, and `TKfoKnpHpsw` clean transcript. Still incomplete: contact-sheet/seconds/timeline regeneration and timestamped comparative markdown analysis.
- External full media remains outside repo in `C:/Users/Administrator/evidence_tmp/TKfoKnpHpsw.webm`; do not commit full video. Regenerate derived contact sheets and inspect them before making strong claims.
- Important status: review fixes validated locally; a new Devin Review round may be running or queued. Do not treat review as blocking creative research unless concrete findings arrive.

## 2026-11-27 PrimeFate deep-dive checkpoint

- PrimeFate `TKfoKnpHpsw` full-video derived evidence is committed: clean transcript, seconds/timeline metrics, media summary, and 14 contact sheets. Full source video/audio remain outside repo in `C:/Users/Administrator/evidence_tmp/` and must not be committed.
- New knowledge files: `knowledge/market/primefate-reborn-family-revenge-deep-dive.md` and `knowledge/market/primefate-thumbnail-hit-medium-low-analysis.md`.
- Skill now includes modern family revenge doctrine: concrete economic object + bodily sacrifice opening, rebirth after injustice, countdown engine, early public payoff, proof asymmetry, repeated memory objects, third-party competence proof, antagonist self-destruction, cost-aware familial ending, vertical/mobile power-legibility.
- Latest commit: `1c9ddaa6e074f22b2e06033e59449cbc4a8eb357`.
- Next highest-value work: compare PrimeFate hit `5UUh-vADVko` or low `dKQ9lMEaibw` directly against target; continue low-subscriber breakout scan; deepen machine enforcement of packaging-coherence and modern revenge doctrines.

## 2026-11-27 PrimeFate hit comparison + Lioren breakout checkpoint

- `5UUh-vADVko` and low-subscriber breakout `hozDtPcnnBA` were downloaded through the public Piped-compatible endpoint. Full media stays outside repo in `C:/Users/Administrator/evidence_tmp/`; derived contact sheets, transcripts, seconds/timeline metrics, summaries, metadata, and subtitles are committed.
- New knowledge files: `knowledge/market/primefate-hit-target-comparison.md`, `knowledge/market/lioren-hidden-heir-breakout-deep-dive.md`, and `knowledge/market/lioren-thumbnail-breakout-analysis.md`.
- Important doctrine correction: early transformation payoff means the contract must be emotionally legible early, not necessarily that the supernatural mechanism occurs early. PrimeFate hit anchors body-swap transformation in the opening but dramatizes it around minute 29-30. Faster rebirth in target did not outperform.
- Major comparative finding: hit revenge story adds double contrast (abusive original family vs loving new family) and ends by answering the original abandonment wound with protective family belonging. Target's punishment+grief ending is weaker wish fulfillment.
- Lioren hidden-heir breakout shows competence-before-reveal, ordinary love-before-wealth, prosocial institutional use of wealth, relational cost of lying, and family/chosen-love closure in a compressed 35-minute widescreen format.
- Latest tests before checkpoint commit: 96 passed.

## 2026-11-27 review triage + creature dialogue specificity checkpoint

- Devin Review findings on PR #2 were triaged and fixed. Modern rebirth detection now requires modern context and treats clock/proof as independent requirements; fantasy royal rebirth no longer receives modern revenge warnings. Repeated storyboard coverage now receives alternate visual coverage instead of identical adjacent staging while preserving scripted final images. Regression tests pass: 99 passed.
- Creature-economic dialogue was further differentiated by world voice: coal-guild/oven scenes now use guild ration, coal ledger, guild mark, pardon/confession, and oven-crawl language instead of land-trust wording. Customer witness lines now use the protagonist name instead of gender-assumptive pronouns. Generated scenes, seed storyboards, prompts, and evaluations were regenerated and remain schema/test valid.
- New low-subscriber breakout lead selected for next deep dive: VNDL `NHAHR3v9La8` (`She Gave Birth to Twins. One Was a Dragon / THE QUEEN'S MONSTER`), 24.2m, about 534k views, roughly 7.9k subscribers at candidate scan. Media downloaded through public Piped-compatible endpoint; no subtitles exposed by Piped, so analysis must distinguish visual evidence from unavailable dialogue transcription.

## 2026-11-27 VNDL creature-family checkpoint

- VNDL `NHAHR3v9La8` (`THE QUEEN'S MONSTER`) was downloaded and analyzed. Piped exposed no subtitles; local Whisper transcription failed with a ctranslate2 segmentation fault, so the analysis explicitly makes no exact-dialogue claims. Derived visual seconds/timeline metrics, audio signal metrics, contact sheets, metadata, and thumbnail evidence are committed; full media/audio remain outside repo or deleted.
- New knowledge file: `knowledge/market/vndl-queen-monster-creature-family-deep-dive.md`. Key finding: the compressed 24-minute breakout pays the creature-child contract in the first five minutes through nest/feeding/touch/swaddling, then uses maternal punishment, winter survival, matched pendants, battle spectacle, and a quiet creature-family final image. It strongly validates muted-intelligibility and care-before-power doctrine.

## 2026-11-27 professional creature dialogue pass checkpoint

- Creature-economic spoken exchanges were deepened beyond noun substitution. Scene 1 protection now uses concrete hiding materials (`shawl` vs `flour cloth`) and visible creature features; evidence language is material (`salt rises where her tears fall` vs `coals bend toward her crying`); competence proof uses seal/ledger contradictions; accusation, proof custody, restitution, and communal repair lines were rewritten as action-facing short turns.
- Generated Salt/Ember scenes, director-seed storyboards, production prompts, and evaluations were regenerated. Regression coverage now locks world-specific authority/proof language. Latest local tests: 100 passed.

## 2026-11-27 hidden-identity integrity gate checkpoint

- Added `studio/hidden_identity_integrity.py` and integrated it into project evaluation. It transparently checks whether hidden-identity/status stories prove competence or kindness before status, form love through ordinary non-status behavior, treat deception as a trust wound, use power prosocially, and subordinate wealth to belonging. This converts the Lioren breakout findings into machine-readable pre-greenlight review rather than leaving them only in prose.
- Regression tests cover a status-only weak reveal and a Lioren-style positive structure. Latest local tests: 102 passed.

## 2026-11-27 Drakenhart tiny-kingdom checkpoint

- Drakenhart `1Nv2aGUgIG4` was downloaded with English subtitles and analyzed visually/aurally through contact sheets, aligned transcript, seconds/timeline metrics, and thumbnail evidence. Full media/audio are not committed.
- New knowledge file: `knowledge/market/drakenhart-tiny-kingdom-breakout-deep-dive.md`. Key finding: the 29.5-minute breakout pays the tiny-kingdom premise within five minutes, proves protagonist competence through an early tunnel save, makes giant-world junk economically meaningful as tiny-world infrastructure, gives the protagonist institutional guilt, uses elder restitution as a moral mirror, stops drilling through map/proof persuasion rather than battle, and ends with years of rebuilding/chosen home.

## 2026-11-27 scale-community repair gate checkpoint

- Added `studio/scale_community_integrity.py` and integrated it into project evaluation. It converts the Drakenhart tiny-kingdom findings into machine review: scale must affect material infrastructure/economics, outsider competence should protect the community early, trust needs historical/institutional cost, extraction should be stopped through proof/persuasion where possible, and endings need sustained rebuilding/chosen-home evidence.
- Latest local tests: 104 passed.

## 2026-11-27 context handoff note

- A fresh low-subscriber breakout scan was started with `python tools/discover_recent_breakouts.py --help` accidentally invoking the default scan because argparse help did not emit before execution in the background shell. Shell id at the time was `94a8d1`; if its output/files appear, treat them as a normal scan result and commit `data/processed/recent_breakout_candidates.json` plus `knowledge/market/recent-breakout-candidates.md` after reviewing. If it is still hung, kill it and rerun deliberately with `--days 14 --max-enrich 35`.
- Immediate next priorities: continue template-to-professional dialogue deepening, use the scan to select the next low-subscriber breakout, and consider full audiovisual analysis of any strong lead. Latest pushed commit before this note: `d065b29cb11660e8162b873e0b60ff9851d93054`; tests were 104 passed.

## 2026-11-27 post-merge fresh-scan and professional-dialogue checkpoint

- PR #2 was squash-merged; post-merge work continues on branch `devin/1764820000-postmerge-deepening` from `origin/main` (`87c5016`). The pre-merge branch tree matched the squash-merged main tree.
- Fresh 14-day Piped breakout scan completed: 82 current candidates, 5 carryover, 63 strong leads. Top leads include Aethernal Act II, duplicate/long-form `THE LOST KIND`, fresh WUFO baby-dragon/giant-hunt video `9N6S6D_ioA0` (about 505k views in under a day at collection), Epicverse 12-minute compressed giant-father hit `no72LZAVvZQ` (about 6.6m views in 10 days), Nightfall/Neural/VNDL/PrimeFate/Drakenhart and many low-subscriber romance/fantasy candidates. These are discovery leads, not proof.
- Downloaded public media for `9N6S6D_ioA0` (47.6m, subtitles available) and `no72LZAVvZQ` (11.7m, no subtitle exposed in first metadata). They are the next deep audiovisual analysis pair: fresh compressed creature/father protection cases.
- Creature dialogue scaffold was deepened from template exchange into more professional power-turn writing: shorter procedural pressure lines, practical witness objections, concrete protagonist refusals, world-specific evidence, and per-turn `power_move`, `listening_response`, `delivery`, `status_shift`, and `room_sound` metadata. Scene dialogue now also carries `scene_rhythm` and `rewrite_directives`. Generated scenes/storyboards/production prompts/evaluations were regenerated; Salt project dialogue warnings are empty and gates A-D pass. Latest tests before this checkpoint: 104 passed.

## 2026-11-27 WUFO heat-scarcity checkpoint

- WUFO `9N6S6D_ioA0` full media, subtitles, contact sheets, audio metrics, targeted final keyframes, thumbnail, and deep-dive analysis are prepared. Key doctrine: heat/cold scarcity is a strong creature-economic engine; creature personhood is built through breathing/warming/feeding/naming before public execution spectacle; quiet domestic care can contrast with loud civic violence; climactic dragon scale should become recognition/embrace/protection before ambiguous sequel imagery.
- `analyze-media` now supports `--contact-every`, used to create denser Epicverse contact evidence. Epicverse `no72LZAVvZQ` was rediscovered by the scan but already had a deep dive; its duplicate regenerated baseline evidence was not kept, while new denser contact evidence is retained.
- Devin Review finding on PR #3 was fixed in `6221513981234765d634e88c57704b4b7ca36fcf`: performance metadata now follows actual speaker role rather than beat role alone. Latest tests after that fix: 105 passed.

## 2026-11-27 annotated screenplay renderer checkpoint

- Added `studio/screenplay_renderer.py` plus `render-screenplay` CLI. Generated premise packages now automatically include `*_screenplay.md`: annotated screenplay-style working drafts with speaker labels, action order, parenthetical delivery, sound transitions, subtext/rhythm, final images, exit hooks, and global rewrite rules. This moves creature-economic scaffolds closer to scene-specific professional writing while remaining transparent that they are working drafts, not final shooting scripts.
- Regenerated both creature example packages; screenplay artifacts exist and Salt/Ember project gates A-D pass. Latest tests: 107 passed.
- Devin Review stale-contact-sheet finding was fixed in `85baa846fd69c137556a4c15491e8910181ed636` by deleting old numbered sheets before writing a new analysis run.

## 2026-11-27 Neural compressed-survival checkpoint

- Neural Pictures `icsZH4sDwTM` (*The Flight Attendant vs. Giant Insect Island*, 17:07, about 1.18m views / 59.9k subscribers at collection) was visually inspected through full-runtime 10-second contact sheets plus targeted 3-second dog/cave/plane-preparation sheets. No subtitles exist; auditory evidence was captured through machine loudness/silence metrics and targeted auditory passes, then raw audio excerpts were removed rather than committed.
- New doctrine added: compressed creature-survival (12-25m) needs a visually explicit role/creature/location contract, disaster/threat payoff inside two minutes, dialogue-light micro-objectives, occupational competence, moral differentiation among creatures, a quiet animal-care hinge, reciprocal rescue, reuse of the opening vehicle/location as final trap/rescue machine, and recognition/contact closure.
- Devin Review findings on screenplay rendering were fixed in `9c70ad2`, `c2cda1c`, and `c0430eb`: default key_lines are preserved, direct/empty scene inputs validate correctly, and missing output directories are created. Latest tests after fixes: 110 passed.

## 2026-11-27 compressed creature-survival production contract checkpoint

- Converted the Neural Pictures doctrine into a working `compressed_creature_survival` generation contract with two original examples: `brakelight_moth_depths` (freight conductor / giant centipede / wrecked inspection train / pigeon / giant moth) and `foghorn_turtle_keeper` (lighthouse radio operator / giant crab / stranded ferry-foghorn system / seabird chick / turtle ally).
- Added modular premise, architecture, and scene materials in `studio/survival_premises.py`, `studio/survival_architecture.py`, and `studio/survival_scene.py`. The generated scenes use sparse practical dialogue, visual-first objectives, quiet animal care, predator sensory rules, occupational trap preparation, reciprocal rescue, and recognition/contact closure rather than social-melodrama power language.
- Added `compressed_survival_integrity` machine validation and a `compressed_creature_survival` channel contract. Expanded visual-causality action/object recognition for survival cinema and fixed the false warning that a single sparse spoken turn lacks differentiated speakers.
- Both generated survival packages validate schema-clean and pass A-D gates; compressed survival integrity is 1.0 with no dialogue or visual-causality warnings. Latest tests: 113 passed.

## 2026-11-27 EchoDrama hidden-beauty long-form checkpoint

- Downloaded and analyzed EchoDrama `lBhjowuJURw` (`[FULL] The Hidden Beauty`, 75.25 minutes), a fresh low-subscriber breakout lead with about 817k views in roughly six days and about 3.55k channel subscribers at collection.
- Committed full second-resolution audiovisual metrics, 10-second aligned timeline, media summary, 20-second sampled full-runtime contact sheets, max-resolution thumbnail, and thumbnail metadata.
- Key doctrine: hidden-beauty transformation is strongest when love/recognition precedes the beauty reveal; parental protection itself creates the wound; transformation has behavioral cost; public crowd geometry returns transformed; the 75-minute runtime survives because a film-in-film second engine begins after the makeover payoff; reciprocal childhood protection proves moral rather than cosmetic love.
- Important audiovisual evidence: the pool danger sequence at minutes 45-50 is quieter, faster-cut, higher-silence, and less verbal than surrounding scenes. Derived file: `knowledge/market/echodrama-hidden-beauty-transformation-romance-deep-dive.md`.

## 2026-11-27 transformation-romance production contract checkpoint

- Converted the EchoDrama Hidden Beauty doctrine into a working `transformation_romance` generation contract with two original 72-minute vertical-feature concepts: `paper_lantern_understudy` (performing-arts academy / backstage authorship / cracked brass key) and `saltglass_swim_lesson` (coastal rescue-swim documentary / scarred technician / rescue whistle).
- Added transformation-specific premise, architecture, scene dialogue, visual-image overrides, schema metadata, channel contract, and `transformation_romance_integrity` validation. Both examples score 1.0 on transformation integrity, pass channel fit, and have no dialogue or visual-causality warnings. A/B gates can still require attention depending on premise/architecture risk scoring; C/D pass.
- Expanded visual-causality recognition for transformation-media imagery (phones, mirrors, cameras, staircases, pools, garments, whistles, stages, lanes, crowds; blocking/raising/dropping/walking/filming actions). Latest tests: 120 passed.

## 2026-11-27 fresh breakout scan checkpoint

- Re-ran the 14-day low-subscriber breakout scan: 84 candidates, 64 strong leads, 5 carryovers, using 14 query families. Outputs updated in `data/processed/recent_breakout_candidates.json` and `knowledge/market/recent-breakout-candidates.md`.
- Fixed transformation-romance scene 7 screenplay/scene synchronization so the reciprocal-memory exchange uses the intended line `I choose you, not the gratitude.` and a coherent shared-memory object action; regenerated both production packages. Both retain transformation integrity 1.0, no visual-causality warnings, and no dialogue warnings. Tests: 120 passed.

## 2026-11-27 fresh creature breakout evidence checkpoint

- Downloaded and analyzed two priority creature breakouts: WUFO `F-RnV2OicIU` (24:32, about 848k views) and Movie Maxx `EUaUwhMAUgE` (28:18, about 754k views, about 1.9k subscribers at collection).
- Major packaging discovery: exact subtitle anchors and shifted frame comparison indicate the larger WUFO hit `9N6S6D_ioA0` appears to reuse most/all of `F-RnV2OicIU` after roughly 22:15 of preceding material. It should be treated as compound/serial packaging evidence, not clean duration causality.
- Craft findings: WUFO strongly validates heat-scarcity economics, creature care before power, sparse practical dialogue, authoritarian coal control, execution ritual, and climax-as-protection/contact. Movie Maxx validates visual-archetypal creature fantasy and slower atmospheric shot lengths; no subtitle track was available, so no exact dialogue claims were made.
- Committed report: `knowledge/market/fresh-creature-breakouts-wufo-moviemaxx-deep-dive.md`; evidence folders include full timelines/metrics/contact sheets and the WUFO overlap montage.

## 2026-11-27 compound-expansion production integration checkpoint

- Converted the WUFO serial-reuse discovery into production machinery: `compound_expansion.py` evaluates whether a creature film is ethically/materially complete enough to be reused inside a longer prequel/continuation package; it explicitly refuses to treat compound runtime as duration causality.
- Added `creature_pacing.py`: creature fantasy is allowed slower atmospheric composition, but must move care/material stakes -> staged spectacle -> quiet contact/recognition/home resolution instead of uniformly fast cutting.
- Integrated both evaluators into `evaluate_project`; generated creature-economic and compressed-survival premises now carry concrete `packaging.compound_expansion` reuse/prequel/tail rules.
- Updated format strategy with explicit `compound_serial_expansion` guidance. Tests: 124 passed.

## 2026-11-27 QueenFlix hidden-identity evidence checkpoint

- Downloaded/analyzed QueenFlix `G97N92SR1qQ` (79:28 vertical mobile-native hidden-identity romantic comedy, about 398k views at collection, roughly 2.5k subscribers).
- Major doctrine: hidden identity works as dramatic irony plus ethics; reveal is midpoint, restitution must become procedural consent-based repair, and final love proof uses both partners' real competencies in a public rescue.
- Format correction: vertical dialogue-rich romance can sustain long composed shots with very dense subtitles/dialogue; this is not the same pacing machine as sparse creature fantasy.
- Committed report: `knowledge/market/queenflix-hidden-identity-romcom-deep-dive.md` with timestamped evidence and sound/pacing table.
- PR #4 review findings were fixed/triaged; tests reached 127 passed before the QueenFlix documentation/evidence commit.

## 2026-11-27 pre-rotation integration note

- QueenFlix doctrine partially integrated into `hidden_identity_integrity.py` as `queenflix_accountability` checks: intelligent evidence-driven deceived party, post-reveal spatial boundary, procedural full disclosure, consent-based help rules, inconvenient repeat compliance, truthful re-choice. Tests: 128 passed.
- Next high-priority work: deepen these checks from advisory output into scored gates without weakening Lioren baseline; continue priority queue with `U_Tecg95FWA` or `Z50wCIqEa2k`; monitor/triage PR #4 review if new findings arrive.

## 2026-11-27 Twistora online-deception evidence checkpoint

- Downloaded/analyzed Twistora `Z50wCIqEa2k` (57:32 vertical campus romance, about 356k views at collection, roughly 12.3k subscribers).
- Major doctrine: do not copy the minor surface hook; extract online identity error -> immediate safeguarding -> adult accountability -> consent-aware adult romance -> social-anxiety accommodation -> real-self closure.
- Added `romance_deception_integrity.py` and integrated it into `evaluate_project`: checks immediate boundary, exploitation audit, adult accountability, consent-aware escalation, public-pressure removal, coercion repair, anxiety accommodation, real-self closure.
- Committed report: `knowledge/market/twistora-online-deception-romance-deep-dive.md`; derived evidence in `evidence/research/rediscovery_analysis/Z50wCIqEa2k/`.

## 2026-11-27 ReelQuest very-long serial-loop checkpoint

- Downloaded/analyzed ReelQuest `U_Tecg95FWA` (2:17:04 horizontal zero-to-hero fantasy, about 278.5k views at collection, roughly 3.1k subscribers).
- Major doctrine: recurring prophetic trauma -> systemic class exclusion -> courage before power -> costly multi-bloodline progression -> institutional adaptation -> serial circular cliffhanger.
- Circular flashforward evidence: 00:08 vs 136:59 villain shot is near-identical; ending catches up to opening and stops mid-sentence because this is explicit series/compound packaging, not standalone closure evidence.
- Added `zero_to_hero_integrity.py` to production evaluation. Committed report `knowledge/market/reelquest-zero-to-hero-serial-loop-deep-dive.md` and evidence under `evidence/research/rediscovery_analysis/U_Tecg95FWA/`.
- Next priority queue candidates: `ylN26llRtmw` (40m sci-fi pregnancy/alpha alien), `oHKc_rXrxm8` (50m alien/Gladiator pregnancy), `Gx7nwqNr9YY` (100m werewolf surrogate). Compare serial/standalone closure carefully.
