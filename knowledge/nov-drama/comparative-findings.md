# Nov Drama comparative findings — working evidence base

Updated: 2026-11-26. Evidence tiers follow the repository README: public outcomes are discovery signals, not CTR or retention causality. Casebook metrics are exploratory and use low-resolution audiovisual proxies plus aligned auto-subtitles. Contact sheets and full media remain local copyrighted evidence; this document records timestamps and short orientation quotes rather than redistributing footage.

## Corpus status

- 48 public Nov Drama videos are indexed in `data/raw/novdrama_archive.jsonl`.
- Age-adjusted leaderboard uses exact/scraped public views and publish dates where available.
- End-to-end media casebooks are being built in `data/processed/casebooks/`; cohort aggregation is in `data/processed/casebook_cohort_comparison.md`.
- Comment evidence is aggregated in `data/processed/novdrama_comment_signals.json`.

## Strongest archive-level observations

1. `family_child` was the clearest positive title-level signal in the first 48-video comparison (+1.50 mean log views/day; exploratory permutation p≈0.013). This is not causal proof.
2. `dragon`, hidden/secret identity, and setup-then-reversal were directionally positive but unstable.
3. Revenge/retribution was directionally negative at archive level, but this hypothesis is too simple: high-performing `vYNuKn6GiaE` receives audience praise for revenge being resolved early rather than delayed.
4. Thumbnail brightness rank-correlated positively with outcome (~0.40), while dark/red generic couple imagery clustered lower. Packaging cannot be separated from story quality without CTR/impression data.
5. Modern billionaire/power stories are not inherently doomed: `gkRXl9lDReY` is a major hit. The risk appears when modern power lacks the channel's vulnerable child/heir/protector emotional anchor.

## Timestamped audiovisual contrasts

### Successful or promising openings

| video | cohort/status | observed opening evidence | working interpretation |
|---|---|---|---|
| `ULJ7-z1zm6M` | top-tier hit | 0:00 crying orphan clutching bunny; 1:20 extreme dragon-eye close-up; 1:40–2:20 public rejection (“Who would want you?” mechanism); 2:40 boy invites her to come with them; 3:00 adoption/belonging choice; 3:20 castle spectacle; 4:40 warm welcome; 6:20 new noble/dragon-family tension | Extremely fast wound → kindness → spectacle → belonging → new tension loop. Faces and emotional legibility dominate vertical framing. |
| `0ofXaXWcfi0` | outperforming | 0:00 cliff/sea setting; 0:20 boy underwater; 1:00 luminous mermaid asks for help; 1:40–2:20 violent family persecution; 3:20–3:40 mermaid/boy mutual concern; 5:00 sea-god threat; 6:00 “come home with us” protective line | Mythic hook and emotional rescue arrive together. Lore is embodied in a character in danger rather than explained as politics. |
| `gkRXl9lDReY` | proven modern hit | 0:00 direct confession: husband cheated when she was seven months pregnant; 1:00–2:20 rejection, financial abandonment, forced move; 3:40 government/housing deadline pressure; 4:40 grandfather heart attack; 5:00 wealthy male protector enters social frame | No mythology, but the injustice is instantly legible and the child/pregnancy stake creates vulnerability. This disproves “modern arena fails” as a rule. |
| `j3U5JsLvbLg` | very strong but only 3 days old | 0:00 royal/ocean conflict already underway; 1:20 “Let me go”; 2:00 heroine thrown into sea; 2:40 sea monster; 4:40 supernatural merman/sea entity; 6:00 rescue/protection image | High lore count is not fatal when lore is visual action, creature spectacle, romance, and immediate peril. Recency makes views/day unstable. |

### Weak or failed openings

| video | cohort/status | observed opening evidence | working interpretation |
|---|---|---|---|
| `NnPZaWSGYuc` | failure case | 0:00–2:00 corpse pit/mother’s bones, coercion into slavery, clan genocide; 2:00–4:00 killing escort plus sexualized bond/soul-mark imagery; 4:00–8:00 trial/humiliation/Elder Council/pureblood politics; 8:00–10:00 War King protection expressed through violent spectacle | Visually rich, not cheap-looking. The problem is density: dark, coercive, proper-noun-heavy, and emotionally unrelenting before a safe relational anchor is established. |
| `1UB6EA3L7I4` | underperforming | 0:00 healer/magic exposition; 0:20 sealed scroll; 1:00 pregnancy revelation; 2:40–4:40 husband/infidelity/domestic confrontation; 5:40–6:20 bloodied victim and ritual imagery | Betrayal is immediate, but relationships and lore are confusing; the tone is claustrophobic adult misery before agency or protection. |
| `BeX5LHLqOEI` | underperforming despite animal-child appeal | 0:00 bunny-eared woman; 0:20 “urgent report”/sacred relic theft; 1:00 panther-clan accusation; 1:40 public sentencing imagery; 2:20–3:20 explanatory caretaker/selection material; 4:00 arranged selection; 5:40 guardian/veil ceremony | Cute creature/family ingredients exist, but the first minutes lead with report/court/selection machinery rather than a simple wound-rescue loop. This is a key counterexample to “animal child is enough.” |
| `KsxgWoFS50I` | underperforming | 0:00 “Ten years ago” time-shift; 0:20 cat-girl identity; 0:40 pirate/adoptive backstory; 1:40–2:20 mouse transformation/care vow; 4:00–6:20 adult intimacy/bedroom/censored-body imagery | Warm adoption exists in backstory, but the opening is temporally nested and adult/sexualized before a clear present-tense dramatic question. Length alone does not explain failure. |

