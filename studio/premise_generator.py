"""Original premise generation from evidence-backed mechanisms.

Generated packets are compositional starting points for a creative agent, not
finished scripts and not copies of reference plots. They deliberately combine a
legible wound, vulnerable anchor, spatial status grammar, meaning-carrier object,
agency chain, relational contract, and circular inversion.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .failure_intelligence import evaluate_candidate
from .format_strategy import format_strategy
from .meaning_carrier import evaluate_meaning_carrier
from .relational_contract import evaluate_relational_contract
from .spatial_status import evaluate_spatial_status
from .architecture_generator import generate_architecture
from .scene_generator import generate_scenes
from .screenplay_renderer import write_screenplay
from .survival_premises import COMPRESSED_SURVIVAL_VARIANTS, compressed_survival_premise
from .transformation_premises import TRANSFORMATION_ROMANCE_VARIANTS, transformation_romance_premise

CREATURE_ECONOMIC_VARIANTS = [
    {
        "id": "salt_window_garden",
        "setting": "a desert rail town where water is rationed by a private land trust",
        "protagonist": "Nura, a pastry-cart baker trying to save her grandmother's drought-cracked house",
        "creature": "a child-sized moonfin creature with silver fins and a frightened singing voice",
        "object": "blue glass salt vial",
        "opening_object_meaning": "the vial is the last measured gift of clean rainwater left by Nura's mother",
        "closing_object_meaning": "the same vial proves the land trust has been secretly diverting the town aquifer",
        "care_network": "her grandmother offers food, shelter, and patient labor before anyone powerful believes her",
        "child_ally": "the moonfin child, whose trust is earned through feeding and protection",
        "power_figure": "the land-trust heir and the step-uncle who fabricated the family debt",
        "status_space": "Nura is forced to kneel beside the dry public pump outside the gated garden while trust customers drink inside",
        "inversion_space": "the dry pump yard transformed into a shared garden where water and food are shared by choice",
        "public_wound": "accused of water theft and illegal possession of a valuable creature",
        "proof_chain": "salt crystallization in the vial, pump pressure marks, land-trust ledger timing, a repaired water meter, and a child witness who heard the moonfin sing underground",
        "economic_engine": "pastry cart, water ration tickets, honest customers, and the temptation to sell moonfin tears that can purify water",
        "return_home": "the moonfin returns to the underground spring family rather than becoming Nura's property",
        "bond": "a rival cart seller becomes an accountable partner only after choosing truth over profit",
    },
    {
        "id": "emberseed_oven_cart",
        "setting": "a volcanic hillside city where bakery ovens are licensed by a coal guild",
        "protagonist": "Lio, a debt-bound flatbread baker whose mother's oven license was erased",
        "creature": "a sparrow-sized emberseed bird child whose feathers can relight cold ovens",
        "object": "blackened brass oven key",
        "opening_object_meaning": "the key is dismissed as scrap because the guild removed her mother's maker mark",
        "closing_object_meaning": "the key opens the sealed oven ledger wall and proves the license was stolen",
        "care_network": "a flour miller and night watchman feed Lio before guild protection exists",
        "child_ally": "the emberseed bird child plus the miller's lonely daughter who first hides it",
        "power_figure": "the coal guildmaster and Lio's status-hungry stepbrother",
        "status_space": "Lio is made to bake on the ash floor outside the licensed oven hall while guild families eat inside",
        "inversion_space": "the ash floor converted into a communal dawn bakery where guild and non-guild families eat together",
        "public_wound": "accused of stealing licensed fire and endangering the city",
        "proof_chain": "oven-key teeth, heat-pattern marks, erased maker stamp, coal delivery ledger, and the emberseed's song response",
        "economic_engine": "flatbread cart, oven-license debt, ethical refusal to pluck feathers, and customer proof through bread quality",
        "return_home": "the emberseed returns to the volcanic nesting vents after helping reopen the communal ovens",
        "bond": "the miller becomes family through daily labor and protection rather than wealth rescue",
    },
]

VARIANTS = [
    {
        "id": "glasswing_banquet_platform",
        "setting": "a floating city of glasswing workshops",
        "craft": "glasswing smith",
        "protagonist": "Sefa, a debt-bound glasswing smith whose late mother taught her to read wing fractures",
        "object": "cracked blue measuring cup",
        "opening_object_meaning": "the cup is the only surviving tool from her mother's bench and is treated as junk",
        "closing_object_meaning": "the same cup measures the alloy that proves whose hands made the stolen wings",
        "child_ally": "the guild heir's six-year-old daughter",
        "power_figure": "the guildmaster's ambitious fiancée",
        "status_space": "she is forced to eat scraps beneath the suspended banquet platform while guild guests dine above her",
        "inversion_space": "the workshop floor mat where the whole guild eventually eats by choice",
        "public_wound": "accused of stealing the city's glasswing heart-mold",
        "proof_chain": "wing-fracture signature, alloy ratio in the measuring cup, workshop delivery ledger, and a lift operator who saw the mold move",
        "care_network": "an elderly furnace keeper gives shelter and work before any romantic rescue",
        "bond": "the widowed guild heir learns to trust his daughter's instinct and his own presence at the family table",
    },
    {
        "id": "midnight_lantern_court",
        "setting": "a submerged railway city lit by pressure lanterns",
        "craft": "lantern-mapmaker",
        "protagonist": "Ari, a dismissed lantern-mapmaker who can read pressure cracks in glass",
        "object": "hairline-cracked lantern lens",
        "opening_object_meaning": "the lens is evidence of the flood that killed Ari's father and is treated as superstition",
        "closing_object_meaning": "the same lens projects the pressure signature that proves sabotage",
        "child_ally": "the mayor's mute nephew",
        "power_figure": "the mayor's controlling chief engineer",
        "status_space": "Ari is made to eat in the flooded service tunnel while officials dine in the dry observation car",
        "inversion_space": "the service tunnel floor where survivors and officials share the first dry meal",
        "public_wound": "blamed for a lantern failure that flooded a workers' district",
        "proof_chain": "lens fracture pattern, pressure-log handwriting, valve key tooth marks, and the child's lamp signals",
        "care_network": "a canteen cook hides Ari and trades food for lamp repairs before power intervenes",
        "bond": "the mayor learns that protecting the city means listening below it, not ruling above it",
    },
    {
        "id": "clockwork_orphan_bench",
        "setting": "a mountain city powered by clockwork cable cars",
        "craft": "bell tuner",
        "protagonist": "Mina, an orphan bell tuner whose father was erased from the guild registry",
        "object": "flat brass tuning key",
        "opening_object_meaning": "the key is dismissed as a broken trinket because its maker's mark was filed away",
        "closing_object_meaning": "the key opens the master bell casing and reveals the original registry plate",
        "child_ally": "the cable-car owner's lonely son",
        "power_figure": "the owner's status-hungry betrothed",
        "status_space": "Mina is ordered to eat beside the grease pit while investors eat above the machinery hall",
        "inversion_space": "the grease-pit floor converted into a communal worker breakfast bench",
        "public_wound": "framed for stripping copper from the cable-car bells",
        "proof_chain": "bell resonance, filed maker's mark, key-tooth wear, registry plate, and a night watchman's timing log",
        "care_network": "a night cook and cable mechanic feed her before the owner believes her",
        "bond": "the owner must choose daily presence with his son over status performance",
    },
]


def social_craft_premise(v: dict[str, str], target_minutes: float = 42) -> dict[str, Any]:
    name = v["protagonist"].split(",", 1)[0]
    compressed = target_minutes <= 35.5
    return {
        "premise_id": v["id"],
        "title_candidates": [
            f"They Made Her Eat Below Them, Until a Child Sat Beside Her",
            "The Maid They Called a Thief Was the Only One Who Could Read the Truth",
            f"Nobody Wanted the Broken {v['craft'].title()} — Until the City's Future Depended on Her Hands",
        ],
        "logline": f"In {v['setting']}, {v['protagonist']} is publicly humiliated and framed as a thief, but {v['child_ally']} physically chooses her side; using her craft, a proof chain, and one inherited object, she exposes the real betrayal and turns the place of shame into chosen belonging.",
        "audience_promise": "An emotionally legible animated social melodrama: public humiliation, innocent child alliance, craft-based proof, family repair, class reversal, and a circular ending in which the place of shame becomes chosen community.",
        "target_minutes": target_minutes,
        "release_format": "compressed_feature" if compressed else "mid_length_feature",
        "channel_contract": "social_test_melodrama",
        "emotional_engine": {
            "wound": f"{name} is poor, displaced, and publicly treated as disposable while carrying grief for her parent's stolen craft legacy.",
            "want": "survive, protect family/work obligations, and clear her name",
            "need": "trust that her competence and dignity deserve space without begging for permission",
            "injustice": f"{v['power_figure']} enforces status rules, plants blame, and turns public opinion against her",
            "protective_counterforce": f"{v['child_ally']} physically crosses the status boundary; {v['care_network']}",
            "belonging_payoff": f"the place of forced humiliation becomes {v['inversion_space']}, and her craft receives paid public recognition",
            "secret_or_power_asymmetry": "wealth, institutional authority, and social opinion stand against a worker whose proof depends on specialized craft knowledge",
            "cost_of_failure": "she loses work, family care, public reputation, and the chance to restore her parent's stolen legacy",
        },
        "protagonist": {
            "identity": v["protagonist"],
            "vulnerability": "class displacement, debt, public shame, and lack of institutional power",
            "capability": f"{v['craft']} expertise, proof literacy, persistence, and dignity-preserving work ethic",
            "agency_first_action": "she protects the child or another vulnerable person before protecting herself, then chooses work over humiliating charity",
            "transformation": "from surviving humiliation to authoring the public proof and choosing belonging without surrendering agency",
        },
        "opening_event": {
            "first_10_seconds": v["status_space"],
            "first_60_seconds": f"{v['child_ally']} crosses the boundary and sits or eats beside her while adults laugh or film the humiliation.",
            "first_5_minutes": f"an authority figure witnesses the child's choice; {v['care_network']} gives concrete help; the inherited {v['object']} and her craft identity are introduced before the romance/status reversal.",
            "dramatic_question": "can a publicly shamed craftswoman prove truth without surrendering dignity or becoming dependent on rescue?",
        },
        "theme_lane": {
            "family_or_heir_hook": "lonely child chooses the morally safe adult before powerful adults understand why",
            "romance_hook": v["bond"],
            "modern_power_hook": "institutional wealth, social spectacle, public accusation, and proof",
        },
        "failure_intelligence": {
            "evaluation_path": "pending_generated_evaluation",
            "nearest_failures": [
                "procedural accusation without embodied deprivation",
                "wealth rescue replacing protagonist agency",
                "abstract kindness without a repeatable object",
            ],
            "mitigations": [
                "show humiliation spatially in the first minute",
                "make kindness cost something before high-status intervention",
                "seed the proof object and craft competence before the accusation",
                "reassemble the original public audience for reversal",
                "pay off agency through work and changed ritual, not wealth alone",
            ],
            "counterexamples_checked": [
                "low views do not prove weak story",
                "immediate spectacle alone does not guarantee retention",
                "hidden wealth reveal is weak if treated as reward rather than trust rupture",
            ],
        },
        "packaging": {
            "thumbnail_single_read": f"{name} below the status platform/table while {v['child_ally']} crosses to her side and {v['power_figure']} points down",
            "curiosity_gap": "why is the child choosing the person every powerful adult rejects?",
            "visual_before_after": "forced floor/service space becomes chosen communal floor/workbench; dismissed object becomes proof instrument",
            "title_thumbnail_mismatch_risk": "generic billionaire romance packaging would hide the stronger craft-proof and child-truth mechanism",
        },
        "evidence_boundaries": [
            "Inspired by mechanism-level evidence in social-test and legal-proof research; characters, world, object, proof chain, and dialogue are original.",
            "No CTR, retention, or traffic causality is claimed from public video metadata.",
        ],
        "meaning_carrier": {
            "object_or_space": v["object"],
            "opening_meaning": v["opening_object_meaning"],
            "closing_reversal": v["closing_object_meaning"],
            "final_sequence_use": f"the object is used openly in the proof/restoration ritual before the final communal meal in {v['inversion_space']}",
        },
        "relational_contract": {
            "power_asymmetry": "institutional wealth/status power versus debt-bound worker with no protection",
            "safety_or_kindness_before_power": f"{v['care_network']} offers shelter, food, and paid work before knowing his power or status",
            "costly_protagonist_action": f"{name} protects the child or another worker at cost to her job and refuses humiliating payment even when desperate",
            "consent_or_personhood_repair": "after the accusation, authority figures must trust her account, return control of the proof, and accept her conditions rather than buying forgiveness",
            "payoff_image": f"{v['inversion_space']} where everyone eats or works by choice while the restored object remains visible",
        },
    }


def creature_economic_premise(v: dict[str, str], target_minutes: float = 42) -> dict[str, Any]:
    name = v["protagonist"].split(",", 1)[0]
    compressed = target_minutes <= 35.5
    return {
        "premise_id": v["id"],
        "title_candidates": [
            "She Saved the Creature They Called a Treasure — Then Refused to Sell Its Tears",
            "They Took Her Home for Debt, Unaware the Little Creature Knew Where the Water Went",
            "The Child Creature Was Never Hers to Keep, So She Chose to Set It Free",
        ],
        "logline": f"In {v['setting']}, {v['protagonist']} rescues {v['creature']} while fighting fabricated debt; tempted to monetize its gift, she proves the fraud, returns it home, and transforms the excluded workspace into shared belonging.",
        "audience_promise": "A compressed creature-economic melodrama combining childlike nonhuman personhood, debt/home insecurity, small-business competence, ethical temptation, legal proof, ownership reversal, loving separation, and a materially transformed ending.",
        "target_minutes": target_minutes,
        "release_format": "compressed_feature" if compressed else "mid_length_feature",
        "channel_contract": "creature_economic_melodrama",
        "emotional_engine": {
            "wound": f"{name} is trapped by debt, housing insecurity, public shame, and the fear that survival may require exploiting someone weaker.",
            "want": "save the home/business, survive the debt deadline, and protect the creature",
            "need": "learn that dignity and care cannot be built by owning or monetizing another vulnerable person",
            "injustice": f"{v['power_figure']} uses debt, legal papers, social status, and creature ownership logic to trap both the protagonist and the vulnerable nonhuman child",
            "protective_counterforce": f"{v['child_ally']}; {v['care_network']}",
            "belonging_payoff": f"the opening exclusion space becomes {v['inversion_space']}; the creature returns home rather than becoming property, while the human community gains water/work/dignity",
            "secret_or_power_asymmetry": "private wealth/legal ownership versus a debtor and a creature treated as living treasure",
            "cost_of_failure": "the home is seized, the creature is harvested or caged, and the protagonist becomes complicit in the same ownership system that victimized her",
        },
        "protagonist": {
            "identity": v["protagonist"],
            "vulnerability": "debt, housing precarity, low institutional power, and temptation to survive through another being's pain",
            "capability": "small-business craft, observation of material proof, persistence, care under pressure, and ethical refusal",
            "agency_first_action": f"she saves {v['creature']} before understanding or monetizing its gift",
            "transformation": "from desperate survivor to ethical proof-author who can accept partnership without ownership",
        },
        "opening_event": {
            "first_10_seconds": v["status_space"],
            "first_60_seconds": f"debt papers or a public demand make the home/business deadline concrete while {name} continues serving customers rather than begging.",
            "first_5_minutes": f"she finds {v['creature']} injured or trapped, chooses rescue before profit, discovers the first impossible sign of its gift, and hides it while the inherited {v['object']} appears.",
            "dramatic_question": "can she save her home without turning a vulnerable creature into property?",
        },
        "theme_lane": {
            "family_or_heir_hook": "childlike creature personhood, grandmother/family care, and loving return-home separation",
            "romance_hook": v["bond"],
            "modern_power_hook": "fabricated debt, resource ownership, legal proof, and ethical small-business economics",
        },
        "failure_intelligence": {
            "evaluation_path": "pending_generated_evaluation",
            "nearest_failures": [
                "magic as free money without suffering or consent cost",
                "creature treated as pet/weapon/resource before personhood",
                "legal paperwork replacing embodied stakes",
                "ending that saves the creature but leaves the original debt/home wound unpaid",
            ],
            "mitigations": [
                "make care precede monetization in the opening",
                "give the gift a suffering/consent cost",
                "tie creature ownership and home ownership into one moral system",
                "seed documents/object proof before the reversal",
                "end with transformed space, honest work, and return-home rather than possession",
            ],
            "counterexamples_checked": [
                "low-view creature stories can still have strong mechanics",
                "creature spectacle alone is insufficient",
                "plot cliffhangers only work after relational recognition pays off",
            ],
        },
        "packaging": {
            "thumbnail_single_read": f"{name} sheltering {v['creature']} under cloth or hands while the hostile economic environment and the creature's luminous gift remain visible",
            "curiosity_gap": "will she sell the creature's gift to survive, or protect it and lose everything?",
            "visual_before_after": f"dry/excluded workspace becomes {v['inversion_space']}; {v['object']} changes from discarded inheritance into proof",
            "title_thumbnail_mismatch_risk": "generic creature fantasy packaging would hide the stronger debt/personhood/economic-choice mechanism",
            "compound_expansion": {
                "standalone_requirement": "the film must first resolve the home/debt wound, creature personhood, and community water/work consequence",
                "prequel_window": "15-25 minutes can later show the resource monopoly before the opening debt deadline, ending on the exact exclusion image that begins the standalone film",
                "reuse_rule": "the compressed film may be reused only in original care-before-power order; do not front-load creature spectacle",
                "tail_rule": "any expansion epilogue must clarify rebuilding/nest/community consequence rather than replace closure with a sequel tease",
            },
        },
        "evidence_boundaries": [
            "Inspired by mechanism-level evidence in desert-mermaid, creature-family, social-test, and legal-proof research; characters, world, object, proof chain, and dialogue are original.",
            "No CTR, retention, or traffic causality is claimed from public video metadata.",
        ],
        "meaning_carrier": {
            "object_or_space": v["object"],
            "opening_meaning": v["opening_object_meaning"],
            "closing_reversal": v["closing_object_meaning"],
            "final_sequence_use": f"the object is used openly in the proof/restoration ritual before the final communal meal or work ritual in {v['inversion_space']}",
        },
        "relational_contract": {
            "power_asymmetry": "private resource/legal ownership versus debt-bound worker and a nonhuman child treated as property",
            "safety_or_kindness_before_power": f"{v['care_network']} before knowing the creature's value or any powerful ally's status",
            "costly_protagonist_action": f"{name} protects {v['creature']} at cost to her home, business, safety, and the chance to solve debt quickly",
            "consent_or_personhood_repair": "the creature is never owned as a reward; authority must admit the fraud, the creature chooses home/contact, and the protagonist accepts partnership without possession",
            "payoff_image": f"{v['inversion_space']}; {v['return_home']}",
        },
    }


def generate_premises(contract: str = "social_test_melodrama", count: int = 3, target_minutes: float = 42) -> list[dict[str, Any]]:
    if contract == "social_test_melodrama":
        return [social_craft_premise(v, target_minutes) for v in VARIANTS[:count]]
    if contract == "creature_economic_melodrama":
        return [creature_economic_premise(v, target_minutes) for v in CREATURE_ECONOMIC_VARIANTS[:count]]
    if contract == "compressed_creature_survival":
        return [compressed_survival_premise(v, target_minutes) for v in COMPRESSED_SURVIVAL_VARIANTS[:count]]
    if contract == "transformation_romance":
        return [transformation_romance_premise(v, target_minutes) for v in TRANSFORMATION_ROMANCE_VARIANTS[:count]]
    raise ValueError("currently implemented contracts: social_test_melodrama, creature_economic_melodrama, compressed_creature_survival")


def evaluate_generated_premise(premise: dict[str, Any], archive_rows: list[dict[str, Any]]) -> dict[str, Any]:
    combined = json.dumps(premise, ensure_ascii=False)
    return {
        "premise_id": premise.get("premise_id"),
        "failure_intelligence": evaluate_candidate((premise.get("title_candidates") or ["untitled"])[0], archive_rows, combined),
        "format_strategy": format_strategy(premise.get("target_minutes"), combined, premise.get("release_format", "")),
        "meaning_carrier": evaluate_meaning_carrier(premise, {}),
        "relational_contract": evaluate_relational_contract(premise),
        "spatial_status": evaluate_spatial_status(premise, {}, []),
    }


def generate_and_write(output_dir: Path, count: int, target_minutes: float, archive_rows: list[dict[str, Any]], contract: str = "social_test_melodrama") -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for premise in generate_premises(contract=contract, count=count, target_minutes=target_minutes):
        path = output_dir / f"{premise['premise_id']}_premise.json"
        path.write_text(json.dumps(premise, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        evaluation = evaluate_generated_premise(premise, archive_rows)
        eval_path = output_dir / f"{premise['premise_id']}_evaluation.json"
        eval_path.write_text(json.dumps(evaluation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        architecture = generate_architecture(premise)
        arch_path = output_dir / f"{premise['premise_id']}_architecture.json"
        arch_path.write_text(json.dumps(architecture, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        scenes_dir = output_dir / f"{premise['premise_id']}_scenes"
        scenes_dir.mkdir(parents=True, exist_ok=True)
        scenes = generate_scenes(premise, architecture)
        for scene in scenes:
            (scenes_dir / f"{scene['scene_id']}.json").write_text(json.dumps(scene, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        screenplay_path = output_dir / f"{premise['premise_id']}_screenplay.md"
        write_screenplay(premise, scenes, screenplay_path)
        rows.append({"premise_id": premise["premise_id"], "path": str(path), "evaluation_path": str(eval_path), "architecture_path": str(arch_path), "scenes_dir": str(scenes_dir), "screenplay_path": str(screenplay_path), "evaluation": evaluation})
    return {"count": len(rows), "premises": rows}
