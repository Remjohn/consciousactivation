---
title: Canonical Glossary
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---


# 4. Canonical Glossary

Downstream artifacts must use these terms consistently. Synonyms that blur authority are prohibited.

- **Delegation Protocol** — The governed contract protocol and deterministic boundary services connecting a Content Harness and Visual Asset Editor without becoming a third creative authority.

- **Delegation Envelope** — The common versioned metadata wrapper carrying message identity, correlation, causation, principals, authority, integrity, idempotency, and payload reference.

- **Visual Asset Demand** — The immutable, versioned, Content Harness-owned contract expressing semantic intent, Activative purpose, visual role, composition intent, continuity, delivery, evaluation, and budget authority.

- **Visual Asset Editor** — The independently versioned production authority that derives and executes Visual Production Plans and certifies production acceptance.

- **Content Harness** — The atomic product authority that owns the Visual Asset Demand and acknowledges current downstream consumption compatibility.

- **Delegation Correlation** — The complete lifecycle of one delegated visual request, identified by a correlation ID.

- **Causation ID** — The message identifier that directly caused a later message.

- **Submission Receipt** — The protocol acknowledgement that a submitted delegation was validated and accepted or rejected at the boundary.

- **Production Acceptance** — The Visual Asset Editor's certification that an asset satisfies the authorized demand and production gates.

- **Consumption Acknowledgement** — The Content Harness or composition runtime's confirmation that a production-accepted result is current and compatible for downstream use.

- **Delegation Set** — A versioned coordination contract grouping independent Visual Asset Demands under shared continuity, dependency, and completion constraints.

- **Supersession** — The authority-scoped replacement of one immutable demand version by a newer linked version.

- **Selective Invalidation** — The explicit preservation of unaffected artifacts and invalidation of only those results or nodes impacted by an authoritative change.

- **Amendment Proposal** — A typed, non-binding VAE proposal describing exact demand changes, authority class, evidence, and predicted consequences.

- **Budget Authorization** — The immutable Content Harness-owned envelope defining approved Budget Program, ceilings, purpose, and escalation policy.

- **Compatibility Manifest** — A machine-readable declaration of accepted/emitted protocol versions, message versions, features, profiles, and limitations.

- **Negotiated Delegation Profile** — The pinned protocol, message, feature, category, adapter, and migration configuration accepted for one delegation.

- **Lifecycle Projection** — The stable shared state derived from accepted authoritative messages, distinct from either product's internal state machine.

- **Failure Taxonomy** — The protocol-owned stable classification of unsuccessful conditions, responsibility, retry, invalidation, and next-authority semantics.

- **Invalidation Notice** — A post-completion message requiring current-use revalidation without necessarily declaring an asset defective.

- **Revocation Notice** — A post-completion message immediately blocking new or active consumption for a critical defect, integrity, security, or regression reason.

- **Replacement Notice** — A typed link from an affected result or asset to a new candidate for future use, still requiring compatibility validation.

- **Delegation Audit Receipt** — An append-only chained record of identity, integrity, schema, authority, lifecycle, and persistence validation for a message.

- **Protocol Principal** — A registered product, runtime, service, operator, or policy identity permitted to perform defined delegation actions.

- **Replay** — A previously valid signed message reused outside its permitted idempotent or lifecycle context.

- **Conformance Suite** — The shared executable producer, consumer, authority, lifecycle, compatibility, integrity, and resilience tests for the protocol.

- **Development Capsule** — The implementation-ready governed package containing approved product, architecture, contracts, fixtures, tests, migration, observability, and authorization evidence.
