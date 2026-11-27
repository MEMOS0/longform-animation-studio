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
