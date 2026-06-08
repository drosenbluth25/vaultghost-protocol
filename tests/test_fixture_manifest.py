import json
from pathlib import Path
import pytest
from vaultghost.fixture_manifest import get_expected_for_fixture, load_expected_results

NEGATIVE_DIR = Path(__file__).resolve().parents[1] / "test-vectors" / "negative"

def test_manifest_loads_list_format():
    data = json.loads((NEGATIVE_DIR / "EXPECTED_RESULTS.json").read_text())
    assert isinstance(data, list)
    assert len(data) == 29
    manifest = load_expected_results(NEGATIVE_DIR / "EXPECTED_RESULTS.json")
    assert len(manifest) == 29

def test_get_expected_for_fixture_missing_fails_closed():
    with pytest.raises(KeyError):
        get_expected_for_fixture("missing.json", {})
