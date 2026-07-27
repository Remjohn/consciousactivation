---
title: Architecture Handoff
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: ready_for_architecture_after_prd_approval
created: '2026-07-13'
updated: '2026-07-13'
---

# Architecture Handoff — Delegation Protocol

## Architecture objective

Translate this PRD into an executable, transport-independent cross-product boundary without changing the locked authority model or frozen upstream architectures.

## Required architecture views

1. **Context and authority view**
   - Content Harness, Visual Asset Editor, composition runtime, operator/policy, boundary services
   - field-level authority and prohibited actions
2. **Contract and schema view**
   - common envelope
   - contract registry
   - schema/version resolution
   - stable resource references and hashes
3. **Lifecycle and event view**
   - executable transition machine
   - authoritative message mappings
   - projection rebuild
   - timeout and terminal-state behavior
4. **Trust and integrity view**
   - principal registry
   - credential issuance/rotation/revocation
   - signing, hashing, replay protection
   - audit-chain durability
5. **Compatibility view**
   - product manifests
   - negotiation
   - adapter and migration services
   - deprecation
6. **Coordination view**
   - supersession and selective invalidation
   - amendments
   - budgets
   - cancellation
   - Delegation Sets
   - result acknowledgement
   - post-completion notices
7. **Deployment and transport view**
   - HTTP/queue/event/local fixture adapters
   - durable stores
   - high availability
   - backpressure
   - object/contract storage resolution
8. **Observability and conformance view**
   - Control Tower projections
   - SLO instrumentation
   - conformance runner
   - fault injection
   - incidents

## Required architecture components

- Delegation API / boundary gateway
- Principal and authority service
- Schema and Message Type Registry
- Compatibility negotiator
- Deterministic adapter and migration runner
- Idempotency and replay service
- Lifecycle machine and projection service
- Durable message/event store
- Append-only audit-chain service
- Transport adapters and router
- Supersession and selective-invalidation coordinator
- Budget and escalation coordinator
- Cancellation and deadline coordinator
- Amendment exchange coordinator
- Result acknowledgement and post-completion governance service
- Delegation Set dependency and impact service
- Control Tower projection adapter
- Shared conformance and fixture runner

## Mandatory ADRs

1. Canonical transport and delivery guarantees
2. Event/message and audit storage
3. Idempotency, ordering and race resolution
4. Principal identity, signing and key rotation
5. Contract/schema registry and resource URI resolution
6. Compatibility negotiation, adapters and migration
7. Lifecycle projection and rebuild
8. Control Tower integration
9. High availability, backpressure and disaster recovery
10. Format 02 reference deployment topology

## Architecture prohibitions

Architecture may not:

- place semantic or production judgment inside boundary services;
- expose VAE internal production nodes as protocol states;
- depend on exactly-once transport without idempotency;
- use one mutable delegation row as the only historical truth;
- introduce lossy compatibility handling;
- bypass audit persistence for state-changing actions.


## Constitutional semantic-preservation requirements

The implementation must preserve the complete Activative semantic lineage, Activation Contract, Visual Semantic Pack, Visual Narrative Program, Feature Contracts, T/V request, Expression Moment lineage, and wrong-reading locks through schemas, adapters, migrations, hashes, authority checks, and compatibility tests. Parseability without behavioral enforcement is incompatible.
