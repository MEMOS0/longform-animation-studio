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
    heat_based = bool(ctx["heat_based"])
    pain_unit = "feather" if heat_based else "fin-ray"
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

    if heat_based:
        opening_demand = f"Oven ration's for guild households, {protagonist}. Back of the line."
        pain_offer = f"One {pain_unit}, and the coal ledger closes tonight."
        license_demand = f"No guild mark, no hand on that {system}."
        theft_accusation = f"Thief. You stole {resource} and hid the guild proof."
        rescue_offer = "Take the guild pardon. Sign the confession."
        revenge_temptation = f"The guild is finished. Take their {system}s and make them crawl."
        evidence_reaction = "Coals are bending. Look—she's crying, not performing."
        proof_line = "This seam is still hot. Your ledger says the oven was closed."
        open_first = "Open the oven door first. Then ask me to trust your ink."
        shared_line = "No. One oven burning for everyone is worth more than ten men kneeling."
    else:
        opening_demand = f"Pump's for paying households, {protagonist}. Back of the line."
        pain_offer = f"One {pain_unit}, and the debt ledger closes tonight."
        license_demand = f"No license, no hand on that {system}."
        theft_accusation = f"Thief. You stole {resource} and hid the proof."
        rescue_offer = "Take the rescue. Sign the apology."
        revenge_temptation = "The trust is finished. Take their gates and make them crawl."
        evidence_reaction = "Salt's rising. Look—she's crying, not performing."
        proof_line = "Salt inside this seal is fresh. Your ledger says it was closed."
        open_first = "Open the pump gate first. Then ask me to trust your ink."
        shared_line = "No. One gate open for everyone is worth more than ten men kneeling."

    creature_cover = "flour cloth" if heat_based else "shawl"
    fear_feature = "feathers" if heat_based else "fins"
    habitat = "carts" if heat_based else "crowd"
    shelter_work = "mill" if heat_based else "cart"
    child_term = "bird" if heat_based else "child"
    proof_marks = "Heat" if heat_based else "Salt"
    gate_times = "kiln times" if heat_based else "gate times"

    exchanges = [
        [
            (authority, opening_demand, "the crowd blocks the public resource threshold"),
            (caregiver, "Don't scoop her up. Sudden hands make her bolt.", f"{caregiver} shifts between the crowd and the creature"),
            (protagonist, f"Easy. Under my {creature_cover}—no one sees {fear_feature}.", f"{protagonist} kneels and covers the creature"),
            (caregiver, evidence_reaction, f"the {resource} response becomes visible to the nearest witness"),
        ],
        [
            (caregiver, "This roof feeds workers. Miracles don't pay for bread.", "shelter is offered as labor rather than charity"),
            (caregiver, "Price her pain, and you eat somewhere else.", "the caregiver names the safe boundary before help becomes control"),
            (protagonist, f"Then I'll work the {shelter_work}. Her pain isn't rent.", "the protagonist accepts work while refusing monetized suffering"),
            (protagonist, f"The {object_term} opens the {system} seam. It doesn't make her mine.", f"the {object_term} is set beside the creature rather than used as a claim"),
        ],
        [
            (authority, pain_offer, "the offer converts creature pain into economic rescue"),
            (caregiver, "Pull it, and no hand will ever mean safety again.", f"{caregiver} blocks the reach toward the creature"),
            (protagonist, "Not while she's shaking.", f"{protagonist} steps into the reach instead of arguing abstractions"),
            (authority, "Hold her still. Breathing creatures bring higher prices.", f"fear moves through the creature's {trait}, making the cost visible"),
        ],
        [
            (authority, license_demand, "competence is reframed as illegality"),
            ("customer witness", f"{protagonist}'s patch held through the morning rush. I watched it.", "one practical witness breaks the crowd's certainty"),
            (protagonist, "Test the work before you invent a thief.", f"{protagonist} keeps working instead of pleading"),
            (protagonist, proof_line, f"the first {evidence} trace is exposed"),
        ],
        [
            (authority, theft_accusation, "public accusation turns the creature into evidence"),
            (caregiver, f"Give them the {child_term}; perhaps they'll leave the {system} standing.", f"{caregiver} offers the safer betrayal"),
            (protagonist, "I opened your cage. That isn't theft.", f"{protagonist} shields the creature before defending reputation"),
            (protagonist, f"The {object_term} is past the gate. Your ledger can't swallow it now.", f"the {object_term} passes out of institutional control"),
        ],
        [
            (caregiver, "Give me the proof. I run faster than you.", "help threatens to become takeover"),
            ("care network witness", "Fast hands can bury proof as easily as carry it.", "the witness makes the cost of surrendering authorship concrete"),
            (protagonist, "Then run beside me. Don't take it from my hands.", "the protagonist accepts help while keeping control of the proof"),
            (protagonist, f"{proof_marks} marks, {gate_times}, witnesses—line them up.", "the proof chain becomes a physical arrangement"),
        ],
        [
            (authority, rescue_offer, "institutional rescue is offered before restitution"),
            (caregiver, "She won't step forward while your papers own the room.", "the creature remains outside reach until consent is possible"),
            (protagonist, open_first, "the protagonist refuses the shortcut public win"),
            (protagonist, "Door first. If she comes uncaged, they can see why.", f"{creature} is allowed to move forward by choice"),
        ],
        [
            (authority, revenge_temptation, "the ending is tempted toward revenge"),
            (caregiver, f"Revenge won't fill one {portion}.", "the community's material need interrupts triumph"),
            (protagonist, shared_line, "the exclusion threshold is opened for communal use"),
            (caregiver, "She crossed alone. Leave the door open.", "the creature's free crossing confirms non-possessive belonging"),
        ],
    ][index - 1]

    subtexts = [
        [
            "need is being framed as illegality so control of the resource stays unquestioned",
            "intervention can become exposure if panic drives the creature into the crowd",
            "safety outranks being understood or socially approved",
            "the creature's response makes personhood materially visible before anyone can explain it",
        ],
        [
            "care is being offered, but only inside a labor hierarchy that can become control",
            "the witness is warning that charity becomes exploitation the moment suffering gets priced",
            "accepting work preserves dignity while refusing to convert pain into currency",
            "the object is a means of passage, not a claim of ownership",
        ],
        [
            "the offer is seductive because one small wound could erase an unbearable debt",
            "the objection names the moral cost before anyone can call the bargain practical",
            "the protagonist refuses in the present tense because the creature's fear matters more than the argument",
            "the antagonist tries to make the creature's body testify against its own personhood",
        ],
        [
            "competence is dangerous to the authority because it exposes whom the system actually depends on",
            "the witness is not defending the protagonist emotionally; they are defending results they personally verified",
            "the protagonist asks for evidence to be tested rather than asking to be believed",
            "the infrastructure itself becomes a witness that contradicts institutional authorship",
        ],
        [
            "public shame is being used to force the creature into visibility as evidence",
            "the safer betrayal sounds merciful because it promises immediate social peace",
            "the protagonist protects before defending reputation, proving the hierarchy of values",
            "the proof escaping the ledger means truth no longer belongs to the institution that controlled it",
        ],
        [
            "help becomes dangerous when speed quietly transfers authorship away from the person who paid the cost",
            "the witness understands that whoever controls the proof can also erase it",
            "the protagonist accepts support while keeping moral agency and public accountability",
            "the proof chain must become procedural and physical so emotion cannot be dismissed as rumor",
        ],
        [
            "the institution prefers a rescue narrative that preserves its authority instead of making restitution",
            "the creature cannot consent while legal coercion remains in the room",
            "the protagonist refuses a shortcut victory because trust without repair would repeat the original theft",
            "consent is staged materially before language, so the creature is not merely won as a prize",
        ],
        [
            "victory creates a final temptation to turn protection into domination",
            "material survival interrupts triumph because revenge cannot feed the community",
            "the protagonist converts the old exclusion mechanism into shared infrastructure",
            "non-possessive belonging is confirmed only when the creature is free to leave or stay",
        ],
    ][index - 1]

    beat_names = ["external_pressure", "witness_objection", "protagonist_decision", "evidence_or_cost"]
    craft_by_beat = {
        "external_pressure": {
            "power_move": "coercive exclusion or institutional demand",
            "listening_response": "answers the immediate resource/status threat before anyone can explain the larger conflict",
            "delivery": "clipped, public, procedural; the speaker does not need to sound emotional to exercise power",
            "status_shift": "authority controls the threshold, crowd, or paperwork",
            "room_sound": "crowd texture, ledger paper, coin/metal, or machinery stays louder than the vulnerable body",
        },
        "witness_objection": {
            "power_move": "reasonable protective objection that makes the safe betrayal legible",
            "listening_response": "responds to what the pressure physically endangers rather than repeating the protagonist's wish",
            "delivery": "low, urgent, close-mic; advice sounds practical rather than thematic",
            "status_shift": "fear moves from public punishment into relational and bodily cost",
            "room_sound": "breath, cloth, small movement, and nearby labor noise replace the crowd's certainty",
        },
        "protagonist_decision": {
            "power_move": "embodied boundary, refusal, or controlled acceptance of cost",
            "listening_response": "answers the objection by changing behavior, not by winning the argument",
            "delivery": "quiet, concrete, no pleading; short enough to survive interruption",
            "status_shift": "the protagonist accepts cost and takes moral initiative",
            "room_sound": "contact, kneeling, object touch, or withheld breath lands before music can resolve the choice",
        },
        "evidence_or_cost": {
            "power_move": "material proof or irreversible cost escapes verbal control",
            "listening_response": "the final speaker reacts to what the room/object/creature has made undeniable",
            "delivery": "observational and restrained; do not explain the meaning after the image proves it",
            "status_shift": "truth, personhood, or proof becomes publicly harder to erase",
            "room_sound": "object resonance, creature response, and negative space carry the reversal",
        },
    }
    enriched_exchange = []
    for beat, (speaker, line, action), subtext in zip(beat_names, exchanges, subtexts):
        craft = dict(craft_by_beat[beat])
        if beat == "external_pressure" and speaker != authority:
            craft.update({
                "power_move": "urgent help or shelter pressure that can quietly become control",
                "listening_response": "responds to the concrete danger by offering speed, work, or shelter rather than institutional command",
                "delivery": "low, urgent, practical; concern is audible even when the offer threatens agency",
                "status_shift": "the helper gains logistical control while risking takeover of the protagonist's choice",
                "room_sound": "breath, cloth, footsteps, food/labor texture, and nearby danger crowd the vulnerable body",
            })
        elif beat == "evidence_or_cost" and speaker == authority:
            craft.update({
                "power_move": "coercive bodily escalation or commodification threat",
                "listening_response": "the authority answers refusal by forcing the creature's body to carry the cost",
                "delivery": "sharp, transactional, threatening; cruelty is procedural rather than observational",
                "status_shift": "authority tries to convert fear and bodily harm into control",
                "room_sound": "chains, coin counts, hostile murmur, and creature distress overpower restraint",
            })
        enriched_exchange.append({
            "beat": beat,
            "speaker": speaker,
            "line": line,
            "action": action,
            "subtext": subtext,
            **craft,
        })
    return {
        "key_lines": key_lines,
        "spoken_exchange": enriched_exchange,
        "scene_rhythm": "enter inside pressure, compress the objection into a concrete unsafe choice, let the protagonist answer through behavior, then end on proof/cost rather than explanation",
        "rewrite_directives": [
            "keep every turn short enough to be interrupted by movement, crowd noise, or creature reaction",
            "make each answer respond to the previous speaker's concrete pressure rather than restating theme",
            "let hands, objects, witnesses, thresholds, and creature behavior carry meaning between lines",
            "avoid naming feelings that the action has already proven",
        ],
    }
