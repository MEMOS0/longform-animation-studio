"""Scene-level materials for transformation-romance packages."""

from typing import Any


def transformation_scene_materials(premise: dict[str, Any], index: int) -> dict[str, Any] | None:
    if premise.get("channel_contract") != "transformation_romance":
        return None
    protagonist = str(premise.get("protagonist", {}).get("identity", "the protagonist")).split(",", 1)[0]
    key_lines = {
        1: ["Stop filming her.", "I'm fine. Please don't make it worse."],
        2: ["You taught me hiding was love.", "Whatever I become, I choose it this time."],
        3: ["Choose again. One more try.", "I am not doing this for their mirror."],
        4: ["Don't trust their mirror. They only know what they want to see."],
        5: ["I don't know how to be watched yet.", "Then don't perform. Do the work."],
        6: ["Stop deciding for me.", "Then ask me now. Really ask."],
        7: ["You remembered me before anyone clapped.", "I choose you, not the gratitude."],
        8: ["I am not the person you filmed.", "This time I choose the light."],
    }
    spoken_exchange = {
        1: [
            ("witness_objection", "student witness", "Everyone is filming. We should go.", "the witness pulls at a sleeve while phones rise", "escape is reasonable because exposure has already become harm", "whispered urgency"),
            ("protagonist_decision", protagonist, "Don't film her.", f"{protagonist} steps between the vulnerable person and the phones", "protection precedes self-protection", "low, shaking but firm"),
        ],
        2: [
            ("external_pressure", "caregiver", "I only wanted them not to hurt you.", "the caregiver cannot meet the mirror or the protagonist's eyes", "love is defending the control that caused the wound", "defensive, breaking"),
            ("protagonist_decision", protagonist, "You taught me hiding was love.", f"{protagonist} places the hidden garment/object down instead of obeying it", "naming the system is the first act of authorship", "quiet, exact"),
        ],
        4: [
            ("witness_objection", "school witness", "Do you know who she is?", "phones and bodies turn toward the transformed entrance", "the crowd's desire is still ignorance", "hushed, excited"),
            ("protagonist_decision", protagonist, "They don't know me. They only know what they want to see.", f"{protagonist} keeps walking without smiling for the phones", "visibility does not equal recognition", "controlled, private"),
        ],
        6: [
            ("external_pressure", "director or coach", "We already arranged it. This is your chance.", "the authority offers the opportunity as if refusal is ingratitude", "good outcomes do not erase consent violations", "efficient, impatient"),
            ("protagonist_decision", protagonist, "You decided for me. Then ask me now. Really ask.", f"{protagonist} stops at the threshold until the choice is returned", "the opportunity is worthless if it repeats erasure", "steady, unblinking"),
        ],
        7: [
            ("evidence_or_cost", "love interest", "You protected me before anyone clapped.", "the love interest returns the damaged memory object that proves their shared past", "memory proves recognition before transformation", "barely above breath"),
            ("protagonist_decision", protagonist, "I choose you, not the gratitude.", f"{protagonist} closes the distance only after the truth is separated from performance", "desire is chosen after worth is known", "quiet, certain"),
        ],
        8: [
            ("protagonist_decision", protagonist, "This time I choose the light.", f"{protagonist} steps into the original public geometry and uses the object openly", "visibility becomes authorship rather than approval-seeking", "clear, unforced"),
        ],
    }
    power_positions = [
        ("hidden and publicly misread", "protector despite social exposure"),
        ("self-erasing inside a protective family system", "person who can name the wound and choose change"),
        ("ashamed of practice failure", "disciplined author of transformation"),
        ("object of shallow attention", "skeptical observer of the crowd's reversal"),
        ("validated but professionally unprepared", "participant in a second arena of competence"),
        ("beneficiary of arranged visibility", "person who reclaims consent before opportunity"),
        ("uncertain whether love is gratitude or performance", "reciprocally recognized partner"),
        ("target of the original gaze", "public author and leader in the transformed wound-space"),
    ]
    subtexts = [
        "Protection is meaningful only when it crosses the gaze boundary at cost.",
        "Love distorted by fear can become the wound it tries to prevent.",
        "Transformation is self-authorship only when behavior, practice, and consent carry it.",
        "The crowd's reversal is power, not recognition.",
        "A second arena converts image into competence.",
        "Even helpful allies violate personhood when they arrange visibility without consent.",
        "Romance becomes credible when memory proves love before transformation.",
        "Visibility is repaired when the protagonist controls the original public space.",
    ]
    image_pairs = [
        ("phones rise while the protagonist steps between a frightened performer and the crowd", "the protagonist lowers the performer's shaking hands and guides her through a side door"),
        ("the caregiver hides a bright garment while the protagonist stands before a mirror", "the protagonist opens the garment bag and lays it aside instead of wearing the imposed image"),
        ("the protagonist runs speech/movement drills until she drops to the floor beside the key or whistle", "she lifts the object, opens the practice-room door, and enters again after failure"),
        ("students raise phones as the transformed protagonist crosses the public staircase or pool gallery", "she lowers her phone hand, holds the railing, and walks past without performing for the crowd"),
        ("a camera or rescue clock starts while the rival blocks the lane or stage entrance", "the protagonist enters the performance/training space and begins the work under witnesses"),
        ("the authority holds a consent form or entry list while machinery runs behind them", "the protagonist takes the form back, closes the pen in her hand, and waits until they ask"),
        ("the love interest places a damaged memory object in the protagonist's hand during rehearsal", "their hands close around the object as they step out of the staged pose and face each other"),
        ("the rival raises a phone or blocks the final public threshold", "the protagonist steps into the same public space, lifts the object openly, and guides others forward"),
    ]
    first_image, final_image = image_pairs[index - 1]
    exchange = []
    for beat, speaker, line, action, subtext, delivery in spoken_exchange.get(index, []):
        exchange.append({
            "beat": beat,
            "speaker": speaker,
            "line": line,
            "action": action,
            "subtext": subtext,
            "power_move": "image pressure answered through consent, authorship, protection, or recognition",
            "listening_response": "the next behavior answers the concrete boundary rather than explaining confidence",
            "delivery": delivery,
            "status_shift": "the speaker converts spectatorship or arranged visibility into chosen agency",
            "room_sound": "phones, crowd murmur, breath, threshold noise, camera/stage/pool machinery, and object texture remain audible beneath the line",
        })
    return {
        "key_lines": key_lines.get(index, []),
        "spoken_exchange": exchange,
        "first_image": first_image,
        "final_image": final_image,
        "scene_rhythm": "visual/social pressure first; dialogue names consent, recognition, or authorship only after blocking, objects, phones, thresholds, and protective behavior have made the psychology legible",
        "rewrite_directives": [
            "write the scene so the gaze geometry is understandable with sound off",
            "make the protagonist answer image pressure through behavior, boundaries, work, or movement rather than speeches about confidence",
            "use phones, mirrors, thresholds, cameras, water/stage machinery, and repeated public spaces as psychology carriers",
            "do not use despair harm as a cheap transformation trigger",
            "separate desire, gratitude, performance, and recognition in the romance turns",
        ],
        "power_start": power_positions[index - 1][0],
        "power_end": power_positions[index - 1][1],
        "subtext": subtexts[index - 1],
    }
