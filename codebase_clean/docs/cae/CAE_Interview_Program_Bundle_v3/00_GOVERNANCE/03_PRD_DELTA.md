# Proposed PRD Delta — Interview Program Integration

**Status:** PROPOSED / NOT YET RATIFIED
**Build authority:** false
**Purpose:** translate the Interview Program decisions from the supplied design conversation into a repository-native product requirements delta without inventing current PRD story text.

## 1. Existing product requirements this delta extends

The current Composer tech spec explicitly controls FR-APP-010, FR-APP-011, and FR-APP-012, including Guest Research Package, Activative Interview Brief, and session scheduling/hand-off. The Interview Program increment extends the intelligence that feeds the existing Brief and the operator workflow around it; it does not replace those FRs.

## 2. Proposed capability requirements

### FR-IP-001 — Hypothesis-driven interview acquisition
The system shall support an Operator-facing workflow in which upstream CAE/AIR intelligence is represented as a bounded candidate hypothesis portfolio, without duplicating canonical AIR hypothesis ownership.

### FR-IP-002 — Diversified hypothesis selection
The system shall permit selection of a diversified working portfolio from a larger candidate set, preserving candidate lineage and avoiding selection based on rank score alone.

### FR-IP-003 — Question-to-evidence planning
Each selected hypothesis line shall resolve to an explicit question objective and required evidence/response shape before it becomes part of the executable interview plan.

### FR-IP-004 — Question-to-composition compatibility
Question planning shall preserve compatibility with intended archetype, format, narrative role, and other downstream syntax requirements when such intent exists.

### FR-IP-005 — Bounded adaptive interview
The live interview shall preserve a coverage spine while selecting the next move from a bounded set of candidate question operations using observed answer state.

### FR-IP-006 — Semantic acquisition observation
The runtime shall record enough information to distinguish evidence resolution, completeness, discrepancy, branch discovery, and other answer-state changes relevant to routing and downstream interpretation.

### FR-IP-007 — Evidence/inference lineage
Guest-stated evidence, system inference, and Guest-validated interpretation shall remain distinguishable in stored lineage.

### FR-IP-008 — Operator-controlled regeneration
The Operator shall be able to give structured feedback and request constrained regeneration while preserving locked semantic dimensions and original provenance.

### FR-IP-009 — Brief compilation and launch authorization
Selected material shall compile into the existing Activative Interview Brief and shall not launch without explicit Operator authorization through the authoritative path.

### FR-IP-010 — Production candidate readiness
Interview evidence shall be traceable to downstream content candidates and their compatible format/archetype/narrative roles without asserting that every hypothesis must produce a fixed number of pieces.

## 3. Proposed acceptance themes

- existing Composer ownership remains intact;
- no unauthorized canonical object family is introduced;
- 96→16–24 is implemented as candidate search + diversified selection, not a fixed quota;
- question decisions are attributable to hypothesis/objective/evidence requirements;
- bounded adaptive routing changes with observed answers;
- evidence cannot be fabricated by receipts or UI state;
- Operator approval is authoritative;
- downstream compatibility is explicit;
- PRD and tech-spec state are updated in-session when implementation changes durable product truth.

## 4. Story handling

The current Composer tech spec notes a discrepancy in the repository's existing story-range documentation and explicitly resolves acceptance against the controlling FRs rather than inventing missing story text. This bundle follows that precedent. Do not create new story IDs in this bundle merely to make the delta look complete. A PRD-authoring pass must map the proposed requirements into the repository's actual current story structure before ratification.

## 5. Ratification gate

This delta becomes build-authoritative only after:

1. the current PRD owner accepts or revises the proposed requirements;
2. relevant PRD sections and change log are updated in the same authoring session;
3. a technical spec is accepted against the ratified requirements;
4. the execution plan is frozen against that spec.
