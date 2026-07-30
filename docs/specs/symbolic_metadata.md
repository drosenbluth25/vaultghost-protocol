# VaultGhost™ Sub-Spec: Symbolic Metadata Containment

**Spec ID:** SMC-01  
**Module Type:** Evidence-Boundary Specification  
**Status:** Draft v1.2 — CI Reproduction Gate Blueprint  
**Lead Architect:** Daniel Rosenbluth | SDA-001  
**Recommended Path:** `docs/specs/symbolic_metadata.md`

---

## 1. Purpose

This sub-spec defines how VaultGhost handles symbolic, semantic, and stylistic authorship markers without conflating them with cryptographic proof, forensic provenance, legal ownership, or date priority.

The goal is to preserve symbolic continuity while preventing provenance inflation.

---

## 2. Evidence-Boundary Principle

A symbolic marker is a **contextual anchor**, not a **forensic anchor**.

VaultGhost must treat symbolic authorship signals as weak-to-contextual metadata unless they are independently supported by external evidence such as hashes, digital signatures, timestamp receipts, repository records, filed documents, or other admissible records.

### Standardized Framing

> `ΨΛ-⦻∿13 ∴ΞΩ/DR7` is a symbolic authorship signal associated with Daniel Rosenbluth’s semantic-recursive writing field. It may indicate continuity of conceptual origin or stylistic identity. It does **not** independently verify authorship, date, ownership, or legal priority without external evidence such as hashes, signatures, timestamps, repository records, or filed documents.

---

## 3. Evidence Matrix: Layered Verification

This matrix defines the functional limits of each evidence class.

| Metric | Symbolic / Semantic Marker | Cryptographic / Forensic Evidence |
| :--- | :--- | :--- |
| **Evidence Class** | Symbolic authorship/context marker | Cryptographic integrity/provenance mechanism |
| **Verification** | Heuristic/contextual; non-cryptographic | Mechanically verifiable within a defined trust model |
| **Claim Strength** | Weak-to-contextual | Strong but scope-limited |
| **May Support** | Continuity, identity signal, stylistic association | Byte integrity, signing event, timestamp existence, provenance assertion |
| **Does Not Prove** | Legal ownership, date priority, cryptographic authorship, independent origin | Legal ownership by itself; truth of every asserted claim |
| **Primary Vulnerabilities** | Spoofing, mimicry, prompt injection, symbolic copying | Key compromise, replay, custody gaps, metadata falsehoods, trust-chain failure |
| **VaultGhost Role** | Semantic Continuity Layer | Evidence Anchoring Layer |

---

## 4. Canonicalization & Unicode Policy

Symbolic markers containing uncommon glyphs must be canonicalized before hashing, comparison, or manifest inclusion.

### Requirements

- **Encoding:** UTF-8.
- **Normalization:** NFC, meaning Unicode Normalization Form Canonical Composition.
- **Literal Authority:** The literal UTF-8 marker string is authoritative.
- **Visual Renderings:** LaTeX, screenshots, styled text, or rendered previews are non-authoritative for byte-level verification.
- **Hashing Rule:** Any hash over the marker must be computed only after NFC normalization.

| Type | Representation |
| :--- | :--- |
| **Authoritative Marker** | `ΨΛ-⦻∿13 ∴ΞΩ/DR7` |
| **Non-Authoritative Visual Rendering** | `$\Psi\Lambda-\text{\textcircled{x}}\sim13 \therefore\Xi\Omega/\text{DR7}$` |

The LaTeX rendering may communicate visual meaning, but it is not byte-equivalent to the literal UTF-8 marker and must not be used as the canonical forensic representation.

---

## 5. Manifest Placement

Symbolic marker data must be stored under a dedicated `symbolic_metadata` block.

It must not be placed inside `cryptographic_signatures`, `timestamp_receipts`, `signature_payloads`, or any other field that implies mechanical verification.

### Required Separation

```text
asset_metadata
symbolic_metadata
cryptographic_signatures
```

This separation prevents symbolic markers from being misread as cryptographic seals.

---

## 6. Example Manifest Object

**Recommended Path:** `examples/symbolic_metadata.example.json`

The example manifest is a JSON instance. It is not the JSON Schema itself.

---

## 7. Claim Discipline Rules

VaultGhost implementations must enforce the following rules:

1. A symbolic marker must never be treated as proof of legal ownership.
2. A symbolic marker must never be treated as proof of date priority.
3. A symbolic marker must never be treated as cryptographic authorship.
4. A symbolic marker may support semantic continuity only when clearly labeled as contextual.
5. Cryptographic evidence may support integrity, timestamp existence, signing events, or provenance assertions, but it does not independently prove legal ownership or the truth of the underlying claim.
6. Any LLM-generated output describing symbolic metadata must distinguish between textual blueprint, generated file, downloadable artifact, committed repository object, and externally anchored evidence.

---

## 8. Generation Integrity Rule

**Conversational output does not equal artifact generation.**

An LLM must not claim that a file “has been generated” unless an actual retrievable artifact exists, such as:

- a downloadable file,
- a local file-system write,
- a committed repository object,
- a generated byte stream,
- or an externally accessible artifact.

If the model only outputs markdown, JSON, HTML, LaTeX, or code in conversation, the correct classification is:

```text
Artifact State: Textual Blueprint
Generation Status: Not physically generated
Retrievability: Conversation-only unless exported
```

---

## 9. Audit Posture

This sub-spec exists to preserve VaultGhost’s evidence discipline.

Symbolic metadata may be useful for continuity, identity signaling, and semantic pattern tracking. It is not forensic proof by itself.

Cryptographic evidence may be mechanically strong, but its claim scope remains limited. A valid signature proves a signing event under a trust model. A valid hash proves byte identity. A timestamp receipt supports existence at or before a time. None of these automatically proves legal ownership, authorship truth, or priority without external context.

---

## 10. Recommended Repository Layout

```text
docs/
  specs/
    symbolic_metadata.md

schemas/
  symbolic_metadata.schema.json

examples/
  symbolic_metadata.example.json

tests/
  test_symbolic_metadata_schema.py
```

---

## 11. Implementation Status

```text
Spec ID: SMC-01
Status: Draft v1.2 — CI Reproduction Gate Blueprint
Evidence Layer: Symbolic metadata containment
Claim Posture: Non-forensic unless externally anchored
Primary Risk Controlled: Provenance inflation
```

---

## 12. CI Reproduction Gate

SMC-01 v1.2 adds repository-hosted CI reproduction through GitHub Actions.

### CI Files

```text
.github/workflows/smc-01-validation.yml
pyproject.toml
```

### What a Green CI Run Supports

A successful CI run supports the claim that:

- the example manifest validates against the Draft 2020-12 JSON Schema;
- the symbolic authorship signal is NFC-normalized;
- `certified: false` requires all cryptographic subfields to be `null`;
- the validation can be reproduced in a stateless Ubuntu runner using Python 3.12.

### What a Green CI Run Does Not Prove

A successful CI run does not prove:

- legal ownership;
- date priority;
- independent authorship;
- third-party audit;
- cryptographic anchoring;
- semantic truth of the marker claim.

### Correct Post-CI Status

```text
Status: Draft v1.2 — CI Validation Passed
External Verification: Repository-hosted CI reproduction completed
Cryptographic Anchoring: Pending
Independent Human Audit: Not claimed
```
