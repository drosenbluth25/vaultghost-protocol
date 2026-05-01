# VaultGhost Ecosystem Evidence Map

## Purpose

This document maps public VaultGhost ecosystem claims to observable GitHub evidence. It separates public repository evidence from unproven integration claims.

This file is not a promotional summary. It is an evidence-bound status map.

## Status Labels

| Label | Meaning |
|---|---|
| Specified | The repository defines protocol structure, documentation, or metadata, but does not itself prove executable implementation. |
| Implemented with tests | The repository contains implementation artifacts and public tests supporting at least part of the claimed behavior. |
| Implemented with verification command | The repository documents a public command or workflow for verification behavior, such as `make verify`, expected-output matching, or tamper-check behavior. |
| Implemented but isolated | The repository contains provenance, chain, ledger, or verification artifacts, but does not by itself prove full ecosystem-level integration. |
| Stub / red-team prototype | The repository is intentionally minimal, experimental, or review-oriented and should not be represented as production-ready. |
| Private / not publicly verifiable | The repository or tool is not publicly inspectable, so its claims cannot be verified from public GitHub evidence. |

## Repository Evidence Table

| Repository | Safer public status | Public evidence | What this proves | What remains unproven |
|---|---|---|---|---|
| [`vaultghost-protocol`](https://github.com/drosenbluth25/vaultghost-protocol) | Specified | README, SPECIFICATION.md, LICENSE, release manifests, evidence memos, checksum files. | Public protocol documentation and evidence-oriented archival structure exist. | Does not itself prove executable implementation or full cross-repository integration. |
| [`vaultghost-core`](https://github.com/drosenbluth25/vaultghost-core) | Implemented with tests | Schemas, tests, package files, signing-related implementation files, and release materials. | At least part of the signing/canonicalization layer is publicly implemented and test-backed. | Does not by itself prove that outputs are consumed across the full VaultGhost ecosystem. |
| [`vaultghost-verify`](https://github.com/drosenbluth25/vaultghost-verify) | Implemented with verification command | README verification commands, Makefile, EXPECTED_OUTPUT.txt, tools, tests, and tamper-check behavior where present. | Public verification workflow evidence exists. | Does not by itself prove full cross-repository artifact consumption or complete forensic correctness. |
| [`vaultghost-chain-ledger`](https://github.com/drosenbluth25/vaultghost-chain-ledger) | Implemented but isolated | CHAIN_INDEX.json, provenance files, release manifests, artifacts, and verify-chain documentation where present. | Public provenance-chain artifacts and chain-verification structure exist. | Does not by itself prove external timestamping, third-party validation, or complete integration with signing and verification repos. |
| [`vaultghost-stub`](https://github.com/drosenbluth25/vaultghost-stub) | Stub / red-team prototype | README describes the repository as a minimal stub for simulation or red-team review and not production-ready. | Public stub/prototype work exists. | Does not prove production readiness or full integration with the rest of the ecosystem. |
| `spec-orchestration-eval-harness` | Private / not publicly verifiable | No public repository evidence available. | Nothing publicly verifiable from GitHub. | Public reviewers cannot verify its implementation, tests, or orchestration claims. |

## Evidence Boundary

This document is limited to public GitHub evidence. It does not evaluate private repositories, unmerged local work, legal novelty, patent scope, third-party adoption, commercial readiness, external validation, or production readiness.

## Integration Gap

The main remaining public evidence gap is not absence of all implementation. The gap is absence of a single public end-to-end integration record showing signing, canonicalization, verification, and provenance-chain mechanics operating together across repositories.

## Recommended Current Claim Boundary

Based on public evidence, the safest current public claim is:

“VaultGhost has a public written specification and multiple public implementation-adjacent repositories with tested or command-verifiable components. Full cross-repository end-to-end integration remains a public evidence gap.”

Avoid stronger claims unless and until a public integration record exists.
