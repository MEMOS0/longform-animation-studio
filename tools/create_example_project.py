"""Create a complete original example project using the studio system end-to-end."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "stormglass_keepers"

premise = {
    "premise_id": "stormglass_keepers_v1",
    "title_candidates": [
        "They Hunted the Last Stormglass Dragon Child… Until the Disgraced Keeper Chose to Protect It",
        "The Last Stormglass Child Trusts the Keeper Everyone Else Calls a Traitor",
        "A Hunted Dragon Child. A Disgraced Keeper. One Storm That Can Save Them Both."
    ],
    "logline": "A disgraced royal beastkeeper rescues the last stormglass dragon child from the navy that made her a scapegoat, then must return to the kingdom that condemned her before the child is weaponized and the sea storm destroys both their homes.",
    "audience_promise": "A cinematic creature-protection fantasy: visible vulnerable dragon child, costly protective love, injustice and public reversal, storm-scale spectacle, and a warm found-family/belonging payoff.",
    "target_minutes": 48,
    "release_format": "mid_length_feature",
    "channel_contract": "creature_protection_feature",
    "emotional_engine": {
        "wound": "Mira was publicly branded a traitor after a nursery fire she did not start, losing her home, rank, and every creature she loved.",
        "want": "Mira wants to survive far from the kingdom and never bond with another creature she can lose.",
        "need": "She needs to accept protection as love rather than weakness and risk attachment again.",
        "injustice": "The admiral who caused the nursery fire now hunts the last dragon child and plans to use it as a navigation weapon.",
        "protective_counterforce": "Mira repeatedly chooses the dragon child's safety over her own exile, freedom, and revenge.",
        "belonging_payoff": "Mira, the child, and the coastal villagers form a protected home where the child is no longer property and Mira is publicly restored.",
        "secret_or_power_asymmetry": "Mira knows the child's stormcall can calm the sea only when it feels safe; the navy thinks pain can control it.",
        "cost_of_failure": "The child becomes a weapon, the storm wall collapses, and both the capital and fishing coast are flooded."
    },
    "protagonist": {
        "identity": "Mira Vale, ex-royal beastkeeper living as a lighthouse laborer",
        "vulnerability": "Social disgrace, fear of attachment, and a burn scar that the navy uses to identify her",
        "capability": "Reads creature fear, weather behavior, and body language better than anyone in the kingdom",
        "agency_first_action": "She cuts the dragon child free from a weighted capture net even though helping it exposes her identity",
        "transformation": "From self-protective exile to public protector willing to trust and be trusted again"
    },
    "opening_event": {
        "first_10_seconds": "A weighted navy net crashes into black water; inside it, a palm-sized translucent blue dragon child claws at the ropes and cries silently.",
        "first_60_seconds": "Mira recognizes the creature's panic, sees the royal brand on the net, and cuts it free while soldiers close in on the shore.",
        "first_5_minutes": "The child bonds to Mira after she shields it from crossbow fire; its fear calls the first impossible storm wall, proving the title promise visually.",
        "dramatic_question": "Can Mira keep the child emotionally and physically safe long enough to expose the admiral before fear turns the storm against everyone?"
    },
    "theme_lane": {
        "mythic_creature": "stormglass dragon child whose emotional state shapes sea weather",
        "family_or_heir_hook": "last surviving creature child and deposed protector becoming chosen family",
        "romance_hook": "",
        "modern_power_hook": ""
    },
    "failure_intelligence": {
        "evaluation_path": "examples/stormglass_keepers/production_evaluation.json",
        "nearest_failures": [
            "Epic Earthquake: diffuse spectacle before relational anchor",
            "The Next Show ARKAN: abstract quest lore before embodied stakes",
            "Nov underperformers: lore/court exposition before wound-care loop"
        ],
        "mitigations": [
            "Open on the child in visible peril, not mythology.",
            "Make every spectacle scene threaten or protect the child/Mira relationship.",
            "Limit exposition to facts that change immediate protection choices.",
            "Each act gives Mira an active protective decision and a cost.",
            "End with belonging and public restoration, not only punishment."
        ],
        "counterexamples_checked": [
            "Epic One Last Phone Call proves a strong opening alone cannot overcome channel-contract mismatch; therefore creature/protector fit is explicit.",
            "The Next Show Sinbad proves serialization/continuation can work after a major setpiece payoff; this film still resolves its core emotional arc."
        ]
    },
    "packaging": {
        "thumbnail_single_read": "Close protective hands around a glowing translucent dragon child while a storm-lit naval fleet approaches behind them.",
        "curiosity_gap": "Why is the kingdom hunting a creature child, and why is the accused traitor the only one it trusts?",
        "visual_before_after": "cold netted creature in darkness vs warm glowing child protected in hands",
        "title_thumbnail_mismatch_risk": "Low if the dragon child and protection relationship are visually dominant; avoid making the navy/army the main read."
    },
    "evidence_boundaries": [
        "Observational evidence informs the design but does not prove CTR or retention causality.",
        "The concept is original; it uses mechanisms rather than copying plot, dialogue, characters, or thumbnail artwork.",
        "No AI-generated media has been produced yet; production feasibility still requires provider validation."
    ]
}

architecture = {
    "target_minutes": 48,
    "central_dramatic_question": "Can protective trust calm what violence is trying to weaponize?",
    "protagonist_need_arc": "Mira moves from refusing attachment to choosing public, costly protective love.",
    "sequences": [
        {
            "sequence": 1,
            "time_range": "0-5 minutes",
            "function": "embodied hook and creature-protection promise",
            "turn": "Mira's hiding place becomes a rescue site",
            "protagonist_choice": "cut the child free despite exposure",
            "new_capability_or_clue": "the child's fear can raise stormglass walls",
            "ally_or_relationship_change": "child imprints on Mira after protection",
            "secret_reveal_escalation": "royal brand proves kingdom involvement",
            "emotional_shift": "fear to protective urgency",
            "visual_setpiece": "black-water net rescue and first storm wall",
            "sound_design_intent": "near-silent creature cry under rope creaks, then storm sub-bass",
            "retention_hook": "why does the navy hunt a child whose fear controls weather?"
        },
        {
            "sequence": 2,
            "time_range": "5-10 minutes",
            "function": "establish injustice and pursuit",
            "turn": "Mira is recognized by the burn scar",
            "protagonist_choice": "abandon her safe lighthouse cover and flee inland",
            "new_capability_or_clue": "the child calms when Mira hums the old beastkeeper lullaby",
            "ally_or_relationship_change": "young ferryman Tam chooses to help after seeing the child spared",
            "secret_reveal_escalation": "Mira admits she once protected the royal nursery",
            "emotional_shift": "urgency to fugitive dread",
            "visual_setpiece": "cliffside lighthouse escape as lantern ships sweep the rocks",
            "sound_design_intent": "lullaby close and intimate against distant engine thrum",
            "retention_hook": "the admiral brands Mira a kidnapper and offers a public bounty"
        },
        {
            "sequence": 3,
            "time_range": "10-16 minutes",
            "function": "deepen bond and first cost",
            "turn": "the child refuses food because captivity trauma makes it fear metal",
            "protagonist_choice": "Mira removes her protective gloves and lets the child bite/bond with her scarred hand",
            "new_capability_or_clue": "the child projects memory-images through its glass scales",
            "ally_or_relationship_change": "Tam shifts from profit motives to genuine ally",
            "secret_reveal_escalation": "memory shows Admiral Rook ordering the nursery fire",
            "emotional_shift": "dread to tenderness and moral certainty",
            "visual_setpiece": "memory-light cave filled with floating images of the nursery fire",
            "sound_design_intent": "drop music for the bite; heartbeat and scale chimes carry the moment",
            "retention_hook": "they now possess proof, but no one will believe a disgraced exile"
        },
        {
            "sequence": 4,
            "time_range": "16-22 minutes",
            "function": "social-world complication",
            "turn": "villagers shelter them until the bounty makes neighbors afraid",
            "protagonist_choice": "Mira surrenders her last royal token to buy boats for evacuation rather than her own escape",
            "new_capability_or_clue": "stormglass shards react to collective fear in the village",
            "ally_or_relationship_change": "village elder Ilsa becomes a protective witness",
            "secret_reveal_escalation": "Mira learns the king believes she murdered the nursery creatures",
            "emotional_shift": "tenderness to communal vulnerability",
            "visual_setpiece": "lantern-lit evacuation through tidal tunnels",
            "sound_design_intent": "whispered crowd fear, water drips, child whimper as rhythmic tension",
            "retention_hook": "navy ships arrive before the evacuation completes"
        },
        {
            "sequence": 5,
            "time_range": "22-28 minutes",
            "function": "midpoint reversal",
            "turn": "Tam apparently betrays their route, causing Mira and the child to be captured",
            "protagonist_choice": "Mira chooses to shield the child rather than attack Tam or escape alone",
            "new_capability_or_clue": "the child's pain can crack stormglass and destroy ships",
            "ally_or_relationship_change": "Mira's trust in people is shattered even as her bond with the child deepens",
            "secret_reveal_escalation": "Rook reveals he plans to force the child to open a storm channel for invasion",
            "emotional_shift": "communal hope to betrayal and captivity",
            "visual_setpiece": "iron containment chamber where every lash of fear fractures the walls",
            "sound_design_intent": "music cuts out when the child is restrained; metal and breath dominate",
            "retention_hook": "Tam is shown slipping a copied key into his sleeve"
        },
        {
            "sequence": 6,
            "time_range": "28-35 minutes",
            "function": "dark-night escape and trust repair",
            "turn": "Tam's betrayal is revealed as infiltration, but Mira must choose whether to trust him again",
            "protagonist_choice": "she accepts Tam's help without forgiving him yet and frees other captured sea creatures first",
            "new_capability_or_clue": "freed creatures can carry the memory-proof to the capital witnesses",
            "ally_or_relationship_change": "Mira, Tam, and the child become a coordinated found-family unit",
            "secret_reveal_escalation": "the child recognizes the mother-call beneath the capital storm vault",
            "emotional_shift": "betrayal to fragile trust and purpose",
            "visual_setpiece": "multi-creature escape through storm-lit ship canals",
            "sound_design_intent": "lullaby motif returns broken, then harmonizes with creature calls",
            "retention_hook": "the child may not be the last: its mother or sibling is imprisoned below the capital"
        },
        {
            "sequence": 7,
            "time_range": "35-42 minutes",
            "function": "climactic public exposure and spectacle",
            "turn": "Rook uses the imprisoned parent creature to weaponize the storm channel",
            "protagonist_choice": "Mira enters the vault publicly rather than fleeing, forcing witnesses to see who truly protects the creatures",
            "new_capability_or_clue": "calm bonding can reverse the weaponized storm channel",
            "ally_or_relationship_change": "villagers and sailors begin defending Mira after seeing the memory-proof",
            "secret_reveal_escalation": "the king witnesses Rook's confession through the child's projected memories",
            "emotional_shift": "fragile purpose to sacrificial resolve",
            "visual_setpiece": "storm vault opens over the capital as parent and child call across chaos",
            "sound_design_intent": "massive storm drops into silence for the child's answering call",
            "retention_hook": "Mira must reach the parent before Rook collapses the vault"
        },
        {
            "sequence": 8,
            "time_range": "42-48 minutes",
            "function": "justice, belonging, and future image",
            "turn": "the creatures calm the storm only after Mira releases control and trusts them",
            "protagonist_choice": "she refuses to use the child's power even to win, breaking the weaponization logic",
            "new_capability_or_clue": "the stormglass network responds to sanctuary rather than command",
            "ally_or_relationship_change": "Mira is publicly restored and chooses a communal coastal home rather than royal rank",
            "secret_reveal_escalation": "the surviving parent remains free by treaty, not captivity",
            "emotional_shift": "sacrificial tension to relief, warmth, and belonging",
            "visual_setpiece": "sunlit stormglass arch over the sea as child and parent fly free",
            "sound_design_intent": "lullaby completed by child/parent calls, then human celebration underneath",
            "retention_hook": "final warmth and restoration rather than sequel dependency"
        }
    ],
    "midpoint_reversal": "Tam's apparent betrayal delivers Mira and the child to Rook, converting a fugitive protection story into a captive weaponization crisis while secretly planting the key to later trust repair.",
    "ending_payoff": {
        "justice": "Rook is publicly exposed by creature memory evidence and his own weaponization attempt, not by hearsay.",
        "belonging": "Mira, the child, Tam, villagers, and freed creatures form a chosen protective community; the child is safe by bond rather than ownership.",
        "future_image": "Mira watches parent and child fly freely through a sunlit stormglass arch while the coastal home lights its first peaceful beacon."
    },
    "anti_patterns_checked": [
        "no diffuse spectacle before relational anchor",
        "no abstract lore before wound/protection loop",
        "no finale-only creature payoff",
        "no repetitive suffering without capability or relationship progression",
        "no revenge-only ending"
    ],
    "evidence_references": [
        "knowledge/market/epic-deep-dive.md",
        "knowledge/market/ironcrest-deep-dive.md",
        "knowledge/market/cross-channel-hit-failure-deep-dives.md"
    ]
}

scene_specs = [
    ("S01", "0-5 minutes", "free the child without being identified", "navy soldiers close in while the child's panic endangers everyone", "hidden exile", "active rescuer", "Mira becomes the child's protector at the cost of exposure", "she cuts the net and shields the child with her body", "a weighted net sinking into black water", "Mira's face hardens when she recognizes the royal brand", "child framed low center, hands and net dominating foreground", "first stormglass wall reflecting soldiers in fractured blue light"),
    ("S02", "5-10 minutes", "escape the lighthouse before the bounty party arrives", "the child cannot control fear and the soldiers have Mira's scar description", "recognized fugitive", "committed fugitive protector", "Mira gives up her safe cover", "she destroys the lighthouse ledger that could reveal the villagers", "lantern ships sweeping wet cliffs", "the child watches Mira hum, fear softening", "vertical shaft composition with Mira below and searchlights above", "child curled inside Mira's coat as the lighthouse collapses behind them"),
    ("S03", "10-16 minutes", "earn the child's trust enough to feed it", "metal triggers captivity panic and Tam wants to sell information", "caregiver without trust", "trusted bond partner", "the child chooses contact with Mira", "Mira removes her gloves and accepts the bite", "the child hissing at a metal cup", "Mira's pain flashes but she stays still", "hands and face stacked vertically; cave darkness isolating them", "memory-light reveals Admiral Rook at the nursery fire"),
    ("S04", "16-22 minutes", "evacuate villagers before the navy arrives", "neighbors fear the bounty and the child reacts to collective fear", "protected outsiders", "exposed communal defenders", "the village becomes involved in the stakes", "Mira trades her royal token for evacuation boats", "stormglass shards pulsing with crowd fear", "elder Ilsa shifts from suspicion to witness", "crowd layers above tidal tunnel depth", "lantern evacuation lines vanish into dark water as warships arrive"),
    ("S05", "22-28 minutes", "protect the child during capture", "Tam appears to betray them and the iron chamber intensifies the child's terror", "free protectors", "captives facing weaponization", "the protection story becomes a weaponization crisis", "Mira covers the child rather than escaping alone", "iron doors closing over blue scale-light", "Tam avoids Mira's eyes, hiding the copied key", "vertical cage bars and faces compressed by closeups", "the chamber wall cracks with each terrified creature cry"),
    ("S06", "28-35 minutes", "escape while testing whether Tam can be trusted", "Mira must free other creatures before the ship locks down", "betrayed captive", "fragile alliance leader", "rescue expands from one child to all captive creatures", "Mira accepts Tam's key but not yet his apology", "copied key turning in a wet lock", "Mira sees Tam take a whip blow meant for the child", "canal depth behind foreground decision faces", "freed creatures streaming through storm-lit canals"),
    ("S07", "35-42 minutes", "expose Rook and stop the weaponized storm channel", "the parent creature is chained beneath the vault and the capital is watching", "hunted exile", "public protector", "private protection becomes public truth", "Mira steps into the vault rather than escaping", "a giant storm eye opening above the capital", "the child's face answering the parent's call", "vast vertical shaft with tiny figures below", "total silence as child and parent hear each other"),
    ("S08", "42-48 minutes", "end the weaponization logic rather than merely win", "using the child's power could defeat Rook but repeat the same violence", "powerless witness", "trusted sanctuary keeper", "control is replaced by trust", "Mira releases the child instead of commanding it", "Rook reaching for the control chain", "the king's certainty breaks as memory-proof appears", "crowd, ruler, and creature aligned in one vertical revelation", "sunlit stormglass arch as parent and child fly free")
]

scenes = []
for sid, tr, objective, conflict, start, end, turn, decision, first, face, comp, final in scene_specs:
    scenes.append({
        "scene_id": sid,
        "time_range": tr,
        "objective": objective,
        "conflict": conflict,
        "power_position_start": start,
        "power_position_end": end,
        "turn": turn,
        "protagonist_decision": decision,
        "subtext": "Protection means risking attachment without turning love into control.",
        "visual_action": {
            "first_image": first,
            "face_reaction": face,
            "vertical_composition": comp,
            "final_image": final
        },
        "dialogue_design": {
            "function": "advance protective choices and power shifts rather than explain lore",
            "subtext_rule": "Characters rarely say fear or love directly; they negotiate control, debt, blame, and safety.",
            "max_exposition_sentences": 2,
            "key_lines": [
                "Pain makes it obey. Trust makes it answer.",
                "You don't save a child by becoming its cage."
            ]
        },
        "sound_design": {
            "dialogue_priority": "dialogue remains intelligible under weather and crowd effects",
            "music_function": "lullaby motif evolves with trust rather than constant emotional wallpaper",
            "silence_or_negative_space": "drop music before each bonding or revelation beat so breath, scale chimes, and creature calls carry meaning",
            "motif": "three-note lullaby answered by glassy creature harmonics"
        },
        "edit_hook": {
            "entry_hook": "enter on immediate danger, choice, or visible emotional consequence",
            "exit_hook": "exit on changed power, new evidence, or an unanswered protective cost"
        },
        "failure_checks": [
            "Does the scene change power, trust, evidence, or capability?",
            "Is spectacle tied to the vulnerable child/protector relationship?",
            "Is exposition converted into a decision or visible event?"
        ]
    })


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "premise.json").write_text(json.dumps(premise, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "architecture.json").write_text(json.dumps(architecture, ensure_ascii=False, indent=2), encoding="utf-8")
    scenes_dir = OUT / "scenes"
    scenes_dir.mkdir(exist_ok=True)
    for scene in scenes:
        (scenes_dir / f"{scene['scene_id']}.json").write_text(json.dumps(scene, ensure_ascii=False, indent=2), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
