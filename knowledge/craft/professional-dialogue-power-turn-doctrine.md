# Professional Dialogue Power-Turn Doctrine

## Evidence base

Derived from the current deep-dive corpus: QueenFlix hidden-identity procedural repair, Velvet family-exit boundary dialogue, MythicTwist animal-guise consent naming, Twistora safeguarding/accountability dialogue, WUFO sparse creature melodrama, ReelQuest class-exclusion confrontation, and visual-first creature films where behavior must carry what dialogue does not explain.

This doctrine is for professional screenplay generation and revision. It is not a claim that every hit uses dense dialogue. Creature spectacle may be sparse; vertical melodrama may be dense. The shared professional rule is that dialogue must perform dramatic work when it appears.

## 1. A line is a move, not information

Every important line should do at least one of the following:

- demand: force a choice, payment, confession, permission, boundary, or surrender;
- refuse: block extraction, coercion, ownership, humiliation, or premature intimacy;
- offer: provide help with a visible price or risk;
- object: make the safe/betraying choice reasonable;
- prove: introduce evidence that changes what the room can deny;
- boundary: define what will no longer happen;
- re-choice: ask again after truth/freedom has been restored.

If a line only explains what the audience already sees, cut it or convert it into action.

## 2. Listening is visible in the answer

A professional answer responds to the previous speaker's concrete move, not merely to the theme.

Bad pattern:

- Authority: “Sign the confession.”
- Protagonist: “I believe in truth and love.”

Better pattern:

- Authority: “Sign the confession and the house survives.”
- Protagonist: “Then the house burns honestly. I don't sign.”

The second answer hears the exact bargain. It costs something.

## 3. The objection must make betrayal reasonable

A weak witness says “be careful.” A strong objection explains why the wrong choice is tempting:

- “Give them the child; perhaps they'll leave the oven standing.”
- “Price her pain, and you eat somewhere else.”
- “He uses that form because he knows you cannot bear to lose it.”

This is how dialogue creates suspense without plot confusion: the audience understands the seductive wrong path.

## 4. Protagonist decisions should be embodied and interruptible

Prefer short behavior-forward lines:

- “Not while she's shaking.”
- “Then run beside me. Don't take it from my hands.”
- “Door first. If she comes uncaged, they can see why.”

These lines work because they attach to physical action: stepping into reach, refusing proof transfer, opening a gate. Long speeches should be reserved for moral pivots after action has already proven the stakes.

## 5. Proof should not be self-certified by the protagonist

If the protagonist both makes the moral choice and announces that the proof validates them, the scene becomes self-explanatory. Stronger endings let a witness, object, opponent, or environment confirm the cost/proof:

- customer witnesses work quality;
- caregivers observe creature fear/trust;
- ledgers, heat marks, salt patterns, doors, keys, and timestamps contradict authority;
- opponents accidentally reveal that commodification was the real motive.

Production rule added to `dialogue_craft`: when the same speaker carries `protagonist_decision` and `evidence_or_cost`, flag protagonist self-explanation.

## 6. Explicit moral language belongs at the pivot, not everywhere

MythicTwist shows when explicit naming is powerful:

- “I hate being lied to.”
- using animal form to obtain forgiveness “destroyed” the remaining trust;
- “Whether you want to stay or leave, I won't force you again.”
- “This time it's my choice.”

These lines work because the audience has already seen the deception, boundary, restitution, and no-force choice. Do not start with abstract consent speeches. Let behavior create the problem, then use exact moral language to make the pivot undeniable.

## 7. Boundary dialogue is forward-looking, not revenge decoration

Velvet's strongest family-exit language does not merely accuse. It defines future reality:

- not because of one object, but because she was at the bottom of priorities;
- not to punish them, but to live outside the favored sibling's shadow;
- return is conditional and no longer needed in the old way.

Professional boundary dialogue should answer: what will the speaker no longer participate in, what material condition must change, and what behavior would count as repair?

## 8. Voice differentiation by function

### Authority / institution

Uses procedure, price, permission, deadline, ledger, license, legality, public order. It rarely needs to sound emotional. Its power is impersonal.

Example shape: “No license, no hand on that pump.”

### Caregiver / witness

Uses sensory risk, practical timing, bodily consequence, work knowledge, and immediate safety. It warns because it knows cost.

Example shape: “Pull it, and no hand will ever mean safety again.”

### Protagonist

Uses embodied refusal, concrete acceptance of cost, and short directives tied to action. Avoid generic courage language.

Example shape: “Then run beside me. Don't take it from my hands.”

### Evidence voice

Can belong to a witness, opponent, object-reading expert, or observational caregiver. It states what can no longer be denied, not what the theme means.

Example shape: “Salt inside this seal is fresh. Your ledger says it was closed.”

### Vulnerable creature/child

Should not become a cute exposition device. Nonverbal reaction, fragments, withdrawal, approach, freezing, singing, or touching often carry more truth than dialogue.

## 9. Convert exposition into procedure

Instead of “The land trust has controlled water for twenty years,” stage:

- a ration line;
- a ledger timestamp;
- a pump that only opens for paying households;
- a signature demand;
- a witness who remembers the meter being changed.

Exposition becomes dramatized when someone uses it to extract behavior.

## 10. Scene rhythm template

The default four-turn professional rhythm is:

1. **External pressure** — institution/person demands something concrete.
2. **Witness objection** — a reasonable voice makes the safe betrayal legible.
3. **Protagonist decision** — protagonist answers through behavior and accepts cost.
4. **Evidence or cost** — proof/consequence escapes verbal control.

This template is not mandatory for visual-first creature scenes. If only one spoken turn exists, it should still carry pressure/decision/subtext while images do the rest.

## 11. Density must match format

- **Vertical romantic/melodrama:** dense negotiation, procedural repair, boundary language, repeated status shifts.
- **Creature fantasy:** sparse imperatives and care language; let visual objectives, creature behavior, sound, and spatial movement carry causality.
- **Found-family compression:** origin/endangerment and care montage can be nearly dialogue-free; the few lines should be protective, instructional, or rupture-defining.
- **Political fantasy:** institutional language must remain concrete—decrees, ledgers, licenses, borders, signatures—not floating lore.

## 12. Rewrite checklist

For every exchange ask:

1. What does each speaker want in this exact moment?
2. What concrete pressure is being answered?
3. What is the safe/betraying option, and why is it tempting?
4. Which line changes behavior rather than opinion?
5. Who confirms proof—and is it someone other than the protagonist?
6. Which feeling is already visible and therefore should not be named?
7. Can any long line be split by movement, interruption, object handling, or silence?
8. Does the final turn escape the protagonist's verbal control?

## Current production integration

- `creature_dialogue.py` now distributes proof/cost confirmation away from repeated protagonist self-certification in key creature-economic scenes.
- `dialogue_craft.py` warns when the same speaker carries both protagonist decision and evidence/cost confirmation.
- Existing performance fields (`power_move`, `listening_response`, `delivery`, `status_shift`, `room_sound`) should remain synchronized with actual speaker role.

## Bottom line

Professional dialogue is not prettier exposition. It is a sequence of audible power moves in which characters listen, evade, pressure, refuse, protect, and reveal—while objects, witnesses, silence, and behavior carry the psychology the words cannot honestly say.
