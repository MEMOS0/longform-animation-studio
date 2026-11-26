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
