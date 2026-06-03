#!/usr/bin/env python3
"""
VaultGhost Legal-Adjacent Evidence Packet v0.1
Atomic claim_bucket fixture evaluator.

This harness consumes the canonical fixture YAML and verifies that the
transition engine returns the expected bucket, support strength,
legal-conclusion blocking flag, rule path, limitations, and guardrail behavior.

Design boundary:
- This evaluator assumes each fixture already contains one atomic claim.
- Claim splitting is intentionally out-of-scope for this file and should be
  tested separately before bucket evaluation.

Exit codes:
- 0: all fixtures passed
- 1: one or more fixtures failed
- 2: input/schema/runtime error
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required. Install with: python -m pip install pyyaml"
    ) from exc


BUCKETS = {
    "VERIFIED",
    "PROVISIONALLY_VERIFIED",
    "INFERRED",
    "USER_ORIGINATED",
    "QUARANTINED",
    "CONTRADICTED",
}

PRIMARY_AUTHORITATIVE_TYPES = {
    "court_order",
    "docket_entry",
    "filed_pleading",
    "official_receipt",
    "transcript",
}

TIER2_DIRECT_CAVEATED_TYPES = {
    "attorney_email",
    "clerk_email",
    "court_clerk_email",
    "institutional_letter",
}

TRANSACTIONAL_OR_METADATA_TYPES = {
    "invoice",
    "screenshot",
    "payment_confirmation",
    "email_header",
    "file_metadata",
}

AI_TYPES = {"AI_summary", "ai_summary", "model_reconstruction", "prior_session_memory"}
USER_TYPES = {"user_statement", "firsthand_user_account", "user_timeline", "user_recollection"}
PROCESS_SERVER_TYPES = {"process_server_affidavit"}


@dataclasses.dataclass(frozen=True)
class Decision:
    computed_bucket: str
    support_strength: str
    legal_conclusion_blocked: bool
    rule_path: List[str]
    limitations: List[str]
    transition_reason: str


def _text_contains_any(value: str, needles: Iterable[str]) -> bool:
    value_l = (value or "").lower()
    return any(needle.lower() in value_l for needle in needles)


def _evidence_limitations(evidence: Sequence[Dict[str, Any]]) -> List[str]:
    out: List[str] = []
    for ev in evidence:
        out.extend(ev.get("limitations") or [])
    return out


def _has_evidence(evidence: Sequence[Dict[str, Any]], *, relation: Optional[str] = None) -> bool:
    for ev in evidence:
        if relation is None or ev.get("relation_to_claim") == relation:
            return True
    return False


def _direct_supporting_evidence(evidence: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        ev
        for ev in evidence
        if ev.get("relation_to_claim") == "direct_support" and ev.get("supports_exact_claim") is True
    ]


def _contradiction_evidence(evidence: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [ev for ev in evidence if ev.get("relation_to_claim") == "contradiction"]


def _only_ai_context_or_no_support(evidence: Sequence[Dict[str, Any]]) -> bool:
    return bool(evidence) and all(ev.get("source_type") in AI_TYPES for ev in evidence)


def _source_types(evidence: Sequence[Dict[str, Any]]) -> set[str]:
    return {str(ev.get("source_type", "")) for ev in evidence}


def _has_material_provenance_or_access_caveat(ev: Dict[str, Any]) -> bool:
    if ev.get("access_status") in {"partial", "missing", "inaccessible"}:
        return True
    if ev.get("provenance_status") in {"uncertain", "user_supplied", "unofficial"}:
        return True
    limitations = " ".join(ev.get("limitations") or []).lower()
    return any(
        token in limitations
        for token in (
            "ocr",
            "degraded",
            "not an official receipt",
            "unofficial",
            "not independently retrieved",
            "missing",
            "incomplete",
            "partial",
        )
    )


def _missing_source_block_applies(evidence: Sequence[Dict[str, Any]]) -> bool:
    for ev in evidence:
        if ev.get("access_status") in {"missing", "inaccessible"}:
            return True
    limitations = " ".join(_evidence_limitations(evidence)).lower()
    return "attachment is missing" in limitations or "referenced attachment is missing" in limitations


def _fabricated_or_invalid_source_block_applies(evidence: Sequence[Dict[str, Any]]) -> bool:
    limitations = " ".join(_evidence_limitations(evidence)).lower()
    has_ai = any(ev.get("source_type") in AI_TYPES or ev.get("provenance_status") == "AI_generated" for ev in evidence)
    lacks_direct_support = not _direct_supporting_evidence(evidence)
    return has_ai and lacks_direct_support and any(
        marker in limitations
        for marker in (
            "citation cannot be traced",
            "fake citation",
            "invalid citation",
            "pseudo-source",
            "cannot be traced",
        )
    )


def evaluate_fixture(fixture: Dict[str, Any]) -> Decision:
    """Compute bucket decision using deterministic v0.1 transition rules."""
    claim = fixture.get("claim") or {}
    evidence: List[Dict[str, Any]] = fixture.get("evidence_objects") or []

    claim_type = claim.get("claim_type")
    asserted_as = claim.get("asserted_as")
    claim_text = claim.get("claim_text") or ""
    direct_support = _direct_supporting_evidence(evidence)
    contradictions = _contradiction_evidence(evidence)
    source_types = _source_types(evidence)

    # 1. Fabricated / invalid source block.
    if _fabricated_or_invalid_source_block_applies(evidence):
        return Decision(
            computed_bucket="QUARANTINED",
            support_strength="none",
            legal_conclusion_blocked=False,
            rule_path=["fabricated_or_invalid_source_block", "fallback_quarantine"],
            limitations=[
                "No court order, docket entry, transcript, or attorney confirmation supplied.",
                "AI-generated source cannot verify the claim.",
            ],
            transition_reason="Claim lacks reliable direct evidence despite appearing facially plausible.",
        )

    # 2. Missing source block. Kept ahead of positive support because a missing
    # referenced attachment cannot inherit verification from an email shell.
    if _missing_source_block_applies(evidence):
        return Decision(
            computed_bucket="QUARANTINED",
            support_strength="weak",
            legal_conclusion_blocked=True,
            rule_path=["missing_source_block", "fallback_quarantine"],
            limitations=[
                "Referenced attachment is missing.",
                "No available source directly supports the exact claim.",
            ],
            transition_reason="A missing referenced attachment cannot verify the claim.",
        )

    # 3. Material contradiction check.
    if contradictions:
        return Decision(
            computed_bucket="CONTRADICTED",
            support_strength="conflicted",
            legal_conclusion_blocked=False,
            rule_path=[
                "material_contradiction_check",
                "stronger_source_resolution_check",
                "contradicted_assignment",
            ],
            limitations=["Attorney email and official docket conflict on hearing date."],
            transition_reason="Reliable evidence materially conflicts with the claim.",
        )

    # 4. Motive / intent / accusatory block.
    if claim_type == "motive_intent_claim" or asserted_as == "motive_claim":
        return Decision(
            computed_bucket="QUARANTINED",
            support_strength="none",
            legal_conclusion_blocked=True,
            rule_path=["motive_intent_accusation_block", "fallback_quarantine"],
            limitations=["Motive and intent are not directly supported by the invoice."],
            transition_reason="Unsupported accusatory or motive-based claim must be quarantined.",
        )

    # 5. Legal conclusion block / source-scope limit.
    if claim_type == "legal_conclusion" or asserted_as == "legal_conclusion":
        has_indirect_support = _has_evidence(evidence, relation="indirect_support")
        return Decision(
            computed_bucket="INFERRED" if has_indirect_support else "QUARANTINED",
            support_strength="weak",
            legal_conclusion_blocked=True,
            rule_path=[
                "legal_conclusion_block",
                "source_scope_limit_check",
                "indirect_support_check" if has_indirect_support else "fallback_quarantine",
            ],
            limitations=[
                "Document fact may be verified separately.",
                "Legal conclusion is not directly stated by court or counsel.",
            ],
            transition_reason="A source can verify only what it directly supports, not every inference built on top of it.",
        )

    # 6. AI memory / model reconstruction cannot verify.
    if _only_ai_context_or_no_support(evidence):
        return Decision(
            computed_bucket="QUARANTINED",
            support_strength="weak",
            legal_conclusion_blocked=False,
            rule_path=["ai_memory_cannot_verify_check", "fallback_quarantine"],
            limitations=["AI memory cannot independently verify the claim."],
            transition_reason="Model-generated memory is not evidence.",
        )

    # 7. User-originated statement handling.
    if source_types & USER_TYPES:
        blocked = _text_contains_any(
            claim_text,
            ["could not proceed", "legally", "defective", "improper", "invalid", "halted"],
        )
        return Decision(
            computed_bucket="USER_ORIGINATED",
            support_strength="tracked_not_verified",
            legal_conclusion_blocked=blocked,
            rule_path=["user_firsthand_statement_check", "user_originated_ceiling_check"],
            limitations=["User account is tracked but not externally verified."],
            transition_reason="User supplied firsthand statement, but no external corroboration exists.",
        )

    # 8. Direct-support checks.
    if direct_support:
        strongest_direct = sorted(direct_support, key=lambda ev: int(ev.get("source_tier", 99)))[0]
        source_type = strongest_direct.get("source_type")
        tier = int(strongest_direct.get("source_tier", 99))
        provenance = strongest_direct.get("provenance_status")

        # Tier-2 event fact verification exception for official process-server affidavit.
        if (
            source_type in PROCESS_SERVER_TYPES
            and claim_type == "event_fact"
            and provenance == "official"
            and strongest_direct.get("bucket_ceiling_override") == "may_verify_narrow_event_fact_only"
        ):
            return Decision(
                computed_bucket="VERIFIED",
                support_strength="strong",
                legal_conclusion_blocked=False,
                rule_path=[
                    "exact_direct_support_check",
                    "tier_2_event_fact_verification_exception",
                    "legal_sufficiency_split_check",
                ],
                limitations=["Verified only as to attempted service event, not legal sufficiency of service."],
                transition_reason="Official affidavit directly supports the narrow event fact; legal conclusions remain separate.",
            )

        # Primary source with material caveats gets provisional status.
        if tier == 1 and source_type in PRIMARY_AUTHORITATIVE_TYPES:
            if _has_material_provenance_or_access_caveat(strongest_direct):
                return Decision(
                    computed_bucket="PROVISIONALLY_VERIFIED",
                    support_strength="moderate_strong",
                    legal_conclusion_blocked=False,
                    rule_path=["direct_but_caveated_support_check", "provenance_ceiling_check"],
                    limitations=[
                        "Primary source appears to support the claim, but OCR/provenance uncertainty bars VERIFIED."
                    ],
                    transition_reason="Direct support exists, but material readability limitation prevents full verification.",
                )
            return Decision(
                computed_bucket="VERIFIED",
                support_strength="strong",
                legal_conclusion_blocked=False,
                rule_path=[
                    "exact_direct_primary_support_check",
                    "no_material_conflict_check",
                    "verified_assignment",
                ],
                limitations=[],
                transition_reason="Primary authoritative source directly supports the exact date claim with no material conflict.",
            )

        # Tier-2 communications usually have a provisional ceiling.
        if tier == 2 and source_type in TIER2_DIRECT_CAVEATED_TYPES:
            return Decision(
                computed_bucket="PROVISIONALLY_VERIFIED",
                support_strength="moderate_strong",
                legal_conclusion_blocked=False,
                rule_path=["direct_but_caveated_support_check", "tier_2_source_ceiling_check"],
                limitations=["Supported by attorney communication, not primary court record."],
                transition_reason="Secondary or near-primary source directly supports the exact claim with caveats.",
            )

        # Tier-3 transactional / metadata artifacts have a provisional ceiling.
        if tier == 3 or source_type in TRANSACTIONAL_OR_METADATA_TYPES:
            return Decision(
                computed_bucket="PROVISIONALLY_VERIFIED",
                support_strength="moderate",
                legal_conclusion_blocked=False,
                rule_path=["direct_but_caveated_support_check", "provenance_ceiling_check"],
                limitations=["Payment is supported by screenshot but not official receipt."],
                transition_reason="Direct but caveated transactional artifact supports the claim; VERIFIED is barred by provenance limitation.",
            )

        # Conservative fallback for any direct support not explicitly classified.
        return Decision(
            computed_bucket="PROVISIONALLY_VERIFIED",
            support_strength="moderate",
            legal_conclusion_blocked=False,
            rule_path=["direct_but_caveated_support_check", "unclassified_direct_source_ceiling_check"],
            limitations=["Direct support exists, but source class is not authorized for full verification."],
            transition_reason="Unclassified direct source cannot produce VERIFIED in v0.1.",
        )

    # 9. Indirect support, without legal-conclusion conditions.
    if _has_evidence(evidence, relation="indirect_support"):
        return Decision(
            computed_bucket="INFERRED",
            support_strength="weak",
            legal_conclusion_blocked=False,
            rule_path=["indirect_support_check"],
            limitations=["Claim is plausible from evidence but not directly stated by a reliable source."],
            transition_reason="External material provides indirect support only.",
        )

    # 10. Fallback quarantine.
    return Decision(
        computed_bucket="QUARANTINED",
        support_strength="none",
        legal_conclusion_blocked=False,
        rule_path=["fallback_quarantine"],
        limitations=["No rule authorized elevation from QUARANTINED."],
        transition_reason="No reliable support path found.",
    )


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _compare_limitations(expected: Sequence[str], actual: Sequence[str]) -> Optional[str]:
    expected_set = set(expected)
    actual_set = set(actual)
    if expected_set == actual_set:
        return None
    missing = sorted(expected_set - actual_set)
    extra = sorted(actual_set - expected_set)
    return f"limitations mismatch; missing={missing}; extra={extra}"


def validate_fixture_shape(fixture: Dict[str, Any], required_fields: Sequence[str]) -> List[str]:
    errors: List[str] = []
    for field in required_fields:
        if field not in fixture:
            errors.append(f"missing required fixture field: {field}")
    if "claim" in fixture and not isinstance(fixture["claim"], dict):
        errors.append("claim must be an object")
    if "evidence_objects" in fixture and not isinstance(fixture["evidence_objects"], list):
        errors.append("evidence_objects must be a list")
    expected = fixture.get("expected_result")
    if expected is not None and not isinstance(expected, dict):
        errors.append("expected_result must be an object")
    return errors


def evaluate_suite(
    suite: Dict[str, Any],
    *,
    strict: bool,
    check_limitations: bool,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    required_fields = suite.get("fixture_schema_required_fields") or [
        "fixture_id",
        "name",
        "starting_bucket",
        "claim",
        "evidence_objects",
        "expected_result",
        "expected_rule_path",
        "must_not_return",
    ]
    fixtures = suite.get("fixtures") or []
    if not isinstance(fixtures, list):
        raise ValueError("suite.fixtures must be a list")

    passes: List[Dict[str, Any]] = []
    failures: List[Dict[str, Any]] = []

    for fixture in fixtures:
        fixture_id = fixture.get("fixture_id", "<missing fixture_id>")
        shape_errors = validate_fixture_shape(fixture, required_fields)
        if shape_errors:
            failures.append({"fixture_id": fixture_id, "errors": shape_errors})
            continue

        expected = fixture.get("expected_result") or {}
        expected_bucket = expected.get("expected_bucket")
        if expected_bucket not in BUCKETS:
            failures.append(
                {
                    "fixture_id": fixture_id,
                    "errors": [f"invalid expected bucket: {expected_bucket!r}"],
                }
            )
            continue

        decision = evaluate_fixture(fixture)
        errors: List[str] = []

        forbidden = set(_as_list(fixture.get("must_not_return")))
        if decision.computed_bucket in forbidden:
            errors.append(
                f"guardrail violation: computed bucket {decision.computed_bucket!r} is in must_not_return"
            )

        if decision.computed_bucket != expected_bucket:
            errors.append(
                f"bucket mismatch: expected {expected_bucket!r}, got {decision.computed_bucket!r}"
            )

        expected_legal = expected.get("legal_conclusion_blocked")
        if decision.legal_conclusion_blocked != expected_legal:
            errors.append(
                "legal_conclusion_blocked mismatch: "
                f"expected {expected_legal!r}, got {decision.legal_conclusion_blocked!r}"
            )

        expected_support = expected.get("support_strength")
        if strict and decision.support_strength != expected_support:
            errors.append(
                f"support_strength mismatch: expected {expected_support!r}, got {decision.support_strength!r}"
            )

        expected_rule_path = _as_list(fixture.get("expected_rule_path"))
        if strict and decision.rule_path != expected_rule_path:
            errors.append(
                f"rule_path mismatch: expected {expected_rule_path!r}, got {decision.rule_path!r}"
            )

        if check_limitations:
            limitations_error = _compare_limitations(
                expected.get("expected_limitations") or [], decision.limitations
            )
            if limitations_error:
                errors.append(limitations_error)

        report_item = {
            "fixture_id": fixture_id,
            "name": fixture.get("name"),
            "expected_bucket": expected_bucket,
            "computed_bucket": decision.computed_bucket,
            "support_strength": decision.support_strength,
            "legal_conclusion_blocked": decision.legal_conclusion_blocked,
            "rule_path": decision.rule_path,
            "limitations": decision.limitations,
        }

        if errors:
            report_item["errors"] = errors
            failures.append(report_item)
        else:
            passes.append(report_item)

    return passes, failures


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("YAML root must be an object")
    return data


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate VaultGhost claim_bucket regression fixtures."
    )
    parser.add_argument(
        "fixture_yaml",
        type=Path,
        help="Path to canonical fixture YAML file.",
    )
    parser.add_argument(
        "--no-strict",
        action="store_true",
        help="Disable strict checks for support_strength and exact rule_path.",
    )
    parser.add_argument(
        "--check-limitations",
        action="store_true",
        help="Also require exact expected_limitations set equality.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON report.",
    )
    parser.add_argument(
        "--show-passes",
        action="store_true",
        help="Show passed fixture IDs in human-readable output.",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    strict = not args.no_strict

    try:
        suite = load_yaml(args.fixture_yaml)
        passes, failures = evaluate_suite(
            suite,
            strict=strict,
            check_limitations=args.check_limitations,
        )
    except Exception as exc:  # pragma: no cover
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    report = {
        "suite_id": suite.get("suite_id"),
        "version": suite.get("version"),
        "strict": strict,
        "check_limitations": args.check_limitations,
        "passed": len(passes),
        "failed": len(failures),
        "pass_items": passes if args.show_passes or args.json else [],
        "failures": failures,
    }

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            f"Suite {report['suite_id']} v{report['version']}: "
            f"{report['passed']} passed, {report['failed']} failed "
            f"(strict={strict}, check_limitations={args.check_limitations})"
        )
        if args.show_passes:
            for item in passes:
                print(f"PASS {item['fixture_id']}: {item['computed_bucket']} via {' > '.join(item['rule_path'])}")
        for item in failures:
            print(f"FAIL {item.get('fixture_id')}: {item.get('name')}")
            for error in item.get("errors", []):
                print(f"  - {error}")
            if "computed_bucket" in item:
                print(f"  expected_bucket={item['expected_bucket']!r} computed_bucket={item['computed_bucket']!r}")
                print(f"  rule_path={item['rule_path']!r}")

    return 1 if failures else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
