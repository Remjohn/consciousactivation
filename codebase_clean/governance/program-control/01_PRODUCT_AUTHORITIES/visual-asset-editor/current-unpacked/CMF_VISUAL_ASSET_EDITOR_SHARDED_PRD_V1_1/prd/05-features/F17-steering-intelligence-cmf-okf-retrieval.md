---
title: F17 — Visual Steering Intelligence, CMF-OKF Knowledge, and Smart Retrieval
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F17
governing_decisions:
- D014
- D019
- D020
- D021
- D027
user_journeys:
- UJ-09
- UJ-10
- UJ-15
functional_requirement_count: 8
---


# F17 — Visual Steering Intelligence, CMF-OKF Knowledge, and Smart Retrieval

**User outcome:** A production or repair node receives the smallest authoritative memory that matches its demand, Visual Syntax context, capability, and failure rather than scanning a generic archive.

## Description

The product converts validated production evidence into governed Steering Recipes and publishes durable knowledge through a stricter CMF-OKF profile while canonical state remains typed and transactional.

## Brownfield baseline

OKF offers portable Markdown/frontmatter, progressive disclosure, and graph links, but it is intentionally minimally opinionated. CMF requires typed authority, lifecycle, compatibility, retrieval facets, evidence, and operational references layered above it.

## Required product delta

Define Steering Recipe lifecycle, CMF-OKF profile, concept projection, indexes, authority filters, typed edges, hybrid multimodal retrieval, VLM reranking, contradiction coverage, Minimum Complete Context, and no silent self-modification.

## Traceability

- **Decisions:** D014, D019, D020, D021, D027
- **User journeys:** UJ-09, UJ-10, UJ-15
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-MEM-001, NFR-MEM-002, NFR-MEM-003, NFR-MEM-004, NFR-MEM-005

## Functional Requirements

### FR-129 — Capture steering evidence from production

**Requirement:** Candidate portfolios, evaluations, repairs, syntax contexts, bindings, costs, and final outcomes must produce structured evidence suitable for recurring pattern analysis.

**Consequences (testable):

- Evidence distinguishes correlation, controlled comparison, and validated intervention.

- Raw winning prompts cannot be promoted directly as production knowledge.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-130 — Compile versioned Visual Steering Recipes

**Requirement:** A Steering Recipe must define applicability, failure/success pattern, compatible workflows and assets, intervention, preserved properties, evidence, observed runs, control comparison, regression cases, cost effect, lifecycle, and authority.

**Consequences (testable):

- Recipes are independently inspectable and benchmarkable.

- A recipe without applicability boundaries cannot enter shadow routing.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-131 — Promote recipes through governed learning states

**Requirement:** Recipes must move through proposed, experimental, validated, shadow, limited-production, production, deprecated, and retired states with minimum evidence and rollback.

**Consequences (testable):

- Production routing uses only policy-eligible recipe states.

- A single successful run cannot alter defaults.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-132 — Publish durable knowledge through CMF-OKF

**Requirement:** The product must project selected workflows, models, LoRAs, failure patterns, repair patterns, Steering Recipes, syntax usage contexts, benchmarks, and operator knowledge into OKF-compatible Markdown with CMF frontmatter extensions.

**Consequences (testable):

- Concepts remain readable, version-controllable, portable, and linked to canonical records.

- OKF documents cannot become the authoritative lifecycle or execution store.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-133 — Define typed CMF knowledge relationships

**Requirement:** CMF-OKF concepts and the retrieval graph must support explicit edges such as derived-from, validated-by, compatible-with, contradicts, supersedes, repairs, failed-under, applies-to, observed-in, consumed-by, and shares-syntax-with.

**Consequences (testable):

- Graph traversal can distinguish evidence, compatibility, contradiction, and succession.

- Untyped prose links alone cannot govern production retrieval.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-134 — Apply authority and compatibility filters before similarity search

**Requirement:** Retrieval must first filter by lifecycle, authority, category, format, asset family, syntax role, Activative function, failure code, workflow/model compatibility, validity, and current demand constraints.

**Consequences (testable):

- Incompatible or superseded concepts are excluded or marked explicitly.

- Semantic similarity cannot override hard eligibility.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-135 — Use hybrid multimodal retrieval and VLM reranking

**Requirement:** Eligible memory must be ranked using lexical search, text embeddings, image embeddings, composition embeddings, syntax fingerprints, graph proximity, evidence quality, and VLM comparison with current demand, composition, failure, and preservation constraints.

**Consequences (testable):

- Results include scores, reasons, conflicts, and exclusions.

- The system cannot rely solely on one vector index.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

### FR-136 — Compile Minimum Complete Context with contradiction coverage

**Requirement:** The JIT retrieval compiler must select only relevant frontmatter, body sections, typed contract references, exceptions, superseding knowledge, failure cases, and material conflicting evidence needed by the current node.

**Consequences (testable):

- The compilation receipt records included, excluded, compressed, and unavailable resources.

- The model may not receive the entire memory corpus by default.

**Traceability:** Decisions D014, D019, D020, D021, D027; journeys UJ-09, UJ-10, UJ-15.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
