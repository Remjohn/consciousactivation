# Technical-Specification Plan

## Objective

Produce an implementation-boundary specification set for the complete Release 1 Builder spine and the Format 02 reference slice before any production code is written.

## Architecture Phase Result

The canonical architecture, ADR register, 18 individual ADRs, and 263-row architecture traceability matrix now exist under `docs/architecture/`. All 18 ADRs are accepted following human ratification on 2026-07-14. Structural architecture validation is `PASS`; the architecture completion gate remains `FAIL` because BD-004, BD-007, BD-008, BD-010, and BD-014 still require external or empirical evidence.

The dedicated Control Tower UX contract remains approved and unchanged. TS-00 through TS-15 now carry the Builder V1.2 constitutional alignment patch. Epic Step 2 is not authorized until the revised planning inventory is confirmed by the human.

## Specification Set

| ID | File | Primary ownership | Initial state |
|---|---|---|---|
| TS-00 | `ARCHITECTURE_PRESERVATION_CONTRACT.md` | Constitution, boundaries, hard gates | Ratified derived contract |
| TS-01 | `specs/TS-01-GOVERNED-LIFECYCLE-AND-TARGET-PROFILES.md` | F01 | Complete conditional draft |
| TS-02 | `specs/TS-02-CONFIGURED-EVIDENCE-WORKSPACE.md` | F02 | Complete conditional draft |
| TS-03 | `specs/TS-03-VISUAL-SYNTAX-FIRST.md` | F03 | Complete empirical draft |
| TS-04 | `specs/TS-04-ATOMICITY-AND-DRAFT-HARNESS-MODEL.md` | F04 | Complete empirical draft |
| TS-05 | `specs/TS-05-DEPENDENCY-DRIVEN-GENESIS.md` | F05 | Complete conditional draft |
| TS-06 | `specs/TS-06-CANONICAL-HARNESS-IR-AND-COMPILATION.md` | F06 | Complete conditional draft |
| TS-07 | `specs/TS-07-OWNERSHIP-PHASE-CONTEXT-CONTRACT-REFERENCE-REPAIR-GRAPHS.md` | F07, F08, graph portion of F13 | Complete conditional draft |
| TS-08 | `specs/TS-08-CANONICAL-SKILL-ECOLOGY.md` | F09 | Complete conditional draft |
| TS-09 | `specs/TS-09-SKILL-RECIPES-AND-JIT-CAPSULES.md` | F10 | Complete conditional draft |
| TS-10 | `specs/TS-10-BEHAVIORAL-EVALUATION-AND-BENCHMARKS.md` | F11 | Complete empirical draft |
| TS-11 | `specs/TS-11-CATEGORY-CONSTITUTIONS-AND-TARGET-COMPILERS.md` | F14, F17 | Complete conditional draft |
| TS-12 | `specs/TS-12-HARNESS-CONTROL-TOWER.md` | F12 | Complete conditional draft |
| TS-13 | `specs/TS-13-IMPLEMENTATION-AUTHORIZATION-AND-DEVELOPMENT-CAPSULE.md` | F13, F15 | Complete conditional draft |
| TS-14 | `specs/TS-14-BUILDER-WORKFLOW-RUNTIME.md` | F18 | Complete conditional draft |
| TS-15 | `specs/TS-15-FORMAT-02-RELEASE-1-VERTICAL-SLICE.md` | FR-167, FR-168, deferred FR-169 and end-to-end proof | Complete empirical draft |

F16 migration behavior is deliberately not assigned an implementation specification. Its locally applicable disposition is documented in `IMPLEMENTATION_BASELINE.md`; migration is reopened only if authoritative V2.1 artifacts enter the repository.

## Authoring Order

1. TS-00, TS-01, TS-06: freeze boundaries, lifecycle, identity, IR, events, artifacts, and transactions.
2. TS-02 through TS-05: define the evidence-to-ratified-Genesis pipeline.
3. TS-07 through TS-09: define harness architecture, context, skills, and capsule compilation.
4. TS-10 and TS-13: define evaluation, repair, readiness, authorization, and handoff.
5. TS-11 and TS-15: bind the Format 02 category/profile and the cross-product target boundaries.
6. TS-14: compile the above product graphs into executable Builder Workflow IR.
7. TS-12: project authoritative events and commands into the Control Tower.
8. Run traceability, hard-gate, security, fault, and vertical-slice readiness reviews.

## Required Content Gate Per Specification

Every TS file must contain owned FRs/NFRs/decisions; authority boundaries; modules; canonical structures; APIs, commands, events, and persistence; actor ownership; dependency/invalidation; idempotency/checkpoints/resume; security/isolation; observability/cost/performance; failures/recovery; acceptance tests; implementation tasks; non-goals; and an explicit migration disposition.

## Completion Checks

- Exactly 210 FRs and 53 NFRs appear once as primary coverage in the matrix, including explicit `NOT_APPLICABLE` and `DEFERRED` dispositions.
- All D001-D033 map to at least one specification or the no-V2.1 disposition.
- All 15 hard gates and 22 anti-goals are operationalized by TS-00 plus subsystem acceptance tests.
- Every V1.2 changed obligation has an implementation owner, component boundary, data/contract definition, failure behavior, test seam, acceptance criteria, and compatibility disposition.
- Activation First runtime ordering and Visual Syntax First harness-development ordering are tested as distinct laws.
- The Visual Asset Editor and Delegation Protocol appear only as target-profile contracts and external ports.
- Format 02 has one traceable shadow workflow, benchmark plan, authorization path, Development Capsule, and downstream evidence interface.
- Implementation readiness remains `FAIL` until all blocking decisions are ratified and empirical prerequisites exist.
- Epic and Story IDs remain empty until the revised V1.2 inventory receives explicit human confirmation.
