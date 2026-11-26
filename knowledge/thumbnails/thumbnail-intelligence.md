# Thumbnail Intelligence — evidence base and operating system

Updated: 2026-11-26. This system treats thumbnails as packaging evidence, not proven CTR causality. Public views are affected by impressions, topic demand, title, audience, channel trust, and recommendation traffic. Without impressions/CTR/retention, visual analysis can identify design mechanisms but cannot prove that a thumbnail caused performance.

## Reference archive

Persistent reference images are stored under `thumbnails/reference/<channel>/` and indexed in:

- `thumbnails/novdrama_index.jsonl` — 48 Nov Drama thumbnails, linked to archive metadata and measured visual metrics
- `thumbnails/openmicrodrama_top20_index.jsonl` — top cross-channel market sample with channel/title/rank metadata
- `thumbnails/novdrama_top_bottom_montage.jpg` — same-channel high/low age-adjusted comparison montage
- `thumbnails/openmicrodrama_top20_montage.jpg` — cross-channel market packaging montage
- `thumbnails/novdrama_metric_cohorts.json` — aggregate visual metrics by age-adjusted cohort

The archive is for mechanism learning, not copying. Reference images remain copyrighted by their owners; use them internally for comparative research and generate original artwork for production.

## Professional source base

1. YouTube Help, “Thumbnail & title tips” — thumbnails and titles work together; use readable fonts, avoid excessive complexity, account for device differences, keep important title words early, and evaluate CTR by surface/audience rather than as one universal number. YouTube also states that 90% of best-performing videos have custom thumbnails.
2. YouTube Help, “A/B test titles & thumbnails” — creators can compare up to three title/thumbnail combinations; the winning combination is selected by watch time, not clicks alone. This is crucial: clickbait that damages watch time is not a successful package.
3. Decision Support Systems (2022), “An exploration of the relation between the visual attributes of thumbnails and the view-through of videos” — branded-video study framing thumbnails as both informative and visually appealing; object/element complexity are central information cues, while colorfulness/brightness/image quality operate as peripheral cues. It is not fantasy-drama-specific, so use as a design prior.
4. “The Effect of Design Elements in YouTube Thumbnails” (2024) — quantitative content analysis reporting stronger engagement for human-focused thumbnails, medium framing, natural colors, and content-centered text. Treat as correlational and market/context-dependent.
5. YouTube Creator Insider thumbnail discussion with MrBeast’s thumbnail designer and YouTube algorithm staff — no magic “number of faces” rule; packaging should be judged by audience response, clarity, expectation-setting, and recognizable channel consistency.

## Nov Drama measured visual patterns

Cohort aggregation over 47 scored thumbnails:

| metric | outperforming | middle | underperforming | interpretation |
|---|---:|---:|---:|---|
| brightness | 0.397 | 0.350 | 0.300 | Strongest simple measured separation. Hits tend to be brighter/luminous; failures trend dark. |
| contrast | 0.272 | 0.273 | 0.268 | Nearly flat; raw contrast is not enough. |
| saturation | 0.497 | 0.538 | 0.523 | Hits are slightly less saturated; saturated red/dark intensity is not inherently better. |
| colorfulness | 0.235 | 0.224 | 0.242 | No meaningful monotonic separation. |
| edge density | 0.310 | 0.279 | 0.294 | Weak/ambiguous; do not overinterpret. |
| center salience proxy | 0.128 | 0.131 | 0.143 | Underperformers show slightly higher clutter/contrast concentration proxy, but the metric is experimental. |
| mobile contrast | 0.241 | 0.243 | 0.237 | Nearly flat at thumbnail-feed-size proxy. |

These are observational correlations. Brightness may encode genre/emotional promise rather than directly causing clicks.

## Direct visual comparison: Nov Drama top versus low performers

Evidence image: `thumbnails/novdrama_top_bottom_montage.jpg`.

### Patterns in the strongest examples

- `v03oauoFveU` / Dragon King’s Secret Daughter: luminous romantic couple close-up, gold/blue fantasy palette, dragon-wing/power imagery, clear central intimacy.
- `vYNuKn6GiaE` / Dragon babies and Dragon King: glamorous heroine centered with multiple glowing dragon eggs; the image visually pays the title’s core fantasy object.
- `ULJ7-z1zm6M` / abandoned orphan becomes dragon family favorite: warm family ensemble with child central; belonging is visible rather than merely stated.
- `jRa3_WZYDdY` / pet wolf king: intimate couple plus cute black wolf/pet bridge; romance and creature hook coexist.
- `gkRXl9lDReY` / pregnant wife to billionaire payoff: bright wedding/luxury romance, high-status clothing, relational clarity rather than revenge imagery.
- `u1RoW_083xM` / match girl crown: childlike vulnerability object (teddy) plus powerful men and crown/fantasy setting; vulnerability/protection are visible.
- `l5ICXoEffPs` / mafia queen/runaway bride: woman central and composed, romance/power triangle behind; despite dark clothing, face/status hierarchy are clear.

Common mechanisms:

