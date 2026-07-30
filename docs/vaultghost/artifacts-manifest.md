# Artifacts Manifest

This manifest lists every artifact added under `docs/vaultghost/` in this branch with computed SHA-256 hashes. Where source artifacts were not supplied to this workspace, the entry is marked accordingly. Internal manifest values from the supplied counsel-intake packet are recorded in their own table.

## File SHA-256 hashes

Hashes computed from the working tree on branch `chore/vaultghost-counsel-intake-baseline`.

| Path (relative to repo root) | Type | SHA-256 |
|---|---|---|
| `docs/vaultghost/README.md` | Counsel-safe README | `7169d0e6f13d5eb7a5ed27b12b8d6630e06cee8bf873078a8704c9e3181c2e6a` |
| `docs/vaultghost/index.md` | Public-facing technical overview | `7d82c28afc6331b64cd7f6942ff0f0781c7fe61bcf1b910805e81385a092d747` |
| `docs/vaultghost/counsel-intake-baseline.md` | Counsel-intake baseline summary | `ac101e695ad883a0aa8cb1c20039c6faeeab6bb108d70c14f6493af6c634c38c` |
| `docs/vaultghost/artifacts-manifest.md` | This manifest | Pending — self-referential, computed post-write |
| `docs/vaultghost/counsel-intake/VaultGhost_Counsel_Intake_and_GitHub_Integration_Pack_v0.5.2.pdf` | Supplied counsel-intake PDF | `594f5e3dff46edeb5544daa2ae64e2a075b4064261fe68c20b6b2f3a9b8e67fb` |
| `docs/vaultghost/counsel-intake/VaultGhost_Manus_Kimi_GitHub_Integration_Prompt.txt` | Supplied integration prompt | `4e7bde8b6d80f97528d081c3d7cd3881da89be14443e5efa02d416af41d96c52` |
| `docs/vaultghost/counsel-intake/VaultGhost_Handoff_Artifact_Hashes.txt` | Supplied handoff hash manifest | `a5ba321496639f7e63fd92bc3063a43be2760630f05f41cca9326e5b6882d3db` |
| `docs/vaultghost/specs/README.md` | Specs pointer index (placeholder) | `e4526b2aaede7012555b9eb73f1272baa8ba521173b2cfb6113487eb8b79a3aa` |
| `docs/vaultghost/fixtures/README.md` | Fixtures pointer index (placeholder) | `0df9c3ecbd29a05aabf2ec378b3ae1087659c6c15a1607367de13a806543c811` |
| `docs/vaultghost/verification/README.md` | Verification documentation | `53819fa19867c12d6ca0b03a76013b110d3db2c25064d97d40d4625430a65761` |
| `docs/vaultghost/verification/VERIFY_OUTPUT.txt` | Captured `sha256sum` output | `c634a9144b98d316bd844d7e8b4fe90c0f69f29cbafdf09b3d9a50ee5f27468c` |
| `docs/vaultghost/implementation-report.md` | Implementation report | Pending — self-referential, computed post-write |

The two entries marked self-referential are computed after the manifest itself is written and committed. They will be recorded in `implementation-report.md` once the working tree is final.

## Spec / fixture artifacts referenced but not vendored

| Artifact | Expected path | Hash status |
|---|---|---|
| Evidence Bundle Manifest Schema v0.1.6 | `docs/vaultghost/specs/vaultghost-evidence-bundle-manifest-schema-v0.1.6.json` | Pending — source artifact not supplied to this workspace |
| Verifier CLI Specification v0.3.1 | `docs/vaultghost/specs/vaultghost-verifier-cli-spec-v0.3.1.md` | Pending final exported markdown hash |
| Evidence Bundle Generator Specification v0.4.1 | `docs/vaultghost/specs/vaultghost-generator-spec-v0.4.1.md` | Pending final exported markdown hash |
| Signature Alignment v0.4.5 | `docs/vaultghost/specs/vaultghost-signature-alignment-v0.4.5.md` | Pending final exported markdown hash |
| Reproducible Unsigned Fixture v0.1.5 ZIP | `docs/vaultghost/fixtures/vaultghost_v015_reproducible_fixture.zip` | Pending — fixture ZIP not supplied to this workspace |
| Real Signed Fixture v0.4.5 ZIP | `docs/vaultghost/fixtures/vaultghost_v045_real_signed_fixture.zip` | Pending — fixture ZIP not supplied to this workspace |

## Internal manifest values from the supplied counsel-intake packet

These values are taken from the supplied integration packet. They describe the contents of the signed fixture ZIP, which is not vendored in this branch. They are reproduced unmodified for counsel intake.

| Field | Value type | Value |
|---|---|---|
| `signed_payload_digest` | sha256 (prefixed) | `sha256:b2a2d5400c43249264b6d463a9ada18c24b68048d5dc8a94a9c0bbc2ac119c73` |
| Signed fixture `manifest_digest` | sha256 (prefixed) | `sha256:fdd9cb0749705b2c351ca49bac43c0c885f672cb3baca467c3a920ca0ad510c9` |
| Ed25519 public key | base64url (no padding) | `EIlCg_p4_eRFJVhDBwhC2I5gSf1ykOjrqlbY-iHQqcw` |
| Ed25519 signature | base64url (no padding) | `tfzRyGoaao_8YNIppNNpUTo19_7kSpeUBgie68haSUG_abG2FBOvJqhuRgzpY8DSMVaDhCGqiHZZMcNPyG8YAQ` |

## Notes

- Every file SHA-256 in the first table was computed with `sha256sum` against the working tree on `chore/vaultghost-counsel-intake-baseline`.
- The three supplied artifact hashes match the values published in `VaultGhost_Handoff_Artifact_Hashes.txt`.
- No fixture ZIP contents were altered. No fixture verification result was synthesized.
