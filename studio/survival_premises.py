"""Compressed visual-first creature-survival premise variants.

These packages transfer the Neural Pictures mechanism into original premises:
role/creature/location contract, early disaster, moral creature differentiation,
occupational competence, quiet animal care, reciprocal rescue, and vehicle/station
reversal. They are creative starting points, not copies of reference plots.
"""
from __future__ import annotations

from typing import Any

COMPRESSED_SURVIVAL_VARIANTS = [
    {
        "id": "brakelight_moth_depths",
        "setting": "a storm-cut mountain railway where a night inspection train has crashed inside abandoned mineral tunnels",
        "protagonist": "Ilsa, a young freight conductor who knows the train's brakes, couplers, radio, and emergency light circuits",
        "occupation": "freight conductor",
        "vehicle_or_station": "the wrecked inspection train and its working brake-light/horn system",
        "predator": "a tunnel-sized centipede with a black glass shell",
        "predator_short": "Giant Centipede",
        "innocent_animal": "a trapped railway pigeon with a red leg band",
        "ally_creature": "a dust-blue giant moth whose wings react to light",
        "object": "cracked red brake-light lens",
        "opening_object_meaning": "the lens is a routine safety part Ilsa almost discards while checking the train",
        "closing_object_meaning": "the same lens focuses the train lamp into a light path that lures the centipede away from the survivors",
        "status_space": "Ilsa is thrown from the cab as the inspection train derails inside the tunnel mouth",
        "inversion_space": "the wrecked train transformed from crash site into a lighted rescue shelter",
        "public_wound": "she believes the crash means she failed every passenger entrusted to her",
        "proof_chain": "red lens fracture, headlamp circuit, moth wing reflection, centipede shell scratches, coupler position, and the pigeon's leg-band path through the tunnel",
        "return_home": "the freed moth carries its young back into the high cave dark while the survivors follow the train light out",
        "bond": "a frightened apprentice who resented the pigeon admits that the animal's path saved them",
    },
    {
        "id": "foghorn_turtle_keeper",
        "setting": "a tidal lighthouse station cut off after a supply ferry wrecks on black rock flats",
        "protagonist": "Noor, a lighthouse radio operator who knows the foghorn, lens room, tide charts, and ferry emergency panels",
        "occupation": "lighthouse radio operator",
        "vehicle_or_station": "the stranded ferry hull and the lighthouse foghorn/lens mechanism",
        "predator": "a barnacle-armored giant crab that hunts through tidal channels",
        "predator_short": "Giant Crab",
        "innocent_animal": "an injured seabird chick tangled in radio wire",
        "ally_creature": "an ancient leatherback turtle carrying moss and shell scars",
        "object": "bent brass foghorn valve key",
        "opening_object_meaning": "the key is a maintenance tool Noor uses as routine maintenance before the wreck",
        "closing_object_meaning": "the same key opens the foghorn line that drives the crab into the tide gate and frees trapped passengers",
        "status_space": "Noor is knocked against the radio desk as the ferry breaks apart outside the lighthouse",
        "inversion_space": "the dead lighthouse transformed into a sounding beacon guiding survivors and sea creatures home",
        "public_wound": "she blames herself for transmitting the wrong tide window before the ferry struck the rocks",
        "proof_chain": "foghorn valve timing, tide chart, turtle shell scrape, crab claw marks, ferry panel light, and the seabird chick's nest location",
        "return_home": "the turtle returns to open water with the seabird chick safe on its mossy shell",
        "bond": "the ferry mate who dismissed the seabird as a nuisance helps carry it to the turtle before apologizing",
    },
]


