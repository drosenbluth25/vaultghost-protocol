import json
from pathlib import Path
import pytest

NEGATIVE_DIR = Path(__file__).resolve().parents[1] / "test-vectors" / "negative"

REQUIRED = [
    "EXPECTED_RESULTS.json",
    "01_legacy_model_id_confirmed.json",
    "02_model_id_mismatch_fatal.json",
    "03_token_delta_trusted_top_level.json",
    "04_reasoning_absent_sentinel.json",
    "05_reasoning_content_leakage.json",
    "06_fingerprint_drift_stored_false.json",
    "07_gating_field_mutation.json",
    "08_genesis_zero_prior_hash.json",
    "09_sequence_gap.json",
    "10_tee_counter_regression.json",
    "11_sealed_with_fault_type.json",
    "12_voided_without_reason.json",
    "13_role_key_mismatch.json",
    "14_key_collision.json",
    "15_unknown_anomaly_flag.json",
    "16_fatal_anomaly_not_voided.json",
    "17_confidence_boundary_ambiguity.json",
    "18_hazard_index_pre_oi003.json",
    "19_bac_model_profile_mismatch.json",
    "20_bac_cross_session_chain.json",
    "21_non_utc_timestamp.json",
    "22_timestamp_regression.json",
    "23_missing_provider_binding_ref.json",
    "24_profile_superseded_stale.json",
    "25_raw_rs_signature.json",
    "26_double_hash_signature.json",
    "27_placeholder_hash.json",
    "28_bad_log_head_commitment.json",
    "29_partial_record_after_fault.txt",
]

def test_all_29_fixtures_present():
    missing = [name for name in REQUIRED if not (NEGATIVE_DIR / name).exists()]
    assert not missing
    assert len([p for p in NEGATIVE_DIR.iterdir() if p.is_file()]) == 30

def test_partial_record_is_malformed_text():
    p = NEGATIVE_DIR / "29_partial_record_after_fault.txt"
    with pytest.raises(json.JSONDecodeError):
        json.loads(p.read_text())
