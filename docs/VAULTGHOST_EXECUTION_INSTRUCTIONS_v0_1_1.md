# VaultGhost v0.1.1 — Perplexity-Recommended Execution Pack

## Purpose

This pack gives you the missing execution layer:

1. JSON Schemas for core fixture families.
2. `validate_all_schemas.py`
3. `run_all_checks.py`

## Install dependency

```bash
python3 -m pip install pyyaml jsonschema
```

## Copy these files into your VaultGhost repo root

- `claim_splitting_fixture.schema.json`
- `bucket_fixture.schema.json`
- `integration_fixture.schema.json`
- `precedence_fixture.schema.json`
- `final_claim_packet.schema.json`
- `validate_all_schemas.py`
- `run_all_checks.py`

## Run

```bash
python3 validate_all_schemas.py
python3 run_all_checks.py
```

## Reports produced

```text
SCHEMA_VALIDATION_REPORT_v0_1_1.json
FULL_RELEASE_CHECK_REPORT_v0_1_1.json
```

## On schema failure

Paste only the failing entry fields:

```json
{
  "file": "...",
  "schema": "...",
  "error": "..."
}
```

## On full-check failure

Paste only the failing check fields:

```json
{
  "name": "...",
  "command": ["..."],
  "stderr": "..."
}
```

## Note

`final_claim_packet.schema.json` is included, but `validate_all_schemas.py` does not require a final packet instance by default. It validates the four required fixture suites. Use `--include-optional` if you add a sample final packet named `vaultghost_sample_final_claim_packet_v0_1.json` or `.yaml`.
