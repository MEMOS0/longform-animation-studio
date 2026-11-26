"""Scene-specific creature-economic dialogue scaffolds.

These are not final shooting-script lines. They convert abstract theme statements
into short pressure/objection/decision/evidence exchanges that a later professional
rewrite can deepen without losing causality.
"""
from __future__ import annotations

from typing import Any


def creature_dialogue_materials(ctx: dict[str, Any], index: int) -> dict[str, Any]:
    creature = ctx["creature"]
    creature_label = ctx["creature_label"]
    caregiver = ctx["caregiver"]
    authority = ctx["authority"]
    protagonist = ctx["protagonist_name"]
    object_term = ctx["object_term"]
    resource = ctx["resource"]
    system = ctx["system"]
    evidence = ctx["evidence"]
    trait = ctx["trait"]
    pain_unit = "feather" if ctx["heat_based"] else "fin-ray"
    portion = "bowl" if ctx["heat_based"] else "cup"

    key_lines = [
        [f"Back off. {creature_label} came to me bleeding, not asking for permission.", "I hide her first. Questions after she's safe.", f"The {resource} moved when she cried; the {system} saw her."],
        ["I'll work for the roof. I won't sell her pain for it.", f"The {object_term} opens a way; it doesn't make her ours.", "Feed her first. Price her never."],
        ["I refuse your price while she's shaking.", "A house bought by her pain isn't a home.", f"She isn't inventory with {trait}."],
        [f"Your ledger can lie; {evidence} can't.", "One honest customer before you call me a thief.", f"The {system} remembers every hand that opened it."],
        ["I saved her from you. That isn't theft.", "Hunger isn't permission.", "The proof is already beyond your ledger."],
        ["Help me carry the proof, not my choice.", "Wait for permission and they own the truth.", f"{evidence.capitalize()}, timing, witnesses—line them up."],
        ["Return what your papers stole before you ask for trust.", "She chooses first. Law second.", f"Let the {resource} answer."],
        [f"This {system} is not a cage anymore.", f"Revenge won't fill one {portion}.", "She crosses by choice; the doors stay open."],
    ][index - 1]

    exchanges = [
        [
            (authority, f"Paying hands first, {protagonist}. Step away from the {system}.", "the crowd blocks the public resource threshold"),
            (caregiver, "Don't lift her into the crowd—she'll bolt.", f"{caregiver} shifts between the crowd and the creature"),
            (protagonist, "I hide her first. Questions after she's safe.", f"{protagonist} kneels and covers the creature"),
            (caregiver, f"Look at the {resource}. It moved when she cried.", f"the {resource} response becomes visible to the nearest witness"),
        ],
        [
            (caregiver, "This roof feeds workers, not miracles.", "shelter is offered as labor rather than charity"),
            (caregiver, "But hunger isn't a bill yet. Don't price her before she eats.", "the caregiver names the safe boundary before help becomes control"),
            (protagonist, "Then I'll work. I won't sell her pain for a bed.", "the protagonist accepts work while refusing monetized suffering"),
            (protagonist, f"The {object_term} opens a way. It doesn't make her ours.", f"the {object_term} is set beside the creature rather than used as a claim"),
        ],
        [
            (authority, f"One {pain_unit}, and your debt is gone.", "the offer converts creature pain into economic rescue"),
            (caregiver, "A cheap miracle is still a wound.", f"{caregiver} blocks the reach toward the creature"),
            (protagonist, "Not while she's shaking.", f"{protagonist} steps into the reach instead of arguing abstractions"),
            (authority, f"Look at those {trait}. Even she knows what you're worth.", f"fear moves through the creature's {trait}, making the cost visible"),
        ],
        [
            (authority, f"Unlicensed hands don't touch the {system}.", "competence is reframed as illegality"),
            ("customer witness", "Her repair held mine all morning.", "one practical witness breaks the crowd's certainty"),
            (protagonist, "One honest customer before you call me a thief.", f"{protagonist} keeps working instead of pleading"),
            (protagonist, f"The {system} remembers every hand that opened it.", f"the first {evidence} trace is exposed"),
        ],
        [
            (authority, f"Thief. You stole {resource} and hid the proof.", "public accusation turns the creature into evidence"),
            (caregiver, "Show the child and this ends.", f"{caregiver} offers the safer betrayal"),
            (protagonist, "I saved her from you. That isn't theft.", f"{protagonist} shields the creature before defending reputation"),
            (protagonist, "The proof is already beyond your ledger.", f"the {object_term} passes out of institutional control"),
        ],
        [
            (caregiver, "Give me the proof. I can carry it faster.", "help threatens to become takeover"),
            ("care network witness", "If one pair of hands carries it, one pair of hands can bury it.", "the witness makes the cost of surrendering authorship concrete"),
            (protagonist, "Help me carry it. Don't carry my choice.", "the protagonist accepts help while keeping control of the proof"),
            (protagonist, f"{evidence.capitalize()}, timing, witnesses—line them up.", "the proof chain becomes a physical arrangement"),
        ],
        [
            (authority, "Take the rescue. Sign the apology.", "institutional rescue is offered before restitution"),
            (caregiver, "She won't come forward while you hold the papers.", "the creature remains outside reach until consent is possible"),
            (protagonist, "Return what your papers stole before you ask for trust.", "the protagonist refuses the shortcut public win"),
            (protagonist, f"Let her choose. Let the {resource} answer first.", f"{creature} is allowed to move forward by choice"),
        ],
        [
            (authority, "You win. Now make them pay.", "the ending is tempted toward revenge"),
            (caregiver, f"Revenge won't fill one {portion}.", "the community's material need interrupts triumph"),
            (protagonist, f"This {system} is not a cage anymore.", "the exclusion threshold is opened for communal use"),
            (caregiver, "She crossed by herself. Leave the door open.", "the creature's free crossing confirms non-possessive belonging"),
        ],
    ][index - 1]

    beat_names = ["external_pressure", "witness_objection", "protagonist_decision", "evidence_or_cost"]
    return {
        "key_lines": key_lines,
        "spoken_exchange": [
            {"beat": beat, "speaker": speaker, "line": line, "action": action}
            for beat, (speaker, line, action) in zip(beat_names, exchanges)
        ],
    }
