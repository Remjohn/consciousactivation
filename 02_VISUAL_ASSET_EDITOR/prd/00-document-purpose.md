---
title: Document Purpose and Authority
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# Document Purpose and Authority

This PRD defines the product requirements for an independently versioned **CMF Visual Asset Editor**. The intended readers are CMF product owners, Harness Architects, Visual Runtime specialists, evaluators, infrastructure engineers, implementation agents, and release reviewers.

The PRD is governed by:

- the 28 locked decisions in [`../governance/DECISION_REGISTER.md`](../governance/DECISION_REGISTER.md);
- the frozen upstream architecture in [`../governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml`](../governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml);
- globally stable Functional Requirement and Non-Functional Requirement IDs;
- the source and evidence register;
- the Release 1 Format 02 reference slice.

## Authority order

```text
Validated Atomic Harness Builder architecture
→ approved Visual Asset Editor product constitution
→ this PRD and Requirements Registry
→ future Visual Asset Editor Architecture
→ future Epics, Stories and feature specifications
→ implementation
```

A lower layer may implement or clarify an approved requirement. It may not silently redefine an upstream authority.

## Product separation

The Visual Asset Editor is one of three explicit compilation targets already recognized by the Atomic Harness Builder:

1. Atomic Content Harness;
2. Visual Asset Editor;
3. Content ↔ Visual Asset Delegation Contract.

This PRD governs only the second product. Shared request/response schemas and compatibility policy will be finalized by the separate Delegation PRD.

## Stable identifiers

- Decisions: `D001`–`D028`
- User journeys: `UJ-01`–`UJ-16`
- Features: `F01`–`F22`
- Functional Requirements: `FR-001`–`FR-176`
- Non-Functional Requirements: category-specific `NFR-<GROUP>-NNN`

## Status meaning

`draft_for_review` means the planning decisions have been compiled and mechanically validated, but Architecture has not yet been approved and implementation is not authorized.
