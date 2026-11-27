"""Original transformation-romance premise variants.

Mechanism inputs come from the EchoDrama Hidden Beauty deep dive, but the
characters, institutions, objects, wounds, and plots are original.
"""

TRANSFORMATION_ROMANCE_VARIANTS = [
    {
        "id": "paper_lantern_understudy",
        "setting": "an elite performing-arts academy built inside a converted railway station",
        "protagonist": "Mina, a scholarship stagehand who writes plays in empty lighting booths but hides behind black crew clothes after being mocked as the 'invisible stage rat'",
        "love_interest": "Aren, the academy's withdrawn lighting designer who once watched Mina calm a panicking child performer before anyone knew she wrote the play",
        "family_system": "her aunt made Mina wear oversized clothes and stay backstage after her mother was harassed for being too visible on stage",
        "rival": "Vega, a legacy performer whose family funds the academy's new student film",
        "second_engine": "a student film adaptation of a masked heroine story that forces Mina to perform visibility rather than merely receive admiration",
        "meaning_object": "cracked brass backstage key",
        "opening_object_meaning": "the key opens the lighting booth where Mina secretly writes and where her mother once hid during harassment",
        "closing_object_meaning": "the same key opens the booth publicly so Mina can claim authorship and choose visibility on her own terms",
        "pre_transform_witness": "Aren remembers Mina's anonymous voice guiding a child performer through a blackout and values her courage before her appearance changes",
        "reciprocal_memory": "years earlier Mina protected Aren from older students who scattered his lighting notes; he never forgot that she was brave before anyone admired her",
        "public_space": "the station-hall staircase where students gather, film, whisper, and later applaud",
        "transformation_cost": "speech practice, movement training, authorship workshops, and repeated threshold-crossing rather than a cosmetic montage alone",
        "agency_violation": "the director and Mina's aunt agree to cast her before asking whether she consents",
        "closure": "the staircase that once turned her into a spectacle becomes the place where she speaks as author rather than object of attention",
    },
    {
        "id": "saltglass_swim_lesson",
        "setting": "a coastal boarding school where the annual rescue-swim film is shot inside the old tidal pool",
        "protagonist": "Noa, a scholarship pool technician who hides a burn scar and her swimming ability after classmates turned a rescue failure into a humiliating viral clip",
        "love_interest": "Eren, a quiet safety diver who saw Noa keep a younger swimmer alive before the viral clip made her a joke",
        "family_system": "her father taught her to hide the scar and avoid cameras because his own rescue career ended in public blame",
        "rival": "Ilsa, a champion swimmer whose sponsorship depends on staying the school's visible heroine",
        "second_engine": "a training documentary about real rescue swimming that turns performance into dangerous physical competence",
        "meaning_object": "scratched rescue whistle",
        "opening_object_meaning": "the whistle belonged to Noa's mother and is treated as a superstitious piece of pool equipment",
        "closing_object_meaning": "the same whistle coordinates the final rescue drill and proves Noa's competence without erasing the scar",
        "pre_transform_witness": "Eren knows Noa stayed underwater with a panicking child when no camera was recording and trusts that act more than appearance",
        "reciprocal_memory": "as children Noa pulled Eren away from a suction grate and told him to breathe before she knew who he was",
        "public_space": "the tiled pool gallery where students once replayed the humiliating clip and later watch the final drill",
        "transformation_cost": "breath training, scar exposure, rescue certification, and learning to command a room rather than chasing beauty approval",
        "agency_violation": "the coach and Eren enter Noa into the documentary without asking after seeing her secret practice footage",
        "closure": "the pool gallery changes from replay-screen humiliation to a safety community where Noa instructs others openly",
    },
]


