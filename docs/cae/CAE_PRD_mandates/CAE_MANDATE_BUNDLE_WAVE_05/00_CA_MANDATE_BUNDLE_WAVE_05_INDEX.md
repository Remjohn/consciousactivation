# CAE Mandate Bundle — Wave 05

**Bundle ID:** `CAE_MANDATE_BUNDLE_WAVE_05`  
**Scope:** Canonical Questions Q32–Q40 (including Gate Suspension & Resumption)  
**Status:** Execution-ready mandate bundle  
**Date:** 2026-09-06  
**Predecessor:** Wave 04 (Authorization, composition, release & distribution)  
**Successor handoff target:** Wave 06 (CAS, Merkle, replay, reconciliation, preemption, security — Q40–Q47)

## Authority chain

1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
2. Master 57-Question Decision & Convergence Canon
3. CAE Product Brief / PRDs / Functional Requirements (`FUNCTIONAL_REQUIREMENTS.md`, modular PRD-005)
4. `UI.md`
5. `Architecture.md`
6. Individual mandates in this bundle
7. Repository implementation and executable evidence

## Wave strategy

Wave 05 deliberately follows the next eight canonical questions after the authorization/composition/release increment:

`Governed Memory Write-back → FR test-contract lifecycle → Real program execution dispatch → Real workflow dispatch → State-local context projection → Live agent host runner → Resilient multi-provider routing → Deterministic output contract & self-repair`

These mandates convert the ratified memory-promotion and early production-engine spine decisions into bounded, fail-closed, testable repository behavior. They do not claim that later CAS, Merkle chaining, lease reconciliation, tenant fencing, or production seals are implemented merely because interfaces are prepared.

Wave 05 is the natural successor to Wave 04’s authorization and release foundation. The defining achievement of Wave 05 is:

> **CAE promotes memory only under verified attribution, treats FUNCTIONAL_REQUIREMENTS.md as a normative test contract with SPECIFIED→IMPLEMENTED→VERIFIED lifecycle, dispatches real (non-synthetic) programs and workflows, projects strictly pruned lane-masked context, runs live bounded agent hosts, routes across resilient providers, and enforces deterministic output parsing with bounded self-repair.**

## Execution rule

Execute one mandate at a time unless the Operator explicitly authorizes parallelism and the outputs are independently mergeable. Shared state, migrations, registries, agent hosts, and authority decisions have one integration owner.

Every mandate requires repository inspection, positive and negative executable evidence, exact evidence locators, explicit distinction between documented claims and executable proof, no adjacent-mandate implementation, exact commit SHA, and explicit Operator approval/rejection before proceeding.

Inherited Wave 01–04 evidence (causal ordering, sovereign media, multi-dimensional admission, yield gating, authorization policy, release manifests) is treated as a hard prerequisite. Mandates must not weaken those properties; they may only consume them.

## Files

| File | Canonical question | Invariant / requirement |
|---|---:|---|
| `02_CA_MANDATE_032.md` | Q32 | `INV-MEM-001` |
| `03_CA_MANDATE_033.md` | Q33 | `FR-PRD-001` |
| `04_CA_MANDATE_034.md` | Q34 | `INV-DISP-001` |
| `05_CA_MANDATE_035.md` | Q35 | `INV-DISP-002` |
| `06_CA_MANDATE_036.md` | Q36 | `INV-CTX-002` |
| `07_CA_MANDATE_037.md` | Q37 | `INV-RUN-001` |
| `08_CA_MANDATE_038.md` | Q38 | `INV-ROUT-001` |
| `09_CA_MANDATE_039.md` | Q39 | `INV-OUT-001` |
| `10_CA_MANDATE_040.md` | Q40 | `INV-GATE-001` |
| `11_CA_MANDATE_041.md` | Q40 | `INV-GATE-002` / `INV-AUTH-001` |

## Status discipline

The Master Canon contains ratified decisions and may describe a production-authorized target state. The mandate executor must not convert those statements into false claims about the current repository. Completion of each mandate is determined by executable evidence from the actual codebase.

## Bundle completion

Wave 05 is complete only when all eight mandates independently meet their evidence standards and receive the required Operator decisions. A green result for one mandate does not imply green results for the others. The handoff package into Wave 06 must list residual blockers, shared artifacts, and any integration-owner decisions required for human gates, CAS, and Merkle surfaces.
