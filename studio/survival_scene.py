"""Scene-level materials for compressed visual-first creature-survival packages."""
from __future__ import annotations

from typing import Any


def compressed_survival_scene_materials(premise: dict[str, Any], index: int) -> dict[str, Any]:
    surv = premise.get("survival_engine", {})
    predator = surv.get("predator", "the predator")
    vehicle = surv.get("vehicle_or_station", "the wrecked vehicle")
    animal = surv.get("innocent_animal", "the small animal")
    ally = surv.get("ally_creature", "the creature ally")
    occupation = surv.get("occupation", "professional")
    object_name = premise.get("meaning_carrier", {}).get("object_or_space", "the survival tool")
    protagonist = str(premise.get("protagonist", {}).get("identity", "the protagonist")).split(",", 1)[0]

    power_positions = [
        ("controlled professional routine", "injured survivor with protective duty"),
        ("hunted and territorially powerless", "observant survivor learning the predator rule"),
        ("terrified of every giant creature", "cautious participant in a creature alliance"),
        ("escape-focused and exposed", "emotionally committed protector"),
        ("able to escape but morally implicated", "rescue-obligated plan witness"),
        ("outmatched by the predator", "occupational author of the rescue mechanism"),
        ("physically exposed inside the trap", "sacrificial controller of the release moment"),
        ("survivor with unresolved guilt", "recognized protector inside chosen survival community"),
    ]
    subtexts = [
        "Care means reaching vulnerable life before answers are available.",
        "Survival knowledge comes from watching the threat instead of dominating it.",
        "Not every powerful creature carries the same moral meaning.",
        "Small acts of care cost time but create direction, trust, and identity.",
        "Escape without rescue would repeat the original guilt wound.",
        "Professional identity becomes agency when it converts wreckage into a plan.",
        "Learned restraint can defeat force when the predator's rule is understood.",
        "Survival becomes belonging only when recognition and reciprocal rescue land.",
    ]
    key_lines_by_scene = {
        1: ["Stay behind me.", "What hit us?"],
        2: [],
        3: ["Easy. I won't hurt you."],
        4: [],
        5: ["They're alive. We save them."],
        6: ["The light can hold it. Help me keep the line open."],
        7: [],
        8: ["I was wrong about them.", "They saved us. We take everyone home."],
    }
    spoken_exchange_by_scene = {
        1: [
            ("evidence_or_cost", "injured survivor", "What hit us?", "the survivor looks up through dust and debris", "fear needs orientation before courage", "fractured, breathless"),
            ("protagonist_decision", protagonist, "Stay behind me.", f"{protagonist} steps between the survivor and the shifting wreck", "protection becomes responsibility before understanding", "low, immediate"),
        ],
        3: [
            ("protagonist_decision", protagonist, "Easy. I won't hurt you.", f"{protagonist} lowers her hand and light rather than reaching for a weapon", "restraint is the first proof of safety", "quiet, careful"),
        ],
        5: [
            ("protagonist_decision", protagonist, "They're alive. We save them.", f"{protagonist} counts the trapped bodies and turns back toward the nest entrance", "escape becomes rescue through choice", "whispered, hard"),
        ],
        6: [
            ("protagonist_decision", protagonist, "The light can hold it. Help me keep the line open.", f"{protagonist} braces the mechanism while pointing to the open path", "competence becomes shared action without surrendering authorship", "urgent, precise"),
        ],
        8: [
            ("witness_objection", "doubtful survivor", "I was wrong about them.", "the survivor looks from the rescued animal to the freed creature ally", "the apology admits misreading vulnerable life", "quiet, ashamed"),
            ("protagonist_decision", protagonist, "They saved us. We take everyone home.", f"{protagonist} opens the final path instead of claiming the creature ally", "recognition becomes shared rescue rather than possession", "steady, warm"),
        ],
    }
    exchange = []
    for beat, speaker, line, action, subtext, delivery in spoken_exchange_by_scene.get(index, []):
        exchange.append({
            "beat": beat,
            "speaker": speaker,
            "line": line,
            "action": action,
            "subtext": subtext,
            "power_move": "practical survival pressure answered through protection, restraint, rescue, or recognition",
            "listening_response": "the next action answers the immediate bodily danger rather than explaining theme",
            "delivery": delivery,
            "status_shift": "the speaker converts fear or doubt into a concrete survival obligation",
            "room_sound": "breath, debris, creature texture, machinery, weather, and animal vocalization remain present beneath the sparse line",
        })
    pressure_objection_decision_cost = [
        (
            "the wreck keeps shifting while injured people and animals remain exposed",
            "escaping the visible danger may mean abandoning survivors who cannot move",
            f"{protagonist} chooses immediate reach/protection before understanding the whole threat",
            f"{object_name} and {animal} become established as functional survival signs rather than decoration",
        ),
        (
            f"{predator} controls the terrain through scale, speed, and sensory advantage",
            "running blindly may trigger the exact sense the predator hunts by",
            f"{protagonist} protects {animal} while learning the predator rule through observation",
            "the predator's repeated behavior establishes a readable rule the climax can pay off",
        ),
        (
            f"{ally} is large enough to be misread as another monster",
            "killing or fleeing every creature would destroy the first possible ally",
            f"{protagonist} risks stillness and gentle contact before expecting help",
            f"{ally} responds to light/wound/texture/behavior connected to {object_name}",
        ),
        (
            "predator proximity makes every second spent caring feel dangerous",
            f"{animal} cannot yet repay rescue and slowing down may cost escape",
            f"{protagonist} frees, warms, feeds, or protects {animal} anyway",
            f"{animal} notices a path, sound, or behavior that points toward survivors",
        ),
        (
            "the nest/cave/structure proves the predator has been collecting living victims",
            "escape alone is still possible, but it would repeat the opening guilt",
            f"{protagonist} turns escape into rescue and memorizes the spatial layout",
            f"survivors and {ally} are visible as living rescue obligations rather than abstract stakes",
        ),
        (
            f"preparing {vehicle} requires noise, light, heat, or movement that can attract {predator}",
            "a failed test may waste the only working mechanism",
            f"{protagonist} uses {occupation} knowledge to convert wreckage into a controlled trap/rescue system",
            f"{object_name} becomes the key operating part of the final mechanism",
        ),
        (
            f"{predator} enters the trap space before every captive is safe",
            "staying exposed may cost the protagonist her own escape",
            f"{protagonist} holds position long enough for the object/mechanism sequence to fire",
            f"{ally} helps only through established creature behavior while the mechanism redirects {predator}",
        ),
        (
            "survival relief could end the story before the relational wound is repaired",
            "the rescued group may still treat the animal/creature as expendable unless behavior changes",
            f"{protagonist} chooses contact, release, and shared survival rather than ownership or revenge",
            f"{object_name} remains visible in the transformed rescue shelter as proof of competence and care",
        ),
    ]
    pressure, objection, decision, cost = pressure_objection_decision_cost[index - 1]
    opposition_beats = [
        {"beat": "external_pressure", "voice": predator if index in (2, 5, 7) else "disaster terrain", "dramatic_job": pressure, "writing_note": "pressure is spatial, sensory, mechanical, or creature behavior rather than villain exposition"},
        {"beat": "witness_objection", "voice": animal if index in (1, 2, 4, 5) else ally, "dramatic_job": objection, "writing_note": "the objection is embodied by vulnerability, hesitation, warning, or creature behavior"},
        {"beat": "protagonist_decision", "voice": protagonist, "dramatic_job": decision, "writing_note": "the decision must be visible through action before any sparse dialogue validates it"},
        {"beat": "evidence_or_cost", "voice": object_name, "dramatic_job": cost, "writing_note": "end with changed access, proof, injury, creature response, or a plan component rather than explanation"},
    ]

    visual_pairs = [
        (
            f"the role/vehicle/location contract reads instantly: {vehicle} breaking apart under the disaster",
            f"{protagonist} reaches {animal} while {object_name} catches a first meaningful glint in the wreckage",
        ),
        (
            f"{predator} fills the frame behind or above the small protagonist and animal",
            f"{protagonist} freezes or hides as the predator repeats the sensory behavior she must later exploit",
        ),
        (
            f"{ally} emerges at giant scale but injured, hesitant, or reactive rather than simply attacking",
            f"{protagonist}'s open hand or light touches the creature's boundary without capturing it",
        ),
        (
            f"{animal} trembles in wire, cloth, water, dust, or darkness while danger remains off-screen but audible",
            f"{protagonist} releases/protects it and notices the path or behavior it has been trying to reveal",
        ),
        (
            "the nest/cave interior opens as a living map of victims, webs, shells, cages, tunnels, or root-like structures",
            f"{protagonist} sees survivors and {ally} alive but trapped, then withdraws before the predator cycle returns",
        ),
        (
            f"{protagonist} crawls through {vehicle}, opens panels, pulls wires, braces doors, and tests improvised light or sound barriers",
            f"{object_name} locks into the mechanism and the first controlled test flashes/sounds through the wreck",
        ),
        (
            f"{protagonist} lures {predator} into the vehicle/station geometry as light, smoke, sparks, water, or sound transforms the space",
            f"{protagonist} holds the control position while {ally} and the captives move through the opened path",
        ),
        (
            "freed survivors emerge through the opened threshold into environmental air",
            f"{ally} leaves or chooses contact freely while {object_name} remains visible in the transformed rescue shelter",
        ),
    ]
    sound_pairs = [
        (
            "impact metal, debris, wind/water, alarm remnants, breath, and small animal distress; no musical explanation",
            "brief silence after impacts lets the audience locate bodies, animal sound, and the first object glint",
        ),
        (
            "predator scraping, stepping, clicking, shell/armor movement, low air pressure, and close breathing",
            "held silence before each predator reaction makes its sensory rule readable",
        ),
        (
            "hostile creature texture softens into wing/skin/shell movement, exhausted breath, and environmental tone",
            "the alliance forms in shared breathing and reduced movement rather than dialogue",
        ),
        (
            "tiny animal vocalization, cloth/wire/water texture, wind or cave tone, footsteps, and close breath at the quietest density",
            "music withdraws so care is audible as time lost and risk accepted",
        ),
        (
            "muffled living bodies, web/cave resonance, distant predator rhythm, dripping or structural creaks, suppressed breath",
            "the protagonist's realization lands in near silence before the rescue decision",
        ),
        (
            "mechanical clicks, electrical charge, tool rhythm, metal stress, cloth movement, and brief failed-test silence",
            "sound rhythm turns preparation into suspense rather than montage noise",
        ),
        (
            "creature mass, machine crescendo, alarm/light hum, impact debris, breath, then one decisive mechanical click or silence",
            "the loudest spectacle pauses around the exact release decision so causality is readable",
        ),
        (
            "machine noise falls away into breath, environmental air, creature contact, freed movement, and sparse validation dialogue",
            "the ending resolves because contact and return are visible, not because score declares triumph",
        ),
    ]
    music_function, negative_space = sound_pairs[index - 1]
    first_image, final_image = visual_pairs[index - 1]
    return {
        "key_lines": key_lines_by_scene[index],
        "spoken_exchange": exchange,
        "scene_rhythm": "visual objective first; sparse dialogue only validates choices after action, creature behavior, or mechanical proof has already made them legible",
        "rewrite_directives": [
            "write objectives that remain understandable with sound off",
            "use creature behavior, terrain, tools, animal reaction, and occupational action instead of exposition",
            "allow breath, silence, machinery, and small animal sound to carry emotion before score",
            "keep any spoken line short, practical, and subordinate to the visual decision",
        ],
        "opposition_beats": opposition_beats,
        "first_image": first_image,
        "final_image": final_image,
        "power_start": power_positions[index - 1][0],
        "power_end": power_positions[index - 1][1],
        "subtext": subtexts[index - 1],
        "sound_override": {
            "dialogue_priority": "dialogue is sparse and practical; breath, creature texture, machinery, weather, footsteps, and animal vocalization carry most narrative information",
            "music_function": music_function,
            "silence_or_negative_space": negative_space,
            "motif": f"{object_name} clicks/scrapes, predator texture, small animal vocalization, and mechanical air/light rhythm",
        },
    }
