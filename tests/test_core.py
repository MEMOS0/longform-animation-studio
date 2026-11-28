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
    assert "Pump's for paying households, Nura" in exchange[0]['line']
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
    assert any("Pump's for paying households, Nura" in s['dialogue'] for s in dialogue_shots)
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
    assert "run beside me" in next(t for t in scenes[5]['dialogue_design']['spoken_exchange'] if t['beat']=='protagonist_decision')['line']


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
    witness_idx=next(i for i,s in enumerate(board['shots']) if 'Fast hands can bury proof' in s['dialogue'])
    decision_idx=next(i for i,s in enumerate(board['shots']) if 'run beside me' in s['dialogue'])
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
    assert all(t.get('power_move') and t.get('delivery') and t.get('status_shift') for t in exchange)
    assert 'scene_rhythm' in scene['dialogue_design']
    assert scene['dialogue_design']['rewrite_directives']


def test_creature_dialogue_uses_world_specific_material_proof_language():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    salt=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    ember=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[1])
    salt_scenes=generate_scenes(salt,generate_architecture(salt))
    ember_scenes=generate_scenes(ember,generate_architecture(ember))
    assert "Salt's rising" in salt_scenes[0]['dialogue_design']['spoken_exchange'][3]['line']
    assert "Coals are bending" in ember_scenes[0]['dialogue_design']['spoken_exchange'][3]['line']
    assert "Oven ration's for guild households" in ember_scenes[0]['dialogue_design']['spoken_exchange'][0]['line']
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
    arch={"sequences":[{"turn":"competence and love grow before status"},{"turn":"the true identity reveal creates a trust wound because he lied"},{"turn":"he apologizes, uses wealth to save the university and protect vulnerable students"},{"turn":"evidence records documents full disclosure; separate homes and boundaries; help requires consent, no tests, no surveillance; he proves compliance when inconvenient and asks her to choose me again with full truth"},{"turn":"chosen love, proposal, wedding, family and belonging matter more than wealth"}]}
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



def test_creature_dialogue_performance_notes_follow_actual_speaker_role():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    scenes=generate_scenes(premise,generate_architecture(premise))
    shelter_pressure=scenes[1]['dialogue_design']['spoken_exchange'][0]
    pain_cost=scenes[2]['dialogue_design']['spoken_exchange'][3]
    assert shelter_pressure['speaker']=='her grandmother'
    assert 'urgent help' in shelter_pressure['power_move']
    assert 'institutional demand' not in shelter_pressure['power_move']
    assert pain_cost['speaker']=='land trust'
    assert 'commodification threat' in pain_cost['power_move']
    assert 'restrained' not in pain_cost['delivery']


def test_media_analysis_removes_stale_contact_sheets_before_rerun():
    import inspect
    source=inspect.getsource(__import__('studio.media_analysis',fromlist=['sample_video_frames']).sample_video_frames)
    assert 'stale_sheet.unlink()' in source
    assert 'output_dir.glob("contact_*.jpg")' in source


def test_screenplay_renderer_produces_annotated_professional_draft():
    from studio.premise_generator import creature_economic_premise,CREATURE_ECONOMIC_VARIANTS
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.screenplay_renderer import render_screenplay
    premise=creature_economic_premise(CREATURE_ECONOMIC_VARIANTS[0])
    text=render_screenplay(premise,generate_scenes(premise,generate_architecture(premise)))
    assert 'Annotated Screenplay Draft' in text
    assert 'GLOBAL REWRITE RULES' in text
    assert 'SCENE SUBTEXT' in text
    assert 'GRANDMOTHER' in text
    assert 'NURA' in text
    assert "Pump's for paying households" in text
    assert 'FINAL IMAGE' in text
    assert 'EXIT HOOK' in text


def test_screenplay_renderer_preserves_default_key_lines_without_spoken_exchange():
    from studio.screenplay_renderer import render_scene
    scene={'scene_id':'S01','time_range':'0-5','objective':'test','power_position_start':'low','power_position_end':'high','visual_action':{},'sound_design':{},'edit_hook':{},'dialogue_design':{'key_lines':['I refuse to vanish.']}}
    text=render_scene(scene)
    assert 'KEY DIALOGUE' in text
    assert 'I refuse to vanish.' in text


def test_render_screenplay_scene_loader_accepts_file_and_rejects_empty_dir(tmp_path):
    from studio.cli import load_scene_inputs
    import json,pytest
    scene_file=tmp_path/'one.json'
    scene_file.write_text(json.dumps({'scene_id':'S01'}),encoding='utf8')
    assert load_scene_inputs(scene_file)==[{'scene_id':'S01'}]
    empty=tmp_path/'empty'
    empty.mkdir()
    with pytest.raises(ValueError):
        load_scene_inputs(empty)


def test_write_screenplay_creates_missing_output_directory(tmp_path):
    from studio.screenplay_renderer import write_screenplay
    target=tmp_path/'new'/'nested'/'draft.md'
    result=write_screenplay({'title_candidates':['Test'],'premise_id':'test'},[],target)
    assert result.exists()
    assert 'Annotated Screenplay Draft' in result.read_text(encoding='utf8')


def test_visual_causality_recognizes_survival_actions_and_objects():
    from studio.visual_causality import evaluate_visual_causality
    scene={'scene_id':'S01','visual_action':{'first_image':'the conductor crawls from the wrecked train as a giant centipede fills the tunnel','final_image':'she frees the trapped pigeon and locks the red lens into the light panel'}}
    result=evaluate_visual_causality([scene])
    assert result['scene_scores'][0]['first_action'] is True
    assert result['scene_scores'][0]['final_action'] is True
    assert result['scene_scores'][0]['concrete_image'] is True


def test_single_sparse_spoken_turn_is_valid_for_visual_first_scene():
    from studio.dialogue_craft import evaluate_scenes_dialogue
    scene={'scene_id':'S01','dialogue_design':{'key_lines':[],'opposition_beats':[{'beat':b} for b in ['external_pressure','witness_objection','protagonist_decision','evidence_or_cost']],'spoken_exchange':[{'beat':'protagonist_decision','speaker':'Ilsa','line':'Easy. I won\'t hurt you.','action':'she lowers her hand','subtext':'restraint proves safety'}]}}
    result=evaluate_scenes_dialogue([scene])
    assert not result['warnings_by_scene']


def test_compressed_survival_integrity_passes_generated_contract():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.compressed_survival_integrity import evaluate_compressed_survival_integrity
    premise=generate_premises('compressed_creature_survival',1,18)[0]
    result=evaluate_compressed_survival_integrity(premise,generate_architecture(premise),generate_scenes(premise,generate_architecture(premise)))
    assert result['applies'] is True
    assert result['score_0_to_1'] >= 0.75
    assert result['checks']['predator_and_innocent_or_ally_are_differentiated'] is True
    assert result['checks']['escape_converts_to_reciprocal_rescue'] is True


def test_seed_storyboard_does_not_repeat_sparse_dialogue_across_shots():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.storyboard_seed import build_seed_board
    premise=generate_premises('compressed_creature_survival',1,18)[0]
    scene=generate_scenes(premise,generate_architecture(premise))[2]
    board=build_seed_board(scene)
    lines=[shot.get('dialogue','') for shot in board['shots'] if shot.get('dialogue')]
    assert len(lines)==len(set(lines))
    assert lines.count("Easy. I won't hurt you.")<=1


def test_compressed_survival_integrity_partial_scene_draft_not_perfect():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.compressed_survival_integrity import evaluate_compressed_survival_integrity
    premise=generate_premises('compressed_creature_survival',1,18)[0]
    arch=generate_architecture(premise)
    scenes=generate_scenes(premise,arch)[:1]
    result=evaluate_compressed_survival_integrity(premise,arch,scenes)
    assert result['checks']['complete_scene_coverage'] is False
    assert result['score_0_to_1'] < 0.2
    assert any('incomplete' in w for w in result['warnings'])


def test_compressed_survival_architecture_uses_survival_midpoint_and_ending():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    premise=generate_premises('compressed_creature_survival',1,18)[0]
    arch=generate_architecture(premise)
    assert 'reciprocal rescue' in arch['midpoint_reversal']
    assert 'captives and the creature are freed' in arch['ending_payoff']['justice']
    assert 'frame-up' not in arch['midpoint_reversal']
    assert 'true manipulator' not in arch['ending_payoff']['justice']


def test_compressed_survival_integrity_duplicate_scene_does_not_count_twice():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.compressed_survival_integrity import evaluate_compressed_survival_integrity
    premise=generate_premises('compressed_creature_survival',1,18)[0]
    arch=generate_architecture(premise)
    scenes=generate_scenes(premise,arch)
    duplicate_draft=[scenes[0],dict(scenes[0])]
    result=evaluate_compressed_survival_integrity(premise,arch,duplicate_draft)
    assert result['unique_scene_count']==1
    assert result['checks']['complete_scene_coverage'] is False
    assert result['score_0_to_1'] < 0.2


def test_transformation_romance_contract_generates_and_integrity_passes():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.transformation_romance_integrity import evaluate_transformation_romance_integrity
    premise=generate_premises('transformation_romance',1,72)[0]
    arch=generate_architecture(premise)
    scenes=generate_scenes(premise,arch)
    result=evaluate_transformation_romance_integrity(premise,arch,scenes)
    assert result['applies'] is True
    assert result['score_0_to_1'] >= 0.9
    assert 'second performance arena' in arch['midpoint_reversal']
    assert scenes[5]['dialogue_design']['spoken_exchange'][0]['line']


def test_transformation_romance_duplicate_scene_does_not_count_twice():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.transformation_romance_integrity import evaluate_transformation_romance_integrity
    premise=generate_premises('transformation_romance',1,72)[0]
    arch=generate_architecture(premise)
    scenes=generate_scenes(premise,arch)
    result=evaluate_transformation_romance_integrity(premise,arch,[scenes[0],dict(scenes[0])])
    assert result['checks']['complete_scene_coverage'] is False
    assert result['score_0_to_1'] < 0.2


def test_transformation_visual_images_are_readable_by_causality_gate():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.visual_causality import evaluate_visual_causality
    premise=generate_premises('transformation_romance',1,72)[0]
    scenes=generate_scenes(premise,generate_architecture(premise))
    assert evaluate_visual_causality(scenes)['warnings']==[]


def test_compound_expansion_readiness_generated_creature_contracts():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.compound_expansion import evaluate_compound_expansion_readiness
    for contract,minutes in [('creature_economic_melodrama',32),('compressed_creature_survival',24)]:
        premise=generate_premises(contract,1,minutes)[0]
        arch=generate_architecture(premise)
        result=evaluate_compound_expansion_readiness(premise,arch,generate_scenes(premise,arch))
        assert result['applicable']
        assert result['score_0_to_1']==1.0
        assert 'not proof' in result['packaging_boundary']
        assert premise['packaging']['compound_expansion']['reuse_rule']


def test_compound_expansion_warns_when_closure_is_missing():
    from studio.compound_expansion import evaluate_compound_expansion_readiness
    premise={'target_minutes':24,'logline':'a dragon creature in a coal heat crisis'}
    arch={'sequences':[{'sequence':1,'turn':'the heat infrastructure collapses and the creature departs into mystery'}]}
    result=evaluate_compound_expansion_readiness(premise,arch,[])
    assert result['warnings']
    assert result['score_0_to_1']<1.0


def test_creature_pacing_generated_contracts_and_bad_loud_tail():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.creature_pacing import evaluate_creature_pacing
    premise=generate_premises('compressed_creature_survival',1,24)[0]
    arch=generate_architecture(premise)
    scenes=generate_scenes(premise,arch)
    assert evaluate_creature_pacing(premise,arch,scenes)['score_0_to_1']==1.0
    bad=[dict(scene) for scene in scenes]
    bad[-1]['sound_design']={'dialogue_priority':'dialogue intelligible','music_function':'constant music and generic epic loud throughout','silence_or_negative_space':'','motif':'wallpaper'}
    bad[-1]['visual_action']['final_image']='explosion spectacle continues without contact'
    result=evaluate_creature_pacing(premise,arch,bad)
    assert any('final scene' in warning or 'final sound design' in warning or 'ending' in warning for warning in result['warnings'])


def test_compound_serial_expansion_format_is_not_duration_causality():
    from studio.format_strategy import format_strategy
    result=format_strategy(47,'compound expansion with reused footage and prequel material','compound_serial_expansion')
    assert result['format_class']=='compound_serial_expansion'
    assert any('not proof that longer duration' in row for row in result['recommendations'])
    inferred=format_strategy(47,'compound expansion with reused footage','long_feature')
    assert any('duration is not mistaken' in warning for warning in inferred['warnings'])


def test_future_compound_expansion_guidance_does_not_reclassify_current_release():
    from studio.premise_generator import generate_premises,evaluate_generated_premise
    premise=generate_premises('compressed_creature_survival',1,24)[0]
    result=evaluate_generated_premise(premise,[])['format_strategy']
    assert result['format_class']=='short_feature'
    assert not any('compound/serial expansion' in warning or 'episodic labeling' in warning for warning in result['warnings'])


def test_compound_expansion_personal_safety_does_not_mask_infrastructure_collapse():
    from studio.compound_expansion import evaluate_compound_expansion_readiness
    premise={'target_minutes':24,'logline':'a dragon creature in a town where the water system collapses'}
    arch={'sequences':[{'sequence':1,'turn':'the water infrastructure collapse destroys the community supply'},{'sequence':2,'turn':'the creature gets safely home with the protagonist'}]}
    result=evaluate_compound_expansion_readiness(premise,arch,[])
    assert any('infrastructure' in warning or 'community survival' in warning for warning in result['warnings'])
    assert result['score_0_to_1']<1.0


def test_creature_contract_partial_opening_draft_not_perfect():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.compound_expansion import evaluate_compound_expansion_readiness
    from studio.creature_pacing import evaluate_creature_pacing
    premise=generate_premises('creature_economic_melodrama',1,32)[0]
    arch=generate_architecture(premise)
    opening_only=generate_scenes(premise,arch)[:1]
    compound=evaluate_compound_expansion_readiness(premise,arch,opening_only)
    pacing=evaluate_creature_pacing(premise,arch,opening_only)
    assert compound['score_0_to_1']<0.2
    assert pacing['score_0_to_1']<0.2
    assert any('partial scene draft' in warning for warning in compound['warnings'])
    assert any('partial scene draft' in warning for warning in pacing['warnings'])


def test_hidden_identity_integrity_reports_queenflix_accountability_extensions():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    premise={"title_candidates":["The CEO Faked Being Broke"],"opening_event":{"first_5_minutes":"ordinary kindness before status"}}
    arch={"sequences":[{"turn":"competence and love grow before status"},{"turn":"the true identity reveal creates a trust wound because he lied"},{"turn":"evidence records documents full disclosure; separate homes and boundaries; help requires consent, no tests, no surveillance; he proves compliance when inconvenient and asks her to choose me again with full truth"},{"turn":"chosen love family belonging wedding"}]}
    result=evaluate_hidden_identity_integrity(premise,arch,[])
    assert all(result['queenflix_accountability'].values())


def test_hidden_identity_predates_and_status_boundary_are_not_repair_evidence():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    premise={"title_candidates":["Poor Student Was Secretly a Billionaire Heir"],"opening_event":{"first_10_seconds":"a status boundary predates the hidden identity reveal"}}
    result=evaluate_hidden_identity_integrity(premise,{},[])
    assert not result['queenflix_accountability']['post_reveal_spatial_boundary']
    assert not result['queenflix_accountability']['repeat_inconvenient_compliance']


def test_compound_recovery_requires_non_negated_access_or_sharing():
    from studio.compound_expansion import evaluate_compound_expansion_readiness
    premise={'target_minutes':24,'logline':'a dragon creature in a town where the water system collapses'}
    arch={'sequences':[{'sequence':1,'turn':'the water infrastructure collapse destroys the community supply'},{'sequence':2,'turn':'water access is still cut off but the creature gets safely home'}]}
    assert evaluate_compound_expansion_readiness(premise,arch,[])['warnings']
    arch_shared={'sequences':[{'sequence':1,'turn':'the water infrastructure collapse destroys the community supply'},{'sequence':2,'turn':'the community rebuilds shared water access and the creature returns home'}]}
    result=evaluate_compound_expansion_readiness(premise,arch_shared,[])
    assert not any('community survival' in warning or 'expansion hook' in warning for warning in result['warnings'])


def test_creature_contract_missing_finale_not_offset_by_extra_early_scene():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.compound_expansion import evaluate_compound_expansion_readiness
    from studio.creature_pacing import evaluate_creature_pacing
    premise=generate_premises('creature_economic_melodrama',1,32)[0]
    arch=generate_architecture(premise)
    scenes=generate_scenes(premise,arch)
    missing_finale=scenes[:-1]+[dict(scenes[0],scene_id='S01B_extra_early_half')]
    compound=evaluate_compound_expansion_readiness(premise,arch,missing_finale)
    pacing=evaluate_creature_pacing(premise,arch,missing_finale)
    assert compound['scene_coverage_ratio']<1.0
    assert pacing['scene_coverage_ratio']<1.0
    assert compound['score_0_to_1']<1.0
    assert pacing['score_0_to_1']<1.0


def test_romance_deception_integrity_accepts_safeguarded_twistora_pattern():
    from studio.romance_deception_integrity import evaluate_romance_deception_integrity
    premise={"title_candidates":["Her Online Boyfriend Was 11, Then His Older Brother Fell for Her"],"opening_event":{"first_5_minutes":"she rejects the interaction when he says he is 11, deletes the game, and the older brother asks about money, sexual or inappropriate messages; she says no, never, they only played games"}}
    arch={"sequences":[
      {"turn":"the brother handles him, parents remove the phone, and the child apologizes"},
      {"turn":"fake dating begins with no kissing not negotiable; if she wants him to let go she can say it"},
      {"turn":"he corrects lies publicly but says she does not have to answer in public"},
      {"turn":"he apologizes for pressure and coercion, prepares her for unexpected questions because she is socially anxious, and never tells her to relax"},
      {"turn":"he asks can I kiss you; she is seen anxious awkward weird at her absolute worst and the right ones stay"}]}
    result=evaluate_romance_deception_integrity(premise,arch,[])
    assert result['applies']
    assert result['minor_risk_detected']
    assert result['score_0_to_1']==1.0


def test_romance_deception_integrity_flags_unsafeguarded_minor_hook_and_coercion():
    from studio.romance_deception_integrity import evaluate_romance_deception_integrity
    premise={"title_candidates":["Her Online Boyfriend Was 11"],"opening_event":{"first_5_minutes":"she keeps the secret romance alive"}}
    arch={"sequences":[{"turn":"he uses humiliating secrets as leverage unless she fake dates him and kisses her without asking"}]}
    result=evaluate_romance_deception_integrity(premise,arch,[])
    assert result['score_0_to_1']<0.5
    assert any('safeguarding' in warning for warning in result['warnings'])
    assert any('coercion' in warning for warning in result['warnings'])


def test_hidden_identity_old_apology_pattern_scores_below_accountable_standard():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    premise={"title_candidates":["She Fell in Love With a Poor Student, Not Knowing He Was a Billionaire Heir"],"opening_event":{"first_10_seconds":"a poor student is mocked but helps another student","first_60_seconds":"ordinary kindness over coffee and library study","first_5_minutes":"he corrects a valuation and proves competence"}}
    arch={"sequences":[{"turn":"competence and love grow before status"},{"turn":"the true identity reveal creates a trust wound because he lied"},{"turn":"he apologizes, uses wealth to save the university and protect vulnerable students"},{"turn":"chosen love, proposal, wedding, family and belonging matter more than wealth"}]}
    result=evaluate_hidden_identity_integrity(premise,arch,[])
    assert result['base_score_0_to_1']==1.0
    assert result['accountability_score_0_to_1']<0.5
    assert result['score_0_to_1']<1.0


def test_zero_to_hero_integrity_accepts_reelquest_pattern():
    from studio.zero_to_hero_integrity import evaluate_zero_to_hero_integrity
    premise={"release_format":"series_premiere","title_candidates":["They Mocked His Empty Bloodline"],"logline":"a commoner awakens soul blood power at a battle academy to rescue his father"}
    arch={"sequences":[
      {"turn":"he could have run but turned to protect villagers, proving courage before power"},
      {"turn":"nobles say commoner lowborn blood cannot rise and the rules changed to move the bar, sealing off every commoner's way up"},
      {"turn":"fusion rank ladder crystal and bloodline rules are legible, but clashing energy can burst his container, burn lifespan, or kill him"},
      {"turn":"a mentor ally demands a deal condition and exchange rather than helping passively"},
      {"turn":"he promises to find his father and bring him home"}]}
    result=evaluate_zero_to_hero_integrity(premise,arch,[])
    assert result['applies']
    assert result['score_0_to_1']==1.0


def test_zero_to_hero_integrity_flags_generic_power_fantasy():
    from studio.zero_to_hero_integrity import evaluate_zero_to_hero_integrity
    premise={"title_candidates":["He Awakened Ultimate Bloodline Power"],"logline":"a commoner becomes the strongest"}
    result=evaluate_zero_to_hero_integrity(premise,{},[])
    assert result['score_0_to_1']<0.5
    assert any('cost' in warning for warning in result['warnings'])


def test_prohibition_scifi_integrity_accepts_2050_pattern():
    from studio.prohibition_scifi_integrity import evaluate_prohibition_scifi_integrity
    premise={"title_candidates":["The World in 2050, After World War III"],"logline":"post-apocalyptic eden collectors take anyone who looks up"}
    arch={"sequences":[
      {"turn":"father makes child practice face down don't look up; collectors carried people off and wipe memory after three days deadline"},
      {"turn":"robot companion earns trust, he is not a thing, he is my friend"},
      {"turn":"machine didn't start war, it said no and refused to launch; a man blamed a machine"},
      {"turn":"eden paradise is mines, collars, erased memory and control"},
      {"turn":"look at its eyes, look up safe now; dad compass find your way back, I'll remember for both, build a world where no one hides face"},
      {"turn":"another eden sequel hook after closure"}]}
    result=evaluate_prohibition_scifi_integrity(premise,arch,[])
    assert result['applies']
    assert result['score_0_to_1']==1.0


def test_prohibition_scifi_integrity_flags_surface_rule_copy():
    from studio.prohibition_scifi_integrity import evaluate_prohibition_scifi_integrity
    premise={"title_candidates":["Don't Look Up in 2050"],"logline":"an evil AI rules eden"}
    result=evaluate_prohibition_scifi_integrity(premise,{},[])
    assert result['score_0_to_1']<0.5


def test_scene_coverage_extra_minutes_do_not_mask_internal_gap():
    from studio.scene_coverage import scene_time_coverage
    scenes=[{"time_range":"0-10"},{"time_range":"20-35"}]
    result=scene_time_coverage(scenes,30)
    assert result['covered_minutes']==20
    assert not result['complete']
    assert result['coverage_ratio']<0.98


def test_romance_deception_does_not_apply_to_creature_hidden_identity():
    from studio.romance_deception_integrity import evaluate_romance_deception_integrity
    premise={"title_candidates":["The Keeper's Hidden Identity"],"logline":"a keeper hides their identity while protecting a dragon child"}
    result=evaluate_romance_deception_integrity(premise,{},[])
    assert not result['applies']


def test_romance_deception_detects_teen_minor_age():
    from studio.romance_deception_integrity import evaluate_romance_deception_integrity
    premise={"title_candidates":["Her Online Boyfriend Was 16"],"logline":"an adult keeps dating him after the reveal"}
    result=evaluate_romance_deception_integrity(premise,{},[])
    assert result['applies']
    assert result['minor_risk_detected']
    assert not result['checks']['immediate_boundary_or_rejection']


def test_romance_deception_age_disclosure_alone_is_not_rejection():
    from studio.romance_deception_integrity import evaluate_romance_deception_integrity
    premise={"title_candidates":["Her Online Boyfriend Was 11"],"opening_event":{"first_5_minutes":"he was 11 and they kept dating"}}
    result=evaluate_romance_deception_integrity(premise,{},[])
    assert not result['checks']['immediate_boundary_or_rejection']


def test_romance_deception_blackmail_alone_does_not_count_as_repair():
    from studio.romance_deception_integrity import evaluate_romance_deception_integrity
    premise={"title_candidates":["Fake Dating the Campus Prince"],"logline":"he blackmails her into fake dating"}
    result=evaluate_romance_deception_integrity(premise,{},[])
    assert not result['checks']['coercion_named_or_avoided']


def test_prohibition_scifi_does_not_match_ai_inside_traitor():
    from studio.prohibition_scifi_integrity import evaluate_prohibition_scifi_integrity
    premise={"title_candidates":["Stormglass Keepers"],"logline":"a traitor threatens the dragon sanctuary"}
    assert not evaluate_prohibition_scifi_integrity(premise,{},[])['applies']


def test_romance_hidden_identity_detected_across_fields():
    from studio.romance_deception_integrity import evaluate_romance_deception_integrity
    premise={"title_candidates":["Hidden Identity Heir"],"logline":"a love story about marriage and choice"}
    assert evaluate_romance_deception_integrity(premise,{},[])['applies']


def test_romance_blocking_doorway_is_not_contact_rejection():
    from studio.romance_deception_integrity import evaluate_romance_deception_integrity
    premise={"title_candidates":["Her Online Boyfriend Was 16"],"logline":"he blocks the doorway and the adult keeps dating him"}
    result=evaluate_romance_deception_integrity(premise,{},[])
    assert not result['checks']['immediate_boundary_or_rejection']


def test_prohibition_sequel_hook_requires_closure_before_hook():
    from studio.prohibition_scifi_integrity import evaluate_prohibition_scifi_integrity
    premise={"title_candidates":["Don't Look Up"],"logline":"post-apocalyptic eden"}
    arch={"sequences":[{"turn":"another eden new threat appears, then later look up safe now and they build a world"}]}
    assert not evaluate_prohibition_scifi_integrity(premise,arch,[])['checks']['sequel_hook_after_closure']


def test_prohibition_no_sequel_hook_does_not_warn():
    from studio.prohibition_scifi_integrity import evaluate_prohibition_scifi_integrity
    premise={"title_candidates":["Don't Look Up"],"logline":"post-apocalyptic eden"}
    arch={"sequences":[{"turn":"look up safe now and they build a world"}]}
    assert evaluate_prohibition_scifi_integrity(premise,arch,[])['checks']['sequel_hook_after_closure']


def test_family_exit_integrity_accepts_velvet_pattern():
    from studio.family_exit_integrity import evaluate_family_exit_integrity
    premise={"title_candidates":["I Was the Obedient Daughter for 20 Years Until I Left Without Saying Goodbye"]}
    arch={"sequences":[{"turn":"one dowry wedding dress savings jewelry and gold go to twin sister; hospital blood allergy medical report ignored"},{"turn":"mother-in-law notices thinness, remembers likes dietary routine, makes food and cushions her"},{"turn":"she leaves the group chat, phone off, no invite; it is not punish but live my own life, bottom of your priorities and Chloe shadow"},{"turn":"mother says I was wrong and regret; father gifts again but she feels nothing, no longer needs it, they may return if we have time"}]}
    assert evaluate_family_exit_integrity(premise,arch,[])['score_0_to_1']==1.0


def test_family_exit_chosen_family_alone_does_not_apply():
    from studio.family_exit_integrity import evaluate_family_exit_integrity
    premise={"title_candidates":["Stormglass Keepers"],"logline":"a creature-protection chosen family fantasy"}
    assert not evaluate_family_exit_integrity(premise,{},[])['applies']


def test_family_exit_title_alone_does_not_count_as_exit_event():
    from studio.family_exit_integrity import evaluate_family_exit_integrity
    premise={"title_candidates":["Left Without Saying Goodbye"],"logline":"family favoritism and dowry conflict"}
    result=evaluate_family_exit_integrity(premise,{},[])
    assert not result['checks']['quiet_procedural_exit']


def test_family_exit_finale_uses_structured_sequences_not_character_tail():
    from studio.family_exit_integrity import evaluate_family_exit_integrity
    premise={"title_candidates":["Left Without Saying Goodbye"],"logline":"family favoritism dowry hospital"}
    arch={"sequences":[{"turn":"x"*3000},{"turn":"mother says I was wrong and regret; she feels nothing and no longer needs forgiveness; if we have time bounded contact"}]}
    result=evaluate_family_exit_integrity(premise,arch,[])
    assert result['checks']['repair_not_objects_only']
    assert result['checks']['no_forced_forgiveness_reset']


def test_romance_blocks_him_counts_as_contact_rejection():
    from studio.romance_deception_integrity import evaluate_romance_deception_integrity
    premise={"title_candidates":["Her Online Boyfriend Was 16"],"opening_event":{"first_5_minutes":"she blocks him immediately"}}
    assert evaluate_romance_deception_integrity(premise,{},[])['checks']['immediate_boundary_or_rejection']


def test_family_exit_warnings_are_strings_not_booleans():
    from studio.family_exit_integrity import evaluate_family_exit_integrity
    premise={"title_candidates":["Left Without Saying Goodbye"],"logline":"family favoritism dowry"}
    result=evaluate_family_exit_integrity(premise,{},[])
    assert all(isinstance(w,str) for w in result['warnings'])
    assert any('forces emotional forgiveness' in w for w in result['warnings'])


def test_family_exit_reads_architecture_ending_payoff():
    from studio.family_exit_integrity import evaluate_family_exit_integrity
    premise={"title_candidates":["Left Without Saying Goodbye"],"logline":"family favoritism dowry hospital"}
    arch={"ending_payoff":{"justice":"mother says I was wrong and regret","belonging":"bounded contact if we have time; she feels nothing and no longer needs forgiveness","future_image":"chosen family care"}}
    result=evaluate_family_exit_integrity(premise,arch,[])
    assert result['checks']['repair_not_objects_only']
    assert result['checks']['no_forced_forgiveness_reset']


def test_romance_physical_obstruction_is_not_contact_rejection():
    from studio.romance_deception_integrity import evaluate_romance_deception_integrity
    premise={"title_candidates":["Her Online Boyfriend Was 16"],"logline":"she blocks him from leaving but they keep dating"}
    result=evaluate_romance_deception_integrity(premise,{},[])
    assert not result['checks']['immediate_boundary_or_rejection']


def test_family_exit_opening_apology_does_not_pass_finale():
    from studio.family_exit_integrity import evaluate_family_exit_integrity
    premise={"title_candidates":["Left Without Saying Goodbye"],"logline":"family favoritism dowry hospital","opening_event":{"first_5_minutes":"mother says I was wrong and regret but nothing is resolved"}}
    result=evaluate_family_exit_integrity(premise,{},[])
    assert not result['checks']['repair_not_objects_only']


def test_family_exit_premise_ending_key_counts():
    from studio.family_exit_integrity import evaluate_family_exit_integrity
    premise={"title_candidates":["Left Without Saying Goodbye"],"logline":"family favoritism dowry hospital","ending":{"resolution":"mother says I was wrong and regret; bounded if we have time; she feels nothing and no longer needs forgiveness"}}
    result=evaluate_family_exit_integrity(premise,{},[])
    assert result['checks']['repair_not_objects_only']


def test_romance_blocks_from_contact_counts_as_rejection():
    from studio.romance_deception_integrity import evaluate_romance_deception_integrity
    premise={"title_candidates":["Her Online Boyfriend Was 16"],"opening_event":{"first_5_minutes":"she blocks him from contacting her after learning his age"}}
    assert evaluate_romance_deception_integrity(premise,{},[])['checks']['immediate_boundary_or_rejection']


