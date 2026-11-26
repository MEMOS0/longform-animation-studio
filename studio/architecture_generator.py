"""Generate first-pass story architecture for original premise packets.

The output is a disciplined creative scaffold for an agent to deepen, not a final
screenplay. It translates evidence-backed mechanisms into sequence-level turns,
proof chains, relational changes, visual setpieces, and retention hooks.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

FRACTIONS = [0.0, 0.10, 0.20, 0.32, 0.45, 0.58, 0.74, 0.88, 1.0]


def time_ranges(target_minutes: float) -> list[str]:
    points = [round(target_minutes * f, 1) for f in FRACTIONS]
    return [f"{points[i]:g}-{points[i + 1]:g} minutes" for i in range(8)]


def text(premise: dict[str, Any], path: list[str], default: str = "") -> Any:
    cur: Any = premise
    for key in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(key)
    return cur if cur not in (None, "") else default


def generate_architecture(premise: dict[str, Any]) -> dict[str, Any]:
    target = float(premise.get("target_minutes") or 42)
    ranges = time_ranges(target)
    protagonist = text(premise, ["protagonist", "identity"], "the protagonist")
    capability = text(premise, ["protagonist", "capability"], "their craft")
    object_name = text(premise, ["meaning_carrier", "object_or_space"], "inherited object")
    opening_space = text(premise, ["opening_event", "first_10_seconds"], "a public status boundary")
    child = text(premise, ["emotional_engine", "protective_counterforce"], "a vulnerable ally")
    injustice = text(premise, ["emotional_engine", "injustice"], "the antagonist abuses institutional power")
    care = text(premise, ["relational_contract", "safety_or_kindness_before_power"], "a non-romantic care network")
    repair = text(premise, ["relational_contract", "consent_or_personhood_repair"], "authority must restore choice and trust")
    payoff = text(premise, ["relational_contract", "payoff_image"], "the wounded space becomes chosen belonging")
    carrier_close = text(premise, ["meaning_carrier", "closing_reversal"], "the opening object becomes proof")
    final_use = text(premise, ["meaning_carrier", "final_sequence_use"], "the object returns in the ending ritual")
    question = text(premise, ["opening_event", "dramatic_question"], "can dignity survive public humiliation?")

    beats = [
        {
            "function": "spatial humiliation, vulnerable alliance, and promise payoff",
            "turn": f"the forced status ritual is interrupted when {child} physically crosses toward the humiliated protagonist",
            "choice": "protect the vulnerable ally or preserve dignity before protecting personal safety",
            "clue": f"{object_name} is introduced as emotionally and practically significant",
            "ally": f"{child} creates the first morally trustworthy bond",
            "secret": "the antagonist realizes the protagonist's bond threatens status control",
            "shift": "shame to protective purpose",
            "visual": opening_space,
            "sound": "public laughter and clatter thin into close breath/contact silence at the moment of alliance",
            "hook": "why does the powerless ally trust the person every powerful adult rejects?",
        },
        {
            "function": "care network, work identity, and dignity economy",
            "turn": f"{care}; help becomes work and shelter rather than humiliating charity",
            "choice": "accept costly honest work while refusing payment that would commodify humiliation",
            "clue": f"the protagonist demonstrates {capability} in a small practical problem",
            "ally": "non-romantic witnesses begin treating the protagonist as a person rather than a servant",
            "secret": "a high-status observer notices the alliance but does not yet understand the proof/craft implication",
            "shift": "survival fear to cautious agency",
            "visual": "small labor ritual with inherited object, care-giver space, and first repeatable customer/ally interaction",
            "sound": "warm practical labor textures replace dining-room laughter",
            "hook": "can honest work create safety before power notices?",
        },
        {
            "function": "bond growth, antagonist retaliation, and object rule",
            "turn": "the antagonist repeats the original spatial punishment and raises the economic/social cost",
            "choice": "continue helping or working openly despite wage loss, ridicule, or exclusion",
            "clue": f"the rules of {object_name} and the protagonist's proof literacy become legible",
            "ally": f"the bond with {child} becomes habitual and trusted",
            "secret": injustice,
            "shift": "hope to renewed vulnerability",
            "visual": "status space repeated with a sharper punishment; object lesson embedded in action",
            "sound": "intimate object/craft detail against hostile public murmur",
            "hook": "what does the object know that powerful people do not?",
        },
        {
            "function": "competence deepens while antagonist reaches for irreversible control",
            "turn": "the protagonist's craft identity becomes public enough to threaten the antagonist, who prepares a frame-up or institutional attack",
            "choice": "tell a partial truth to protect someone weaker even though it increases personal risk",
            "clue": "first contradiction in the antagonist's timeline/object story appears",
            "ally": "a minor worker/witness notices a detail that later becomes evidence",
            "secret": "the antagonist's motive is status/property control, not merely jealousy",
            "shift": "confidence to unstable hope",
            "visual": "craft demonstration intercut with antagonist moving pieces behind doors",
            "sound": "competence rhythm interrupted by institutional silence and door/lock sounds",
            "hook": "will the audience see the trap before the protagonist does?",
        },
        {
            "function": "midpoint public accusation and maximum shame",
            "turn": "the protagonist is publicly accused/arrested/excluded using planted or manipulated evidence",
            "choice": "defend truth without exposing or endangering the vulnerable ally",
            "clue": f"{carrier_close} becomes the central question, but the proof chain is incomplete",
            "ally": f"{child} or a lower-status witness sees the public wound clearly while powerful people misread it",
            "secret": "the accusation attacks the same identity that can eventually disprove it",
            "shift": "hard-won hope to public despair",
            "visual": "the original audience/social space is reused for arrest, accusation, or expulsion",
            "sound": "public noise drops into a thin close perspective during the decisive accusation",
            "hook": "who planted the proof, and can the victim author the reversal?",
        },
        {
            "function": "agency reconstruction and first proof chain movement",
            "turn": "the protagonist refuses passive rescue and begins reading the evidence through established competence",
            "choice": "accept only accountable help/advance while retaining control of the proof",
            "clue": "maker marks, timing, witness geometry, or object behavior contradict the frame-up",
            "ally": "the care network and minor witnesses become an active proof community",
            "secret": "the timeline predates the protagonist's alleged opportunity",
            "shift": "despair to disciplined anger",
            "visual": "investigation through craft locations, work surfaces, and overlooked service spaces",
            "sound": "quiet concentrated labor, location-specific reverberation, and proof-object texture",
            "hook": "which small detail will collapse the antagonist's timeline?",
        },
        {
            "function": "proof chain completion and relational repair before public victory",
            "turn": "the final witness/object/timeline locks into place; the protagonist claims the right to present the proof personally",
            "choice": repair,
            "clue": f"all layers of the proof chain align through {object_name}: object, craft knowledge, timeline, witness, and motive",
            "ally": "former doubters change behavior before asking forgiveness",
            "secret": "the antagonist exploited institutional trust and public spectacle, not just personal cruelty",
            "shift": "fear to controlled resolve",
            "visual": "preparation for the same-audience confrontation, with the original space reset as a trap for truth",
            "sound": "near-silent resolve and restrained breathing rather than triumphant music",
            "hook": "will public proof repair social shame or only expose guilt?",
        },
        {
            "function": "same-audience reversal, justice, craft restoration, and circular chosen-space payoff",
            "turn": "the original audience witnesses the proof; status power reverses through changed conduct and material consequences",
            "choice": "choose belonging and forgiveness only after agency, work, and truth are secure",
            "clue": final_use,
            "ally": "care network, innocent ally, and reformed authority gather as a new community",
            "secret": "the final revelation is relational: power admits what it failed to see",
            "shift": "public vindication to warm chosen belonging",
            "visual": payoff,
            "sound": "the original humiliation sound motif returns transformed into communal rhythm or completed musical motif",
            "hook": "the ending answers the opening spatial question rather than teasing a sequel",
        },
    ]
    sequences = []
    for index, beat in enumerate(beats):
        sequences.append({
            "sequence": index + 1,
            "time_range": ranges[index],
            "function": beat["function"],
            "turn": beat["turn"],
            "protagonist_choice": beat["choice"],
            "new_capability_or_clue": beat["clue"],
            "ally_or_relationship_change": beat["ally"],
            "secret_reveal_escalation": beat["secret"],
            "emotional_shift": beat["shift"],
            "visual_setpiece": beat["visual"],
            "sound_design_intent": beat["sound"],
            "retention_hook": beat["hook"],
        })
    return {
        "target_minutes": target,
        "central_dramatic_question": question,
        "protagonist_need_arc": text(premise, ["protagonist", "transformation"], "from survival to chosen agency"),
        "sequences": sequences,
        "midpoint_reversal": "public accusation/frame-up converts private humiliation into maximum social shame while seeding the proof chain that will reverse it",
        "ending_payoff": {
            "justice": "the true manipulator loses the exact status/property/control they exploited, with material consequences rather than insults alone",
            "belonging": payoff,
            "future_image": f"the protagonist's capability becomes public work/legacy, while {object_name} remains visible as transformed proof rather than nostalgia",
        },
        "anti_patterns_checked": [
            "wealth or romance does not replace protagonist agency",
            "hidden power/status creates relational consequences rather than instant reward",
            "public accusation receives public repair",
            "proof chain is seeded before the reversal",
            "opening spatial wound returns transformed in the ending",
        ],
        "evidence_references": [
            "knowledge/market/karma-floor-table-social-proof-deep-dive.md",
            "knowledge/market/dramora-compressed-social-melodrama-deep-dive.md",
            "knowledge/market/leso-faith-economic-reversal-deep-dive.md",
        ],
    }


def write_architecture(premise_path: Path, output_path: Path) -> dict[str, Any]:
    premise = json.loads(premise_path.read_text(encoding="utf-8"))
    architecture = generate_architecture(premise)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(architecture, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return architecture