## Endings: payoff is necessary but not sufficient

- `ULJ7-z1zm6M` ends around 78:40–79:20 with family waiting, a birthday celebration, and gratitude for a home — direct emotional answer to the orphan wound.
- `0ofXaXWcfi0` ends around 80:00–82:40 with public justice, romantic embrace, wedding/celebration, and communal applause.
- `gkRXl9lDReY` ends around 66:40–67:20 with gray-haired family continuity and a joyful child in ceremonial white — family legitimacy rather than only wealth.
- Counterevidence: `BeX5LHLqOEI` ends around 56:20–59:00 with mother/children/family restoration and pure-blood panther cubs, yet underperformed.
- Counterevidence: `KsxgWoFS50I` ends around 116:00–118:20 with creature spectacle, romantic coronation/union, and golden payoff imagery, yet underperformed.
- Therefore “add a warm ending” is not a sufficient fix. Opening clarity, middle momentum, audience trust, packaging, and artifact quality still determine whether viewers stay long enough to receive the payoff.

## Quantitative casebook patterns so far

Current small-sample cohort means (`data/processed/casebook_cohort_comparison.md`) show:

- Underperforming videos have much higher lore/mythology language per hour and lore-to-care ratio than outperformers.
- Underperformers also have higher threat/violence language per hour and threat-to-care ratio.
- Raw care/belonging word counts do **not** separate hits cleanly: failures can contain many apologies, family words, or end-state reconciliation. Quality, timing, and causal emotional meaning matter more than keyword volume.
- `gkRXl9lDReY` has very low mythology density and high success; `bI0uHNOVewI` also has low mythology density but only middle performance. Low lore is not sufficient either.
- `j3U5JsLvbLg` has high lore/threat language but strong performance so far. The difference appears to be that lore is embodied as visual sea-creature action/romance rather than abstract court procedure. This hypothesis needs more falsification.

## Comment-evidence production lessons

Across public comments, even when viewers like a story they complain about:

- censorship/blurring/pixelation breaking immersion;
- music being too loud under dialogue;
- sound dropping out in parts;
- sudden cuts or near-zero glitches;
- on-screen “reup protection”/watermark-like distraction;
- logic holes such as poison evidence not being acted on.

Positive comments reward complete stories, well-defined characters, happy endings, differentiated good characters, and fast satisfying justice. `ULJ7-z1zm6M` viewers specifically praise a non-evil stepsister and the absence of unnecessary sister drama; differentiation from trope fatigue can itself be a retention asset.

## Hypothesis ledger

| hypothesis | current status | evidence/counterevidence |
|---|---|---|
| Child/heir/creature anchors increase demand | Supported but insufficient | Strong metadata and hit pattern; contradicted by `BeX` animal-child failure. |
| Revenge causes failure | Rejected as simplistic | `vYNu` comments praise early revenge; archive negativity may reflect delayed/unsatisfying revenge or cold emotional engine. |
| Modern arena causes failure | Rejected as simplistic | `gkR` disproves; lack of child/family emotional anchor is the narrower risk. |
| Dense lore politics before emotional grounding is harmful | Supported, needs more testing | `1UB`, `_I5`, `BeX` high lore ratios; `j3` counterexample suggests embodied spectacle-lore is different from abstract politics-lore. |
| Early protective warmth matters | Supported | `ULJ`, `0ofX`, `j3`; failures either delay warmth or make the protector coercive/ambiguous. |
| Warm ending explains success | Rejected as sufficient cause | `BeX` and `Ksxg` have warm payoff imagery but fail. |
| Production artifacts suppress performance | Plausible but unproven causally | Repeated comments, but no CTR/retention access. Treat as quality gate regardless. |
| Packaging explains outcome gaps | Plausible, untested causally | Thumbnail cohort differences visible; cannot isolate CTR without impressions. |
| Publish recency drives misleading views/day | Supported methodologically | `j3` is only 3 days old at snapshot and may regress; use age bands and revisit snapshots. |

## Production rules derived so far

1. In the first 60 seconds, establish one vulnerable person/creature, one legible injustice, and one reason to hope.
2. Do not open with council/report/ceremony exposition unless it is interrupted by irreversible action.
3. Lore must be embodied in a character, creature, object, or visible cost. Abstract clan/politics terminology must be delayed or compressed.
4. A powerful protector is not automatically emotional warmth. If the protector is coercive, ambiguous, or sexualized before trust, the audience may not feel safe.
5. Every humiliation must convert into alliance, clue, capability, decision, or escalation. Otherwise compress it.
6. Justice should arrive in stages, not only at the end. Audience comments reward early satisfying consequences.
7. Ending payoff must answer the original wound: home, family legitimacy, chosen love, safety for child/heir, public acceptance. But a warm ending cannot compensate for a confusing opening or exhausting middle.
8. Treat audio/dialogue clarity, continuity, censorship artifacts, and watermark distractions as release-blocking quality gates.
9. Titles/thumbnails should make a single impossible emotional promise readable in one glance; do not sell generic attractive couples.
10. Every concept must list counterexamples before greenlight. If a rule has a hit counterexample, narrow the rule instead of ignoring it.
