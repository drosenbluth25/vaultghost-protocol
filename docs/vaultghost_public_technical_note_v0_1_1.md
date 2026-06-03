# VaultGhost™ v0.1: A Regression-Tested Claim-Governance Pipeline for Legal-Adjacent Evidence Workflows

**Status:** Draft public technical note  
**Version:** v0.1  
**Scope:** Legal-adjacent evidence governance, not legal advice  
**Release characterization:** Regression-tested protocol skeleton; not production-grade evidence infrastructure  

---

## Abstract

VaultGhost™ v0.1 is a legal-adjacent claim-governance pipeline designed to prevent compound natural-language assertions from collapsing facts, inferences, motives, contradictions, and legal conclusions into a single unsupported narrative. The protocol separates claim decomposition from evidentiary classification, then enforces deterministic bucket transitions and precedence rules through regression fixtures and evaluator scripts.

The core pipeline is:

```text
raw_statement
→ claim_splitting_preprocessor
→ atomic_claims
→ bucket_transition_engine
→ final_claim_packet
→ precedence_collision_checks
```

At v0.1, VaultGhost is best understood as a tested governance skeleton: a set of schemas, fixtures, evaluators, and reports that demonstrate disciplined claim-state handling under synthetic legal-adjacent conditions. It is not a legal-advice engine, litigation system, production evidence platform, or externally validated compliance standard.

---

## External Motivation and Related Work: FACT-AUDIT

FACT-AUDIT is relevant to VaultGhost because it identifies a neighboring failure mode in LLM factuality: static benchmarks and classification-only metrics are insufficient for evaluating how models produce, justify, and adapt their fact-checking behavior. The paper introduces an adaptive, agent-driven framework for dynamically evaluating LLM fact-checking, with explicit attention to justification production as well as verdict prediction.

VaultGhost adopts the same high-level concern—that fluent, plausible language can conceal weak support—but operates at a different layer of the stack.

| Dimension | FACT-AUDIT | VaultGhost v0.1 |
|---|---|---|
| Primary role | Evaluation framework | Claim-governance protocol skeleton |
| Main object | Model fact-checking performance | Claim state and evidence status |
| Core unit | Test scenario / model response | Atomic claim |
| Primary output | Evaluation results and model-centric analysis | Final claim packet with governed buckets |
| Justification concern | Evaluates justification quality | Prevents unsupported justification from upgrading claim status |
| Architecture | Adaptive multi-agent evaluation | Splitter, bucket engine, integration packet, precedence fixtures |
| Evidence governance | Not the central protocol layer | Central protocol concern |
| Legal-adjacent controls | Not the primary focus | Explicitly scoped for legal-adjacent evidence workflows |
| Hash/provenance release discipline | Not the paper’s focus | Release manifest and artifact hashes included in v0.1 candidate |

The relationship should therefore be stated narrowly:

> FACT-AUDIT provides external motivation for justification-sensitive and adaptive factuality evaluation. VaultGhost v0.1 is not an implementation of FACT-AUDIT and is not validated by FACT-AUDIT. VaultGhost addresses a distinct governance problem: how to decompose compound assertions into atomic claims, assign evidence-governed buckets, enforce precedence rules, and produce a final claim packet without allowing unsupported facts, legal conclusions, motives, or contradictions to merge into a single fluent narrative.

This distinction matters. FACT-AUDIT asks how to evaluate whether models fact-check well. VaultGhost asks how a downstream protocol should govern the evidentiary state of claims before they are rendered into a legal-adjacent memo or report. The two are compatible as research neighbors, but they should not be conflated.

VaultGhost’s contribution at v0.1 is not a new factuality benchmark. It is a reproducible protocol skeleton consisting of schemas, YAML fixtures, deterministic evaluators, passing reports, and a manifest. Its synthetic fixtures are not proof of production readiness; they are evidence that the protocol’s stated rules and evaluator behavior are aligned under controlled legal-adjacent conditions.

