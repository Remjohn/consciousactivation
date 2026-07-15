---
title: F17 — Three Explicit Compilation Target Profiles
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F17
governing_decisions:
- D001
- D004
- D005
- D006
- D011
- D013
- D027
- D029
- D032
- D033
user_journeys:
- UJ-01
- UJ-05
- UJ-06
- UJ-11
- UJ-12
functional_requirement_count: 11
---

# F17 — Three Explicit Compilation Target Profiles

**User outcome:** The Builder can compile Atomic Content Harnesses, Visual Asset Editors, and Delegation Contracts through shared governance while preserving the distinct evidence, decisions, IR, artifacts, benchmarks, and authorization each product requires.

## Description

This feature keeps the Builder product-specific rather than universal. It uses one control plane and one IR framework with explicit target-profile extensions, preventing a Content Harness model from being incorrectly reused for asset authority or ABI design.

## Brownfield baseline

V2.1 already exposes three modules with separate prompt paths and approximate artifact sets. The next architecture must make those differences first-class in source profiles, Genesis, capability ownership, evaluation, repair, Development Capsules, and certification.

## Required product delta

Create three versioned target profiles, shared and target-local IR schemas, lifecycle and decision extensions, output packages, cross-target compatibility checks, and certification boundaries.

## Traceability

- **Decisions:** D001, D004, D005, D006, D011, D013, D027, D029, D032, D033
- **User journeys:** UJ-01, UJ-05, UJ-06, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-ARCH-001, NFR-CAT-001, NFR-COMPAT-001, NFR-SEC-003, NFR-PORT-002

## Functional Requirements

### FR-170 — Maintain three versioned target profiles

**Requirement:** The Builder must register Atomic Content Harness, Visual Asset Editor, and Content↔Asset Delegation Contract as explicit versioned compilation targets sharing only proven control-plane and IR abstractions.

**Consequences (testable):**

- Each run selects one profile with a stable version.
- A profile declares its required extensions and forbidden cross-target assumptions.

**Traceability:** Decisions D004, D006; journeys UJ-01.

### FR-171 — Compile the Atomic Content Harness profile

**Requirement:** The content profile must cover evidence and specimens, Visual Syntax First, atomicity, Activative semantics, category and format profiles, sequencing, assets, runtime, JIT skills, evaluation, repair, and content-harness authorization.

**Consequences (testable):**

- Category constitution and atomic production promise are mandatory.
- The profile does not grant asset-editing authority beyond its demand contract.

**Traceability:** Decisions D004, D030, D031; journeys UJ-02, UJ-06.

### FR-172 — Compile the Visual Asset Editor profile

**Requirement:** The asset-editor profile must cover asset taxonomy, demand-contract intake, semantic non-mutation, source and rights provenance, research and provider routing, transformation authority, quality, versions, receipts, repair, and editor authorization.

**Consequences (testable):**

- The editor cannot change content meaning, sequence role, or composition purpose without a new request.
- Representative real demand contracts are required evidence for production certification.

**Traceability:** Decisions D004; journeys UJ-11, UJ-12.

### FR-173 — Compile the Delegation Contract profile

**Requirement:** The delegation profile must cover request and response ABI, ownership boundaries, compatibility, idempotency, timeouts, retries, partial results, errors, provenance, reconciliation, version negotiation, and certification between one content harness and one asset editor.

**Consequences (testable):**

- The ABI cannot redefine either product's constitution.
- Representative request, response, and failure examples are required.

**Traceability:** Decisions D004; journeys UJ-11, UJ-12.

### FR-174 — Use target-specific source profiles

**Requirement:** Each compilation target must declare its own required repositories, contracts, examples, prior implementations, doctrine, and target folder expectations.

**Consequences (testable):**

- The Visual Asset Editor can require visual research and asset-intelligence sources not mandatory for every content harness.
- Delegation compilation may use compiled product changes and representative ABI fixtures instead of the full specimen corpus.

**Traceability:** Decisions D005; journeys UJ-01.

### FR-175 — Use target-specific Harness IR profiles

**Requirement:** The canonical Harness IR must provide a shared governance spine plus typed target-local sections and validation rules for content, editor, and delegation products.

**Consequences (testable):**

- Target-local fields are not represented as an uncontrolled sea of optional properties.
- Cross-target shared nodes have identical semantics and version policy.

**Traceability:** Decisions D011; journeys UJ-05.

### FR-176 — Use target-specific Genesis decision graphs

**Requirement:** Each target must define the constitutional decisions, dependencies, evidence, ratification owners, and cascade-lock conditions appropriate to its authority and product promise.

**Consequences (testable):**

- Content format decisions are not asked during a pure delegation run unless they affect the ABI.
- Asset semantic-authority decisions are mandatory for the editor profile.

**Traceability:** Decisions D006, D010; journeys UJ-04.

### FR-177 — Compile target-specific artifact sets

**Requirement:** Each target profile must declare its required specifications, contracts, skills, graphs, tests, benchmarks, observability views, Development Capsule contents, and readiness receipts.

**Consequences (testable):**

- Missing target-required artifacts block readiness.
- Artifact counts are not forced to be equal across profiles.

**Traceability:** Decisions D029; journeys UJ-11.

### FR-178 — Apply target-specific evaluation and authorization gates

**Requirement:** The score dimensions, hard blockers, skill maturity, benchmark corpus, repair routes, and implementation authorization criteria must be profile-specific while preserving shared evidence and integrity gates.

**Consequences (testable):**

- A content visual-syntax benchmark cannot substitute for editor provenance testing.
- The Delegation Contract cannot be production-authorized before both endpoint specifications are compatible and sufficiently mature.

**Traceability:** Decisions D021, D024, D027; journeys UJ-12.

### FR-179 — Prevent universal-profile flattening

**Requirement:** The Builder must reject attempts to model all three targets as one generic agent schema whose meaning depends on optional fields and prose conventions.

**Consequences (testable):**

- Shared abstractions require demonstrated semantic equivalence.
- Target-specific responsibilities remain explicit in IR and documentation.

**Traceability:** Decisions D004, D033; journeys UJ-05.

### FR-180 — Validate cross-target compatibility

**Requirement:** Where products interact, the Builder must validate content demand contracts, editor response contracts, delegation versions, ownership, provenance, error semantics, and authorization compatibility.

**Consequences (testable):**

- A mismatch generates a typed compatibility blocker and repair route.
- Compatibility results identify which target owns each correction.

**Traceability:** Decisions D004, D014, D026; journeys UJ-10, UJ-11.

## Known failure and edge conditions

- One generic profile uses dozens of optional fields to represent all targets.
- The Content Harness directly owns asset transformation policy.
- A Delegation Contract is compiled before its endpoint contracts exist.
- Structural support is presented as production certification.

## Explicitly out of scope

- Arbitrary agent or workflow types beyond the three named targets.
- Implementing the Visual Asset Editor or Delegation runtime in Release 1 unless selected by the reference-slice scope.
- Guaranteeing compatibility with unspecified third-party editors.