def test_animal_guise_consent_accepts_mythictwist_pattern():
    from studio.animal_guise_consent import evaluate_animal_guise_consent
    premise={"title_candidates":["She Thought He Was a Dog, Turns Out He's the Alpha King"],"logline":"werewolf husband in wolf form and luna mate romance"}
    arch={"sequences":[
      {"turn":"she demands conditions inheritance deeds gold because she had no say; cares, bandages, teaches button, protects and dances with him"},
      {"turn":"she says I hate being lied to liar, sleeping in separate rooms not sharing a bed; he used that form to make me forgive and destroyed everything, lowest man"},
      {"turn":"mother estate deeds orchard rent ledgers recovered it all; stay or leave won't force you, no one asked you before, will you stand beside me, this time my choice"},
      {"turn":"kidnapping and forced marriage are not consensual; guilty sentenced prison arrest"}]}
    result=evaluate_animal_guise_consent(premise,arch,[])
    assert result['applies']
    assert result['score_0_to_1']==1.0


def test_animal_guise_consent_flags_cute_unrepaired_disguise():
    from studio.animal_guise_consent import evaluate_animal_guise_consent
    premise={"title_candidates":["Her Dog Was the Alpha King"],"logline":"she cuddles the cute werewolf every night and they marry"}
    result=evaluate_animal_guise_consent(premise,{},[])
    assert result['score_0_to_1']<0.5


def test_family_exit_schema_closure_fields_count():
    from studio.family_exit_integrity import evaluate_family_exit_integrity
    premise={"title_candidates":["Left Without Saying Goodbye"],"logline":"family favoritism dowry hospital","meaning_carrier":{"final_sequence_use":"mother says I was wrong and regret; bounded if we have time; she feels nothing and no longer needs forgiveness"},"relational_contract":{"consent_or_personhood_repair":"boundary if we have time not punishment"}}
    result=evaluate_family_exit_integrity(premise,{},[])
    assert result['checks']['repair_not_objects_only']


def test_animal_guise_does_not_apply_to_mate_substrings_or_ferry_roles():
    from studio.animal_guise_consent import evaluate_animal_guise_consent
    result=evaluate_animal_guise_consent({"logline":"an animated ferry mate is materially challenged"}, {}, [])
    assert not result['applies']


def test_animal_guise_requires_care_before_reveal_not_after():
    from studio.animal_guise_consent import evaluate_animal_guise_consent
    premise={"logline":"werewolf husband romance. reveal truth."}
    arch={"sequences":[{"turn":"after reveal she cares feeds and protects him"}]}
    result=evaluate_animal_guise_consent(premise,arch,[])
    assert not result['checks']['care_before_reveal']


def test_animal_guise_rejects_unrepaired_deeds_and_kidnapping_mentions():
    from studio.animal_guise_consent import evaluate_animal_guise_consent
    premise={"logline":"werewolf husband romance truth reveal. stolen deeds and kidnapping are mentioned, but nobody is punished"}
    result=evaluate_animal_guise_consent(premise,{},[])
    assert not result['checks']['material_agency_restored']
    assert not result['checks']['coercive_actors_accountable']


def test_animal_guise_pre_reveal_proposal_is_not_informed_rechoice():
    from studio.animal_guise_consent import evaluate_animal_guise_consent
    premise={"logline":"werewolf husband romance. will you be my mate and it is my choice. later truth reveal exposes him"}
    result=evaluate_animal_guise_consent(premise,{},[])
    assert not result['checks']['explicit_rechoice_after_truth']


def test_creature_power_inversion_accepts_wufo_pattern():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    premise={"logline":"cold winter coal poor stable girl finds dragon that is not fire but freezes frost"}
    arch={"sequences":[{"turn":"king calls it monster cursed weakness and threw abandoned creature; she feeds warms names him steals coal"},{"turn":"execution burn stake trap bait crowd soldiers; frost fire protects rescues"},{"turn":"recognition contact forehead touch, thaw green village community snow melt proclamation"}]}
    r=evaluate_creature_power_inversion(premise,arch,[])
    assert r['applies'] and r['score_0_to_1']==1.0


def test_creature_power_inversion_flags_spectacle_only():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    r=evaluate_creature_power_inversion({"logline":"a frost dragon fights in a big fantasy battle"}, {}, [])
    assert r['applies'] and r['score_0_to_1']<0.5


def test_creature_inversion_does_not_apply_to_human_fear_freeze():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    r=evaluate_creature_power_inversion({"logline":"survival heroine freezes in fear beside a train"}, {}, [])
    assert not r['applies']


def test_creature_inversion_requires_care_and_stakes_before_power():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    premise={"logline":"dragon exhales frost instead of fire as protective power. later she feeds him and winter cold poverty appears"}
    r=evaluate_creature_power_inversion(premise,{},[])
    assert not r['checks']['care_costs_before_power']
    assert not r['checks']['material_survival_stakes_before_spectacle']


def test_creature_inversion_requires_inverted_power_protection():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    premise={"logline":"dragon exhales frost instead of fire. keeper rescues dragon but dragon uses frost to harm villagers"}
    r=evaluate_creature_power_inversion(premise,{},[])
    assert not r['checks']['inverted_power_protects']


def test_creature_inversion_short_opening_not_counted_as_closure():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    premise={"logline":"dragon frost fire inversion in village; opening contact touch recognition"}
    r=evaluate_creature_power_inversion(premise,{},[])
    assert not r['checks']['recognition_contact_closure']
    assert not r['checks']['communal_consequence']


def test_animal_guise_recipient_split_restitution_counts():
    from studio.animal_guise_consent import evaluate_animal_guise_consent
    premise={"logline":"werewolf husband romance truth reveal. he gives her back the deeds"}
    r=evaluate_animal_guise_consent(premise,{},[])
    assert r['checks']['material_agency_restored']


def test_found_family_guardian_accepts_epicverse_pattern():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    premise={"logline":"pursued mother newborn infant danger serpent giant rescues saves and raises daughter"}
    arch={"sequences":[{"turn":"he feeds warms teaches hunts protects her by fire shelter; she learns hunt survive bow"},{"turn":"argument rupture leaves journey; ruthless lord sees fortune captured monster beast city square public prison crossbow trap army"},{"turn":"rescue save final confrontation and carries daughter on his back home reunited"}]}
    r=evaluate_found_family_guardian_integrity(premise,arch,[])
    assert r['applies'] and r['score_0_to_1']==1.0


def test_found_family_guardian_flags_spectacle_without_rupture():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    r=evaluate_found_family_guardian_integrity({"logline":"giant daughter monster army rescue victory"}, {}, [])
    assert r['score_0_to_1']<0.6


def test_creature_inversion_detects_freezing_mist_instead_of_flames():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    r=evaluate_creature_power_inversion({"logline":"dragon exhales freezing mist instead of flames"}, {}, [])
    assert r['applies']


def test_creature_inversion_logline_marked_aftermath_counts():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    premise={"logline":"dragon exhales freezing mist instead of flames. Aftermath: recognition contact in the village as snow melts green and people rebuild"}
    r=evaluate_creature_power_inversion(premise,{},[])
    assert r['checks']['recognition_contact_closure']
    assert r['checks']['communal_consequence']


def test_animal_guise_keeps_deeds_is_not_restitution():
    from studio.animal_guise_consent import evaluate_animal_guise_consent
    premise={"logline":"werewolf husband romance truth reveal. he gives her back her coat but keeps the deeds"}
    r=evaluate_animal_guise_consent(premise,{},[])
    assert not r['checks']['material_agency_restored']


def test_found_family_does_not_apply_to_covenant_guardianship():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    premise=open('examples/stormglass_project/premise.json',encoding='utf8').read()
    import json
    r=evaluate_found_family_guardian_integrity(json.loads(premise),{},[])
    assert not r['applies']


def test_creature_structured_finale_overrides_premise_aftermath():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    premise={"logline":"dragon exhales freezing mist instead of flames. Aftermath: recognition contact village thaw rebuild"}
    scenes=[{"scene_id":f"S{i}","visual_action":{"final_image":"battle smoke"}} for i in range(5)]
    r=evaluate_creature_power_inversion(premise,{},scenes)
    assert not r['checks']['recognition_contact_closure']
    assert not r['checks']['communal_consequence']


def test_creature_ordinary_fire_melting_ice_does_not_apply():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    r=evaluate_creature_power_inversion({"logline":"a dragon melting ice with its flames attacks the castle"}, {}, [])
    assert not r['applies']


def test_creature_freezing_mist_counts_as_behavioral_difference():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    r=evaluate_creature_power_inversion({"logline":"dragon exhales freezing mist instead of flames"}, {}, [])
    assert r['applies'] and r['checks']['difference_shown_behaviorally']


def test_animal_guise_notebook_does_not_negate_returned_deeds():
    from studio.animal_guise_consent import evaluate_animal_guise_consent
    premise={"logline":"werewolf husband romance truth reveal. he returns the notebook and the deeds"}
    r=evaluate_animal_guise_consent(premise,{},[])
    assert r['checks']['material_agency_restored']


def test_found_family_single_repeated_feeding_is_not_repeated_care():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    premise={"logline":"giant found family daughter. he feeds the infant. opening outline: he feeds the infant. scene: he feeds the infant"}
    r=evaluate_found_family_guardian_integrity(premise,{},[])
    assert not r['checks']['repeated_operational_care']


def test_dialogue_unhashable_beat_warns_instead_of_crashing():
    from studio.dialogue_craft import evaluate_scenes_dialogue
    r=evaluate_scenes_dialogue([{"scene_id":"bad","dialogue_design":{"spoken_exchange":[{"beat":["x"],"speaker":"a","line":"hi","action":"acts"}]}}])
    assert any('malformed' in w for w in r['scenes'][0]['warnings'])


def test_creature_fire_but_instead_freezes_applies():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    r=evaluate_creature_power_inversion({"logline":"a dragon that would breathe fire but instead freezes the world"}, {}, [])
    assert r['applies']


def test_creature_partial_opening_uses_premise_logline_ending():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    p={"logline":"a dragon exhales frost instead of fire. final recognition contact and village thaw rebuild"}
    scenes=[{"scene_id":"S1","visual_action":{"final_image":"cold shelter"}},{"scene_id":"S2","visual_action":{"final_image":"coal"}}]
    r=evaluate_creature_power_inversion(p,{},scenes)
    assert r['checks']['recognition_contact_closure']


def test_guardian_time_jump_without_care_fails_repeated_care():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    p={"logline":"giant found family orphan daughter. years pass in the forest creature"}
    r=evaluate_found_family_guardian_integrity(p,{},[])
    assert not r['checks']['repeated_operational_care']


def test_guardian_logline_homecoming_counts_for_premise_only():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    p={"logline":"giant found family orphan daughter. in the end he carries her home"}
    r=evaluate_found_family_guardian_integrity(p,{},[])
    assert r['checks']['physical_custody_or_carrying_closure']


def test_child_first_guardian_premise_applies():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    p={"logline":"an orphan is rescued by a troll who becomes her guardian"}
    r=evaluate_found_family_guardian_integrity(p,{},[])
    assert r['applies']


def test_returns_nothing_from_estate_is_not_restitution():
    from studio.animal_guise_consent import evaluate_animal_guise_consent
    p={"logline":"werewolf husband romance truth reveal. he returns nothing from her estate"}
    r=evaluate_animal_guise_consent(p,{},[])
    assert not r['checks']['material_agency_restored']


def test_guardian_civic_orphan_acceptance_does_not_apply():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    p={"logline":"a woman becomes the city's guardian. orphans among the people accept her as the city's guardian"}
    r=evaluate_found_family_guardian_integrity(p,{},[])
    assert not r['applies']


def test_creature_architecture_ending_overrides_promised_logline_closure():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    p={"logline":"dragon exhales frost instead of fire. final recognition contact village thaw rebuild"}
    arch={"sequences":[{"ending":"battle smoke"},{"ending":"the dragon leaves alone"}],"ending_payoff":{"payoff_image":"empty cave"}}
    r=evaluate_creature_power_inversion(p,arch,[])
    assert not r['checks']['recognition_contact_closure']
    assert not r['checks']['communal_consequence']


def test_early_logline_homecoming_is_not_closure_evidence():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    p={"logline":"a giant found family daughter carries her home at the beginning. in the end she leaves alone without contact"}
    r=evaluate_found_family_guardian_integrity(p,{},[])
    assert not r['checks']['physical_custody_or_carrying_closure']


def test_guardian_sheltering_counts_as_care():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    p={"logline":"giant found family daughter. he shelters and feeds the child each night"}
    r=evaluate_found_family_guardian_integrity(p,{},[])
    assert r['checks']['repeated_operational_care']


def test_fire_melts_ice_object_is_not_power_inversion():
    from studio.creature_power_inversion import evaluate_creature_power_inversion
    p={"logline":"a dragon breathes fire but instead melts ice rather than burning a town"}
    r=evaluate_creature_power_inversion(p,{},[])
    assert not r['applies']


def test_child_power_obsolescence_full_chain_passes():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"A child sees a countdown and saves a man before explaining her visions. He protects her before DNA proof. Lab records, sealed tests and hospital witnesses establish paternity. The child investigates records. Her powers become unstable and then gone. He says you're my daughter not my bodyguard. In the end she is a normal child at home eating cake, and someone will come when she is afraid. Another weird kid appears."}
    r=evaluate_child_power_obsolescence(p,{},[])
    assert r['applies'] and r['score_0_to_1']==1.0


def test_child_power_obsolescence_requires_family_context():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    r=evaluate_child_power_obsolescence({"logline":"a child has visions and super strength in a battle academy"},{},[])
    assert not r['applies']


def test_child_power_obsolescence_flags_power_never_tested_as_unnecessary():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a child sees a countdown and saves her father before explaining her visions. He protects her before DNA proof and lab records establish paternity. She investigates records and uses unstable powers. In the end the family is home."}
    r=evaluate_child_power_obsolescence(p,{},[])
    assert r['applies'] and not r['checks']['love_not_payment_for_power']


def test_child_power_obsolescence_does_not_apply_to_creature_economic_child_ally():
    import json
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p=json.load(open('examples/generated_creature_concepts/emberseed_oven_cart_premise.json',encoding='utf8'))
    r=evaluate_child_power_obsolescence(p,{},[])
    assert not r['applies']


def test_child_power_scene_order_not_masked_by_premise_summary():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"visions biological paternity home family. a child has powers"}
    scenes=[{"scene_id":"S1","visual_action":{"first_image":"countdown danger save"},"dialogue_design":{"key_lines":["He protects her before any test"]}},{"scene_id":"S2","visual_action":{"final_image":"she explains visions and later lab DNA proof"}}]
    r=evaluate_child_power_obsolescence(p,{},scenes)
    assert r['checks']['power_demonstrated_before_explanation']
    assert r['checks']['protective_bond_before_biological_proof']


def test_guardian_city_setting_does_not_hide_explicit_child_guardianship():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    r=evaluate_found_family_guardian_integrity({"logline":"in the city, a troll is guardian of an orphan child"},{},[])
    assert r['applies']


def test_guardian_adoptive_mother_applies():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    r=evaluate_found_family_guardian_integrity({"logline":"a troll becomes an orphan child's adoptive mother"},{},[])
    assert r['applies']


def test_child_power_opening_scene_uses_explicit_planned_ending():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a child sees a countdown and saves her father. in the end she is a normal child at home with family"}
    scenes=[{"scene_id":"S1","visual_action":{"first_image":"countdown danger"},"dialogue_design":{"key_lines":["vision"]}}]
    r=evaluate_child_power_obsolescence(p,{},scenes)
    assert r['checks']['ordinary_belonging_closure']


def test_child_power_foster_home_does_not_count_as_final_closure_for_hook_order():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a child leaves a foster home and sees visions. her father protects her before DNA proof. another weird kid appears"}
    r=evaluate_child_power_obsolescence(p,{},[])
    assert not r['checks']['sequel_hook_after_belonging_closure']


def test_child_power_adult_investigation_alone_not_child_agency():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a child sees a countdown and saves her father. adults search records and order DNA tests. he protects her. powers become unstable. in the end the family is home."}
    r=evaluate_child_power_obsolescence(p,{},[])
    assert not r['checks']['child_agency_investigation']


def test_child_power_does_not_apply_to_institutional_power_drama():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a daughter of a father faces institutional casting power and legal pressure at a swim lesson"}
    assert not evaluate_child_power_obsolescence(p,{},[])['applies']


def test_child_power_first_person_investigation_counts():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a child sees a countdown and saves her father. he protects her before dna proof. she says i will investigate the records. powers become unstable. in the end she goes home with her dad. another weird kid appears."}
    r=evaluate_child_power_obsolescence(p,{},[])
    assert r['checks']['child_agency_investigation']


def test_child_power_home_with_dad_counts_before_hook():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a child sees a countdown and saves her father. he protects her before dna proof. the child investigates records. powers become unstable. in the end she goes home with her dad. another weird kid appears."}
    r=evaluate_child_power_obsolescence(p,{},[])
    assert r['checks']['sequel_hook_after_belonging_closure']


def test_guardian_of_orphanage_is_not_child_custody():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    r=evaluate_found_family_guardian_integrity({"logline":"a creature becomes guardian of an orphanage and protects the building"},{},[])
    assert not r['applies']


def test_girl_predictive_power_applies_family_gate():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    r=evaluate_child_power_obsolescence({"logline":"a girl predicts accidents to save her father"},{},[])
    assert r['applies']


def test_child_guardian_at_orphanage_applies():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    r=evaluate_found_family_guardian_integrity({"logline":"at an orphanage, a troll becomes guardian of a child"},{},[])
    assert r['applies']


def test_early_foster_home_return_not_closure():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a child returns home to a foster house, sees a countdown, and saves her father. he protects her before dna proof. the child investigates records. powers become unstable. another weird kid appears."}
    assert not evaluate_child_power_obsolescence(p,{},[])['checks']['sequel_hook_after_belonging_closure']


def test_father_first_person_investigation_not_child_agency():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a child sees a countdown and saves her father. the father says i will investigate the records. he protects her before dna proof. powers become unstable. in the end she goes home with her dad."}
    assert not evaluate_child_power_obsolescence(p,{},[])['checks']['child_agency_investigation']


def test_girl_asks_nurse_counts_as_child_agency():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a girl sees a countdown and saves her father. he protects her before dna proof. the girl asks a nurse for birth records. powers become unstable. in the end she goes home with her dad."}
    assert evaluate_child_power_obsolescence(p,{},[])['checks']['child_agency_investigation']


def test_guardian_of_plural_children_applies():
    from studio.found_family_guardian_integrity import evaluate_found_family_guardian_integrity
    r=evaluate_found_family_guardian_integrity({"logline":"a troll becomes guardian of the children he rescued"},{},[])
    assert r['applies']


def test_epic_creature_extraction_full_chain_passes():
    from studio.epic_creature_extraction import evaluate_epic_creature_extraction
    p={"logline":"In a kingdom at war, creatures feed shelter and teach a human child in their valley community. A royal army uses capture wagons to drain creature essence as energy for the holy fire. The boy's blood lights a stone, so power use exposes him. Archives, guard rotations, service passages and evidence guide infiltration. A rescued prisoner cannot stop his hands because of mind control. In the end they destroy the source even though souls are trapped inside and the kingdom is left in darkness, then rebuild another way, remember the lost, welcome people home, and choose peace day after day."}
    r=evaluate_epic_creature_extraction(p,{},[])
    assert r['applies']
    assert r['score_0_to_1'] == 1.0


def test_epic_creature_extraction_flags_costless_villain_defeat():
    from studio.epic_creature_extraction import evaluate_epic_creature_extraction
    p={"logline":"In a kingdom at war, a royal army drains dragon essence for energy. The hero kills the villain and the story ends."}
    r=evaluate_epic_creature_extraction(p,{},[])
    assert r['applies']
    assert not r['checks']['communal_consequence_or_peace_maintenance']
    assert not r['checks']['liberation_trauma_persists']


def test_royal_hidden_identity_golden_rose_chain():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    p={"logline":"A princess secretly escapes the palace disguised as a village girl. A hidden prince poses as a beggar. She gives her last bread before status is known and ordinary kindness forms love. The rose ritual and law force her to live in his hut and affect marriage and kingdom inheritance. She tells him she is the king's daughter. He lied, creating a trust wound and apology. She exposes poison evidence, interrupts the signing, saves her father, and protects the kingdom. In the end they choose each other in a palace or hut and choose every day at a wedding, with full disclosure, records, consent, boundaries, and no gifts."}
    r=evaluate_hidden_identity_integrity(p,{},[])
    assert r['applies']
    assert r['checks']['ritual_or_object_has_material_consequence']
    assert r['checks']['truthful_status_invariant_rechoice']


def test_royal_hidden_identity_flags_passive_princess_after_reveal():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    p={"logline":"A princess secretly escapes the palace disguised as a maid. A hidden prince reveals himself, lied to her, and then arranges their royal wedding."}
    r=evaluate_hidden_identity_integrity(p,{},[])
    assert r['applies']
    assert not r['checks']['agency_retained_after_reveal']


def test_epic_extraction_rejects_local_resource_word_matches():
    from studio.epic_creature_extraction import evaluate_epic_creature_extraction
    p={"logline":"an unaware baker protects a creature and uses a resource oven cart in a local debt story"}
    assert not evaluate_epic_creature_extraction(p,{},[])['applies']


def test_epic_extraction_costless_source_destruction_fails():
    from studio.epic_creature_extraction import evaluate_epic_creature_extraction
    p={"logline":"in a kingdom at war, a royal army drains dragon essence for energy. creatures feed and shelter a child. in the end the hero destroys the source and kills the villain."}
    r=evaluate_epic_creature_extraction(p,{},[])
    assert not r['checks']['source_defeat_has_moral_or_infrastructural_cost']
    assert not r['checks']['communal_consequence_or_peace_maintenance']


def test_epic_extraction_hook_order_matters():
    from studio.epic_creature_extraction import evaluate_epic_creature_extraction
    p={"logline":"in a kingdom at war, a royal army drains dragon essence for energy. creatures feed and shelter a child. a new threat awakens. in the end souls trapped inside are freed and the source destroyed, the kingdom left in darkness, then refugees are welcomed home to rebuild peace."}
    r=evaluate_epic_creature_extraction(p,{},[])
    assert not r['checks']['sequel_hook_after_home_closure']


def test_child_power_home_to_father_counts_before_case():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a girl sees a countdown and saves her father. he protects her before dna proof. the child investigates records. powers become unstable. in the end she returns home to her father. a new case appears."}
    assert evaluate_child_power_obsolescence(p,{},[])['checks']['sequel_hook_after_belonging_closure']


def test_child_power_scene_dialogue_first_person_counts():
    from studio.child_power_obsolescence import evaluate_child_power_obsolescence
    p={"logline":"a child sees a countdown and saves her father. he protects her before dna proof. powers become unstable. in the end she goes home with her dad."}
    scenes=[{"dialogue_design":{"spoken_exchange":[{"speaker":"girl","line":"I'll search the hospital records.","beat":"decision","action":"she stands"}]}}]
    assert evaluate_child_power_obsolescence(p,{},scenes)['checks']['child_agency_investigation']


def test_undercover_detective_disguise_not_hidden_identity():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    r=evaluate_hidden_identity_integrity({"logline":"a detective poses as a maid to solve a theft"},{},[])
    assert not r['applies']


def test_explicit_royal_disclosure_counts_as_reveal():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    p={"logline":"a secret princess disguised as a village girl tells her partner she is the king's daughter after ordinary kindness before status. he lied and trust was damaged. she protects the kingdom. in the end they choose each other in a palace or hut every day."}
    r=evaluate_hidden_identity_integrity(p,{},[])
    assert r['checks']['reveal_present']


def test_hidden_identity_agency_must_follow_reveal():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    p={"logline":"a secret princess disguised as a maid exposes a thief. later she tells him she is the king's daughter and then becomes passive until they separate."}
    r=evaluate_hidden_identity_integrity(p,{},[])
    assert not r['golden_rose_extensions']['agency_retained_after_reveal']


def test_refusal_to_marry_crown_is_not_rechoice():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    p={"logline":"a secret princess disguised as a maid loves a hidden prince. he says he will not marry a crown, but after the truth they separate."}
    r=evaluate_hidden_identity_integrity(p,{},[])
    assert not r['golden_rose_extensions']['truthful_status_invariant_rechoice']


def test_unrelated_admission_not_identity_reveal():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    p={"logline":"a secret princess disguised as a maid admits stealing bread from a prince, then leaves."}
    r=evaluate_hidden_identity_integrity(p,{},[])
    assert not r['checks']['reveal_present']


def test_introduced_heiress_reveal_allows_aftermath_credit():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    p={"logline":"a princess secretly disguised as a commoner loves before status through ordinary kindness. the king introduces his concealed daughter as his heiress. after that she exposes poison evidence and they choose each other in a palace or hut every day."}
    r=evaluate_hidden_identity_integrity(p,{},[])
    assert r['checks']['reveal_present']
    assert r['golden_rose_extensions']['agency_retained_after_reveal']


def test_disguised_countess_applies_hidden_rank_review():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    r=evaluate_hidden_identity_integrity({"logline":"a countess disguises herself as a commoner and falls in love"},{},[])
    assert r['applies']


def test_looking_does_not_count_as_king_rank_context():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    r=evaluate_hidden_identity_integrity({"logline":"a detective poses as a maid while looking for evidence"},{},[])
    assert not r['applies']


def test_direct_identity_disclosure_counts_as_reveal():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    result = evaluate_hidden_identity_integrity(
        {"title": "Hidden Princess", "logline": "A hidden princess disguises herself as a maid. She has craft competence and ordinary kindness before status. She discloses her identity. The lie creates a trust wound. She protects the village. Ending chosen love family home."},
        {"beats": []},
        [],
    )
    assert result["checks"]["reveal_present"] is True


def test_bare_heiress_label_does_not_start_aftermath():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    result = evaluate_hidden_identity_integrity(
        {"title": "Hidden Princess", "logline": "An heiress hidden princess disguises herself as a maid. She has craft competence and ordinary kindness before status. She exposes the steward's fraud. She discloses her identity. The lie creates a trust wound. Ending chosen love family home."},
        {"beats": []},
        [],
    )
    assert result["checks"]["agency_retained_after_reveal"] is False


def test_confession_match_does_not_swallow_following_action():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    result = evaluate_hidden_identity_integrity(
        {"title": "Hidden Princess", "logline": "A hidden princess disguises herself as a maid. She has craft competence and ordinary kindness before status. She confesses that she is the princess. Royal court follows. She exposes the villain with proof. Ending chosen love family home."},
        {"beats": []},
        [],
    )
    assert result["checks"]["agency_retained_after_reveal"] is True


def test_secret_plot_near_prince_does_not_trigger_hidden_identity():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    result = evaluate_hidden_identity_integrity(
        {"title": "Court Mystery", "logline": "A prince uncovers a secret plot but never hides his identity."},
        {"beats": []},
        [],
    )
    assert result["applies"] is False


def test_counting_guests_is_not_count_rank():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    result = evaluate_hidden_identity_integrity(
        {"title": "Detective", "logline": "A detective poses as a maid to count guests at the inn."},
        {"beats": []},
        [],
    )
    assert result["applies"] is False


def test_plural_royals_activate_disguise_review():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    result = evaluate_hidden_identity_integrity(
        {"title": "Last Royal", "logline": "The last of the royals poses as a maid. She has craft competence and ordinary kindness before status. She discloses her identity. The lie creates a trust wound. She protects the village. Ending chosen love family home."},
        {"beats": []},
        [],
    )
    assert result["applies"] is True


def test_rank_kept_secret_applies_without_disguise():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    result = evaluate_hidden_identity_integrity(
        {"title": "Secret Princess", "logline": "A princess keeps her rank secret while living among ordinary people."},
        {"beats": []},
        [],
    )
    assert result["applies"] is True


def test_continued_identity_mystery_is_not_disclosure():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    result = evaluate_hidden_identity_integrity(
        {"title": "Secret Princess", "logline": "A princess keeps her rank secret. She exposes corruption before the reveal. She admits her identity is still a mystery to him. Much later she discloses her identity."},
        {"beats": []},
        [],
    )
    assert result["checks"]["reveal_present"] is True
    assert result["checks"]["agency_retained_after_reveal"] is False


def _witness_pass_project():
    premise = {
        "title": "The Child Witness",
        "logline": "A father protects his son after a supernatural vision reveals a missing girl cold case. In the end they are safe at home together.",
    }
    architecture = {
        "sequences": [
            {"summary": "Hospital bedside care: the father holds his son's hand, comforts him through grief, and keeps him safe before asking what he knows."},
            {"summary": "The child remembers impossible knowledge about a missing girl; adults debate trauma, imagination, spiritual memory, and evidence while police verify records, photographs, locations, and witness testimony."},
            {"summary": "The sheriff and a powerful local family resist the investigation through a cover-up. The child is forced to publicly identify the killer, becomes afraid, and is protected by his father before the criminal confesses the moral truth."},
        ],
        "ending_payoff": {"summary": "After the confession, father and son go home together, safe, ordinary, and no longer extracting answers from the child."},
    }
    scenes = [
        {"summary": "The child names the victim and the knowledge becomes dangerous; the father protects him rather than exploiting him as an oracle.", "dialogue": [{"speaker": "FATHER", "line": "You are not alone. I will keep you safe."}]}
    ]
    return premise, architecture, scenes


def test_supernatural_child_witness_full_chain_passes():
    from studio.supernatural_child_witness import evaluate_supernatural_child_witness
    premise, architecture, scenes = _witness_pass_project()
    result = evaluate_supernatural_child_witness(premise, architecture, scenes)
    assert result["applies"] is True
    assert result["score_0_to_1"] == 1.0
    assert result["warnings"] == []


def test_supernatural_child_witness_requires_investigation_context():
    from studio.supernatural_child_witness import evaluate_supernatural_child_witness
    result = evaluate_supernatural_child_witness(
        {"title": "Dreamer", "logline": "A child has supernatural visions and learns kindness."},
        {"sequences": []},
        [],
    )
    assert result["applies"] is False


def test_supernatural_child_witness_flags_oracle_shortcut():
    from studio.supernatural_child_witness import evaluate_supernatural_child_witness
    result = evaluate_supernatural_child_witness(
        {"title": "Oracle Boy", "logline": "A boy with supernatural visions solves a murder cold case. The police arrest the killer and everyone celebrates."},
        {"sequences": [{"summary": "The detective asks the boy what he knows, then acts on the answer."}]},
        [],
    )
    assert result["applies"] is True
    assert result["checks"]["care_before_knowledge_extraction"] is False
    assert result["checks"]["confession_or_moral_truth_payoff"] is False
    assert result["warnings"]


def test_supernatural_child_witness_opening_events_do_not_satisfy_finale():
    from studio.supernatural_child_witness import evaluate_supernatural_child_witness
    result = evaluate_supernatural_child_witness(
        {"title": "Vision Witness", "logline": "A child has supernatural visions of a murder cold case."},
        {"sequences": [
            {"summary": "Hospital care and comfort come first, then a cover-up is mentioned and the child is safe at home."},
            {"summary": "The vision becomes dangerous; trauma and skepticism compete with spiritual explanation while police verify records and photographs."},
            {"summary": "A powerful family resists and the afraid child publicly identifies the killer."},
            {"summary": "The villain is arrested after a fight and the film stops."},
        ]},
        [],
    )
    assert result["applies"] is True
    assert result["checks"]["confession_or_moral_truth_payoff"] is False
    assert result["checks"]["ordinary_safety_reestablished_after_mystery"] is False


