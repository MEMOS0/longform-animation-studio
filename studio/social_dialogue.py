"""Scene-specific social-test melodrama dialogue scaffolds.

These are structured first-pass professional exchanges for noncreature social
melodrama. They are not final shooting-script lines; they preserve pressure,
reasonable objection, embodied decision, and visible proof so a later rewrite can
deepen voice without losing causality.
"""
from __future__ import annotations

import re
from typing import Any


def _first_words(text: str, count: int, fallback: str) -> str:
    words = re.findall(r"[A-Za-z0-9'-]+", text)
    return " ".join(words[:count]) if words else fallback


def social_test_dialogue_materials(premise: dict[str, Any], index: int) -> dict[str, Any]:
    protagonist_identity = str(premise.get("protagonist", {}).get("identity", "the protagonist"))
    protagonist = protagonist_identity.split(",", 1)[0].strip() or "the protagonist"
    capability = str(premise.get("protagonist", {}).get("capability", "craft expertise"))
    craft = capability.split(" expertise", 1)[0].split(",", 1)[0].strip() or "craft"
    object_name = str(premise.get("meaning_carrier", {}).get("object_or_space", "inherited object")).strip() or "inherited object"
    child_ally = str(premise.get("emotional_engine", {}).get("protective_counterforce", "the child ally")).split(" physically", 1)[0].split(";", 1)[0].strip() or "the child ally"
    child_label = _first_words(child_ally, 5, "child ally")
    care_text = str(premise.get("relational_contract", {}).get("safety_or_kindness_before_power", premise.get("emotional_engine", {}).get("protective_counterforce", "the caregiver"))).strip() or "the caregiver"
    care_base = re.split(r"\s+(?:offers?|gives?|hides?|trades?|feeds?)\s+", care_text, maxsplit=1)[0].strip()
    caregiver = _first_words(care_base, 4, "caregiver").removesuffix(" and")
    power_text = str(premise.get("emotional_engine", {}).get("injustice", "the status authority")).split(" enforces", 1)[0].strip() or "the status authority"
    if "chief engineer" in power_text:
        authority = "chief engineer"
    elif "betrothed" in power_text:
        authority = "status betrothed"
    elif "guildmaster" in power_text or "guild" in power_text:
        authority = "guild authority"
    else:
        authority = _first_words(power_text, 3, "status authority")
    proof_items = [item.strip() for item in str(premise.get("proof_chain", "object mark, witness timing, ledger record")).split(",") if item.strip()]
    proof_one = proof_items[0] if proof_items else "object mark"
    proof_two = proof_items[1] if len(proof_items) > 1 else "ledger timing"
    witness = "practical witness"

    key_lines = [
        ["Your floor is below. Guests eat above.", "Then my plate goes down there too.", "Don't make yourself small because they're watching."],
        ["I don't have charity. I have work no one else will finish.", "Pay me when the work holds, not before.", "I asked for a bench, not a hiding place."],
        ["A license proves you know who owns it.", "Test the work. Don't measure my bloodline.", "The proof answers before I do."],
        ["Her repair held through the morning rush. I watched it.", "Give me one minute before you invent a thief.", f"The {proof_one} doesn't match their story."],
        ["A bench bought with a lie isn't mine.", "Show the lock my hands opened.", f"The {proof_two} was already outside their control."],
        ["Carry the copy. The original stays with me.", "Fast hands can bury truth as easily as carry it.", "Lies fail when they have to answer every angle."],
        ["Return the name you erased first.", "Repair isn't a favor.", "I heard what was said when the doors were closed."],
        ["Open the doors. Pay the hands that built the room.", "Revenge won't feed the people who were locked out.", "I sit here because I choose to, not because you allow it."],
    ][index - 1]

    exchanges = [
        [
            (authority, "Your floor is below. Guests eat above.", f"{authority} uses the room arrangement to make exclusion feel procedural"),
            (child_label, "Then my plate goes down there too.", f"{child_label} lifts a plate and crosses toward {protagonist}"),
            (protagonist, "Don't make yourself small because they're watching.", f"{protagonist} tries to stop the child without rejecting the kindness"),
            (child_label, "You shared yours before anyone told you to.", f"{child_label} sits beside {protagonist} in full view"),
        ],
        [
            (caregiver, "I don't have charity. I have work no one else will finish.", f"{caregiver} points to unfinished labor instead of offering rescue"),
            (child_label, "She helped before she knew anyone was watching.", f"{child_label} keeps the object within sight without touching it"),
            (protagonist, "Then pay me when the work holds, not before.", f"{protagonist} accepts the tools and sets a boundary around pity"),
            (caregiver, "Fair. But if they ask, I won't say you're hiding here.", f"{caregiver} leaves the door visible rather than concealing the arrangement"),
        ],
        [
            (authority, "A license proves you know who owns it. Nothing more.", f"{authority} turns craft legitimacy into property"),
            (caregiver, "Careful. Skilled hands are useful until they stop asking permission.", f"{caregiver} warns that refusal has a price"),
            (protagonist, "Then test the work. Don't measure my bloodline.", f"{protagonist} places the workpiece or tool where everyone can inspect it"),
            (witness, f"The {proof_one} answers before she does.", f"{witness} notices the first material contradiction"),
        ],
        [
            (authority, "This failure carries your mark. Convenient, isn't it?", f"{authority} displays the accusation before the evidence is examined"),
            (witness, "Her repair held through the morning rush. I watched it myself.", f"{witness} speaks from direct use, not loyalty"),
            (protagonist, "Give me one minute before you invent a thief.", f"{protagonist} reaches for the bench/control rather than pleading"),
            (witness, f"The {proof_one} doesn't match the time they wrote down.", f"{witness} exposes the first crack in the official sequence"),
        ],
        [
            (authority, "Admit the theft, and perhaps you keep working.", f"{authority} offers survival as the price of false confession"),
            (caregiver, "A quiet lie buys one more night. It also buys the next one.", f"{caregiver} makes the safe betrayal understandable"),
            (protagonist, "A bench bought with a lie isn't mine.", f"{protagonist} steps away from the offered protection"),
            (witness, f"The {proof_two} doesn't fit her hands or her hours.", f"{witness} moves the evidence beyond rumor"),
        ],
        [
            (caregiver, "Give me the proof. I can move faster than you.", f"{caregiver} reaches for the proof with urgent protective intent"),
            (witness, "Fast hands can bury truth as easily as carry it.", f"{witness} blocks the transfer without accusing care"),
            (protagonist, "Carry the copy. The original stays with me.", f"{protagonist} separates duplication from authorship"),
            (witness, "Then we need eyes on every angle before they close the room.", f"{witness} begins arranging timing, access, and testimony"),
        ],
        [
            (authority, "I can reinstate you. Isn't that what you came for?", f"{authority} offers status restoration before restitution"),
            (caregiver, "A title is easier than admitting who broke it.", f"{caregiver} refuses to let restoration replace accountability"),
            (protagonist, "Return the name you erased first.", f"{protagonist} keeps the demand material and specific"),
            (child_label, "I heard what was said when the doors were closed.", f"{child_label} steps forward as witness rather than mascot"),
        ],
        [
            (authority, "What would satisfy you?", f"{authority} finally asks because command no longer controls the room"),
            (caregiver, "Revenge won't feed the people who were locked out.", f"{caregiver} turns attention back to material survival"),
            (protagonist, "Open the doors. Pay the hands that built the room. Let everyone sit by choice.", f"{protagonist} converts victory into changed access"),
            (child_label, "Then I'll sit here because I want to—not because you allow it.", f"{child_label} chooses the once-shamed place freely"),
        ],
    ][index - 1]

    subtexts = [
        [
            "public exclusion depends on making status geography look like neutral procedure",
            "the child refuses the premise that dignity is allocated by height, wealth, or permission",
            "the protagonist protects the child's dignity even while needing the protection herself",
            "kindness becomes evidence because it repeats behavior that predates public advantage",
        ],
        [
            "help is safest when it offers work rather than ownership or rescue",
            "the witness separates character from usefulness by naming behavior before observation",
            "the protagonist preserves dignity by tying payment to real work",
            "transparent shelter is riskier than hidden charity, which is why it matters",
        ],
        [
            "institutional ownership tries to redefine competence as borrowed permission",
            "the caregiver understands that competence becomes dangerous when it stops being dependent",
            "the protagonist asks for a test of reality rather than belief or pity",
            "material proof interrupts status theater before anyone can control the explanation",
        ],
        [
            "the accusation uses surface resemblance to avoid examining causality",
            "a practical witness matters because they verify outcomes rather than emotions",
            "the protagonist asks for a finite procedural test instead of demanding trust",
            "time and material evidence begin contradicting the institution's authored sequence",
        ],
        [
            "the institution prefers a false confession because it converts theft into the victim's identity",
            "the safe betrayal is reasonable because survival is immediate and justice is uncertain",
            "the protagonist refuses ownership built on erasing truth",
            "proof escapes narrative control when timing and bodily capability no longer align",
        ],
        [
            "help becomes dangerous when speed quietly transfers authorship away from the person who paid the cost",
            "the witness understands that whoever controls proof can erase it",
            "the protagonist accepts support without surrendering accountability",
            "a proof chain becomes stronger when independent angles must all be answered",
        ],
        [
            "restoration without admission lets the institution keep authorship of the harm",
            "repair must name what was broken before status can mean anything",
            "the protagonist demands restitution in concrete form rather than revenge",
            "the vulnerable witness becomes an agent whose testimony cannot be reduced to innocence symbolism",
        ],
        [
            "power only asks what would satisfy the victim after losing unilateral control",
            "community need interrupts triumph because punishment alone cannot feed or shelter anyone",
            "the protagonist turns reversal into shared access rather than personal elevation",
            "chosen presence in the former shame-space proves the status order has actually changed",
        ],
    ][index - 1]

    beat_names = ["external_pressure", "witness_objection", "protagonist_decision", "evidence_or_cost"]
    craft_by_beat = {
        "external_pressure": {
            "power_move": "procedural exclusion, coercive offer, accusation, or status demand",
            "listening_response": "answers the immediate threat before the room can hear the larger truth",
            "delivery": "clipped, public, procedural; power sounds impersonal rather than emotionally loud",
            "status_shift": "authority controls the room, paperwork, or resource threshold",
            "room_sound": "crowd texture, cutlery, machinery, ledger paper, or work noise dominates the vulnerable body",
        },
        "witness_objection": {
            "power_move": "reasonable protective objection or testimony that makes the cost legible",
            "listening_response": "responds to what the pressure physically endangers rather than repeating the protagonist's wish",
            "delivery": "low, practical, specific; care and evidence sound observed rather than inspirational",
            "status_shift": "fear or truth moves from abstraction into relational and material consequence",
            "room_sound": "breath, object contact, work rhythm, and nearby movement replace public certainty",
        },
        "protagonist_decision": {
            "power_move": "embodied boundary, refusal, or controlled acceptance of cost",
            "listening_response": "answers the objection by changing behavior rather than winning the argument",
            "delivery": "quiet, concrete, no pleading; short enough to survive interruption",
            "status_shift": "the protagonist accepts cost and takes moral initiative",
            "room_sound": "tool contact, footstep, withheld breath, or object placement lands before music resolves the choice",
        },
        "evidence_or_cost": {
            "power_move": "material proof, witness choice, or irreversible social cost escapes verbal control",
            "listening_response": "the final speaker reacts to what the room/object/proof has made undeniable",
            "delivery": "observational and restrained; do not explain what the image or evidence already proves",
            "status_shift": "truth becomes harder for the institution or crowd to erase",
            "room_sound": "object resonance, public silence, or communal movement carries the reversal",
        },
    }
    voice_profiles = {
        "authority": {
            "voice_signature": "procedural extraction: rules, licenses, seating, confessions, restoration offers, and controlled permission",
            "withheld_need": "preserve institutional authorship and prevent worker competence from exposing dependence or theft",
        },
        "care": {
            "voice_signature": "practical sensory risk: work, food, shelter, timing, survival, and the price of sheltering someone vulnerable",
            "withheld_need": "help without letting charity become ownership or a safer betrayal",
        },
        "protagonist": {
            "voice_signature": "short embodied boundary: what she will test, carry, refuse, repay, or open with her hands now",
            "withheld_need": "survive without accepting dignity as a gift controlled by the people who harmed her",
        },
        "witness": {
            "voice_signature": "observed evidence: what was personally seen, heard, timed, measured, or used; no thematic explanation",
            "withheld_need": "tell the truth while limiting retaliation and avoiding becoming the institution's spectacle",
        },
    }

    def voice_profile(speaker_name: str) -> dict[str, str]:
        if speaker_name == authority:
            return voice_profiles["authority"]
        if speaker_name == protagonist:
            return voice_profiles["protagonist"]
        if speaker_name == witness or speaker_name == child_label:
            return voice_profiles["witness"]
        return voice_profiles["care"]

    enriched_exchange = []
    for beat, (speaker, line, action), subtext in zip(beat_names, exchanges, subtexts):
        enriched_exchange.append({
            "beat": beat,
            "speaker": speaker,
            "line": line,
            "action": action,
            "subtext": subtext,
            **voice_profile(speaker),
            **craft_by_beat[beat],
        })
    return {
        "key_lines": key_lines,
        "spoken_exchange": enriched_exchange,
        "scene_rhythm": "enter inside a procedural status move, let a witness or caregiver make the safe cost reasonable, answer through embodied refusal/work, then end on material proof or changed access",
        "rewrite_directives": [
            "keep each line short enough to be interrupted by labor, crowd noise, or object movement",
            "make every answer respond to the previous speaker's concrete pressure rather than restating theme",
            "let tools, seating, doors, ledgers, witnesses, and work rhythms carry meaning between lines",
            "avoid naming feelings that spatial action or evidence has already proven",
        ],
    }
