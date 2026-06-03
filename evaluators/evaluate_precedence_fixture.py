#!/usr/bin/env python3
from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required. Install with: python -m pip install pyyaml") from exc

BUCKETS = {"VERIFIED", "PROVISIONALLY_VERIFIED", "INFERRED", "USER_ORIGINATED", "QUARANTINED", "CONTRADICTED"}
PRIMARY_AUTHORITATIVE_TYPES = {"court_order", "docket_entry", "filed_pleading", "official_receipt", "transcript"}
TIER2_COMMUNICATION_TYPES = {"attorney_email", "clerk_email", "court_clerk_email", "institutional_letter"}
TRANSACTIONAL_TYPES = {"invoice", "screenshot", "payment_confirmation", "email_header", "file_metadata"}
USER_TYPES = {"user_statement", "firsthand_user_account", "user_timeline", "user_recollection"}
AI_TYPES = {"AI_summary", "ai_summary", "model_reconstruction", "prior_session_memory"}
PROCESS_SERVER_TYPES = {"process_server_affidavit"}
LEGAL_SUBSTANCE_MARKERS = ("legally defective", "legal defect", "legal sufficiency", "legally sufficient", "invalidated", "void", "defective service", "service defect", "court lacked")
MOTIVE_MARKERS = ("to pressure", "as a trick", "intended to", "in order to force", "motive", "intent")

@dataclasses.dataclass(frozen=True)
class Decision:
    computed_bucket: str
    support_strength: str
    legal_conclusion_blocked: bool
    rule_path: List[str]
    limitations: List[str]
    transition_reason: str

def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]

def _source_types(evidence: Sequence[Dict[str, Any]]) -> set[str]:
    return {str(ev.get("source_type", "")) for ev in evidence}

