# VaultGhost(TM) Protocol

VaultGhost(TM) is an external evidence-layer protocol for AI-mediated artifacts. It creates tamper-evident evidence bundles and separates four layers that are often confused:

1. Internal consistency.
2. Cryptographic signature validity.
3. Signer identity trust.
4. Provenance confidence.

A valid signature is not trusted identity. Internal consistency is not provenance.

The current counsel-intake baseline includes a strict manifest schema, reproducible unsigned fixture, verifier CLI contract, generator contract, and a real signed fixture demonstrating Ed25519 signature validity while correctly returning `insufficient_evidence` because signer identity is not externally trusted.

## What this repository does not claim

- It does not claim patent issuance.
- It does not claim legal sufficiency.
- It does not claim model-provider endorsement.
- It does not claim contribution to GPT-5.5 or any third-party model.
- It does not claim the fixture image is a real AI-generated poster.

## Verification baseline

- Unsigned fixture: `artifact_integrity` true, `bundle_integrity` true, `manifest_digest_valid` true, `computed_status` `insufficient_evidence`.
- Signed fixture: `signature_valid` true, `signer_identity_trusted` false, `computed_status` `insufficient_evidence`.

## Required implementation behavior

- The verifier must recompute status from actual files and cryptographic checks.
- The verifier must never trust `manifest.verification.status`.
- The generator creates claims; the verifier computes truth.

## Counsel-safe disclaimer

This documentation is a technical handoff only. It is not legal advice, not a patentability analysis, and not a legal opinion. Patent determinations must be made by qualified patent counsel.

## Contents

- `index.md` — public-facing technical overview.
- `counsel-intake-baseline.md` — counsel-intake baseline summary and links.
- `artifacts-manifest.md` — SHA-256 hash manifest for every artifact in this tree.
- `counsel-intake/` — supplied counsel-intake packet, prompt, and hash manifest.
- `specs/` — placeholder pointers to spec artifacts (see `artifacts-manifest.md` for status).
- `fixtures/` — placeholder pointers to fixture ZIPs (see blockers).
- `verification/README.md` — verification commands and captured outputs.
- `implementation-report.md` — final implementation report.
