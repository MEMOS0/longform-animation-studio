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

def test_exact_storyboards_s01_to_s04_valid():
    from studio.storyboard import validate_storyboard_file
    expected = {"S01": 300.0, "S02": 300.0, "S03": 360.0, "S04": 360.0}
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
