from vaultghost import time_checks

def test_non_utc_timestamp_rejected():
    valid, reason, ctx_req = time_checks.validate({"timestamp_iso8601": "2026-06-08T12:00:19+02:00"})
    assert valid is False
    assert reason == "NON_UTC_TIMESTAMP"
    assert ctx_req is False

def test_timestamp_regression_missing_context():
    fixture = {"timestamp_iso8601": "2026-06-08T12:00:00Z"}
    valid, reason, ctx_req = time_checks.validate(fixture, expected_time_context_required=True, context=None)
    assert valid is False
    assert reason == "MISSING_CONTEXT"
    assert ctx_req is True

def test_timestamp_regression_detected_with_parsed_datetime():
    fixture = {"timestamp_iso8601": "2026-06-08T11:59:00Z"}
    context = {"prior_timestamp": "2026-06-08T12:00:00Z"}
    valid, reason, ctx_req = time_checks.validate(fixture, expected_time_context_required=True, context=context)
    assert valid is False
    assert reason == "TIMESTAMP_REGRESSION"
    assert ctx_req is False
