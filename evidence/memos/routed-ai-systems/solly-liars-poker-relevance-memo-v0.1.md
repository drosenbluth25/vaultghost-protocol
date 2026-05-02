# VaultGhost Relevance Memorandum -- Routed AI Systems, Specialized RL Agents, and the Provenance Gap

## Status

Draft v0.1. External technical relevance memo.

This memorandum does **not** allege copying, adoption, infringement, awareness, derivation, or legal validation. It documents why the Solly/Liar's Poker research is technically relevant to VaultGhost's broader thesis that hybrid, routed AI systems increase the need for provenance, verification, replayability, and evidence-layer records.

## Source Reviewed

1. Richard Dewey, Janos Botyanszki, Ciamac C. Moallemi, Andrew T. Zheng, "Outbidding and Outbluffing Elite Humans: Mastering Liar's Poker via Self-Play and Reinforcement Learning," arXiv:2511.03724.
   - https://arxiv.org/abs/2511.03724
2. Richard Dewey, Janos Botyanszki, Ciamac C. Moallemi, Andrew Zheng, "Beyond Reasoning: RL-Policy Guided LLM Inference for Efficient Strategy in Liar's Poker," OpenReview.
   - https://openreview.net/forum?id=1JC8EZfCPb

## Executive Summary

The Solly/Liar's Poker paper is relevant to VaultGhost because it supports a broader architectural premise: advanced AI systems are unlikely to remain simple, monolithic LLM interfaces. Instead, they are likely to become routed systems that combine general-purpose language models, reinforcement-learning agents, search systems, tools, and specialized policy modules.

The paper reports that Solly, a specialized reinforcement-learning agent trained through self-play, achieved elite-human-level performance in reduced-format Liar's Poker and outperformed tested LLMs on the same metrics. The OpenReview listing further states that Solly's policies, when provided to LLMs as domain-specific guidance, improved LLM performance and reduced token costs.

This does not prove any connection to VaultGhost. It does, however, strengthen the technical case for provenance records that identify which model, policy, tool, or subsystem acted during an AI-mediated event.

## Facts

1. The arXiv paper presents Solly as a specialized AI agent for reduced-format Liar's Poker.
2. The paper describes Liar's Poker as a multi-player, imperfect-information game involving uncertainty and strategic reasoning.
3. Solly was trained using self-play with a model-free actor-critic deep reinforcement-learning algorithm.
4. The paper reports that Solly achieved elite-human-level performance in reduced-format Liar's Poker.
5. The paper reports that Solly outperformed large language models, including reasoning-capable LLMs, on the same metrics.
6. The OpenReview listing describes the work using the keywords: multi-agent, self-play, reinforcement learning, and large language models.
7. The OpenReview listing states that Solly's policies, when used as domain-specific guidance for LLM inference, improved LLM performance and decreased token costs.

## Inferences

1. General-purpose language competence and specialized strategic competence are separable.
2. A general LLM can be a powerful interface without being the optimal decision engine for every adversarial or uncertainty-heavy task.
3. Specialized reinforcement-learning systems may outperform frontier LLMs in narrow domains where success depends on randomized policy, bluffing, opponent modeling, and exploitability resistance.
4. Future AI systems may increasingly route tasks across different architectures rather than rely on one universal model.
5. Routed AI systems create a larger provenance problem because users and auditors may not know which subsystem actually shaped an output.

## VaultGhost Relevance

VaultGhost is relevant because it is designed as an evidence-layer protocol for AI-mediated events. If an AI system routes work across an LLM, reinforcement-learning policy, search system, tool, or other specialized subsystem, then a reliable record should preserve:

- model or subsystem identity
- input state
- output state
- routing decision
- policy guidance, if any
- tool invocation record, if any
- verification status
- replayability conditions
- evidence hashes
- signature or timestamp evidence where applicable

The Solly paper strengthens the technical plausibility of this need. Once different AI architectures can produce materially different performance under different strategic conditions, the user cannot treat "the AI answered" as a sufficient record of what happened.

## Unsupported Claims to Avoid

This memo does not claim:

- that the authors copied VaultGhost
- that the authors were aware of VaultGhost
- that the paper adopts VaultGhost
- that the paper infringes VaultGhost
- that the paper legally validates VaultGhost
- that LLMs are weak or obsolete
- that reinforcement-learning agents are universally superior
- that Liar's Poker results automatically generalize to law, finance, negotiation, intelligence, or other real-world strategic domains
- that every future AI system will necessarily use the exact architecture anticipated by VaultGhost

## Recommended Public Statement

The Solly/Liar's Poker paper is relevant to VaultGhost because it reinforces a broader technical premise: as AI systems increasingly combine general-purpose LLM interfaces with specialized strategic engines, provenance, routing transparency, replayability, and verification become more important.

The point is not that LLMs are weak. The point is that LLMs are not universal optimal decision engines. A system may need to route between language models, reinforcement-learning policies, tools, search systems, and domain-specific modules. When that happens, users and auditors need evidence of what acted, when it acted, what inputs were used, what constraints applied, and whether the result can be replayed or verified.

## Proposed Repository Classification

Artifact type: external relevance memorandum  
Legal posture: non-accusatory  
Evidence posture: third-party technical relevance  
Repository location: `evidence/memos/routed-ai-systems/`  
Suggested filename: `solly-liars-poker-relevance-memo-v0.1.md`

## Final Thesis

This paper does not diminish LLMs. It clarifies them. LLMs are powerful general-purpose cognitive interfaces, but they are not universal optimal decision engines. In adversarial, uncertainty-heavy, multi-agent domains, specialized training regimes can outperform general language reasoning.

That strengthens the case for routed, evidence-tracked, hybrid AI systems -- and for protocols designed to preserve verifiable records of AI-mediated events.
