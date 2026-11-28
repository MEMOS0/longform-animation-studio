"""Elder remittance/care-delegation integrity checks from Nightfall evidence."""
from __future__ import annotations

import re
from typing import Any


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(_text(item) for item in value.values())
    if isinstance(value, list):
        return "\n".join(_text(item) for item in value)
    return ""


def evaluate_elder_remittance_care_integrity(premise: dict[str, Any], architecture: dict[str, Any], scenes: list[dict[str, Any]]) -> dict[str, Any]:
    full = "\n".join([_text(premise), _text(architecture), _text(scenes)]).lower()
    elder = bool(re.search(r"\b(?:mother|mom|mama|grandmother|grandma|elder|elderly|old lady)\b", full))
    delegated = bool(re.search(r"send\w*[^.\n]{0,40}(?:money|\$|dollars?|month)|remittance|caregiver|guardian|power of attorney|health care proxy|family plan|trustee", full))
    exploitation = bool(re.search(r"begging|credit|exploit|forge|forgery|identity theft|elder abuse|blocked?|padlock|guardianship|dementia|poa|power of attorney", full))
    if not (elder and delegated and exploitation):
        return {"applies": False, "score_0_to_1": 1.0, "warnings": [], "checks": {}}

    ending_parts: list[str] = []
    if isinstance(architecture, dict):
        for key, value in architecture.items():
            if re.search(r"ending|final|closing|resolution|epilogue|payoff", str(key).lower()):
                ending_parts.append(_text(value).lower())
        sequences = architecture.get("sequences") or architecture.get("sequence")
        if isinstance(sequences, list) and sequences:
            ending_parts.append(_text(sequences[-1]).lower())
    architecture_text = _text(architecture).lower()
    end = "\n".join(ending_parts + ([_text(scenes[-1]).lower()] if scenes else [])) or (architecture_text[-max(1, len(architecture_text) // 3):] if architecture_text else "")

    checks = {
        "opening_juxtaposes_apparent_support_with_material_neglect": bool(re.search(r"send\w*[^.\n]{0,50}(?:money|\$|dollars?|month)|three thousand|remittance", full)) and bool(re.search(r"begging|credit|rice|hungry|fever|no food|empty pantry|padlock|debt", full)),
        "elder_has_dignified_competence_work_history_and_selfhood": bool(re.search(r"sew\w*|machine|order slips|work|nurse|trade|business|learned my letters|recalled|recited|competent|put me through school", full)),
        "proxy_control_is_material_not_only_mean": bool(re.search(r"padlock|key|blocked?|forwarded|account administrator|power of attorney|health care proxy|guardian|medicine|lorazepam|control", full)),
        "sender_initially_mistakes_money_transfer_for_care": bool(re.search(r"i send|sent money|money doesn't sit|should have come home|why didn't anybody call|i stopped asking|made her the administrator", full)),
        "unannounced_witnessing_breaks_information_asymmetry": bool(re.search(r"unannounced|came home|didn't tell me you were coming|saw her like this|saw it|i read it this time|witness|recorder|recorded", full)),
        "capacity_attack_uses_falsified_medical_or_legal_procedure": bool(re.search(r"dementia|moderate dementia|no evidence of dementia|doctor|medical certificate|proxy|power of attorney|guardianship|incompetent|sedation|lorazepam|forgery", full)),
        "ordinary_records_and_witnesses_carry_exculpatory_power": bool(re.search(r"grocery account|store|ledger|book|order slips|loan forms|signature|receipt|bank|phone records?|camera|witness|raffle|transcript", full)),
        "elder_speaks_for_herself_in_the_reversal": bool(re.search(r"let her speak|i learned my letters|i've never|being angry at my son|doesn't make me crazy|she recognized me|your honor", full)),
        "restitution_revokes_false_authority_and_restores_control": bool(re.search(r"petition is denied|order is vacated|revocation stands|no sale|goes home|under arrest|attorney's fees|frozen|come off your name|take my name back", end + "\n" + full[-max(1, len(full) // 3):])),
        "ending_converts_money_into_consented_presence_and_care_infrastructure": bool(re.search(r"ask me first|sit at the table|money doesn't sit|porch light|nurse twice|bills on autopay|new phone|teach me|come home|somebody lives here", end)),
        "community_dignity_is_repaired_not_only_villain_punished": bool(re.search(r"pay your tab|you don't owe|exactly why i'm paying|thursday|store|community|neighbor|porch light|folks see", end + "\n" + full[-max(1, len(full) // 3):])),
    }
    labels = {
        "opening_juxtaposes_apparent_support_with_material_neglect": "the story does not establish the central contradiction that money/support is being sent while the elder materially lacks food, medicine, or autonomy",
        "elder_has_dignified_competence_work_history_and_selfhood": "the elder is only a victim rather than a person with craft, memory, labor, judgment, and selfhood",
        "proxy_control_is_material_not_only_mean": "the caregiver/proxy antagonism is interpersonal cruelty without concrete control over food, communication, medication, documents, or legal authority",
        "sender_initially_mistakes_money_transfer_for_care": "the remitting family member never confronts the difference between sending money and being present/attentive",
        "unannounced_witnessing_breaks_information_asymmetry": "the truth appears without an unannounced witnessing or verification event that breaks the information asymmetry",
        "capacity_attack_uses_falsified_medical_or_legal_procedure": "the antagonist does not weaponize medical/legal capacity procedure, or the procedure is too vague to investigate",
        "ordinary_records_and_witnesses_carry_exculpatory_power": "the reversal lacks ordinary records, ledgers, receipts, signatures, phone records, or witnesses",
        "elder_speaks_for_herself_in_the_reversal": "the elder does not speak for herself; others simply rescue or interpret her",
        "restitution_revokes_false_authority_and_restores_control": "the resolution does not revoke false authority, stop the asset transfer, or restore legal/financial control",
        "ending_converts_money_into_consented_presence_and_care_infrastructure": "the ending substitutes gifts or punishment for consented presence, care infrastructure, and ongoing participation",
        "community_dignity_is_repaired_not_only_villain_punished": "community dignity is not repaired; only the villain is punished",
    }
    warnings = [label for key, label in labels.items() if not checks[key]]
    return {
        "applies": True,
        "score_0_to_1": round(sum(checks.values()) / len(checks), 3),
        "warnings": warnings,
        "checks": checks,
        "craft_rule": "Elder-remittance exploitation works when apparent financial support coexists with material neglect, the elder retains craft/judgment/selfhood, proxy control is material and procedural, the sender confronts money-as-insufficient-care, unannounced witnessing breaks misinformation, capacity attacks use falsified medical/legal documents, ordinary records and witnesses reverse them, the elder speaks for herself, false authority is revoked, and the ending converts money into consented presence plus community dignity.",
    }