def transformation_romance_premise(v: dict, target_minutes: float = 72) -> dict:
    name = v["protagonist"].split(",", 1)[0]
    return {
        "premise_id": v["id"],
        "title_candidates": [
            "They Filmed Her When She Hid — Now They Can't Look Away",
            "The Girl Behind the Curtain Was the Story Everyone Wanted",
            "He Knew Her Before the World Called Her Beautiful",
        ],
        "logline": f"In {v['setting']}, {v['protagonist']} is pushed toward public transformation, but the love interest is credible only because he witnessed her courage before the world approved of her.",
        "audience_promise": "A mobile-native transformation romance in which public gaze inversion, pre-transformation witness, behavioral cost, reciprocal memory debt, and a second performance engine turn visibility into agency rather than mere makeover reward.",
        "target_minutes": target_minutes,
        "release_format": "long_vertical_feature",
        "channel_contract": "transformation_romance",
        "emotional_engine": {
            "wound": f"{name} learned that visibility is dangerous because {v['family_system']}; public misreading then confirmed the shame.",
            "want": "remain useful and safe without becoming a spectacle again",
            "need": "claim authorship, visibility, and love without treating appearance approval as proof of worth",
            "injustice": f"{v['rival']} converts status insecurity into public humiliation and image control",
            "protective_counterforce": f"{v['love_interest']} protects the person before the transformation because {v['pre_transform_witness']}",
            "belonging_payoff": v["closure"],
            "secret_or_power_asymmetry": "legacy status, image control, and institutional casting power oppose a scholarship protagonist with no public protection",
            "cost_of_failure": "she retreats into hiding, loses authorship/professional agency, and confirms the false belief that visibility is annihilation",
        },
        "protagonist": {
            "identity": v["protagonist"],
            "vulnerability": "public shame, image control, family fear, and lack of institutional power",
            "capability": "craft/professional competence, protective courage, persistence, and the ability to lead others once she stops hiding",
            "agency_first_action": "she protects or guides a vulnerable person before protecting her image",
            "transformation": "from protected invisibility to chosen visibility grounded in authorship, competence, consent, and reciprocal recognition",
        },
        "opening_event": {
            "first_10_seconds": f"a future-pressure fragment inside {v['second_engine']} hints that powerful people need the hidden protagonist before the story cuts back to the wound",
            "first_60_seconds": f"{name} is spatially trapped in {v['public_space']} while others film, laugh, or misread her silence",
            "first_5_minutes": f"the family fear system, the meaning-carrier {v['meaning_object']}, and the first pre-transformation protective act are established before the visual transformation",
            "dramatic_question": "can a protagonist who learned that visibility is dangerous become publicly seen without surrendering authorship or accepting shallow approval?",
        },
        "theme_lane": {
            "family_or_heir_hook": "protection itself becomes the wound when a family teaches a child to hide in order to survive",
            "romance_hook": f"{v['love_interest']} remembers reciprocal courage rather than rewarding beauty",
            "modern_power_hook": "viral spectatorship, legacy status, institutional casting, and public image control",
        },
        "transformation_engine": {
            "family_protection_wound": v["family_system"],
            "pre_transformation_witness": v["pre_transform_witness"],
            "reciprocal_memory_debt": v["reciprocal_memory"],
            "behavioral_transformation_cost": v["transformation_cost"],
            "second_performance_engine": v["second_engine"],
            "agency_violation": v["agency_violation"],
            "public_space_reversal": v["public_space"],
            "closure": v["closure"],
        },
        "failure_intelligence": {
            "evaluation_path": "pending_generated_evaluation",
            "nearest_failures": [
                "makeover treated as proof of worth",
                "love interest attracted only after transformation",
                "public humiliation without systemic cause or spatial closure",
                "second half repeating jealousy rather than opening a new performance/professional engine",
                "self-destructive despair imagery used as a cheap transformation trigger",
            ],
            "mitigations": [
                "prove care before transformation",
                "show transformation as behavior and skill, not only appearance",
                "make family protection accountable",
                "reuse the humiliation geometry positively",
                "open a second professional/performance engine after the reveal",
                "make consent violations by allies visible and consequential",
            ],
            "counterexamples_checked": [
                "beautiful transformation imagery alone does not explain retention",
                "romantic rescue is weak unless reciprocal and pre-transformation",
                "viral attention can repeat the wound rather than repair it",
            ],
        },
        "packaging": {
            "thumbnail_single_read": f"{name} centered between public approval and a hostile rival while {v['meaning_object']} catches the light",
            "curiosity_gap": "who saw her before the world decided she was worth watching?",
            "visual_before_after": "hidden backstage/pool-floor posture becomes upright public authorship in the same space",
            "title_thumbnail_mismatch_risk": "generic beauty packaging would undersell authorship, consent, and pre-transformation recognition",
        },
        "evidence_boundaries": [
            "Inspired by mechanism-level evidence in the EchoDrama Hidden Beauty deep dive; characters, institutions, object, second engine, and ending are original.",
            "No CTR, retention, or traffic causality is claimed from public video metadata.",
        ],
        "meaning_carrier": {
            "object_or_space": v["meaning_object"],
            "opening_meaning": v["opening_object_meaning"],
            "closing_reversal": v["closing_object_meaning"],
            "final_sequence_use": f"the object is used openly in the final authorship/rescue ritual inside {v['public_space']}",
        },
        "relational_contract": {
            "power_asymmetry": "legacy visibility/status power versus scholarship protagonist with no control over her public image",
            "safety_or_kindness_before_power": v["pre_transform_witness"],
            "costly_protagonist_action": "she protects a vulnerable person before protecting her appearance or reputation",
            "consent_or_personhood_repair": "allies must return authorship and ask consent after trying to arrange her visibility for her",
            "payoff_image": v["closure"],
        },
    }