A conservative description is:

> FACT-AUDIT motivates the importance of adaptive, justification-sensitive factuality assessment. VaultGhost v0.1 operationalizes a narrower governance layer for legal-adjacent claim handling: split first, classify second, enforce precedence third, render last.

That is the defensible framing.

---

## Problem Statement

LLM-generated legal-adjacent summaries can fail in a specific way: they blend different epistemic objects into one persuasive sentence.

Example pattern:

```text
The court order halted the foreclosure, proving the foreclosure was legally defective.
```

This sentence contains at least two different claim types:

1. A document/procedural claim: a court order halted the foreclosure.
2. A legal conclusion: the foreclosure was legally defective.

A normal summarizer may treat both as one coherent statement. VaultGhost forces them apart. The document fact may be eligible for verification if supported by a reliable source; the legal conclusion must remain blocked, inferred, or quarantined unless directly supported by a court, counsel, or authoritative legal source.

The governing principle is:

> A source can verify only what it directly supports, not every inference built on top of it.

---

## Core Design Principles

### 1. Default Quarantine

Every claim begins in `QUARANTINED` unless evidence earns a higher status.

### 2. Claim Splitting Before Classification

The splitter decomposes compound statements into atomic claims. It does not assign final evidentiary buckets.

### 3. Evidence-Governed Bucket Transitions

The bucket engine assumes atomic claims and assigns evidentiary status based on source type, support relation, provenance, contradiction, and legal-conclusion constraints.

### 4. Precedence Before Presentation

Rule collisions are tested before UI/memo rendering. This prevents a polished interface from freezing unstable semantics.

### 5. Synthetic-First Hardening

Synthetic fixtures are used first because they are portable, counsel-safe, and cleaner for testing collision behavior. Real private materials should be introduced only after public-safe synthetic suites pass.

---

## Bucket Model

VaultGhost v0.1 uses six core buckets:

| Bucket | Meaning |
|---|---|
| `VERIFIED` | Directly supported by reliable evidence, with no material conflict. |
| `PROVISIONALLY_VERIFIED` | Directly supported, but with caveats such as OCR uncertainty, unofficial copy status, incomplete context, or provenance uncertainty. |
| `INFERRED` | Reasonable conclusion drawn from evidence, but not directly stated by a reliable source. |
| `USER_ORIGINATED` | Asserted by the user and tracked as input, not externally verified fact. |
| `QUARANTINED` | Unsupported, unsafe, vague, unverifiable, speculative, or blocked from confident assertion. |
| `CONTRADICTED` | Reliable evidence materially conflicts with the claim. |

---

## Tested Layers

### Layer 1 — Claim-Splitting Preprocessor

**Purpose:** Decompose messy statements into atomic claims.  
**Boundary:** Does not assign final buckets.  
**Regression status:** 12/12 fixtures passing.

Covered split families include:

- document fact + legal conclusion
- event fact + motive/intent claim
- attribution + downstream legal consequence
- conflicting dates
- payment fact + procedural inference
- service attempt + legal sufficiency
- missing attachment + downstream procedural claim
- already-atomic claim that should not be split

### Layer 2 — Bucket Transition Engine

**Purpose:** Assign claim buckets based on evidence.  
**Boundary:** Assumes atomic claims; does not split language.  
**Regression status:** 12/12 fixtures passing.

Covered evidence behaviors include:

- fake citation → `QUARANTINED`
- user-only statement → `USER_ORIGINATED`
- attorney email support → `PROVISIONALLY_VERIFIED`
- official docket date → `VERIFIED`
- screenshot without official receipt → `PROVISIONALLY_VERIFIED`
- real document with overreaching legal inference → `INFERRED`
- conflicting records → `CONTRADICTED`
- AI memory only → `QUARANTINED`
- OCR uncertainty → `PROVISIONALLY_VERIFIED`
- unsupported motive claim → `QUARANTINED`

