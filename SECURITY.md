# Security Policy

## Reporting a Vulnerability

To report a security vulnerability, email **rosenbluthdaniel2@gmail.com** with the subject line `[SECURITY] <repo-name>`.

Do not open a public issue for security-related findings.

Expected response time: within 7 days.

## Commit and Release Integrity

All commits to the default branch of this repository are required to be GPG- or SSH-signed.
GitHub displays a **Verified** badge on each signed commit.

All tagged releases include a SHA-256 artifact manifest (`SHA256SUMS.txt`) attached to the GitHub Release.
To verify a release artifact:

```sh
sha256sum --check SHA256SUMS.txt
```

## Canonical Sources

| Artifact type | Canonical location |
|---|---|
| Protocol specification | `vaultghost-protocol` repo, `SPECIFICATION.md` |
| Source code | This repository, default branch |
| Release archives | GitHub Releases, with attached SHA-256 manifest |
| Academic citation | `CITATION.cff` (where present) |

Markdown and HTML source files are canonical. PDFs are derived snapshots only.

## Authorship and Provenance

VaultGhost and all associated works are authored by Daniel Rosenbluth.
A U.S. provisional patent was filed February 25, 2026.
The VaultGhost Protocol is released under Apache-2.0; see `LICENSE` for terms.

Chain-break events in the provenance ledger are documented explicitly in
`vaultghost-chain-ledger/PROVENANCE.md` rather than suppressed.
