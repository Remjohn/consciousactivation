---
title: Document Purpose and Authority
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# 0. Document Purpose and Authority

This sharded Product Requirements Document defines the **CMF Content Harness ↔ Visual Asset Editor Delegation Protocol**. It is intended for CMF product architects, protocol and platform engineers, Content Harness implementers, Visual Asset Editor implementers, security and operations owners, conformance engineers, and downstream composition-runtime maintainers.

The PRD is the product-level authority for the shared boundary only. It does not redesign either independent product. Technical realization belongs in the later Architecture package; implementation stories and feature specifications follow Architecture.

## Source-of-truth hierarchy

1. Locked product decisions in `governance/DECISION_REGISTER.*`
2. Product and protocol requirements in this PRD and `governance/REQUIREMENTS_REGISTRY.*`
3. Frozen upstream architecture in `governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml`
4. Architecture and ADRs, once approved
5. Epics, stories, feature specifications, and code

## Requirement conventions

- Functional Requirements use globally stable IDs `FR-001` through `FR-128`.
- Non-Functional Requirements use grouped IDs such as `NFR-AUTH-001`.
- User journeys use `UJ-01` through `UJ-14`.
- Every feature maps to one of the 16 locked decisions.
- No implementation detail may silently override an authority or lifecycle requirement.
