from vaultghost import state_checks

def test_sealed_with_fault_rejected():
    valid, reason, ctx = state_checks.validate({"state": "SEALED", "fault_type": "CRITICAL_FAULT"})
    assert valid is False
    assert reason == "STATE_CONSISTENCY"
    assert ctx is False

def test_voided_without_reason_rejected():
    valid, reason, ctx = state_checks.validate({"state": "VOIDED", "void_reason": None})
    assert valid is False
    assert reason == "STATE_CONSISTENCY"
    assert ctx is False

def test_fatal_anomaly_not_voided_rejected():
    valid, reason, ctx = state_checks.validate({"state": "SEALED", "anomaly_flags": ["FATAL_ANOMALY"]})
    assert valid is False
    assert reason == "FATAL_NOT_VOIDED"
    assert ctx is False
