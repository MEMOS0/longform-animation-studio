"""Transformation-romance sequence architecture."""

from typing import Any


def _engine(premise: dict[str, Any]) -> dict[str, Any]:
    return premise.get("transformation_engine") or {}


def apply_transformation_architecture(beats: list[dict[str, Any]], premise: dict[str, Any]) -> None:
    """Replace inherited social-melodrama beats with transformation-romance turns."""
    e = _engine(premise)
    object_name = premise.get("meaning_carrier", {}).get("object_or_space", "meaning-carrier object")
    protagonist = premise.get("protagonist", {}).get("identity", "the protagonist").split(",", 1)[0]
    love = premise.get("emotional_engine", {}).get("protective_counterforce", "the love interest")
    rival = premise.get("emotional_engine", {}).get("injustice", "the rival")
    second = e.get("second_performance_engine", "the second performance engine")
    public_space = e.get("public_space_reversal", "the public gaze space")
    replacements = [
        {
            "function": "future-pressure loop hook, public misreading, and protection-wound contract",
            "turn": "a fragment of the future performance/casting pressure plays before the story cuts back to the original public humiliation",
            "choice": "protect a vulnerable person or preserve a small dignity boundary while the crowd misreads her",
            "clue": f"{object_name} is introduced as the private object/space where the protagonist still authors herself",
            "ally": "the first bond is behavioral protection before admiration",
            "secret": "the family protection system is part of the wound, not merely a sad backstory",
            "shift": "mystery to shame and self-concealment",
            "visual": f"future performance fragment intercut with {public_space} spectatorship and the private object space",
            "sound": "a polished future-performance sound fragment collapses into phone noise, crowd murmur, breath, and object texture",
            "hook": "why does the future need the person everyone is trained not to see?",
        },
        {
            "function": "false rescue, social annihilation, and family accountability",
            "turn": "kindness is publicly reinterpreted as nothing or turned against the protagonist, confirming that being seen means being misjudged",
            "choice": "stop performing for the crowd and tell the family what the protection strategy has cost",
            "clue": e.get("family_protection_wound", "the family taught hiding as protection"),
            "ally": "a caregiver admits that protective control caused harm instead of only comforting the victim",
            "secret": "the protagonist's shame is a learned survival system rather than truth about her worth",
            "shift": "romantic hope to maximum self-erasure, then permission to change",
            "visual": "public crowd geometry repeated at close range, then home objects/mirror/food/scar/ritual evidence of the family system",
            "sound": "crowd noise thins into domestic silence and difficult breathing rather than swelling consolation music",
            "hook": "can transformation begin as permission rather than self-hatred?",
        },
        {
            "function": "behavioral transformation cost and first self-authorship",
            "turn": "the protagonist chooses change through training, craft, speech, movement, certification, or authorship rather than instant cosmetic reward",
            "choice": "continue the costly transformation practice after failure because it serves self-authorship",
            "clue": e.get("behavioral_transformation_cost", "the transformation requires repeated behavioral cost"),
            "ally": "the family/care network supports autonomy rather than controlling appearance",
            "secret": "someone has already witnessed her courage before the visible change",
            "shift": "shame to disciplined self-direction",
            "visual": "repeated practice, body/skill labor, mirror hesitation, object use, and threshold-crossing over time",
            "sound": "breath, repetitive training rhythm, room tone, and sparse encouragement replace montage gloss",
            "hook": "will the new self survive re-entry into the same public space?",
        },
        {
            "function": "gaze inversion and morally suspect attention",
            "turn": "the same crowd now admires the protagonist without recognizing the person it previously humiliated",
            "choice": "walk through the space upright without forgiving or trusting the crowd's shallow reversal",
            "clue": "attention is not proof of worth; it is a reversal of social power",
            "ally": "the love interest reacts differently because he already knows who she was before visibility",
            "secret": e.get("pre_transformation_witness", "the love interest witnessed courage before transformation"),
            "shift": "fear of being seen to suspicion of being desired",
            "visual": f"{public_space} repeated with frozen onlookers, phones, whispers, threshold crossing, and upright movement",
            "sound": "crowd murmur swells then drops into close footsteps/breath at the decisive threshold",
            "hook": "if they knew who she was before, would they still look at her this way?",
        },
        {
            "function": "second performance/professional engine opens after the first transformation payoff",
            "turn": second,
            "choice": "enter an arena where she must perform visibility rather than merely receive admiration",
            "clue": "the rival treats the role/public image as property and begins procedural interference",
            "ally": "the love interest becomes a working partner rather than a rescuer",
            "secret": "the director/coach/institution sees authorship or competence the crowd only consumes as image",
            "shift": "social validation to professional fear",
            "visual": "audition/training/rehearsal spaces, camera or drill machinery, public spectators, and the protagonist visibly unprepared but capable",
            "sound": "institutional instructions, camera/pool/stage machinery, countdowns, and withheld music",
            "hook": "can she perform being seen without losing control of herself?",
        },
        {
            "function": "agency violation, protective intimacy, and danger setpiece",
            "turn": e.get("agency_violation", "allies arrange her visibility without asking") + "; the objection is real even though the opportunity is attractive",
            "choice": "continue only after reclaiming consent and boundaries rather than accepting arranged visibility",
            "clue": "rival interference turns public image pressure into physical or professional danger",
            "ally": f"{love} protects through respect, timing, and practical action rather than ownership",
            "secret": "the pre-transformation rescue/witness truth begins surfacing",
            "shift": "obligation to negotiated trust",
            "visual": "rehearsal/training danger, water/stage/camera machinery, improvised protection, and boundaries visible in blocking",
            "sound": "lower loudness, higher negative space, fewer words, and faster cutting during the danger peak",
            "hook": "is protection love if it began by taking away her choice?",
        },
        {
            "function": "reciprocal memory debt and real confession beneath performance",
            "turn": e.get("reciprocal_memory_debt", "the love interest remembers that she protected him before status or beauty"),
            "choice": "accept love only after separating gratitude from desire and performance from truth",
            "clue": "the protagonist learns that her pre-transformation courage, not the transformation, made her unforgettable",
            "ally": "romance becomes reciprocal recognition rather than rescue debt",
            "secret": "the rival interprets loss as annihilation and escalates toward irreversible exposure/violence",
            "shift": "guarded gratitude to mutual recognition",
            "visual": "quiet rehearsal/performance two-shot where staged intimacy is mistaken for fiction, then explicitly claimed as real",
            "sound": "scene noise drops away; breath and close voice carry more weight than score",
            "hook": "what was real once the performance ends?",
        },
        {
            "function": "public-space reversal, institutional consequence, and chosen visibility closure",
            "turn": "the rival's final attempt to annihilate visibility fails; the protagonist fights back and receives support without surrendering agency",
            "choice": "step into the original public space as author/leader rather than object of attention",
            "clue": f"{object_name} returns openly as the tool of authorship, coordination, or self-claiming",
            "ally": "family, institution, and partner repair conduct through public support and consequence rather than private apology alone",
            "secret": "visibility is no longer the crowd's gift; it is the protagonist's chosen action",
            "shift": "defensive survival to chosen public belonging",
            "visual": e.get("closure", "the original humiliation space returns transformed into chosen recognition"),
            "sound": "crowd sound returns but no longer overwhelms the close voice/breath/object signature",
            "hook": "the ending answers the opening gaze wound through chosen authorship, not applause alone",
        },
    ]
    for beat, replacement in zip(beats, replacements):
        beat.update(replacement)
