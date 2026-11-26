# Nov Drama comparative findings — working evidence base

Updated: 2026-11-26. Evidence tiers follow the repository README: public outcomes are discovery signals, not CTR or retention causality. Casebook metrics are exploratory and use low-resolution audiovisual proxies plus aligned auto-subtitles. Contact sheets and full media remain local copyrighted evidence; this document records timestamps and short orientation quotes rather than redistributing footage.

## Corpus status

- 48 public Nov Drama videos are indexed in `data/raw/novdrama_archive.jsonl`.
- Age-adjusted leaderboard uses exact/scraped public views and publish dates where available.
- End-to-end media casebooks are generated in `data/processed/casebooks/`; cohort aggregation is committed in `data/processed/casebook_cohort_comparison.md`. To keep pull requests reviewable, only representative hit/failure sample casebooks are committed; the full set is reproducible with `tools/build_casebooks.py`.
- Comment evidence is aggregated in `data/processed/novdrama_comment_signals.json`.

## Strongest archive-level observations

1. `family_child` was the clearest positive title-level signal in the first 48-video comparison (+1.50 mean log views/day; exploratory permutation p≈0.013). This is not causal proof.
2. `dragon`, hidden/secret identity, and setup-then-reversal were directionally positive but unstable.
3. Revenge/retribution was directionally negative at archive level, but this hypothesis is too simple: high-performing `vYNuKn6GiaE` receives audience praise for revenge being resolved early rather than delayed.
4. Thumbnail brightness rank-correlated positively with outcome (~0.40), while dark/red generic couple imagery clustered lower. Packaging cannot be separated from story quality without CTR/impression data.
5. Modern billionaire/power stories are not inherently doomed: `gkRXl9lDReY`, `l5ICXoEffPs` (mafia boss + daughter), and `OJ5ylArJ03s` (intern + twins) all outperform. The risk appears when modern power lacks the channel's vulnerable child/heir/protector emotional anchor.

## Archive-wide repaired casebook synthesis (46 scored videos)

After repairing per-window silence/rms estimates, the archive-wide lexical/audiovisual comparison shows a consistent directional pattern, still observational rather than causal:

| metric | outperforming | middle | underperforming | interpretation |
|---|---:|---:|---:|---|
| lore/hour | 71.13 | 128.83 | 141.45 | Hits can use fantasy, but weak videos carry roughly twice the explicit lore density. |
| threat/hour | 72.93 | 102.64 | 120.70 | Weak videos are more relentlessly threatening/violent. |
| care/hour | 95.09 | 106.82 | 93.02 | Care frequency alone does not explain success. |
| lore/care ratio | 0.83 | 1.63 | 1.69 | Strongest simple ratio: hits keep explicit lore below care; failures let lore dominate care. |
| threat/care ratio | 0.85 | 1.25 | 1.48 | Hits leave more emotional breathing room relative to threat. |
| final-10 wound count | 7.91 | 11.26 | 13.75 | Weak endings remain more wounded/procedural even when they include warm imagery. |
| final-10 care count | 18.45 | 17.96 | 19.33 | Warm-ending counts are nearly flat across cohorts; warmth at the end is not sufficient. |

Opening timing adds an important correction: explicit lore language begins around 261s in outperformers versus 107s in middle videos and 83s in underperformers. Explicit first wound/care words are not earlier in hits on average, so those lexical counts must not be treated as emotional-proof; visual grounding and immediate comprehensibility matter more than literal words like “love” or “protect.” The robust opening pattern is delayed abstract lore plus early embodied stakes/consequences.

Subtitle sentence-shape analysis adds a more specific mechanism: underperforming openings use ~598 words in the first five minutes versus ~459 in outperforming videos; explicit exposition markers are ~6.45/1000 versus ~1.78/1000; pressure language is ~16.04/1000 versus ~11.75/1000. Hits do not necessarily use shorter sentences; they simply explain less and leave more room for images/action. Their openings also have a slightly higher question ratio (~0.22 versus ~0.17), consistent with dramatic-question-driven narration. These are lexical proxies, not acting/subtext measurements.

