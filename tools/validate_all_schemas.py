#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import yaml
import jsonschema

PAIRS = [
    ("schemas/claim_splitting_fixture.schema.json", "fixtures/vaultghost_claim_splitting_fixtures_v0_1.yaml"),
    ("schemas/bucket_fixture.schema.json", "fixtures/vaultghost_legal_bucket_fixtures_v0_1.yaml"),
    ("schemas/integration_fixture.schema.json", "fixtures/vaultghost_integration_fixtures_v0_1.yaml"),
    ("schemas/precedence_fixture.schema.json", "fixtures/vaultghost_precedence_fixtures_v0_1.yaml"),
]

OPTIONAL_PAIRS = [
    ("schemas/final_claim_packet.schema.json", "fixtures/vaultghost_sample_final_claim_packet_v0_1.json"),
    ("schemas/final_claim_packet.schema.json", "fixtures/vaultghost_sample_final_claim_packet_v0_1.yaml"),
]

def load(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    return json.loads(text)

def validate_pair(root: Path, schema_rel: str, file_rel: str, required: bool):
    schema_path = root / schema_rel
    file_path = root / file_rel
    rec = {
        "schema": schema_rel,
        "file": file_rel,
        "required": required,
        "status": "FAIL" if required else "SKIPPED",
        "error": None,
    }
    if not schema_path.exists():
        rec["error"] = f"schema not found: {schema_rel}"
        return rec
    if not file_path.exists():
        rec["error"] = f"{'required' if required else 'optional'} file not found: {file_rel}"
        return rec
    try:
        validator = jsonschema.Draft202012Validator(load(schema_path))
        errors = sorted(validator.iter_errors(load(file_path)), key=lambda e: list(e.path))
        if errors:
            err = errors[0]
            loc = "/".join(map(str, err.path)) or "<root>"
            rec["error"] = f"{loc}: {err.message}"
            rec["status"] = "FAIL"
        else:
            rec["status"] = "PASS"
            rec["error"] = None
    except Exception as exc:
        rec["status"] = "FAIL"
        rec["error"] = str(exc)
    return rec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--report", type=Path, default=Path("reports/SCHEMA_VALIDATION_REPORT_v0_1_1.json"))
    ap.add_argument("--include-optional", action="store_true")
    args = ap.parse_args()

    root = args.root.resolve()
    entries = [validate_pair(root, s, f, True) for s, f in PAIRS]
    if args.include_optional:
        entries.extend(validate_pair(root, s, f, False) for s, f in OPTIONAL_PAIRS)

    failures = [e for e in entries if e["required"] and e["status"] != "PASS"]
    report = {
        "report_id": "VG-SCHEMA-VALIDATION-REPORT-v0.1.1",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "root": str(root),
        "overall_status": "PASS" if not failures else "FAIL",
        "summary": {
            "total": len(entries),
            "required_total": sum(1 for e in entries if e["required"]),
            "required_passed": sum(1 for e in entries if e["required"] and e["status"] == "PASS"),
            "required_failed": len(failures),
        },
        "entries": entries,
    }

    out = root / args.report
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for e in entries:
        print(f"{e['status']} {e['file']} <= {e['schema']}" + (f": {e['error']}" if e["error"] and e["required"] else ""))
    print(f"Schema validation overall={report['overall_status']}; report={args.report}")
    return 0 if report["overall_status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
