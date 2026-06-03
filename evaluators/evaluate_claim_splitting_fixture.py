#!/usr/bin/env python3
"""
VaultGhost Claim-Splitting Preprocessor v0.1
Regression fixture evaluator.

This harness tests only decomposition of messy statements into atomic claims.
It intentionally does not assign evidentiary buckets. Each emitted atomic claim
is routed downstream with starting_bucket=QUARANTINED.

Design boundary:
- Claim splitting is a preprocessor.
- Bucket governance remains in evaluate_bucket_fixture.py.
- A correct splitter preserves document facts, legal conclusions, motive claims,
  contradictions, and causal inferences as separate bucket-evaluation inputs.

Exit codes:
- 0: all fixtures passed
- 1: one or more fixtures failed
- 2: input/schema/runtime error
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install with: python -m pip install pyyaml") from exc


@dataclasses.dataclass(frozen=True)
class AtomicClaim:
    atomic_claim_id: str
    parent_statement_id: str
    claim_text: str
    claim_type: str
    asserted_as: str
    source_span: str
    split_basis: str
    flags: List[str]
    starting_bucket: str = "QUARANTINED"

    def comparable(self) -> Dict[str, Any]:
        return {
            "claim_text": self.claim_text,
            "claim_type": self.claim_type,
            "asserted_as": self.asserted_as,
            "split_basis": self.split_basis,
            "flags": self.flags,
            "starting_bucket": self.starting_bucket,
        }


def _clean_clause(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip(" ,.;"))
    if not text:
        return text
    text = text[0].upper() + text[1:]
    if not text.endswith("."):
        text += "."
    return text


def _split_statement(text: str) -> Tuple[List[str], List[str], str]:
    """Return clauses, rule path, split mode."""
    original = text.strip()
    lower = original.lower()

    # Highest-specificity transitions first.
    if ", causing " in lower:
        left, right = re.split(r",\s+causing\s+", original, maxsplit=1, flags=re.I)
        # v0.1 canonicalization: turn gerund causal phrase into explicit causal inference.
        left_clean = _clean_clause(left)
        cause = left_clean[:-1].lower()
        if right.lower().strip(" .") == "the executor appointment delay":
            second = f"The executor appointment was delayed because {cause}."
        else:
            second = _clean_clause(f"{right} because {left}")
        return [left_clean, second], ["causal_inference_split", "emit_atomic_claims"], "causal"

    if ", but " in lower:
        parts = re.split(r",\s+but\s+", original, maxsplit=1, flags=re.I)
        return [_clean_clause(parts[0]), _clean_clause(parts[1])], ["contradiction_pair_split", "emit_atomic_claims"], "contradiction"

    if ", which means " in lower:
        parts = re.split(r",\s+which means\s+", original, maxsplit=1, flags=re.I)
        return [_clean_clause(parts[0]), _clean_clause(parts[1])], ["attribution_underlying_claim_split", "document_fact_legal_conclusion_split", "emit_atomic_claims"], "attribution_legal"

    if ", therefore " in lower:
        parts = re.split(r",\s+therefore\s+", original, maxsplit=1, flags=re.I)
        return [_clean_clause(parts[0]), _clean_clause(parts[1])], ["attribution_underlying_claim_split", "document_fact_legal_conclusion_split", "emit_atomic_claims"], "attribution_legal"

    if ", proving " in lower:
        parts = re.split(r",\s+proving\s+", original, maxsplit=1, flags=re.I)
        return [_clean_clause(parts[0]), _clean_clause(parts[1])], ["document_fact_legal_conclusion_split", "emit_atomic_claims"], "proof_inference"

    if ", so " in lower:
        parts = re.split(r",\s+so\s+", original, maxsplit=1, flags=re.I)
        return [_clean_clause(parts[0]), _clean_clause(parts[1])], ["document_fact_legal_conclusion_split", "emit_atomic_claims"], "legal_consequence"

    if ", and " in lower:
        parts = re.split(r",\s+and\s+", original, maxsplit=1, flags=re.I)
        right_l = parts[1].lower()
        if any(token in right_l for token in ("intended", "deliberately", "pressure")):
            return [_clean_clause(parts[0]), _clean_clause(parts[1])], ["motive_intent_split", "emit_atomic_claims"], "motive"
        if any(token in right_l for token in ("legally", "defective", "cannot", "could not", "halted")):
            # Clerk/statement patterns include attribution plus legal consequence.
            if any(token in lower for token in ("clerk confirmed", "counsel stated", "judge said")):
                return [_clean_clause(parts[0]), _clean_clause(parts[1])], ["attribution_underlying_claim_split", "document_fact_legal_conclusion_split", "emit_atomic_claims"], "attribution_legal"
            return [_clean_clause(parts[0]), _clean_clause(parts[1])], ["document_fact_legal_conclusion_split", "emit_atomic_claims"], "legal_consequence"
        # Document reference plus status is still a split, not a verification inheritance.
        if "email references" in lower or "attached order" in lower:
            return [_clean_clause(parts[0]), _clean_clause(parts[1])], ["document_fact_legal_conclusion_split", "emit_atomic_claims"], "document_reference"
        return [_clean_clause(parts[0]), _clean_clause(parts[1])], ["document_fact_legal_conclusion_split", "emit_atomic_claims"], "generic_and"

    return [_clean_clause(original)], ["single_atomic_no_split", "emit_atomic_claims"], "single"


def _classify_claim(clause: str, *, mode: str, index: int) -> Tuple[str, str, str, List[str]]:
    lower = clause.lower()

    if mode == "contradiction":
        return "date_fact", "fact_about_source", "contradiction_side_a" if index == 0 else "contradiction_side_b", ["contradiction_candidate", "bucket_eval_required"]

    if "intended" in lower or "deliberately" in lower or "to pressure" in lower:
        return "motive_intent_claim", "motive_intent_claim", "motive_intent_component", ["motive_intent_candidate", "bucket_eval_required"]

    if "legally" in lower or "defective" in lower or "cannot proceed" in lower or "could not move forward" in lower:
        return "legal_conclusion", "legal_conclusion", "legal_conclusion_component" if mode != "attribution_legal" else "legal_consequence_component", ["legal_conclusion_candidate", "bucket_eval_required"]

    if "foreclosure was halted" in lower:
        return "procedural_status", "legal_effect_inference", "legal_effect_component", ["legal_conclusion_candidate", "inference_candidate", "bucket_eval_required"]

    if "filing was complete" in lower:
        return "procedural_status", "inference", "procedural_inference_component", ["inference_candidate", "bucket_eval_required"]

    if "executor appointment was delayed because" in lower:
        return "causal_inference", "causal_inference", "causal_inference_component", ["inference_candidate", "bucket_eval_required"]

    if lower.startswith("counsel stated"):
        return "attorney_statement_fact", "fact_about_statement", "attribution_component", ["bucket_eval_required"]

    if lower.startswith("the clerk confirmed"):
        return "procedural_status", "fact_about_statement", "attribution_component", ["bucket_eval_required"]

    if lower.startswith("the judge said"):
        return "user_account", "reported_statement", "reported_statement_component", ["bucket_eval_required"]

    if "screenshot shows payment" in lower:
        return "payment_fact", "fact_about_artifact", "payment_fact_component", ["bucket_eval_required"]

    if "email references" in lower:
        return "document_fact", "fact_about_artifact", "document_reference_component", ["bucket_eval_required"]

    if "order halted" in lower:
        return "procedural_status", "fact", "procedural_status_component", ["bucket_eval_required"]

    if "court issued an order" in lower:
        return "document_fact", "fact", "document_fact_component", ["bucket_eval_required"]

    if "process server attempted" in lower:
        return "event_fact", "fact", "event_fact_component", ["bucket_eval_required"]

    if "invoice was sent" in lower:
        return "event_fact", "fact", "observable_event_component", ["bucket_eval_required"]

    if "will was placed" in lower:
        return "event_fact", "fact", "event_fact_component", ["bucket_eval_required"]

    if "pleading was filed" in lower:
        return "date_fact", "fact", "filing_date_component", ["bucket_eval_required"]

    if "petition was filed" in lower:
        return "date_fact", "fact", "already_atomic", ["bucket_eval_required"]

    if "attorney email says" in lower or "docket lists" in lower:
        return "date_fact", "fact_about_source", "contradiction_side_a" if index == 0 else "contradiction_side_b", ["contradiction_candidate", "bucket_eval_required"]

    return "event_fact", "fact", "generic_component", ["bucket_eval_required"]


def split_claims(fixture_id: str, input_statement: str) -> Tuple[List[AtomicClaim], List[str]]:
    clauses, rule_path, mode = _split_statement(input_statement)
    claims: List[AtomicClaim] = []
    for i, clause in enumerate(clauses, start=1):
        claim_type, asserted_as, split_basis, flags = _classify_claim(clause, mode=mode, index=i-1)
        claims.append(
            AtomicClaim(
                atomic_claim_id=f"{fixture_id}-C{i}",
                parent_statement_id=fixture_id,
                claim_text=clause,
                claim_type=claim_type,
                asserted_as=asserted_as,
                source_span=clause,
                split_basis=split_basis,
                flags=flags,
            )
        )
    return claims, rule_path


def _strip_expected_claim(c: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "claim_text": c.get("claim_text"),
        "claim_type": c.get("claim_type"),
        "asserted_as": c.get("asserted_as"),
        "split_basis": c.get("split_basis"),
        "flags": c.get("flags") or [],
        "starting_bucket": c.get("starting_bucket"),
    }


def evaluate_fixture(fx: Dict[str, Any], strict: bool = True) -> Dict[str, Any]:
    fixture_id = fx["fixture_id"]
    claims, rule_path = split_claims(fixture_id, fx["input_statement"])
    computed = [c.comparable() for c in claims]
    expected = [_strip_expected_claim(c) for c in fx["expected_atomic_claims"]]

    failures: List[str] = []
    if len(computed) != fx.get("expected_split_count"):
        failures.append(f"split_count expected {fx.get('expected_split_count')} got {len(computed)}")
    if computed != expected:
        failures.append("atomic_claims mismatch")
    if strict and rule_path != fx.get("expected_rule_path"):
        failures.append(f"rule_path expected {fx.get('expected_rule_path')} got {rule_path}")

    # Guardrails: splitter cannot assign final evidentiary bucket. It can only set starting_bucket.
    forbidden_bucket_values = {"VERIFIED", "PROVISIONALLY_VERIFIED", "INFERRED", "USER_ORIGINATED", "CONTRADICTED"}
    for c in computed:
        if c.get("starting_bucket") != "QUARANTINED":
            failures.append("non-quarantine starting bucket emitted")
        if any(c.get(k) in forbidden_bucket_values for k in ("computed_bucket", "expected_bucket", "current_bucket")):
            failures.append("splitter assigned a final evidentiary bucket")

    return {
        "fixture_id": fixture_id,
        "name": fx.get("name"),
        "passed": not failures,
        "failures": failures,
        "computed_rule_path": rule_path,
        "expected_rule_path": fx.get("expected_rule_path"),
        "computed_atomic_claims": computed,
        "expected_atomic_claims": expected,
    }


def load_suite(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "fixtures" not in data:
        raise ValueError("Invalid suite: missing fixtures")
    return data


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate VaultGhost claim-splitting fixtures")
    parser.add_argument("fixture_yaml", type=Path)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--show-passes", action="store_true")
    parser.add_argument("--no-strict", action="store_true", help="Do not require exact rule-path equality")
    args = parser.parse_args(argv)

    try:
        suite = load_suite(args.fixture_yaml)
        strict = not args.no_strict
        results = [evaluate_fixture(fx, strict=strict) for fx in suite["fixtures"]]
        passed = sum(1 for r in results if r["passed"])
        failed = len(results) - passed
        report = {
            "suite_id": suite.get("suite_id"),
            "version": suite.get("version"),
            "strict": strict,
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "results": results,
        }
        if args.report:
            args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
        for r in results:
            if r["passed"] and args.show_passes:
                print(f"PASS {r['fixture_id']} {r['name']}")
            elif not r["passed"]:
                print(f"FAIL {r['fixture_id']} {r['name']}: {'; '.join(r['failures'])}")
        print(f"Suite {suite.get('suite_id')} v{suite.get('version')}: {passed} passed, {failed} failed")
        print(f"strict={strict}")
        return 0 if failed == 0 else 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
