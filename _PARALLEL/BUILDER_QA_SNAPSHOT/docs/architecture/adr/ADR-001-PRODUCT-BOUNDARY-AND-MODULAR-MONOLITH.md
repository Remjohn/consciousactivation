# ADR-001: Product Boundary And Modular Monolith

Status: `ACCEPTED`

Owners: Product authority and architecture. Trace: D001, D004, D015, D033; TS-00, TS-01, TS-07, TS-13.

## Context

Builder owns one highly coupled governance and compilation transaction spanning evidence, IR, decisions, graphs, evaluation, repair, authorization, and handoff. Premature services would split authority and consistency. A single agent or skill would hide deterministic checks and human gates.

## Decision

Implement Release 1 as a modular monolith with strict domain/application/adapter boundaries and isolated worker processes. Builder stops at compiled target packages, Development Capsules, and signed downstream-result ingestion. External target runtimes remain outside the repository.

## Alternatives

- Microservices from day one: rejected because operational and consistency cost is unsupported by measured scale.
- One Pi skill or agent session: rejected by D001, D033, HG-011, and F18.
- Independent scripts sharing files: rejected because it creates duplicate truth and weak transactions.

## Interfaces, Data, And Errors

Modules expose application commands, queries, domain events, and versioned contracts. Direct database access across modules is prohibited. Boundary violations produce `ArchitectureViolation` and block promotion.

## Authority, Security, And Determinism

Domain decisions and compilation remain deterministic. Agents enter only through declared ports. Human gates are application commands with receipts. Worker isolation does not change domain ownership.

## Consequences

Positive: coherent transactions, simpler replay, one canonical model, and easy test seams. Cost: disciplined module rules and potential later extraction. Service extraction requires measured need and a new ADR preserving events and contracts.

## Observability, Performance, Migration

Trace module calls and queue boundaries by correlation ID. Scale vertically and with isolated workers first. No V2.1 modular migration applies.

## Verification

Architecture tests reject adapter imports from domain, direct UI/database writes, external runtime modules, and monolithic skill-owned workflows.

