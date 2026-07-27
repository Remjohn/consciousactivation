---
title: F06 — Canonical Harness IR and Artifact Compiler
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F06
governing_decisions:
- D003
- D011
- D014
- D017
- D018
- D025
- D029
- D033
user_journeys:
- UJ-04
- UJ-05
- UJ-07
- UJ-11
- UJ-12
functional_requirement_count: 9
---

# F06 — Canonical Harness IR and Artifact Compiler

**User outcome:** All product truth is maintained once in a typed, versioned representation and compiled into consistent human and machine artifacts.

## Description

This feature is the core anti-drift mechanism. The Harness IR stores evidence, knowledge status, authority, decisions, product constitution, architecture intent, skills, graphs, evaluations, repairs, budgets, and implementation traceability.

## Brownfield baseline

V2.1 already generates structured evidence, decision, OpenSpec, and readiness artifacts, but the documents and schemas are not yet views over one complete canonical IR spanning the new architecture.

## Required product delta

Introduce a versioned IR schema, transactional mutation model, artifact compilers, provenance hashes, compatibility migrations, and cross-artifact consistency validation.

## Traceability

- **Decisions:** D003, D011, D014, D017, D018, D025, D029, D033
- **User journeys:** UJ-04, UJ-05, UJ-07, UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-003, NFR-TRACE-001, NFR-TRACE-003, NFR-MAINT-001

## Functional Requirements

### FR-051 — Maintain one canonical typed Harness IR

**Requirement:** The Builder must store the authorized product definition in one machine-readable Harness IR whose schema covers identity, evidence, syntax, Activative semantics, phases, contexts, contracts, modules, skills, references, evaluators, repairs, budgets, implementation units, and authorization.

**Consequences (testable):**

- Every material product value has one authoritative IR location.
- Generated documents do not create independent authoritative meanings.

**Traceability:** Decisions D011; journeys UJ-04, UJ-11.

### FR-052 — Attach provenance and authority metadata to material values

**Requirement:** Every material IR node must support evidence references, knowledge status, confidence where applicable, authority status, decision source, version, timestamps, and dependency impact.

**Consequences (testable):**

- Observed, measured, derived, hypothesized, human-decided, and generated values remain distinguishable.
- A value without required provenance fails validation.

**Traceability:** Decisions D007, D011; journeys UJ-02, UJ-04.

### FR-053 — Version IR schemas and migrations

**Requirement:** The Builder must version the Harness IR schema and provide explicit compatibility and migration rules for supported prior versions.

**Consequences (testable):**

- A run cannot be loaded under an incompatible schema without a migration or explicit block.
- Migration events preserve the original version and transformation receipt.

**Traceability:** Decisions D011, D028; journeys UJ-12.

### FR-054 — Compile sharded human-readable specifications

**Requirement:** The artifact compiler must generate readable, linkable, sharded specifications from the IR, including product, visual syntax, Activative program, runtime architecture, skill system, evaluation, repair, and handoff views appropriate to the target.

**Consequences (testable):**

- Every generated section identifies its governing IR nodes.
- Recompilation updates affected shards without changing unrelated authoritative content.

**Traceability:** Decisions D011, D029; journeys UJ-11.

### FR-055 — Compile OpenSpec as a governed view

**Requirement:** The Builder must generate OpenSpec changes, schemas, and implementation governance from the Harness IR while keeping the IR authoritative.

**Consequences (testable):**

- An OpenSpec artifact records its source IR hash and compiler version.
- Manual OpenSpec edits require a formal delta back into the IR or remain non-authoritative.

**Traceability:** Decisions D011, D028; journeys UJ-11.

### FR-056 — Compile machine artifacts from the same IR

**Requirement:** The Builder must compile registries, contracts, graphs, skill manifests, evaluation manifests, repair policies, dashboard configuration, fixtures, traceability maps, and implementation tickets from the same IR.

**Consequences (testable):**

- Every artifact has source IR node references and a content hash.
- Conflicting values across generated artifacts fail the consistency gate.

**Traceability:** Decisions D011, D029; journeys UJ-05, UJ-11.

### FR-057 — Protect generated authoritative artifacts from silent manual drift

**Requirement:** The Builder must distinguish generated authoritative views, editable proposals, and operator annotations and must detect manual changes to generated authoritative files.

**Consequences (testable):**

- An unauthorized edit fails integrity validation or is captured as a proposed IR delta.
- Operator notes can coexist without being mistaken for compiled truth.

**Traceability:** Decisions D011, D033; journeys UJ-11.

### FR-058 — Bind artifacts to compiler and source hashes

**Requirement:** Every generated artifact must record the Builder/compiler version, source IR hash, source node set, generation timestamp, and artifact hash in a manifest.

**Consequences (testable):**

- The exact artifact used by implementation or evaluation can be proven.
- Stale artifacts are detectable after IR changes.

**Traceability:** Decisions D011, D021, D029; journeys UJ-08, UJ-11.

### FR-059 — Validate cross-artifact consistency and completeness

**Requirement:** The Builder must validate that all required target-profile artifacts exist, all references resolve, all requirement and decision IDs are covered, and all generated views agree with the Harness IR.

**Consequences (testable):**

- A missing or contradictory compiled view blocks readiness.
- The validation report lists the exact IR nodes and artifacts involved.

**Traceability:** Decisions D003, D011, D027; journeys UJ-11, UJ-12.

## Known failure and edge conditions

- A Markdown file contains a decision absent from the IR.
- Two generated schemas use different field names for one contract.
- An OpenSpec edit silently changes the constitution.
- An evaluated skill package differs from the artifact listed in the IR.

## Explicitly out of scope

- Selecting the implementation language or database technology.
- Treating all operator notes as authoritative product state.
- Guaranteeing backward compatibility beyond versions explicitly supported by migration policy.