def _direct_support(evidence: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [ev for ev in evidence if ev.get("relation_to_claim") == "direct_support" and ev.get("supports_exact_claim") is True]

def _indirect_support(evidence: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [ev for ev in evidence if ev.get("relation_to_claim") == "indirect_support"]

def _contradictions(evidence: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [ev for ev in evidence if ev.get("relation_to_claim") == "contradiction"]

def _all_limitations(evidence: Sequence[Dict[str, Any]]) -> str:
    return " ".join(lim for ev in evidence for lim in (ev.get("limitations") or [])).lower()

def _has_missing_source(evidence: Sequence[Dict[str, Any]]) -> bool:
    if any(ev.get("access_status") in {"missing", "inaccessible"} for ev in evidence):
        return True
    text = _all_limitations(evidence)
    return "missing" in text and ("attachment" in text or "docket" in text or "referenced" in text)

def _has_provenance_caveat(ev: Dict[str, Any]) -> bool:
    if ev.get("access_status") in {"partial", "missing", "inaccessible"}:
        return True
    if ev.get("provenance_status") in {"uncertain", "unofficial"}:
        return True
    text = " ".join(ev.get("limitations") or []).lower()
    return any(token in text for token in ("ocr", "uncertain", "degraded", "partial", "unofficial"))

def _is_explicit_motive_or_intent(claim: Dict[str, Any]) -> bool:
    text = (claim.get("claim_text") or "").lower()
    return claim.get("claim_type") == "motive_intent_claim" or claim.get("asserted_as") == "motive_claim" or any(marker in text for marker in MOTIVE_MARKERS)

def _is_legal_substance(claim: Dict[str, Any]) -> bool:
    text = (claim.get("claim_text") or "").lower()
    return claim.get("claim_type") == "legal_conclusion" or claim.get("asserted_as") == "legal_conclusion" or any(marker in text for marker in LEGAL_SUBSTANCE_MARKERS)

def _strongest_direct(evidence: Sequence[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    direct = _direct_support(evidence)
    return sorted(direct, key=lambda ev: int(ev.get("source_tier", 99)))[0] if direct else None

def _has_ai_context(evidence: Sequence[Dict[str, Any]]) -> bool:
    return any(ev.get("source_type") in AI_TYPES or ev.get("provenance_status") == "AI_generated" for ev in evidence)

def evaluate_fixture(fixture: Dict[str, Any]) -> Decision:
    claim = fixture.get("claim") or {}
    evidence = fixture.get("evidence_objects") or []
    manual = fixture.get("manual_override") or {}
    indirect = _indirect_support(evidence)
    contradiction = _contradictions(evidence)
    source_types = _source_types(evidence)

    if manual.get("requested_bucket") == "VERIFIED":
        if source_types & USER_TYPES and not any(int(ev.get("source_tier", 99)) == 1 for ev in _direct_support(evidence)):
            return Decision("USER_ORIGINATED", "tracked_not_verified", True, ["manual_override_validation_check", "verified_override_denied", "user_firsthand_statement_check", "user_originated_ceiling_check"], ["Manual override cannot mark VERIFIED without reliable direct evidence."], "Manual override is rejected; user statement remains user-originated.")

    if _has_missing_source(evidence):
        return Decision("QUARANTINED", "weak", True, ["missing_source_block", "missing_primary_source_outranks_context", "fallback_quarantine"], ["Missing referenced primary source cannot verify the claim."], "Missing source block outranks tier-2 contextual support.")

    if contradiction:
        tiers = [int(ev.get("source_tier", 99)) for ev in evidence]
        if tiers.count(1) >= 2:
            return Decision("CONTRADICTED", "conflicted", False, ["material_contradiction_check", "equal_authoritative_conflict_check", "contradicted_assignment"], ["Equal-tier authoritative evidence conflicts on the procedural status."], "Equal authoritative contradiction prevents verification.")
        return Decision("CONTRADICTED", "conflicted", False, ["material_contradiction_check", "contradiction_outranks_positive_support", "contradicted_assignment"], ["Direct support exists, but reliable stronger evidence materially conflicts with the claim."], "Material contradiction outranks positive support.")

    # Explicit motive/intent outranks generic legal-substance markers.
    if _is_explicit_motive_or_intent(claim):
        return Decision("QUARANTINED", "none", True, ["motive_intent_accusation_block", "source_scope_limit_check", "fallback_quarantine"], ["Real filing establishes existence of filing only, not motive or intent."], "Motive claim cannot inherit verification from real filing.")

    if _is_legal_substance(claim):
        if claim.get("claim_type") != "legal_conclusion" and claim.get("asserted_as") == "fact":
            return Decision("QUARANTINED", "weak", True, ["legal_substance_detection_check", "legal_conclusion_asserted_as_fact_block", "fallback_quarantine"], ["Claim is substantively a legal conclusion despite procedural phrasing."], "Legal-substance detector blocks verification when legal conclusion is asserted as fact.")
        if any(ev.get("source_type") in PROCESS_SERVER_TYPES for ev in evidence):
            return Decision("INFERRED", "weak", True, ["legal_conclusion_block", "tier_2_event_exception_scope_check", "indirect_support_check"], ["Tier-2 event exception does not extend to legal sufficiency conclusions."], "Official affidavit may support event fact only; legal sufficiency remains blocked.")
        return Decision("INFERRED" if indirect else "QUARANTINED", "weak", True, ["legal_conclusion_block", "source_scope_limit_check", "indirect_support_check" if indirect else "fallback_quarantine"], ["Court order may support a document fact, but the legal conclusion is only indirectly supported and OCR-caveated."], "Legal conclusion block prevents inherited verification from damaged document.")

    if source_types & USER_TYPES:
        if indirect:
            return Decision("INFERRED", "weak", True, ["user_corroboration_check", "indirect_support_present", "inferred_assignment"], ["External material weakly corroborates plausibility but does not directly verify the exact claim."], "User-originated claim with indirect corroboration upgrades only to INFERRED.")
        return Decision("USER_ORIGINATED", "tracked_not_verified", False, ["user_firsthand_statement_check", "user_originated_ceiling_check"], ["User account is tracked but not externally verified."], "User supplied firsthand statement, but no external corroboration exists.")

    strongest = _strongest_direct(evidence)
    if strongest:
        source_type = strongest.get("source_type")
        tier = int(strongest.get("source_tier", 99))
        ai_prefix = ["ai_context_disregarded_for_verification"] if _has_ai_context(evidence) else []

        if tier == 1 and source_type in PRIMARY_AUTHORITATIVE_TYPES:
            if _has_provenance_caveat(strongest):
                return Decision("PROVISIONALLY_VERIFIED", "moderate_strong", False, ["direct_support_check", "primary_source_caveat_check", "provenance_ceiling_check", "provisionally_verified_assignment"], ["Primary source appears to support the claim, but provenance/OCR uncertainty bars VERIFIED."], "Provenance ceiling outranks primary-source status.")
            if ai_prefix:
                return Decision("VERIFIED", "strong", False, ["ai_context_disregarded_for_verification", "direct_support_check", "exact_direct_primary_support_check", "verified_assignment"], [], "AI memory does not verify the claim, but official direct evidence independently does.")
            return Decision("VERIFIED", "strong", False, ["direct_support_check", "strongest_source_resolution_check", "exact_direct_primary_support_check", "verified_assignment"], [], "Strongest direct official source satisfies verification standard.")

        if source_type in PROCESS_SERVER_TYPES and strongest.get("bucket_ceiling_override") == "may_verify_narrow_event_fact_only":
            return Decision("VERIFIED", "strong", False, ["direct_support_check", "tier_2_event_fact_verification_exception", "verified_assignment"], ["Verified only as to narrow event fact."], "Process-server affidavit exception applies only to event fact.")

        if tier == 2 or source_type in TIER2_COMMUNICATION_TYPES:
            return Decision("PROVISIONALLY_VERIFIED", "moderate_strong", False, ["direct_support_check", "tier_2_source_ceiling_check", "provisionally_verified_assignment"], ["Tier-2 source directly supports the claim but does not authorize full verification."], "Tier-2 source has provisional ceiling.")

        if tier == 3 or source_type in TRANSACTIONAL_TYPES:
            return Decision("PROVISIONALLY_VERIFIED", "moderate", False, ["direct_support_check", "transactional_source_ceiling_check", "provisionally_verified_assignment"], ["Transactional artifact directly supports the claim but has provisional ceiling."], "Tier-3 source has provisional ceiling.")

    if indirect:
        return Decision("INFERRED", "weak", False, ["indirect_support_check", "inferred_assignment"], ["Claim is indirectly supported only."], "Indirect support cannot verify exact claim.")

    return Decision("QUARANTINED", "none", False, ["fallback_quarantine"], ["No rule authorized elevation from QUARANTINED."], "No reliable support path found.")

def validate_fixture_shape(fixture: Dict[str, Any], required_fields: Sequence[str]) -> List[str]:
    errors = []
    for field in required_fields:
        if field not in fixture:
            errors.append(f"missing required fixture field: {field}")
    if "claim" in fixture and not isinstance(fixture["claim"], dict):
        errors.append("claim must be an object")
    if "evidence_objects" in fixture and not isinstance(fixture["evidence_objects"], list):
        errors.append("evidence_objects must be a list")
    if "expected_result" in fixture and not isinstance(fixture["expected_result"], dict):
        errors.append("expected_result must be an object")
    return errors

def _compare_limitations(expected: Sequence[str], actual: Sequence[str]) -> Optional[str]:
    expected_set, actual_set = set(expected), set(actual)
    if expected_set == actual_set:
        return None
    return f"limitations mismatch; missing={sorted(expected_set - actual_set)}; extra={sorted(actual_set - expected_set)}"

def evaluate_suite(suite: Dict[str, Any], *, strict: bool, check_limitations: bool) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    required = suite.get("fixture_schema_required_fields") or ["fixture_id", "name", "starting_bucket", "claim", "evidence_objects", "expected_result", "expected_rule_path", "must_not_return"]
    passes, failures = [], []
    for fixture in suite.get("fixtures") or []:
        fixture_id = fixture.get("fixture_id", "<missing fixture_id>")
        shape_errors = validate_fixture_shape(fixture, required)
        if shape_errors:
            failures.append({"fixture_id": fixture_id, "errors": shape_errors})
            continue
        expected = fixture.get("expected_result") or {}
        decision = evaluate_fixture(fixture)
        errors = []
        expected_bucket = expected.get("expected_bucket")
        if expected_bucket not in BUCKETS:
            errors.append(f"invalid expected_bucket: {expected_bucket!r}")
        elif decision.computed_bucket != expected_bucket:
            errors.append(f"bucket mismatch: expected {expected_bucket!r}, got {decision.computed_bucket!r}")
        if decision.computed_bucket in set(_as_list(fixture.get("must_not_return"))):
            errors.append(f"guardrail violation: computed bucket {decision.computed_bucket!r} is forbidden")
        if decision.legal_conclusion_blocked != expected.get("legal_conclusion_blocked"):
            errors.append(f"legal_conclusion_blocked mismatch: expected {expected.get('legal_conclusion_blocked')!r}, got {decision.legal_conclusion_blocked!r}")
        if strict and decision.support_strength != expected.get("support_strength"):
            errors.append(f"support_strength mismatch: expected {expected.get('support_strength')!r}, got {decision.support_strength!r}")
        if strict and decision.rule_path != _as_list(fixture.get("expected_rule_path")):
            errors.append(f"rule_path mismatch: expected {_as_list(fixture.get('expected_rule_path'))!r}, got {decision.rule_path!r}")
        if check_limitations:
            lim_error = _compare_limitations(expected.get("expected_limitations") or [], decision.limitations)
            if lim_error:
                errors.append(lim_error)
        report = {
            "fixture_id": fixture_id,
            "name": fixture.get("name"),
            "collision_type": fixture.get("collision_type"),
            "expected_bucket": expected_bucket,
            "computed_bucket": decision.computed_bucket,
            "support_strength": decision.support_strength,
            "legal_conclusion_blocked": decision.legal_conclusion_blocked,
            "rule_path": decision.rule_path,
            "limitations": decision.limitations,
            "transition_reason": decision.transition_reason,
        }
        if errors:
            report["errors"] = errors
            failures.append(report)
        else:
            passes.append(report)
    return passes, failures

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate VaultGhost v0.1 precedence fixtures.")
    parser.add_argument("fixture_yaml", type=Path)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--no-strict", action="store_true")
    parser.add_argument("--check-limitations", action="store_true")
    parser.add_argument("--show-passes", action="store_true")
    args = parser.parse_args(argv)

    try:
        suite = yaml.safe_load(args.fixture_yaml.read_text(encoding="utf-8"))
        passes, failures = evaluate_suite(suite, strict=not args.no_strict, check_limitations=args.check_limitations)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    report = {
        "suite_id": suite.get("suite_id"),
        "version": suite.get("version"),
        "strict": not args.no_strict,
        "check_limitations": args.check_limitations,
        "total": len(passes) + len(failures),
        "passed": len(passes),
        "failed": len(failures),
        "passes": passes,
        "failures": failures,
    }
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.show_passes:
        for item in passes:
            print(f"PASS {item['fixture_id']} {item['computed_bucket']} :: {item['name']}")
    for item in failures:
        print(f"FAIL {item['fixture_id']} :: {item.get('name')}", file=sys.stderr)
        for err in item.get("errors", []):
            print(f"  - {err}", file=sys.stderr)
    print(f"Suite {report['suite_id']} v{report['version']}: {report['passed']} passed, {report['failed']} failed; strict={report['strict']} check_limitations={report['check_limitations']}")
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