Opening density evidence strengthens this: underperforming videos average about 835 subtitle words in the first five minutes versus 648 in outperforming videos, while shot-boundary counts and motion are nearly identical (~11 shots, ~0.15 motion). The difference is therefore not simply “faster editing”; weak openings tend to explain more. Middle videos also have higher ending silence (~0.236 versus ~0.193–0.196), but this is not yet interpretable because music, narration style, and missing-audio artifacts confound silence.

Important counterexample discipline: `v03oauoFveU` and `vYNuKn6GiaE` have substantial lore yet outperform because the lore is embodied early in visible children/creatures/consequences; `lcOFpT0B5Uc` also carries high lore but includes a werewolf-king-heir child-protection promise. Therefore the rule is not “less fantasy,” but “less abstract/procedural lore before emotional grounding.”

## Timestamped audiovisual contrasts

### Successful or promising openings

| video | cohort/status | observed opening evidence | working interpretation |
|---|---|---|---|
| `ULJ7-z1zm6M` | top-tier hit | 0:00 crying orphan clutching bunny; 1:20 extreme dragon-eye close-up; 1:40–2:20 public rejection (“Who would want you?” mechanism); 2:40 boy invites her to come with them; 3:00 adoption/belonging choice; 3:20 castle spectacle; 4:40 warm welcome; 6:20 new noble/dragon-family tension | Extremely fast wound → kindness → spectacle → belonging → new tension loop. Faces and emotional legibility dominate vertical framing. |
| `0ofXaXWcfi0` | outperforming | 0:00 cliff/sea setting; 0:20 boy underwater; 1:00 luminous mermaid asks for help; 1:40–2:20 violent family persecution; 3:20–3:40 mermaid/boy mutual concern; 5:00 sea-god threat; 6:00 “come home with us” protective line | Mythic hook and emotional rescue arrive together. Lore is embodied in a character in danger rather than explained as politics. |
| `gkRXl9lDReY` | proven modern hit | 0:00 direct confession: husband cheated when she was seven months pregnant; 1:00–2:20 rejection, financial abandonment, forced move; 3:40 government/housing deadline pressure; 4:40 grandfather heart attack; 5:00 wealthy male protector enters social frame | No mythology, but the injustice is instantly legible and the child/pregnancy stake creates vulnerability. This disproves “modern arena fails” as a rule. |
| `j3U5JsLvbLg` | very strong but only 3 days old | 0:00 royal/ocean conflict already underway; 1:20 “Let me go”; 2:00 heroine thrown into sea; 2:40 sea monster; 4:40 supernatural merman/sea entity; 6:00 rescue/protection image | High lore count is not fatal when lore is visual action, creature spectacle, romance, and immediate peril. Recency makes views/day unstable. |
| `vYNuKn6GiaE` | archive-leading hit | 0:00 desolate “human girl” aftermath; 0:40 transformation/underwater imagery; 1:20 dragon hatching; 1:40 dirt-streaked heroine; 2:00 cute baby dragon; 3:00 glowing chest/power awakening; 4:00–5:40 public recognition/grief; 7:20 hand-held fire magic; 8:20 dragon projection over castle; 10:00 portal/red-dragon attack; 11:20 child/dragon-baby promise visibly paid; 11:40–13:00 enemy kneeling/tears | This is the key revenge counterexample. Revenge is not delayed to the finale: consequences begin within roughly the first 10–13 minutes. Mythology is concrete (egg, baby dragons, children, flame, portals) rather than parliamentary exposition. |
| `v03oauoFveU` | archive-leading hit | 0:00 snowy dragon kingdom/egg; 0:20 dragon king with egg; 0:40 eye close-up; 1:20 cute child with creature; 1:40 crowd shock; 3:20 mother reassurance; 4:20 black dragon spectacle; 4:40 child nursing creature; 5:40 bruised crying child; 6:00 small comfort gesture | Interleaves royal/dragon mystery with child vulnerability and care almost immediately. Hidden identity is embodied in the child/creature relationship before any abstract political explanation. |

### Weak or failed openings

