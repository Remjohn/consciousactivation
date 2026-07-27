---
title: Epics and Stories Handoff
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: story_step_3_complete_pending_human_confirmation
created: '2026-07-13'
updated: '2026-07-14'
---

# Epics and Stories Handoff

Epics and Stories are intentionally downstream of the approved PRD, Architecture, and Control Tower UX contract.

The Builder V1.2 410-row inventory and 12-Epic design were explicitly confirmed by the human on 2026-07-14. Step 3 was authorized and completed as a proposed vertical Story design. This handoff does not authorize automatic continuation into Step 4.

## Step 1 — Extract requirements

Read every PRD shard, Architecture document, ADR, and UX contract. Extract:

- all `FR-*` requirements with full text;
- all `NFR-*` requirements with full text;
- additional Architecture requirements such as storage, eventing, migrations, security, deployment, and starter templates;
- actionable UX requirements for the Pi Control Tower;
- explicit anti-goal and hard-gate implementation obligations.
- `CONST-001` through `CONST-008`, HG-015, and the complete V1.2 contract/lineage obligations.

Do not begin epic design until the inventory is complete and confirmed.

Current gate: `SATISFIED`.

## Step 2 — Design outcome-centered epics

The explicit human response `CONFIRM V1.2 INVENTORY` is recorded in `docs/planning/V1_2_INVENTORY_CONFIRMATION_RECEIPT.yaml`. Step 2 authorization is recorded in `docs/planning/EPIC_STEP_2_AUTHORIZATION_RECEIPT.yaml`.

Current status: `CONFIRMED_STEP_3_AUTHORIZED`.

Outputs:

- `docs/planning/EPIC_INVENTORY.yaml`;
- `docs/planning/EPIC_REQUIREMENT_COVERAGE.csv`;
- `docs/planning/EPIC_DESIGN_PROPOSAL.md`;
- `docs/planning/EPIC_DESIGN_VALIDATION_REPORT.json`.

All 410 confirmed obligations have exactly one confirmed primary Epic. The original confirmed inventory remains unchanged. Epic confirmation and Step 3 authorization are recorded in `docs/planning/EPIC_INVENTORY_CONFIRMATION_RECEIPT.yaml`.

Epics must:

- enable a meaningful Harness Architect, maintainer, reviewer, or implementation outcome;
- deliver independently usable behavior;
- build only on earlier epics, never future epics;
- represent genuine risk or feedback boundaries;
- avoid database/API/UI horizontal layers;
- consider file and component churn before splitting;
- deliver complete workflow outcomes rather than separate router, queue, agent, validator, or sandbox technical layers;
- list every covered FR and relevant NFR/Architecture/UX requirement.

## Step 3 — Create vertical stories

Entry was authorized by the exact human response `CONFIRM BUILDER V1.2 EPIC INVENTORY AND BEGIN STEP 3`.

Current status: `COMPLETE_PENDING_HUMAN_CONFIRMATION`.

Outputs:

- `docs/planning/STORY_INVENTORY.yaml`;
- `docs/planning/STORY_INVENTORY_BY_EPIC.md`;
- `docs/planning/STORY_REQUIREMENT_COVERAGE.csv`;
- `docs/planning/STORY_DEPENDENCY_GRAPH.csv`;
- `docs/planning/STORY_BLOCKED_CONDITIONAL_REGISTER.yaml`;
- `docs/planning/RELEASE_1_STORY_SUBSET.yaml`;
- `docs/planning/STORY_CROSS_REPOSITORY_DEPENDENCIES.yaml`;
- `docs/planning/STORY_DESIGN_PROPOSAL.md`;
- `docs/planning/STORY_DESIGN_VALIDATION_REPORT.json`.

The proposal contains 69 Stories. Every confirmed obligation has one primary Story, every Story remains inside its confirmed primary Epic, and all dependencies point backward. Every Story has one outcome, explicit FR/NFR ownership, prerequisites, contracts/schemas, tests, observability evidence, and an unissued completion receipt. Blocked, conditional, Release 1, and cross-repository registers are complete. Stop before Step 4.

Each story must:

- fit within one fresh development-agent context;
- produce an independently testable increment;
- depend only on prior stories;
- state the user or operator value;
- reference FRs, NFRs, contracts, modules, events, and acceptance tests;
- use Given/When/Then criteria including failures, authority, observability, and migration where relevant.

## Step 4 — Validate coverage and readiness

Entry is not authorized. Human product authority must confirm the proposed Story inventory and explicitly authorize Step 4.

The planning package must include:

- FR/NFR/Architecture/UX requirements inventory;
- FR-to-epic and FR-to-story coverage maps;
- story dependency graph;
- file-churn and risk-boundary review;
- confirmation that no story depends on a future story;
- feature technical-specification assignments;
- implementation-readiness report.

## Required Release 1 epic quality

The first implementation sequence must establish one complete reference vertical path rather than all infrastructure layers up front. Foundation stories create only the state, contracts, and components needed by the next demonstrable behavior.
