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


def generate_premises(contract: str = "social_test_melodrama", count: int = 3, target_minutes: float = 42) -> list[dict[str, Any]]:
    if contract != "social_test_melodrama":
        raise ValueError("currently implemented contract: social_test_melodrama")
    return [social_craft_premise(v, target_minutes) for v in VARIANTS[:count]]


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


def generate_and_write(output_dir: Path, count: int, target_minutes: float, archive_rows: list[dict[str, Any]]) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for premise in generate_premises(count=count, target_minutes=target_minutes):
        path = output_dir / f"{premise['premise_id']}_premise.json"
        path.write_text(json.dumps(premise, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        evaluation = evaluate_generated_premise(premise, archive_rows)
        eval_path = output_dir / f"{premise['premise_id']}_evaluation.json"
        eval_path.write_text(json.dumps(evaluation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        rows.append({"premise_id": premise["premise_id"], "path": str(path), "evaluation_path": str(eval_path), "evaluation": evaluation})
    return {"count": len(rows), "premises": rows}