| video | cohort/status | observed opening evidence | working interpretation |
|---|---|---|---|
| `NnPZaWSGYuc` | failure case | 0:00–2:00 corpse pit/mother’s bones, coercion into slavery, clan genocide; 2:00–4:00 killing escort plus sexualized bond/soul-mark imagery; 4:00–8:00 trial/humiliation/Elder Council/pureblood politics; 8:00–10:00 War King protection expressed through violent spectacle | Visually rich, not cheap-looking. The problem is density: dark, coercive, proper-noun-heavy, and emotionally unrelenting before a safe relational anchor is established. |
| `1UB6EA3L7I4` | underperforming | 0:00 healer/magic exposition; 0:20 sealed scroll; 1:00 pregnancy revelation; 2:40–4:40 husband/infidelity/domestic confrontation; 5:40–6:20 bloodied victim and ritual imagery | Betrayal is immediate, but relationships and lore are confusing; the tone is claustrophobic adult misery before agency or protection. |
| `BeX5LHLqOEI` | underperforming despite animal-child appeal | 0:00 bunny-eared woman; 0:20 “urgent report”/sacred relic theft; 1:00 panther-clan accusation; 1:40 public sentencing imagery; 2:20–3:20 explanatory caretaker/selection material; 4:00 arranged selection; 5:40 guardian/veil ceremony | Cute creature/family ingredients exist, but the first minutes lead with report/court/selection machinery rather than a simple wound-rescue loop. This is a key counterexample to “animal child is enough.” |
| `KsxgWoFS50I` | underperforming | 0:00 “Ten years ago” time-shift; 0:20 cat-girl identity; 0:40 pirate/adoptive backstory; 1:40–2:20 mouse transformation/care vow; 4:00–6:20 adult intimacy/bedroom/censored-body imagery | Warm adoption exists in backstory, but the opening is temporally nested and adult/sexualized before a clear present-tense dramatic question. Length alone does not explain failure. |
| `rtTbEcFdnZQ` | underperforming | 0:00 crowded ceremony; 0:20 exact day of selection ceremony; 1:20 “pathetic” insult close-up; 1:40/3:00/4:00/5:20 visibly censored cleavage on sexualized villain; 3:20 wand/rite imagery; 4:20 public accusation; 5:00 king rejects/humiliates; 6:00 poverty sentence | Court spectacle is visually polished, but the first minutes are adult sexualized ceremony/politics plus repeated censorship artifacts. There is no child/creature/protective anchor comparable to the hits. |

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


## Direct visual audit notes from representative hits/failures

These notes come from inspecting generated full-runtime contact sheets plus aligned dialogue/timelines. They are still sampled visual inspection, not frame-by-frame human annotation; contact sheets are local copyrighted evidence and are not committed.

### `ULJ7-z1zm6M` — hit: orphan-to-belonging engine

- **00:00–01:20:** The film opens on a small orphan girl physically clutching a stuffed animal while adults discuss whether anyone wants her. At **01:20** a close-up golden/nonhuman eye introduces the fantasy promise. The opening combines child vulnerability, social rejection, and visible magic before explaining politics.
- **02:00–03:00:** Other children/adults verbally reinforce that a family did not adopt her; a boy/protector figure challenges the rejection. At **03:20** a wide castle/world image briefly expands scale after the emotional attachment is already established.
- **04:00–06:20:** The girl is physically held/carried and relational care is visible; a woman says there is something she needs to tell her, then royal/adult power enters. The lore is layered onto an already legible child-protection relationship.
- **40:00–43:40:** A child is carried through a moonlit landscape and introduced into a dragon-family/social space. A woman asks “You adopted a human child?”; warmth and social prejudice coexist. The middle escalates belonging rather than merely repeating abuse.
- **73:20–76:20:** Court/adult judgment returns, but the child’s perspective remains central. At **76:20** the child explicitly notes that a rich dragon family is doting on the protagonist.
- **77:40–79:20:** A magical/creature image appears inside a bright domestic/garden space, followed by a birthday celebration. The final line at **79:20** thanks the protagonist for giving the child a home. The payoff is belonging/home/family acceptance, not simply punishment.
- **Production lesson:** this hit does not avoid fantasy royalty; it makes royalty serve an orphan-care emotional engine. Its high care/hour (~151) and low threat/hour (~31) match what the images show.

### `gkRXl9lDReY` — hit: modern arena with instantly legible child stakes

