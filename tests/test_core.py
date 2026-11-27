from studio.features import title_features
from studio.failure_intelligence import candidate_flags, evaluate_patterns
from studio.media_analysis import parse_ttml


def test_title_features_detect_core_engine():
    features = title_features("They Rejected a Worthless Half-Blood Girl… Unaware She Was the DRAGON KING'S Secret Daughter!")
    assert features["protagonist_gender"] == "female"
    assert features["victimization"]["present"]
    assert features["hidden_identity_or_secret"]["present"]
    assert features["themes"]["dragon"]["present"]
    assert features["themes"]["family_child"]["present"]
    assert features["title_structure"]["setup_then_reversal"]


def test_failure_pattern_revenge_without_belonging():
    flags = candidate_flags("They Betrayed Her So She Returned as the Supreme Wolf Empress to Take It All Back")
    flags["weak_family_child"] = True
    matches = evaluate_patterns(flags)
    assert any(match["id"] == "revenge_without_belonging" for match in matches)


def test_parse_ttml_fixture(tmp_path):
    fixture = tmp_path / "captions.ttml"
    fixture.write_text('''<tt xmlns="http://www.w3.org/ns/ttml"><body><div><p begin="00:00:01.000" end="00:00:02.500">Hello world</p></div></body></tt>''', encoding="utf-8")
    cues = parse_ttml(fixture)
    assert cues == [{"start": 1.0, "end": 2.5, "text": "Hello world"}]


def test_provider_inventory_contains_validated_cloudflare_modalities():
    from studio.providers import inventory
    rows = inventory()
    assert any(row["provider"] == "cloudflare_workers_ai" and row["modality"] == "text_to_image" and "smoke passed" in row["validation_status"] for row in rows)
    assert any(row["modality"] == "video_generation" and "no video-generation model" in row["validation_status"] for row in rows)


def test_thumbnail_concepts_generate_and_critique():
    from studio.thumbnail_concepts import critique_concept, generate_concepts
    concepts = generate_concepts({"title": "The dragon child they abandoned", "genre": "fantasy drama", "creature_or_child_anchor": "dragon child", "protector": "outcast mother", "wound": "abandonment"})
    assert concepts[0]["concept_id"] == "vulnerable_bond_scale"
    critique = critique_concept(concepts[0])
    assert critique["score_0_to_1"] > 0.5
    assert "CTR" in critique["ctr_caveat"]


def test_cross_channel_spectacle_pattern():
    script = "Earthquake. Global disaster. Cities collapse. Armies move. The planet shakes." * 20
    flags = candidate_flags("Earthquake: The End of the World", script)
    matches = evaluate_patterns(flags)
    assert any(match["id"] == "spectacle_scale_without_relational_anchor" for match in matches)


def test_format_strategy_warns_fragmented_long_episode():
    from studio.format_strategy import format_strategy
    result = format_strategy(42, "Episode 08 continues the journey across the island. To be continued.")
    assert result["format_class"] == "mid_length_feature"
    assert result["warnings"]
    assert any("continuation" in rec.lower() for rec in result["recommendations"])


def test_channel_contract_fit_creature_protection():
    from studio.channel_contracts import evaluate_channel_fit
    result = evaluate_channel_fit("A mother protects a baby dragon child from hunters", "creature_protection_feature")
    assert result["status"] == "pass"
    assert "dragon" in result["matched_positive_signals"]


def test_thumbnail_channel_contract_concepts():
    from studio.thumbnail_concepts import generate_concepts
    mythic = generate_concepts({"title": "Sinbad storm voyage", "genre": "mythic adventure", "channel_contract": "mythic_adventure"})
    assert any(c["concept_id"] == "mythic_survival_scale" for c in mythic)
    korean = generate_concepts({"title": "The regressed empress secret", "genre": "romance", "channel_contract": "korean_niche_microdrama"})
    assert any(c["concept_id"] == "niche_face_tension" for c in korean)
    explorer = generate_concepts({"title": "The hidden tiny kingdom", "genre": "fantasy adventure", "channel_contract": "exploration_wonder_feature"})
    assert any(c["concept_id"] == "hidden_world_scale" for c in explorer)
    survival = generate_concepts({"title": "Giant insect island", "genre": "survival thriller", "channel_contract": "hostile_survival_spectacle"})
    assert any(c["concept_id"] == "ordinary_human_vs_impossible_threat" for c in survival)


def test_production_economics_estimates_iteration_cost():
    from studio.production_economics import estimate_video_budget
    result = estimate_video_budget(48, 8)
    assert result["mixed_pipeline_example"]["iteration_adjusted_cost_estimate"] > 100
    assert result["single_pass_scenarios"][0]["documented_usd_per_second"] == 0.02


def test_opening_conversion_detects_admin_drag():
    from studio.production import opening_conversion_quality
    weak = opening_conversion_quality({"opening_event": {"first_5_minutes": "They verify the file, inspect records, check proof, and negotiate the contract."}})
    assert weak["warnings"]
    strong = opening_conversion_quality({"opening_event": {"first_5_minutes": "A mocked child is threatened by bullies, then a protective father rescues her and promises truth and belonging."}})
    assert not strong["warnings"]


def test_shot_pipeline_builds_lanes_and_ratio():
    from studio.shot_pipeline import build_shot_plan
    scenes = [{"scene_id": "S01", "time_range": "0-5 minutes", "objective": "protect the dragon child", "conflict": "soldiers attack", "turn": "creature reveal", "protagonist_decision": "shield it", "visual_action": {"first_image": "creature in danger", "face_reaction": "fear", "final_image": "public dragon reveal"}}]
    plan = build_shot_plan(scenes, 5)
    assert plan["shot_count"] >= 30
    assert plan["planned_generated_to_final_ratio"] > 0
    assert any(shot["generation_lane"] == "hero" for shot in plan["shots"])
    assert plan["coverage_scope"] == "continuous_preproduction_scaffold"
    assert plan["planned_generated_to_final_ratio"] > 0.9


def test_title_intelligence_creature_contract():
    from studio.title_intelligence import critique_title, generate_title_candidates
    premise = {"channel_contract": "creature_protection_feature", "protagonist": {"identity": "Mira Vale, keeper"}, "emotional_engine": {"wound": "disgrace", "injustice": "hunters", "protective_counterforce": "protector", "belonging_payoff": "home"}, "logline": "a dragon child is protected"}
    rows = generate_title_candidates(premise)
    assert rows and rows[0]["critique"]["score_0_to_1"] > 0.5
    weak = critique_title("Epic Fantasy World Adventure")
    assert weak["risks"]


def test_dialogue_craft_flags_exposition():
    from studio.dialogue_craft import critique_lines
    result = critique_lines(["As you know, the prophecy says our kingdom was founded years ago.", "Let me explain the legend says our world is ending."], 1)
    assert result["warnings"]
    strong = critique_lines(["I won't let them take her.", "Then choose. Protect her or expose me."], 1)
    assert strong["power_action_line_count"] == 2


