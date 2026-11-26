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
    assert evaluate_meaning_carrier(premise, {})["score_0_to_1"] == 1.0
    weak = evaluate_meaning_carrier({"opening_event": {"first_10_seconds": "abstract royal politics"}}, {})
    assert weak["score_0_to_1"] < 1.0
    assert weak["warnings"]

def test_relational_contract_gate():
    from studio.relational_contract import evaluate_relational_contract
    good = {"relational_contract": {"power_asymmetry": "x", "safety_or_kindness_before_power": "she protects him before knowing his power", "costly_protagonist_action": "x", "consent_or_personhood_repair": "he is free to choose", "payoff_image": "shared home"}}
    assert evaluate_relational_contract(good)["score_0_to_1"] == 1.0
    assert evaluate_relational_contract({})["warnings"]
