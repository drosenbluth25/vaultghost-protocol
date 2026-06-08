import json
from pathlib import Path
import pytest
from vaultghost.fixture_manifest import load_expected_results
from vaultghost.verifier import verify_fixture

NEGATIVE_DIR = Path(__file__).resolve().parents[1] / "test-vectors" / "negative"
ALLOWED_NEGATIVE_RESULTS = {"REJECT", "VOIDED", "BAC_BLOCKED", "STATE_CONTEXT_REQUIRED", "GENERATOR_REQUIRED", "PARSE_ERROR", "ANOMALY"}

def test_all_negative_fixtures_are_materialized_and_routed():
    manifest = load_expected_results(NEGATIVE_DIR / "EXPECTED_RESULTS.json")
    materialized = {p.name for p in NEGATIVE_DIR.iterdir() if p.is_file() and p.name != "EXPECTED_RESULTS.json"}
    assert materialized == set(manifest.keys())
    routed = []
    parse_checked = []
    for name, expected in manifest.items():
        path = NEGATIVE_DIR / name
        if path.suffix == ".txt":
            with pytest.raises(json.JSONDecodeError):
                json.loads(path.read_text())
            assert expected.expected_result in {"PARSE_ERROR", "REJECT"}
            parse_checked.append(name)
            continue
        data = json.loads(path.read_text())
        result = verify_fixture(data, expected, context=None)
        actual = result.actual_result
        expected_result = expected.expected_result
        assert actual in ALLOWED_NEGATIVE_RESULTS
        if expected.generator_required:
            assert actual == "GENERATOR_REQUIRED"
        elif expected.state_context_required:
            assert actual == "STATE_CONTEXT_REQUIRED"
        else:
            assert actual == expected_result
        routed.append(name)
    assert len(routed) == 28
    assert parse_checked == ["29_partial_record_after_fault.txt"]
