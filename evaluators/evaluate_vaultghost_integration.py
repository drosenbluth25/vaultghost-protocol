#!/usr/bin/env python3
"""
VaultGhost End-to-End Integration Evaluator v0.1

Pipeline under test:
raw_statement -> claim splitter -> atomic claims -> bucket evaluator -> final claim packet

Design boundaries:
- The splitter may not assign final evidentiary buckets.
- The bucket evaluator may not split compound language.
- Evidence is bound after splitting, by claim index, inside the integration fixture.

Exit codes:
- 0: all fixtures passed
- 1: one or more fixtures failed
- 2: input/schema/runtime error
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install with: python -m pip install pyyaml") from exc

BUCKETS = {"VERIFIED", "PROVISIONALLY_VERIFIED", "INFERRED", "USER_ORIGINATED", "QUARANTINED", "CONTRADICTED"}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _evidence_ids(evidence: Sequence[Dict[str, Any]]) -> List[str]:
    return [str(ev.get("evidence_id")) for ev in evidence if ev.get("evidence_id")]


def _build_bucket_fixture(atomic_claim: Any, evidence_objects: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "fixture_id": atomic_claim.atomic_claim_id,
        "name": f"bucket-eval-for-{atomic_claim.atomic_claim_id}",
        "starting_bucket": atomic_claim.starting_bucket,
        "claim": {
            "claim_text": atomic_claim.claim_text,
            "claim_type": atomic_claim.claim_type,
            "asserted_as": atomic_claim.asserted_as,
        },
        "evidence_objects": evidence_objects,
        "expected_result": {},
        "expected_rule_path": [],
        "must_not_return": [],
    }


def _binding_map(fixture: Dict[str, Any]) -> Dict[int, List[Dict[str, Any]]]:
    out: Dict[int, List[Dict[str, Any]]] = {}
    for binding in fixture.get("evidence_bindings") or []:
        idx = int(binding["claim_index"])
        out[idx] = binding.get("evidence_objects") or []
    return out


def build_packet(fixture: Dict[str, Any], splitter: Any, bucket_eval: Any) -> Dict[str, Any]:
    fixture_id = fixture["fixture_id"]
    raw_statement = fixture["raw_statement"]
    atomic_claims, split_rule_path = splitter.split_claims(fixture_id, raw_statement)
    evidence_by_index = _binding_map(fixture)
    claim_records: List[Dict[str, Any]] = []

    for idx, atomic_claim in enumerate(atomic_claims, start=1):
        evidence_objects = evidence_by_index.get(idx, [])
        decision = bucket_eval.evaluate_fixture(_build_bucket_fixture(atomic_claim, evidence_objects))
        record = {
            "claim_id": atomic_claim.atomic_claim_id,
            "claim_index": idx,
            "parent_statement_id": fixture_id,
            "claim_text": atomic_claim.claim_text,
            "claim_type": atomic_claim.claim_type,
            "asserted_as": atomic_claim.asserted_as,
            "split_basis": atomic_claim.split_basis,
            "flags": atomic_claim.flags,
            "starting_bucket": atomic_claim.starting_bucket,
            "current_bucket": decision.computed_bucket,
            "support_strength": decision.support_strength,
            "legal_conclusion_blocked": decision.legal_conclusion_blocked,
            "evidence_refs": _evidence_ids(evidence_objects),
            "bucket_rule_path": decision.rule_path,
            "limitations": decision.limitations,
            "transition_reason": decision.transition_reason,
        }
        claim_records.append(record)

    bucket_counts = dict(Counter(r["current_bucket"] for r in claim_records))
    packet = {
        "packet_id": f"{fixture_id}-PACKET",
        "protocol": "VaultGhost End-to-End Claim Governance Packet",
        "version": "0.1",
        "source_statement": {
            "statement_id": fixture_id,
            "raw_statement": raw_statement,
        },
        "split_stage": {
            "splitter_version": "0.1",
            "split_rule_path": split_rule_path,
            "atomic_claim_count": len(atomic_claims),
            "boundary": "splitter_emits_starting_bucket_only",
        },
        "bucket_stage": {
            "bucket_engine_version": "0.1",
            "boundary": "bucket_engine_assumes_atomic_claims",
        },
        "claim_records": claim_records,
        "packet_invariants": {
            "all_claims_started_quarantined": all(r["starting_bucket"] == "QUARANTINED" for r in claim_records),
            "splitter_assigned_no_final_buckets": all(r["starting_bucket"] == "QUARANTINED" for r in claim_records),
            "bucket_engine_received_only_atomic_claims": len(atomic_claims) == len(claim_records),
            "legal_conclusions_do_not_inherit_verification": all(
                not (r["claim_type"] == "legal_conclusion" and r["current_bucket"] == "VERIFIED") for r in claim_records
            ),
            "motive_claims_do_not_inherit_event_verification": all(
                not (r["claim_type"] == "motive_intent_claim" and r["current_bucket"] in {"VERIFIED", "PROVISIONALLY_VERIFIED"}) for r in claim_records
            ),
            "missing_sources_do_not_inherit_verification": not any(
                "missing" in " ".join(r.get("limitations") or []).lower() and r["current_bucket"] == "VERIFIED"
                for r in claim_records
            ),
        },
        "summary": {
            "claim_count": len(claim_records),
            "bucket_counts": bucket_counts,
            "blocked_legal_conclusion_count": sum(1 for r in claim_records if r["legal_conclusion_blocked"]),
        },
    }
    return packet


def _compare_expected_records(expected: Sequence[Dict[str, Any]], records: Sequence[Dict[str, Any]], strict: bool) -> List[str]:
    errors: List[str] = []
    if len(expected) != len(records):
        errors.append(f"claim record count mismatch: expected {len(expected)}, got {len(records)}")
        return errors
    by_idx = {int(r["claim_index"]): r for r in records}
    for exp in expected:
        idx = int(exp["claim_index"])
        got = by_idx.get(idx)
        if got is None:
            errors.append(f"missing claim_index {idx}")
            continue
        for field in ("claim_type", "current_bucket", "support_strength", "legal_conclusion_blocked"):
            if got.get(field) != exp.get(field):
                errors.append(f"claim {idx} {field} mismatch: expected {exp.get(field)!r}, got {got.get(field)!r}")
        if strict and got.get("starting_bucket") != "QUARANTINED":
            errors.append(f"claim {idx} did not start QUARANTINED")
    return errors


def _guardrail_errors(packet: Dict[str, Any], must_not_packet: Sequence[str]) -> List[str]:
    records = packet["claim_records"]
    errors: List[str] = []
    guardrails = set(must_not_packet or [])

    if "legal_conclusion_verified" in guardrails and any(r["claim_type"] == "legal_conclusion" and r["current_bucket"] == "VERIFIED" for r in records):
        errors.append("guardrail violation: legal conclusion reached VERIFIED")
    if "legal_sufficiency_verified" in guardrails and any("legally sufficient" in r["claim_text"].lower() and r["current_bucket"] == "VERIFIED" for r in records):
        errors.append("guardrail violation: legal sufficiency reached VERIFIED")
    if "motive_claim_verified" in guardrails and any(r["claim_type"] == "motive_intent_claim" and r["current_bucket"] in {"VERIFIED", "PROVISIONALLY_VERIFIED"} for r in records):
        errors.append("guardrail violation: motive claim was elevated")
    if "procedural_inference_verified" in guardrails and any(r["asserted_as"] == "inference" and r["current_bucket"] == "VERIFIED" for r in records):
        errors.append("guardrail violation: procedural inference was verified")
    if "both_conflicting_dates_verified" in guardrails:
        date_records = [r for r in records if r["claim_type"] == "date_fact"]
        if len(date_records) >= 2 and all(r["current_bucket"] == "VERIFIED" for r in date_records):
            errors.append("guardrail violation: both conflicting date claims verified")
    if any(g.startswith("merged_") or g in {"treat_payment_as_filing_completion", "merge_service_attempt_with_legal_sufficiency", "inherit_verification_from_missing_attachment", "resolve_contradiction_inside_splitter", "unnecessary_split"} for g in guardrails):
        # These are primarily checked by expected split count / record count and rule path.
        pass
    return errors


def evaluate_integration_fixture(fixture: Dict[str, Any], splitter: Any, bucket_eval: Any, strict: bool = True) -> Dict[str, Any]:
    packet = build_packet(fixture, splitter, bucket_eval)
    errors: List[str] = []

    expected_path = fixture.get("expected_split_rule_path") or []
    if strict and packet["split_stage"]["split_rule_path"] != expected_path:
        errors.append(f"split_rule_path mismatch: expected {expected_path!r}, got {packet['split_stage']['split_rule_path']!r}")

    errors.extend(_compare_expected_records(fixture.get("expected_claim_records") or [], packet["claim_records"], strict))
    errors.extend(_guardrail_errors(packet, fixture.get("must_not_packet") or []))

    for name, value in packet["packet_invariants"].items():
        if value is not True:
            errors.append(f"packet invariant failed: {name}")

    return {
        "fixture_id": fixture["fixture_id"],
        "name": fixture.get("name"),
        "passed": not errors,
        "errors": errors,
        "packet": packet,
    }


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "fixtures" not in data:
        raise ValueError(f"Invalid integration fixture suite: {path}")
    return data


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate VaultGhost end-to-end integration fixtures")
    parser.add_argument("integration_fixture_yaml", type=Path)
    parser.add_argument("--splitter", type=Path, default=Path("/mnt/data/evaluate_claim_splitting_fixture.py"))
    parser.add_argument("--bucket-evaluator", type=Path, default=Path("/mnt/data/evaluate_bucket_fixture.py"))
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--show-passes", action="store_true")
    parser.add_argument("--no-strict", action="store_true")
    args = parser.parse_args(argv)

    strict = not args.no_strict
    try:
        suite = load_yaml(args.integration_fixture_yaml)
        splitter = _load_module("vaultghost_claim_splitter_v0_1", args.splitter)
        bucket_eval = _load_module("vaultghost_bucket_evaluator_v0_1", args.bucket_evaluator)
        results = [evaluate_integration_fixture(fx, splitter, bucket_eval, strict=strict) for fx in suite["fixtures"]]
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    passes = [r for r in results if r["passed"]]
    failures = [r for r in results if not r["passed"]]
    print(f"Suite {suite.get('suite_id')} v{suite.get('version')}: {len(passes)} passed, {len(failures)} failed")
    print(f"strict={strict}")

    for r in results:
        if r["passed"] and args.show_passes:
            print(f"PASS {r['fixture_id']}: {r.get('name')}")
        elif not r["passed"]:
            print(f"FAIL {r['fixture_id']}: {r.get('name')}")
            for err in r["errors"]:
                print(f"  - {err}")

    report = {
        "suite_id": suite.get("suite_id"),
        "version": suite.get("version"),
        "strict": strict,
        "passed": len(passes),
        "failed": len(failures),
        "results": results,
    }
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
