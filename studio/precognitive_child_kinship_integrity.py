"""Precognitive child kinship integrity checks from Evening Star evidence."""
from __future__ import annotations
import re
from typing import Any

def _text(v:Any)->str:
    if isinstance(v,str):return v
    if isinstance(v,dict):return '\n'.join(_text(x) for x in v.values())
    if isinstance(v,list):return '\n'.join(_text(x) for x in v)
    return ''

def evaluate_precognitive_child_kinship_integrity(premise:dict[str,Any],architecture:dict[str,Any],scenes:list[dict[str,Any]])->dict[str,Any]:
    full='\n'.join([_text(premise),_text(architecture),_text(scenes)]).lower()
    child=bool(re.search(r'\b(?:child|daughter|girl|six-year-old|6-year-old|kid)\b',full))
    precog=bool(re.search(r'death countdown|countdown|predict\w*[^.\n]{0,50}death|saw it|vision|flash of it|about to die|get hurt',full))
    kinship=bool(re.search(r'real dad|father|paternity|dna|kinship|parent|family',full))
    if not(child and precog and kinship):return {'applies':False,'score_0_to_1':1.0,'warnings':[],'checks':{}}
    ending_parts=[]
    if isinstance(architecture,dict):
        for k,v in architecture.items():
            if re.search(r'ending|final|closing|resolution|epilogue|payoff',str(k).lower()):ending_parts.append(_text(v).lower())
        seq=architecture.get('sequences') or architecture.get('sequence')
        if isinstance(seq,list) and seq:ending_parts.append(_text(seq[-1]).lower())
    arch=_text(architecture).lower();end='\n'.join(ending_parts+([_text(scenes[-1]).lower()] if scenes else [])) or (arch[-max(1,len(arch)//3):] if arch else '')
    checks={
      'precognition_opens_with_concrete_countdown_and_preventable_harm':bool(re.search(r'three,? two,? one|countdown|only have .*minute|about to die|going to die|explosion|shot',full)),
      'child_has_independent_quest_and_social_vulnerability':bool(re.search(r'find my dad|looking for (?:my )?(?:dad|father)|foster home|ran away|orphan|no family|stray',full)),
      'power_has_cost_instability_or_uncertainty':bool(re.search(r'unstable|temporary rebound|can.?t test|don.?t know|no more using|gone|normal now|risk yourself|dizzy',full)),
      'kinship_is_contested_through_tamperable_procedure_notinstant_acceptance':bool(re.search(r'dna|paternity|lab|report|tamper|0%|valid blood evidence|test will be redone',full)),
      'independent_objects_records_and_witnesses_corroborate_identity':bool(re.search(r'necklace|carved|death certificate|hospital records?|security footage|payment|foundation account|ring|witness|nurse|ip',full)),
      'adults_protect_child_without_using_or_owning_her':bool(re.search(r'no more using .*pr|permission|safety|under my protection|not my bodyguard|normal six-year-old|protect you',full)),
      'child_truth_telling_has_social_power_but_also_consequences':bool(re.search(r'i don.?t lie|telling the truth|live stream|ruined|comments|misunderstood|great memory',full)),
      'antagonist_conspiracy_has_inheritance_or_control_motive':bool(re.search(r'company|inherit|blackwood|foundation|trust|taking back|ended up back in my hands|kidnap|death certificate',full)),
      'resolution_uses_live_evidence_police_and_procedural_trace':bool(re.search(r'police|live evidence|security footage|traffic camera|payment|digital certificate|search|confess|admitting|surrounded',end+'\n'+full[-max(1,len(full)//3):])),
      'ending_rejects_child_as_utility_and_restores_ordinary_belonging':bool(re.search(r'not my bodyguard|don.?t love you because you can save|normal six-year-old|eat cake|go to school|never be alone|family together|right here beside you',end)),
    }
    labels={
      'precognition_opens_with_concrete_countdown_and_preventable_harm':'precognition is vague exposition rather than immediate preventable harm with a visible countdown',
      'child_has_independent_quest_and_social_vulnerability':'the child has no independent quest or social vulnerability beyond being a plot device',
      'power_has_cost_instability_or_uncertainty':'the power is unlimited convenience rather than costly, unstable, or uncertain',
      'kinship_is_contested_through_tamperable_procedure_notinstant_acceptance':'kinship is accepted instantly or by one test rather than contested through tamperable procedure',
      'independent_objects_records_and_witnesses_corroborate_identity':'identity lacks corroborating objects, records, witnesses, or provenance beyond a single lab result',
      'adults_protect_child_without_using_or_owning_her':'adult protection becomes ownership, publicity use, or dependence on the child as a bodyguard/tool',
      'child_truth_telling_has_social_power_but_also_consequences':'the child’s truth-telling neither disrupts adult image-management nor creates consequences',
      'antagonist_conspiracy_has_inheritance_or_control_motive':'the conspiracy lacks a material inheritance/control motive',
      'resolution_uses_live_evidence_police_and_procedural_trace':'resolution lacks live evidence, police procedure, or traceable records',
      'ending_rejects_child_as_utility_and_restores_ordinary_belonging':'the ending keeps the child valuable only for power rather than restoring ordinary belonging',
    }
    warnings=[v for k,v in labels.items() if not checks[k]]
    return {'applies':True,'score_0_to_1':round(sum(checks.values())/len(checks),3),'warnings':warnings,'checks':checks,'craft_rule':'Precognitive-child kinship stories work when a concrete preventable death opens the bond, the child has an independent family quest, the power is unstable/costly, kinship survives tampered procedure through independent objects/records/witnesses, adults protect without using or owning the child, conspiracy has material inheritance motives, resolution uses live evidence and police traces, and the ending depowers utility into ordinary family belonging.'}