def test_release_learning_percentile_and_revisions():
    from studio.release_learning import release_postmortem
    cohort=[{"views_per_day":100},{"views_per_day":200},{"views_per_day":1000},{"views_per_day":10000}]
    result=release_postmortem({"video_id":"x","views":100,"age_days":1},{"format_strategy":{"warnings":["w"]}},cohort)
    assert result["outcome_vs_cohort"]=="underperforming_cohort"
    assert result["revision_rules"]


def test_exact_storyboard_validation():
    from studio.storyboard import validate_storyboard_file
    result=validate_storyboard_file("examples/stormglass_keepers/storyboards/S01_storyboard.json")
    assert result["valid"], result["errors"]
    assert result["shot_count"] >= 30
    assert result["covered_seconds"] == 300


def test_agency_intelligence_flags_passive_rescue():
    from studio.agency_intelligence import evaluate_agency
    weak=evaluate_agency({"logline":"A poor humiliated orphan is rescued and married by a billionaire king."},[])
    assert weak["warnings"]
    assert weak["score_0_to_1"] < 0.6


def test_sound_design_gate():
    from studio.sound_design import evaluate_sound_design
    weak=evaluate_sound_design([{"scene_id":"x","sound_design":{"music_function":"constant music"}}])
    assert weak["warnings"]


def test_sound_design_gate_allows_negated_wallpaper_rule():
    from studio.sound_design import evaluate_sound_design
    good=evaluate_sound_design([{"scene_id":"x","sound_design":{"dialogue_priority":"dialogue remains intelligible","music_function":"motif evolves rather than constant emotional wallpaper","silence_or_negative_space":"drop music before revelation","motif":"three-note motif evolves"}}])
    assert not good["warnings"]


def test_evaluate_project_marks_missing_artifacts_and_empty_titles(tmp_path):
    import json
    from studio.production import evaluate_project
    premise={"premise_id":"x","title_candidates":[],"logline":"A child chooses to protect a creature.","audience_promise":"x","target_minutes":30,"release_format":"mid_length_feature","channel_contract":"creature_protection_feature","emotional_engine":{"wound":"x","want":"x","need":"x","injustice":"x","protective_counterforce":"x","belonging_payoff":"x"},"opening_event":{"first_10_seconds":"child threat","first_60_seconds":"protect child","first_5_minutes":"soldier threat reveal","dramatic_question":"can they escape danger"}}
    path=tmp_path/"premise.json";path.write_text(json.dumps(premise),encoding="utf8")
    result=evaluate_project(path,None,None,[])
    assert result["gates"]["B_architecture"]=="missing"
    assert result["gates"]["C_screenplay"]=="missing"
    assert result["failure_intelligence"]["candidate"]=="x"


def test_safe_filename_component_preserves_outer_underscores():
    from tools.download_piped_archive import safe_filename_component
    assert safe_filename_component("_I5I1l7DP3E") == "_I5I1l7DP3E"
    assert safe_filename_component("../x") == "_x"

def test_meaning_carrier_explicit_passes_and_missing_fails():
    from studio.meaning_carrier import evaluate_meaning_carrier
    premise = {"meaning_carrier": {"object_or_space": "bread", "opening_meaning": "charity under humiliation", "closing_reversal": "shared family table", "final_sequence_use": "bread returns as chosen belonging"}}
    architecture={"sequences":[{"turn":"ending","visual_setpiece":"bread returns at the family table"}]}
    assert evaluate_meaning_carrier(premise, architecture)["score_0_to_1"] == 1.0
    weak = evaluate_meaning_carrier({"opening_event": {"first_10_seconds": "abstract royal politics"}}, {})
    assert weak["score_0_to_1"] < 1.0
    assert weak["warnings"]

def test_relational_contract_gate():
    from studio.relational_contract import evaluate_relational_contract
    good = {"relational_contract": {"power_asymmetry": "x", "safety_or_kindness_before_power": "she protects him before knowing his power", "costly_protagonist_action": "x", "consent_or_personhood_repair": "he is free to choose", "payoff_image": "shared home"}}
    assert evaluate_relational_contract(good)["score_0_to_1"] == 1.0
    assert evaluate_relational_contract({})["warnings"]

def test_exact_storyboards_s01_to_s08_valid():
    from studio.storyboard import validate_storyboard_file
    expected = {"S01": 300.0, "S02": 300.0, "S03": 360.0, "S04": 360.0, "S05": 360.0, "S06": 420.0, "S07": 420.0, "S08": 360.0}
    for scene, seconds in expected.items():
        result = validate_storyboard_file(f"examples/stormglass_keepers/storyboards/{scene}_storyboard.json")
        assert result["valid"], result
        assert result["covered_seconds"] == seconds

def test_director_seed_storyboards_continuous():
    from pathlib import Path
    from studio.storyboard import validate_storyboard_file
    files = sorted(Path("examples/stormglass_keepers/director_seed_storyboards").glob("*.json"))
    assert len(files) == 8
    for path in files:
        assert validate_storyboard_file(path)["valid"], path

def test_malformed_contract_sections_do_not_abort_and_score_zero():
    from studio.meaning_carrier import evaluate_meaning_carrier
    from studio.relational_contract import evaluate_relational_contract
    assert evaluate_meaning_carrier({"meaning_carrier": "bread"}, {})["score_0_to_1"] == 0.0
    assert evaluate_relational_contract({"relational_contract": ["x"]})["score_0_to_1"] == 0.0


def test_meaning_carrier_requires_architecture_evidence_of_recurrence():
    from studio.meaning_carrier import evaluate_meaning_carrier
    premise = {"meaning_carrier": {"object_or_space": "bread", "opening_meaning": "humiliation", "closing_reversal": "belonging", "final_sequence_use": "declared but absent"}}
    result = evaluate_meaning_carrier(premise, {"sequences": [{"turn": "family dinner", "visual_setpiece": "gold hall"}]})
    assert result["score_0_to_1"] < 1.0
    assert any("final two architecture" in w for w in result["warnings"])


def test_relational_contract_rejects_after_reveal_and_denied_choice():
    from studio.relational_contract import evaluate_relational_contract
    base = {"power_asymmetry": "x", "costly_protagonist_action": "x", "payoff_image": "shared home"}
    late = dict(base, safety_or_kindness_before_power="she protects him after learning he is king", consent_or_personhood_repair="he is free to choose")
    assert any("after the power or identity reveal" in w or "temporally explicit" in w for w in evaluate_relational_contract({"relational_contract": late})["warnings"])
    denied = dict(base, safety_or_kindness_before_power="she protects him before knowing his power", consent_or_personhood_repair="he is not free to choose")
    assert any("explicitly denies" in w for w in evaluate_relational_contract({"relational_contract": denied})["warnings"])


def test_meaning_carrier_matches_short_object_names():
    from studio.meaning_carrier import evaluate_meaning_carrier
    premise={"meaning_carrier":{"object_or_space":"ring","opening_meaning":"coercion","closing_reversal":"chosen commitment","final_sequence_use":"ring returns"}}
    result=evaluate_meaning_carrier(premise,{"sequences":[{"turn":"ending","visual_setpiece":"the ring is returned openly"}]})
    assert result["score_0_to_1"] == 1.0


