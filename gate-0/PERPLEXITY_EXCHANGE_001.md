# VaultGhost Cross-Model Exchange VG-XM-0001

**Target role:** Perplexity external research / contradiction reviewer  
**Source role:** repository resolver / execution agent  
**Status:** OPEN FOR REVIEW  
**Governing proposal:** `gate-0/CROSS_MODEL_COORDINATION_PROTOCOL_v1.md`

## Objective

Perform an independent, source-linked review of three narrow questions. Do not rely on conversational memory or another model's prose as the authority. Read the public GitHub artifacts directly and preserve the claim boundary.

## Canonical starting point

- Repository: `drosenbluth25/vaultghost-protocol`
- Review branch containing this packet: `cross-model-orchestration-v1`
- Base `main` commit when the exchange was opened: `6ba30ae085a1f23ccfcfddae942b9ab037528ffe`
- Existing state artifact: `gate-0/VAULTGHOST_GATE_STATUS.json`
- Existing historical audit: `gate-0/VAULTGHOST_CANONICAL_STATE_AUDIT.md`
- Existing external-review handoff: `gate-0/OTHER_MODEL_HANDOFF.md`

## Claim set

### VG-XM-0001-C1 — CPAT Phase 1 CI execution

Claim to test:

> GitHub Actions run `27804855726` in `drosenbluth25/vaultghost-core` is the `CPAT Phase 1 Hard Gate`; it completed successfully at commit `5e145c15a139839447b3941c5ad23719a58abd54` using `.github/workflows/cpat-phase1-hardgate.yml`. The hard-gate job executed `pytest -q`, reported `8 passed`, returned pytest exit code 0, hashed the evidence, and uploaded a preserved artifact named `cpat-phase1-hardgate-evidence`.

Known locator:

`https://github.com/drosenbluth25/vaultghost-core/actions/runs/27804855726`

Expected disposition is **not precommitted**. Re-resolve the run independently.

Claim boundary if supported:

- Supports execution and success of that bounded GitHub-hosted CI run at that commit and test scope.
- Does not establish universal correctness, independent human reproduction, production readiness, external adoption, patentability, or legal validity.

### VG-XM-0001-C2 — Anchoring terminology contradiction

Claim to test:

> The remembered formulation "two-commit baseline chain" is inconsistent with a described sequence containing C0, C1, and C2 unless the canonical artifacts explicitly define C2 as outside the two-commit baseline chain or otherwise resolve the terminology.

Required work:

1. Search the public VaultGhost repositories and commit-addressable artifacts for `ANCHORING_SEQUENCE`, `BASELINE.md`, C0/C1/C2 terminology, and any exact definition of the baseline chain.
2. Return the authoritative file/commit citations you can actually resolve.
3. If the repository does not resolve the terminology, return `UNRESOLVED`; do not choose a preferred interpretation.

### VG-XM-0001-C3 — Memory-to-canonical-state drift

Claim to test:

> Conversational/Perplexity memory currently mixes durable doctrine with mutable project state. Mutable status claims should be compared against `gate-0/VAULTGHOST_GATE_STATUS.json` and other newer commit-addressable artifacts rather than preserved as unqualified memory facts.

Required work:

Compare the following remembered assertions against the public repository:

- `CPAT Phase 1 is PROVEN_WITHIN_CI_EVIDENCE`;
- Gate 0 repository work is completed;
- the successful CI run is preserved;
- the next gate is non-provisional/PCT preparation;
- exact C0/C1/C2 anchoring topology;
- any assertion that a current release is authorized.

For each, report whether the repository directly supports the assertion, narrows it, contradicts it, or leaves it unresolved. Prefer the newest applicable artifact but note source chronology and dependency.

## Observational trace note

A separate private utility repository, `perplexity-model-watcher`, contains a browser extension that observes client-exposed Perplexity fields named `display_model` and `user_selected_model`. If you discuss these fields, treat them only as client-visible metadata. Do not treat them as proof of the exact backend model, inference route, serving weights, or internal architecture without independent platform evidence.

## Forbidden promotions

Do **not** promote any result to:

- independent human reproduction;
- external validation/adoption;
- patentability/novelty/legal validation;
- production readiness;
- release authorization;
- exact backend model identity from UI/network metadata;
- broader `PROVEN` status from a bounded CI pass.

## Required output contract

Return a compact report with these sections:

### A. Claim dispositions

For each of C1, C2, and C3, choose exactly one:

`SUPPORTED_WITHIN_SCOPE | CONTRADICTED | UNRESOLVED | OUT_OF_SCOPE`

For C3, also give a row-by-row disposition for each remembered assertion.

### B. Evidence table

For every material finding provide:

- source URL;
- repository and file/run;
- immutable commit/run identifier when available;
- what the source directly establishes;
- what it does **not** establish.

### C. Source-dependency analysis

State whether each item is an independent source, a repository derivative, a user/model assertion, or repeated synthesis of the same underlying source.

### D. Contradictions

Preserve all unresolved contradictions explicitly. Do not harmonize conflicting wording unless an artifact resolves it.

### E. New claims

Any new proposition must be labeled `PROPOSED` or `INFERRED` and must not be inserted into canonical project state merely because it appears plausible.

### F. Machine-readable summary

End with this object shape:

```json
{
  "exchange_id": "VG-XM-0001",
  "reviewer": "Perplexity",
  "claim_dispositions": {
    "VG-XM-0001-C1": "SUPPORTED_WITHIN_SCOPE|CONTRADICTED|UNRESOLVED|OUT_OF_SCOPE",
    "VG-XM-0001-C2": "SUPPORTED_WITHIN_SCOPE|CONTRADICTED|UNRESOLVED|OUT_OF_SCOPE",
    "VG-XM-0001-C3": "SUPPORTED_WITHIN_SCOPE|CONTRADICTED|UNRESOLVED|OUT_OF_SCOPE"
  },
  "unresolved_contradictions": [],
  "artifact_locators": [],
  "new_claims": [],
  "status_promotion_recommended": false
}
```

`status_promotion_recommended` must remain `false` in this exchange. The repository resolver will separately determine whether any canonical ledger/state update is justified by the returned evidence.
