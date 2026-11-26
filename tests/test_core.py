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
