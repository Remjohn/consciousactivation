---
title: Epics and Stories Handoff
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: blocked_until_architecture_validated
created: '2026-07-13'
updated: '2026-07-13'
---

# Epics and Stories Handoff

Epics and stories must be generated **after** the Delegation Architecture and ADRs are validated.

## Inputs

- Complete sharded PRD and 128 FRs
- 60 cross-cutting NFRs
- Architecture and ADRs
- Authority Matrix
- Lifecycle Machine
- Failure Taxonomy
- Compatibility Policy
- Contract schemas and Format 02 fixtures
- Conformance and deployment architecture

## Epic design principles

- Organize around operator/product outcomes rather than technical layers.
- Every epic must deliver a complete independently valuable protocol capability.
- Every FR must map to at least one story and acceptance criterion.
- Stories must fit one development-agent context and depend only on earlier stories.
- Infrastructure is introduced only when required by the first vertical story that uses it.
- Each story must include Given/When/Then acceptance, failure cases, events and receipts.
- Stories changing authority, lifecycle or shared contracts require explicit architecture traceability.

## Recommended outcome themes for later epic design

1. Submit and accept a trusted authoritative demand
2. Project a valid idempotent cross-product lifecycle
3. Safely supersede, amend, budget and cancel delegated work
4. Acknowledge current results and govern post-completion change
5. Negotiate compatible product and contract versions
6. Observe, audit and recover the delegation boundary
7. Certify the Format 02 end-to-end reference path

These are planning themes, not approved epics. The BMAD epic workflow must extract and map all requirements after Architecture.
