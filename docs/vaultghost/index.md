# VaultGhost(TM) Protocol — Technical Overview

## 1. What VaultGhost is

VaultGhost(TM) is an external evidence-layer protocol for AI-mediated artifacts. It creates strict evidence bundles containing artifact, prompt, replay, manifest, hash, signature, and verification metadata.

## 2. What it verifies

- Artifact integrity against bundled hashes.
- Bundle integrity against the manifest digest.
- Manifest digest validity.
- Cryptographic signature validity (when a signed fixture is present).

## 3. What it does not verify without external trust anchors

- Real-world authorship.
- Model origin or model-provider endorsement.
- Generation time.
- Trusted signer identity.

A signature alone does not establish that the signer is who they claim to be. A bundle that is internally consistent is not, by that fact, a bundle whose origin has been independently verified.

## 4. Core principle

A valid signature is not trusted identity. Internal consistency is not provenance.

## 5. Technical baseline versions

- Evidence Bundle Manifest Schema v0.1.6.
- Reproducible Unsigned Fixture v0.1.5.
- Image Provenance Demo Walkthrough v0.2.0.
- Verifier CLI Specification v0.3.1.
- Evidence Bundle Generator Specification v0.4.1, with signature alignment through v0.4.5.
- Real Signed Fixture v0.4.5.
- Patent Counsel Packet v0.5.0.
- Counsel Intake Addendum v0.5.2.

## 6. Fixture status

- Unsigned fixture: referenced; ZIP not yet vendored into this tree (see `artifacts-manifest.md` for status and blockers).
- Signed fixture: referenced; ZIP not yet vendored into this tree (see `artifacts-manifest.md` for status and blockers).

The 1x1 PNG fixture is a deterministic test fixture. It is not a real AI-generated poster.

## 7. Counsel-intake note

The counsel-intake materials in this tree are a technical packet. They are not a legal conclusion, not legal advice, and not a patentability analysis. Patent determinations must be made by qualified patent counsel.

## 8. Download / artifact links

- Counsel-intake packet PDF: [`counsel-intake/VaultGhost_Counsel_Intake_and_GitHub_Integration_Pack_v0.5.2.pdf`](counsel-intake/VaultGhost_Counsel_Intake_and_GitHub_Integration_Pack_v0.5.2.pdf)
- Integration prompt: [`counsel-intake/VaultGhost_Manus_Kimi_GitHub_Integration_Prompt.txt`](counsel-intake/VaultGhost_Manus_Kimi_GitHub_Integration_Prompt.txt)
- Handoff hash manifest: [`counsel-intake/VaultGhost_Handoff_Artifact_Hashes.txt`](counsel-intake/VaultGhost_Handoff_Artifact_Hashes.txt)
- Full SHA-256 manifest: [`artifacts-manifest.md`](artifacts-manifest.md)
- Verification: [`verification/README.md`](verification/README.md)
