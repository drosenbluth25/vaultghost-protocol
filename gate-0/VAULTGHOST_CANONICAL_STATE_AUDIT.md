# VaultGhost Canonical State Audit

**Audit date:** 2026-07-27  
**Status:** Conditional no-go for v0.7  
**Scope:** Repository authority, specification/implementation correspondence, evidence boundaries, and immediate remediation.

## 1. Scope

This audit records the currently observable VaultGhost repository structure. It does not establish patentability, external adoption, production readiness, or independent cryptographic validation.

## 2. Repository Inventory

The connected GitHub account exposes a multi-repository VaultGhost ecosystem spanning public specification, implementation, verification, ledger, evidence, experimental integration, and historical RFC repositories. See `VAULTGHOST_REPOSITORY_INVENTORY.csv`.

## 3. Canonical Repository Candidate

`drosenbluth25/vaultghost-protocol` publicly declares itself the canonical specification repository. That declaration is provisionally retained, but correspondence with the executable repositories is not yet established.

## 4. Branch and Commit State

The authoritative branch is currently represented as `main`. Exact release-pinned commit SHAs for the specification, implementation, verifier, and chain ledger are not yet recorded in a single release manifest.

## 5. Existing Releases and Tags

Release/tag state was not comprehensively enumerated through this audit. No release should be described as end-to-end reproducible until the exact cross-repository SHAs are pinned and independently replayed.

## 6. Baseline Verification Results

`vaultghost-verify` documents `make verify`, `make verify-tampered`, and `make test`. These commands were not executed in an independent fresh-clone environment during this connector-backed audit. `vaultghost-core` has observable dependencies but its README contains only a title and does not expose a baseline command.

## 7. Normative Specifications

The current `SPECIFICATION.md` in `vaultghost-protocol` is a short attribution-oriented document focused on prompt influence, latent drift, symbolic payloads, EchoShell, Drift Anchors, and an LLM Contamination Registry. It does not normatively define the implemented signing, canonicalization, manifest verification, evidence-state, contradiction, policy, or chain-ledger behavior described elsewhere.

This is the primary Gate 0 contradiction.

## 8. Schemas and Implementations

Public documentation points to:

- `vaultghost-core` for Ed25519 signing and canonicalization;
- `vaultghost-verify` for deterministic manifest verification;
- `vaultghost-chain-ledger` for artifact/hash-chain consistency;
- private and experimental repositories for evidence archiving, integration, orchestration, and registry work.

Their interfaces and version relationships are not yet fixed in one authoritative manifest.

## 9. Fixture and Test Inventory

Tests and tamper checks are described in public READMEs and commit history. A complete fixture inventory and independent result record remain absent from the canonical specification repository.

## 10. Authorship Classification

The repository history provides a substantial chronology of user-directed work. A claim-level human-conception and AI-assistance ledger has not yet been added. Patent-relevant claims must map to evidence of human conception rather than merely to commit volume.

## 11. Patent-Support Mapping

The repository states that a provisional patent was filed on 2026-02-25. The official receipt, exact application as filed, supported-feature mapping, and counsel-confirmed deadline are not present in this audit package. Patent-sensitive publication remains on hold pending counsel review.

## 12. Public Disclosure Mapping

Public repositories provide dated disclosures for the protocol name, specification language, signing/verification descriptions, chain artifacts, and red-team prototypes. A consolidated disclosure timeline is still required.

## 13. Contradictions and Duplicates

1. `vaultghost-protocol` claims canonical authority while its current specification does not correspond to the executable evidence-governance stack.
2. Private `vaultghost-rfc` may contain historical or conflicting normative material.
3. `vaultghost-core` is described as implemented with tests, but its README does not document that implementation.
4. Experimental repositories include aspirational or insufficiently demonstrated claims.
5. Latent-influence attribution claims are mixed with technically stronger artifact-provenance claims.

## 14. Missing Evidence

- Exact HEAD and release SHAs for each canonical component;
- fresh-clone command logs;
- independent reproduction report;
- full cross-repository interface map;
- claim-to-code and claim-to-provisional mapping;
- AI-assistance/human-conception ledger;
- prior-art comparison;
- external pilot or adopter evidence.

## 15. Canonicalization Decision

**Conditional designation:**

- Canonical specification candidate: `vaultghost-protocol`
- Canonical implementation candidate: `vaultghost-core`
- Verification utility: `vaultghost-verify`
- Ledger component: `vaultghost-chain-ledger`

This designation is not final until exact commits, interfaces, baseline commands, and specification correspondence are established.

## 16. Go/No-Go Decision for v0.7

**CONDITIONAL NO-GO.**

Do not publish a v0.7 normative specification or claim end-to-end readiness until:

1. cross-repository commits are pinned;
2. `vaultghost-core` exposes a documented baseline;
3. the normative spec is rewritten around implemented evidence-governance behavior;
4. speculative latent-influence claims are isolated as experimental research;
5. a fresh-clone reproduction succeeds;
6. counsel confirms publication and filing constraints.

## Immediate Remediation Order

1. Inventory and pin exact repository SHAs.
2. Document and independently run `vaultghost-core` and `vaultghost-verify` baselines.
3. Declare `vaultghost-rfc` historical, supporting, or normative.
4. Create a cross-repository release manifest.
5. Separate operational provenance guarantees from latent-attribution hypotheses.
6. Draft the next normative specification only after the preceding controls pass.