def test_supernatural_child_witness_care_order_ignores_metadata_question():
    from studio.supernatural_child_witness import evaluate_supernatural_child_witness
    result = evaluate_supernatural_child_witness(
        {"title": "Vision Witness", "logline": "A child has supernatural visions of a murder cold case."},
        {"dramatic_question": "What do the visions mean?", "sequences": [
            {"summary": "Hospital bedside care: the father comforts and protects his son."},
            {"summary": "Then the child remembers impossible knowledge about a missing woman."},
        ]},
        [],
    )
    assert result["checks"]["care_before_knowledge_extraction"] is True


def test_supernatural_child_witness_bare_father_interrogation_is_not_care():
    from studio.supernatural_child_witness import evaluate_supernatural_child_witness
    result = evaluate_supernatural_child_witness(
        {"title": "Vision Witness", "logline": "A child has supernatural visions of a murder cold case."},
        {"sequences": [
            {"summary": "The father interrogates the child for answers."},
            {"summary": "Then the child remembers impossible knowledge about a missing woman."},
        ]},
        [],
    )
    assert result["checks"]["care_before_knowledge_extraction"] is False


def test_supernatural_child_witness_ordinary_television_crime_does_not_apply():
    from studio.supernatural_child_witness import evaluate_supernatural_child_witness
    result = evaluate_supernatural_child_witness(
        {"title": "Ordinary Crime", "logline": "A detective investigates a television personality's disappearance and questions a witness."},
        {"sequences": []},
        [],
    )
    assert result["applies"] is False


def test_undercover_identity_secrecy_without_status_does_not_trigger_hidden_identity():
    from studio.hidden_identity_integrity import evaluate_hidden_identity_integrity
    result = evaluate_hidden_identity_integrity(
        {"title": "Undercover", "logline": "A detective keeps her identity secret to investigate a smuggler."},
        {"sequences": []},
        [],
    )
    assert result["applies"] is False


def test_supernatural_child_witness_cast_and_cooperative_sheriff_do_not_pass_procedure():
    from studio.supernatural_child_witness import evaluate_supernatural_child_witness
    result = evaluate_supernatural_child_witness(
        {"title": "Vision Witness", "logline": "A child has supernatural visions after witnessing a murder."},
        {"sequences": [
            {"summary": "Hospital care and comfort come first."},
            {"summary": "The child knows impossible knowledge. A cooperative sheriff listens and helps, but nobody verifies the vision or checks records."},
        ]},
        [],
    )
    assert result["checks"]["supernatural_clues_converted_into_procedure"] is False
    assert result["checks"]["institutional_or_local_power_resistance"] is False


def test_supernatural_child_witness_single_accepted_explanation_is_not_competition():
    from studio.supernatural_child_witness import evaluate_supernatural_child_witness
    result = evaluate_supernatural_child_witness(
        {"title": "Vision Witness", "logline": "A child has supernatural visions of a murder cold case."},
        {"sequences": [
            {"summary": "Hospital care and comfort come first."},
            {"summary": "Everyone accepts reincarnation immediately, and the police investigate the crime using records they already had."},
        ]},
        [],
    )
    assert result["checks"]["competing_explanations_for_child_knowledge"] is False


def test_patronage_consent_full_chain_passes():
    from studio.patronage_consent_integrity import evaluate_patronage_consent_integrity
    premise = {"title": "The Girl He Believed In", "logline": "A billionaire patron helps a poor village girl pursue education and modeling, then loses everything before she freely chooses him."}
    architecture = {"sequences": [
        {"summary": "She serves the women and works to support her mother after her father died and debts blocked school. The wealthy patron offers education with no pressure, private decision time, accommodation, boundaries, and respect for refusal."},
        {"summary": "She earns transformation through school, coaching, practice, feedback, driving lessons, and fashion training. He knows she depends on me and does not ask her to belong to him. She controls passwords, accounts, earnings, contract review, lawyer review, and travel arrangements. She turns down another comfortable proposal because security without love is not enough."},
        {"summary": "He is arrested, accounts freeze, and court evidence puts him in prison. Lawyers examine documents, signatures, case files, testimony, appeal, bail, and original records until acquittal."},
        {"summary": "After he loses everything, she publicly asks marry me and chooses him. They return to the village to fund a roof, drainage, school support, and community rebuilding."},
    ]}
    result = evaluate_patronage_consent_integrity(premise, architecture, [])
    assert result["applies"] is True
    assert result["score_0_to_1"] == 1.0
    assert result["warnings"] == []


def test_patronage_consent_requires_dependency_patronage_context():
    from studio.patronage_consent_integrity import evaluate_patronage_consent_integrity
    result = evaluate_patronage_consent_integrity(
        {"title": "Model", "logline": "A woman becomes a model through work."},
        {"sequences": []},
        [],
    )
    assert result["applies"] is False


def test_patronage_consent_flags_debt_repayment_romance():
    from studio.patronage_consent_integrity import evaluate_patronage_consent_integrity
    result = evaluate_patronage_consent_integrity(
        {"title": "Bought Bride", "logline": "A billionaire transforms a poor village girl into a model and she marries him because she owes him."},
        {"sequences": [{"summary": "He pays for everything, tells her she belongs to him, and she accepts immediately."}]},
        [],
    )
    assert result["applies"] is True
    assert result["checks"]["dependency_suppresses_romantic_pressure"] is False
    assert result["checks"]["benefactor_collapse_inverts_power_before_choice"] is False
    assert result["warnings"]


def test_attachment_repair_full_chain_passes():
    from studio.attachment_repair_integrity import evaluate_attachment_repair_integrity
    premise = {"title": "Daddy I'm Home", "logline": "A grieving father believes his daughter is dead until his long-lost child comes home, and he learns happiness through attachment repair."}
    architecture = {"sequences": [
        {"summary": "The daughter says I'm not dead and came home after records were wrong. DNA, custody, social worker, home assessment, judge approval, placement, and visits safeguard the reunion."},
        {"summary": "The father says he won't make his daughter hide at a press conference and publicly claims my daughter. Care is small and repeated: eat, meal, shoes, bedtime, drawing, hug, toy, frog, hand, and cooking."},
        {"summary": "He uses therapy, breathing, rest, and asks adults for help. He promises five sharp, sets a reminder, apologizes when late, and will call if delayed. The scared child says she forgot me and he listens."},
        {"summary": "He tells her she didn't have to cure him, adults will help, she can love me and still go play, and it was not your fault. Mommy died but I see you, not a replacement. In the ending a teacher, uniformed helper, staff, safe home, school, therapy, and shared meal keep them together."},
    ]}
    result = evaluate_attachment_repair_integrity(premise, architecture, [])
    assert result["applies"] is True
    assert result["score_0_to_1"] == 1.0
    assert result["warnings"] == []


def test_attachment_repair_requires_child_family_loss_context():
    from studio.attachment_repair_integrity import evaluate_attachment_repair_integrity
    result = evaluate_attachment_repair_integrity(
        {"title": "Office Drama", "logline": "A CEO struggles with happiness at work."},
        {"sequences": []},
        [],
    )
    assert result["applies"] is False


def test_attachment_repair_flags_child_as_cure_without_correction():
    from studio.attachment_repair_integrity import evaluate_attachment_repair_integrity
    result = evaluate_attachment_repair_integrity(
        {"title": "Child Cure", "logline": "A grieving father believes his daughter is dead until his long-lost child comes home and cures his sadness forever."},
        {"sequences": [{"summary": "The child feeds him, makes him smile, and becomes his only reason to live."}]},
        [],
    )
    assert result["applies"] is True
    assert result["checks"]["parentification_is_explicitly_corrected"] is False
    assert result["checks"]["adult_grief_regulation_and_support"] is False
    assert result["warnings"]


def test_coerced_rechoice_full_chain_passes():
    from studio.coerced_rechoice_integrity import evaluate_coerced_rechoice_integrity
    premise={"title":"Strong Enough","logline":"A woman is forced to marry a poor single dad who is secretly a billionaire CEO because her missing twins are used as leverage."}
    architecture={"sequences":[{"summary":"The forced marriage uses missing children and tuition leverage. His scar and disguise come from assault, protection, trust, and safety. She does not know he is secretly rich and accepts ordinary partnership, children, bedtime, work, and the package deal before status reveal. Evidence, footage, complaint, attorney, police investigation, records, clinic verification, test, and arrest create accountability. Money was never the wound; she is not signing away her anger or accepting property as a bribe. The lie was betrayal and coercion remains a trust wound. Marital assets, control, documents, consent, choice, and decisions restore agency. Tell me the truth, no more lies, no more hiding. In the ending she freely chooses him as partner, not rescuer, no force, may I ask, when you are ready."}]}
    r=evaluate_coerced_rechoice_integrity(premise,architecture,[])
    assert r["applies"] is True
    assert r["score_0_to_1"] == 1.0


def test_coerced_rechoice_flags_wealth_absolution():
    from studio.coerced_rechoice_integrity import evaluate_coerced_rechoice_integrity
    premise={"title":"Rich Reveal","logline":"A woman is forced to marry a poor single dad who is secretly a billionaire CEO, then instantly forgives him because he is rich."}
    r=evaluate_coerced_rechoice_integrity(premise,{"sequences":[]},[])
    assert r["applies"] is True
    assert r["checks"]["final_choice_is_partnership_not_rescue"] is False
    assert r["checks"]["money_is_not_accepted_as_substitute_repair"] is False
    assert r["warnings"]


def test_attachment_repair_ignores_deadline_as_loss_word():
    from studio.attachment_repair_integrity import evaluate_attachment_repair_integrity
    result = evaluate_attachment_repair_integrity(
        {"title": "Emberseed Oven Cart", "logline": "A child and parent face a festival deadline while caring for a fire creature; the child is scared but hopeful."},
        {"sequences": []},
        [],
    )
    assert result["applies"] is False


def test_patronage_ignores_owe_inside_powered_and_generic_opportunity():
    from studio.patronage_consent_integrity import evaluate_patronage_consent_integrity
    result = evaluate_patronage_consent_integrity(
        {"title": "Clockwork Orphan Bench", "logline": "A discarded billionaire packaging concept becomes a powered bench that gives an orphan an opportunity to repair clocks."},
        {"sequences": []},
        [],
    )
    assert result["applies"] is False


def test_ending_safety_cannot_come_from_premise_setup_alone():
    from studio.attachment_repair_integrity import evaluate_attachment_repair_integrity
    premise = {"title": "Reunion", "logline": "A grieving father believes his daughter is dead until his long-lost child comes home; the ending has a teacher, safe home, school, therapy, and shared meal."}
    result = evaluate_attachment_repair_integrity(premise, {"sequences": []}, [])
    assert result["applies"] is True
    assert result["checks"]["ending_proves_ordinary_safety_systems"] is False


def test_patronage_and_rechoice_endings_cannot_come_from_premise_alone():
    from studio.patronage_consent_integrity import evaluate_patronage_consent_integrity
    from studio.coerced_rechoice_integrity import evaluate_coerced_rechoice_integrity
    patronage = evaluate_patronage_consent_integrity(
        {"title": "Patron", "logline": "A poor village girl owes money; a billionaire patron offers education and opportunity, and the ending returns to the village school."},
        {"sequences": []}, [],
    )
    assert patronage["checks"]["success_returns_as_communal_consequence"] is False
    rechoice = evaluate_coerced_rechoice_integrity(
        {"title": "Forced", "logline": "A woman is forced to marry a poor single dad who is secretly a billionaire CEO, and she freely chooses him as partner, not rescuer."},
        {"sequences": []}, [],
    )
    assert rechoice["checks"]["final_choice_is_partnership_not_rescue"] is False


def test_child_economic_claimant_full_chain_passes():
    from studio.child_economic_claimant_integrity import evaluate_child_economic_claimant_integrity
    premise={"title":"Daddy Pay Up","logline":"A little girl demands child support and formula money from a billionaire CEO deadbeat dad who owes a debt for diapers, hardship pay, expenses, and care."}
    architecture={"sequences":[{"summary":"At the company office lobby she publicly demands pay up, creating a scandal and leading to family tree, paternity, DNA, court, lawyer, and security consequences. She says don't trust, stay back, refuses strangers, hides after she overhears danger, observes, notices, figures out and helps catch the plot; she is not stupid. DNA, doctor, test, camera footage, police, lawyer, court, evidence, records, proof and investigation verify her claims. The mother was pregnant, working, sick, passing out, exiled, framed, set up, disbelieved, wronged, and suffered hardship. Is a simple sorry enough? Money is restitution not forgiveness and cannot buy trust. Adults and parents protect, investigate, and take responsibility while the child can play; the child is not responsible and it is not your job. Court, lawyer, arrest, police, stripped position, recover assets, forged evidence, fraud, consequences, and answer for it land. In the ending kindergarten, school, teacher, peers, class, rules, play, vacation, routine, ordinary home restore childhood."}]}
    r=evaluate_child_economic_claimant_integrity(premise,architecture,[])
    assert r["applies"] is True
    assert r["score_0_to_1"] == 1.0


def test_child_economic_claimant_rejects_nonclaimant_child_story():
    from studio.child_economic_claimant_integrity import evaluate_child_economic_claimant_integrity
    r=evaluate_child_economic_claimant_integrity({"title":"Family","logline":"A child loves her wealthy CEO father."},{"sequences":[]},[])
    assert r["applies"] is False


def test_child_economic_claimant_requires_ordinary_childhood_ending():
    from studio.child_economic_claimant_integrity import evaluate_child_economic_claimant_integrity
    premise={"title":"Daddy Pay Up","logline":"A little girl demands child support and formula money from a billionaire CEO deadbeat dad who owes a debt."}
    r=evaluate_child_economic_claimant_integrity(premise,{"sequences":[{"summary":"The corporate battle ends with adults praising the heir forever."}]},[])
    assert r["checks"]["ending_restores_ordinary_child_development"] is False


def test_economic_abandonment_full_chain_passes():
    from studio.economic_abandonment_integrity import evaluate_economic_abandonment_integrity
    premise={"title":"Train Station","logline":"After the wedding her husband left her at the train station saying don't belong, took everything, and betrayed her for money and orchard property."}
    architecture={"sequences":[{"summary":"Her purse, phone, wallet, id, ring, money, suitcase, letter, home, job, and credit are stripped. Maggie's cafe gives a job, room upstairs, shelter, meal, food, mutual aid not charity, work, labor and a broom defense. She notices invoice price discrepancies, financial bookkeeping, contracts, figures out the fraud, and sees a lawyer before romantic security. She refuses $50,000 to leave Chicago, the class bribe, purchased rescue, and says don't pay your way out. Invoice, financials, power of attorney, notarized revocation, bank loan, purchase agreement, court, judge, prosecutor, records, signature, proof, and evidence establish truth. $186,000 transfer cures the default, auction is canceled, he must pay back, the orchard is in her name, loan paid, debt paid, restitution. Maggie the rescuer is not by blood but mother; wherever I live she lives, our home is her home, chosen family. In the ending before I answer there is something you need to know, she makes a free choice and says yes; a door of her own, business, home, wedding, family, orchard, cafe, own name, belong and mom repair the threshold."}]}
    r=evaluate_economic_abandonment_integrity(premise,architecture,[])
    assert r["applies"] is True
    assert r["score_0_to_1"] == 1.0


def test_economic_abandonment_rejects_non_economic_breakup():
    from studio.economic_abandonment_integrity import evaluate_economic_abandonment_integrity
    r=evaluate_economic_abandonment_integrity({"title":"Breakup","logline":"A husband abandons his wife after an argument."},{"sequences":[]},[])
    assert r["applies"] is False


def test_economic_abandonment_requires_measurable_restitution():
    from studio.economic_abandonment_integrity import evaluate_economic_abandonment_integrity
    premise={"title":"Train Station","logline":"After the wedding her husband left her at the train station saying don't belong, stole everything, and betrayed her for money."}
    r=evaluate_economic_abandonment_integrity(premise,{"sequences":[{"summary":"She feels better because a wealthy man loves her."}]},[])
    assert r["checks"]["restitution_is_measurable"] is False
    assert r["checks"]["first_repair_is_mutual_aid_and_work"] is False


def test_wrongful_accusation_full_chain_passes():
    from studio.wrongful_accusation_integrity import evaluate_wrongful_accusation_integrity
    premise={"title":"Sixteen Years","logline":"A homeless scholarship student was framed and expelled for theft, and years later a planted necklace repeats the false accusation while evidence and court truth repair him."}
    architecture={"sequences":[{"summary":"His tools, repair, fix, work, job as groundskeeper, practical competence and labor come before pity. Nobody hires him after he is homeless, expelled, loses scholarship, housing, credit, reputation and career. Spencer still wears the same watch, the letter and planted fake copy are material contradictions. The necklace in the bag repeats the same trick, planted again like the watch in the bag as a second accusation. He gets a job and work for dignity, earns labor not charity, says not with your money, not for me, don't pay. She investigates questions, timeline, records, evidence, doubt, prove, verify and chain of custody instead of instantly believing. Camera footage, 911 log record, pawn jeweler witness court judge warrant lawyer signature documents evidence and chain of custody prove truth. Not with your money, not for me, don't pay because if you pay he wins preserves agency. In the ending Northbrook apology, readmission, scholarship, semester, school, reputation restored, land stays in trust, career and job restore the future. He says you don't have to answer, ask, if you still want, this time, consent, choose, will you, and she says yes."}]}
    r=evaluate_wrongful_accusation_integrity(premise,architecture,[])
    assert r["applies"] is True
    assert r["score_0_to_1"] == 1.0


def test_wrongful_accusation_rejects_unverified_romantic_belief():
    from studio.wrongful_accusation_integrity import evaluate_wrongful_accusation_integrity
    premise={"title":"Framed","logline":"A homeless scholarship student was framed and expelled for theft, but his old love simply knows he is innocent and they run away rich."}
    r=evaluate_wrongful_accusation_integrity(premise,{"sequences":[{"summary":"She loves him, so nobody needs evidence."}]},[])
    assert r["applies"] is True
    assert r["checks"]["truth_chain_is_procedural"] is False
    assert r["checks"]["institutional_restoration_repairs_stolen_future"] is False


def test_wrongful_accusation_rejects_nonstatus_accusation():
    from studio.wrongful_accusation_integrity import evaluate_wrongful_accusation_integrity
    r=evaluate_wrongful_accusation_integrity({"title":"Mystery","logline":"A person is accused of stealing a sandwich and immediately confesses."},{"sequences":[]},[])
    assert r["applies"] is False


def test_economic_restitution_ignores_sequence_timecodes():
    from studio.economic_abandonment_integrity import evaluate_economic_abandonment_integrity
    premise={"title":"Train Station","logline":"After the wedding her husband left her at the train station saying don't belong, stole everything, and betrayed her for money."}
    result=evaluate_economic_abandonment_integrity(premise,{"sequences":[{"timecode":"00:54:20","summary":"She talks at 54:20 but nobody repays anything."}]},[])
    assert result["checks"]["restitution_is_measurable"] is False


def test_melodrama_claimant_and_abandonment_ignore_creature_debt_contexts():
    from studio.child_economic_claimant_integrity import evaluate_child_economic_claimant_integrity
    from studio.economic_abandonment_integrity import evaluate_economic_abandonment_integrity
    creature={"title":"Emberseed Oven Cart","logline":"A child baker owes debt to a guild while protecting a fire creature whose company comforts her father."}
    assert evaluate_child_economic_claimant_integrity(creature,{"sequences":[]},[])["applies"] is False
    turtle={"title":"Foghorn Turtle Keeper","logline":"A keeper refuses to abandon an injured turtle and learns to trust a harbor family."}
    assert evaluate_economic_abandonment_integrity(turtle,{"sequences":[]},[])["applies"] is False


def test_wrongful_accusation_evaluates_unrepaired_romance():
    from studio.wrongful_accusation_integrity import evaluate_wrongful_accusation_integrity
    premise={"title":"Framed","logline":"A student is framed for theft, expelled, loses his scholarship and reputation, becomes homeless, and his old love simply chooses him."}
    r=evaluate_wrongful_accusation_integrity(premise,{"sequences":[{"summary":"They reunite with no evidence. His college never reinstates him. He does not ask and she never freely says yes."}]},[])
    assert r["applies"] is True
    assert r["checks"]["truth_chain_is_procedural"] is False
    assert r["checks"]["love_interest_investigates_instead_of_instantly_believing"] is False
    assert r["checks"]["institutional_restoration_repairs_stolen_future"] is False
    assert r["checks"]["romantic_closure_is_present_tense_consent"] is False


def test_economic_abandonment_present_tense_spousal_abandonment_applies():
    from studio.economic_abandonment_integrity import evaluate_economic_abandonment_integrity
    premise={"title":"Drained","logline":"A husband abandons his wife and drains their bank accounts."}
    r=evaluate_economic_abandonment_integrity(premise,{"sequences":[]},[])
    assert r["applies"] is True


def test_affirmative_match_does_not_negate_across_unrelated_noun():
    from studio.wrongful_accusation_integrity import evaluate_wrongful_accusation_integrity
    premise={"title":"Framed","logline":"A student is framed for theft, expelled, loses scholarship and reputation, becomes homeless."}
    arch={"sequences":[{"summary":"She has no money but she checks the evidence. The court and judge verify records. His tools and repair work give him a job. He says not with your money. The school offers readmission. He will ask and she says yes."}]}
    r=evaluate_wrongful_accusation_integrity(premise,arch,[])
    assert r["checks"]["love_interest_investigates_instead_of_instantly_believing"] is True
    assert r["checks"]["truth_chain_is_procedural"] is True


def test_wrongful_accusation_ending_tail_boundaries():
    from studio.wrongful_accusation_integrity import _ending_tail
    five="One. Two. Three. Four. Final reunion."
    assert "Final reunion." in _ending_tail(five)
    assert "Four." in _ending_tail(five)
    assert "One." not in _ending_tail(five)
    unpunctuated="opening evidence middle evidence final reinstatement reunion"
    tail=_ending_tail(unpunctuated)
    assert "reinstatement" in tail
    assert "opening" not in tail


def test_justified_expulsion_does_not_trigger_wrongful_accusation():
    from studio.wrongful_accusation_integrity import evaluate_wrongful_accusation_integrity
    premise={"title":"Consequences","logline":"A student is expelled for actual cheating and loses his scholarship."}
    assert evaluate_wrongful_accusation_integrity(premise,{"sequences":[]},[])["applies"] is False


def test_refusing_abandonment_does_not_trigger_economic_abandonment():
    from studio.economic_abandonment_integrity import evaluate_economic_abandonment_integrity
    premise={"title":"Stay","logline":"A husband refuses to abandon his family as debt mounts and the bank calls."}
    assert evaluate_economic_abandonment_integrity(premise,{"sequences":[]},[])["applies"] is False


def test_revenge_autonomy_full_chain_passes():
    from studio.revenge_autonomy_integrity import evaluate_revenge_autonomy_integrity
    premise={"title":"Drowned","logline":"Betrayed through identity fraud when twins switched places, publicly humiliated, pushed and thrown into the sea, a presumed dead drowned woman survives and returns with a new identity for revenge."}
    summary=("At the wedding and auction launch party the public room crowd guests filmed witnesses and trending spectators saw the coercion forced threat and public humiliation. Hospital doctor breath heartbeat injury blood drown water unconscious medical pain lost child body prove cost. She plans decides chooses strategy trap sting bait weapon orchestrates and sets up the revenge. He says only if you want, you choose, supports helps, asks before and won't touch. She takes a new name alias, chooses name, answers who do you want to be, calls herself Eve, identity choice not erase. Letter phone key files documents records bottle formula perfume object seal serial camera accounts ledger evidence proof become leverage. Bait public room auction stage launch same room turns the tables uses desire ownership against them and predator close. Police federal court lawyer regulator legal accounts frozen evidence files signature escrow verified warrant arrest investigation and chain of custody follow. No more favors, won't forgive, don't belong, not yours, refuse and no. In the ending she is free, freedom, live, won't belong, independent, her own, choice. He says I'll wait, if you choose, when you're ready, no pressure, not yours, doesn't claim and free choice.")
    r=evaluate_revenge_autonomy_integrity(premise,{"sequences":[{"summary":summary}]},[])
    assert r["applies"] is True
    assert r["score_0_to_1"] == 1.0


def test_revenge_autonomy_rejects_rescuer_owned_rebirth():
    from studio.revenge_autonomy_integrity import evaluate_revenge_autonomy_integrity
    premise={"title":"Rescued","logline":"Betrayed and publicly humiliated, a presumed dead woman survives drowning and returns for revenge."}
    r=evaluate_revenge_autonomy_integrity(premise,{"sequences":[{"summary":"A billionaire renames her, makes every plan, kisses her as his prize, and she forgives the villains."}]},[])
    assert r["applies"] is True
    assert r["checks"]["victim_authors_revenge_plan"] is False
    assert r["checks"]["new_identity_is_victim_chosen"] is False
    assert r["checks"]["ending_centers_autonomy_before_romance"] is False


def test_revenge_autonomy_ignores_simple_breakup_revenge():
    from studio.revenge_autonomy_integrity import evaluate_revenge_autonomy_integrity
    premise={"title":"Breakup","logline":"After a breakup she returns home and jokes about revenge."}
    assert evaluate_revenge_autonomy_integrity(premise,{"sequences":[]},[])["applies"] is False


def test_revenge_autonomy_ignores_exoneration_without_identity_return():
    import json
    from studio.revenge_autonomy_integrity import evaluate_revenge_autonomy_integrity
    premise=json.load(open('examples/generated_concepts/clockwork_orphan_bench_premise.json',encoding='utf8'))
    assert evaluate_revenge_autonomy_integrity(premise,{"sequences":[]},[])["applies"] is False


def test_wrongful_accusation_infers_exonerated_theft_accusation():
    from studio.wrongful_accusation_integrity import evaluate_wrongful_accusation_integrity
    premise={"title":"Cleared","logline":"An expelled scholarship student accused of theft becomes homeless, but footage clears him and he seeks work."}
    assert evaluate_wrongful_accusation_integrity(premise,{"sequences":[]},[])["applies"] is True


def test_affirmative_match_negation_scope_handles_both_cases():
    from studio.wrongful_accusation_integrity import _affirmative_match
    assert _affirmative_match(r"repay", "nobody persuades a debtor to repay") is False
    assert _affirmative_match(r"records?", "nobody checks the records") is False
    assert _affirmative_match(r"evidence", "she has no money but she checks the evidence") is True


def test_object_testimony_full_chain_passes():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Whispering Relics","logline":"An ordinary appraiser breaks an antique mirror and hears objects speak; relic voices whisper testimony, memory, provenance, fake artifacts, stolen cultural objects, restoration and auction truth."}
    summary=("Objects speak, relics remember, ask, beg, warn, don't melt, history memory belong. They remember limited clues, doesn't know, only saw, hypothesis lead, not proof, must verify. She has apprais craft work labor owed paycheck job competence inspection negotiate expert professional. Scan test lab CT fracture x-ray verify independent evidence proof record document inspect hash chain of custody prove leads. Scan test lab CT fracture independent police court lawyer warrant customs task force record log payment trail chain of custody sealed verify publicly. Own ownership control leash gift obedience salary voting rights shares name independence permission allowance are interrogated. Name stays, keeps name, not changing name, independent, my own life, don't own me, not yours, refuse, leaves control, blood doesn't decide. Museum cultural property provenance stolen recovered return restore restitution relics artifacts history memory matter. Villain wants power, useful threat exploit, price stolen, use ability, target bait criminal black market smuggle. In ending don't want shares, share future, not own, won't belong, independent, forgiveness honest choose condition stays.")
    r=evaluate_object_testimony_integrity(premise,{"sequences":[{"summary":summary}]},[])
    assert r["applies"] is True
    assert r["score_0_to_1"] == 1.0


def test_object_testimony_rejects_omniscient_treasure_power():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Magic Antiques","logline":"A girl hears antique objects speak and instantly knows every fake artifact and stolen treasure."}
    r=evaluate_object_testimony_integrity(premise,{"sequences":[{"summary":"She becomes rich, joins the family empire, and her fiancé controls the collection."}]},[])
    assert r["applies"] is True
    assert r["checks"]["verification_is_procedural"] is False
    assert r["checks"]["cultural_memory_or_restoration_matters"] is False
    assert r["checks"]["romance_or_family_does_not_own_future"] is False


def test_object_testimony_ignores_non_talking_objects():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Auction","logline":"An appraiser authenticates a fake antique using careful provenance research."}
    assert evaluate_object_testimony_integrity(premise,{"sequences":[]},[])["applies"] is False


def test_object_testimony_creature_voice_is_not_applicable():
    import json
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise=json.load(open('examples/generated_creature_concepts/salt_window_garden_premise.json'))
    assert evaluate_object_testimony_integrity(premise,{},[])["applies"] is False


def test_object_testimony_laboratory_test_counts_as_verification():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Whispering Relics","logline":"An appraiser hears an antique relic speak; its whispering object memory concerns fake provenance and stolen museum restoration."}
    summary=("The relic remembers only fragments, a hypothesis lead not proof. She is professional labor competence. Laboratory test is the corroboration. Ownership control gift salary independence. Name stays, refuse control. Museum cultural property recovered. Criminal black market exploit ability. Ending share future independent choose.")
    r=evaluate_object_testimony_integrity(premise,{"sequences":[{"summary":summary}]},[])
    assert r["checks"]["magic_produces_leads_not_verdicts"] is True
    assert r["checks"]["verification_is_procedural"] is True


def test_object_testimony_rejects_refusal_to_verify():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Whispering Relics","logline":"An appraiser hears antique relics speak; whispering objects remember fake provenance and stolen museum restoration."}
    summary=("The relic remembers everything. She refuses to verify and does not check records because magic decides. Professional labor craft. Ownership control. Name stays refuse control. Museum cultural property recovered. Criminal black market exploit ability. Ending share future independent choose.")
    r=evaluate_object_testimony_integrity(premise,{"sequences":[{"summary":summary}]},[])
    assert r["checks"]["object_testimony_is_limited_not_omniscient"] is False
    assert r["checks"]["magic_produces_leads_not_verdicts"] is False
    assert r["checks"]["verification_is_procedural"] is False


def test_object_testimony_named_artifact_voice_applies():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Watch","logline":"A museum appraiser hears a stolen watch speak; its testimony concerns provenance and restoration."}
    assert evaluate_object_testimony_integrity(premise,{"sequences":[]},[])["applies"] is True


def test_object_testimony_independent_chemical_analysis_counts():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Watch","logline":"A museum appraiser hears a stolen watch speak; its testimony concerns provenance and restoration."}
    summary=("The watch only remembers fragments of memory and offers a hypothesis lead not proof. Independent chemical analysis confirms the account. Professional appraiser labor. Ownership control. Name stays refuse control. Museum cultural property recovered. Criminal black market exploit ability. Ending share future independent choose.")
    r=evaluate_object_testimony_integrity(premise,{"sequences":[{"summary":summary}]},[])
    assert r["checks"]["magic_produces_leads_not_verdicts"] is True
    assert r["checks"]["verification_is_procedural"] is True


def test_object_testimony_physical_fragment_is_not_partial_memory():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Mirror","logline":"A museum appraiser hears a stolen mirror speak; its testimony concerns provenance and restoration."}
    summary="A mirror fragment cuts her hand. The mirror knows everything and she refuses to verify."
    r=evaluate_object_testimony_integrity(premise,{"sequences":[{"summary":summary}]},[])
    assert r["checks"]["object_testimony_is_limited_not_omniscient"] is False


