#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def run(root: Path, name: str, command: list[str]):
    rec = {
        "name": name,
        "command": command,
        "started_at": utc_now(),
        "finished_at": None,
        "returncode": None,
        "stdout": "",
        "stderr": "",
        "status": "FAIL",
    }
    proc = subprocess.run(command, cwd=str(root), text=True, capture_output=True)
    rec["finished_at"] = utc_now()
    rec["returncode"] = proc.returncode
    rec["stdout"] = proc.stdout
    rec["stderr"] = proc.stderr
    rec["status"] = "PASS" if proc.returncode == 0 else "FAIL"
    return rec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--report", type=Path, default=Path("reports/FULL_RELEASE_CHECK_REPORT_v0_1_1.json"))
    args = ap.parse_args()

    root = args.root.resolve()
    py = sys.executable
    checks = [
        ("schema_validation", [
            py, "tools/validate_all_schemas.py", "--root", "."
        ]),
        ("claim_splitting", [
            py, "evaluators/evaluate_claim_splitting_fixture.py",
            "fixtures/vaultghost_claim_splitting_fixtures_v0_1.yaml",
            "--report", "reports/vaultghost_claim_splitting_eval_report_v0_1.json"
        ]),
        ("bucket_transitions", [
            py, "evaluators/evaluate_bucket_fixture.py",
            "fixtures/vaultghost_legal_bucket_fixtures_v0_1.yaml",
            "--check-limitations"
        ]),
        ("integration", [
            py, "evaluators/evaluate_vaultghost_integration.py",
            "fixtures/vaultghost_integration_fixtures_v0_1.yaml",
            "--splitter", "evaluators/evaluate_claim_splitting_fixture.py",
            "--bucket-evaluator", "evaluators/evaluate_bucket_fixture.py",
            "--report", "reports/vaultghost_integration_eval_report_v0_1.json"
        ]),
        ("precedence", [
            py, "evaluators/evaluate_precedence_fixture.py",
            "fixtures/vaultghost_precedence_fixtures_v0_1.yaml",
            "--report", "reports/vaultghost_precedence_eval_report_v0_1.json",
            "--check-limitations"
        ]),
        ("manifest_verification", [
            py, "tools/verify_release_manifest.py",
            "vaultghost_public_release_manifest_v0_1_1.json",
            "--schema", "schemas/release_manifest.schema.json",
            "--report", "reports/MANIFEST_VERIFY_REPORT_v0_1_1.json"
        ]),
    ]

    results = []
    for name, cmd in checks:
        rec = run(root, name, cmd)
        results.append(rec)
        print(f"{rec['status']} {name}")
        if rec["status"] != "PASS":
            if rec["stderr"]:
                print(rec["stderr"])
            break

    failed = [r for r in results if r["status"] != "PASS"]
    report = {
        "report_id": "VG-FULL-RELEASE-CHECK-REPORT-v0.1.1",
        "created_at": utc_now(),
        "root": str(root),
        "overall_status": "PASS" if not failed and len(results) == len(checks) else "FAIL",
        "summary": {"total": len(results), "passed": len(results)-len(failed), "failed": len(failed)},
        "checks": results,
    }

    out = root / args.report
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Full release checks overall={report['overall_status']}; report={args.report}")
    return 0 if report["overall_status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
