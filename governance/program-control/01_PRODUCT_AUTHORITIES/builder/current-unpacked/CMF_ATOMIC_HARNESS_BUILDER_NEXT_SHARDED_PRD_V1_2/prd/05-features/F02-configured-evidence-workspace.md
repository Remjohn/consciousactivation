---
title: F02 — Configured Evidence Workspace, Source Lock, and Saturation
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F02
governing_decisions:
- D003
- D005
- D006
- D007
- D022
- D023
- D028
user_journeys:
- UJ-01
- UJ-02
- UJ-03
- UJ-12
functional_requirement_count: 10
---

# F02 — Configured Evidence Workspace, Source Lock, and Saturation

**User outcome:** A Harness Architect can prove exactly which sources and specimens were available, inspected, missing, contradictory, and sufficient before synthesis begins.

## Description

This feature operationalizes Saturation Before Compression. Source presence alone is insufficient: the Builder must establish coverage, provenance, gaps, and authority before it may classify or design.

## Brownfield baseline

V2.1 already reads directories and ZIP archives, validates required sources, creates SOURCE_INSPECTION, SOURCE_LOCK, EVIDENCE_INDEX, SPECIMEN_INDEX, and a saturation report. Its source configuration is generic and some embedded references are not automatically registered.

## Required product delta

Introduce target-specific source profiles, richer coverage contracts, contradiction authority, gap classes, source readiness diagnostics, and explicit waiver effects while retaining read-only archive support.

## Traceability

- **Decisions:** D003, D005, D006, D007, D022, D023, D028
- **User journeys:** UJ-01, UJ-02, UJ-03, UJ-12
- **Cross-cutting NFRs:** NFR-REL-004, NFR-TRACE-001, NFR-TRACE-004, NFR-SEC-003, NFR-SCALE-001

## Functional Requirements

### FR-009 — Define target-specific source profiles

**Requirement:** The Builder must define required, recommended, optional, and prohibited source roles independently for each compilation target and category profile.

**Consequences (testable):**

- A Content Harness, Visual Asset Editor, and Delegation run may require different source sets.
- The resolved profile is stored and versioned with the run.

**Traceability:** Decisions D005, D006; journeys UJ-01.

### FR-010 — Run source-readiness diagnostics before initialization

**Requirement:** The Builder must inspect configured paths, archive readability, source type, expected role, and version hints before committing the run to analysis.

**Consequences (testable):**

- Missing required sources block with actionable diagnostics.
- Recommended or optional omissions are recorded without pretending they were inspected.

**Traceability:** Decisions D005; journeys UJ-01.

### FR-011 — Read directories and archives without mutating sources

**Requirement:** The Builder must index approved directory and ZIP sources in place while preserving source immutability and recorded hashes.

**Consequences (testable):**

- No source file is modified, renamed, or unpacked into its origin by the Builder.
- Derived artifacts are written only to approved run or workspace output locations.

**Traceability:** Decisions D005, D028; journeys UJ-01.

### FR-012 — Require a real target candidate boundary

**Requirement:** The exact target candidate must resolve to a real accessible directory or another target type explicitly supported by its profile; internal archive paths may not be treated as traversable directories without deterministic extraction.

**Consequences (testable):**

- Invalid target boundaries block before specimen indexing.
- The resolved target replaces any placeholder target binding in the run configuration.

**Traceability:** Decisions D005; journeys UJ-01.

### FR-013 — Create an immutable source lock

**Requirement:** The Builder must record source identifiers, canonical paths, cryptographic hashes, sizes, timestamps where available, roles, precedence, and authority status in a Source Lock.

**Consequences (testable):**

- Every evidence reference resolves to one locked source version.
- Changing a locked source creates a new source version and invalidates affected evidence rather than mutating history.

**Traceability:** Decisions D005, D025; journeys UJ-01.

### FR-014 — Build a queryable evidence index

**Requirement:** The Builder must index relevant files, archive entries, documents, schemas, registries, code, media, and prior implementations with provenance and semantic role metadata.

**Consequences (testable):**

- Material Builder recommendations can cite stable evidence references.
- The index distinguishes found content from merely configured sources.

**Traceability:** Decisions D003, D005; journeys UJ-01, UJ-03.

### FR-015 — Inventory every target specimen

**Requirement:** The Builder must assign stable IDs, hashes, media types, dimensions or duration, source paths, duplicate relationships, and analysis status to every target specimen.

**Consequences (testable):**

- All target media is accounted for or explicitly unreadable.
- Duplicates remain traceable but are not silently treated as independent evidence.

**Traceability:** Decisions D007, D023; journeys UJ-02.

### FR-016 — Evaluate a measurable saturation contract

**Requirement:** Each target profile must define the required source coverage, specimen coverage, evidence categories, prior-art inspection, contradiction detection, and traceability conditions needed for saturation.

**Consequences (testable):**

- Saturation cannot pass solely because files exist.
- The saturation matrix shows each required obligation and its evidence.

**Traceability:** Decisions D003, D007; journeys UJ-01, UJ-02.

### FR-017 — Classify evidence gaps and authority conflicts

**Requirement:** The Builder must distinguish missing evidence, unreadable evidence, sparse target evidence, contradictory sources, contradictory authority, and unresolved provenance.

**Consequences (testable):**

- Each gap class has a defined blocker or waiver policy.
- Higher-precedence canonical sources are not silently overridden by lower-precedence references.

**Traceability:** Decisions D005, D007; journeys UJ-01, UJ-09.

### FR-018 — Issue typed saturation outcomes

**Requirement:** The Builder must issue PASS, PASS_WITH_LIMITATIONS, BLOCKED_MISSING_EVIDENCE, BLOCKED_CONTRADICTORY_AUTHORITY, or INSUFFICIENT_TARGET_EVIDENCE with evidence and downstream consequences.

**Consequences (testable):**

- PASS_WITH_LIMITATIONS requires a human waiver and marks affected decisions provisional.
- A blocked saturation outcome prevents atomicity and Genesis.

**Traceability:** Decisions D007, D027; journeys UJ-01, UJ-09.

## Known failure and edge conditions

- A configured source is counted as inspected even though no relevant content was indexed.
- A duplicate specimen inflates evidence strength.
- A missing canonical registry is replaced by an invented local concept.
- Genesis starts despite a blocking saturation status.

## Explicitly out of scope

- General enterprise knowledge management.
- Editing or repairing upstream repositories.
- Automatically resolving substantive contradictions without the declared authority model.
