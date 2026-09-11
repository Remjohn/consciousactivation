# CAE Mandate Bundle — Wave 03

**Bundle ID:** `CAE_MANDATE_BUNDLE_WAVE_03`  
**Scope:** Canonical Questions Q17–Q24  
**Status:** Execution-ready mandate bundle  
**Date:** 2026-09-06  
**Predecessor:** Wave 02 (Q09–Q16) evidence-sovereignty and collision-foundation increment  
**Successor handoff target:** Wave 04 (Authorization, composition, release & distribution)

## Authority chain

1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
2. Master 57-Question Decision & Convergence Canon
3. CAE Product Brief / PRDs / Functional Requirements (`FUNCTIONAL_REQUIREMENTS.md`, modular PRD-003 / PRD-005)
4. `UI.md`
5. `Architecture.md`
6. Individual mandates in this bundle
7. Repository implementation and executable evidence

## Wave strategy

Wave 03 deliberately follows the next eight canonical questions after the Wave 02 evidence-sovereignty foundation:

`Multi-dimensional evidence admission → hierarchical context lineage → Expression Moments → Reaction Receipts → Anchor Hits → adaptive elicitation resilience → deterministic yield gating → configurable authorization policy`

These mandates convert the ratified evidence-admission, composition-bridge, yield, and first authorization decisions into bounded, fail-closed, testable repository behavior. They do not claim that later authorization receipts, composition engines, release manifests, or runtime CAS/Merkle surfaces are implemented merely because interfaces are prepared.

Wave 03 is the natural successor to Wave 02’s defining achievement (“evidence is physically grounded, sovereign, temporally located, continuous, and verbatim”). The defining achievement of Wave 03 is:

> **CAE admits only multi-dimensionally gated evidence, preserves hierarchical context, packages evidence into composition-ready Expression Moments with reaction and anchor coordinates, evaluates interview completion and portfolio yield deterministically, and exposes a configurable (but constitutionally bounded) authorization policy surface.**

## Execution rule

Execute one mandate at a time unless the Operator explicitly authorizes parallelism and the outputs are independently mergeable. Shared state, migrations, registries, evidence graphs, and authority decisions have one integration owner.

Every mandate requires repository inspection, positive and negative executable evidence, exact evidence locators, explicit distinction between documented claims and executable proof, no adjacent-mandate implementation, exact commit SHA, and explicit Operator approval/rejection before proceeding.

Inherited Wave 02 evidence (sovereign media, temporal anchoring, continuity, verbatim integrity, sealed pre-production snapshot, collision foundation) is treated as a hard prerequisite. Mandates must not weaken or re-implement those properties; they may only consume them.

## Files

| File | Canonical question | Invariant / requirement |
|---|---:|---|
| `02_CA_MANDATE_017.md` | Q17 | `FR-EVID-001` |
| `03_CA_MANDATE_018.md` | Q18 | `INV-CTX-001` |
| `04_CA_MANDATE_019.md` | Q19 | `FR-EXPR-001` |
| `05_CA_MANDATE_020.md` | Q20 | `FR-REACT-001` |
| `06_CA_MANDATE_021.md` | Q21 | `FR-ANCH-001` |
| `07_CA_MANDATE_022.md` | Q22 | `FR-ELIC-002` |
| `08_CA_MANDATE_023.md` | Q23 | `INV-YIELD-001` |
| `09_CA_MANDATE_024.md` | Q24 | `FR-AUTH-001` |

## Status discipline

The Master Canon contains ratified decisions and may describe a production-authorized target state. The mandate executor must not convert those statements into false claims about the current repository. Completion of each mandate is determined by executable evidence from the actual codebase.

## Bundle completion

Wave 03 is complete only when all eight mandates independently meet their evidence standards and receive the required Operator decisions. A green result for one mandate does not imply green results for the others. The handoff package into Wave 04 must list residual blockers, shared artifacts, and any integration-owner decisions required for authorization receipts and composition.
