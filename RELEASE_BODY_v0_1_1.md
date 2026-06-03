# VaultGhost™ v0.1.1

VaultGhost™ v0.1.1 is a release-hardened, reproducible legal-adjacent claim-governance protocol skeleton.

## Release Status

This release passed the reproducible release gate:

```bash
python3 tools/validate_all_schemas.py --root . && python3 tools/run_all_checks_local_v0_1_1.py --root .
```

## Verified Checks

- Schema validation: PASS
- Claim splitting: PASS
- Bucket transitions: PASS
- End-to-end integration: PASS
- Precedence collision checks: PASS
- Manifest verification: PASS

## Core Pipeline

```text
raw statement
→ claim splitter
→ atomic claims
→ bucket transition engine
→ final claim packet
→ precedence checks
```

## Non-Goals

VaultGhost v0.1.1 is not legal advice, not a production-grade evidence system, not court-recognized, not externally certified, and not FACT-AUDIT-validated.

## Related Work Framing

FACT-AUDIT motivates the importance of adaptive, justification-sensitive factuality assessment. VaultGhost v0.1.1 operationalizes a narrower governance layer for legal-adjacent claim handling: split first, classify second, enforce precedence third, render last.