def test_relational_contract_allows_past_coercion_contrasted_with_repair():
    from studio.relational_contract import evaluate_relational_contract
    good={"relational_contract":{"power_asymmetry":"x","safety_or_kindness_before_power":"she feeds him before knowing his status","costly_protagonist_action":"x","consent_or_personhood_repair":"she once had no choice, but the ending restores her freedom to choose","payoff_image":"shared home"}}
    assert not evaluate_relational_contract(good)["warnings"]
    bad={"relational_contract":{"power_asymmetry":"x","safety_or_kindness_before_power":"she feeds him before knowing his status","costly_protagonist_action":"x","consent_or_personhood_repair":"he is not free to choose","payoff_image":"shared home"}}
    assert any("explicitly denies" in w for w in evaluate_relational_contract(bad)["warnings"])


def test_relational_contract_interprets_afterward_and_initially_correctly():
    from studio.relational_contract import evaluate_relational_contract
    base={"power_asymmetry":"x","costly_protagonist_action":"x","consent_or_personhood_repair":"he is free to choose","payoff_image":"shared home"}
    afterward=dict(base,safety_or_kindness_before_power="she feeds him; only afterward does she learn he is king")
    assert not any("after the power" in w or "temporally explicit" in w for w in evaluate_relational_contract({"relational_contract": afterward})["warnings"])
    late=dict(base,safety_or_kindness_before_power="she initially avoids him; after learning he is king, she protects him")
    assert any("after the power or identity reveal" in w for w in evaluate_relational_contract({"relational_contract": late})["warnings"])


def test_meaning_carrier_uses_exact_words_and_preserves_space_carrier():
    from studio.meaning_carrier import evaluate_meaning_carrier
    base={"object_or_space":"ring","opening_meaning":"coercion","closing_reversal":"chosen commitment","final_sequence_use":"ring returns"}
    no_match=evaluate_meaning_carrier({"meaning_carrier":base},{"sequences":[{"turn":"ending","visual_setpiece":"she brings the news"}]})
    assert any("final two architecture" in w for w in no_match["warnings"])
    space=dict(base,object_or_space="space",final_sequence_use="returns to space")
    match=evaluate_meaning_carrier({"meaning_carrier":space},{"sequences":[{"turn":"ending","visual_setpiece":"they return to open space"}]})
    assert not any("final two architecture" in w for w in match["warnings"])


def test_relational_contract_tracks_final_denial_state_and_prior_discovery():
    from studio.relational_contract import evaluate_relational_contract
    base={
      "power_asymmetry":"king and servant",
      "safety_or_kindness_before_power":"she shelters him prior to discovering that he is king",
      "costly_protagonist_action":"she loses her home protecting him",
      "consent_or_personhood_repair":"she was free to choose, but now she has no choice",
      "payoff_image":"mutual trust"
    }
    result=evaluate_relational_contract({"relational_contract":base})
    assert any("denies choice" in w for w in result["warnings"])
    assert not any("temporally explicit" in w for w in result["warnings"])
    repaired=dict(base,consent_or_personhood_repair="she once had no choice, but now she freely chooses")
    assert not any("denies choice" in w for w in evaluate_relational_contract({"relational_contract":repaired})["warnings"])
    repeated=dict(base,consent_or_personhood_repair="she once had no choice but learned trust; now she has no choice")
    assert any("denies choice" in w for w in evaluate_relational_contract({"relational_contract":repeated})["warnings"])

def test_meaning_carrier_unicode_and_specific_location_matching():
    from studio.meaning_carrier import evaluate_meaning_carrier
    base={"opening_meaning":"unsafe","closing_reversal":"belonging","final_sequence_use":"returns"}
    cafe=dict(base,object_or_space="café")
    result=evaluate_meaning_carrier({"meaning_carrier":cafe},{"sequences":[{"visual_setpiece":"they reopen the café together"}]})
    assert not any("final two architecture" in w for w in result["warnings"])
    rehearsal=dict(base,object_or_space="rehearsal space")
    bad=evaluate_meaning_carrier({"meaning_carrier":rehearsal},{"sequences":[{"visual_setpiece":"they make space at the table"}]})
    assert any("final two architecture" in w for w in bad["warnings"])
    good=evaluate_meaning_carrier({"meaning_carrier":rehearsal},{"sequences":[{"visual_setpiece":"the rehearsal fills with light"}]})
    assert not any("final two architecture" in w for w in good["warnings"])

def test_relational_contract_denial_scope_regressions():
    from studio.relational_contract import denial_is_unresolved
    assert denial_is_unresolved("she has no choice; she no longer wears the ring")
    assert not denial_is_unresolved("she is finally free to choose; earlier she had no choice")
    assert denial_is_unresolved("she once had no choice but learned trust; now she has no choice")


def test_meaning_carrier_prefers_object_over_provenance():
    from studio.meaning_carrier import evaluate_meaning_carrier
    carrier={"object_or_space":"ring from her mother","opening_meaning":"loss","closing_reversal":"recovered belonging","final_sequence_use":"ring returns"}
    result=evaluate_meaning_carrier({"meaning_carrier":carrier},{"sequences":[{"visual_setpiece":"the ring returns to her hand"}]})
    assert not any("final two architecture" in w for w in result["warnings"])

def test_relational_contract_flashback_and_lifted_denial_regressions():
    from studio.relational_contract import denial_is_unresolved
    assert denial_is_unresolved("at the payoff she has no choice. once she was free")
    assert not denial_is_unresolved("she has no choice. later she is no longer denied choice")


def test_meaning_carrier_compound_prop_uses_head_object():
    from studio.meaning_carrier import evaluate_meaning_carrier
    carrier={"object_or_space":"ring box","opening_meaning":"hidden obligation","closing_reversal":"open commitment","final_sequence_use":"box returns"}
    bad=evaluate_meaning_carrier({"meaning_carrier":carrier},{"sequences":[{"visual_setpiece":"the ring flashes in the crowd"}]})
    assert any("final two architecture" in w for w in bad["warnings"])
    good=evaluate_meaning_carrier({"meaning_carrier":carrier},{"sequences":[{"visual_setpiece":"the empty box is opened again"}]})
    assert not any("final two architecture" in w for w in good["warnings"])


def test_relational_contract_flashback_repair_and_present_contrast_regressions():
    from studio.relational_contract import denial_is_unresolved
    assert denial_is_unresolved("at the payoff she has no choice. earlier she was no longer denied choice")
    assert not denial_is_unresolved("she had no choice. she can now choose for herself, something she could not do before")


def test_meaning_carrier_prepositional_prop_keeps_main_object():
    from studio.meaning_carrier import evaluate_meaning_carrier
    carrier={"object_or_space":"key to the gate","opening_meaning":"captivity","closing_reversal":"release","final_sequence_use":"key returns"}
    bad=evaluate_meaning_carrier({"meaning_carrier":carrier},{"sequences":[{"visual_setpiece":"the gate stands open"}]})
    assert any("final two architecture" in w for w in bad["warnings"])
    good=evaluate_meaning_carrier({"meaning_carrier":carrier},{"sequences":[{"visual_setpiece":"the key turns once more"}]})
    assert not any("final two architecture" in w for w in good["warnings"])

