---
title: Feature Technical Specification Template
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: template
created: '2026-07-13'
updated: '2026-07-13'
---

# FS-XXX — Feature Technical Specification

## 1. Identity and traceability

- Feature:
- FRs:
- NFRs:
- Decisions:
- Epics and Stories:
- Category / format / target profile:
- Constitutional authority and precedence refs:
- Runtime law and harness-development evidence order:
- Source evidence:

## 2. Files and systems read

List current implementation files, schemas, registries, tests, prior artifacts, and authoritative references inspected before design.

## 3. Problem, solution, and scope

- Current failure or missing capability
- Required behavior
- In scope
- Explicitly out of scope
- Brownfield behavior retained, adapted, deprecated, or removed

## 4. Architecture traceability

Map every mechanism to FR/NFR IDs and Architecture components. Identify public interfaces, ownership, and forbidden authority.

## 5. States, flows, and graphs

Define lifecycle, phase, context, contract, dependency, event, repair, UI, and Builder Workflow IR state relevant to this feature. For workflow features include an Actor Assignment Matrix, node graph, conditions, feedback edges, retries, sandboxes, human gates, and terminal states.

## 6. Contracts and data

Provide exact schemas, versions, producer/consumer roles, implementation owner, component boundary, examples, compatibility, authority, provenance, invalidation, failure behavior, test seam, and acceptance criteria. For sparse semantic tokens, pin all rich source-object references and frozen versions.

## 7. Detailed behavior

Specify positive path, branches, conditions, completion criteria, failure behavior, degradation, retry, and escalation.

## 8. Observability and receipts

Define events, metrics, cost and latency data, operator views, commands, and receipt identity.

## 9. Security and authority

Define access, secrets, source safety, human gates, policy restrictions, and audit requirements.

## 10. Performance and context budgets

Define expected scale, hard and soft budgets, concurrency, caching, retrieval, and overflow behavior.

## 11. Compatibility and migration

Define V2.1 behavior, aliases, schema migration, deprecation, dual-run, rollback, and required regression.

## 12. Implementation tasks

Map tasks to approved stories. Each task identifies files, interfaces, tests, dependencies, and completion evidence.

## 13. Acceptance criteria

Use Given/When/Then. Include positive, negative, edge, missing-evidence, authority, compatibility, and repair cases. Every criterion references FR/NFR IDs.

## 14. Testing strategy

- unit and deterministic validation;
- contract and schema;
- integration and event flow;
- behavioral skill or model-program evaluation;
- visual, temporal, conversational, expression, golden, adversarial, and protected benchmarks;
- constitutional precedence, Activation First, semantic non-mutation, and external-runtime boundary tests;
- migration and backward compatibility;
- performance, context, cost, and observability.