1. luminous, high-key or jewel-toned separation;
2. one dominant emotional relationship rather than undifferentiated crowd;
3. child/creature/object of vulnerability visible when it is the story engine;
4. romance/protection framing more than abstract violence;
5. typography short, high-contrast, and secondary to faces/objects;
6. the thumbnail and title divide labor: title explains the reversal, thumbnail shows the desirable emotional/fantasy promise.

### Patterns in low performers

- `pkYxdUwG-pg` / Redline Rage: black/red adult racing revenge aggression; readable but mismatched with the channel’s child/protection melodrama contract.
- `bl02sfZAcuA` / Wolf King forbidden love: dark red multi-person sexualized triangle; hierarchy is emotionally colder and more cluttered.
- `1UB6EA3L7I4` / rejected mate wolf princess: many competing faces/figures and dark romantic tension; vulnerable/protective object less clear.
- `aj2gST2O5l` / Starlight turns against her: dark blue/red conflict imagery, more threat than warmth.
- `YKL3A2gFHbO` / Silent Guard: bright but adult bodyguard/love-triangle framing; less differentiated within the channel’s fantasy/family expectations.
- `ZhAYjMLvIqc` / Stolen Dragon Queen: dark monstrous coercion/damsel threat; protection appears coercive rather than safe.
- `UDjV1_6TqFs` / Forest Princess second mate: ornate but crowded multi-face hierarchy; focal emotion diffuses.
- `Prsthri0ktA` / They took his family: bloody revenge spectacle, dark/red violence, little belonging or protection promise.

These examples do **not** prove dark thumbnails fail. They suggest a packaging-fit pattern: Nov Drama’s audience appears more responsive to luminous vulnerability/protection/belonging than to cold revenge, coercive sexuality, crowded triangles, or arena spectacle. This is a channel/format-specific hypothesis.

## Cross-channel packaging taxonomy

Evidence image: `thumbnails/openmicrodrama_top20_montage.jpg`.

1. **Localized family melodrama:** Ai Kedo Met and AI DRAMA TV use realist domestic confrontation, local-language text, and clear victim/oppressor relationships. The fantasy-polish rules of Nov Drama do not transfer directly.
2. **Transformation/rebirth:** FablePop uses glamorous transformation, before/after visual contrast, clean high-key backgrounds, and explicit titles like “Reborn” or “I Became Beautiful.”
3. **Creature power bond:** Ironcrest’s baby-dragon image uses a vulnerable small creature plus huge protector/power presence; scale itself is the emotional mechanic.
4. **Romantic/family betrayal:** Dunvaris and Nov Drama use wedding/couple/family compositions, often bright and luxurious, where the relationship triangle is readable.
5. **Ensemble monster/franchise spectacle:** RIFTBORN uses grouped creature characters and a series brand; different from intimate melodrama packaging.
6. **Lone hero versus scale threat:** Starseed’s dragon/samurai thumbnail uses tiny human silhouette against huge creature; spectacle and scale are central.
7. **Science-fiction/horror threat:** Last Sumerian and Epic AI Films use darker world-threatening imagery, monster texture, and high-concept menace; these must not be judged by romantic melodrama rules.
8. **Child/family recognition:** Crown Her Drama uses child/parent warmth and playful handwriting-like text; belonging itself is the hook.

The same “bright thumbnail” heuristic does not apply uniformly. Genre contract matters: luminous intimacy fits melodrama; scale contrast fits creature adventure; darker texture may fit horror/sci-fi. What transfers is not brightness itself but immediate emotional/concept legibility.

## Thumbnail design protocol for future films

Before generating a thumbnail, answer:

1. What is the one emotion the viewer must feel before reading the title?
2. What is the one story question the image must create?
3. Which object/person/creature embodies the wound or promise?
4. Is the thumbnail showing the same promise the first 10 minutes actually pay?
5. Who is vulnerable, who has power, and who protects or threatens?
6. Can the image be understood at 160px wide?
7. Does text add information, or merely repeat the title?
8. Does the package match the channel/format genre contract?
9. Does the image accidentally promise sexual coercion, misery spectacle, or action spectacle when the film is really about belonging/protection?
10. What are three materially different alternatives worth A/B testing?

## Concept-generation integration

`studio/thumbnail_concepts.py` now provides:

- reference classification into visual mechanism categories;
- concept generation for creature-bond, transformation, relational-betrayal, and general emotional-drama premises;
- transparent concept critique with mobile-readability and CTR-caveat warnings.

This is a design-support heuristic, not a predictor. The correct validation path is YouTube Test & Compare where available, interpreted through watch time and audience-surface CTR rather than clicks alone.

## Immediate falsification tasks

- Build hit/middle/failure archives inside Ironcrest, FablePop, RIFTBORN, Future Frame, Epic AI Films, and The Next Show before generalizing beyond Nov Drama.
- Separate vertical mobile-native melodrama from landscape cinematic fantasy/sci-fi packaging.
- Compare thumbnail changes over time when detectable; a thumbnail may have been updated after a video became successful.
- Do not use stylized-art face detection as reliable evidence yet; the current Haar-based detector fails on these images and is intentionally not used as a conclusion.