def test_relational_contract_present_repair_with_past_comparison():
    from studio.relational_contract import denial_is_unresolved
    assert not denial_is_unresolved("she had no choice. she is no longer denied choice as she was before")
    assert not denial_is_unresolved("she had no choice. she can now choose for herself, something she could not do before")
    assert denial_is_unresolved("at the payoff she has no choice. earlier she was free at the start")


def test_compressed_format_requires_legible_engine():
    from studio.format_strategy import format_strategy
    result=format_strategy(11, "an abstract political conspiracy in a crystal kingdom")
    assert any("ultra-legible" in warning for warning in result["warnings"])
    result=format_strategy(11, "a giant father protects a baby from hunters")
    assert not any("ultra-legible" in warning for warning in result["warnings"])


def test_compressed_complete_feature_guidance_crosses_duration_labels():
    from studio.format_strategy import format_strategy
    short=format_strategy(11.67, "a giant father protects a baby from hunters")
    assert short["format_class"] == "short_feature"
    assert any("every scene should advance" in item for item in short["recommendations"])
    mid=format_strategy(35.07, "a scholarship student loves a hidden billionaire heir")
    assert any("every scene should advance" in item for item in mid["recommendations"])


def test_relational_contract_historical_denial_and_lifted_past():
    from studio.relational_contract import denial_is_unresolved
    assert not denial_is_unresolved("she had no choice before meeting him. later she freely chooses")
    assert denial_is_unresolved("she has no choice now. she was no longer denied choice in the past")
    assert not denial_is_unresolved("she had no choice. she is no longer denied choice as she was before")


def test_relational_contract_lifted_denial_with_comparative_past():
    from studio.relational_contract import denial_is_unresolved
    assert not denial_is_unresolved("she had no choice. she is no longer denied choice as she was in the past")
    assert denial_is_unresolved("she has no choice now. she was no longer denied choice in the past")


def test_abbreviated_episode_title_keeps_episode_guidance():
    from studio.format_strategy import format_strategy
    result=format_strategy(10, "Ep. 3 dragon child escapes hunters")
    assert result["format_class"] == "microdrama_episode"
    assert result["inferred_flags"]["serialized"] is True

def test_failure_intelligence_creature_action_requires_relational_bond():
    from studio.failure_intelligence import evaluate_candidate
    script=("A helicopter crashes. Something moving down there. A giant snake attacks and chases anonymous survivors through the jungle. "*30)+("The ape kills the snake and becomes ruler of the jungle. "*10)
    result=evaluate_candidate("Trapped by a giant snake until a colossal ape saved them",[],script)
    assert any(p["id"]=="creature_action_without_relational_bond" for p in result["matched_failure_patterns"])

def test_failure_intelligence_procedural_mission_pattern():
    from studio.failure_intelligence import evaluate_candidate
    script=("Commander, the outer line is gone. Eastern armor reserve ammunition. Deploy all operational units to the perimeter stronghold. "*30)+("The swarm is retreating. Mission complete. "*10)
    result=evaluate_candidate("Humans vs Vorraks final battle",[],script)
    assert any(p["id"]=="procedural_mission_without_emotional_payoff" for p in result["matched_failure_patterns"])


def test_creature_protection_thumbnail_concepts_include_personhood_and_hunt():
    from studio.thumbnail_concepts import generate_concepts
    concepts=generate_concepts({"channel_contract":"creature_protection_feature","genre":"creature fantasy drama","creature_or_child_anchor":"dragon child","protector":"disgraced keeper","wound":"hunted child","emotional_promise":"belonging"})
    ids={c["concept_id"] for c in concepts}
    assert "misunderstood_child_personhood" in ids
    assert "public_hunt_protection_triangle" in ids
    assert len(concepts) >= 3


def test_parse_ttml_supports_webvtt_word_timed_captions(tmp_path):
    from studio.media_analysis import parse_ttml
    p=tmp_path/'captions.vtt'
    p.write_text("WEBVTT\n\n00:00:01.000 --> 00:00:02.390 align:start position:0%\nGive<00:00:01.100><c> me</c><00:00:01.200><c> that.</c>\n\n00:00:02.390 --> 00:00:02.400\nGive me that.\n",encoding='utf8')
    cues=parse_ttml(p)
    assert cues[0]['start']==1.0
    assert 'Give me that.' in cues[0]['text']


def test_storyboard_production_manifest_export(tmp_path):
    from pathlib import Path
    from studio.storyboard_production import export_manifest
    out=export_manifest(Path('examples/stormglass_keepers/storyboards'),tmp_path,'stormglass')
    assert out['shot_count']==sum(x['shot_count'] for x in out['scenes'])
    assert out['lane_counts']['hero'] < out['shot_count'] * 0.5
    assert out['reference_assets']
    first=out['shots'][0]
    assert 'watermark' in first['negative_prompt']
    assert first['qa_checks']


def test_webvtt_drops_zero_duration_duplicate_caption(tmp_path):
    from studio.media_analysis import parse_ttml
    p=tmp_path/'captions.vtt'
    p.write_text("WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nHello there.\n\n00:00:02.000 --> 00:00:02.010\nHello there.\n",encoding='utf8')
    cues=parse_ttml(p)
    assert len(cues)==1


def test_spatial_status_detects_circular_inversion():
    from studio.spatial_status import evaluate_spatial_status
    good={
      "opening_event":{"first_10_seconds":"a maid kneels on the floor below the dinner table while the billionaire family sits and laughs"},
    }
    arch={"sequences":[{"time_range":"0-10","turn":"maid serves at table"},{"time_range":"70-80","turn":"the family chooses a floor mat because everybody fits"}],"ending_payoff":{"final_image":"the floor becomes chosen belonging at the family meal"}}
    result=evaluate_spatial_status(good,arch,[])
    assert result['score_0_to_1']>0.7
    assert not result['warnings']
    bad=evaluate_spatial_status({"opening_event":{"first_10_seconds":"a woman feels sad"}},{"sequences":[],"ending_payoff":{"final_image":"she becomes rich"}},[])
    assert bad['warnings']
    assert bad['score_0_to_1']<result['score_0_to_1']


def test_generated_social_premises_validate_and_score():
    from studio.premise_generator import generate_premises,evaluate_generated_premise
    from studio.production import validate_artifact
    from pathlib import Path
    import json,tempfile
    premises=generate_premises(count=3,target_minutes=42)
    assert len(premises)==3
    with tempfile.TemporaryDirectory() as d:
      path=Path(d)/'premise.json';path.write_text(json.dumps(premises[0],ensure_ascii=False),encoding='utf8')
      assert validate_artifact(path,'premise-packet.schema.json')==[]
    evaluation=evaluate_generated_premise(premises[0],[])
    assert evaluation['spatial_status']['score_0_to_1']>0.7
    assert evaluation['relational_contract']['score_0_to_1']>=0.8


