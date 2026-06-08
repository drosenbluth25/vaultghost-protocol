from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from . import anomaly_checks, bac_checks, schema_checks, signature_checks, state_checks, time_checks, token_privacy
from .fixture_manifest import ExpectedFixture

ALLOWED_RESULTS = {"PASS", "REJECT", "VOIDED", "BAC_BLOCKED", "STATE_CONTEXT_REQUIRED", "GENERATOR_REQUIRED", "PARSE_ERROR", "ANOMALY"}

@dataclass
class VerificationResult:
    fixture: str
    patch_ids: List[str]
    layer: str
    expected_result: str
    actual_result: str
    existing_error_code: Optional[str]
    proposed_error_code: Optional[str]
    anomaly_flags: List[str]
    state_context_required: bool
    generator_required: bool
    blocked_by_missing_context: bool
    blocked_by_generator: bool
    routing_ok: bool
    passed_expectation: bool
    notes: str

def _codes(expected: ExpectedFixture) -> tuple[Optional[str], Optional[str]]:
    return expected.existing_error_code, expected.proposed_error_code

def verify_fixture(
    fixture: Dict[str, Any],
    expected: ExpectedFixture,
    context: Optional[Dict[str, Any]] = None,
) -> VerificationResult:
    def build(layer: str, actual: str, anomalies: Optional[List[str]] = None, notes: str = "") -> VerificationResult:
        existing, proposed = _codes(expected)
        blocked_ctx = actual == "STATE_CONTEXT_REQUIRED"
        blocked_gen = actual == "GENERATOR_REQUIRED"
        passed = actual == expected.expected_result
        if blocked_ctx or blocked_gen:
            passed = False
        return VerificationResult(
            fixture=expected.fixture,
            patch_ids=expected.patch_ids,
            layer=layer,
            expected_result=expected.expected_result,
            actual_result=actual,
            existing_error_code=existing,
            proposed_error_code=proposed,
            anomaly_flags=anomalies or [],
            state_context_required=expected.state_context_required,
            generator_required=expected.generator_required,
            blocked_by_missing_context=blocked_ctx,
            blocked_by_generator=blocked_gen,
            routing_ok=True,
            passed_expectation=passed,
            notes=notes,
        )

    valid, reason = schema_checks.validate(fixture)
    if not valid:
        return build("SCHEMA", "REJECT", notes=reason)

    valid, reason = token_privacy.validate(fixture)
    if not valid:
        return build("TOKEN_PRIVACY", "REJECT", notes=reason)

    valid, reason, ctx_req = time_checks.validate(
        fixture,
        expected_time_context_required=(expected.layer == "TIME" and expected.state_context_required),
        context=context,
    )
    if ctx_req:
        return build("TIME", "STATE_CONTEXT_REQUIRED", notes=reason)
    if not valid:
        return build("TIME", "REJECT", notes=reason)

    valid, reason, ctx_req = state_checks.validate(
        fixture,
        expected_state_context_required=(expected.state_context_required and expected.layer not in {"TIME", "PROFILE"}),
        context=context,
    )
    if ctx_req:
        return build("STATE", "STATE_CONTEXT_REQUIRED", notes=reason)
    if not valid:
        return build("STATE", "REJECT", notes=reason)

    anomalies, _ = anomaly_checks.validate(fixture)
    if "ANOMALY_MODEL_MISMATCH" in anomalies:
        return build("ANOMALY", "VOIDED", anomalies=anomalies, notes="metadata discrepancy")
    if "ANOMALY_FINGERPRINT_DRIFT" in anomalies:
        return build("ANOMALY", "REJECT", anomalies=anomalies, notes="metadata discrepancy")

    valid, reason, ctx_req = bac_checks.validate(fixture, expected, context=context)
    if ctx_req:
        return build("BAC", "STATE_CONTEXT_REQUIRED", notes=reason)
    if not valid:
        return build("BAC", "BAC_BLOCKED", notes=reason)

    valid, reason, gen_req = signature_checks.validate(
        fixture,
        expected_generator_required=expected.generator_required,
        context=context,
    )
    if gen_req:
        return build("SIGNATURE", "GENERATOR_REQUIRED", notes=reason)
    if not valid:
        return build("SIGNATURE", "REJECT", notes=reason)

    return build("COMPLETE", "PASS", notes="No negative condition matched")
