#!/usr/bin/env python3
"""
VaultGhost(TM) v0.1.1 release manifest verifier.

Purpose:
- Load a VaultGhost release manifest.
- Perform built-in structural validation.
- Optionally validate against a JSON Schema if the `jsonschema` package is installed.
- Confirm each listed artifact exists.
- Recompute SHA-256 for each artifact.
- Compare expected vs. computed hashes.
- Compare expected vs. actual file size.
- Emit a machine-readable JSON report.
- Exit nonzero on failure.

This script intentionally does not require the verification report to be listed
inside the manifest. Self-referential manifests are avoided at v0.1.1.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


HEX64 = set("0123456789abcdefABCDEF")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError(f"{path} did not contain a JSON object")
    return value


def built_in_validate_manifest(manifest: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    required = ["manifest_id", "protocol", "version", "created_at", "status", "artifacts"]
    for key in required:
        if key not in manifest:
            errors.append(f"missing required top-level field: {key}")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifacts must be a non-empty list")
        return errors

    seen_filenames = set()
    for idx, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            errors.append(f"artifacts[{idx}] must be an object")
            continue

        for key in ["filename", "path", "bytes", "sha256"]:
            if key not in artifact:
                errors.append(f"artifacts[{idx}] missing required field: {key}")

        filename = artifact.get("filename")
        if isinstance(filename, str):
            if filename in seen_filenames:
                errors.append(f"duplicate artifact filename: {filename}")
            seen_filenames.add(filename)
        else:
            errors.append(f"artifacts[{idx}].filename must be a string")

        if not isinstance(artifact.get("path"), str):
            errors.append(f"artifacts[{idx}].path must be a string")

        if not isinstance(artifact.get("bytes"), int) or artifact.get("bytes", -1) < 0:
            errors.append(f"artifacts[{idx}].bytes must be a nonnegative integer")

        digest = artifact.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64 or any(ch not in HEX64 for ch in digest):
            errors.append(f"artifacts[{idx}].sha256 must be a 64-character hexadecimal string")

    return errors


def jsonschema_validate_if_available(manifest: Dict[str, Any], schema_path: Optional[Path]) -> Tuple[str, List[str]]:
    if schema_path is None:
        return "not_requested", []

    try:
        schema = load_json(schema_path)
    except Exception as exc:
        return "schema_load_error", [f"could not load schema: {exc}"]

    try:
        import jsonschema  # type: ignore
    except Exception:
        return "jsonschema_not_installed_builtin_validation_used", []

    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(manifest), key=lambda e: list(e.path))
    if not errors:
        return "passed", []

    return "failed", [
        f"{'/'.join(map(str, err.path)) or '<root>'}: {err.message}"
        for err in errors
    ]


def resolve_artifact_path(raw_path: str, *, manifest_dir: Path) -> Path:
    p = Path(raw_path)
    if p.is_absolute():
        return p
    return manifest_dir / p


def verify_artifacts(manifest: Dict[str, Any], *, manifest_path: Path) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    manifest_dir = manifest_path.resolve().parent

    for artifact in manifest.get("artifacts", []):
        filename = artifact.get("filename")
        raw_path = artifact.get("path")
        expected_bytes = artifact.get("bytes")
        expected_sha256 = str(artifact.get("sha256", "")).lower()

        resolved = resolve_artifact_path(str(raw_path), manifest_dir=manifest_dir)
        exists = resolved.exists() and resolved.is_file()

        record: Dict[str, Any] = {
            "filename": filename,
            "declared_path": raw_path,
            "resolved_path": str(resolved),
            "exists": exists,
            "expected_bytes": expected_bytes,
            "actual_bytes": None,
            "bytes_match": False,
            "expected_sha256": expected_sha256,
            "computed_sha256": None,
            "sha256_match": False,
            "status": "FAIL",
            "errors": []
        }

        if not exists:
            record["errors"].append("file missing")
            results.append(record)
            continue

        actual_bytes = resolved.stat().st_size
        computed = sha256_file(resolved)

        record["actual_bytes"] = actual_bytes
        record["computed_sha256"] = computed
        record["bytes_match"] = (actual_bytes == expected_bytes)
        record["sha256_match"] = (computed.lower() == expected_sha256)

        if not record["bytes_match"]:
            record["errors"].append("byte size mismatch")
        if not record["sha256_match"]:
            record["errors"].append("sha256 mismatch")

        if not record["errors"]:
            record["status"] = "PASS"

        results.append(record)

    return results


def summarize(manifest_errors: List[str], schema_status: str, schema_errors: List[str], artifact_results: List[Dict[str, Any]]) -> str:
    if manifest_errors or schema_errors:
        return "FAIL"
    if any(item.get("status") != "PASS" for item in artifact_results):
        return "FAIL"
    if schema_status == "failed":
        return "FAIL"
    return "PASS"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Verify a VaultGhost release manifest.")
    parser.add_argument("manifest", type=Path, help="Path to release manifest JSON.")
    parser.add_argument("--schema", type=Path, default=None, help="Optional JSON Schema path.")
    parser.add_argument("--report", type=Path, default=None, help="Write verification report JSON.")
    parser.add_argument("--show-passes", action="store_true", help="Print PASS lines for each artifact.")
    args = parser.parse_args(argv)

    try:
        manifest = load_json(args.manifest)
        built_in_errors = built_in_validate_manifest(manifest)
        schema_status, schema_errors = jsonschema_validate_if_available(manifest, args.schema)
        artifact_results = verify_artifacts(manifest, manifest_path=args.manifest)

        overall_status = summarize(built_in_errors, schema_status, schema_errors, artifact_results)

        report = {
            "report_id": "VG-MANIFEST-VERIFY-REPORT",
            "created_at": utc_now(),
            "overall_status": overall_status,
            "manifest_path": str(args.manifest),
            "schema_path": str(args.schema) if args.schema else None,
            "manifest_id": manifest.get("manifest_id"),
            "protocol": manifest.get("protocol"),
            "version": manifest.get("version"),
            "status": manifest.get("status"),
            "environment": {
                "python_version": sys.version.split()[0],
                "platform": platform.platform(),
                "cwd": os.getcwd()
            },
            "validation": {
                "built_in_status": "PASS" if not built_in_errors else "FAIL",
                "built_in_errors": built_in_errors,
                "jsonschema_status": schema_status,
                "jsonschema_errors": schema_errors
            },
            "artifact_summary": {
                "total": len(artifact_results),
                "passed": sum(1 for item in artifact_results if item.get("status") == "PASS"),
                "failed": sum(1 for item in artifact_results if item.get("status") != "PASS")
            },
            "artifacts": artifact_results
        }

        if args.report:
            args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        for item in artifact_results:
            if item.get("status") == "PASS" and args.show_passes:
                print(f"PASS {item.get('filename')} {item.get('computed_sha256')}")
            elif item.get("status") != "PASS":
                print(f"FAIL {item.get('filename')} :: {', '.join(item.get('errors', []))}", file=sys.stderr)

        print(
            f"Manifest {manifest.get('manifest_id')} v{manifest.get('version')}: "
            f"{report['artifact_summary']['passed']} passed, "
            f"{report['artifact_summary']['failed']} failed; "
            f"overall={overall_status}"
        )

        return 0 if overall_status == "PASS" else 1

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