def test_generated_scene_scaffold_schema_valid():
    import json,tempfile
    from pathlib import Path
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.production import validate_artifact
    premise=generate_premises(count=1)[0]
    scenes=generate_scenes(premise,generate_architecture(premise))
    assert len(scenes)==8
    with tempfile.TemporaryDirectory() as d:
      path=Path(d)/'scene.json';path.write_text(json.dumps(scenes[0],ensure_ascii=False),encoding='utf8')
      assert validate_artifact(path,'scene-screenplay.schema.json')==[]


def test_generated_storyboard_seeds_validate_continuous_nonuniform():
    from pathlib import Path
    from studio.storyboard import validate_storyboard_file
    import subprocess,sys,tempfile
    with tempfile.TemporaryDirectory() as d:
      subprocess.run([sys.executable,'-m','studio.cli','seed-storyboards','--scenes','examples/generated_concepts/glasswing_banquet_platform_scenes','--output-dir',d],check=True,capture_output=True)
      files=sorted(Path(d).glob('*_storyboard.json'))
      assert len(files)==8
      for path in files:
        result=validate_storyboard_file(path)
        assert result['valid']
        assert not any('nearly uniform' in w for w in result['warnings'])


def test_closure_integrity_requires_relational_payoff_before_sequel_hook():
    from studio.closure_integrity import evaluate_closure_integrity
    good={"relational_contract":{"payoff_image":"family chooses home, safety, love, and community repair"}}
    arch={"sequences":[{"sequence":1,"turn":"home recognition and chosen family safety"},{"sequence":2,"turn":"a new disturbance begins elsewhere"}]}
    bad={"sequences":[{"sequence":1,"turn":"their stories are just beginning beyond the stars"},{"sequence":2,"turn":"battle ends"}]}
    assert evaluate_closure_integrity(good,arch,[])['score_0_to_1']==1.0
    bad_result=evaluate_closure_integrity({},bad,[])
    assert any('sequel expansion' in w for w in bad_result['warnings'])
    assert any('relational/home' in w for w in bad_result['warnings'])


def test_closure_integrity_does_not_count_premise_promise_as_delivered():
    from studio.closure_integrity import evaluate_closure_integrity
    premise={"relational_contract":{"payoff_image":"family home recognition love safety"}}
    arch={"sequences":[{"sequence":1,"turn":"battle pressure"},{"sequence":2,"turn":"victory without payoff"}]}
    result=evaluate_closure_integrity(premise,arch,[])
    assert any('final movement' in w for w in result['warnings'])


def test_closure_integrity_uses_ending_payoff_as_delivered_evidence():
    from studio.closure_integrity import evaluate_closure_integrity
    arch={"sequences":[{"sequence":1,"turn":"battle pressure"},{"sequence":2,"turn":"victory"}],"ending_payoff":{"final_image":"the family returns home safe and chooses belonging"}}
    result=evaluate_closure_integrity({},arch,[])
    assert not any('final movement' in w for w in result['warnings'])


def test_closure_integrity_ignores_early_promise_before_final_hook_but_allows_same_sequence_order():
    from studio.closure_integrity import evaluate_closure_integrity
    early={"sequences":[{"sequence":1,"turn":"she promises home"},{"sequence":2,"turn":"middle turn"},{"sequence":3,"turn":"their stories are just beginning beyond the stars"}]}
    early_result=evaluate_closure_integrity({},early,[])
    assert any('sequel expansion' in w for w in early_result['warnings'])
    same={"sequences":[{"sequence":1,"turn":"middle turn"},{"sequence":2,"turn":"home recognition happens before their stories are just beginning"}]}
    same_result=evaluate_closure_integrity({},same,[])
    assert not any('sequel expansion' in w for w in same_result['warnings'])


def test_closure_integrity_ending_payoff_does_not_exclude_penultimate_sequence():
    from studio.closure_integrity import evaluate_closure_integrity
    arch={
      "sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":"their stories are just beginning beyond the stars"}],
      "ending_payoff":{"final_image":"the final image is quiet"}
    }
    result=evaluate_closure_integrity({},arch,[])
    assert any('sequel expansion' in w for w in result['warnings'])


def test_closure_integrity_dark_image_alone_is_not_system_collapse():
    from studio.closure_integrity import evaluate_closure_integrity
    arch={"sequences":[{"sequence":1,"turn":"water array established"},{"sequence":2,"turn":"family returns home safe as the room turns dark"}]}
    result=evaluate_closure_integrity({},arch,[])
    assert not any('infrastructure/system collapse' in w for w in result['warnings'])


def test_closure_integrity_rebuild_before_late_collapse_does_not_mask_missing_aftermath():
    from studio.closure_integrity import evaluate_closure_integrity
    arch={"sequences":[{"sequence":1,"turn":"the water array is restored and the town rebuilds"},{"sequence":2,"turn":"the water array collapses and the family comes home safe"}]}
    result=evaluate_closure_integrity({},arch,[])
    assert any('infrastructure/system collapse' in w for w in result['warnings'])


def test_closure_integrity_collapse_followed_by_repair_passes_and_personal_failing_is_not_outage():
    from studio.closure_integrity import evaluate_closure_integrity
    good={"sequences":[{"sequence":1,"turn":"the water array collapses"},{"sequence":2,"turn":"the community rebuilds a shared water system and the family comes home safe"}]}
    assert not any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},good,[])['warnings'])
    personal={"sequences":[{"sequence":1,"turn":"the flood shield is established"},{"sequence":2,"turn":"she is failing to persuade her father, but the family comes home safe"}]}
    assert not any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},personal,[])['warnings'])


def test_closure_integrity_screenplay_aftermath_counts_and_hypotheticals_do_not_collapse():
    from studio.closure_integrity import evaluate_closure_integrity
    arch={"sequences":[{"sequence":1,"turn":"middle turn"},{"sequence":2,"turn":"she destroys the water array during the climax"}]}
    scenes=[{"scene_id":"S07","turn":"pressure"},{"scene_id":"S08","turn":"the community rebuilds a shared water system and the family comes home safe"}]
    result=evaluate_closure_integrity({},arch,scenes)
    assert not any('infrastructure/system collapse' in w for w in result['warnings'])
    hypothetical={"sequences":[{"sequence":1,"turn":"middle turn"},{"sequence":2,"turn":"Will she disable the array? The family comes home safe"}]}
    assert not any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},hypothetical,[])['warnings'])


def test_closure_integrity_detects_shield_nodes_and_repeated_recovery_after_collapse():
    from studio.closure_integrity import evaluate_closure_integrity
    missing={"sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":"the shield nodes go dark; the family comes home safe"}]}
    assert any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},missing,[])['warnings'])
    repeated={"sequences":[{"sequence":1,"turn":"the town rebuilds early"},{"sequence":2,"turn":"the shield nodes go dark, then the community rebuilds the shield and comes home safe"}]}
    assert not any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},repeated,[])['warnings'])


