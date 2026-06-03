# VaultGhost v0.1.1 — Local Runner Patch Notes

## Patch

`run_all_checks_local_v0_1_1.py` is a portability patch for `run_all_checks.py`.

## Reason

The prior runner invoked:

```bash
python3 evaluate_vaultghost_integration.py vaultghost_integration_fixtures_v0_1.yaml --report vaultghost_integration_eval_report_v0_1.json
```

If `evaluate_vaultghost_integration.py` defaults its helper evaluators to `/mnt/data/...`, that can fail outside this environment.

## Fix

The patched runner passes repo-local paths explicitly:

```bash
python3 evaluate_vaultghost_integration.py \
  vaultghost_integration_fixtures_v0_1.yaml \
  --splitter evaluate_claim_splitting_fixture.py \
  --bucket-evaluator evaluate_bucket_fixture.py \
  --report vaultghost_integration_eval_report_v0_1.json
```

## Run

From the VaultGhost repo root:

```bash
python3 run_all_checks_local_v0_1_1.py
```

## Failure evidence

If it fails, paste only the failing check from `FULL_RELEASE_CHECK_REPORT_v0_1_1.json`:

```json
{
  "name": "...",
  "command": ["..."],
  "stderr": "..."
}
```
