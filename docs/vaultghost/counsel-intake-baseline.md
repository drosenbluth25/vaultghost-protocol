# Counsel-Intake Baseline

This page summarizes the VaultGhost(TM) counsel-intake baseline as supplied to this branch.

## Source-of-truth fields

- Authoritative repository: `https://github.com/drosenbluth25/vaultghost-protocol`
- Starting branch: `main`
- Starting commit SHA: `a1f3ab2188eab5bac1f315417d002470cd646fe4`
- Workflow mode: pull request workflow
- Working branch: `chore/vaultghost-counsel-intake-baseline`
- Verification command: checksum-only artifact verification, plus any repo-local verification command discovered during inspection.

## Supplied artifacts (vendored in this tree)

| File | Path | SHA-256 |
|---|---|---|
| Counsel-intake PDF packet v0.5.2 | `counsel-intake/VaultGhost_Counsel_Intake_and_GitHub_Integration_Pack_v0.5.2.pdf` | `594f5e3dff46edeb5544daa2ae64e2a075b4064261fe68c20b6b2f3a9b8e67fb` |
| Integration prompt TXT | `counsel-intake/VaultGhost_Manus_Kimi_GitHub_Integration_Prompt.txt` | `4e7bde8b6d80f97528d081c3d7cd3881da89be14443e5efa02d416af41d96c52` |
| Handoff hash manifest | `counsel-intake/VaultGhost_Handoff_Artifact_Hashes.txt` | `a5ba321496639f7e63fd92bc3063a43be2760630f05f41cca9326e5b6882d3db` |

## Internal manifest values from the supplied packet

These values are referenced in the packet and reproduced here for counsel intake. They are not recomputed in this branch because the underlying signed fixture ZIP is not vendored.

| Field | Value |
|---|---|
| `signed_payload_digest` | `sha256:b2a2d5400c43249264b6d463a9ada18c24b68048d5dc8a94a9c0bbc2ac119c73` |
| Signed fixture `manifest_digest` | `sha256:fdd9cb0749705b2c351ca49bac43c0c885f672cb3baca467c3a920ca0ad510c9` |
| Ed25519 public key | `EIlCg_p4_eRFJVhDBwhC2I5gSf1ykOjrqlbY-iHQqcw` |
| Ed25519 signature | `tfzRyGoaao_8YNIppNNpUTo19_7kSpeUBgie68haSUG_abG2FBOvJqhuRgzpY8DSMVaDhCGqiHZZMcNPyG8YAQ` |

## Baseline language to preserve

VaultGhost(TM) is an external evidence-layer protocol for AI-mediated artifacts. It separates internal consistency, cryptographic signature validity, signer identity trust, and provenance confidence rather than collapsing them into a single trust claim.

A valid signature is not trusted identity. Internal consistency is not provenance.

## Counsel-safe disclaimer

This is a technical handoff only. It is not legal advice, not a patentability analysis, and not a legal opinion. Patent determinations must be made by qualified patent counsel.