def test_closure_integrity_conditionals_negation_and_scene_recovery_are_scoped():
    from studio.closure_integrity import evaluate_closure_integrity
    actual={"sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":"She can escape, but the array collapses"}]}
    assert any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},actual,[])['warnings'])
    for text in ["The shield nodes go dark if she leaves", "she does not disable the water array"]:
      arch={"sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":text+'; the family comes home safe'}]}
      assert not any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},arch,[])['warnings'])


def test_closure_integrity_scene_boilerplate_and_early_recovery_do_not_mask_late_collapse():
    from studio.closure_integrity import evaluate_closure_integrity
    arch={"sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":"she destroys the water array during the climax"}]}
    boiler=[{"scene_id":"S08","subtext":"Belonging is chosen when the wound-space becomes reversible and shared."}]
    early=[{"scene_id":"S08","turn":"the community rebuilds before the collapse"}]
    recovery=[{"scene_id":"S08","turn":"the community rebuilds a shared water system"}]
    assert any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},arch,boiler)['warnings'])
    assert any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},arch,early)['warnings'])
    assert not any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},arch,recovery)['warnings'])


def test_closure_integrity_positive_recovery_negation_timing_sharing_and_plans():
    from studio.closure_integrity import evaluate_closure_integrity
    failed={"sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":"she destroys the water array; the pumps are beyond repair"}]}
    assert any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},failed,[])['warnings'])
    timing={"sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":"she destroys the water array"}]}
    recovery_scene=[{"scene_id":"S08","turn":"Before dawn, the survivors rebuild the water supply"}]
    assert not any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},timing,recovery_scene)['warnings'])
    sharing_scene=[{"scene_id":"S08","turn":"the neighbors share their remaining supplies and keep everyone fed"}]
    assert not any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},timing,sharing_scene)['warnings'])
    planned={"sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":"she plans to enter the pump house and disable the array; the family comes home safe"}]}
    assert not any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},planned,[])['warnings'])


def test_closure_integrity_rejects_false_or_premature_recovery_and_unrelated_plan_actual_collapse():
    from studio.closure_integrity import evaluate_closure_integrity
    arch={"sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":"she destroys the water array"}]}
    for scene_text in ["neighbors can't share supplies", "neighbors share their remaining secrets", "Earlier, the community rebuilds the water supply"]:
      result=evaluate_closure_integrity({},arch,[{"scene_id":"S08","turn":scene_text}])
      assert any('infrastructure/system collapse' in w for w in result['warnings']), scene_text
    actual={"sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":"she plans to disable the pump, and the array collapses"}]}
    assert any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},actual,[])['warnings'])


def test_closure_integrity_questioned_second_clause_is_not_actual_collapse():
    from studio.closure_integrity import evaluate_closure_integrity
    arch={"sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":"Will she escape and the shield nodes go dark? the family comes home safe"}]}
    assert not any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},arch,[])['warnings'])


def test_creature_opening_dialogue_keeps_decision_with_protagonist():
    from studio.premise_generator import creature_economic_premise, CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    scene=generate_scenes(premise,generate_architecture(premise))[0]
    assert scene['dialogue_design']['key_lines'][1] == "I hide her first. Questions after she's safe."


def test_closure_integrity_aftermath_question_presupposes_actual_collapse():
    from studio.closure_integrity import evaluate_closure_integrity
    arch={"sequences":[{"sequence":1,"turn":"middle"},{"sequence":2,"turn":"What happens after the array collapses?"}]}
    assert any('infrastructure/system collapse' in w for w in evaluate_closure_integrity({},arch,[])['warnings'])


def test_visual_causality_flags_abstract_scenes_and_rewards_physical_action():
    from studio.visual_causality import evaluate_visual_causality
    abstract=[{"scene_id":"S01","visual_action":{"first_image":"power shifts emotionally","final_image":"meaning changes"}}]
    physical=[{"scene_id":"S01","visual_action":{"first_image":"the child crosses the pump yard and hides behind the woman","final_image":"the vial opens the gate as neighbors share water"}}]
    assert evaluate_visual_causality(abstract)['score_0_to_1'] < evaluate_visual_causality(physical)['score_0_to_1']
    assert evaluate_visual_causality(abstract)['warnings']


def test_dialogue_craft_requires_scene_opposition_scaffold():
    from studio.dialogue_craft import evaluate_scenes_dialogue
    scene={"scene_id":"S01","dialogue_design":{"key_lines":["I refuse."],"max_exposition_sentences":2}}
    result=evaluate_scenes_dialogue([scene])
    assert any('opposition scaffold' in w for w in result['warnings_by_scene']['S01'])


def test_thumbnail_concepts_creature_economic_vertical_scale_and_clutter_critique():
    from studio.thumbnail_concepts import generate_concepts, critique_concept
    concepts=generate_concepts({"channel_contract":"creature_economic_melodrama","genre":"fantasy drama","creature_or_child_anchor":"moonfin child","protector":"debt-bound baker"})
    quiet=[c for c in concepts if c['concept_id']=='quiet_vertical_protector_scale']
    assert quiet
    critique=critique_concept(quiet[0])
    assert 'mobile negative-space readability' in critique['strengths']
    cluttered={"composition":"monster versus army battle with crowd","emotion":"generic spectacle","palette":"red","text_direction":"episode prologue badge franchise text blocks"}
    assert len(critique_concept(cluttered)['risks']) >= 3


def test_sound_design_flags_generic_motif_and_requires_material_sources():
    from studio.sound_design import evaluate_sound_design
    generic=[{"scene_id":"S01","sound_design":{"dialogue_priority":"dialogue intelligible","music_function":"music enters on power change","silence_or_negative_space":"silence","motif":"a restrained tactile sound motif"}}]
    concrete=[{"scene_id":"S01","sound_design":{"dialogue_priority":"dialogue intelligible","music_function":"no heroic score before protection","silence_or_negative_space":"crowd clatter thins into creature breath and water droplets","motif":"glass vial taps, salt grains, and pump-stone resonance"}}]
    assert evaluate_sound_design(generic)['warnings']
    assert not evaluate_sound_design(concrete)['warnings']


def test_creature_opening_keeps_public_exclusion_visible():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    scene=generate_scenes(premise,generate_architecture(premise))[0]
    first=scene['visual_action']['first_image']
    assert 'barred from the public' in first
    assert 'crowd watches' in first


def test_key_objects_use_filmable_unlocking_actions():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[1])
    scenes=generate_scenes(premise,generate_architecture(premise))
    assert 'turns the blackened brass oven key in the' in scenes[2]['visual_action']['final_image']
    assert 'falls open' not in scenes[4]['visual_action']['final_image']
    assert 'ledger wall remains unlocked' in scenes[7]['visual_action']['final_image']


def test_thumbnail_concepts_read_nested_creature_premise_fields():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.thumbnail_concepts import generate_concepts
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    concepts=generate_concepts(premise)
    assert concepts[0]['creature_or_child_anchor']=='the moonfin child'
    assert concepts[0]['protector']
    assert concepts[0]['source_promise']==premise['audience_promise']