def test_object_testimony_recounting_relic_applies():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Recounting Relic","logline":"A museum appraiser hears relics recount their history of stolen provenance and restoration."}
    assert evaluate_object_testimony_integrity(premise,{},[])["applies"] is True


def test_object_testimony_canceled_analysis_not_corroboration():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Watch","logline":"A museum appraiser hears a stolen watch speak; its testimony concerns provenance and restoration."}
    summary="The watch remembers only fragments of the theft. The appraiser cancels chemical analysis and trusts the relic."
    r=evaluate_object_testimony_integrity(premise,{"sequences":[{"summary":summary}]},[])
    assert r["checks"]["magic_produces_leads_not_verdicts"] is False
    assert r["checks"]["verification_is_procedural"] is False


def test_object_testimony_human_speakers_not_applicable():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Panel","logline":"A museum appraiser watches speakers discuss provenance and restoration."}
    assert evaluate_object_testimony_integrity(premise,{},[])["applies"] is False


def test_object_testimony_remembers_only_fragments_counts_limited():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Watch","logline":"A museum appraiser hears a stolen watch speak; its testimony concerns provenance and restoration."}
    summary="The relic remembers only fragments of a theft."
    r=evaluate_object_testimony_integrity(premise,{"sequences":[{"summary":summary}]},[])
    assert r["checks"]["object_testimony_is_limited_not_omniscient"] is True


def test_object_testimony_speaking_watch_has_personhood():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Watch","logline":"A museum appraiser hears a stolen watch speak; its testimony concerns provenance and restoration."}
    summary="The museum watch speaks and begs to be spared."
    r=evaluate_object_testimony_integrity(premise,{"sequences":[{"summary":summary}]},[])
    assert r["checks"]["objects_have_history_or_personhood"] is True


def test_object_testimony_third_person_speaks_applies():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Watch","logline":"A museum appraiser discovers that a stolen watch speaks about provenance and restoration."}
    assert evaluate_object_testimony_integrity(premise,{},[])["applies"] is True


def test_object_testimony_unrelated_cancellation_preserves_analysis():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Watch","logline":"A museum appraiser hears a stolen watch speak; its testimony concerns provenance and restoration."}
    summary="The watch remembers only fragments of the theft. The appraiser cancels an auction and orders chemical analysis."
    r=evaluate_object_testimony_integrity(premise,{"sequences":[{"summary":summary}]},[])
    assert r["checks"]["magic_produces_leads_not_verdicts"] is True
    assert r["checks"]["verification_is_procedural"] is True


def test_object_testimony_non_speaking_revealing_artifacts_not_applicable():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Artifacts","logline":"Museum artifacts reveal a collection's history of provenance and restoration without speaking."}
    assert evaluate_object_testimony_integrity(premise,{},[])["applies"] is False


def test_object_testimony_testify_and_reveal_aloud_apply():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    one={"title":"Relics","logline":"A museum appraiser hears museum relics testify about stolen provenance and restoration."}
    two={"title":"Relics","logline":"A museum appraiser hears relics reveal their stolen provenance history aloud."}
    assert evaluate_object_testimony_integrity(one,{},[])["applies"] is True
    assert evaluate_object_testimony_integrity(two,{},[])["applies"] is True


def test_object_testimony_speaking_watch_personhood_third_person():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Watch","logline":"A museum appraiser hears the stolen watch speak about provenance and restoration."}
    summary="The stolen watch speaks."
    r=evaluate_object_testimony_integrity(premise,{"sequences":[{"summary":summary}]},[])
    assert r["checks"]["objects_have_history_or_personhood"] is True


def test_object_testimony_speaks_volumes_idiom_not_applicable():
    from studio.object_testimony_integrity import evaluate_object_testimony_integrity
    premise={"title":"Museum Artifact","logline":"The artifact speaks volumes about museum history, provenance, and restoration."}
    assert evaluate_object_testimony_integrity(premise,{},[])["applies"] is False


def _competence_cascade_fixture():
    premise={
        "title":"The Quiet Blade",
        "logline":"A reborn assassin in a bullied scholarship student's body protects her poor family and takes revenge after classmates publicly read her diary.",
    }
    architecture={
        "sequences":[
            {"summary":"School bullies publicly read her diary and humiliate her. Her mother cares for her in hospital while her brother sacrifices school and the family faces medical debt."},
            {"summary":"She proves hidden competence early in a night race, then uses combat skill against debt collectors while explaining the clean source of prize money and evidence."},
            {"summary":"The academy math contest, military shooting training, hospital family scenes, elite banquet, underground arena, and police investigation rotate the same wound through new institutions."},
            {"summary":"During a team test she refuses to abandon a wounded comrade and shields a subordinate, proving loyalty is the real standard."},
        ],
        "ending_payoff":{"repair":"Police, law, and a public apology close the conspiracy. The ally stands with her without taking over, respects her choice, justice and family belonging land, and only then a new mission calls her back."},
    }
    scenes=[{"summary":"She becomes a special agent and instructor; marriage is framed by explicit mutual consent and she freely chooses intimacy."}]
    return premise,architecture,scenes


def test_competence_cascade_integrity_balanced_example_passes_core_checks():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    r=evaluate_competence_cascade_integrity(premise,architecture,scenes)
    assert r["applies"] is True
    assert r["checks"]["distinct_competence_domains"] is True
    assert r["checks"]["institutional_arena_rotation"] is True
    assert r["checks"]["ethical_loyalty_test"] is True
    assert r["checks"]["closure_before_mission_hook"] is True
    assert r["checks"]["romance_or_intimacy_respects_refusal"] is True


def test_competence_cascade_integrity_flags_refusal_overriding_romance():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes.append({"summary":"During intimacy, when she asks him to stop, he laughs that she has no right to refuse."})
    r=evaluate_competence_cascade_integrity(premise,architecture,scenes)
    assert r["checks"]["romance_or_intimacy_respects_refusal"] is False
    assert any("coercive refusal" in w for w in r["warnings"])


def test_competence_cascade_integrity_flags_hook_before_closure():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture["ending_payoff"]={"repair":"A new mission calls her back immediately. Much later, justice and family belonging are only vaguely mentioned."}
    r=evaluate_competence_cascade_integrity(premise,architecture,scenes)
    assert r["checks"]["closure_before_mission_hook"] is False


def test_competence_cascade_integrity_not_applicable_without_hidden_mastery_reversal():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise={"title":"Gentle Garden","logline":"A gardener repairs a community greenhouse."}
    r=evaluate_competence_cascade_integrity(premise,{},[])
    assert r["applies"] is False


def test_competence_cascade_applies_to_bullied_secret_prodigy():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise={"title":"Hidden Numbers","logline":"A bullied scholarship student is secretly a mathematical prodigy and takes revenge on the academy that humiliated her."}
    assert evaluate_competence_cascade_integrity(premise,{},[])["applies"] is True


def test_competence_cascade_does_not_apply_when_assassin_is_only_villain():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise={"title":"Ordinary Target","logline":"A bullied student survives when an assassin villain attacks her school; she has no hidden mastery."}
    assert evaluate_competence_cascade_integrity(premise,{},[])["applies"] is False


def test_competence_cascade_architecture_closure_survives_final_mission_scene():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes=[{"summary":"After the victory epilogue, command gives her a new mission."}]
    r=evaluate_competence_cascade_integrity(premise,architecture,scenes)
    assert r["checks"]["closure_before_mission_hook"] is True


def test_competence_cascade_detects_ignored_refusal_during_kiss():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes.append({"summary":"She asked him to stop, but he kept kissing her."})
    r=evaluate_competence_cascade_integrity(premise,architecture,scenes)
    assert r["checks"]["romance_or_intimacy_respects_refusal"] is False


def test_competence_cascade_military_order_refusal_is_not_romantic_coercion():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes.append({"summary":"The commander says soldiers can't refuse a lawful order during the mission briefing."})
    r=evaluate_competence_cascade_integrity(premise,architecture,scenes)
    assert r["checks"]["romance_or_intimacy_respects_refusal"] is True


def test_competence_cascade_title_skill_is_not_early_proof():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    premise["title"]="The Skilled Assassin"
    architecture["sequences"]=[
        {"summary":"School bullies publicly humiliate her while her poor mother cares for the family through medical debt."},
        {"summary":"The family argues about debt collectors, hospital bills, and school prejudice without any demonstration of her ability."},
        {"summary":"The academy, military, banquet, arena, and police institutions rotate while she refuses to abandon a wounded comrade."},
        {"summary":"In the finale she finally demonstrates skill, wins evidence, and police close the case according to law."},
    ]
    r=evaluate_competence_cascade_integrity(premise,architecture,scenes)
    assert r["checks"]["hidden_competence_is_proven_early"] is False


def test_compressed_wish_integrity_balanced_creature_family_example():
    from studio.compressed_wish_integrity import evaluate_compressed_wish_integrity
    premise={"title":"The Tide Star","logline":"A mermaid son wishes for a tail because his legs make him too slow and he feels caught between sea and land family worlds."}
    architecture={"sequences":[
      {"summary":"Daddy has one breath underwater. At Christmas the child learns to give something you love to someone you love, then follows the fallen star because he thinks it fell for him."},
      {"summary":"The wishing star is a creature baby alone and scared. When the mother creature attacks, the child learns that's her baby and gives it back for you."},
      {"summary":"The mother admits she blamed the father's stories but they brought him home. Grandpa says the child stood between them with one breath."},
      {"summary":"In the sea a tail, on land your legs; he gave his star away and got his wish, closing Christmas with merry Christmas."},
    ]}
    r=evaluate_compressed_wish_integrity(premise,architecture,[])
    assert r["applies"] is True
    assert r["checks"]["possession_reframed_as_attachment"] is True
    assert r["checks"]["sacrifice_before_reward"] is True
    assert r["checks"]["transformation_integrates_identity"] is True


def test_compressed_wish_integrity_flags_vending_machine_reward():
    from studio.compressed_wish_integrity import evaluate_compressed_wish_integrity
    premise={"title":"Tail Wish","logline":"A mermaid son wishes for a tail."}
    architecture={"sequences":[{"summary":"He finds a magic stone and immediately gets a tail."}]}
    r=evaluate_compressed_wish_integrity(premise,architecture,[])
    assert r["checks"]["wish_carrier_is_vulnerable_or_personlike"] is False
    assert r["checks"]["sacrifice_before_reward"] is False
    assert r["score_0_to_1"] < 0.5


def test_competence_cascade_hook_before_closure_across_scene_order_fails():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['ending_payoff']={'repair':'Status victory is mentioned.'}
    scenes=[
      {"summary":"Command gives her a new mission."},
      {"summary":"Only afterward does she reunite with family and belonging."},
    ]
    r=evaluate_competence_cascade_integrity(premise,architecture,scenes)
    assert r['checks']['closure_before_mission_hook'] is False


def test_competence_cascade_consensual_continued_kissing_passes():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes.append({"summary":"They both consent enthusiastically, and he keeps kissing her as she pulls him closer."})
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['romance_or_intimacy_respects_refusal'] is True


def test_competence_cascade_midpoint_reversal_coercion_is_checked():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['midpoint_reversal']='During intimacy she says stop, but he keeps kissing her.'
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['romance_or_intimacy_respects_refusal'] is False


def test_compressed_wish_reward_before_sacrifice_fails_order():
    from studio.compressed_wish_integrity import evaluate_compressed_wish_integrity
    premise={"title":"The Tide Star","logline":"A mermaid son wishes for a tail because he feels slow between sea and land."}
    architecture={"sequences":[{"summary":"He follows the wishing star, which is a creature baby. In the sea a tail appears and his wish comes true. Much later he gives the baby back and says for you."}]}
    assert evaluate_compressed_wish_integrity(premise,architecture,[])['checks']['sacrifice_before_reward'] is False


def test_compressed_wish_details_do_not_mean_tail():
    from studio.compressed_wish_integrity import evaluate_compressed_wish_integrity
    premise={"title":"Family Mystery","logline":"A mother wishes detectives would uncover the details of a realistic family mystery."}
    assert evaluate_compressed_wish_integrity(premise,{},[])['applies'] is False


def test_competence_cascade_after_clause_refusal_is_detected():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes.append({"summary":"He keeps kissing her after she says no."})
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['romance_or_intimacy_respects_refusal'] is False


def test_competence_cascade_anti_patterns_checklist_not_story_evidence():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['anti_patterns_checked']=['During intimacy she says stop, but he keeps kissing her.']
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['romance_or_intimacy_respects_refusal'] is True


def test_competence_cascade_scene_closure_before_teaser_beats_recap_order():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['ending_payoff']={'repair':'Recap: a new mission was teased, after justice and family belonging had already been resolved.'}
    scenes=[
      {"summary":"Police close the case and justice restores the family."},
      {"summary":"Finally command gives her a new mission."},
    ]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is True


def test_competence_cascade_closure_without_teaser_passes():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['ending_payoff']={'repair':'Police close the case; justice and family belonging are restored.'}
    scenes=[{'summary':'The family returns home in peace.'}]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is True


def test_competence_cascade_split_outline_closure_then_teaser_passes():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['sequences'][-1]={'summary':'Police deliver justice and the family is reunited.'}
    architecture['ending_payoff']={'repair':'Afterward command gives her a new mission.'}
    scenes=[]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is True


def test_competence_cascade_now_kiss_me_is_not_refusal():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes.append({'summary':'She says, “Now kiss me again,” and he keeps kissing her.'})
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['romance_or_intimacy_respects_refusal'] is True


def test_taboo_family_irony_balanced_example():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'The Don Next Door','logline':'A student secretly marries a powerful older mafia boss, unaware he is her best friend\'s father.'}
    architecture={'sequences':[
      {'summary':'The audience knows the hidden identity while the best friend stays unaware and investigates to protect her.'},
      {'summary':'Mansion breakfast, boutique shopping, campus humiliation, hockey arena party, and mafia business operations rotate the conflict.'},
      {'summary':'After public gold-digger shame, he uses evidence and family rules rather than lawless force. She hears the truth, says no more lies, rejects him, and can leave.'},
      {'summary':'He apologizes for possessive surveillance and asks for free choice. The final reveal makes the best friend ask whether she is now family or stepmother.'}
    ]}
    r=evaluate_taboo_family_irony_integrity(premise,architecture,[])
    assert r['applies'] is True
    assert r['score_0_to_1'] > 0.8


def test_taboo_family_irony_flags_unrepaired_possession():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Owned',"logline":"A student secretly marries a mafia boss who is her best friend's father."}
    architecture={'sequences':[{'summary':'After a drunken marriage he cuts her internet, uses surveillance, and says you are mine. The story treats this as romantic proof.'}]}
    r=evaluate_taboo_family_irony_integrity(premise,architecture,[])
    assert r['checks']['possessiveness_is_flaw_not_reward'] is False
    assert r['score_0_to_1'] < 0.7


def test_competence_cascade_opening_family_is_not_final_closure():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['ending_payoff']={'repair':'The conflict remains open.'}
    scenes=[
      {'summary':'The family appears in the opening hospital backstory.'},
      {'summary':'The academy conflict escalates.'},
      {'summary':'The final scene leaves the conspiracy unresolved.'},
    ]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is False


def test_competence_cascade_recapped_early_mission_is_not_positioned_late():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['sequences'][-1]={'summary':'Police deliver justice and the family is reunited.'}
    architecture['ending_payoff']={'repair':'Recap: before the finale, command had already offered her a new mission.'}
    assert evaluate_competence_cascade_integrity(premise,architecture,[])['checks']['closure_before_mission_hook'] is False


def test_competence_cascade_drawn_out_refusal_is_detected():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes.append({'summary':'She says, “Nooo!”, but he keeps kissing her.'})
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['romance_or_intimacy_respects_refusal'] is False


def test_taboo_family_irony_stormglass_not_applicable():
    import json
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise=json.load(open('examples/stormglass_project/premise.json',encoding='utf8'))
    assert evaluate_taboo_family_irony_integrity(premise,{},[])['applies'] is False


def test_taboo_family_irony_truth_reveal_does_not_mask_coercion():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Bestie Dad','logline':"A student secretly marries a mafia boss who is her bestie's father."}
    architecture={'sequences':[{'summary':'She learns the truth, but he says she has no right to refuse, keeps surveillance, and calls that love.'}]}
    r=evaluate_taboo_family_irony_integrity(premise,architecture,[])
    assert r['applies'] is True
    assert r['checks']['possessiveness_is_flaw_not_reward'] is False
    assert r['checks']['protagonist_can_reject_power'] is False
    assert r['checks']['truth_and_consent_repair'] is False


def test_competence_cascade_before_credits_mission_passes():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['sequences'][-1]={'summary':'Police deliver justice and the family is reunited.'}
    architecture['ending_payoff']={'repair':'Before the credits roll, she accepts a new mission.'}
    assert evaluate_competence_cascade_integrity(premise,architecture,[])['checks']['closure_before_mission_hook'] is True


def test_competence_cascade_new_unresolved_case_does_not_negate_closure():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['sequences'][-1]={'summary':'Police deliver justice and the family is reunited.'}
    architecture['ending_payoff']={'repair':'A new mission sends her after an unresolved case in another city.'}
    assert evaluate_competence_cascade_integrity(premise,architecture,[])['checks']['closure_before_mission_hook'] is True


def test_taboo_family_irony_besties_dad_applies():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Secret Vows','logline':"She secretly marries a mafia boss, unaware he is her bestie's dad."}
    assert evaluate_taboo_family_irony_integrity(premise,{},[])['applies'] is True


def test_taboo_family_irony_late_logline_not_opening_evidence():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Late Reveal','logline':"She secretly marries a mafia boss, unaware he is her bestie's dad.",'opening_event':{'first_60_seconds':'She studies quietly at school and nothing romantic or criminal is established.'}}
    r=evaluate_taboo_family_irony_integrity(premise,{},[])
    assert r['checks']['compounded_impossibility_early'] is False


def test_taboo_family_irony_shared_reveal_not_superior_knowledge():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Shared Reveal','logline':"She secretly marries a mafia boss, unaware he is her bestie's dad."}
    architecture={'sequences':[{'summary':'The audience and characters learn the secret together at the ending; until then she is unaware.'}]}
    assert evaluate_taboo_family_irony_integrity(premise,architecture,[])['checks']['audience_has_superior_knowledge'] is False


def test_competence_cascade_unresolved_original_plus_mission_fails():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['sequences'][-1]={'summary':'Police deliver justice for one minor victim.'}
    architecture['ending_payoff']={'repair':'The original conflict remains unresolved, and a new mission begins.'}
    assert evaluate_competence_cascade_integrity(premise,architecture,[])['checks']['closure_before_mission_hook'] is False


def test_competence_cascade_full_scene_order_crosses_cutoff():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['ending_payoff']={'repair':'Status epilogue.'}
    resolved_then_hook=[
      {'summary':'Opening setup.'},{'summary':'Middle escalation.'},{'summary':'Police deliver justice and family is reunited.'},
      {'summary':'Epilogue noise.'},{'summary':'Finally command gives her a new mission.'},
    ]
    hook_then_resolved=[
      {'summary':'Opening setup.'},{'summary':'Command gives her a new mission.'},{'summary':'Middle escalation.'},
      {'summary':'More escalation.'},{'summary':'Police deliver justice and family is reunited.'},
    ]
    assert evaluate_competence_cascade_integrity(premise,architecture,resolved_then_hook)['checks']['closure_before_mission_hook'] is True
    assert evaluate_competence_cascade_integrity(premise,architecture,hook_then_resolved)['checks']['closure_before_mission_hook'] is False


def test_taboo_family_irony_falls_inlove_and_former_guardian_apply():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    one={'title':'Guardian Secret','logline':'She falls in love with a powerful mafia boss who is her former guardian, hiding the truth.'}
    two={'title':'Bestie Parent','logline':"She falls in love with a powerful mafia boss, unaware he is her bestie's dad."}
    assert evaluate_taboo_family_irony_integrity(one,{},[])['applies'] is True
    assert evaluate_taboo_family_irony_integrity(two,{},[])['applies'] is True


def test_taboo_family_irony_cut_to_internet_not_coercion():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Bestie Parent','logline':"She secretly marries a mafia boss, unaware he is her bestie's dad."}
    architecture={'sequences':[{'summary':'Cut to a classroom scene.'},{'summary':'She uses the internet for homework.'}]}
    r=evaluate_taboo_family_irony_integrity(premise,architecture,[])
    assert r['checks']['possessiveness_is_flaw_not_reward'] is True


def test_taboo_family_irony_chooses_to_leave_counts_agency():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Bestie Parent','logline':"She secretly marries a mafia boss, unaware he is her bestie's dad."}
    architecture={'sequences':[{'summary':'After the truth comes out, she chooses to leave him.'}]}
    assert evaluate_taboo_family_irony_integrity(premise,architecture,[])['checks']['protagonist_can_reject_power'] is True


def test_competence_cascade_same_scene_finale_order_positions():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['ending_payoff']={'repair':'Status epilogue.'}
    good=[{'summary':'In the finale police close the conspiracy, and only then command offers a new mission.'}]
    bad=[{'summary':'In the finale command offers a new mission, before police close the conspiracy.'}]
    assert evaluate_competence_cascade_integrity(premise,architecture,good)['checks']['closure_before_mission_hook'] is True
    assert evaluate_competence_cascade_integrity(premise,architecture,bad)['checks']['closure_before_mission_hook'] is False


def test_competence_cascade_setup_family_or_school_order_not_finale_evidence():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['ending_payoff']={'repair':'Status epilogue.'}
    scenes=[
      {'summary':'Opening: her family is poor and the school ordered her to attend class.'},
      {'summary':'A new mission is mentioned in the middle.'},
      {'summary':'The case is closed at the end.'},
    ]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is False


def test_competence_cascade_new_open_case_and_explicit_conspiracy_unresolved():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['sequences'][-1]={'summary':'Police close the conspiracy.'}
    architecture['ending_payoff']={'repair':'The main case is closed. Her new mission leaves the next case unresolved.'}
    assert evaluate_competence_cascade_integrity(premise,architecture,[])['checks']['closure_before_mission_hook'] is True
    architecture['ending_payoff']={'repair':'She goes home. The conspiracy is unresolved.'}
    assert evaluate_competence_cascade_integrity(premise,architecture,[])['checks']['closure_before_mission_hook'] is False


def test_taboo_family_irony_access_internet_coercion_and_bestfriend_departure():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Bestie Parent','logline':"She secretly marries a mafia boss, unaware he is her bestie's dad."}
    architecture={'sequences':[{'summary':'He cut off her access to the internet.'}]}
    assert evaluate_taboo_family_irony_integrity(premise,architecture,[])['checks']['possessiveness_is_flaw_not_reward'] is False
    architecture={'sequences':[{'summary':'The best friend chooses to leave town for college.'}]}
    assert evaluate_taboo_family_irony_integrity(premise,architecture,[])['checks']['protagonist_can_reject_power'] is False


def test_competence_cascade_explicit_before_order_beats_field_order():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['ending_payoff']={'repair':'Status epilogue.'}
    scenes=[{'visual_action':'Final reunion image: the family is reunited.','dialogue_design':'The commander offers a new mission before this final reunion image.'}]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is False


def test_competence_cascade_separate_payoff_field_sequel_mystery_not_original():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['sequences'][-1]={'summary':'Police close the conspiracy.'}
    architecture['ending_payoff']={'repair':'The case is closed and the family is reunited.','sequel':'The new case mystery remains open for the next mission.'}
    assert evaluate_competence_cascade_integrity(premise,architecture,[])['checks']['closure_before_mission_hook'] is True


def test_competence_cascade_role_acceptance_closure_and_fresh_assignment_hook():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    architecture['ending_payoff']={'repair':'Status epilogue.'}
    good=[{'summary':'She earns her new role and finds acceptance. Only then command gives her a fresh case.'}]
    bad=[{'summary':'Command gives her a fresh case before she earns her new role and finds acceptance.'}]
    assert evaluate_competence_cascade_integrity(premise,architecture,good)['checks']['closure_before_mission_hook'] is True
    assert evaluate_competence_cascade_integrity(premise,architecture,bad)['checks']['closure_before_mission_hook'] is False


def test_taboo_family_irony_named_protagonist_chooses_to_leave_partner():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Bestie Parent','protagonist_name':'Lily','logline':"She secretly marries a mafia boss, unaware he is her bestie's dad."}
    architecture={'sequences':[{'summary':'After the reveal, Lily chooses to leave him.'}]}
    assert evaluate_taboo_family_irony_integrity(premise,architecture,[])['checks']['protagonist_can_reject_power'] is True


def _chosen_bond_fixture():
    premise={
        'title':'The Chosen Queen',
        'logline':'At her bonding ceremony, a healer is publicly humiliated when her fated mate chooses another woman, so she refuses him and later chooses a consenting elven king.',
        'opening_event':{'first_60_seconds':'At the public bonding ceremony before the clan, her fated mate crowns another woman and humiliates her.'},
    }
    architecture={
        'sequences':[
            {'summary':'At the public wedding ceremony he cheats and says fate is a curse they cannot resist, using destiny as an excuse while her parents support her exit.'},
            {'summary':'For years her blood essence and healing elixir kept his rage at bay, sustained the clan, and secured his succession position.'},
            {'summary':'She refuses to accept the humiliating marriage before the elf king appears; only afterward does she consider the chosen partner.'},
            {'summary':'He heals her power core, protects her, waits patiently, says he will not bind her with so-called fate, and asks consent with no pressure.'},
            {'summary':'Only after that care does she believe him and later reciprocate with a mutual vow. When he begs forgiveness, she rejects his apology because regret is not repair and he chose power.'},
            {'summary':'At the banquet witnesses see the impostor; blood resonance gives physical proof, the ring and potion mechanism explain the fraud, and his confession supplies testimony before the council strips his title, revokes resources, and banishes him.'},
            {'summary':'She goes home with her freely chosen partner and chosen family in peace.'},
        ]
    }
    scenes=[]
    return premise,architecture,scenes


def test_chosen_bond_integrity_balanced_example_passes_core_checks():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise,architecture,scenes=_chosen_bond_fixture()
    r=evaluate_chosen_bond_integrity(premise,architecture,scenes)
    assert r['applies'] is True
    assert r['checks']['public_betrayal_opening'] is True
    assert r['checks']['sacrificial_labor_has_system_value'] is True
    assert r['checks']['fate_functions_as_excuse'] is True
    assert r['checks']['protagonist_refuses_before_upgrade'] is True
    assert r['checks']['alternative_bond_is_chosen_and_consenting'] is True
    assert r['checks']['care_precedes_romantic_reciprocity'] is True
    assert r['checks']['late_repentance_is_not_rewarded'] is True
    assert r['checks']['exposure_is_layered_evidence'] is True
    assert r['checks']['institutional_consequence_matches_institutional_theft'] is True
    assert r['checks']['closure_reclassifies_home_or_chosen_family'] is True


def test_chosen_bond_integrity_not_applicable_to_ordinary_romance():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise={'title':'Ordinary Romance','logline':'Two rivals fall in love while restoring a bakery.'}
    assert evaluate_chosen_bond_integrity(premise,{},[])['applies'] is False


def test_chosen_bond_integrity_flags_upgrade_before_refusal_and_forced_forgiveness():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise,architecture,scenes=_chosen_bond_fixture()
    architecture['sequences']=[
      {'summary':'At the public bonding ceremony her fated mate humiliates her and chooses another woman. The elf king immediately claims her as his mate before she refuses anyone.'},
      {'summary':'Her blood essence sustained his succession. Destiny made them do it. There is no evidence or procedure. Her family makes her forgive him and she returns to the clan.'},
    ]
    r=evaluate_chosen_bond_integrity(premise,architecture,scenes)
    assert r['checks']['protagonist_refuses_before_upgrade'] is False
    assert r['checks']['alternative_bond_is_chosen_and_consenting'] is False
    assert r['checks']['exposure_is_layered_evidence'] is False
    assert r['checks']['institutional_consequence_matches_institutional_theft'] is False
    assert r['checks']['forgiveness_is_not_coerced'] is False


def test_taboo_family_irony_best_friend_leaving_own_husband_not_heroine_agency():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Bestie Parent','protagonist_name':'Lily','logline':"She secretly marries a mafia boss, unaware he is her bestie's dad."}
    architecture={'sequences':[{'summary':'The best friend chooses to leave her own husband. Lily remains trapped.'}]}
    assert evaluate_taboo_family_irony_integrity(premise,architecture,[])['checks']['protagonist_can_reject_power'] is False


def test_chosen_bond_does_not_apply_to_creature_imprint_protection():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise={'title':'Stormglass','logline':'A dragon imprints on a child protector guarding a kingdom and abandoned hideout.'}
    assert evaluate_chosen_bond_integrity(premise,{},[])['applies'] is False


def test_chosen_bond_forced_new_marriage_is_not_consenting():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise,architecture,scenes=_chosen_bond_fixture()
    architecture['sequences'][3]={'summary':'The elf king asks for her hand, then forces her to marry him against her will.'}
    assert evaluate_chosen_bond_integrity(premise,architecture,scenes)['checks']['alternative_bond_is_chosen_and_consenting'] is False


def test_chosen_bond_premise_only_chronology_can_order_refusal_and_care():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise={
      'title':'Chosen After Betrayal',
      'logline':'At a public wedding ceremony her fated mate cheats with another woman. She refuses him before the chosen partner appears; he heals and protects her patiently before she believes him and accepts a mutual vow. The council strips the betrayer of his title and she goes home with chosen family.',
    }
    r=evaluate_chosen_bond_integrity(premise,{},[])
    assert r['checks']['protagonist_refuses_before_upgrade'] is True
    assert r['checks']['care_precedes_romantic_reciprocity'] is True


def test_chosen_bond_care_for_ex_does_not_count_as_new_partner_care():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise,architecture,scenes=_chosen_bond_fixture()
    architecture['sequences']=[
      {'summary':'At the public bonding ceremony her fated mate cheats and humiliates her; her blood essence sustained his succession.'},
      {'summary':'She refuses him before the elf king appears as a chosen partner. She heals her former mate one last time. She accepts the king, then he finally protects her, and she believes him.'},
    ]
    assert evaluate_chosen_bond_integrity(premise,architecture,scenes)['checks']['care_precedes_romantic_reciprocity'] is False


def test_chosen_bond_happy_fated_wedding_is_not_public_betrayal():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise,architecture,scenes=_chosen_bond_fixture()
    premise['opening_event']={'first_60_seconds':'At the public bonding ceremony she happily marries her fated mate.'}
    architecture['sequences']=[
      {'summary':'At the public wedding ceremony she happily marries her fated mate; betrayal arrives years later.'},
      {'summary':'They share a quiet domestic life with no immediate betrayal.'},
      {'summary':'The later betrayal is foreshadowed only as a distant future problem.'},
    ]
    assert evaluate_chosen_bond_integrity(premise,architecture,scenes)['checks']['public_betrayal_opening'] is False


def test_competence_cascade_opening_investigation_not_sequel_hook():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes=[
      {'id':'S01','scene_goal':'The agency assigns her to investigate the missing child.'},
      {'id':'S02','scene_goal':'Her hidden mastery is publicly revealed.'},
      {'id':'S03','scene_goal':'Police close the conspiracy, the family is reunited, and peace is restored.'},
    ]
    r=evaluate_competence_cascade_integrity(premise,architecture,scenes)
    assert r['checks']['closure_before_mission_hook'] is True
    assert not any('sequel' in w for w in r['warnings'])


