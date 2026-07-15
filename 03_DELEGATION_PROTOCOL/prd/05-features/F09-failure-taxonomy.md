---
title: F09 — Protocol Failure Taxonomy, Responsibility, and Recovery Semantics
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F09
decision_id: D009
---


# F09 — Protocol Failure Taxonomy, Responsibility, and Recovery Semantics

## User outcome

Every unsuccessful condition routes to the correct owner and recovery path without blind retries or cross-product confusion.

## Product behavior

The protocol owns stable failure families/codes and required semantics; products attach diagnostics without redefining shared meaning.

## Brownfield baseline

The VAE PRD distinguishes contract, authority, compatibility, infrastructure, quality, budget, human, and integrity failures.

## Required product delta

Create a canonical taxonomy, typed failure envelope, retry/round rules, invalidation semantics, and partial-result behavior.

## Traceability

- **Locked decision:** `D009`

- **User journeys:** `UJ-10`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

## Functional Requirements

### FR-065 — Canonical failure families

**Requirement:** The protocol shall define stable families for contract, authority, compatibility, staleness, feasibility, infrastructure, quality, budget/timing, human exception, and security/integrity failures.

**Testable consequences:**

- Every registered code belongs to one family.

- Unknown product diagnostics map to a stable fallback family.

**Failure examples:**

- All failures are returned as FAILED with prose.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-066 — Stable failure codes

**Requirement:** Each protocol code shall have an immutable semantic definition, severity range, terminality rule, and recovery class.

**Testable consequences:**

- Clients can branch deterministically.

- Deprecated codes publish replacements.

**Failure examples:**

- The same code means retryable in one product and terminal in another.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-067 — Responsibility and decision ownership

**Requirement:** Every failure message shall identify detector, responsible system, next-decision owner, and enforcement owner.

**Testable consequences:**

- Cross-product responsibility is explicit.

- The Control Tower displays the next owner.

**Failure examples:**

- A VAE feasibility failure has no indication that the Content Harness must decide.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-068 — Retry classification

**Requirement:** Failures shall state whether retry is permitted, whether payload changes are required, and which retry class applies.

**Testable consequences:**

- Contract failures require corrected immutable messages.

- Infrastructure failures may use operational retries.

**Failure examples:**

- An unchanged authority violation is retried three times.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-069 — Quality-round accounting

**Requirement:** The protocol shall distinguish infrastructure recovery from VLM-directed quality-repair rounds and shall enforce the declared remaining quality rounds.

**Testable consequences:**

- GPU restart does not consume a quality round.

- A semantic-fidelity repair does.

**Failure examples:**

- Every error decrements the same retry counter.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-070 — Invalidation and preservation semantics

**Requirement:** Failure contracts shall identify affected artifacts or nodes, preserved valid outputs, and downstream state impact.

**Testable consequences:**

- Targeted repair can reuse unaffected work.

- Terminal failures block inappropriate promotion.

**Failure examples:**

- A pose failure invalidates the background plate without explanation.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-071 — Partial-result protocol

**Requirement:** The protocol shall support typed partial results with accepted roles, unresolved roles, failures, and an original completion policy.

**Testable consequences:**

- Partial consumption is allowed only when predeclared.

- Unresolved members retain independent lifecycle.

**Failure examples:**

- The VAE returns two of three assets and the harness guesses whether they are usable.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-072 — Product diagnostic extensions

**Requirement:** Products may attach detailed diagnostics through stable references while preserving the protocol-level classification and privacy boundary.

**Testable consequences:**

- Deep VLM evidence remains in VAE storage.

- The shared message stays bounded and parseable.

**Failure examples:**

- A product invents a new top-level failure meaning in a diagnostics blob.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

## Feature failure conditions

- Generic failure without recovery semantics.

- Infrastructure retry consumes quality rounds.

- Failure lacks responsible owner.

## Explicitly out of scope

- Internal stack traces

- VAE-specific evaluator taxonomies beyond shared mappings