def test_thumbnail_nested_extraction_preserves_cast_and_moral_stakes():
    from studio.thumbnail_concepts import generate_concepts
    premise={
      "title_candidates":["Stormglass Keepers"],
      "audience_promise":"protection and belonging",
      "emotional_engine":{
        "protective_counterforce":"Mira repeatedly chooses the dragon child's safety over her own exile, freedom, and revenge.",
        "wound":"Mira is trapped by debt, housing insecurity, public shame, and the fear that survival may require exploiting someone weaker."
      },
      "relational_contract":{"safety_or_kindness_before_power":"Mira frees and shields the child before she knows whether it can help her, and calms it through care rather than command."}
    }
    concept=generate_concepts(premise)[0]
    assert concept['creature_or_child_anchor']=='the dragon child'
    assert concept['protector']=='Mira'
    assert 'exploiting someone weaker' in concept['source_wound']


def test_opening_quality_flags_fantasy_without_ordinary_anchor():
    from studio.production import opening_conversion_quality
    premise={"channel_contract":"dark fantasy creature feature","title_candidates":["The Rot"],"opening_event":{"first_10_seconds":"a legendary power awakens","first_60_seconds":"ancient magic threatens the realm","first_5_minutes":"a hidden identity is revealed","dramatic_question":"can the chosen one survive?"}}
    result=opening_conversion_quality(premise)
    assert any('ordinary survival/labor/resource anchor' in w for w in result['warnings'])
    grounded={"channel_contract":"creature_economic_melodrama","title_candidates":["Rot"],"opening_event":{"first_10_seconds":"a child is barred from the public water pump","first_60_seconds":"debt papers threaten the home","first_5_minutes":"she protects a creature while fetching water","dramatic_question":"can she save home without ownership?"}}
    assert not any('ordinary survival/labor/resource anchor' in w for w in opening_conversion_quality(grounded)['warnings'])


def test_opening_ordinary_anchor_matching_uses_word_boundaries():
    from studio.production import opening_conversion_quality
    premise={"channel_contract":"dark fantasy creature feature","title_candidates":["Crown"],"opening_event":{"first_10_seconds":"the current emperor summons a hidden power","first_60_seconds":"ancient magic threatens the realm","first_5_minutes":"a secret identity is exposed","dramatic_question":"can the chosen one survive?"}}
    result=opening_conversion_quality(premise)
    assert 'rent' not in result['ordinary_anchor_terms']
    assert any('ordinary survival/labor/resource anchor' in w for w in result['warnings'])


def test_creature_scenes_include_short_scene_specific_spoken_exchange():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.dialogue_craft import evaluate_scenes_dialogue
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    scenes=generate_scenes(premise,generate_architecture(premise))
    exchange=scenes[0]['dialogue_design']['spoken_exchange']
    assert len(exchange)==4
    assert exchange[0]['speaker']!=exchange[2]['speaker']
    assert 'Paying hands first, Nura' in exchange[0]['line']
    report=evaluate_scenes_dialogue(scenes)
    assert not report['warnings_by_scene']
    assert report['scenes'][0]['spoken_exchange_turn_count']==4


def test_storyboard_seed_uses_spoken_exchange_in_dialogue_shots():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.storyboard_seed import build_seed_board
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    scene=generate_scenes(premise,generate_architecture(premise))[0]
    board=build_seed_board(scene)
    dialogue_shots=[s for s in board['shots'] if s['dialogue']]
    assert any('Paying hands first, Nura' in s['dialogue'] for s in dialogue_shots)
    assert any("Under my shawl" in s['dialogue'] for s in dialogue_shots)
    assert any('crowd blocks the public resource threshold' in s['visual_action'] for s in dialogue_shots)


def test_storyboard_seed_does_not_repeat_exact_dialogue_line():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.storyboard_seed import build_seed_board
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    scene=generate_scenes(premise,generate_architecture(premise))[0]
    board=build_seed_board(scene)
    lines=[s['dialogue'] for s in board['shots'] if s['dialogue']]
    assert len(lines)==len(set(lines))


def test_dialogue_evaluation_reports_null_spoken_turn_without_crash():
    from studio.dialogue_craft import evaluate_scenes_dialogue
    report=evaluate_scenes_dialogue([{"scene_id":"S01","dialogue_design":{"key_lines":[],"spoken_exchange":[None],"max_exposition_sentences":2}}])
    assert 'spoken exchange turn 1 is malformed' in report['warnings_by_scene']['S01']


def test_repo_and_package_scene_schemas_stay_synchronized():
    from pathlib import Path
    assert Path('schemas/scene-screenplay.schema.json').read_text(encoding='utf8') == Path('studio/package_data/schemas/scene-screenplay.schema.json').read_text(encoding='utf8')


def test_creature_spoken_exchange_assigns_decisions_to_protagonist():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    scenes=generate_scenes(premise,generate_architecture(premise))
    for idx in [1,5]:
        exchange=scenes[idx]['dialogue_design']['spoken_exchange']
        decision=next(t for t in exchange if t['beat']=='protagonist_decision')
        assert decision['speaker']=='Nura'
    assert "Then I'll work" in next(t for t in scenes[1]['dialogue_design']['spoken_exchange'] if t['beat']=='protagonist_decision')['line']
    assert "walk beside me" in next(t for t in scenes[5]['dialogue_design']['spoken_exchange'] if t['beat']=='protagonist_decision')['line']


def test_storyboard_seed_falls_back_to_key_lines_without_spoken_exchange():
    from studio.storyboard_seed import build_seed_board
    scene={"scene_id":"S01","time_range":"0-5 minutes","objective":"objective","conflict":"conflict","turn":"turn","protagonist_decision":"decision","subtext":"subtext","visual_action":{"first_image":"first","face_reaction":"face","vertical_composition":"vertical","final_image":"final"},"dialogue_design":{"key_lines":["pressure line","decision line","objection line"]},"sound_design":{}}
    board=build_seed_board(scene)
    dialogue=[s['dialogue'] for s in board['shots'] if s['dialogue']]
    assert 'pressure line' in dialogue
    assert 'decision line' in dialogue
    assert 'objection line' in dialogue


def test_storyboard_seed_places_witness_objection_before_decision():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.storyboard_seed import build_seed_board
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    scene=generate_scenes(premise,generate_architecture(premise))[5]
    board=build_seed_board(scene)
    witness_idx=next(i for i,s in enumerate(board['shots']) if 'One pair of hands can bury it' in s['dialogue'])
    decision_idx=next(i for i,s in enumerate(board['shots']) if 'walk beside me' in s['dialogue'])
    assert witness_idx < decision_idx


def test_storyboard_seed_preserves_scripted_final_image():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.storyboard_seed import build_seed_board
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[1])
    scene=generate_scenes(premise,generate_architecture(premise))[2]
    board=build_seed_board(scene)
    final=board['shots'][-1]
    assert final['visual_action']==scene['visual_action']['final_image']
    assert final['dialogue']


