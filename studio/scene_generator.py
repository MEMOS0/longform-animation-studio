"""Generate first-pass scene screenplay units from story architecture.

These scenes are structured creative scaffolds: they preserve causality, power
change, subtext, sound negative space, and edit hooks so a later writing/directing
pass can deepen them rather than inventing structure from nothing.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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
    if premise.get("channel_contract") == "creature_economic_melodrama":
        contract_text = json.dumps(premise, ensure_ascii=False).lower()
        heat_based = any(term in contract_text for term in ["oven", "ember", "fire", "coal", "volcanic"])
        resource = "fire" if heat_based else "water"
        system = "oven" if heat_based else "pump"
        evidence = "heat" if heat_based else "salt"
        authority = "coal guild" if heat_based else "land trust"
        trait = "feathers" if heat_based else "fins"
        object_term = str(object_name).lower()
        creature_lines = [
            ["Eat first. We can count what it costs after she is safe.", "No one is selling her pain tonight.", f"If the {resource} remembers her, we follow the {resource}."],
            ["I will work for shelter, but I will not make her suffer for coins.", f"The {object_term} proves access, not ownership.", f"We eat because someone shared before profit, not because the {authority} permits it."],
            ["Look at her fear before you look at her price.", "If her pain can buy the house, the price is wrong.", f"She is not inventory with {trait}."],
            [f"Your ledger can lie; {evidence} cannot.", "Give me one honest customer before you call me a thief.", f"The {system} remembers who opened it."],
            [f"I did not steal {resource}. I saved a child you wanted to harvest.", "Do not mistake desperation for consent.", "You can freeze the deed, but not the evidence under the stone."],
            ["Help me carry the proof, but do not carry my choice.", "I choose the road because waiting makes us property.", f"The {object_term} remembers what the {authority} buried."],
            ["She belongs to no one, and neither do I.", "If you want forgiveness, return what your papers stole.", f"Let the {resource} answer before the law does."],
            [f"This {system} is not a cage anymore. Everyone eats by choice.", "I refuse rescue that becomes ownership.", "We keep the doors open because she taught us power is not ownership."],
        ]
        key_lines = creature_lines[index - 1]
    return {
        "scene_id": f"S{index:02d}",
        "time_range": sequence.get("time_range", "0-0 minutes"),
        "objective": function,
        "conflict": turn,
        "power_position_start": POWER_START[index - 1],
        "power_position_end": POWER_END[index - 1],
        "turn": turn,
        "protagonist_decision": sequence.get("protagonist_choice", "act despite social cost"),
        "subtext": SUBTEXT[index - 1],
        "visual_action": {
            "first_image": visual,
            "face_reaction": f"the protagonist's expression shifts from {emotional_shift.split(' to ')[0]} toward controlled attention when the turn lands",
            "vertical_composition": "vulnerable or morally important figures remain visually legible while status power occupies height, threshold, or audience control",
            "final_image": f"{object_name} visible after the power shift, its meaning altered by: {clue}",
        },
        "dialogue_design": {
            "function": "make choices, objections, and proof implications audible rather than explaining theme",
            "subtext_rule": "characters negotiate status, debt, permission, blame, and care; they rarely name the theme directly",
            "max_exposition_sentences": 2,
            "key_lines": key_lines,
        },
        "sound_design": {
            "dialogue_priority": "close dialogue remains intelligible beneath crowd, labor, weather, or institutional texture",
            "music_function": "music enters only when relational power changes; it must not paper over unresolved tension",
            "silence_or_negative_space": sound,
            "motif": motif,
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