def test_competence_cascade_banquet_justice_celebration_does_not_override_closed_case():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes=[
      {'id':'S01','scene_goal':'She accepts the investigation.'},
      {'id':'S02','scene_goal':'Police close the conspiracy.'},
      {'id':'S03','scene_goal':'She receives a fresh assignment before leaving a banquet celebrating justice.'},
    ]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is True


def test_chosen_bond_applies_to_destiny_bride_unfaithful_groom_rechoice():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise={'title':'Destiny Bride','logline':'A bride bound by destiny leaves her unfaithful groom and falls for another person.'}
    assert evaluate_chosen_bond_integrity(premise,{},[])['applies'] is True


def test_chosen_bond_old_coercion_and_no_force_promise_do_not_disqualify_new_bond():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise,architecture,scenes=_chosen_bond_fixture()
    architecture['sequences']=[
      {'summary':'At the public bonding ceremony her fated mate cheats and humiliates her; she was forced to marry him under the old clan contract.'},
      {'summary':'She refuses him before the elf king appears as a chosen partner. He promises not to force marriage, heals her patiently, and waits for her answer before she believes him.'},
    ]
    assert evaluate_chosen_bond_integrity(premise,architecture,scenes)['checks']['alternative_bond_is_chosen_and_consenting'] is True


def test_chosen_bond_named_partner_care_counts_before_reciprocity():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise,architecture,scenes=_chosen_bond_fixture()
    architecture['sequences']=[
      {'summary':'At the public bonding ceremony her fated mate cheats and humiliates her; her blood essence sustained his succession.'},
      {'summary':'She refuses him before the elf king, Calith, appears as a chosen partner. Calith heals her wounds and protects her patiently before she believes him.'},
    ]
    assert evaluate_chosen_bond_integrity(premise,architecture,scenes)['checks']['care_precedes_romantic_reciprocity'] is True


def test_chosen_bond_public_betrayal_can_cross_adjacent_opening_sentences():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise,architecture,scenes=_chosen_bond_fixture()
    premise['opening_event']={'first_60_seconds':'The clan gathers for the public bonding ceremony. In front of everyone, her fated mate cheats and humiliates her.'}
    assert evaluate_chosen_bond_integrity(premise,architecture,scenes)['checks']['public_betrayal_opening'] is True


def test_competence_cascade_recap_cannot_mask_earlier_premature_hook():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes=[
      {'id':'S01','scene_goal':'Before the current case is closed, command gives her a fresh case.'},
      {'id':'S02','scene_goal':'She exposes the conspiracy.'},
      {'id':'S03','scene_goal':'Police close the conspiracy. Only then command briefs the fresh case that had already been assigned.'},
    ]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is False


def test_competence_cascade_finale_only_fresh_assignment_counts_as_hook():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes=[{'id':'finale','scene_goal':'In the finale, command gives her a fresh case before the epilogue.'}]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is False


def test_taboo_family_irony_protagonist_identity_field_enables_named_departure():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Bestie Parent','protagonist':{'identity':'Lily'},'logline':"She secretly marries a mafia boss, unaware he is her bestie's dad."}
    architecture={'sequences':[{'summary':'After the reveal, Lily chooses to leave him.'}]}
    assert evaluate_taboo_family_irony_integrity(premise,architecture,[])['checks']['protagonist_can_reject_power'] is True


def test_taboo_family_irony_supporting_departure_does_not_veto_named_protagonist():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Bestie Parent','protagonist':{'identity':'Lily'},'logline':"She secretly marries a mafia boss, unaware he is her bestie's dad."}
    architecture={'sequences':[{'summary':'The best friend chooses to leave her own husband.'},{'summary':'Lily chooses to leave him.'}]}
    assert evaluate_taboo_family_irony_integrity(premise,architecture,[])['checks']['protagonist_can_reject_power'] is True


def _restitution_pact_fixture():
    premise={
      'title':'The Memory Lantern',
      'logline':'A woman sacrifices her memory-sight in a magical pact to save five sworn wards; if they betray her, the pact restores her perception and curses them.',
    }
    architecture={'sequences':[
      {'summary':'She trades her eyes and memory-sight as the price of a pact to save them. They vow to protect her forever and never let anyone hurt her; if they betray her, the pact returns her sight and the curse rebounds.'},
      {'summary':'After they betray her, she can see again but hides her sight and pretends to still be blind so they cannot find out the pact has judged them.'},
      {'summary':'They once owed her because she saved them, but now call her a blood bag and dead weight. They drain her blood because it is useful, then try to cut out her heart because it will grow back.'},
      {'summary':'In a public test before the crowd, the hunters force them to pick one between the false saintess and the protagonist; they choose the false victim. Their curse becomes visible as they become true monsters.'},
      {'summary':'They apologize only to break the curse, but she says she gave them chances and does not forgive them.'},
      {'summary':'A quiet protector heals and protects her before she learns he is the hidden king. He lets her end the engagement and choose freely before the identity reveal.'},
      {'summary':'The ending is a mutual vow, chosen family, and home; she is never forced to forgive them.'},
    ]}
    scenes=[]
    return premise,architecture,scenes


def test_restitution_pact_integrity_balanced_example_passes_core_checks():
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise,architecture,scenes=_restitution_pact_fixture()
    r=evaluate_restitution_pact_integrity(premise,architecture,scenes)
    assert r['applies'] is True
    assert r['checks']['explicit_bodily_sacrifice_cost'] is True
    assert r['checks']['conditional_accountability_mechanism'] is True
    assert r['checks']['beneficiaries_vow_protection_before_betrayal'] is True
    assert r['checks']['restored_perception_creates_hidden_irony'] is True
    assert r['checks']['bodily_extraction_escalates_through_entitlement'] is True
    assert r['checks']['public_forced_choice_reveals_real_hierarchy'] is True
    assert r['checks']['instrumental_repentance_is_not_rewarded'] is True
    assert r['checks']['alternative_partner_proves_care_before_status'] is True
    assert r['checks']['consent_or_exit_choice_precedes_identity_reward'] is True


def test_restitution_pact_integrity_flags_decorative_curse_and_forced_forgiveness():
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise,architecture,scenes=_restitution_pact_fixture()
    architecture['sequences']=[
      {'summary':'She sacrifices her eyes in a curse-flavored bargain to save them.'},
      {'summary':'A powerful king immediately loves her status and reveals his identity before she can choose.'},
      {'summary':'The betrayers apologize only to break the curse, and she must forgive them because the magic requires it.'},
    ]
    r=evaluate_restitution_pact_integrity(premise,architecture,scenes)
    assert r['checks']['conditional_accountability_mechanism'] is False
    assert r['checks']['beneficiaries_vow_protection_before_betrayal'] is False
    assert r['checks']['restored_perception_creates_hidden_irony'] is False
    assert r['checks']['alternative_partner_proves_care_before_status'] is False
    assert r['checks']['consent_or_exit_choice_precedes_identity_reward'] is False
    assert r['checks']['closure_is_mutual_not_forced_forgiveness'] is False


def test_taboo_family_irony_blank_identity_does_not_crash():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Bestie Parent','protagonist':{'identity':''},'logline':"She secretly marries a mafia boss, unaware he is her bestie's dad."}
    r=evaluate_taboo_family_irony_integrity(premise,{},[])
    assert r['applies'] is True


def test_taboo_family_irony_ana_not_credited_for_diana_departure():
    from studio.taboo_family_irony_integrity import evaluate_taboo_family_irony_integrity
    premise={'title':'Bestie Parent','protagonist':{'identity':'Ana'},'logline':"She secretly marries a mafia boss, unaware he is her bestie's dad."}
    architecture={'sequences':[{'summary':'The rival Diana chooses to leave him. Ana remains trapped.'}]}
    assert evaluate_taboo_family_irony_integrity(premise,architecture,[])['checks']['protagonist_can_reject_power'] is False


def test_restitution_pact_does_not_apply_to_non_supernatural_survival_contract():
    import json
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise=json.load(open('examples/generated_survival_concepts/brakelight_moth_depths_premise.json',encoding='utf8'))
    assert evaluate_restitution_pact_integrity(premise,{},[])['applies'] is False


def test_chosen_bond_forced_marriage_to_named_alternative_is_coercive():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise,architecture,scenes=_chosen_bond_fixture()
    architecture['sequences']=[
      {'summary':'At the public bonding ceremony her fated mate cheats and humiliates her; her blood essence sustained his succession.'},
      {'summary':'She refuses him, but the clan forces her to marry the elf king. He says she need not answer and waits patiently before she believes him.'},
    ]
    assert evaluate_chosen_bond_integrity(premise,architecture,scenes)['checks']['alternative_bond_is_chosen_and_consenting'] is False


def test_competence_cascade_standalone_sequel_excerpt_can_follow_documented_closure():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes=[{'id':'sequel_excerpt','scene_goal':'In this sequel scene after the main case, command gives her a new mission.'}]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is True


def test_restitution_pact_conditional_terms_not_actual_betrayal_position():
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise,architecture,scenes=_restitution_pact_fixture()
    architecture['sequences']=[
      {'summary':'If they betray her, the pact returns her sight. They vow to protect her forever.'},
      {'summary':'Much later they actually betray her and abandon her during the attack.'},
      {'summary':'She hides her restored sight. The alternative protector heals her before she learns he is the hidden king; he lets her end the engagement before the identity reveal. They make a mutual vow at home.'},
    ]
    r=evaluate_restitution_pact_integrity(premise,architecture,scenes)
    assert r['checks']['beneficiaries_vow_protection_before_betrayal'] is True


def _maternal_sovereignty_fixture():
    premise={'title':'Lantern Ward of the Glass Court','protagonist':{'identity':'Mira'},'logline':'A pregnant secret contract wife is abandoned by her alpha husband for his first love while hiding that she is a lost royal healer.'}
    architecture={'sequences':[
      {'summary':'In the opening he abandons his pregnant bleeding wife to protect another woman; she begs him to save the baby. Mira accepted contract money to save her vulnerable friend from persecution, but the clause says she belongs to him whenever he wants and birth during the contract gives him full custody.'},
      {'summary':'She publicly rejects the unwanted marriage, lies that the baby died to hide the live pregnancy because he could steal the baby through custody law, and becomes chief healer through a resume without nepotism, a healing demonstration, scientific research, and a medical breakthrough independent of her princess identity.'},
      {'summary':'A medical board examination, security footage, reports, investors, election endorsements, and hospital evidence expose the false pregnancy publicly. When he says he never cheated, she answers that he never trusted her and never really wanted her. He signs the divorce papers and lets go before any reunion.'},
      {'summary':'His breakfasts are rejected; apology is insufficient. He gives up the election campaign and loses power to save her, waits patiently, and tells her she can refuse. Only after the truth is revealed does he ask her to marry him again, calling her healer princess and strongest woman; informed and uncoerced, she says yes.'},
    ]}
    return premise,architecture,[]


def test_maternal_sovereignty_integrity_positive():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    r=evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)
    assert r['applies'] is True
    assert r['score_0_to_1'] >= 0.9
    assert all(r['checks'].values())


def test_maternal_sovereignty_integrity_rejects_status_without_repair():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences']=[{'summary':'A pregnant secret contract wife is humiliated. She is a princess, so everyone kneels. The rival lied, so he apologizes and she immediately remarries him.'}]
    r=evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)
    assert r['checks']['professional_competence_is_independent_of_hidden_status'] is False
    assert r['checks']['male_repair_requires_material_cost_not_only_apology'] is False
    assert r['checks']['release_of_control_precedes_reunion'] is False


def test_maternal_sovereignty_does_not_apply_to_creature_survival():
    import json
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise=json.load(open('examples/generated_survival_concepts/foghorn_turtle_keeper_premise.json',encoding='utf8'))
    assert evaluate_maternal_sovereignty_integrity(premise,{},[])['applies'] is False


def test_chosen_bond_negated_force_and_former_partner_sentence_not_new_coercion():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise,architecture,scenes=_chosen_bond_fixture()
    architecture['sequences']=[
      {'summary':'At the public bonding ceremony her fated mate cheats and humiliates her; her blood essence sustained his succession.'},
      {'summary':'She refuses him. Her former mate once forced women into alliances. The elf king will not force her to marry; he asks consent and waits patiently before she freely chooses him.'},
    ]
    assert evaluate_chosen_bond_integrity(premise,architecture,scenes)['checks']['alternative_bond_is_chosen_and_consenting'] is True


def test_maternal_sovereignty_release_after_reunion_fails_order():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences'][2]={'summary':'A medical board examination and security footage expose the false pregnancy publicly. When he says he never cheated, she answers that he never trusted her.'}
    architecture['sequences'][-1]={'summary':'He apologizes, she says yes and they remarry; afterward he signs the divorce papers and releases control.'}
    assert evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)['checks']['release_of_control_precedes_reunion'] is False


def test_maternal_sovereignty_epilogue_truth_does_not_inform_rechoice():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences'][-1]={'summary':'He signs the divorce papers and lets go. She says yes and they remarry. In the epilogue the truth is revealed about why he abandoned her.'}
    assert evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)['checks']['re_choice_is_informed_and_not_coerced'] is False


def test_restitution_pact_time_clause_abandonment_is_actual_betrayal():
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise,architecture,scenes=_restitution_pact_fixture()
    architecture['sequences']=[
      {'summary':'They vow to protect her forever after the pact.'},
      {'summary':'When hunters attack, they abandon her and flee.'},
      {'summary':'She hides her restored sight. The alternative protector heals her before she learns he is the hidden king; he lets her end the engagement before the identity reveal. They make a mutual vow at home.'},
    ]
    assert evaluate_restitution_pact_integrity(premise,architecture,scenes)['checks']['beneficiaries_vow_protection_before_betrayal'] is True


def test_competence_cascade_later_next_episode_mention_does_not_excuse_premature_assignment():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes=[
      {'id':'S01','scene_goal':'Before the current case is closed, command assigns her a new case.'},
      {'id':'S02','scene_goal':'The next episode will continue the mission.'},
    ]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is False


def test_maternal_sovereignty_patient_apology_is_not_material_sacrifice():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences'][-1]={'summary':'He signs the divorce papers and lets go. He apologizes and waits patiently, but gives up nothing. The truth is revealed before she says yes and they remarry.'}
    assert evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)['checks']['male_repair_requires_material_cost_not_only_apology'] is False


def test_maternal_sovereignty_disclosure_is_not_costly_concealment():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences'][1]={'summary':'She reveals her pregnancy to protect the baby and becomes chief healer through professional medical competence.'}
    assert evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)['checks']['pregnancy_concealment_is_protective_and_costly'] is False


def test_restitution_pact_when_rule_without_betrayal_scene_fails_vow_order():
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise,architecture,scenes=_restitution_pact_fixture()
    architecture['sequences']=[
      {'summary':'They vow to protect her forever after the pact.'},
      {'summary':'The pact rule states that when they betray her, the pact will return her sight.'},
    ]
    assert evaluate_restitution_pact_integrity(premise,architecture,scenes)['checks']['beneficiaries_vow_protection_before_betrayal'] is False


def test_chosen_bond_prior_denial_does_not_erase_later_forced_marriage():
    from studio.chosen_bond_integrity import evaluate_chosen_bond_integrity
    premise,architecture,scenes=_chosen_bond_fixture()
    architecture['sequences']=[
      {'summary':'At the public bonding ceremony her fated mate cheats and humiliates her; her blood essence sustained his succession.'},
      {'summary':'She refuses him. The elf king will not force her to marry. Later the clan forces her to marry the elf king despite her refusal, though he asks consent and waits patiently.'},
    ]
    assert evaluate_chosen_bond_integrity(premise,architecture,scenes)['checks']['alternative_bond_is_chosen_and_consenting'] is False


def test_maternal_sovereignty_explicit_only_after_order_counts():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences'][-1]={'summary':'He gives up the election campaign and loses power. Their remarriage happens only after release of control and disclosure of the truth; informed and uncoerced, she says yes as healer princess.'}
    r=evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)
    assert r['checks']['release_of_control_precedes_reunion'] is True
    assert r['checks']['re_choice_is_informed_and_not_coerced'] is True


def test_competence_cascade_multiscene_explicit_sequel_excerpt_follows_closure():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes=[
      {'id':'epilogue1','scene_goal':'In this sequel scene after the main case, command gives her a new mission.'},
      {'id':'epilogue2','scene_goal':'The team reacts to the sequel mission.'},
    ]
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is True


def test_maternal_sovereignty_past_tense_hid_pregnancy_counts_with_cost():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences'][1]={'summary':'She hid the pregnancy to protect the baby, risking exile and custody loss, while becoming chief healer through professional medical competence.'}
    assert evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)['checks']['pregnancy_concealment_is_protective_and_costly'] is True


def test_maternal_sovereignty_plural_heirs_trigger_applicability():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise={'title':'Heirs of the Contract','logline':'In a contract marriage, her husband abandons her and their heirs for another woman.'}
    architecture={'sequences':[{'summary':'The secret wife is betrayed; custody of the heirs becomes leverage.'}]}
    assert evaluate_maternal_sovereignty_integrity(premise,architecture,[])['applies'] is True

def test_maternal_sovereignty_negated_release_does_not_count_as_ordering():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences'][2]={'summary':'A medical board examination, security footage, reports, investors, election endorsements, and hospital evidence expose the false pregnancy publicly. When he says he never cheated, she answers that he never trusted her and never really wanted her. He refuses to sign the divorce papers and never releases control.'}
    architecture['sequences'][3]={'summary':'His apology is insufficient. She remarries him after he refuses to release control and withholds disclosure, without informed consent.'}
    result=evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)
    assert result['checks']['release_of_control_precedes_reunion'] is False
    assert result['checks']['re_choice_is_informed_and_not_coerced'] is False


def test_competence_cascade_later_sequel_label_does_not_excuse_early_hook():
    from studio.competence_cascade_integrity import evaluate_competence_cascade_integrity
    premise,architecture,scenes=_competence_cascade_fixture()
    scenes[0]['scene_cards']=[{'title':'Early Hook','objective':'A new mission calls her back.'}]
    scenes.append({'summary':'Later Label. This scene is called a sequel scene after the new case has already begun.'})
    assert evaluate_competence_cascade_integrity(premise,architecture,scenes)['checks']['closure_before_mission_hook'] is False


def test_restitution_pact_narrative_when_clause_counts_as_actual_betrayal():
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise,architecture,scenes=_restitution_pact_fixture()
    architecture['sequences']=[
      {'summary':'They vow to protect her forever after the pact.'},
      {'summary':'When they betray her, the pact returns her sight.'},
    ]
    assert evaluate_restitution_pact_integrity(premise,architecture,scenes)['checks']['beneficiaries_vow_protection_before_betrayal'] is True

def test_maternal_sovereignty_unrelated_prior_refusal_does_not_hide_release():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences'][2]={'summary':'A medical board examination exposes the false pregnancy publicly. She refuses his first offer. He signs the divorce papers and lets go before any reunion.'}
    architecture['sequences'][3]={'summary':'She once says she does not trust him. Later the truth is revealed. He gives up the election campaign, waits patiently, and tells her she can refuse. Informed and uncoerced, she says yes when he asks her to marry him again, calling her healer princess.'}
    result=evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)
    assert result['checks']['release_of_control_precedes_reunion'] is True
    assert result['checks']['re_choice_is_informed_and_not_coerced'] is True


def test_maternal_sovereignty_notary_does_not_read_as_negation():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences'][3]={'summary':'He gives up the election campaign and tells her she can refuse. She remarries him only after a notary witnesses him sign the divorce papers and after the truth is revealed; informed and uncoerced, she says yes, remaining healer princess.'}
    result=evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)
    assert result['checks']['release_of_control_precedes_reunion'] is True


def test_restitution_pact_whenever_standing_rule_is_not_actual_betrayal():
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise,architecture,scenes=_restitution_pact_fixture()
    architecture['sequences']=[
      {'summary':'They vow to protect her forever after the pact.'},
      {'summary':'The pact restores sight whenever the beneficiaries betray her.'},
    ]
    assert evaluate_restitution_pact_integrity(premise,architecture,scenes)['checks']['beneficiaries_vow_protection_before_betrayal'] is False

def _protective_kinship_fixture():
    premise={
      'title':'The Viper Guardian',
      'logline':'Called a cruel viper after she struck back against abuse, Mira is sold in an arranged marriage to a widowed lord whose two daughters are neglected.',
    }
    architecture={'sequences':[
      {'summary':'The daughters have split shoes, bruises, thin blankets, empty wardrobes, and freezing rooms near the servants quarters. Mira tells them that if anyone hurts them they must tell me immediately and protects them from humiliating servants.'},
      {'summary':'Mira teaches the girls self-defense, tells them not to apologize when innocent, and shows them how to scream, run to help, and defend themselves. She orders hot water, blankets, food, and room assignments while taking the household keys.'},
      {'summary':'In the treasury she reads ledgers and accounts showing stolen inheritance. When the family says we are family and blood is blood, she answers that family protects children. The lord listens to the children, orders an audit, examines evidence, and divides the house as institutional consequence.'},
      {'summary':'He admits the truth: he used her because he needed her strength and chose her without telling her the truth. He transfers treasury keys, accounts, estates, revenues, money, control, and freedom to leave as material autonomy.'},
      {'summary':'He tells her she can refuse and waits for permission. Only then does she choose a real marriage and kiss him freely. Her healing gift belongs to herself; the court is told she is not property or an object.'},
      {'summary':'When her stepmother and father return in debt saying blood is blood and family has missed you, she decides they owe nothing and refuses to answer. Years later the wedding renewal, breakfast, ordinary home labor, and children leaving only when they choose prove durable chosen family care.'},
    ]}
    return premise,architecture,[]


def test_protective_kinship_integrity_balanced_example_passes_core_checks():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise,architecture,scenes=_protective_kinship_fixture()
    result=evaluate_protective_kinship_integrity(premise,architecture,scenes)
    assert result['applies'] is True
    assert result['score_0_to_1'] >= 0.9
    assert result['checks']['children_receive_agency_not_only_rescue'] is True
    assert result['checks']['material_autonomy_transfer_precedes_intimacy'] is True
    assert result['checks']['child_power_is_not_property'] is True


def test_protective_kinship_integrity_intimacy_before_autonomy_fails_order():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise,architecture,scenes=_protective_kinship_fixture()
    architecture['sequences'][3]={'summary':'He admits the truth: he used her because he needed her strength. She chooses a real marriage and kisses him.'}
    architecture['sequences'][4]={'summary':'Only afterward he transfers treasury keys, accounts, money, and freedom to leave. He tells her she can refuse. Her healing gift belongs to herself, not property.'}
    result=evaluate_protective_kinship_integrity(premise,architecture,scenes)
    assert result['checks']['material_autonomy_transfer_precedes_intimacy'] is False


def test_protective_kinship_integrity_does_not_apply_to_generic_creature_survival():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise={'title':'Turtle of the Salt City','logline':'A turtle child survives eviction and protects a storm-fragile community.'}
    architecture={'sequences':[{'summary':'A community contract protects water and shelter.'}]}
    assert evaluate_protective_kinship_integrity(premise,architecture,[])['applies'] is False

def test_protective_kinship_does_not_apply_to_emberseed_creature_example():
    import json
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise=json.load(open('examples/generated_creature_concepts/emberseed_oven_cart_premise.json',encoding='utf8'))
    architecture=json.load(open('examples/generated_creature_concepts/emberseed_oven_cart_architecture.json',encoding='utf8'))
    assert evaluate_protective_kinship_integrity(premise,architecture,[])['applies'] is False


def test_protective_kinship_screenplay_order_is_not_reversed_by_outline():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise,architecture,scenes=_protective_kinship_fixture()
    architecture['sequences'][3]={'summary':'She chooses a real marriage and kisses him.'}
    architecture['sequences'][4]={'summary':'Her healing gift belongs to herself, not property.'}
    scenes=[{'summary':'He transfers treasury keys, money, control, and freedom to leave. Later she chooses a real marriage and kisses him.'}]
    assert evaluate_protective_kinship_integrity(premise,architecture,scenes)['checks']['material_autonomy_transfer_precedes_intimacy'] is True


def test_protective_kinship_denied_freedom_does_not_count_as_consent():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise,architecture,scenes=_protective_kinship_fixture()
    architecture['sequences'][3]={'summary':'He admits the truth: he used her because he needed her strength. He transfers treasury keys, accounts, estates, revenues, money, and control.'}
    architecture['sequences'][4]={'summary':'He tells her she is not free to leave and she cannot refuse. She chooses a real marriage and kisses him. Her healing gift belongs to herself, not property.'}
    result=evaluate_protective_kinship_integrity(premise,architecture,scenes)
    assert result['checks']['consent_preserving_re_choice'] is False


def test_protective_kinship_instrumental_setup_is_not_confession():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise,architecture,scenes=_protective_kinship_fixture()
    architecture['sequences'][3]={'summary':'The premise calls this an instrumental marriage. He transfers treasury keys, accounts, money, and freedom to leave.'}
    architecture['sequences'][4]={'summary':'He tells her she can refuse. She chooses a real marriage and kisses him. Her healing gift belongs to herself, not property.'}
    assert evaluate_protective_kinship_integrity(premise,architecture,scenes)['checks']['truth_disclosure_precedes_re_choice'] is False


def test_maternal_sovereignty_never_even_signing_does_not_count_as_release():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences'][2]={'summary':'A medical board examination exposes the false pregnancy publicly. He never even signs the divorce papers.'}
    architecture['sequences'][3]={'summary':'The truth is never publicly revealed. He gives up the election campaign, waits patiently, and she says yes when he asks her to marry him again, calling her healer princess.'}
    result=evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)
    assert result['checks']['release_of_control_precedes_reunion'] is False
    assert result['checks']['re_choice_is_informed_and_not_coerced'] is False


def test_protective_kinship_parental_love_is_not_romantic_intimacy():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise,architecture,scenes=_protective_kinship_fixture()
    architecture['sequences'][0]={'summary':'She loves her daughters. The daughters have split shoes, bruises, thin blankets, empty wardrobes, and freezing rooms. Mira tells them that if anyone hurts them they must tell me immediately and protects them.'}
    assert evaluate_protective_kinship_integrity(premise,architecture,scenes)['checks']['material_autonomy_transfer_precedes_intimacy'] is True


def test_protective_kinship_unchallenged_child_property_fails():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise,architecture,scenes=_protective_kinship_fixture()
    architecture['sequences'][4]={'summary':'The court seizes her magical gift and treats children as property. He tells her she can refuse. She chooses a real marriage and kisses him.'}
    assert evaluate_protective_kinship_integrity(premise,architecture,scenes)['checks']['child_power_is_not_property'] is False


def test_restitution_pact_whenever_does_not_cross_newline_into_actual_betrayal():
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise,architecture,scenes=_restitution_pact_fixture()
    architecture['sequences']=[
      {'summary':'They vow to protect her forever after the pact. The pact restores sight whenever'},
      {'summary':'they betray her in the hunter attack.'},
    ]
    assert evaluate_restitution_pact_integrity(premise,architecture,scenes)['checks']['beneficiaries_vow_protection_before_betrayal'] is True

def test_maternal_sovereignty_not_hesitate_to_sign_counts_as_release():
    from studio.maternal_sovereignty_integrity import evaluate_maternal_sovereignty_integrity
    premise,architecture,scenes=_maternal_sovereignty_fixture()
    architecture['sequences'][2]={'summary':'A medical board examination exposes the false pregnancy publicly. He does not hesitate to sign the divorce papers and lets go before any reunion.'}
    assert evaluate_maternal_sovereignty_integrity(premise,architecture,scenes)['checks']['release_of_control_precedes_reunion'] is True


def test_protective_kinship_named_truth_and_permission_free_exit_count():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise,architecture,scenes=_protective_kinship_fixture()
    architecture['sequences'][3]={'summary':'He tells Mira the truth about using her. He transfers treasury keys, accounts, money, and control.'}
    architecture['sequences'][4]={'summary':'He says you can leave without my permission. She chooses a real marriage and kisses him. Her healing gift belongs to herself, not property.'}
    result=evaluate_protective_kinship_integrity(premise,architecture,scenes)
    assert result['checks']['truth_disclosure_precedes_re_choice'] is True
    assert result['checks']['consent_preserving_re_choice'] is True


def test_restitution_pact_newline_wrapped_if_rule_is_not_actual_betrayal():
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise,architecture,scenes=_restitution_pact_fixture()
    architecture['sequences']=[
      {'summary':'They vow to protect her forever after the pact. If'},
      {'summary':'they betray her, the pact restores her sight.'},
    ]
    assert evaluate_restitution_pact_integrity(premise,architecture,scenes)['checks']['beneficiaries_vow_protection_before_betrayal'] is False


def test_protective_kinship_condemns_child_property_counts_as_rejection():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise,architecture,scenes=_protective_kinship_fixture()
    architecture['sequences'][4]={'summary':'The prince claims her magical gift, but Mira condemns treating children as property. He tells her she can refuse. She chooses a real marriage and kisses him.'}
    assert evaluate_protective_kinship_integrity(premise,architecture,scenes)['checks']['child_power_is_not_property'] is True

def _constructive_restoration_fixture():
    premise={
      'title':'The Circuit Shepherd',
      'logline':'An orphaned mechanic is taken in without payment, learns repair from a mentor, and restores machines in a wrecked science-fiction frontier.',
    }
    architecture={'sequences':[
      {'summary':'The orphaned girl is homeless until a workshop keeper offers food, shelter, and care without asking payment.'},
      {'summary':'She repairs a small lamp circuit and radio first, then fixes a robot servo and a damaged vehicle while the mentor supervises her hands-on work.'},
      {'summary':'She is paid fair wages, earns independent workshop commissions, and the crew needs her as trusted mechanic because only she can keep the transport running. Money buys tools, parts, supplies, and repair capacity.'},
      {'summary':'After invasion and corporate extraction, the victors owe restitution and must help rebuild what the war damaged. A combat unit war machine is converted into shelter power, workshop labor, and care infrastructure.'},
      {'summary':'An ancient advanced station becomes usable infrastructure: power, water, transport, repair bay, home, and a ship network. She teaches a childlike robot apprentice, completing the mentorship cycle.'},
      {'summary':'In the finale the crew runs diagnostics, a trial run, systems checks, and a maiden flight launch proving the tested systems before a new journey.'},
    ]}
    return premise,architecture,[]


def test_constructive_restoration_fixture_passes_core_checks():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    premise,architecture,scenes=_constructive_restoration_fixture()
    result=evaluate_constructive_restoration_integrity(premise,architecture,scenes)
    assert result['applies'] is True
    assert result['checks']['repair_object_competence_ladder'] is True
    assert result['checks']['weapon_is_repurposed_into_care_or_work_infrastructure'] is True
    assert result['checks']['finale_demonstrates_capability_through_tested_systems'] is True


def test_constructive_restoration_spectacle_without_restoration_warns():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    premise={'title':'The Miracle Ship','logline':'A drifter mechanic witnesses an alien machine.'}
    architecture={'sequences':[
      {'summary':'A homeless orphan is given food and shelter.'},
      {'summary':'A miraculous alien ship appears and the mentor instantly fixes every machine while armies fight a war for treasure.'},
    ]}
    scenes=[]
    result=evaluate_constructive_restoration_integrity(premise,architecture,scenes)
    assert result['checks']['repair_object_competence_ladder'] is False
    assert result['checks']['war_conflict_carries_restitution_ethic'] is False
    assert result['checks']['weapon_is_repurposed_into_care_or_work_infrastructure'] is False