def compressed_survival_premise(v: dict[str, str], target_minutes: float = 18) -> dict[str, Any]:
    name = v["protagonist"].split(",", 1)[0]
    compressed = target_minutes <= 35.5
    return {
        "premise_id": v["id"],
        "title_candidates": [
            f"The {v['occupation'].title()} vs. the {v['predator_short']} — Full Survival Movie",
            "She Survived the Crash — Then the Creature Led Her Back",
            "Nobody Believed the Small Animal Mattered — Until It Saved Them All",
        ],
        "logline": f"After a violent wreck in {v['setting']}, {name} must use {v['occupation']} knowledge, {v['object']}, and trust in vulnerable creatures to rescue survivors from {v['predator']}.",
        "audience_promise": "A compressed visual-first creature-survival film: immediate disaster, giant predator readability, innocent animal stakes, morally differentiated creatures, occupational problem-solving, quiet care, trap preparation, rescue closure, and minimal dialogue.",
        "target_minutes": target_minutes,
        "release_format": "short_feature" if compressed else "mid_length_feature",
        "channel_contract": "compressed_creature_survival",
        "survival_engine": {
            "occupation": v["occupation"],
            "vehicle_or_station": v["vehicle_or_station"],
            "predator": v["predator"],
            "innocent_animal": v["innocent_animal"],
            "ally_creature": v["ally_creature"],
            "rescue_inversion": "escape becomes rescue when captives and the allied creature are found alive but trapped",
        },
        "emotional_engine": {
            "wound": f"{name} believes the wreck proves she failed the people and animals under her care.",
            "want": "survive the predator territory and reach safety",
            "need": "accept that care, humility, and reciprocal rescue matter more than escaping alone or proving invulnerability",
            "injustice": "the disaster is not a human villain's plot; the cruelty is exposure, predation, injury, and the temptation to abandon weaker lives",
            "protective_counterforce": f"{v['innocent_animal']} and {v['ally_creature']} create trust through vulnerability rather than speech",
            "belonging_payoff": f"the wrecked space becomes {v['inversion_space']}; {v['return_home']}",
            "secret_or_power_asymmetry": "the predator owns the terrain while the protagonist owns only professional knowledge, tools, and attention to vulnerable life",
            "cost_of_failure": "survivors remain trapped, the innocent animal is abandoned, the creature ally is captured, and the protagonist escapes with guilt instead of home",
        },
        "protagonist": {
            "identity": v["protagonist"],
            "vulnerability": "injury, isolation, guilt, limited weapons, and dependence on terrain she cannot control",
            "capability": f"{v['occupation']} competence, mechanical improvisation, observation of animal behavior, and refusal to abandon weaker lives",
            "agency_first_action": f"she protects or frees {v['innocent_animal']} before understanding how it can help her",
            "transformation": "from guilty survivor to rescue author who reads the ecosystem instead of dominating it",
        },
        "opening_event": {
            "first_10_seconds": v["status_space"],
            "first_60_seconds": "the disaster becomes physically undeniable; the first injury, animal distress, or survivor separation is visible before any explanation.",
            "first_5_minutes": f"{v['predator']} appears in scale relation to the protagonist; {v['innocent_animal']} and the first sign of {v['ally_creature']} establish that the ecosystem is morally differentiated.",
            "dramatic_question": "can she turn professional knowledge and care for vulnerable creatures into rescue before the predator owns the terrain?",
        },
        "theme_lane": {
            "family_or_heir_hook": "innocent animal protection and reciprocal creature rescue",
            "romance_hook": v["bond"],
            "modern_power_hook": "occupational competence, disaster machinery, visual survival problem-solving, and creature ecology",
        },
        "failure_intelligence": {
            "evaluation_path": "pending_generated_evaluation",
            "nearest_failures": [
                "monster spectacle without emotional differentiation",
                "escape-only ending that abandons the animal/creature relationship",
                "professional identity used as costume rather than survival mechanism",
                "continuous noise/action with no quiet care hinge",
            ],
            "mitigations": [
                "pay the role/creature/location contract within two minutes",
                "keep every objective legible with sound off",
                "make the opening vehicle or station become the final trap/rescue machine",
                "use silence, breath, creature texture, and small animal contact after the first pursuit",
                "reveal captives or the allied creature in danger so escape becomes reciprocal rescue",
            ],
            "counterexamples_checked": [
                "high-performing compressed creature films can contain visible AI artifacts; polish alone does not explain performance",
                "giant scale alone is insufficient unless tied to care, vulnerability, or rescue",
                "sparse dialogue is a format choice, not permission for thin causality",
            ],
        },
        "packaging": {
            "thumbnail_single_read": f"{name} in occupational costume fleeing or standing before {v['predator']}, with {v['vehicle_or_station']} and scale contrast instantly visible",
            "curiosity_gap": f"how can a {v['occupation']} survive a creature that owns the terrain?",
            "visual_before_after": f"wrecked vehicle/station becomes {v['inversion_space']}; {v['object']} changes from routine tool into rescue mechanism",
            "title_thumbnail_mismatch_risk": "generic monster packaging would hide the stronger occupational-care-rescue mechanism",
        },
        "evidence_boundaries": [
            "Inspired by mechanism-level evidence in compressed creature-survival research; characters, species mix, vehicle, object, and rescue chain are original.",
            "No CTR, retention, or traffic causality is claimed from public video metadata.",
        ],
        "meaning_carrier": {
            "object_or_space": v["object"],
            "opening_meaning": v["opening_object_meaning"],
            "closing_reversal": v["closing_object_meaning"],
            "final_sequence_use": f"the object operates the final light/sound/trap mechanism before the rescued group reaches {v['inversion_space']}",
        },
        "relational_contract": {
            "power_asymmetry": "predator-controlled terrain versus an injured professional with only knowledge, tools, and attention to vulnerable life",
            "safety_or_kindness_before_power": f"{name} frees or protects {v['innocent_animal']} before knowing it can guide, prove, or save anyone",
            "costly_protagonist_action": f"she turns back toward the predator territory to free captives and {v['ally_creature']} instead of escaping alone",
            "consent_or_personhood_repair": "the allied creature is never commanded as a weapon; it chooses contact or return freely, and survivors repair their earlier dismissal of the animal",
            "payoff_image": f"{v['inversion_space']}; {v['return_home']}",
        },
    }
