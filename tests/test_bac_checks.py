from vaultghost import bac_checks
from vaultghost.fixture_manifest import ExpectedFixture

def _expected(name, layer="BAC"):
    return ExpectedFixture(name, [], layer, "BAC_BLOCKED", None, None, False, False, False, "PROPOSED")

def test_bac_model_profile_mismatch_fixture_19():
    fixture = {"model_id_requested": "model-alpha", "bac": {"profile_ref": {"model_id": "model-beta"}, "session_id": "s1"}, "session_id": "s1"}
    valid, reason, ctx = bac_checks.validate(fixture, _expected("19_bac_model_profile_mismatch.json"))
    assert valid is False
    assert reason == "BAC_MODEL_MISMATCH"
    assert ctx is False

def test_bac_cross_session_fixture_20():
    fixture = {"session_id": "s1", "bac": {"session_id": "s2"}}
    valid, reason, ctx = bac_checks.validate(fixture, _expected("20_bac_cross_session_chain.json"))
    assert valid is False
    assert reason == "BAC_SESSION_MISMATCH"
    assert ctx is False

def test_profile_superseded_fixture_24_missing_context():
    fixture = {"bac": {"profile_version_hash": "x"}}
    valid, reason, ctx = bac_checks.validate(fixture, _expected("24_profile_superseded_stale.json", layer="PROFILE"), context=None)
    assert valid is False
    assert reason == "MISSING_CONTEXT"
    assert ctx is True