def test_constructive_restoration_does_not_apply_to_romance_without_repair():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    result=evaluate_constructive_restoration_integrity({'title':'Contract Bride','logline':'A duchess enters a marriage bargain.'},{'sequences':[{'summary':'Ballrooms and inheritance conflict.'}]},[])
    assert result['applies'] is False

def test_maternal_modal_not_hesitation_is_not_completed_release():
    from studio.maternal_sovereignty_integrity import _first_non_negated
    pattern=r'signs? (?:the )?divorce papers'
    assert _first_non_negated(pattern,'he would not hesitate to sign the divorce papers, but leaves them unsigned') is None
    assert _first_non_negated(pattern,'he does not hesitate to sign the divorce papers') is not None


def test_protective_truth_refusal_and_conditional_exit_do_not_count():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity
    premise,architecture,scenes=_protective_kinship_fixture()
    architecture['sequences'][3]={'summary':'He refuses to tell Mira the truth. He transfers treasury keys, accounts, money, and control.'}
    architecture['sequences'][4]={'summary':'He says she can leave only after marrying him. She chooses a real marriage and kisses him. Her healing gift belongs to herself.'}
    result=evaluate_protective_kinship_integrity(premise,architecture,scenes)
    assert result['checks']['truth_disclosure_precedes_re_choice'] is False
    assert result['checks']['consent_preserving_re_choice'] is False


def test_protective_with_permission_and_negated_child_condemnation():
    from studio.protective_kinship_integrity import evaluate_protective_kinship_integrity,_first_non_negated
    assert _first_non_negated(r'with (?:her|his|their) permission','he kisses her with her permission') is not None
    premise,architecture,scenes=_protective_kinship_fixture()
    architecture['sequences'][4]={'summary':'The prince claims her magical gift and never condemns treating children as property. He tells her she can refuse. She chooses a real marriage and kisses him.'}
    assert evaluate_protective_kinship_integrity(premise,architecture,scenes)['checks']['child_power_is_not_property'] is False


def test_restitution_prior_not_if_does_not_hide_actual_betrayal():
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise,architecture,scenes=_restitution_pact_fixture()
    architecture['sequences']=[
      {'summary':'They vow to protect her forever. She asks whether they will abandon her, and he says not if'},
      {'summary':'they betray her, the pact restores her sight.'},
    ]
    assert evaluate_restitution_pact_integrity(premise,architecture,scenes)['checks']['beneficiaries_vow_protection_before_betrayal'] is True

def test_constructive_restoration_scifi_applicability_ignores_relationship_ship():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    premise={'title':'Stormglass Keepers','logline':'Mira is publicly restored to honor and a relationship deepens.'}
    architecture={'sequences':[{'summary':'A village dispute and inheritance conflict unfold.'}]}
    assert evaluate_constructive_restoration_integrity(premise,architecture,[])['applies'] is False


def test_constructive_restoration_ladder_uses_story_not_logline_and_finale_tail():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    premise={'title':'Ship Repair','logline':'A mechanic restores a starship.'}
    architecture={'sequences':[
      {'summary':'An orphan is given food and shelter. She repairs a small lamp circuit.'},
      {'summary':'She repairs a robot, then a vehicle, then the ship infrastructure.'},
      {'summary':'The crew pays wages for tools and parts; a war machine is converted into shelter power. She teaches a childlike robot apprentice.'},
      {'summary':'At the end diagnostics, systems checks, and a maiden flight launch prove the ship.'},
    ]}
    result=evaluate_constructive_restoration_integrity(premise,architecture,[])
    assert result['checks']['repair_object_competence_ladder'] is True
    assert result['checks']['finale_demonstrates_capability_through_tested_systems'] is True


def test_constructive_restoration_opening_diagnostic_and_mentor_repair_do_not_pass():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    premise={'title':'Reactor Shop','logline':'A mechanic apprentice watches machines.'}
    architecture={'sequences':[
      {'summary':'Diagnostics open the story. The homeless apprentice is given food.'},
      {'summary':'The apprentice watches the mentor repair a reactor machine and the mentor does every repair.'},
      {'summary':'The ship leaves without tests.'},
    ]}
    result=evaluate_constructive_restoration_integrity(premise,architecture,[])
    assert result['checks']['learner_performs_repair_under_mentorship'] is False
    assert result['checks']['finale_demonstrates_capability_through_tested_systems'] is False


def test_constructive_restoration_requires_related_weapon_and_money_use():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    premise={'title':'Generator Shop','logline':'A mechanic repairs machines.'}
    architecture={'sequences':[
      {'summary':'An orphan is given food and shelter. She repairs a lamp, a robot, and a ship.'},
      {'summary':'A civilian generator is repaired. Elsewhere a weapon stays armed. Wages fund a holiday far away.'},
    ]}
    result=evaluate_constructive_restoration_integrity(premise,architecture,[])
    assert result['checks']['weapon_is_repurposed_into_care_or_work_infrastructure'] is False
    assert result['checks']['wealth_is_converted_into_repair_capacity'] is False


def test_maternal_unrelated_modal_does_not_negate_without_hesitation_signing():
    from studio.maternal_sovereignty_integrity import _first_non_negated
    pattern=r'signs? (?:the )?divorce papers'
    assert _first_non_negated(pattern,'he could wait but without hesitation signs the divorce papers') is not None


def test_protective_only_after_disclosure_and_desired_exit_count_as_choice():
    from studio.protective_kinship_integrity import _first_non_negated
    assert _first_non_negated(r'kiss','he kisses her only after disclosure') is not None
    assert _first_non_negated(r'free to leave','she is free to leave only if she wants') is not None


def test_restitution_vote_no_if_line_wrap_counts_as_conditional_rule():
    from studio.restitution_pact_integrity import evaluate_restitution_pact_integrity
    premise,architecture,scenes=_restitution_pact_fixture()
    architecture['sequences']=[
      {'summary':'They vow to protect her forever. The wards vote no if'},
      {'summary':'they betray her, the pact restores her sight.'},
    ]
    assert evaluate_restitution_pact_integrity(premise,architecture,scenes)['checks']['beneficiaries_vow_protection_before_betrayal'] is False

def test_constructive_restoration_applies_to_abandoned_robot_repair():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    result=evaluate_constructive_restoration_integrity(
      {'title':'Robot Repair','logline':'A homeless mechanic finds work.'},
      {'sequences':[{'summary':'She repairs an abandoned robot.'}]},[])
    assert result['applies'] is True


def test_constructive_restoration_qualified_plural_ladder_and_ending_payoff():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    premise={'title':'Station Repair','logline':'A mechanic apprentice repairs machines.'}
    architecture={
      'sequences':[
        {'summary':'The apprentice carefully repairs a lamp under supervision.'},
        {'summary':'She fixes a lamp, repairs several robots, then restores the station.'},
      ],
      'ending_payoff':{'summary':'A final trial run and systems check prove the station.'},
    }
    result=evaluate_constructive_restoration_integrity(premise,architecture,[])
    assert result['checks']['repair_object_competence_ladder'] is True
    assert result['checks']['learner_performs_repair_under_mentorship'] is True
    assert result['checks']['finale_demonstrates_capability_through_tested_systems'] is True


def test_constructive_restoration_reference_next_sentence_counts_resource_reuse():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    premise={'title':'Parts Fund','logline':'A mechanic repairs robots.'}
    architecture={'sequences':[{'summary':'She receives the payment. She spends it on parts and tools. They capture the war machine. It is converted into a clinic.'}]}
    result=evaluate_constructive_restoration_integrity(premise,architecture,[])
    assert result['checks']['wealth_is_converted_into_repair_capacity'] is True
    assert result['checks']['weapon_is_repurposed_into_care_or_work_infrastructure'] is True


def test_protective_debt_dependent_exit_is_not_consent():
    from studio.protective_kinship_integrity import _first_non_negated
    assert _first_non_negated(r'free to leave','she is free to leave only if she pays off his debt') is None


def test_maternal_absolute_modal_hypothetical_is_not_completed_release():
    from studio.maternal_sovereignty_integrity import _first_non_negated
    pattern=r'signs? (?:the )?divorce papers'
    assert _first_non_negated(pattern,'he would absolutely not hesitate to sign the divorce papers, but leaves them unsigned') is None

def test_constructive_restoration_negated_learner_and_testimony_do_not_count():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    premise={'title':'Machine Shop','logline':'A mechanic repairs machines.'}
    architecture={'sequences':[{'summary':'The apprentice never repairs the robot. The mentor does every repair.'}], 'ending_payoff':{'summary':'Court testimony closes the case.'}}
    result=evaluate_constructive_restoration_integrity(premise,architecture,[])
    assert result['checks']['learner_performs_repair_under_mentorship'] is False
    assert result['checks']['finale_demonstrates_capability_through_tested_systems'] is False


def test_constructive_restoration_early_robot_mention_does_not_hide_later_ladder():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    premise={'title':'Station Shop','logline':'A mechanic repairs machines.'}
    architecture={'sequences':[{'summary':'Robots are forbidden in the city. She repairs a lamp.'},{'summary':'She repairs several robots, then restores the station.'}]}
    assert evaluate_constructive_restoration_integrity(premise,architecture,[])['checks']['repair_object_competence_ladder'] is True


def test_constructive_restoration_cross_sentence_ship_does_not_create_applicability():
    from studio.constructive_restoration_integrity import evaluate_constructive_restoration_integrity
    premise={'title':'Clock Shop','logline':'A repairer works in town.'}
    architecture={'sequences':[{'summary':'She repairs a clock. A ship arrives in the harbor.'}]}
    assert evaluate_constructive_restoration_integrity(premise,architecture,[])['applies'] is False


def test_protective_learning_truth_is_not_payment_condition():
    from studio.protective_kinship_integrity import _first_non_negated
    assert _first_non_negated(r'kiss','he kisses her only after she learns the truth') is not None


def test_maternal_prior_alternative_does_not_make_signing_hypothetical():
    from studio.maternal_sovereignty_integrity import _first_non_negated
    pattern=r'signs? (?:the )?divorce papers'
    assert _first_non_negated(pattern,'he could refuse, but he does not hesitate to sign the divorce papers') is not None

def test_dual_incognito_workplace_integrity_positive_cineai_like():
    from studio.dual_incognito_workplace_integrity import evaluate_dual_incognito_workplace_integrity
    premise={'logline':'A secret hotel owner takes an ordinary staff position and meets a framed CEO who lost everything and now works there.'}
    architecture={'sequences':[
        {'summary':'The hidden owner becomes an ordinary worker. The stripped executive applies for a job and does it properly. She defends him: do not humiliate workers.'},
        {'summary':'A birthday cake and treatment for his bleeding hand build community care. Payroll, overtime sheets, maintenance logs, security footage, bank confirmation, vendor registration, and access code records expose the plot.'},
        {'summary':'He says she made that decision for both of them. She admits she was wrong to hide the truth and gives him time without demanding forgiveness.'},
        {'summary':'He refuses a senior role, seeks investment on the same terms through an independent committee, builds transparent payroll and scheduling tools with employee access, and they agree to no more secrets.'}
    ]}
    result=evaluate_dual_incognito_workplace_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['score_0_to_1'] >= 0.9


def test_dual_incognito_workplace_integrity_flags_missing_consent_and_independence():
    from studio.dual_incognito_workplace_integrity import evaluate_dual_incognito_workplace_integrity
    premise={'logline':'A secret billionaire owner takes a hotel job.'}
    architecture={'sequences':[{'summary':'She kisses a worker, uses one document to fire a manager, gives him a senior job because they are dating, and they instantly marry.'}]}
    result=evaluate_dual_incognito_workplace_integrity(premise,architecture,[])
    assert result['checks']['concealment_creates_named_consent_debt'] is False
    assert result['checks']['career_restoration_is_not_romantic_patronage'] is False
    assert result['warnings']

def test_social_test_generated_dialogue_is_scene_specific_and_warn_free():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    from studio.dialogue_craft import evaluate_scenes_dialogue
    premise=generate_premises('social_test_melodrama',1,42)[0]
    scenes=generate_scenes(premise,generate_architecture(premise))
    assert len(scenes)==8
    assert all(len(scene['dialogue_design']['spoken_exchange'])==4 for scene in scenes)
    assert 'Your floor is below. Guests eat above.' in scenes[0]['dialogue_design']['key_lines']
    assert scenes[0]['dialogue_design']['spoken_exchange'][1]['speaker'] != scenes[0]['dialogue_design']['spoken_exchange'][2]['speaker']
    assert evaluate_scenes_dialogue(scenes)['warnings_by_scene']=={}


def test_social_test_dialogue_uses_material_proof_and_restitution_turns():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    premise=generate_premises('social_test_melodrama',1,42)[0]
    scenes=generate_scenes(premise,generate_architecture(premise))
    s5=scenes[4]['dialogue_design']['spoken_exchange']
    s7=scenes[6]['dialogue_design']['spoken_exchange']
    assert any('doesn\'t fit her hands or her hours' in turn['line'] for turn in s5)
    assert any('Return the name you erased first' in turn['line'] for turn in s7)
    assert all(turn.get('subtext') and turn.get('voice_signature') for scene in scenes for turn in scene['dialogue_design']['spoken_exchange'])

def test_dual_incognito_does_not_apply_to_restored_laborer_fantasy():
    from studio.dual_incognito_workplace_integrity import evaluate_dual_incognito_workplace_integrity
    premise={'logline':'A restored dragon laborer rescues a hidden heir in a magical forest.'}
    architecture={'sequences':[{'summary':'The laborer restored the dragon and protected the child.'}]}
    assert evaluate_dual_incognito_workplace_integrity(premise,architecture,[])['applies'] is False


def test_dual_incognito_one_payroll_file_is_not_multi_source_evidence():
    from studio.dual_incognito_workplace_integrity import evaluate_dual_incognito_workplace_integrity
    premise={'logline':'A secret hotel owner takes an ordinary staff position.'}
    architecture={'sequences':[{'summary':'A payroll document, later called a payroll record, is the only proof.'}]}
    result=evaluate_dual_incognito_workplace_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['checks']['evidence_is_procedural_and_multi_source'] is False

def test_social_dialogue_uses_variant_proof_chain_and_no_early_accusation():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    premise=generate_premises('social_test_melodrama',1,42)[0]
    assert 'wing-fracture signature' in premise['proof_chain']
    scenes=generate_scenes(premise,generate_architecture(premise))
    scene4=' '.join(t['line'] for t in scenes[3]['dialogue_design']['spoken_exchange']).lower()
    assert 'invent a thief' not in scene4 and 'convenient' not in scene4
    all_dialogue=' '.join(t['line'] for s in scenes for t in s['dialogue_design']['spoken_exchange'])
    assert 'wing-fracture signature' in all_dialogue


def test_mute_child_communicates_by_signal_not_spoken_testimony():
    from studio.premise_generator import generate_premises
    from studio.architecture_generator import generate_architecture
    from studio.scene_generator import generate_scenes
    premise=generate_premises('social_test_melodrama',3,42)[1]
    scenes=generate_scenes(premise,generate_architecture(premise))
    child_lines=[t['line'] for s in scenes for t in s['dialogue_design']['spoken_exchange'] if 'nephew' in t['speaker']]
    assert child_lines and all(line.startswith('[') for line in child_lines)


def test_dual_incognito_plural_employee_shift_cues_apply():
    from studio.dual_incognito_workplace_integrity import evaluate_dual_incognito_workplace_integrity
    premise={'logline':'A fired ceo joins employees on a night shift.'}
    assert evaluate_dual_incognito_workplace_integrity(premise,{},[])['applies'] is True

def test_adversarial_coparent_integrity_positive_and_non_applicable():
    from studio.adversarial_coparent_integrity import evaluate_adversarial_coparent_integrity
    premise={'logline':'An FBI single mom falls for a security guard, unaware he is a mafia don; her daughter and his son arrange the blind date.'}
    architecture={'sequences':[{'summary':'The children only introduced them, but marriage is an adult decision made of free will. She helps him find a steady job, they share dinner, bedtime stories, rent and bills, and neither child is baggage. She is a debt collector; he is a security guard. He is hunting the FBI agent while she investigates the mafia family. At the identity reveal, she says deciding when to tell her was up to him; they promise no more secrets and full disclosure. They verify ledgers, personnel records, security footage, witness statements, financial records, communications, and a recorded confession. This time they figure it out together with backup and a tactical team. The children did nothing wrong; adults settle it themselves and grown-up problems are for grown-ups. In the ending he asks her to choose me again in a proper proposal with full identity, respect choices, always be honest, conflict of interest review, other agents, investigation, arrest, and records secured.'}]}
    result=evaluate_adversarial_coparent_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['score_0_to_1'] >= 0.9
    assert result['checks']['children_are_not_secret_keepers_or_family_glue'] is True
    ordinary=evaluate_adversarial_coparent_integrity({'logline':'A glasswing smith is framed by the guild.'},{},[])
    assert ordinary['applies'] is False


def test_adversarial_coparent_integrity_warns_when_children_force_consent():
    from studio.adversarial_coparent_integrity import evaluate_adversarial_coparent_integrity
    premise={'logline':'An FBI agent and mafia boss conceal their identities as a security guard and debt collector; unaware, they marry as husband and wife because their daughter and son demand it.'}
    architecture={'sequences':[{'summary':'The investigation and hunting escalate, but no one says the marriage was an adult decision or free choice.'}]}
    result=evaluate_adversarial_coparent_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['checks']['children_catalyze_but_do_not_own_adult_choice'] is False
    assert any('children or dependents' in w for w in result['warnings'])

def test_adversarial_coparent_requires_dual_incognito_not_borrowed_cover_job():
    from studio.adversarial_coparent_integrity import evaluate_adversarial_coparent_integrity
    premise={'logline':'An openly identified FBI agent and an openly identified mafia boss are husband and wife with a son; a supporting neighbor works as a security guard.'}
    result=evaluate_adversarial_coparent_integrity(premise,{},[])
    assert result['applies'] is False


def test_adversarial_coparent_applies_to_climate_extraction_translation():
    from studio.adversarial_coparent_integrity import evaluate_adversarial_coparent_integrity
    premise={'logline':'A climate inspector and an extraction heir conceal their identities, posing as a field aide and a bookkeeper while raising an apprentice together as husband and wife.'}
    architecture={'sequences':[{'summary':'They investigate and expose each other as enemies, then must decide what marriage means.'}]}
    result=evaluate_adversarial_coparent_integrity(premise,architecture,[])
    assert result['applies'] is True


def test_adversarial_coparent_detects_forced_child_secrecy():
    from studio.adversarial_coparent_integrity import evaluate_adversarial_coparent_integrity
    premise={'logline':'An FBI agent and mafia boss conceal their identities as a security guard and debt collector; unaware spouses marry and raise a daughter and son.'}
    architecture={'sequences':[{'summary':'The adults explicitly make the children cover their lies and carry adult secrets.'}]}
    result=evaluate_adversarial_coparent_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['checks']['children_are_not_secret_keepers_or_family_glue'] is False
    assert any('children carry adult secrets' in w for w in result['warnings'])


def test_adversarial_coparent_reads_scene_care_before_architecture_reveal_label():
    from studio.adversarial_coparent_integrity import evaluate_adversarial_coparent_integrity
    premise={'logline':'An FBI agent and mafia boss conceal their identities as a security guard and debt collector; unaware spouses marry and raise a daughter and son.'}
    architecture={'sequences':[{'summary':'Identity reveal happens in the final movement.'}]}
    scenes=[
        {'scene_id':'S01','summary':'She helps him find a steady job; they share dinner, bedtime stories, rent and bills.'},
        {'scene_id':'S08','summary':'Identity reveal forces both institutions into the open.'},
    ]
    result=evaluate_adversarial_coparent_integrity(premise,architecture,scenes)
    assert result['applies'] is True
    assert result['checks']['material_care_precedes_status_reward'] is True

def test_evidentiary_withdrawal_integrity_positive_and_non_applicable():
    from studio.evidentiary_withdrawal_integrity import evaluate_evidentiary_withdrawal_integrity
    premise={'logline':'Reborn after an edited recording destroyed her, a woman leaves a shared apartment rather than consenting to a roommate boyfriend moving in.'}
    architecture={'sequences':[{'summary':'This time around she will not meddle or argue; she will move out, but she does not consent. Income and job status do not matter; tenant consent and shared-space safety are the boundary. She preserves the lease, security footage, full recording, screenshots, witness testimony, timestamped photos, police and legal records. The antagonists escalate with fake photos, hidden cameras, debt, kidnapping and confession while coworkers, landlord and roommates form a witness network. They prepare a code to call the police and use raw footage as backup. She did not save anyone or forgive anyone. The ending has changed the locks, cameras installed, a safer home, and a long-term lease: a door I could close.'}]}
    result=evaluate_evidentiary_withdrawal_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['score_0_to_1'] >= 0.9
    ordinary=evaluate_evidentiary_withdrawal_integrity({'logline':'A dragon smith rebuilds a village.'},{},[])
    assert ordinary['applies'] is False


def test_evidentiary_withdrawal_warns_when_exit_implies_consent():
    from studio.evidentiary_withdrawal_integrity import evaluate_evidentiary_withdrawal_integrity
    premise={'logline':'Reborn after edited audio ruined her, a woman leaves a roommate lease.'}
    architecture={'sequences':[{'summary':'This time she will move out and never argue again.'}]}
    result=evaluate_evidentiary_withdrawal_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['checks']['withdrawal_does_not_mean_consent'] is False
    assert any('refuses consent' in w or 'never explicitly refuses consent' in w for w in result['warnings'])

def test_evidentiary_withdrawal_supports_shipboard_crew_quarters():
    from studio.evidentiary_withdrawal_integrity import evaluate_evidentiary_withdrawal_integrity
    premise={'logline':'Reborn after doctored proof cost her a disputed berth, a ship crew member leaves the crew quarters rather than consenting to the arrangement.'}
    result=evaluate_evidentiary_withdrawal_integrity(premise,{},[])
    assert result['applies'] is True


def test_evidentiary_withdrawal_does_not_count_one_screenshot_as_corroboration():
    from studio.evidentiary_withdrawal_integrity import evaluate_evidentiary_withdrawal_integrity
    premise={'logline':'Reborn after an edited clip ruined her, a woman leaves a roommate lease.'}
    architecture={'sequences':[{'summary':'She moves out but does not consent, citing tenant consent and safety. One timestamped camera screenshot clears her.'}]}
    result=evaluate_evidentiary_withdrawal_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['checks']['evidence_is_multi_source_and_material'] is False


def test_evidentiary_withdrawal_rejects_physical_fire_without_epistemic_wound():
    from studio.evidentiary_withdrawal_integrity import evaluate_evidentiary_withdrawal_integrity
    premise={'logline':'Reborn before a dormitory fire, she investigates the disaster.'}
    architecture={'sequences':[{'summary':'Later evidence shows faulty wiring caused the fire.'}]}
    result=evaluate_evidentiary_withdrawal_integrity(premise,architecture,[])
    assert result['applies'] is False

def test_evidentiary_withdrawal_review_regressions_forging_and_corroboration():
    from studio.evidentiary_withdrawal_integrity import evaluate_evidentiary_withdrawal_integrity
    base = "She does not consent and objects to the boundary violation. She moves out, with witness testimony, police legal support, a prepared backup plan, no reconciliation, and changed the locks for a safer home."
    forged = evaluate_evidentiary_withdrawal_integrity({'logline':'Reborn in her shared apartment after forged evidence destroyed her, she withdraws.'},{'sequences':[{'summary':base}]},[])
    assert forged['applies'] is True
    corroborated = evaluate_evidentiary_withdrawal_integrity({'logline':'Reborn in a shared apartment after forged evidence, she withdraws.'},{'sequences':[{'summary':'Lease, security footage, and chat screenshots corroborate her account. '+base}]},[])
    assert corroborated['checks']['evidence_is_multi_source_and_material'] is True
    unrelated_call = evaluate_evidentiary_withdrawal_integrity({'logline':'Reborn in a shared apartment after forged evidence, she withdraws.'},{'sequences':[{'summary':'A witness and a full recording clear her. She later has a video call about dinner. She does not consent, objects to the boundary violation, moves out, uses a prepared backup plan, refuses reconciliation, and changed the locks for a safer home.'}]},[])
    assert unrelated_call['checks']['evidence_is_multi_source_and_material'] is False


def test_evidentiary_withdrawal_ignores_sports_berth_but_accepts_ship_berth():
    from studio.evidentiary_withdrawal_integrity import evaluate_evidentiary_withdrawal_integrity
    sports = evaluate_evidentiary_withdrawal_integrity({'logline':'Reborn after an edited clip costs an athlete an Olympic berth, she clears her name.'},{},[])
    assert sports['applies'] is False
    ship = evaluate_evidentiary_withdrawal_integrity({'logline':'Reborn after forged evidence on a ship, she loses the disputed crew berth and withdraws.'},{'sequences':[{'summary':'The captain controls the cabin assignment.'}]},[])
    assert ship['applies'] is True
def test_labor_romance_power_balance_positive_and_non_applicable():
    from studio.labor_romance_power_balance_integrity import evaluate_labor_romance_power_balance_integrity
    premise={'logline':'A debt-burdened woman disguises herself as a male assistant for a billionaire heir because only male applicants are hired, then falls in love.'}
    architecture={'sequences':[{'summary':'She needs the job to pay the loan. The gauze, shared room, hospital privacy and uniform make concealment costly. He says he does not own you and she says you do not get to decide. A kiss without asking is named as a violation, followed by apology, permission and repair. Handmade gifts, cooked meals, schedule help and time together matter before money. A rich rival says quit and I will hire you, testing autonomy. She takes responsibility: she lied to get the job but earned her pay and was not after your money. At the end they end the contract with no penalty, create a separate repayment plan, she takes a part-time job, and romance continues outside employment.'}]}
    result=evaluate_labor_romance_power_balance_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['score_0_to_1'] >= 0.85
    ordinary=evaluate_labor_romance_power_balance_integrity({'logline':'A dragon smith rebuilds a village.'},{},[])
    assert ordinary['applies'] is False


def test_labor_romance_power_balance_warns_when_romance_stays_dependency():
    from studio.labor_romance_power_balance_integrity import evaluate_labor_romance_power_balance_integrity
    premise={'logline':'A poor maid in debt secretly falls in love with her billionaire boss.'}
    architecture={'sequences':[{'summary':'He controls her time and she remains his employee and debtor as they become a couple.'}]}
    result=evaluate_labor_romance_power_balance_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['checks']['ending_separates_romance_from_employment_debt'] is False
    assert any('dependency' in w for w in result['warnings'])

def test_labor_romance_review_regressions_consent_dependency_and_candidate():
    from studio.labor_romance_power_balance_integrity import evaluate_labor_romance_power_balance_integrity
    premise={'logline':'A poor maid in debt disguises herself to work for a billionaire boss and falls in love.'}
    coercive={'sequences':[{'summary':'He repeatedly kisses her without asking and nobody objects. He never apologizes or changes his behavior.'}]}
    result=evaluate_labor_romance_power_balance_integrity(premise,coercive,[])
    assert result['applies'] is True
    assert result['checks']['consent_pressure_is_named_not_romanticized'] is False

    dependent={'sequences':[{'summary':'In the ending he threatens her career unless she stays with him, so she remains his employee and girlfriend.'}]}
    dep=evaluate_labor_romance_power_balance_integrity(premise,dependent,[])
    assert dep['checks']['ending_separates_romance_from_employment_debt'] is False

    nonromance=evaluate_labor_romance_power_balance_integrity({'logline':'A disguised princess and her maid interview every candidate for a royal post while hiding from a powerful prince.'},{'sequences':[{'summary':'They complete the palace labor assignment.'}]},[])
    assert nonromance['applies'] is False

def test_labor_romance_consent_negation_and_unrelated_objection_regressions():
    from studio.labor_romance_power_balance_integrity import evaluate_labor_romance_power_balance_integrity
    premise={'logline':'A poor maid in debt disguises herself to work for a billionaire boss and falls in love.'}
    ignored={'sequences':[{'summary':'He kisses her without asking. She refuses, but he never respects her refusal and never apologizes.'}]}
    ignored_result=evaluate_labor_romance_power_balance_integrity(premise,ignored,[])
    assert ignored_result['checks']['consent_pressure_is_named_not_romanticized'] is False

    repaired={'sequences':[{'summary':'She accepts a schedule change without objection. Later he kisses her without asking. She refuses and says stop. He apologizes, asks for permission, and changes his behavior.'}]}
    repaired_result=evaluate_labor_romance_power_balance_integrity(premise,repaired,[])
    assert repaired_result['checks']['consent_pressure_is_named_not_romanticized'] is True

def test_cozy_disaster_shelter_validator_positive_and_generic_negative():
    from studio.cozy_disaster_shelter_integrity import evaluate_cozy_disaster_shelter_integrity
    premise={'logline':'In 1960, a Japanese farming family with a grandmother, young son, daughter, and Shiba dog prepares their riverside wooden home for a typhoon survival night.'}
    architecture={'sequences':[{'summary':'They farm, harvest, cook, clean, and prepare food before the flood. Inside warm lantern light contrasts with the storm outside the window. With little rice and limited drinking water remaining, they move upstairs, board the window, protect the wooden home, and sacrifice the wooden boat. The child helps feed the dog. After the floodwaters recede they rebuild the village at sunrise.'}]}
    result=evaluate_cozy_disaster_shelter_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['score_0_to_1'] >= 0.9

    generic={'logline':'A family survives a storm in a shelter.'}
    generic_result=evaluate_cozy_disaster_shelter_integrity(generic,{},[])
    assert generic_result['applies'] is True
    assert generic_result['score_0_to_1'] < 0.5
    assert generic_result['warnings']

def test_labor_romance_consent_repair_context_and_negation_regressions():
    from studio.labor_romance_power_balance_integrity import evaluate_labor_romance_power_balance_integrity
    premise={'logline':'A poor maid in debt disguises herself to work for a billionaire boss and falls in love.'}

    unrelated={'sequences':[{'summary':'He kisses her without asking and she refuses. He apologizes about the shift change but never mentions the kiss.'}]}
    unrelated_result=evaluate_labor_romance_power_balance_integrity(premise,unrelated,[])
    assert unrelated_result['checks']['consent_pressure_is_named_not_romanticized'] is False

    permission={'sequences':[{'summary':'He asks for permission, and she can say no. Their romance continues by choice.'}]}
    permission_result=evaluate_labor_romance_power_balance_integrity(premise,permission,[])
    assert permission_result['checks']['consent_pressure_is_named_not_romanticized'] is True

    objection={'sequences':[{'summary':'She objects when he kisses her without permission. He apologizes for the kiss and changes his behavior.'}]}
    objection_result=evaluate_labor_romance_power_balance_integrity(premise,objection,[])
    assert objection_result['checks']['consent_pressure_is_named_not_romanticized'] is True