- **00:00–01:20:** A visibly pregnant woman is escorted/confronted in a modern corporate environment. Dialogue establishes cheating/betrayal and pregnancy almost immediately. No mythology or world rules are needed.
- **01:40–03:40:** The husband/rival power structure is clear; the wife is isolated, visibly pregnant, and financially/socially threatened. A small child/heir image appears by **03:40**, reinforcing that the conflict is about lineage and protection, not only adult romance.
- **04:00–06:20:** Hospital/elder illness and public confrontation add irreversible costs. The protagonist’s distress is photographed in direct face closeups, and antagonist pressure produces immediate plot consequences.
- **66:40–67:20:** Final imagery centers a family/child in a church/ceremonial aisle. The child/heir payoff is literal and visual.
- **Production lesson:** modern billionaire/inheritance material can outperform when the first minute supplies a concrete vulnerable body (pregnancy), an unjust betrayal, and child/heir stakes. The archive-level “modern power” failure pattern must therefore remain conditional, not absolute.

### `a2pydTch_Tg` — failure: child vulnerability converted into relentless suffering spectacle

- **00:00–01:40:** The opening moves quickly from a romantic garden/picnic image to red-eyed vampire threat and blood/violence language. Child vulnerability appears early, but the dominant emotional register is menace rather than safety.
- **02:00–05:00:** The vampire/power figure dominates the frame while a child is shown ill/injured and socially powerless. Several frames center threat, infection, punishment, or coercive authority; protective warmth is weak or ambiguous.
- **28:00–33:00:** The middle contains extreme child-endangerment imagery: armed guards, monstrous werewolf transformation, blood on the child, and the child crying/being physically threatened. This is not a single painful turn; it is a sustained misery/violence escalation.
- **53:20–56:20:** The ending does contain warm domestic images (food, comfort, embrace), but they arrive after prolonged graphic suffering and cannot retroactively make the middle safe or emotionally balanced.
- **Production lesson:** child presence is not automatically a positive signal. Child vulnerability must be coupled with credible protection, agency, progression, and relief. If the child is mainly a body to be harmed, the same “child” surface feature becomes a retention risk.

### `Ze0hWktEfRI` — middle outcome: care exists but the opening lacks child/heir specificity

- **00:00–02:40:** The opening is a modern hospital/business-family conversation. Adults discuss a grandmother, absence, rain, and relationship tension. There is emotional conflict, but it begins as explanatory adult dialogue rather than a visually endangered child/creature.
- **03:00–06:20:** A couple argues around hospital/family pressure; a romantic rival triangle becomes clear. Faces are legible and production is competent, but the stakes remain adult relational jealousy for longer than the strongest modern hit (`gkRXl9lDReY`).
- **Production lesson:** high care frequency alone is insufficient. Care must attach to a sharply vulnerable/protective object early; otherwise it becomes diffuse melodrama. This helps explain why `Ze0hWktEfRI` is middle rather than top despite high measured care language.

### `xJUN_KOCnME` — failure: spectacle-first arena mismatch

- **00:00–01:00:** The opening is racing spectacle: track, shaking car, garage/crew, adult champion pressure. It is visually competent but does not establish the channel’s core child/heir/protective fantasy contract.
- **01:20–04:40:** Adult male racing/business conflict dominates. Dialogue concerns championship, deals, skills, and driving level. Even when competence reversal is possible, the emotional anchor remains adult competition.
- **05:40–06:20:** A child finally appears and recognizes/approaches the protagonist, but this vulnerable relational hook arrives after several minutes of arena spectacle.
- **Production lesson:** spectacle does not substitute for emotional grounding. A child/heir element arriving late cannot fully repair an opening that first trains the audience to expect sports-business drama rather than family/protection melodrama.

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
6. Justice should arrive in stages, not only at the end. Audience comments reward early satisfying consequences; `vYNuKn6GiaE` begins visible consequences within roughly the first 10–13 minutes.
7. Ending payoff must answer the original wound: home, family legitimacy, chosen love, safety for child/heir, public acceptance. But a warm ending cannot compensate for a confusing opening or exhausting middle.
8. Treat audio/dialogue clarity, continuity, censorship artifacts, and watermark distractions as release-blocking quality gates.
9. Titles/thumbnails should make a single impossible emotional promise readable in one glance; do not sell generic attractive couples.
10. Pay the core title promise visually within the first 10–15 minutes, then escalate it. `vYNuKn6GiaE` shows dragon-baby/child imagery and public consequences early rather than saving everything for the finale.
11. Every concept must list counterexamples before greenlight. If a rule has a hit counterexample, narrow the rule instead of ignoring it.
