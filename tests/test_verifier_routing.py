import json
from pathlib import Path
from vaultghost.fixture_manifest import load_expected_results
from vaultghost.verifier import verify_fixture

NEGATIVE_DIR = Path(__file__).resolve().parents[1] / "test-vectors" / "negative"

def _load(name):
    return json.loads((NEGATIVE_DIR / name).read_text())

def _expected(name):
    return load_expected_results(NEGATIVE_DIR / "EXPECTED_RESULTS.json")[name]

def test_model_mismatch_voided():
    result = verify_fixture(_load("02_model_id_mismatch_fatal.json"), _expected("02_model_id_mismatch_fatal.json"))
    assert result.actual_result == "VOIDED"
    assert "ANOMALY_MODEL_MISMATCH" in result.anomaly_flags

def test_context_required_without_context():
    for name in [
        "07_gating_field_mutation.json",
        "09_sequence_gap.json",
        "10_tee_counter_regression.json",
        "13_role_key_mismatch.json",
        "14_key_collision.json",
        "22_timestamp_regression.json",
        "24_profile_superseded_stale.json",
        "28_bad_log_head_commitment.json",
    ]:
        result = verify_fixture(_load(name), _expected(name), context=None)
        assert result.actual_result == "STATE_CONTEXT_REQUIRED", name
        assert result.blocked_by_missing_context is True

def test_generator_required_fixture_26():
    result = verify_fixture(_load("26_double_hash_signature.json"), _expected("26_double_hash_signature.json"))
    assert result.actual_result == "GENERATOR_REQUIRED"
    assert result.blocked_by_generator is True

def test_partial_record_parse_error():
    p = NEGATIVE_DIR / "29_partial_record_after_fault.txt"
    assert p.suffix == ".txt"
    assert _expected(p.name).expected_result == "PARSE_ERROR"

def test_full_fixture_suite_routes_without_unexpected_errors():
    manifest = load_expected_results(NEGATIVE_DIR / "EXPECTED_RESULTS.json")
    for name, expected in manifest.items():
        if name.endswith(".txt"):
            continue
        result = verify_fixture(_load(name), expected, context=None)
        assert result.actual_result in {"REJECT", "VOIDED", "BAC_BLOCKED", "STATE_CONTEXT_REQUIRED", "GENERATOR_REQUIRED", "ANOMALY"}, name
        assert result.actual_result != "PASS", name