def test_review_regressions_labor_consent_and_cozy_applicability():
    from studio.labor_romance_power_balance_integrity import evaluate_labor_romance_power_balance_integrity
    from studio.cozy_disaster_shelter_integrity import evaluate_cozy_disaster_shelter_integrity
    premise={'logline':'A poor maid in debt disguises herself to work for a billionaire boss and falls in love.'}

    for text in [
        'She no longer consents after he kisses her without asking.',
        'He kisses her without asking and she refuses. He didn’t take responsibility.',
        'He kisses her without asking. Nobody objected. He apologizes for the kiss.',
    ]:
        result=evaluate_labor_romance_power_balance_integrity(premise,{'sequences':[{'summary':text}]},[])
        assert result['checks']['consent_pressure_is_named_not_romanticized'] is False, text

    grabbed={'sequences':[{'summary':'He grabbed her without asking. She refused. He apologizes for grabbing her and changes his behavior.'}]}
    assert evaluate_labor_romance_power_balance_integrity(premise,grabbed,[])['checks']['consent_pressure_is_named_not_romanticized'] is True

    flooding={'logline':'A family sheltering upstairs survives flooding with food and water.'}
    assert evaluate_cozy_disaster_shelter_integrity(flooding,{},[])['applies'] is True

    financial={'logline':'A mother returns home after a financial disaster to rescue her marriage.'}
    assert evaluate_cozy_disaster_shelter_integrity(financial,{},[])['applies'] is False

    late_labor_premise={'logline':'A family survives a storm in their home with food.'}
    late_labor={'sequences':[{'summary':'The storm floods the house. Later they cook during recovery.'}]}
    assert evaluate_cozy_disaster_shelter_integrity(late_labor_premise,late_labor,[])['checks']['ordinary_labor_establishes_world_before_disaster'] is False

    survival_only={'sequences':[{'summary':'They board the windows and endure. The storm passes and the film cuts to black.'}]}
    assert evaluate_cozy_disaster_shelter_integrity(late_labor_premise,survival_only,[])['checks']['resolution_rebuilds_or_restores_connection'] is False

def test_cozy_shelter_ordered_opening_ending_and_rescue_regressions():
    from studio.cozy_disaster_shelter_integrity import evaluate_cozy_disaster_shelter_integrity
    premise={'logline':'A family survives a storm in their wooden home with food and water.'}

    sequences={'sequences':[
        {'summary':'The family tends grandmother and their dog in the village house.'},
        {'summary':'They farm, harvest, cook, and prepare the upper floor.'},
        {'summary':'The storm strikes, they protect the windows, rebuild the wall, and return home to a hopeful new beginning.'},
    ]}
    result=evaluate_cozy_disaster_shelter_integrity(premise,sequences,[])
    assert result['checks']['ordinary_labor_establishes_world_before_disaster'] is True

    midstorm_meal={'sequences':[
        {'summary':'They prepare food and board the windows before the storm.'},
        {'summary':'During the worst wind they share a meal under blankets.'},
        {'summary':'They endure until the storm passes and the film cuts to black.'},
    ]}
    meal_result=evaluate_cozy_disaster_shelter_integrity(premise,midstorm_meal,[])
    assert meal_result['checks']['resolution_rebuilds_or_restores_connection'] is False

    rescue_only={'logline':'A family trapped upstairs in a flood is rescued from their home.'}
    assert evaluate_cozy_disaster_shelter_integrity(rescue_only,{},[])['applies'] is True

def test_cozy_shelter_epilogue_meal_event_order_and_keepsake_regressions():
    from studio.cozy_disaster_shelter_integrity import evaluate_cozy_disaster_shelter_integrity
    premise={'logline':'A family survives a storm in their wooden home with food.'}

    quiet_epilogue={'sequences':[
        {'summary':'They farm, cook, and prepare before the storm.'},
        {'summary':'After the storm they rebuild the damaged wall together.'},
        {'summary':'At dawn they sit quietly and look at the fields.'},
    ]}
    assert evaluate_cozy_disaster_shelter_integrity(premise,quiet_epilogue,[])['checks']['resolution_rebuilds_or_restores_connection'] is True

    closing_meal={'sequences':[
        {'summary':'They farm, cook, and prepare before the storm.'},
        {'summary':'After the storm, the family shares a warm meal at sunrise.'},
    ]}
    assert evaluate_cozy_disaster_shelter_integrity(premise,closing_meal,[])['checks']['resolution_rebuilds_or_restores_connection'] is True

    intrusion_first={'sequences':[
        {'summary':'Water rushes indoors and the family retreats upstairs.'},
        {'summary':'They cook in the shelter while waiting.'},
    ]}
    assert evaluate_cozy_disaster_shelter_integrity(premise,intrusion_first,[])['checks']['ordinary_labor_establishes_world_before_disaster'] is False

    keepsake={'logline':'A daughter rescues letters from an empty storm-damaged home.'}
    assert evaluate_cozy_disaster_shelter_integrity(keepsake,{},[])['applies'] is False

def test_capability_inversion_care_validator_positive_and_nonapplicable():
    from studio.capability_inversion_care_integrity import evaluate_capability_inversion_care_integrity
    premise={'logline':'A freakishly strong farm woman mocked as a freak is hired as bodyguard for a wheelchair CEO and falls in love.'}
    architecture={'sequences':[
        {'summary':'She cannot control her strength, causes damage, loses jobs, and returns to her parents farm where honest labor and pigs give her dignity.'},
        {'summary':'The wealthy estate hires her to protect him. She refuses to treat him as only someone to be taken care of, gives him tools and practice choices, and learns city life while he learns farm labor and street food.'},
        {'summary':'He cooks, plans, works, and confesses. When the job is done she considers leaving, but he asks permission and respects her choice. She keeps earning her own money and chooses to be his girlfriend.'},
    ]}
    result=evaluate_capability_inversion_care_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['score_0_to_1'] >= 0.75

    plain={'logline':'A strong superhero saves a city.'}
    assert evaluate_capability_inversion_care_integrity(plain,{},[])['applies'] is False

def test_cozy_validator_irrigation_does_not_count_as_disaster_onset():
    from studio.cozy_disaster_shelter_integrity import evaluate_cozy_disaster_shelter_integrity
    premise={'logline':'A farming family shelters during a typhoon.'}
    architecture={'sequences':[
        {'summary':'Water rushes into the irrigation ditch before harvest while the family works the fields and gathers food.'},
        {'summary':'A typhoon floods the shelter and the family survives by rationing food and drinking water.'},
        {'summary':'After the storm they rebuild the house and share a warm meal.'},
    ]}
    result=evaluate_cozy_disaster_shelter_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['checks']['ordinary_labor_establishes_world_before_disaster'] is True

def test_capability_validator_uses_architecture_ending_payoff():
    from studio.capability_inversion_care_integrity import evaluate_capability_inversion_care_integrity
    premise={'logline':'A freakishly strong woman mocked as a freak is hired as bodyguard for a wheelchair CEO.'}
    architecture={
      'sequences':[{'summary':'She protects him and helps him practice agency.'}],
      'ending_payoff':'When the job is done, she chooses to become his girlfriend, keeps her own work, and he respects her choice.'
    }
    result=evaluate_capability_inversion_care_integrity(premise,architecture,[])
    assert result['checks']['intimacy_is_renegotiated_beyond_the_job'] is True
    assert result['checks']['ending_preserves_independent_livelihood_or_work_choice'] is True


def test_capability_validator_rejects_generic_strength_disaster_story():
    from studio.capability_inversion_care_integrity import evaluate_capability_inversion_care_integrity
    premise={'logline':'After her husband dies of illness and a bridge breaks, a widow finds strength protecting her family during a disaster.'}
    assert evaluate_capability_inversion_care_integrity(premise,{},[])['applies'] is False


def test_capability_validator_forced_dependence_fails_ending_checks():
    from studio.capability_inversion_care_integrity import evaluate_capability_inversion_care_integrity
    premise={'logline':'A freakishly strong woman mocked as a freak is hired as bodyguard for a wheelchair CEO.'}
    architecture={'sequences':[{'summary':'She protects him with care labor.'},{'summary':'She has no choice but to stay as his bodyguard.'}]}
    result=evaluate_capability_inversion_care_integrity(premise,architecture,[])
    assert result['checks']['intimacy_is_renegotiated_beyond_the_job'] is False
    assert result['checks']['ending_preserves_independent_livelihood_or_work_choice'] is False


def test_cozy_validator_possessive_home_intrusion_counts_as_disaster_onset():
    from studio.cozy_disaster_shelter_integrity import evaluate_cozy_disaster_shelter_integrity
    premise={'logline':'A family shelters during a flood.'}
    architecture={'sequences':[
        {'summary':'Water rushes into their home before they cook in the shelter.'},
        {'summary':'The family survives rising water with food and drinking water.'},
        {'summary':'After the storm they rebuild the house and share a warm meal.'},
    ]}
    result=evaluate_cozy_disaster_shelter_integrity(premise,architecture,[])
    assert result['checks']['ordinary_labor_establishes_world_before_disaster'] is False

def test_capability_validator_explicit_leg_choice_counts_as_agency():
    from studio.capability_inversion_care_integrity import evaluate_capability_inversion_care_integrity
    premise={'logline':'A freakishly strong woman mocked as a freak is hired as bodyguard for a wheelchair CEO.'}
    architecture={'sequences':[{'summary':'She tells him: your legs, your choice, and she protects him through care labor.'},{'summary':'When the job is done she chooses work and love freely.'}]}
    result=evaluate_capability_inversion_care_integrity(premise,architecture,[])
    assert result['checks']['care_restores_agency_rather_than_infantilizing'] is True


def test_capability_validator_connects_separated_capability_and_stigma():
    from studio.capability_inversion_care_integrity import evaluate_capability_inversion_care_integrity
    premise={'logline':'A woman with superhuman strength is hired as bodyguard for a wheelchair CEO and falls in love.'}
    architecture={'sequences':[{'summary':'She works quietly.'},{'summary':'She protects him.'},{'summary':'The town mocked her as a freak for the damage she caused.'}]}
    assert evaluate_capability_inversion_care_integrity(premise,architecture,[])['applies'] is True


def test_cozy_validator_household_pipe_is_not_disaster_onset():
    from studio.cozy_disaster_shelter_integrity import evaluate_cozy_disaster_shelter_integrity
    premise={'logline':'A family shelters during a storm.'}
    architecture={'sequences':[
        {'summary':'Water comes into their home through a pipe. They cook breakfast, harvest vegetables, and prepare food.'},
        {'summary':'A storm floods the shelter and the family survives with food and drinking water.'},
        {'summary':'After the storm they rebuild the house and share a warm meal.'},
    ]}
    result=evaluate_cozy_disaster_shelter_integrity(premise,architecture,[])
    assert result['checks']['ordinary_labor_establishes_world_before_disaster'] is True

def test_serial_relational_anchor_validator_positive_and_nonapplicable():
    from studio.serial_relational_anchor_integrity import evaluate_serial_relational_anchor_integrity
    premise={'logline':'Season 1 episode 1 of an assassin thriller about a spy protecting her civilian friend.'}
    architecture={'sequences':[
        {'summary':'After a painful goodbye, the agent returns home guilt-ridden because she broke her promise to her friend and chosen family.'},
        {'summary':'The organization leaks intelligence and the antagonist manipulates her fear of losing family, threatening the civilian friend as bait while a mission unfolds.'},
        {'summary':'The friend is abducted as a hostage, forcing a choice and ending the chapter on a cliffhanger.'},
    ]}
    result=evaluate_serial_relational_anchor_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['score_0_to_1'] >= 0.75

    standalone={'logline':'A wizard rescues a dragon in a standalone fantasy film.'}
    assert evaluate_serial_relational_anchor_integrity(standalone,{},[])['applies'] is False

def test_cozy_validator_river_water_submerging_sink_counts_as_disaster_onset():
    from studio.cozy_disaster_shelter_integrity import evaluate_cozy_disaster_shelter_integrity
    premise={'logline':'A family shelters during a flood.'}
    architecture={'sequences':[
        {'summary':'River water enters their home and submerges the sink. Later they cook in the shelter.'},
        {'summary':'The family survives rising water with food and drinking water.'},
        {'summary':'After the flood they rebuild the house and share a warm meal.'},
    ]}
    result=evaluate_cozy_disaster_shelter_integrity(premise,architecture,[])
    assert result['checks']['ordinary_labor_establishes_world_before_disaster'] is False


def test_serial_relational_anchor_declared_format_and_series_of_crimes_boundary():
    from studio.serial_relational_anchor_integrity import evaluate_serial_relational_anchor_integrity
    declared={'release_format':'serial_episode','logline':'A spy protects her civilian friend from an assassin organization.'}
    architecture={'sequences':[
        {'summary':'After a painful goodbye, the agent returns home guilt-ridden because she broke her promise to her friend.'},
        {'summary':'The organization threatens the civilian friend as bait while a mission unfolds.'},
        {'summary':'The friend is abducted as a hostage, forcing an impossible choice.'},
    ]}
    assert evaluate_serial_relational_anchor_integrity(declared,architecture,[])['applies'] is True

    standalone={'logline':'A standalone crime film about a detective solving a series of thefts.'}
    assert evaluate_serial_relational_anchor_integrity(standalone,{},[])['applies'] is False


def test_serial_relational_anchor_ending_requires_final_turn_not_guidance_or_penultimate_event():
    from studio.serial_relational_anchor_integrity import evaluate_serial_relational_anchor_integrity
    premise={'release_format':'serial_episode','logline':'A spy protects her civilian friend from an assassin organization.'}
    scenes=[
        {'turn':'After a painful goodbye, the agent returns home guilt-ridden because she broke her promise to her friend.'},
        {'turn':'The organization threatens the civilian friend as bait. The friend is arrested by corrupt agents.'},
        {'turn':'The finale quietly stops with the agent thinking in her room.','dialogue_design':{'function':'make choices, objections, and proof implications audible rather than explaining theme'}},
    ]
    result=evaluate_serial_relational_anchor_integrity(premise,{},scenes)
    assert result['checks']['chapter_ends_on_active_turn_or_cliffhanger'] is False


def test_serial_relational_anchor_season_label_is_not_relationship():
    from studio.serial_relational_anchor_integrity import evaluate_serial_relational_anchor_integrity
    premise={'logline':'Season 1 of a spy thriller about missions inside a criminal organization.'}
    result=evaluate_serial_relational_anchor_integrity(premise,{},[])
    assert result['applies'] is True
    assert result['checks']['intimate_anchor_exists_beyond_the_mission'] is False


def test_cozy_validator_household_water_systems_do_not_count_as_disaster_onset():
    from studio.cozy_disaster_shelter_integrity import evaluate_cozy_disaster_shelter_integrity
    for chore_text in (
        'Piped water from the river enters their home and fills the sink.',
        "Water enters the household's cistern through the pipe.",
    ):
        premise={'logline':'A family shelters during a flood.'}
        architecture={'sequences':[
            {'summary':chore_text},
            {'summary':'They harvest vegetables and prepare food before the storm.'},
            {'summary':'The storm flood enters their home. They survive rising water with food and drinking water.'},
            {'summary':'After the flood they rebuild the house and share a warm meal.'},
        ]}
        result=evaluate_cozy_disaster_shelter_integrity(premise,architecture,[])
        assert result['checks']['ordinary_labor_establishes_world_before_disaster'] is True


def test_serial_relational_anchor_episode_phrasing_and_plural_family_anchor():
    from studio.serial_relational_anchor_integrity import evaluate_serial_relational_anchor_integrity
    pilot={'logline':'Pilot episode of a spy thriller about an agent protecting her sisters from an organization.'}
    assert evaluate_serial_relational_anchor_integrity(pilot,{},[])['applies'] is True
    assert evaluate_serial_relational_anchor_integrity(pilot,{},[])['checks']['intimate_anchor_exists_beyond_the_mission'] is True

    multi={'logline':'A series of six episodes following a mercenary protecting his brothers.'}
    assert evaluate_serial_relational_anchor_integrity(multi,{},[])['applies'] is True
    assert evaluate_serial_relational_anchor_integrity(multi,{},[])['checks']['intimate_anchor_exists_beyond_the_mission'] is True


def test_cozy_validator_overflowing_river_and_plural_homes_count_as_disaster_onset():
    from studio.cozy_disaster_shelter_integrity import evaluate_cozy_disaster_shelter_integrity
    premise={'logline':'A family shelters during a flood.'}
    cases=[
        'An overflowing river sweeps away the sink as water enters their home.',
        'Water rushes into their homes.',
    ]
    for intrusion in cases:
        architecture={'sequences':[
            {'summary':intrusion},
            {'summary':'They harvest vegetables and prepare food after the intrusion.'},
            {'summary':'The family survives rising water with food and drinking water.'},
            {'summary':'After the flood they rebuild the house and share a warm meal.'},
        ]}
        result=evaluate_cozy_disaster_shelter_integrity(premise,architecture,[])
        assert result['checks']['ordinary_labor_establishes_world_before_disaster'] is False


def test_wound_price_revenge_full_chain_passes():
    from studio.wound_price_revenge_integrity import evaluate_wound_price_revenge_integrity
    premise={'logline':'In a dark fantasy world, a boy whose mother is murdered by a demon hides counting to one hundred while carving a wooden listening wolf. A hunter mentor protects him out of penance and teaches monster weaknesses, the first rule never hunt angry, and six winters of training. When the demon weaponizes his mother’s final words, the boy accepts a soul bargain for revenge, travels with a companion who cares for him, breaks the rule not to go alone, and in the ending says mama it is done before paying the soul price without begging.'}
    architecture={'sequences':[
        {'summary':'The mother hides her child in the cottage and tells him to count while the demon smells a child.'},
        {'summary':'The mentor teaches weaknesses, rules, and training before the boy earns competence.'},
        {'summary':'The antagonist says your mother begged not my son; the wounded hunter counts again as identity.'},
        {'summary':'Ending: he tells mama it is done, accepts the soul price and death without begging, and the companion witnesses the grief.'},
    ]}
    result=evaluate_wound_price_revenge_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['score_0_to_1'] == 1.0


def test_wound_price_revenge_flags_free_power_and_missing_motif_payoff():
    from studio.wound_price_revenge_integrity import evaluate_wound_price_revenge_integrity
    premise={'logline':'A dark fantasy hero takes revenge on a demon king and becomes strong enough to win.'}
    architecture={'sequences':[{'summary':'He fights the demon and wins a crown.'}]}
    result=evaluate_wound_price_revenge_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['checks']['power_or_revenge_has_irreversible_price'] is False
    assert result['checks']['motif_returns_as_climax_identity'] is False
    assert result['score_0_to_1'] < 0.5


def test_wound_price_revenge_does_not_apply_to_generic_romance():
    from studio.wound_price_revenge_integrity import evaluate_wound_price_revenge_integrity
    premise={'logline':'A CEO and a chef fall in love while repairing a family restaurant.'}
    result=evaluate_wound_price_revenge_integrity(premise,{},[])
    assert result['applies'] is False


def test_bonded_machine_pilot_full_chain_passes():
    from studio.bonded_machine_pilot_integrity import evaluate_bonded_machine_pilot_integrity
    premise={
        'title':'The Last Delivery Pilot',
        'logline':'A delivery rider behind on rent is chosen by an alien mech during an invasion and must protect his mother while learning to pilot it.',
        'release_format':'standalone long-form film',
    }
    architecture={'sequences':[
        {'summary':'Leo is a delivery worker worried about rent, money, insurance, and his mother before the alien invasion interrupts ordinary life.'},
        {'summary':'The mech chooses him through a neural link; a mentor makes him practice walking, balance, and first steps again and again before battle.'},
        {'summary':'He calls his mother, promises to come home, and the machine listens, protects civilians, and becomes damaged while refusing to be only a military weapon.'},
    ]}
    scenes=[
        {'summary':'The command treats the machine as an unauthorized asset and orders surrender of the specimen.'},
        {'summary':'In the final battle they share the load as systems overload; cooperation, trust, and timing—not firepower alone—open the core.'},
        {'summary':'The ending names the machine, recognizes it as a companion rather than a weapon, and gives pilot and machine a home beyond utility.'},
    ]
    result=evaluate_bonded_machine_pilot_integrity(premise,architecture,scenes)
    assert result['applies'] is True
    assert result['score_0_to_1'] == 1.0


def test_bonded_machine_pilot_flags_tool_machine_and_free_competence():
    from studio.bonded_machine_pilot_integrity import evaluate_bonded_machine_pilot_integrity
    premise={'title':'War Mech','logline':'A soldier is assigned a robot weapon in an alien war.'}
    architecture={'sequences':[{'summary':'He uses the robot weapon in battle and destroys the core.'}]}
    scenes=[{'summary':'More firepower destroys the enemy. The machine remains a weapon.'}]
    result=evaluate_bonded_machine_pilot_integrity(premise,architecture,scenes)
    assert result['applies'] is True
    assert result['checks']['machine_or_creature_has_vulnerable_agency'] is False
    assert result['checks']['embodied_training_precedes_competence'] is False
    assert result['score_0_to_1'] < 0.4


def test_bonded_machine_pilot_does_not_apply_to_romance():
    from studio.bonded_machine_pilot_integrity import evaluate_bonded_machine_pilot_integrity
    result=evaluate_bonded_machine_pilot_integrity({'title':'Contract bride','logline':'A contract marriage becomes real love.'},{'sequences':[]},[])
    assert result['applies'] is False


def test_wound_price_revenge_rejected_revenge_does_not_trigger_applicability():
    from studio.wound_price_revenge_integrity import evaluate_wound_price_revenge_integrity
    premise={'logline':'In a creature-protection fantasy, Mira repeatedly chooses the dragon child safety over her own exile, freedom, and revenge.'}
    result=evaluate_wound_price_revenge_integrity(premise,{},[])
    assert result['applies'] is False


def test_wound_price_revenge_requires_same_motif_setup_and_payoff():
    from studio.wound_price_revenge_integrity import evaluate_wound_price_revenge_integrity
    premise={'logline':'A boy takes revenge on the demon that murdered his mother.'}
    architecture={'sequences':[
        {'summary':'The opening wooden keepsake and carving ritual define his grief.'},
        {'summary':'He trains and hunts the demon.'},
        {'summary':'In the climax an unrelated song plays while he kills it.'},
    ]}
    result=evaluate_wound_price_revenge_integrity(premise,architecture,[])
    assert result['checks']['motif_returns_as_climax_identity'] is False


def test_wound_price_revenge_rejected_bargain_and_plain_homecoming_are_free():
    from studio.wound_price_revenge_integrity import evaluate_wound_price_revenge_integrity
    premise={'logline':'A boy takes revenge on the demon that murdered his mother.'}
    architecture={'sequences':[
        {'summary':'He rejects the soul bargain, wins for free, and simply goes home in the ending.'},
    ]}
    result=evaluate_wound_price_revenge_integrity(premise,architecture,[])
    assert result['checks']['power_or_revenge_has_irreversible_price'] is False
    assert result['checks']['ending_pays_price_and_closes_grief'] is False


def test_bonded_machine_pilot_ignores_production_ai_notes_for_applicability():
    from studio.bonded_machine_pilot_integrity import evaluate_bonded_machine_pilot_integrity
    premise={
        'title':'Stormglass Keepers',
        'logline':'A dragon protector faces a naval invasion and chooses the dragon child safety over revenge.',
        'production_notes':'AI-generated media reference; not a story machine or artificial intelligence character.',
    }
    result=evaluate_bonded_machine_pilot_integrity(premise,{},[])
    assert result['applies'] is False


def test_wound_price_revenge_discovers_lair_and_swears_revenge_applies():
    from studio.wound_price_revenge_integrity import evaluate_wound_price_revenge_integrity
    premise={'logline':'After a heroine discovers a demon lair, she swears revenge for her murdered mother.'}
    result=evaluate_wound_price_revenge_integrity(premise,{},[])
    assert result['applies'] is True


def test_bonded_machine_pilot_ending_is_independent_of_architecture_key_order():
    from studio.bonded_machine_pilot_integrity import evaluate_bonded_machine_pilot_integrity
    shared={
        'title':'Iron Delivery',
        'logline':'A delivery rider behind on rent is chosen by a robot mech during an alien invasion and trained by a mentor before protecting his mother.',
    }
    ending_text='In the ending the machine says my name is Cole and becomes a companion with a home, not a weapon.'
    sequences=[
        {'summary':'The delivery worker owes rent, is chosen by the mech, trains through walking failure, calls his mother, and protects civilians.'},
        {'summary':'The military calls the machine an unauthorized specimen; pilot and machine trust each other, share the load, overload systems, and cooperate in the final battle core attack.'},
    ]
    first=dict(shared)
    first['architecture']={'ending_payoff':ending_text,'sequences':sequences}
    second=dict(shared)
    second['architecture']={'sequences':sequences,'ending_payoff':ending_text}
    a=evaluate_bonded_machine_pilot_integrity(first,first['architecture'],[])
    b=evaluate_bonded_machine_pilot_integrity(second,second['architecture'],[])
    assert a['checks']['ending_gives_machine_or_pilot_identity_beyond_utility'] is True
    assert b['checks']['ending_gives_machine_or_pilot_identity_beyond_utility'] is True
    assert a['checks']==b['checks']