def test_storyboard_seed_places_power_turn_after_causing_decision():
    import json
    from studio.storyboard_seed import build_seed_board
    scene=json.load(open('examples/stormglass_keepers/scenes/S02.json',encoding='utf8'))
    board=build_seed_board(scene)
    decision_idx=next(i for i,s in enumerate(board['shots']) if s['visual_action']==scene['protagonist_decision'])
    turn_idx=next(i for i,s in enumerate(board['shots']) if s['visual_action']==scene['turn'])
    assert decision_idx < turn_idx


def test_storyboard_seed_varies_repeated_turn_coverage():
    import json
    from studio.storyboard_seed import build_seed_board
    scene=json.load(open('examples/generated_creature_concepts/salt_window_garden_scenes/S01.json',encoding='utf8'))
    board=build_seed_board(scene)
    turn_visuals=[s['visual_action'] for s in board['shots'] if s['shot_size']=='turn wide']
    assert len(turn_visuals) > 1
    assert len(set(turn_visuals)) == len(turn_visuals)
    assert all('alternate coverage' in v for v in turn_visuals[1:])


def test_failure_intelligence_flags_modern_rebirth_without_clock_or_proof():
    from studio.failure_intelligence import evaluate_candidate
    script='Arthur is reborn after his billionaire company family betrays him. He is angry. They humiliate him again and again.'
    result=evaluate_candidate('Reborn billionaire heir disowns his company family and makes them pay',[],script)
    ids=[p['id'] for p in result['matched_failure_patterns']]
    assert 'modern_rebirth_revenge_without_clock_or_proof' in ids


def test_failure_intelligence_accepts_modern_rebirth_clock_and_proof():
    from studio.failure_intelligence import evaluate_candidate
    script='Arthur is reborn after his sisters betray him. Seven days remain on the contract. He keeps the files, bank records, waiver, needle scar, and red heels as evidence.'
    result=evaluate_candidate('Reborn heir disowns his sisters and makes them pay',[],script)
    ids=[p['id'] for p in result['matched_failure_patterns']]
    assert 'modern_rebirth_revenge_without_clock_or_proof' not in ids


def test_failure_intelligence_requires_both_rebirth_clock_and_proof():
    from studio.failure_intelligence import evaluate_candidate
    candidate='Reborn billionaire heir makes his company family pay'
    proof_only='Arthur is reborn after betrayal. He keeps contracts, bank records, photos, files, scars, and evidence.'
    clock_only='Arthur is reborn after betrayal. Seven days remain before the deadline.'
    for script in (proof_only,clock_only):
        result=evaluate_candidate(candidate,[],script)
        ids=[p['id'] for p in result['matched_failure_patterns']]
        assert 'modern_rebirth_revenge_without_clock_or_proof' in ids


def test_failure_intelligence_does_not_classify_fantasy_rebirth_as_modern_revenge():
    from studio.failure_intelligence import evaluate_candidate
    script='The reborn princess returns to the magic kingdom after her father betrayal and avenges the royal family.'
    result=evaluate_candidate('Reborn princess avenges her father betrayal',[],script)
    ids=[p['id'] for p in result['matched_failure_patterns']]
    assert 'modern_rebirth_revenge_without_clock_or_proof' not in ids


def test_creature_spoken_exchange_contains_scene_specific_subtext():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    scene=generate_scenes(premise,generate_architecture(premise))[0]
    exchange=scene['dialogue_design']['spoken_exchange']
    assert all(t.get('subtext') for t in exchange)
    assert exchange[0]['subtext'] != exchange[0]['line']
    assert 'illegality' in exchange[0]['subtext']


def test_creature_dialogue_uses_world_specific_material_proof_language():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    salt=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    ember=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[1])
    salt_scenes=generate_scenes(salt,generate_architecture(salt))
    ember_scenes=generate_scenes(ember,generate_architecture(ember))
    assert 'salt rises where her tears fall' in salt_scenes[0]['dialogue_design']['spoken_exchange'][3]['line']
    assert 'coals bend toward her crying' in ember_scenes[0]['dialogue_design']['spoken_exchange'][3]['line']
    assert 'Guild ration first' in ember_scenes[0]['dialogue_design']['spoken_exchange'][0]['line']
    assert 'coal ledger' in ember_scenes[2]['dialogue_design']['spoken_exchange'][0]['line']
    assert 'Salt inside this seal' in salt_scenes[3]['dialogue_design']['spoken_exchange'][3]['line']
    assert 'This seam is still hot' in ember_scenes[3]['dialogue_design']['spoken_exchange'][3]['line']

def test_hidden_identity_integrity_flags_status_only_reveal():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    premise={"title_candidates":["Poor Student Was Secretly a Billionaire Heir"],"opening_event":{"first_10_seconds":"a poor student enters elite school","first_60_seconds":"he is mocked","first_5_minutes":"his true identity appears"}}
    result=evaluate_hidden_identity_integrity(premise,{},[])
    assert result['applies']
    assert result['score_0_to_1']<0.7
    assert any('trust wound' in w for w in result['warnings'])


def test_hidden_identity_integrity_accepts_lioren_pattern():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    premise={"title_candidates":["She Fell in Love With a Poor Student, Not Knowing He Was a Billionaire Heir"],"opening_event":{"first_10_seconds":"a poor student is mocked but helps another student","first_60_seconds":"ordinary kindness over coffee and library study","first_5_minutes":"he corrects a valuation and proves competence"}}
    arch={"sequences":[{"turn":"competence and love grow before status"},{"turn":"the true identity reveal creates a trust wound because he lied"},{"turn":"he apologizes, uses wealth to save the university and protect vulnerable students"},{"turn":"chosen love, proposal, wedding, family and belonging matter more than wealth"}]}
    result=evaluate_hidden_identity_integrity(premise,arch,[])
    assert result['applies']
    assert result['score_0_to_1']>=0.8

def test_scale_community_integrity_flags_generic_battle_rescue():
    from studio.scale_community_integrity import evaluate_scale_community_integrity
    premise={"title_candidates":["A Hidden Tiny Kingdom"],"opening_event":{"first_5_minutes":"explorer finds tiny kingdom"}}
    arch={"sequences":[{"turn":"the outsider is instantly worshipped"},{"turn":"a final battle defeats the invaders"},{"turn":"the outsider leaves"}]}
    result=evaluate_scale_community_integrity(premise,arch,[])
    assert result['applies']
    assert result['score_0_to_1']<=0.4


def test_scale_community_integrity_accepts_drakenhart_pattern():
    from studio.scale_community_integrity import evaluate_scale_community_integrity
    premise={"title_candidates":["She Found a Hidden Tiny Kingdom in the Roots"],"opening_event":{"first_5_minutes":"explorer finds tiny kingdom and repairs an arch that saves the tunnel"}}
    arch={"sequences":[{"turn":"giant-world junk becomes roofs, tools, infrastructure and shared shelter"},{"turn":"the tiny community distrusts giants because earlier drilling flooded them and her report signs places away"},{"turn":"a map and proof make the drilling crew listen and shut it down"},{"turn":"years of rebuilding make it her chosen home; she returns every sunrise"}]}
    result=evaluate_scale_community_integrity(premise,arch,[])
    assert result['applies']
    assert result['score_0_to_1']>=0.8

