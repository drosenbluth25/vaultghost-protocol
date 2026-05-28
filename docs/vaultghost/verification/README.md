# Verification

## Verification scope in this branch

The verification command requested for this branch is checksum-only artifact verification, plus any repo-local verification command discovered during inspection. The signed-fixture verification script and its required Python dependencies are not vendored in this branch because the fixture ZIPs were not supplied. No fixture verification result is fabricated here.

## Checksum verification command

To re-verify the supplied artifacts against the published hashes:

```bash
sha256sum \
  docs/vaultghost/counsel-intake/VaultGhost_Counsel_Intake_and_GitHub_Integration_Pack_v0.5.2.pdf \
  docs/vaultghost/counsel-intake/VaultGhost_Manus_Kimi_GitHub_Integration_Prompt.txt \
  docs/vaultghost/counsel-intake/VaultGhost_Handoff_Artifact_Hashes.txt
```

Expected output (matches the published handoff manifest):

```
594f5e3dff46edeb5544daa2ae64e2a075b4064261fe68c20b6b2f3a9b8e67fb  docs/vaultghost/counsel-intake/VaultGhost_Counsel_Intake_and_GitHub_Integration_Pack_v0.5.2.pdf
4e7bde8b6d80f97528d081c3d7cd3881da89be14443e5efa02d416af41d96c52  docs/vaultghost/counsel-intake/VaultGhost_Manus_Kimi_GitHub_Integration_Prompt.txt
a5ba321496639f7e63fd92bc3063a43be2760630f05f41cca9326e5b6882d3db  docs/vaultghost/counsel-intake/VaultGhost_Handoff_Artifact_Hashes.txt
```

The captured output from the run performed in this branch is recorded in `VERIFY_OUTPUT.txt`.

## Repo-local verification commands discovered

A repository scan for existing verification entry points found:

- No `Makefile`, `tox.ini`, `pytest.ini`, `pyproject.toml`, `package.json`, or test directory.
- No GitHub Actions workflows under `.github/workflows/`.
- No `verify_signed_fixture.py` or equivalent script under `docs/` or the repository root.

The repository at the starting commit (`a1f3ab2188eab5bac1f315417d002470cd646fe4`) has no executable verification harness. Checksum-only verification is therefore the only verification command run in this branch.

## Required verifier behavior (specification, not implementation)

When a verifier is implemented for this protocol it must:

- Recompute status from actual files and cryptographic checks.
- Never trust `manifest.verification.status`.
- Treat `signature_valid` and `signer_identity_trusted` as separate, independently-derived fields.

For the unsigned fixture, the expected computed result is `artifact_integrity` true, `bundle_integrity` true, `manifest_digest_valid` true, `computed_status` `insufficient_evidence`. For the signed fixture, the expected computed result is `signature_valid` true, `signer_identity_trusted` false, `computed_status` `insufficient_evidence`.
