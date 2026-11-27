"""Generate first-pass scene screenplay units from story architecture.

These scenes are structured creative scaffolds: they preserve causality, power
change, subtext, sound negative space, and edit hooks so a later writing/directing
pass can deepen them rather than inventing structure from nothing.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .creature_dialogue import creature_dialogue_materials
from .survival_scene import compressed_survival_scene_materials

POWER_START = [
    "socially exposed and institutionally powerless",
    "dependent on care but beginning to act",
    "emotionally bonded but economically vulnerable",
    "competent but not yet publicly believed",
    "publicly accused and close to maximum powerlessness",
    "no longer passive but still outmatched",
    "morally credible and nearly ready to confront power",
    "able to choose the terms of public repair",
]
POWER_END = [
    "protector with a defined relational duty",
    "worker with a first zone of dignity",
    "threatened but visibly competent",
    "dangerous enough to provoke the antagonist",
    "stripped of status but in possession of the decisive question",
    "active investigator with an accountable alliance",
    "author of the coming public reversal",
    "secure in agency, work, truth, and chosen belonging",
]
SUBTEXT = [
    "Care is meaningful only when it crosses a social boundary at cost.",
    "Help becomes dignity when it creates work rather than dependence.",
    "Love and trust are shown through repeated protection, not declared as feelings.",
    "Competence threatens people whose power depends on others remaining illegible.",
    "Public shame is an attack on identity before it is an attack on facts.",
    "Agency means accepting help without surrendering authorship of the proof.",
    "Forgiveness is not owed before conduct changes.",
    "Belonging is chosen when the wound-space becomes reversible and shared.",
]


def scene_from_sequence(sequence: dict[str, Any], premise: dict[str, Any], index: int) -> dict[str, Any]:
    object_name = premise.get("meaning_carrier", {}).get("object_or_space", "inherited object")
    motif = premise.get("meaning_carrier", {}).get("sensory_signature", "a restrained tactile sound motif")
    visual = sequence.get("visual_setpiece", "a status space under pressure")
    turn = sequence.get("turn", "the power balance changes")
    clue = sequence.get("new_capability_or_clue", "a new clue or capability appears")
    relationship = sequence.get("ally_or_relationship_change", "the relationship balance changes")
    hook = sequence.get("retention_hook", "what will this choice cost?")
    function = sequence.get("function", "escalate the dramatic question")
    sound = sequence.get("sound_design_intent", "prioritize breath, room tone, and object texture over constant score")
    emotional_shift = sequence.get("emotional_shift", "pressure to resolve")
    line_options = [
        ["Sit here if you choose. No one eats beneath us again.", "I will protect her before I protect myself.", "Let them laugh; I won't leave her alone."],
        ["I will work for my shelter, not sell my shame.", "Take the wage only when the work is real.", "I can help if you let me stand on my own feet."],
        ["I refuse to hide the work my hands can prove.", "Watch what this object remembers.", "If you trust me, don't ask me to become small again."],
        ["Stop the spectacle before someone else pays for your pride.", "I can prove the flaw if you give me the bench.", "Power built on someone else's hands always leaves a mark."],
        ["I did not take it. Let me prove who did.", "Do not mistake survival for consent.", "You can chain my name, but you can't make the evidence obey you."],
        ["Help me, but do not take the proof from my hands.", "I choose the risk because silence costs more.", "The object remembers what power overlooked."],
        ["I choose the room, the witnesses, and the questions.", "If you want forgiveness, change what you do before you ask for trust.", "Give me back the proof and I will show you the truth."],
        ["This floor is not punishment anymore. Everyone sits by choice.", "I refuse revenge without repair.", "We save the legacy by opening the doors, not by becoming the cage."],
    ]
    key_lines = line_options[index - 1]
    first_image_override = None
    final_image_override = None
    sound_override = None
    spoken_exchange = []
    scene_rhythm = "enter inside pressure, compress the objection into a concrete unsafe choice, let the protagonist answer through behavior, then end on proof/cost rather than explanation"
    rewrite_directives = [
        "make pressure procedural and specific rather than generically cruel",
        "let the protagonist answer through action or refusal rather than theme explanation",
        "end on visible proof, cost, or changed access instead of explanation",
    ]
    opposition_beats = [
        {"beat": "external_pressure", "voice": "antagonist or social crowd", "dramatic_job": turn, "writing_note": "pressure must be specific behavior, not generic cruelty"},
        {"beat": "witness_objection", "voice": "caregiver, worker, or vulnerable witness", "dramatic_job": relationship, "writing_note": "the objection should make the safe choice reasonable"},
        {"beat": "protagonist_decision", "voice": "protagonist", "dramatic_job": sequence.get("protagonist_choice", "act despite cost"), "writing_note": "the answer is a choice or refusal, not a theme statement"},
        {"beat": "evidence_or_cost", "voice": "object, proof, or consequence", "dramatic_job": clue, "writing_note": "the scene must leave a visible cost or proof implication"},
    ]
    if premise.get("channel_contract") == "creature_economic_melodrama":
        contract_text = json.dumps(premise, ensure_ascii=False).lower()
        heat_based = any(term in contract_text for term in ["oven", "ember", "fire", "coal", "volcanic"])
        resource = "fire" if heat_based else "water"
        system = "oven" if heat_based else "pump"
        evidence = "heat" if heat_based else "salt"
        authority = "coal guild" if heat_based else "land trust"
        trait = "feathers" if heat_based else "fins"
        object_term = str(object_name).lower()
        raw_child = str(premise.get("emotional_engine", {}).get("protective_counterforce", "the creature child"))
        creature = raw_child.split(" plus ")[0].split(";")[0].split(", whose")[0].strip() or "the creature child"
        raw_care = str(premise.get("relational_contract", {}).get("safety_or_kindness_before_power", "the caregiver"))
        caregiver = re.split(r"\s+(?:offers?|feeds?|gives?|shelters?)\s+", raw_care, maxsplit=1)[0].split(";")[0].split(" and ")[0].strip() or "the caregiver"
        creature_label = creature[:1].upper() + creature[1:]
        caregiver_label = caregiver[:1].upper() + caregiver[1:]
        protagonist_identity = str(premise.get("protagonist", {}).get("identity", "the protagonist"))
        protagonist_name = protagonist_identity.split(",")[0].strip() or "the protagonist"
        dialogue_materials = creature_dialogue_materials({
            "creature": creature,
            "creature_label": creature_label,
            "caregiver": caregiver,
            "authority": authority,
            "protagonist_name": protagonist_name,
            "object_term": object_term,
            "resource": resource,
            "system": system,
            "evidence": evidence,
            "trait": trait,
            "heat_based": heat_based,
        }, index)
        key_lines = dialogue_materials["key_lines"]
        spoken_exchange = dialogue_materials["spoken_exchange"]
        scene_rhythm = dialogue_materials.get("scene_rhythm")
        rewrite_directives = dialogue_materials.get("rewrite_directives") or []
        creature_opposition = [
            {"pressure": f"the crowd or {authority} demands that the humiliated protagonist abandon the exposed child", "objection": f"hiding {creature} can destroy the protagonist's last economic shelter", "decision": "the protagonist hides/protects before knowing whether anyone will help", "evidence_or_cost": f"the {resource} response marks {creature} as a witness rather than a commodity"},
            {"pressure": "shelter is offered in a way that could become debt, pity, or control", "objection": f"{caregiver} needs labor and honesty, not ownership of the creature", "decision": "the protagonist accepts work but refuses to monetize suffering", "evidence_or_cost": f"the {object_term} separates access from possession"},
            {"pressure": f"the {authority} repeats the public punishment and prices the creature's pain", "objection": f"selling even a little of {creature}'s value could solve the debt faster", "decision": "the protagonist chooses slower safety over profitable harm", "evidence_or_cost": f"fear, {trait}, and {evidence} make exploitation physically visible"},
            {"pressure": f"the {authority} reframes competence as theft or illegality", "objection": "one honest witness is safer than a dramatic public claim", "decision": "the protagonist protects consent before economic rescue", "evidence_or_cost": f"the {system} creates timestamps, pressure marks, or access traces"},
            {"pressure": "public accusation converts the creature into evidence and the protagonist into a thief", "objection": f"revealing {creature} may prove innocence while causing capture", "decision": "the protagonist protects the child before protecting reputation", "evidence_or_cost": f"the {object_term} falls open as proof but does not complete the chain"},
            {"pressure": "waiting for rescue would leave both truth and creature inside institutional control", "objection": "help is needed, but help can steal authorship of the proof", "decision": "the protagonist accepts accountable help while keeping control of the evidence", "evidence_or_cost": f"ledger timing, {evidence}, pressure marks, and witness geometry begin aligning"},
            {"pressure": "forgiveness or rescue is offered before restitution", "objection": "a public win without consent repair would turn the creature into a trophy", "decision": "the protagonist demands return of what papers/power stole before trust", "evidence_or_cost": f"the proof chain shows fraud and makes {creature}'s choice audible/visible"},
            {"pressure": "the ending could become possession, revenge, or escape-only relief", "objection": "community survival matters more than punishing one villain", "decision": "the protagonist chooses non-possessive belonging after safety and proof", "evidence_or_cost": f"the transformed {system} space visibly shares or rebuilds access to {resource}"},
        ]
        beat = creature_opposition[index - 1]
        opposition_beats = [
            {"beat": "external_pressure", "voice": authority, "dramatic_job": beat["pressure"], "writing_note": "pressure should arrive as a demand, payment, threat, or institutional move"},
            {"beat": "witness_objection", "voice": caregiver if index in (1, 2, 6, 8) else creature, "dramatic_job": beat["objection"], "writing_note": "the objection makes the safe choice reasonable and forces a cost"},
            {"beat": "protagonist_decision", "voice": "protagonist", "dramatic_job": beat["decision"], "writing_note": "decision is spoken through action/refusal, not theme explanation"},
            {"beat": "evidence_or_cost", "voice": object_name, "dramatic_job": beat["evidence_or_cost"], "writing_note": "end the scene with visible proof implication or irreversible cost"},
        ]
        if heat_based:
            material_motif = "blackened brass key clicks, ember breath, wing-feather tremor, and oven stone resonance"
            resource_texture = "fire crackle, coal shift, oven-door metal, warm bakery labor"
        else:
            material_motif = "blue glass vial taps, salt grains, water droplets, fin movement, and pump-stone resonance"
            resource_texture = "water droplets, pump pressure, wet stone, and shared-food labor"
        creature_sound = [
            ("public clatter and accusation thin until creature breath, infant-like movement, and the first object touch remain audible", "no heroic score yet; let the protection choice register as close breath and contact before music enters"),
            (resource_texture + " replace crowd noise as care becomes labor", "music may form a small rhythmic motif only after work/shelter becomes chosen rather than charitable"),
            ("institutional chains, coin counts, ledger paper, and hostile murmur press against small creature fear sounds", "keep the creature's fear acoustically close while power remains reverberant and distant"),
            ("practical repair textures and system mechanics carry competence; guild/customer murmur interrupts rhythm", "use sound interruptions to show the antagonist converting competence into threat"),
            ("public noise drops into room tone, heartbeat, cloth movement, and the object striking stone", "music must withhold resolution during accusation so shame remains spatial and bodily"),
            ("paper, pressure ticks, measurement scratches, witness whispers, and repeated object handling build the proof chain", "let investigation rhythm replace battle music; each proof layer should have a distinct tactile sound"),
            ("near-silent proof assembly: each ledger, trace, witness, and object placement lands as a separate acoustic event", "a restrained motif can answer earlier care sounds but must not become triumph before consent repair"),
            (resource_texture + " open into communal rhythm while the original public-humiliation sound returns transformed", "the ending motif resolves because home, consent, and shared survival are visible, not because the score insists they are resolved"),
        ]
        negative_space, music_function = creature_sound[index - 1]
        sound_override = {
            "dialogue_priority": "close dialogue remains intelligible beneath crowd, labor, weather, or institutional texture; creature/child breath and contact sounds remain specific rather than generic cute noise",
            "music_function": music_function,
            "silence_or_negative_space": negative_space,
            "motif": material_motif,
        }
        if "key" in object_term:
            unlock_action = f"the protagonist turns the {object_term} in the {system} lock and compares its maker mark with the first {evidence} trace"
            dropped_evidence = f"the {object_term} drops beside the exposed ledger seam as evidence"
            final_public_proof = f"the {system} ledger wall remains unlocked while the {object_term} stays visible as public proof"
        else:
            unlock_action = f"the protagonist opens the {object_term} and compares its mark with the first {evidence} trace"
            dropped_evidence = f"the {object_term} falls open as evidence"
            final_public_proof = f"the {object_term} remains open as public proof"
        creature_visuals = [
            (f"the crowd watches the protagonist being barred from the public {system} as {creature} crosses toward her", f"the protagonist kneels, hides {creature}, and closes a protective hand around the {object_term}"),
            (f"{caregiver} carries food into the shelter while the protagonist refuses payment for pain", f"the protagonist places the {object_term} beside {creature} instead of selling access to it"),
            (f"the antagonist's people chain the public {system} while {creature} shakes behind the protagonist", unlock_action),
            (f"the protagonist repairs a small {system} fault while guild/customer witnesses watch", f"she pockets a marked ledger fragment and carries {creature} away from the offer of sale"),
            (f"guards force the protagonist before the public {system} as the accusation lands", f"she shields {creature} with her body while {dropped_evidence}"),
            (f"the protagonist lifts the {object_term} over the work surface and reads pressure, timing, and witness geometry", f"the care network carries matched proof pieces toward the public hearing"),
            (f"the protagonist lays ledger, {evidence} trace, witness statement, and {object_term} in one line", f"{creature} steps forward by choice as the protagonist refuses to claim ownership"),
            (f"neighbors carry shared {resource} into the transformed {system} space", f"{creature} crosses the home threshold freely while {final_public_proof}"),
        ]
        first_image_override, final_image_override = creature_visuals[index - 1]
    if premise.get("channel_contract") == "compressed_creature_survival":
        survival_materials = compressed_survival_scene_materials(premise, index)
        key_lines = survival_materials["key_lines"]
        spoken_exchange = survival_materials["spoken_exchange"]
        scene_rhythm = survival_materials["scene_rhythm"]
        rewrite_directives = survival_materials["rewrite_directives"]
        opposition_beats = survival_materials["opposition_beats"]
        sound_override = survival_materials["sound_override"]
        first_image_override = survival_materials["first_image"]
        final_image_override = survival_materials["final_image"]
    first_image = first_image_override or visual
    final_image = final_image_override or f"{object_name} visible after the power shift, its meaning altered by: {clue}"
    power_start = POWER_START[index - 1]
    power_end = POWER_END[index - 1]
    subtext = SUBTEXT[index - 1]
    if premise.get("channel_contract") == "compressed_creature_survival":
        power_start = survival_materials["power_start"]
        power_end = survival_materials["power_end"]
        subtext = survival_materials["subtext"]
    return {
        "scene_id": f"S{index:02d}",
        "time_range": sequence.get("time_range", "0-0 minutes"),
        "objective": function,
        "conflict": turn,
        "power_position_start": power_start,
        "power_position_end": power_end,
        "turn": turn,
        "protagonist_decision": sequence.get("protagonist_choice", "act despite social cost"),
        "subtext": subtext,
        "visual_action": {
            "first_image": first_image,
            "face_reaction": f"the protagonist's expression shifts from {emotional_shift.split(' to ')[0]} toward controlled attention when the turn lands",
            "vertical_composition": "vulnerable or morally important figures remain visually legible while status power occupies height, threshold, or audience control",
            "final_image": final_image,
        },
        "dialogue_design": {
            "function": "make choices, objections, and proof implications audible rather than explaining theme",
            "subtext_rule": "characters negotiate status, debt, permission, blame, and care; they rarely name the theme directly",
            "max_exposition_sentences": 2,
            "key_lines": key_lines,
            "opposition_beats": opposition_beats,
            "spoken_exchange": spoken_exchange,
            "scene_rhythm": scene_rhythm,
            "rewrite_directives": rewrite_directives,
        },
        "sound_design": {
            "dialogue_priority": (sound_override or {}).get("dialogue_priority", "close dialogue remains intelligible beneath crowd, labor, weather, or institutional texture"),
            "music_function": (sound_override or {}).get("music_function", "music enters only when relational power changes; it must not paper over unresolved tension"),
            "silence_or_negative_space": (sound_override or {}).get("silence_or_negative_space", sound),
            "motif": (sound_override or {}).get("motif", motif),
        },
        "edit_hook": {
            "entry_hook": f"enter on the immediate consequence of the previous turn: {relationship}",
            "exit_hook": hook,
        },
        "failure_checks": [
            "Does the scene change power, trust, evidence, capability, or relational obligation?",
            "Is the object/space doing narrative work rather than decorative worldbuilding?",
            "Is public or institutional pressure expressed through visible behavior rather than exposition?",
            "Does the protagonist retain agency instead of being rescued into passivity?",
        ],
    }


def generate_scenes(premise: dict[str, Any], architecture: dict[str, Any]) -> list[dict[str, Any]]:
    return [scene_from_sequence(seq, premise, i + 1) for i, seq in enumerate(architecture.get("sequences", []))]


def write_scenes(premise_path: Path, architecture_path: Path, output_dir: Path) -> list[dict[str, Any]]:
    premise = json.loads(premise_path.read_text(encoding="utf-8"))
    architecture = json.loads(architecture_path.read_text(encoding="utf-8"))
    scenes = generate_scenes(premise, architecture)
    output_dir.mkdir(parents=True, exist_ok=True)
    for scene in scenes:
        (output_dir / f"{scene['scene_id']}.json").write_text(json.dumps(scene, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return scenes
