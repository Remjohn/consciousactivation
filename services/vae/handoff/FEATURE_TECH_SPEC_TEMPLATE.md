# FS-XXX — Feature Technical Specification

## 1. Specification identity

- Feature:
- FRs:
- NFRs:
- Decisions:
- User journeys:
- Architecture components:
- Stories:

## 2. Files and evidence read

List complete source paths, schemas, registries, existing code, fixtures, benchmark cases, and upstream constitutions read before writing this specification.

## 3. Problem, solution, and scope

### Problem

### Approved solution behavior

### In scope

### Explicitly out of scope

## 4. Brownfield behavior

- Existing V2.1 mechanism:
- Retained behavior:
- Adapted behavior:
- Deprecated behavior:
- Removed behavior:
- Compatibility risk:

## 5. Architecture traceability

Map every requirement to:

- component/module;
- state machine or workflow node;
- contract/schema;
- storage entity;
- event;
- JIT Skill/model program;
- evaluator;
- repair route;
- Control Tower view;
- test seam.

## 6. User and system flows

Include successful, failure, resume, cancellation, amendment, repair, and rollback flows.

## 7. State machine

Define states, transitions, actors, guards, side effects, events, terminal conditions, invalidation, and idempotency.

## 8. Contracts and public interfaces

For each contract:

- identity/version;
- producer/consumer;
- required/optional fields;
- validation;
- authority;
- compatibility;
- example;
- failure behavior.

## 9. Detailed behavioral rules

Use numbered, testable rules. Distinguish deterministic rules, model judgment, human authority, and external-provider behavior.

## 10. Failure, degradation, and recovery

- failure taxonomy;
- responsible owner;
- infrastructure retry;
- quality repair;
- frozen state;
- invalidated state;
- max attempts;
- escalation;
- receipts.

## 11. Observability

Events, logs, metrics, traces, dashboards, evidence links, operator actions, alerts, and retention.

## 12. Security and authority

Least privilege, untrusted data, secrets, network/storage permissions, model/asset integrity, caller authorization, and prohibited mutations.

## 13. Performance and budgets

Latency, concurrency, GPU/CPU/memory/storage, candidate and evaluator budgets, cost, timeout, cache, early stop and backpressure.

## 14. Compatibility and migration

Version rules, old data/contracts, migrations, rollback, deprecation, and historical reproducibility.

## 15. Implementation plan

Ordered vertical implementation units tied to Stories and test seams. Do not front-load unused infrastructure.

## 16. Acceptance criteria

Use Given/When/Then and include:

- successful paths;
- edge/error cases;
- constitutional hard gates;
- failure examples;
- observability evidence;
- performance/budget conditions;
- backward compatibility;
- rollback.

## 17. Testing strategy

- unit;
- schema/contract;
- workflow integration;
- evaluator/behavioral;
- visual golden;
- adversarial;
- repair;
- recovery/fault injection;
- performance/cost;
- compatibility/migration;
- reference-slice end-to-end.
