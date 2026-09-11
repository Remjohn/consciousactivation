---
title: Epics and Stories Handoff
product: CMF Atomic Harness Builder Next
version: 0.3.0-draft
status: blocked_until_architecture_and_ux
created: '2026-07-13'
updated: '2026-07-13'
---

# Epics and Stories Handoff

Epics and Stories are intentionally downstream of the approved PRD, Architecture, and Control Tower UX contract.

## Step 1 — Extract requirements

Read every PRD shard, Architecture document, ADR, and UX contract. Extract:

- all `FR-*` requirements with full text;
- all `NFR-*` requirements with full text;
- additional Architecture requirements such as storage, eventing, migrations, security, deployment, and starter templates;
- actionable UX requirements for the Pi Control Tower;
- explicit anti-goal and hard-gate implementation obligations.

Do not begin epic design until the inventory is complete and confirmed.

## Step 2 — Design outcome-centered epics

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

Each story must:

- fit within one fresh development-agent context;
- produce an independently testable increment;
- depend only on prior stories;
- state the user or operator value;
- reference FRs, NFRs, contracts, modules, events, and acceptance tests;
- use Given/When/Then criteria including failures, authority, observability, and migration where relevant.

## Step 4 — Validate coverage and readiness

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