def test_thumbnail_write_index_merges_existing_rows(tmp_path):
    import json
    from studio.thumbnail_intelligence import write_index
    path=tmp_path/'index.jsonl'
    write_index([{'video_id':'a','channel':'one','views':1}],path)
    write_index([{'video_id':'b','channel':'two','views':2}],path)
    rows=[json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
    assert [r['video_id'] for r in rows]==['a','b']
    write_index([{'video_id':'a','channel':'one','views':3}],path)
    rows=[json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
    assert len(rows)==2 and rows[0]['views']==3


def test_self_selected_athlete_romance_full_chain_passes():
    from studio.self_selected_athlete_romance_integrity import evaluate_self_selected_athlete_romance_integrity
    premise={'title':'The Vault Captain','logline':'A gymnast is humiliated by her basketball-star ex, breaks up publicly, and chooses a supportive team captain while fighting for her own competition future.'}
    architecture={'sequences':[
        {'summary':'At a party he pushes and humiliates her; she says we are done, leaves, and refuses to be picked up after. When the men challenge each other, the captain says they do not get to bet with her because she already chose.'},
        {'summary':'Her gymnastics comeback proceeds through tryouts, training, coach review, scores, routine practice, competition selection, and medical clearance.'},
        {'summary':'Sabotage causes an incident report and suspension; injury requires scans, rehab, medical staff, and eight weeks of physical cost rather than instant return.'},
    ]}
    scenes=[
        {'summary':'The partner supports her, watches, listens, and refuses to be an excuse to skip rehab; neither career is sacrificed for romance.'},
        {'summary':'The rival apologizes and signs a statement, but the report stays and team consequences remain.'},
        {'summary':'In the ending she wins first place through a visible landing and score, says this time I picked me, then lets the partner keep up with her.'},
    ]
    result=evaluate_self_selected_athlete_romance_integrity(premise,architecture,scenes)
    assert result['applies'] is True
    assert result['score_0_to_1'] == 1.0


def test_self_selected_athlete_romance_flags_trophy_romance_and_free_win():
    from studio.self_selected_athlete_romance_integrity import evaluate_self_selected_athlete_romance_integrity
    premise={'title':'Winning the Cheerleader','logline':'Two basketball captains bet on who will win the cheerleader.'}
    architecture={'sequences':[{'summary':'The hero wins the game and gets the girl.'}]}
    result=evaluate_self_selected_athlete_romance_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['checks']['competence_is_procedural_and_visible'] is False
    assert result['checks']['injury_or_comeback_has_physical_cost'] is False
    assert result['score_0_to_1'] < 0.5


def test_self_selected_athlete_romance_not_apply_to_space_mecha():
    from studio.self_selected_athlete_romance_integrity import evaluate_self_selected_athlete_romance_integrity
    result=evaluate_self_selected_athlete_romance_integrity({'logline':'A pilot bonds with a robot during an alien invasion.'},{},[])
    assert result['applies'] is False


def test_bonded_machine_pilot_reads_dialogue_design_identity_reveal():
    from studio.bonded_machine_pilot_integrity import evaluate_bonded_machine_pilot_integrity
    premise={'logline':'A delivery rider is chosen by a robot mech during an alien invasion.'}
    scenes=[
        {'summary':'He trains and protects civilians with the damaged machine.'},
        {'dialogue_design':{'spoken_exchange':[{'speaker':'machine','line':'My name is Cole. I am your companion, not a weapon.'}]}},
    ]
    result=evaluate_bonded_machine_pilot_integrity(premise,{},scenes)
    assert result['checks']['ending_gives_machine_or_pilot_identity_beyond_utility'] is True


def test_bonded_machine_pilot_screenplay_ending_overrides_outline_payoff():
    from studio.bonded_machine_pilot_integrity import evaluate_bonded_machine_pilot_integrity
    premise={'logline':'A delivery rider is chosen by a robot mech during an alien invasion.'}
    architecture={'ending_payoff':'The machine becomes a free companion with a home.'}
    scenes=[{'summary':'In the ending the machine is locked away in a military vault.'}]
    result=evaluate_bonded_machine_pilot_integrity(premise,architecture,scenes)
    assert result['checks']['ending_gives_machine_or_pilot_identity_beyond_utility'] is False


def test_bonded_machine_pilot_finds_cooperative_climax_before_two_aftermath_scenes():
    from studio.bonded_machine_pilot_integrity import evaluate_bonded_machine_pilot_integrity
    premise={'logline':'A delivery rider is chosen by a robot mech during an alien invasion.'}
    scenes=[
        {'summary':'In the final battle they trust each other, share the load, and fire together at the core.'},
        {'summary':'Aftermath crews count the damage.'},
        {'summary':'Later the pilot leaves the base.'},
    ]
    result=evaluate_bonded_machine_pilot_integrity(premise,{},scenes)
    assert result['checks']['climax_requires_cooperation_not_firepower_alone'] is True


def test_wound_price_revenge_refusal_then_later_vow_still_applies():
    from studio.wound_price_revenge_integrity import evaluate_wound_price_revenge_integrity
    premise={'logline':'Mira refuses revenge and chooses protection. Then a second witness swears revenge on the demon that murdered her family.'}
    result=evaluate_wound_price_revenge_integrity(premise,{},[])
    assert result['applies'] is True


def test_wound_price_revenge_explicit_refusal_to_avenge_does_not_apply():
    from studio.wound_price_revenge_integrity import evaluate_wound_price_revenge_integrity
    premise={'logline':'A dragon protector refuses to avenge anyone and chooses protection instead of revenge.'}
    result=evaluate_wound_price_revenge_integrity(premise,{},[])
    assert result['applies'] is False


def test_self_selected_athlete_romance_applicability_avoids_container_vault_and_includes_ballet():
    from studio.self_selected_athlete_romance_integrity import evaluate_self_selected_athlete_romance_integrity
    dragon={'logline':'A dragon lover hides treasure in a vault and romance follows.'}
    assert evaluate_self_selected_athlete_romance_integrity(dragon,{},[])['applies'] is False
    ballet={'logline':'A ballet dancer falls in love while preparing for an audition.'}
    assert evaluate_self_selected_athlete_romance_integrity(ballet,{},[])['applies'] is True


def test_self_selected_athlete_romance_reversed_outcomes_do_not_pass():
    from studio.self_selected_athlete_romance_integrity import evaluate_self_selected_athlete_romance_integrity
    premise={'logline':'A basketball player romance follows a tournament injury.'}
    architecture={'sequences':[{'summary':'She abandons her career for romance, the injury heals overnight, and the rival apology erases the penalty.'}]}
    result=evaluate_self_selected_athlete_romance_integrity(premise,architecture,[])
    assert result['checks']['ambition_is_not_sacrificed_for_romance'] is False
    assert result['checks']['injury_or_comeback_has_physical_cost'] is False
    assert result['checks']['rival_accountability_does_not_erase_consequence'] is False


def test_self_selected_athlete_romance_ending_not_changed_by_field_order():
    from studio.self_selected_athlete_romance_integrity import evaluate_self_selected_athlete_romance_integrity
    premise={'logline':'A gymnast romance reaches the final competition.'}
    seq=[{'summary':'In the ending her routine score wins first place and she chose myself before partnership.'}]
    a={'sequences':seq,'production_note':'metadata after sequences'}
    b={'production_note':'metadata before sequences','sequences':seq}
    ra=evaluate_self_selected_athlete_romance_integrity(premise,a,[])
    rb=evaluate_self_selected_athlete_romance_integrity(premise,b,[])
    assert ra['checks']['climax_is_decided_by_visible_skill'] == rb['checks']['climax_is_decided_by_visible_skill']


def test_curse_cure_intimacy_integrity_positive_case():
    from studio.curse_cure_intimacy_integrity import evaluate_curse_cure_intimacy_integrity
    premise={'logline':'A woman whose mother is ill marries a cursed dragon king whose touch burns every woman.'}
    architecture={'sequences':[{'summary':'He waits because she is not ready; she learns one breath again to control the shift. An enemy spreads lies and tampers with the medicine. He admits that is how it started, but now it is different. She chooses to stay and the curse is broken as they build a family home.'}]}
    result=evaluate_curse_cure_intimacy_integrity(premise,architecture,[])
    assert result['applies'] is True
    assert result['score_0_to_1'] >= 0.66


def test_curse_cure_intimacy_integrity_rejects_instant_transactional_cure():
    from studio.curse_cure_intimacy_integrity import evaluate_curse_cure_intimacy_integrity
    premise={'logline':'A nameless woman instantly cures a cursed dragon king by touch and becomes his possessive bride.'}
    result=evaluate_curse_cure_intimacy_integrity(premise,{},[])
    assert result['applies'] is True
    assert result['checks']['cure_person_has_independent_need_or_identity'] is False
    assert result['checks']['control_or_cure_is_procedural_not_instant'] is False
    assert result['checks']['instrumental_origin_is_confessed_or_revised'] is False


def test_swapped_child_identity_positive_case():
    from studio.swapped_child_identity_integrity import evaluate_swapped_child_identity_integrity
    premise={'logline':'Swapped at birth, the duke real heiress is called a jinx while the false daughter enters the estate.'}
    architecture={'sequences':[{'summary':'The swap is for a better life and good luck. Luck only works if they truly love the child and force will backfire. The child is denied food, marked at the temple, blackmailed to keep her mouth shut, and the loving mother says both are her children and no secrets. A ring and witness reveal the truth; the antagonist will pay and the child is safe at home with family love.'}]}
    r=evaluate_swapped_child_identity_integrity(premise,architecture,[])
    assert r['applies'] is True
    assert r['score_0_to_1'] >= 0.7


def test_swapped_child_identity_rejects_rank_only_restoration():
    from studio.swapped_child_identity_integrity import evaluate_swapped_child_identity_integrity
    premise={'logline':'Swapped at birth, a real daughter heiress returns to a duke estate.'}
    r=evaluate_swapped_child_identity_integrity(premise,{},[])
    assert r['applies'] is True
    assert r['checks']['child_abuse_is_specific_and_material'] is False
    assert r['checks']['truth_is_procedurally_uncovered'] is False
    assert r['checks']['ending_restores_secure_belonging_not_only_rank'] is False


def test_curse_cure_does_not_apply_to_found_family_beastkeeper():
    import json
    from studio.curse_cure_intimacy_integrity import evaluate_curse_cure_intimacy_integrity
    premise=json.load(open('examples/stormglass_keepers/premise.json',encoding='utf-8'))
    assert evaluate_curse_cure_intimacy_integrity(premise,{},[])['applies'] is False


def test_curse_cure_bare_curse_removal_and_nonconsent_do_not_pass():
    from studio.curse_cure_intimacy_integrity import evaluate_curse_cure_intimacy_integrity
    premise={'logline':'A cursed dragon king romance with a bride.'}
    scenes=[{'summary':'He kisses her and never asks permission. At the end the curse is broken.'}]
    r=evaluate_curse_cure_intimacy_integrity(premise,{},scenes)
    assert r['checks']['intimacy_progresses_by_consent_and_pacing'] is False
    assert r['checks']['ending_restores_autonomy_or_shared_life_beyond_curse'] is False


def test_athlete_romance_negated_rejected_outcomes_do_not_count_as_reversed():
    from studio.self_selected_athlete_romance_integrity import evaluate_self_selected_athlete_romance_integrity
    premise={'logline':'A basketball player romance follows a tournament injury.'}
    architecture={'sequences':[{'summary':'She refuses to abandon her career for romance. The injury does not heal overnight. The report is not erased, and the rival admits fault and is suspended. She trains for competition and chooses both career and love.'}]}
    r=evaluate_self_selected_athlete_romance_integrity(premise,architecture,[])
    assert r['checks']['ambition_is_not_sacrificed_for_romance'] is True
    assert r['checks']['rival_accountability_does_not_erase_consequence'] is True


def test_athlete_romance_dance_word_boundaries_and_lasting_injury_cost():
    from studio.self_selected_athlete_romance_integrity import evaluate_self_selected_athlete_romance_integrity
    unrelated={'logline':'Attendance and guidance shape a workplace romance.'}
    assert evaluate_self_selected_athlete_romance_integrity(unrelated,{},[])['applies'] is False
    premise={'logline':'A basketball romance follows a tournament injury.'}
    architecture={'sequences':[{'summary':'She is on crutches for a month and misses the season.'}]}
    r=evaluate_self_selected_athlete_romance_integrity(premise,architecture,[])
    assert r['checks']['injury_or_comeback_has_physical_cost'] is True


def test_athlete_romance_short_epilogues_do_not_hide_scored_climax():
    from studio.self_selected_athlete_romance_integrity import evaluate_self_selected_athlete_romance_integrity
    premise={'logline':'A gymnastics romance reaches the final.'}
    scenes=[{'summary':x} for x in ['opening','training','rivalry','injury','Her routine score wins first place and she chose myself.','short epilogue','short epilogue','short epilogue']]
    r=evaluate_self_selected_athlete_romance_integrity(premise,{},scenes)
    assert r['checks']['climax_is_decided_by_visible_skill'] is True
    assert r['checks']['ending_self_selection_precedes_or_frames_romance'] is True


def test_bl_power_autonomy_positive_case():
    from studio.bl_power_autonomy_romance_integrity import evaluate_bl_power_autonomy_romance_integrity
    premise={'logline':'BL vampire billionaire paid at an auction to save a werewolf wolf king and falls for him.'}
    architecture={'sequences':[{'summary':'The investigator keeps records and the rescued man has his own mission. He is not a bargaining chip and cannot be bought; you can leave. The doctor says write down memories and pain meds need food. Police records evidence and investigation preserve responsibility. You can just say no, this is a trial run, and he will not cross the line. At the end he chooses a relationship and future marriage freely.'}]}
    r=evaluate_bl_power_autonomy_romance_integrity(premise,architecture,[])
    assert r['applies'] is True
    assert r['score_0_to_1'] >= 0.7


def test_bl_power_autonomy_rejects_ownership_possession():
    from studio.bl_power_autonomy_romance_integrity import evaluate_bl_power_autonomy_romance_integrity
    premise={'logline':'BL billionaire alpha buys an omega at auction and kisses him because he owns him.'}
    r=evaluate_bl_power_autonomy_romance_integrity(premise,{},[])
    assert r['applies'] is True
    assert r['checks']['rescue_or_payment_does_not_create_ownership'] is False
    assert r['checks']['intimacy_uses_micro_consent_and_refusal_rights'] is False


def test_swapped_child_rank_restoration_alone_does_not_pass_belonging():
    from studio.swapped_child_identity_integrity import evaluate_swapped_child_identity_integrity
    premise={'logline':'Swapped at birth, a real daughter heiress returns to a duke estate.'}
    scenes=[{'summary':'In the finale the child is named heir.'}]
    r=evaluate_swapped_child_identity_integrity(premise,{},scenes)
    assert r['checks']['ending_restores_secure_belonging_not_only_rank'] is False


def test_curse_cure_refusing_unasked_kiss_counts_as_consent_pacing():
    from studio.curse_cure_intimacy_integrity import evaluate_curse_cure_intimacy_integrity
    premise={'logline':'A cursed dragon king falls in love.'}
    scenes=[{'summary':'She refuses to kiss him without asking permission first and tells him to wait until she is ready.'}]
    r=evaluate_curse_cure_intimacy_integrity(premise,{},scenes)
    assert r['applies'] is True
    assert r['checks']['intimacy_progresses_by_consent_and_pacing'] is True


def test_curse_cure_unrelated_unpermitted_action_does_not_veto_consent():
    from studio.curse_cure_intimacy_integrity import evaluate_curse_cure_intimacy_integrity
    premise={'logline':'A cursed dragon king falls in love.'}
    scenes=[{'summary':'He leaves the council room without permission, then asks before kissing her and waits until she is ready.'}]
    r=evaluate_curse_cure_intimacy_integrity(premise,{},scenes)
    assert r['checks']['intimacy_progresses_by_consent_and_pacing'] is True


def test_bl_power_autonomy_coercion_does_not_count_as_consent_or_freedom():
    from studio.bl_power_autonomy_romance_integrity import evaluate_bl_power_autonomy_romance_integrity
    premise={'logline':'BL billionaire alpha buys an omega at auction.'}
    scenes=[{'summary':'He kisses him without consent and keeps him captive. He is not free to leave.'}]
    r=evaluate_bl_power_autonomy_romance_integrity(premise,{},scenes)
    assert r['checks']['rescue_or_payment_does_not_create_ownership'] is False
    assert r['checks']['intimacy_uses_micro_consent_and_refusal_rights'] is False


def test_bl_power_autonomy_does_not_apply_to_wife_husband_hidden_identity():
    from studio.bl_power_autonomy_romance_integrity import evaluate_bl_power_autonomy_romance_integrity
    premise={'logline':'A wife discovers her billionaire husband hid his identity and reconsiders their marriage.'}
    r=evaluate_bl_power_autonomy_romance_integrity(premise,{},[])
    assert r['applies'] is False


def test_curse_cure_unasked_permission_is_nonconsent_even_when_recipient_resists():
    from studio.curse_cure_intimacy_integrity import evaluate_curse_cure_intimacy_integrity, _has_nonconsensual_intimacy
    assert _has_nonconsensual_intimacy('She tries to stop him as he kisses her without permission.') is True
    assert _has_nonconsensual_intimacy("He kisses her and doesn't ask permission.") is True
    premise={'logline':'A cursed dragon king falls in love.'}
    scenes=[{'summary':'She tries to stop him as he kisses her without permission. He asks too late.'}]
    r=evaluate_curse_cure_intimacy_integrity(premise,{},scenes)
    assert r['checks']['intimacy_progresses_by_consent_and_pacing'] is False


def test_curse_cure_later_refusal_does_not_hide_unwanted_contact():
    from studio.curse_cure_intimacy_integrity import _has_nonconsensual_intimacy
    assert _has_nonconsensual_intimacy('He takes her hand without permission, so she refuses to kiss him.') is True


def test_curse_cure_permission_to_enter_does_not_veto_consensual_kiss():
    from studio.curse_cure_intimacy_integrity import _has_nonconsensual_intimacy
    assert _has_nonconsensual_intimacy("He doesn't ask permission to enter the council room, then asks before kissing her.") is False


def test_bl_power_autonomy_negated_or_rival_control_does_not_veto_positive_autonomy():
    from studio.bl_power_autonomy_romance_integrity import evaluate_bl_power_autonomy_romance_integrity
    premise={'logline':'BL billionaire alpha rescues his husband from a rival vampire.'}
    scenes=[{'summary':"He doesn't own him. A rival keeps him captive, but after rescue he is free to walk away. He asks permission, you can just say no, and they choose a trial run relationship."}]
    r=evaluate_bl_power_autonomy_romance_integrity(premise,{},scenes)
    assert r['applies'] is True
    assert r['checks']['rescue_or_payment_does_not_create_ownership'] is True
    assert r['checks']['intimacy_uses_micro_consent_and_refusal_rights'] is True


def test_bl_power_autonomy_gayle_name_does_not_trigger_gay_gate():
    from studio.bl_power_autonomy_romance_integrity import evaluate_bl_power_autonomy_romance_integrity
    premise={'logline':'Gayle falls for her billionaire boss and discovers his secret.'}
    r=evaluate_bl_power_autonomy_romance_integrity(premise,{},[])
    assert r['applies'] is False


def test_progression_system_survival_positive_case():
    from studio.progression_system_survival_integrity import evaluate_progression_system_survival_integrity
    premise={'logline':'After a shipwreck, a falsely accused survivor is kicked out and activates a desert island fishing system.'}
    architecture={'sequences':[{'summary':'The system gives three daily uses, stamina costs, island coins, corruption risk, and quest deadlines. Water, food, shelter, medicine, cold, and injury recur. He fishes, crafts tools, gathers materials, trades, cooks, and builds shelter. Classmates argue over rationing, leadership, loyalty, and sharing. He protects allies and keeps survivors alive while storms, snakes, cannibals, curses, and system penalties escalate. At the end he has enough fish and supplies, a camp plan, and a concrete titan-python hook.'}]}
    r=evaluate_progression_system_survival_integrity(premise,architecture,[])
    assert r['applies'] is True
    assert r['score_0_to_1'] >= 0.7


def test_progression_system_survival_rejects_unbounded_power_fantasy():
    from studio.progression_system_survival_integrity import evaluate_progression_system_survival_integrity
    premise={'logline':'A man on a survival island activates a level-up system and becomes the strongest king.'}
    r=evaluate_progression_system_survival_integrity(premise,{},[])
    assert r['applies'] is True
    assert r['checks']['system_rules_have_quantified_limits_and_costs'] is False
    assert r['checks']['survival_needs_are_concrete_and_recurrent'] is False


def test_kin_protection_power_reversal_positive_case():
    from studio.kin_protection_power_reversal_integrity import evaluate_kin_protection_power_reversal_integrity
    premise={'logline':'A supreme commander returns secretly after seven years to protect his wife daughter and family from the underworld.'}
    architecture={'sequences':[{'summary':'His secret border mission and oath are specific. His wife leads a financial audit and his sisters stand in front of him. Threats include pensions, debts, coma, kidnapping, and murder. Protection uses surveillance, evidence, transfer records, digital signatures, backups, police verification, a badge, and payment records. His kin reciprocate and take care of him. Violence is bounded by innocents and control. The antagonist network is traced to clients, skimmed pensions, foreign agents, and family succession. At the end the family is safe, truth is verified, and the network is arrested before the next hook.'}]}
    r=evaluate_kin_protection_power_reversal_integrity(premise,architecture,[])
    assert r['applies'] is True
    assert r['score_0_to_1'] >= 0.7


def test_kin_protection_power_reversal_rejects_prop_family():
    from studio.kin_protection_power_reversal_integrity import evaluate_kin_protection_power_reversal_integrity
    premise={'logline':'A hidden king protects his sisters because he is powerful.'}
    r=evaluate_kin_protection_power_reversal_integrity(premise,{},[])
    assert r['applies'] is True
    assert r['checks']['protected_kin_have_independent_roles_or_competence'] is False
    assert r['checks']['protection_uses_procedure_or_verification_not_only_violence'] is False


def test_progression_survival_word_boundaries_and_runtime_ranges():
    from studio.progression_system_survival_integrity import evaluate_progression_system_survival_integrity
    premise={'logline':'At a royal banquet, a craft guild protects its status through ceremonial cooking.'}
    arch={'sequences':[{'time_range':'0-12 minutes','summary':'status craft'}]}
    r=evaluate_progression_system_survival_integrity(premise,arch,[])
    assert r['applies'] is False


def test_bl_ellipsis_and_mixed_ownership_are_not_hidden():
    from studio.bl_power_autonomy_romance_integrity import _has_coercive_control, evaluate_bl_power_autonomy_romance_integrity
    assert _has_coercive_control('He kisses him... without asking permission.') is True
    assert _has_coercive_control("He doesn't own him in law, but he owns him in practice.") is True
    premise={'logline':'BL romance: a billionaire alpha rescues a male omega.'}
    scenes=[{'summary':'You can’t walk away.'}]
    r=evaluate_bl_power_autonomy_romance_integrity(premise,{},scenes)
    assert r['checks']['rescue_or_payment_does_not_create_ownership'] is False


def test_curse_taking_breath_refusal_is_not_false_active_intimacy():
    from studio.curse_cure_intimacy_integrity import _has_nonconsensual_intimacy
    assert _has_nonconsensual_intimacy('She takes a breath and refuses to kiss him without consent.') is False


def test_kin_protection_word_boundaries_and_negative_ending():
    from studio.kin_protection_power_reversal_integrity import evaluate_kin_protection_power_reversal_integrity
    premise={'logline':'A resonance technician protects train wreck survivors with hidden power.'}
    r=evaluate_kin_protection_power_reversal_integrity(premise,{},[])
    assert r['applies'] is False
    premise={'logline':'A hidden commander protects his family.'}
    scenes=[{'summary':'At the end the family is not safe and the next revenge hook begins.'}]
    r=evaluate_kin_protection_power_reversal_integrity(premise,{},scenes)
    assert r['checks']['ending_restores_family_safety_or_truth_before_next_hook'] is False


def test_curse_refusal_does_not_mask_unwanted_grab():
    from studio.curse_cure_intimacy_integrity import _has_nonconsensual_intimacy
    assert _has_nonconsensual_intimacy('He grabs her chin without permission and she refuses to kiss him.') is True


def test_animal_communication_zoo_revival_positive_case():
    from studio.animal_communication_zoo_revival_integrity import evaluate_animal_communication_zoo_revival_integrity
    premise={'logline':'A zoo director who understands animals must save a failing wildlife park from debt and sabotage.'}
    architecture={'sequences':[{'summary':'Overdue bills, water and power cutoff, feed mill debt, broken infrastructure, and only 50,000 left create the crisis. A tiger wants an itch scratched, a kangaroo is depressed because he wants to be famous, and an elephant prefers morning sunlight and a pool. The monkey, tiger, kangaroo, elephant, parrot, and hens have distinct personalities. She asks why behavior happens, listens, coaxes, builds trust, and does not force practice; if the elephant does not want to perform, the choice is entirely up to him. Visitors buy tickets after viral videos, a media planner calls, reservations reopen, sponsors invest, and a contract exchange brings revenue. Rescue uses snacks, calm instructions, health exam, transport assessment, double fencing, visitor limits, surveillance, no bait, and barriers. A competitor plots sabotage, blocks the road, and uses an exploitative exchange. At the end the zoo is saved, visitors return, the animals are safe healthy happy at home, and the park thrives.'}]}
    r=evaluate_animal_communication_zoo_revival_integrity(premise,architecture,[])
    assert r['applies'] is True
    assert r['score_0_to_1'] >= 0.8


def test_animal_communication_zoo_revival_rejects_forced_minions():
    from studio.animal_communication_zoo_revival_integrity import evaluate_animal_communication_zoo_revival_integrity
    premise={'logline':'A man who understands animals uses zoo animals to make his failing business viral.'}
    r=evaluate_animal_communication_zoo_revival_integrity(premise,{},[])
    assert r['applies'] is True
    assert r['checks']['animal_autonomy_and_refusal_are_explicit'] is False
    assert r['checks']['animal_safety_protocols_limit_showmanship'] is False


def test_kin_plural_and_temporal_closure_regressions():
    from studio.kin_protection_power_reversal_integrity import evaluate_kin_protection_power_reversal_integrity
    r=evaluate_kin_protection_power_reversal_integrity({'logline':'A hidden commander protects his daughters.'},{},[])
    assert r['applies'] is True
    scenes=[{'summary':'His daughter was never safe until the kidnappers were stopped.'}]
    r=evaluate_kin_protection_power_reversal_integrity({'logline':'A hidden commander protects his family.'},{},scenes)
    assert r['checks']['ending_restores_family_safety_or_truth_before_next_hook'] is True


def test_curse_prop_grab_and_supportive_contact_regressions():
    from studio.curse_cure_intimacy_integrity import _has_nonconsensual_intimacy
    assert _has_nonconsensual_intimacy('He grabs an antidote without asking and saves her.') is False
    assert _has_nonconsensual_intimacy('He takes her arm to steady her and refuses to kiss her without consent.') is False
    assert _has_nonconsensual_intimacy('He grabs her chin without permission and she refuses to kiss him.') is True


def test_curse_unwanted_waist_grab_detected():
    from studio.curse_cure_intimacy_integrity import _has_nonconsensual_intimacy
    assert _has_nonconsensual_intimacy('He grabs her waist without asking.') is True


def test_incognito_moral_test_positive_case():
    from studio.incognito_moral_test_integrity import evaluate_incognito_moral_test_integrity
    premise={'logline':'A billionaire mother pretends to be a maid to test how her son’s fiancée treats powerless workers.'}
    architecture={'sequences':[{'summary':'Before the test, the bride displays a 15-million-naira gown as a status object. The disguised mother spills soup on the gown, is slapped and thrown into the rain, while the unpaid cook opens the door, shelters her, shares food, and risks her job. The son objects that covert testing is not his exam and the mother apologizes because the test cost trust. A tailor tag, rental receipt, witnesses, bill, contract records, and camera evidence prove the fraud. At the end the cook owns her restaurant, receives an independent income, her wages are repaid, she has a voice and free choice rather than merely marrying into wealth.'}]}
    r=evaluate_incognito_moral_test_integrity(premise,architecture,[])
    assert r['applies'] is True
    assert r['score_0_to_1'] >= 0.8


def test_incognito_moral_test_flags_costless_reward_and_uncontested_test():
    from studio.incognito_moral_test_integrity import evaluate_incognito_moral_test_integrity
    premise={'logline':'A billionaire father pretends to be a cleaner to test whether his son’s fiancée is kind.'}
    r=evaluate_incognito_moral_test_integrity(premise,{},[])
    assert r['applies'] is True
    assert r['checks']['kindness_is_active_and_costly_before_reward'] is False
    assert r['checks']['covert_test_is_ethically_contested'] is False
    assert r['checks']['ending_restores_independent_dignity_and_livelihood'] is False


def test_age_gap_romance_positive_autonomy_case():
    from studio.age_gap_romance_autonomy_integrity import evaluate_age_gap_romance_autonomy_integrity
    premise={'logline':'An adult younger woman marries an older widower billionaire despite age-gap gossip and family opposition.'}
    arch={'sequences':[{'summary':'Both adults are explicit; she is a grown woman, never too young to choose, and refuses money. Wealth, gold-digger gossip, account transfer, and financial power are named. She can leave, has her own shop and independent work, and chooses him. Love is patience, respect, honesty, trust, listening, sacrifice, learning habits, and repair. His children grieve their mother and fear replacement, so their protection is legitimate. Transfer records, account access, witnesses, documents, and confession resolve the accusation. After marriage they talk honestly, communicate, apologize, respect boundaries, and feel safe. The ending preserves her own shop, career, ordinary work, chosen family, and identity.'}]}
    r=evaluate_age_gap_romance_autonomy_integrity(premise,arch,[])
    assert r['applies'] is True
    assert r['score_0_to_1'] >= 0.8


def test_age_gap_romance_flags_infantilized_transactional_love():
    from studio.age_gap_romance_autonomy_integrity import evaluate_age_gap_romance_autonomy_integrity
    premise={'logline':'A young girl catches an old billionaire husband and society judges their marriage.'}
    r=evaluate_age_gap_romance_autonomy_integrity(premise,{},[])
    assert r['applies'] is True
    assert r['checks']['both_partners_are_unambiguously_adults'] is False
    assert r['checks']['younger_partner_has_refusal_rights_and_independence'] is False


def test_incognito_moral_test_applicability_and_temporal_regressions():
    from studio.incognito_moral_test_integrity import evaluate_incognito_moral_test_integrity
    unrelated={'logline':'A maid and an heir face humiliation at a banquet.'}
    assert evaluate_incognito_moral_test_integrity(unrelated,{},[])['applies'] is False
    premise={'logline':'A billionaire mother pretends to be a maid to test how the fiancée treats workers.'}
    arch={'sequences':[{'summary':'The worker loses wages in the opening. Only after the mother rewards her with a shop does the worker open the door and share food.'}]}
    r=evaluate_incognito_moral_test_integrity(premise,arch,[])
    assert r['checks']['kindness_is_active_and_costly_before_reward'] is False
    assert r['checks']['ending_restores_independent_dignity_and_livelihood'] is False
    arch={'sequences':[{'summary':'The son says this is not your exam and you never asked me.'}]}
    r=evaluate_incognito_moral_test_integrity(premise,arch,[])
    assert r['checks']['covert_test_is_ethically_contested'] is True


def test_age_gap_numeric_and_unrelated_adult_regressions():
    from studio.age_gap_romance_autonomy_integrity import evaluate_age_gap_romance_autonomy_integrity
    premise={'logline':'A 24-year-old woman marries a 49-year-old billionaire as society judges their marriage.'}
    assert evaluate_age_gap_romance_autonomy_integrity(premise,{},[])['applies'] is True
    same_age={'logline':'A young woman marries a young billionaire as society judges their marriage.'}
    assert evaluate_age_gap_romance_autonomy_integrity(same_age,{},[])['applies'] is False
    premise={'logline':'A young girl catches an old billionaire husband and society judges their marriage.'}
    arch={'sequences':[{'summary':'His adult children object but neither partner is called an adult.'}]}
    r=evaluate_age_gap_romance_autonomy_integrity(premise,arch,[])
    assert r['checks']['both_partners_are_unambiguously_adults'] is False


def test_incognito_premise_only_uses_premise_text():
    from studio.incognito_moral_test_integrity import evaluate_incognito_moral_test_integrity
    premise={'logline':'A billionaire mother pretends to be a maid to test how the fiancée treats workers. The cook shares her food before any reward, the son says this is not your exam, and the ending gives the cook her own restaurant.'}
    r=evaluate_incognito_moral_test_integrity(premise,{},[])
    assert r['applies'] is True
    assert r['checks']['kindness_is_active_and_costly_before_reward'] is True


def test_class_performance_misread_integrity_positive_and_negative():
    from studio.class_performance_misread_integrity import evaluate_class_performance_misread_integrity
    premise={'logline':'Reborn after her first life left her in debt and humiliated for buying her way into belonging, a poor student stops performing wealth. She puts her bag wherever she likes, turns down exclusive invitations, and stays ordinary. Heiresses misread her unbothered taste and generosity as old money, though she has no secret dynasty.'}
    arch={'sequences':[{'summary':'Her boundary, taste, and help saving face create social access through collectors, membership, invitations, and a foundation president. The audience knows the family explanation is a projection, not a secret dynasty.'},{'summary':'Former rivals apologize and become reciprocal friends. An opportunity has public requirements, an independent panel, disclosure, and she asks about the work before the title. The ending preserves ordinary selfhood, her own name, independent choice, and the sense that she does not need approval.'}]}
    r=evaluate_class_performance_misread_integrity(premise,arch,[])
    assert r['applies'] is True
    assert r['score_0_to_1'] >= 0.875
    generic={'logline':'A reborn poor student becomes rich and everyone admires her.'}
    assert evaluate_class_performance_misread_integrity(generic,{},[])['applies'] is False


def test_review_regressions_class_age_and_costly_kindness():
    from studio.class_performance_misread_integrity import evaluate_class_performance_misread_integrity
    from studio.age_gap_romance_autonomy_integrity import evaluate_age_gap_romance_autonomy_integrity, _has_age_gap_evidence
    from studio.incognito_moral_test_integrity import evaluate_incognito_moral_test_integrity

    flashback={'logline':'In a flashback she goes back to the pool, performs better, and earns status in a rich club.'}
    assert evaluate_class_performance_misread_integrity(flashback,{},[])['applies'] is False

    premise={'logline':'Reborn after her first life left her in debt for buying her way into belonging, a poor student stops performing wealth. She turns down exclusive invitations and stays ordinary. Heiresses misread her unbothered taste as old money though she has no secret dynasty. The ending preserves ordinary selfhood, independent choice, and her own name.'}
    arch={'sequences':[{'summary':'Her taste creates invitations, membership, collector access, and gossip. Rivals apologize, become friends, public requirements use an independent panel, disclosure, records, and work.'}]}
    many_scenes=[{'scene':i,'brief':'scene filler status conversation'} for i in range(20)]
    r=evaluate_class_performance_misread_integrity(premise,arch,many_scenes)
    assert r['checks']['ending_preserves_ordinary_selfhood_beyond_status'] is True
    dynasty=evaluate_class_performance_misread_integrity({'logline':premise['logline']+' In the finale she is revealed as old money and they guessed correctly.'},arch,many_scenes)
    assert dynasty['checks']['audience_knows_status_is_projection_not_secret_dynasty'] is False

    same_age={'logline':'A 24-year-old woman marries a 24-year-old man while her 56-year-old mother objects and society judges their marriage.'}
    assert evaluate_age_gap_romance_autonomy_integrity(same_age,{},[])['applies'] is False
    numeric={'logline':'A 24-year-old woman marries a 49-year-old billionaire as society judges their marriage.'}
    nr=evaluate_age_gap_romance_autonomy_integrity(numeric,{},[])
    assert nr['applies'] is True
    assert nr['checks']['both_partners_are_unambiguously_adults'] is True
    assert _has_age_gap_evidence('an older widower marries a woman half his age despite family opposition') is True

    routine={'logline':'A billionaire mother pretends to be a maid to test how the fiancée treats workers. During a routine shift the cook opens the door before any promotion or reward. The son says this is not your exam and records expose the cruelty.'}
    rr=evaluate_incognito_moral_test_integrity(routine,{},[])
    assert rr['checks']['kindness_is_active_and_costly_before_reward'] is False


def test_misplaced_family_loyalty_integrity_positive_and_negative():
    from studio.misplaced_family_loyalty_integrity import evaluate_misplaced_family_loyalty_integrity
    premise={'logline':'A true son is framed by a fake heir and cast out by his family after years of cooking, work, and devotion. The family believed his lies because he could frame him to his face and they would still believe the favorite.'}
    arch={'sequences':[{'summary':'The protagonist disowns them and walks away. Files, records, witnesses, investigation, bankruptcy, and prison expose the theft. The family says we were so wrong, acknowledges favoritism, and the ending chooses protection, welcome home, love, and repair rather than annihilation alone.'}]}
    r=evaluate_misplaced_family_loyalty_integrity(premise,arch,[])
    assert r['applies'] is True
    assert r['score_0_to_1'] >= 0.875
    assert evaluate_misplaced_family_loyalty_integrity({'logline':'A space captain explores a distant planet.'},{},[])['applies'] is False


def test_deprioritized_spouse_power_reversal_integrity_positive_and_negative():
    from studio.deprioritized_spouse_power_reversal_integrity import evaluate_deprioritized_spouse_power_reversal_integrity
    premise={'logline':'A wife whose husband always chose his adopted sister and mistress during hospital and wedding crises finally walked away. The rival had family obligation and personal leverage, but the wife returns with authority over half the family.'}
    arch={'ending_payoff':'His regret is too late and there are no second chances. She has institutional power, earned respect, and is no longer anyone’s wife or weakness; she is the rule, with consequences for his empire.'}
    r=evaluate_deprioritized_spouse_power_reversal_integrity(premise,arch,[])
    assert r['applies'] is True
    assert r['score_0_to_1'] >= 0.85
    assert evaluate_deprioritized_spouse_power_reversal_integrity({'logline':'A sailor crosses the ocean.'},{},[])['applies'] is False
