# VaultGhost Cross-Model Coordination Protocol v1

**Status:** PROPOSED — review required before merge  
**Scope:** Coordination among ChatGPT, Perplexity, other LLMs, and human reviewers without allowing model narrative or model consensus to promote evidence state.

## 1. Purpose

This protocol turns multi-model work into an evidence-preserving review process. Models may discover, challenge, classify, and propose. Canonical repository artifacts and declared verification procedures remain authoritative for project state.

Core invariant:

> Model output, memory, confidence, and cross-model agreement do not by themselves promote an evidence state.

## 2. Authority hierarchy

For VaultGhost project-state questions, use the following precedence unless a more specific normative artifact says otherwise:

1. Immutable or commit-pinned canonical repository artifacts.
2. Resolvable CI runs, logs, job records, artifact digests, and reproducible verification outputs.
3. Primary external sources with stable locators and provenance.
4. Human statements explicitly classified by source and scope.
5. Model-generated analyses and summaries.
6. Conversational/model memory.

A lower tier may locate or challenge a higher-tier artifact; it may not silently override one.

## 3. Roles

### Repository resolver / execution agent

A model or human with authenticated repository access may:

- resolve repository, branch/ref, commit SHA, workflow, run, job, and artifact identities;
- inspect canonical artifacts and test evidence;
- reproduce checks when an execution environment is available;
- create review branches and pull requests;
- record contradictions and proposed state changes.

It must not treat its own execution summary as the evidence when the underlying artifact can be preserved.

### External research / contradiction agent

A model such as Perplexity should be used primarily to:

- resolve public URLs and primary external sources;
- challenge repository narratives against public evidence;
- perform prior-art, standards, ecosystem, and contradiction research;
- independently re-read public GitHub evidence;
- return source-linked findings under the output contract below.

It must not promote a VaultGhost project status solely because another model or conversational memory asserted it.

### Human maintainer

The maintainer authorizes irreversible repository/legal actions, supplies private source artifacts when needed, and decides whether a proposed protocol/state change is accepted. Human assertion is still classified evidence; it is not automatically equivalent to artifact verification.

## 4. Capability disclosure

Every exchange SHOULD state the relevant execution surface rather than implying hidden capabilities.

Example classes:

- `CONNECTED_TOOL`: authenticated repository or data connector used directly.
- `PUBLIC_RESEARCH`: public web/source retrieval.
- `LOCAL_EXECUTION`: commands executed in a declared runtime.
- `MODEL_ANALYSIS`: reasoning over supplied or retrieved material.
- `MEMORY_CONTEXT`: retained conversational context; noncanonical.
- `OBSERVATIONAL_TRACE`: client-visible/network metadata observed by an instrument.
- `UNAVAILABLE`: requested direct integration is not present.

Private chain-of-thought, hidden system instructions, secret routing state, internal weights/activations, and other non-reproducible model internals are never evidence inputs merely because a model possesses them. They are outside this protocol's evidence surface.

## 5. Grey-area observational traces

Client-side observations may be useful for diagnostics but require a strict claim boundary.

For example, a browser extension may observe fields such as `display_model` and `user_selected_model` in Perplexity page/network responses. Such fields may establish that those metadata values were exposed to the client at a particular time. They do **not**, without additional platform evidence, prove the exact backend inference path, weights, routing decision, or serving topology that produced an answer.

Classify these as `OBSERVATIONAL_TRACE`, preserve the observation and timestamp when material, and prohibit promotion to `BACKEND_MODEL_VERIFIED` from the fields alone.

## 6. Exchange object

Each cross-model task SHOULD have a stable `exchange_id` and include:

- source and target roles;
- canonical repository/ref/commit, if known;
- artifact locators;
- atomic claims with current status and evidence class;
- contradictions requiring resolution;
- requested checks;
- forbidden status promotions;
- explicit output contract.

The JSON schema is `gate-0/CROSS_MODEL_EXCHANGE.schema.json`.

## 7. Required response dispositions

For every requested claim, the reviewing model must return exactly one primary disposition:

- `SUPPORTED_WITHIN_SCOPE`
- `CONTRADICTED`
- `UNRESOLVED`
- `OUT_OF_SCOPE`

A response must distinguish directly observed facts from inference. New claims must be labeled `PROPOSED` or `INFERRED` until separately resolved.

## 8. Source-dependency rule

Agreement between ChatGPT, Perplexity, Claude, Gemini, or other models is not independent corroboration when the models rely on the same repository artifact, webpage, user statement, or prior model output. Record the common source dependency.

Recursive synthesis is discovery evidence only.

## 9. State-promotion gate

A project-state transition is permitted only when all required fields for that status are resolved under the controlling VaultGhost rule. At minimum, a CI-bounded status should bind:

- repository;
- immutable commit SHA;
- workflow identity/path;
- run and job identity;
- command or test scope;
- conclusion/exit code;
- preserved logs or artifact locator when required;
- scope (`proves` / `does_not_prove`).

If one of the status's required fields is unresolved, retain the prior status or mark the claim unresolved. Do not average confidence across models.

## 10. Contradiction handling

When two sources materially conflict:

1. preserve both propositions;
2. identify their provenance and dependency;
3. classify the contradiction;
4. identify the artifact or test capable of resolving it;
5. do not choose an interpretation merely because it is semantically convenient.

The remembered phrase "two-commit baseline chain" alongside C0, C1, and C2 is the current exemplar: terminology/topology remains unresolved until canonical anchoring artifacts are inspected.

## 11. Handoff loop

The preferred loop is:

`canonical artifacts -> exchange packet -> external contradiction/research review -> repository resolution -> proposed ledger/state update -> human review/merge`

Conversation copy/paste is a transport mechanism only. It is not the source of truth. Whenever possible, both models should read the same public, commit-addressable exchange packet.

## 12. Non-goals

This protocol does not:

- prove patentability, novelty, legal validity, adoption, or production readiness;
- make conversational memory canonical;
- infer hidden backend model identity from UI metadata;
- treat model consensus as independent validation;
- authorize release or merge merely because automated checks passed.