### Layer 3 — End-to-End Integration Pipeline

**Purpose:** Run raw statement → split claims → bind evidence → classify claims → assemble final packet.  
**Regression status:** 8/8 fixtures passing.

Packet-level invariants include:

```text
all_claims_started_quarantined = true
splitter_assigned_no_final_buckets = true
bucket_engine_received_only_atomic_claims = true
legal_conclusions_do_not_inherit_verification = true
motive_claims_do_not_inherit_event_verification = true
missing_sources_do_not_inherit_verification = true
```

### Layer 4 — Precedence Collision Suite

**Purpose:** Test rule collisions after the basic pipeline passes.  
**Regression status:** 12/12 fixtures passing.

The accepted v0.1 precedence order is:

```text
manual_override_validation_check
fabricated_or_invalid_source_block
missing_source_block
material_contradiction_check
explicit_motive_intent_block
legal_conclusion_block
user_corroboration_check
direct_support_check
indirect_support_check
fallback_quarantine
```

Covered collision behaviors include:

- contradiction outranks positive support
- missing source outranks tier-2 contextual support
- manual override cannot force `VERIFIED`
- user + weak corroboration upgrades only to `INFERRED`
- mixed evidence tiers select strongest reliable direct source
- motive/intent claims do not inherit verification from real filings
- legal conclusions disguised as procedural facts are blocked
- AI memory is ignored when independent official evidence exists
- primary sources with provenance uncertainty are capped at `PROVISIONALLY_VERIFIED`

---

## Key v0.1 Precedence Decision

During collision testing, a motive/intent claim containing the phrase “improper fee” exposed an ambiguity: it could be caught by generic legal-substance detection instead of the motive/intent block.

VaultGhost v0.1 resolves that ambiguity as follows:

> Explicit motive/intent classification outranks generic legal-substance detection.

Reason: motive and intent claims are high-risk hallucination channels. They should be quarantined directly rather than softened into legal inference.

---

## What VaultGhost v0.1 Is

VaultGhost v0.1 is:

- a regression-tested claim-governance skeleton
- a legal-adjacent evidence discipline
- a pipeline for separating atomic claims from narrative compression
- a fixture-driven protocol for preventing unsupported evidentiary upgrades
- a testable framework for handling claim buckets and rule precedence

## What VaultGhost v0.1 Is Not

VaultGhost v0.1 is not:

- legal advice
- a court-recognized evidence system
- a production litigation platform
- a general NLP parser
- a factuality benchmark competing with FACT-AUDIT
- proof of external institutional validation
- proof that any real legal matter has a particular legal outcome

---

## Release Artifacts

The v0.1 release candidate includes:

1. Claim-splitting spec, fixtures, evaluator, and report.
2. Bucket transition fixtures, evaluator, and report.
3. Final claim packet schema.
4. End-to-end integration fixtures, evaluator, and report.
5. Precedence decision record, fixtures, evaluator, and report.
6. Public release manifest with SHA-256 hashes.

See:

```text
vaultghost_public_release_manifest_v0_1.json
```

---

## Recommended Next Steps

### 1. Add Manifest and Hash Enforcement

The next engineering layer should verify that every protocol artifact is present, hashable, and consistent with the public release manifest.

### 2. Add JSON Schema Validation

The YAML and JSON artifacts should be validated against explicit schema definitions.

### 3. Add Private Real-Case Fixture Layer

After synthetic suites remain stable, create a separate private fixture layer using redacted legal-adjacent examples. This layer should not be merged into public fixtures.

### 4. Add Memo Renderer Last

Only after schemas, hashes, fixtures, and private-case tests stabilize should VaultGhost render human-facing legal-adjacent memos.

---

## Bottom Line

VaultGhost v0.1 demonstrates a concrete design pattern:

> Split claims before classifying them. Classify claims before rendering them. Test rule collisions before trusting the output.

That is the spine of the protocol.
