---
title: Users and Journeys
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---


# 2. Users, Systems, and Jobs To Be Done

## Primary actors

### Content Harness and Harness Maintainer
Owns demand meaning, sequence and composition authority, budget authorization, demand versions, amendments, cancellation, and result acknowledgement.

### Visual Asset Editor and Visual Production Maintainer
Owns production planning, resource selection, candidate generation, evaluation, repair, production acceptance, and production lineage.

### Delegation Protocol Maintainer
Maintains schemas, lifecycle machine, authority rules, compatibility, adapters, boundary services, audit, conformance, and release certification.

### Composition Runtime
Consumes only acknowledged, current Asset Results and records exact usage.

### Operations and Security Owner
Observes stalled or compromised delegations, trust failures, SLOs, audit chains, and incident response.

### Conformance and Release Engineer
Runs producer, consumer, authority, lifecycle, compatibility, migration, resilience, and Format 02 end-to-end suites.

## Non-users

The Delegation Protocol is not a manual art workstation, a ComfyUI workflow editor, a visual evaluator, a content ideation system, or an independent creative agent.

## Key user and system journeys

### UJ-01 — A Content Harness submits an authoritative demand

A registered Content Harness submits one immutable Visual Asset Demand through a compatible envelope and receives an idempotent submission receipt.

### UJ-02 — The boundary negotiates a safe protocol profile

The Delegation Layer checks versions, required features, category certification and authority before accepting the delegation.

### UJ-03 — The Visual Asset Editor reports progress without exposing internals

The editor emits product events that project into a stable external lifecycle while internal production nodes remain private.

### UJ-04 — The Content Harness acknowledges a current result

The editor returns a production-accepted result; the Content Harness validates current demand, sequence, composition and dependencies before automatic consumption acknowledgement.

### UJ-05 — A demand changes while production is in flight

The Content Harness submits a superseding version with typed changes; valid work is reused and only affected work is invalidated.

### UJ-06 — The editor proposes a feasible amendment

The editor returns structured amendment options with evidence and predicted effects; the owning authority accepts one through a new demand version or declines.

### UJ-07 — The editor requests more budget

The editor checkpoints and requests an immutable budget extension when the authorized envelope is insufficient; production resumes only after valid approval.

### UJ-08 — A no-longer-needed delegation is cancelled

The Content Harness requests cancellation; queued work stops, atomic work reaches a safe checkpoint, useful evidence is retained and stale promotion is prevented.

### UJ-09 — A scene coordinates several related assets

A Delegation Set coordinates independent character, background and prop demands with shared identity, palette, geometry and atomic completion policy.

### UJ-10 — A failure routes to the correct authority

A typed failure identifies the responsible system, retry class, decision owner, remaining valid artifacts and required next action.

### UJ-11 — Products interoperate across versions

A compatibility manifest and negotiation select a safe pinned profile, use a lossless adapter or produce an immutable migration.

### UJ-12 — A completed asset is invalidated and replaced

A later regression or constitution update triggers an impact notice, blocks unsafe use, preserves history and revalidates a replacement.

### UJ-13 — The protocol rejects a forged or replayed action

Identity, signature, authority and replay checks reject the message before lifecycle state changes and record a security incident receipt.

### UJ-14 — An operator observes and certifies the shared boundary

The Control Tower shows lifecycle, authority, compatibility, budget, events, exceptions, acknowledgements and audit-chain state while conformance suites prove behavior.
