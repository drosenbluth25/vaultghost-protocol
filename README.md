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

## Ecosystem

VaultGhost is organized as a multi-repository protocol ecosystem. The table below separates specification, tested implementation, isolated verification artifacts, red-team stub work, and private/non-public tooling.

| Repository | Role | Public status | Evidence boundary |
|---|---|---|---|
| [`vaultghost-protocol`](https://github.com/drosenbluth25/vaultghost-protocol) | Canonical specification | Specified | Contains the formal protocol specification, citation metadata, license, and release manifests. |
| [`vaultghost-core`](https://github.com/drosenbluth25/vaultghost-core) | Ed25519 signing + canonicalization layer | Implemented with tests | Public repository contains schemas, tests, package files, and signing-related implementation evidence; ecosystem-level integration is not fully demonstrated here. |
| [`vaultghost-verify`](https://github.com/drosenbluth25/vaultghost-verify) | Deterministic verification pipeline | Implemented with verification command | Public repository documents `make verify`, expected output matching, tamper-check behavior, and test commands; cross-repository artifact consumption remains limited. |
| [`vaultghost-chain-ledger`](https://github.com/drosenbluth25/vaultghost-chain-ledger) | SHA-256 provenance-chain artifacts | Implemented but isolated | Public repository documents CHAIN_INDEX.json, provenance artifacts, and verify-chain behavior; external timestamping, third-party validation, and full ecosystem integration remain separate concerns. |
| [`vaultghost-stub`](https://github.com/drosenbluth25/vaultghost-stub) | Python/Rust red-team stub | Stub / red-team prototype | Public repository describes itself as a minimal red-team review stub and not production-ready. |
| `spec-orchestration-eval-harness` | Spec-driven benchmarking / orchestration harness | Private / not publicly verifiable | Repository is private; public README should not imply public verification. |

Status labels describe public repository evidence only. They do not assert full production readiness, legal sufficiency, external adoption, third-party validation, or complete end-to-end integration across all repositories.

PProvisional patent filed February 25, 2026.                
