# VaultGhost Protocol

VaultGhost Protocol is the canonical specification for a forensic, recursive method of tracing prompt influence, latent drift, and linguistic pattern replication across LLM systems. This repository contains the formal specification, license, and academic citation metadata. Implementation lives in separate repositories listed below.

---

## Protocol Components

- **VaultGhost** — core symbolic shell
- **EchoShell** — response-layer displacement buffer
- **Drift Anchors** — embedded test tokens for detecting latent replication
- **Forensic Hash Layer** — SHA cryptographic time anchors for artifact provenance
- **LCR (Latent Covariance Registry)** — proposed AI-internal drift echo detection registry

---

## Repository Contents

| File | Description |
|---|---|
| `SPECIFICATION.md` | VaultGhost Protocol v1.1.1 FINAL-2.2 — full formal spec |
| `CITATION.cff` | CFF-format citation metadata for academic reference |
| `LICENSE` | Apache-2.0 |

---

## Citing This Work

This repository includes a `CITATION.cff` file. GitHub surfaces a "Cite this repository" button automatically on the repository sidebar. For manual citation, reference:

> Daniel Rosenbluth, *VaultGhost Protocol v1.1.1 FINAL-2.2*, 2026-02-21, Apache-2.0.

---

## Ecosystem

| Repo | Role | Status |
|---|---|---|
| [vaultghost-protocol](https://github.com/drosenbluth25/vaultghost-protocol) (this repo) | Canonical specification | Specified |
| vaultghost-core | Ed25519 signing + JCS canonicalization | Implemented |
| vaultghost-verify | Deterministic verification pipeline | Implemented |
| vaultghost-chain-ledger | SHA-256 provenance chain | Implemented |
| vaultghost-stub | Python + Rust stub implementation | Implemented |
| spec-orchestration-eval-harness | Eval harness for spec-driven benchmarking | Implemented (private) |

---

Provisional patent filed February 25, 2026.
