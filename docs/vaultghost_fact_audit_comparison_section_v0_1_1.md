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
