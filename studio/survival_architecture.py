"""Architecture overrides for compressed visual-first creature-survival premises."""
from __future__ import annotations

from typing import Any


def apply_compressed_survival_architecture(beats: list[dict[str, Any]], premise: dict[str, Any]) -> None:
    surv = premise.get("survival_engine", {})
    predator = surv.get("predator", "the predator")
    vehicle = surv.get("vehicle_or_station", "the wrecked vehicle")
    animal = surv.get("innocent_animal", "the small animal")
    ally = surv.get("ally_creature", "the creature ally")
    occupation = surv.get("occupation", "professional")
    object_name = premise.get("meaning_carrier", {}).get("object_or_space", "the survival tool")
    opening_meaning = premise.get("meaning_carrier", {}).get("opening_meaning", "a routine tool")
    closing_meaning = premise.get("meaning_carrier", {}).get("closing_reversal", "the tool becomes the rescue mechanism")
    payoff = premise.get("relational_contract", {}).get("payoff_image", "the wreck becomes a rescue shelter")
    first10 = premise.get("opening_event", {}).get("first_10_seconds", "the disaster begins inside the vehicle")

    replacements = [
        {
            "function": "role contract, disaster, and immediate survival stakes",
            "turn": first10,
            "choice": "save whoever can still be reached before understanding what caused the disaster",
            "clue": f"{object_name} appears as ordinary equipment: {opening_meaning}",
            "ally": f"{animal} is introduced as vulnerable life inside the disaster rather than decoration",
            "secret": "the environment is already unstable, but the protagonist does not yet understand the predator territory",
            "shift": "routine control to bodily emergency",
            "visual": f"the opening role/vehicle/location contract is readable in one image: {vehicle} under catastrophe",
            "sound": "machinery stress, impact rhythm, breath, debris, and animal distress dominate; no explanatory lore",
            "hook": "who is still alive inside the wreck, and what outside force caused the disaster?",
        },
        {
            "function": "predator reveal and terrain-rule establishment",
            "turn": f"{predator} appears in scale relation to the protagonist and turns the disaster site into hunted terrain",
            "choice": "run, hide, or protect the vulnerable animal while learning how the predator tracks movement/sound/light",
            "clue": "the predator's sensory rule and physical scale become visible through one repeated behavior",
            "ally": f"{animal} stays close enough to create a protective obligation",
            "secret": "the disaster may have exposed the victims inside a larger ecological trap",
            "shift": "shock to hunted fear",
            "visual": f"huge predator silhouette against wreckage, terrain, and the small protagonist/animal",
            "sound": "predator texture, scraping shell/claw/limb movement, low silence, and close breath replace crash noise",
            "hook": "what does the predator hunt by — sound, movement, heat, or light?",
        },
        {
            "function": "creature ecology and moral differentiation",
            "turn": f"{ally} enters the ecosystem and proves that not every giant creature is the same kind of threat",
            "choice": "risk stillness, gentleness, or contact rather than treating every creature as a monster",
            "clue": f"{ally} reacts to a color, texture, sound, wound, or light rule connected to {object_name}",
            "ally": f"the first fragile trust forms with {ally} through nonverbal behavior",
            "secret": "the predator is destroying or exploiting the wider ecosystem, not simply occupying it",
            "shift": "terror to uneasy recognition",
            "visual": f"the protagonist's small hand/body beside {ally}, contrasted with the predator's threatening scale",
            "sound": "hostile screech/scrape transitions into exhausted breathing, delicate wing/shell/skin texture, and environmental room tone",
            "hook": "is the strange creature a threat, a victim, or the first ally?",
        },
        {
            "function": "quiet animal-care hinge and first relational cost",
            "turn": f"the protagonist slows down to free, feed, warm, or protect {animal} even though the predator may still be near",
            "choice": "lose escape time to protect a vulnerable life that cannot yet help her",
            "clue": f"{animal} notices a path, sound, scent, or behavior the protagonist missed",
            "ally": f"{animal} becomes an active emotional partner rather than a passive pet image",
            "secret": "the animal's path points toward other survivors or the predator's nest",
            "shift": "panic to protective tenderness",
            "visual": "small animal contact, hands, breath, cloth, wire, feathers/fur, and the protagonist's face in close-up after spectacle",
            "sound": "lowest-density passage in the film: breath, tiny animal vocalization, wind/room tone, footsteps, and no explanatory dialogue",
            "hook": "why is the animal leading her toward danger instead of away from it?",
        },
        {
            "function": "hostage discovery and escape-to-rescue conversion",
            "turn": f"the protagonist finds survivors, victims, or {ally} trapped inside the predator's web/nest/territory",
            "choice": "escape alone or turn back toward the predator center with a rescue obligation",
            "clue": f"the nest layout, victim positions, predator cycle, and {ally}'s capture become spatially legible",
            "ally": f"{animal} guides or warns without becoming a magical solution",
            "secret": "escape alone was always possible, but it would repeat the original guilt wound",
            "shift": "tender fear to guilty resolve",
            "visual": f"cocooned/trapped survivors and {ally} inside a distinct nest/cave/vehicle interior",
            "sound": "web/cave/structure resonance, muffled living bodies, distant predator rhythm, and suppressed breathing",
            "hook": "can she return with a plan before the predator comes back?",
        },
        {
            "function": "occupational preparation and object transformation",
            "turn": f"the protagonist returns to {vehicle} and converts wreckage into a rescue/trap system using {occupation} knowledge",
            "choice": "risk noise, light, fire, or machinery that can attract the predator in order to control where it goes",
            "clue": f"{closing_meaning}; the proof/plan chain aligns through materials established earlier",
            "ally": f"{animal} or a survivor contributes one small behavior that completes the plan without stealing protagonist agency",
            "secret": "the opening disaster space contains the only mechanism strong enough to reverse predator control",
            "shift": "guilt to disciplined competence",
            "visual": f"tools, panels, wires, doors, engine/light/sound systems, and the object being repaired inside {vehicle}",
            "sound": "mechanical clicks, electrical charge, metal stress, fabric, tool rhythm, and brief silence before each test",
            "hook": "will the improvised machine work once, or attract the predator too early?",
        },
        {
            "function": "lure, trap, and spatial climax",
            "turn": f"the protagonist lures {predator} into {vehicle} or its mechanism and pays a bodily cost to keep the plan aligned",
            "choice": "remain exposed long enough for the trap/rescue mechanism to fire rather than abandoning the captives",
            "clue": f"{object_name} operates the final light/sound/gate/engine sequence exactly as seeded",
            "ally": f"{ally} helps only within its established creature behavior; it does not become a convenient weapon",
            "secret": "the predator can be redirected because the protagonist learned its sensory rule rather than overpowering it",
            "shift": "controlled fear to sacrificial resolve",
            "visual": f"predator scale compressed inside the vehicle/station geometry while light, smoke, water, sparks, or sound transform the space",
            "sound": "crescendo of creature mass, machinery, impact, alarm, breath, and one decisive mechanical silence/click before release",
            "hook": "will the mechanism save the captives or trap the protagonist with the predator?",
        },
        {
            "function": "reciprocal rescue, recognition, and chosen survival closure",
            "turn": f"captives are freed, {ally} receives contact or freedom rather than ownership, and {payoff}",
            "choice": "accept help, apology, and shared survival without turning the creature ally into a possession",
            "clue": f"{object_name} remains visible as transformed proof of competence and care",
            "ally": "survivors repair their earlier dismissal of the animal or creature through behavior before dialogue",
            "secret": "the final revelation is relational: the vulnerable lives everyone underestimated carried the path to survival",
            "shift": "survival relief to chosen belonging",
            "visual": f"contact, freed bodies, open threshold, animal/creature return, and the transformed vehicle/station as rescue shelter",
            "sound": "machine noise falls away into breath, creature contact, environmental air, and sparse final validation dialogue",
            "hook": "the ending answers the opening guilt through rescue, recognition, and free return rather than sequel spectacle",
        },
    ]
    for beat, replacement in zip(beats, replacements):
        beat.update(replacement)
