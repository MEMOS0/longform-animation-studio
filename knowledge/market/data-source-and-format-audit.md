# External data-source and format audit

Updated: 2026-11-26. Purpose: prevent category errors when comparing AI-drama channels. A Korean episodic microdrama, a landscape creature fantasy film, a compilation season, and a disaster one-off are different products even when all are labeled “AI movie.”

## Source status

| source | status | what it contributes | limitation |
|---|---|---|---|
| OpenMicroDrama `/ai-dramas` | accessible | English/global top-50 public ranking, strong long-form sample | opaque methodology; view snapshots age quickly |
| Crateh | accessible | large Korean AI-film catalog and genre/format distribution; useful episodic-ecosystem contrast | Korean-language market bias; initial HTML exposes only a sample of full catalog |
| MetaMovies `/ai-movies/` | blocked | none yet | returned verification/interstitial page rather than catalog data |
| Epic AI Films official site | accessible | first-party curated feature catalog, view/date snapshots, franchise/world strategy | self-reported and not complete YouTube archive |
| Hollywood.ai Future Frame page | accessible | preserves 13-title partial catalog after channel termination | view counts and full media unavailable |
| Future Frame YouTube channel | unavailable | none direct | YouTube says the account was terminated; Piped endpoints also fail |

## Crateh ecosystem snapshot

The Crateh landing page reports **1,052 works** and exposes the following category distribution:

- formats: **814 series**, **187 short films**, **6 feature films**, **33 trailers**;
- genres/tags: **788 drama**, **296 romance**, **287 fantasy**, **211 action**, **185 historical/martial arts**, **104 SF**, **96 comedy**;
- rankings include today/7-day/30-day/90-day/year/all-time view windows;
- visible ranking examples are heavily episodic, often 1–10 minutes per episode, with some longer 25+ minute episodes;
- visible successful channels/examples include Drama AI Channel, Yong Director Theater, Onkyul Studio, YOUNG FILMS, First Love Smoke, and AI Drama Scene-Naru AI Studio.

This is structurally different from Nov Drama/Ironcrest/Epic:

| axis | Korean Crateh ecosystem | Nov/Ironcrest/Epic landscape ecosystem |
|---|---|---|
| dominant unit | short/mid-length episode | standalone feature or season compilation |
| retention problem | next-episode click and serial cliffhanger | first-hour retention and complete-film payoff |
| release loop | high-frequency season publishing | slower cinematic drops |
| packaging | episode number + serialized ship/court/revenge hook | protagonist-centered high-concept film title |
| emotional mode | romance fantasy, regression, revenge, BL, royal court, historical action | family melodrama, creature protection, mythic adventure, disaster/sci-fi |
| key risk | fragmentation and weak standalone payoff | slow opening and failure to pay film-scale promise |

## Critical format correction

Do **not** compare a 90-second episode ranking directly against a 100-minute film. For every analysis, first classify:

1. vertical/mobile microdrama episode;
2. horizontal episodic drama;
3. complete season compilation;
4. 15–30 minute short feature;
5. 30–60 minute feature;
6. 60–120 minute feature;
7. 120+ minute compilation;
8. trailer/teaser;
9. off-format meta/documentary.

Only then compare titles, thumbnails, opening structure, retention mechanisms, and emotional engines inside the same format class.

## Breakout-discovery protocol

Crateh’s rolling windows are useful for finding recent low-subscriber breakouts because they reduce dependence on all-time view counts. Required fields before trusting a breakout claim:

- video/channel ID;
- first publish date;
- exact collection date;
- subscribers at collection;
- views and views/day;
- duration and format class;
- episode number/season position;
- language/market;
- whether traffic is a one-off hit or repeated across multiple uploads.

A video with high views in a “today” or “7-day” ranking is a candidate, not proof of a breakout. Confirm channel age and whether the channel has multiple independent performing works.

## Production implications

- If building a serial format, study Crateh-style episode mechanics separately; cliffhanger density and next-episode identity are first-order.
- If building a cinematic long-form film, use Epic/Ironcrest/Nov-style feature mechanics; do not import microdrama rapid-fire exposition blindly.
- If compiling episodes into a season, treat the compilation as a different product with its own thumbnail/title promise and completion value.
- External catalogs are discovery maps, not ground truth. Every important candidate still needs direct media inspection.
