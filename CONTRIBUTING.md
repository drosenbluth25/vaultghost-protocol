# Contributing to VaultGhost™

VaultGhost v0.1.1 is a protocol skeleton. Contributions should preserve semantic boundaries.

## Rules

- Do not introduce private legal materials.
- Do not change bucket semantics without fixtures.
- Do not add UI logic that changes claim status.
- Do not imply legal validation, court recognition, production readiness, or FACT-AUDIT validation.

## Pull Request Checklist

```bash
python3 tools/validate_all_schemas.py --root .
python3 tools/run_all_checks_local_v0_1_1.py --root .
```
