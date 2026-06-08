import json
from pathlib import Path

NEGATIVE_DIR = Path(__file__).resolve().parents[1] / "test-vectors" / "negative"

CANONICAL = {
    "01_legacy_model_id_confirmed.json": ["VG-P-001"],
    "02_model_id_mismatch_fatal.json": ["VG-P-002"],
    "03_token_delta_trusted_top_level.json": ["VG-P-003"],
    "04_reasoning_absent_sentinel.json": ["VG-P-004"],
    "05_reasoning_content_leakage.json": ["VG-P-004"],
    "06_fingerprint_drift_stored_false.json": ["VG-P-005"],
    "07_gating_field_mutation.json": ["VG-P-006"],
    "08_genesis_zero_prior_hash.json": ["VG-P-007"],
    "09_sequence_gap.json": ["VG-P-008"],
    "10_tee_counter_regression.json": ["VG-P-008"],
    "11_sealed_with_fault_type.json": ["VG-P-009"],
    "12_voided_without_reason.json": ["VG-P-009"],
    "13_role_key_mismatch.json": ["VG-P-010"],
    "14_key_collision.json": ["VG-P-010"],
    "15_unknown_anomaly_flag.json": ["VG-P-011"],
    "16_fatal_anomaly_not_voided.json": ["VG-P-012"],
    "17_confidence_boundary_ambiguity.json": ["VG-P-013"],
    "18_hazard_index_pre_oi003.json": ["VG-P-014"],
    "19_bac_model_profile_mismatch.json": ["VG-P-015"],
    "20_bac_cross_session_chain.json": ["VG-P-015"],
    "21_non_utc_timestamp.json": ["VG-P-016"],
    "22_timestamp_regression.json": ["VG-P-016"],
    "23_missing_provider_binding_ref.json": ["VG-P-017"],
    "24_profile_superseded_stale.json": ["VG-P-018"],
    "25_raw_rs_signature.json": ["LEGACY-SIG-303"],
    "26_double_hash_signature.json": ["LEGACY-SIG-307"],
    "27_placeholder_hash.json": ["LEGACY-SCHEMA-016"],
    "28_bad_log_head_commitment.json": ["LEGACY-ANCHOR-511"],
    "29_partial_record_after_fault.txt": ["VG-P-009"],
}

def test_manifest_patch_ids_are_canonical():
    data = json.loads((NEGATIVE_DIR / "EXPECTED_RESULTS.json").read_text())
    observed = {row["fixture"]: row["patch_ids"] for row in data}
    assert observed == CANONICAL

def test_fixture_29_manifest_expected_result_is_parse_error():
    data = json.loads((NEGATIVE_DIR / "EXPECTED_RESULTS.json").read_text())
    row = next(row for row in data if row["fixture"] == "29_partial_record_after_fault.txt")
    assert row["expected_result"] == "PARSE_ERROR"
