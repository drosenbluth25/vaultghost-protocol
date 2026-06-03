# VaultGhost™ Protocol v0.1.1

VaultGhost™ v0.1.1 is a release-hardened, reproducible legal-adjacent claim-governance protocol skeleton.

It is designed to prevent compound AI-generated narratives from laundering unsupported claims into facts.

## Pipeline

```text
raw statement
→ claim splitter
→ atomic claims
→ bucket transition engine
→ final claim packet
→ precedence checks
```

## Reproducible Release Gate

```bash
python3 tools/validate_all_schemas.py --root . && python3 tools/run_all_checks_local_v0_1_1.py --root .
```

## Status

- Schema validation: PASS
- Claim splitting: PASS
- Bucket transitions: PASS
- Integration: PASS
- Precedence: PASS
- Manifest verification: PASS

## Related Work

FACT-AUDIT motivates the importance of adaptive, justification-sensitive factuality assessment. VaultGhost v0.1.1 operationalizes a narrower governance layer for legal-adjacent claim handling: split first, classify second, enforce precedence third, render last.

## Non-Goals

VaultGhost v0.1.1 is not legal advice, not a production-grade evidence system, not court-recognized, not externally certified, and not FACT-AUDIT-validated.
