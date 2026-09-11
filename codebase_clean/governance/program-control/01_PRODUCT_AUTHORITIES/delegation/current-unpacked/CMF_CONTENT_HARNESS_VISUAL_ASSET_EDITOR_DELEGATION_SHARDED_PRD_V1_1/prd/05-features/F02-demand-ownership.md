---
title: F02 — Visual Asset Demand Ownership, Immutability, and Authority
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-14'
feature_id: F02
decision_id: D002
---


# F02 — Visual Asset Demand Ownership, Immutability, and Authority

## User outcome

The Content Harness can express and evolve visual intent without production systems silently changing it.

## Product behavior

The Content Harness exclusively owns Visual Asset Demand meaning and versions; the protocol validates ownership while the VAE may derive plans, annotate feasibility, and propose amendments.

## Brownfield baseline

The VAE PRD defines Visual Asset Demand as authoritative input and semantic non-mutation as a constitutional law.

## Required product delta

Add field-level ownership, immutable acceptance, version identity, and prohibited mutation tests at the shared boundary.

## Traceability

- **Locked decision:** `D002`

- **User journeys:** `UJ-01`, `UJ-05`, `UJ-06`

- **Cross-cutting NFRs:** `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

## Functional Requirements

### FR-009 — Exclusive demand ownership

**Requirement:** Only the registered owning Content Harness shall create or supersede authoritative Visual Asset Demand versions.

**Testable consequences:**

- The demand owner is recorded in the envelope and payload.

- Submissions from non-owners are rejected as authority failures.

**Failure examples:**

- The VAE publishes a modified demand as authoritative.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-010 — Immutable accepted demand

**Requirement:** An accepted demand version shall be immutable and addressed by request ID, version, payload hash, and canonical reference.

**Testable consequences:**

- In-place updates are rejected.

- Every execution pins the exact accepted demand identity.

**Failure examples:**

- A database row is overwritten while production is in progress.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-011 — Field-level authority map

**Requirement:** Every authoritative demand field shall map to an owner and authority class covering Activative semantic lineage, Activation Contract, Expression Moment lineage, Visual Semantics, Visual Narrative, Feature Contracts, somatic route, sequence, composition, identity, continuity, wrong-reading locks, delivery, and budget domains.

**Testable consequences:**

- The boundary can reject an unauthorized field change deterministically.

- Unknown authoritative fields block acceptance until registered.

**Failure examples:**

- An adapter drops a wrong-reading lock, Expression Moment reference, recognition carrier, viewer role, or Visual Narrative field because it does not recognize the field.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-012 — Optional notes separation

**Requirement:** Free-form notes shall be treated as non-authoritative enrichment and shall never override typed demand fields.

**Testable consequences:**

- Conflicts are resolved in favor of typed fields.

- Notes are preserved with provenance for specialist context.

**Failure examples:**

- A note saying 'ignore the BBOX' changes the composition contract.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-013 — Permitted derived artifacts

**Requirement:** The VAE may derive Visual Production Plans, geometry recommendations, feasibility reports, evaluations, and amendment proposals without acquiring demand ownership.

**Testable consequences:**

- Derived artifacts cite the exact demand version.

- They declare their own producer and authority.

**Failure examples:**

- A production plan is presented as a new demand version.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-014 — Amendment-only feedback

**Requirement:** Any VAE-requested change to a demand-owned field shall be expressed through a typed non-binding Amendment Proposal.

**Testable consequences:**

- No accepted demand is changed by the proposal.

- The Content Harness may accept, reject, or supersede.

**Failure examples:**

- The VAE relaxes continuity because generation is difficult.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-015 — Demand identity propagation

**Requirement:** Every submission, event, result, failure, amendment, and receipt shall carry or resolve to the exact demand ID, version, and hash.

**Testable consequences:**

- Stale events can be detected.

- Audit reconstruction identifies the governing demand.

**Failure examples:**

- A result identifies only the request ID, not the demand version.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-016 — No implicit authority transfer

**Requirement:** Submission, acceptance, execution, or budget escalation shall not transfer semantic or composition authority to the VAE or protocol.

**Testable consequences:**

- Authority remains stable through the lifecycle.

- Any proposed ownership change requires upstream governance.

**Failure examples:**

- The service assumes that production acceptance makes it owner of the composition role.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

## Feature failure conditions

- Accepted demand mutated in place.

- Untyped note overrides authoritative contract.

- VAE output masquerades as demand authority.

## Explicitly out of scope

- Internal VAE planning

- Content Harness idea-generation workflow

- Human art-direction UI
