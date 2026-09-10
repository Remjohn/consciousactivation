# M0092 — Final-Hit Storyboard Validation, Motion Plans and Keyframes

**Status:** EXECUTABLE — OPERATOR REVIEW REQUIRED  
**Execution model:** one bounded mandate; parallel only where the campaign control matrix authorizes it.  
**Model recommendation:** Claude  
**Campaign batch:** A2 VALIDATION

## 1. Identity and status

This mandate is part of the first Visual Production / Evidence-First Storyboard campaign after the repository's M72 frontier. It authorizes one bounded change and does not authorize architectural redesign outside its stated scope. The campaign is intended to make Storyboard, Visual Asset Editing, Transformation, Visual Intelligence and runtime handoff executable as one governed CAE production path.

## 2. Decision / objective being authorized

The authorized decision is: **Implement automatic storyboard validation plus MotionPlan/Keyframe compilation for final-hit planning. Validate semantic purpose, source quality, evidence legibility, Design System, geometry, attention cost, motion intensity and harness constraints.**

The implementation must be narrow enough to test independently and explicit enough that a later integration agent can compose it without reverse-engineering the intent. Where a repository supplies useful behavior, the mandate adopts the behavior—not the repository's authority model. Where CAE already has a canonical object or service, this mandate must extend or adapt it rather than creating a duplicate.

## 3. Governing doctrine and authority sources

CAE semantic meaning remains upstream. Atomic Harnesses define bounded execution grammar and contract compilation. Deterministic code owns schema validation, geometry, state transitions, provenance, receipts and release gates. Operators own approval, rejection, repair and strategic exceptions.

The current M65–M72 campaign is historical brownfield evidence. M72 is the starting frontier for this campaign. Product-update documents are implementation-direction sources, not permission to override existing constitutional precedence. All substantive claims must be classified using `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`.

## 4. Mandatory reading before action

The agent MUST read:

- `docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
- `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`
- `docs/PRD/CURRENT.md`
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/CAE_Operational_Product_Campaign_M0058_M0068_v1/README.md`
- `docs/cae/CAE_Operational_Product_Campaign_M0058_M0068_v1/18_BROWNFIELD_REFERENCE.md`
- `docs/cae/CAE_Production_Convergence_M65_M72_v1/README.md`
- `docs/cae/CAE_Production_Convergence_M65_M72_v1/07_PRODUCTION_OPERATOR_GATES/M72_final_production_gate_current_sync.md`
- `docs/cae/CAE_Product_Brief/10_Media_Intelligence_Asset_Intelligence_Evidence_Retrieval.md`
- `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md`
- `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/01_CAE_Product_Update_Visual_Asset_Editor.md`
- `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/02_CAE_PRD_Update_Visual_Asset_Studio.md`
- `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/03_CONSCIOUS_E_MOTION_EDITING_STANDARDS_v2.md`

For external repository work, inspect the exact current upstream files and symbols used for the adopted behavior. Record the source commit/tag, license, and exact file paths. Do not treat README-level descriptions as implementation evidence.

## 5. Exact scope

Implement storyboard validation plus MotionPlan and Keyframe compilation. Validate semantic purpose, source quality, evidence legibility, Design System, geometry, safe areas, attention cost, motion intensity, continuity, harness constraints and wrong-reading locks. The First Amendment rule is that editing must serve meaning and should not create gratuitous attention.

The agent must begin with a brownfield audit of the current code path, identify reusable objects and tests, then make the smallest compatible implementation. Inputs are the current repository, required authority documents, and exact external source files where named. Outputs are the requested implementation/reference artifact, tests, evidence, and handoff.

## 6. Allowed artifacts and file boundary

**Allowed boundary:** `packages/, services/, docs/cae/specs/, tests`

Changes outside this boundary are prohibited unless the operator explicitly authorizes a boundary change. If a necessary dependency falls outside the boundary, STOP and record an `OPERATOR_DECISION_REQUIRED` blocker. Do not broaden scope silently.

Operator-facing objects must remain linked to canonical CAE state. Any state transition must identify actor, preconditions, validators, postconditions, receipt, error route and recovery path.

## 7. Prohibitions and collision procedure

No unrelated refactors, no competing authority, no bypass of existing contracts, no silent state mutation, and no production claims based solely on mocks or documentation.

Do not create a second retrieval system, storyboard authority, Design System authority, VAE state model, or semantic program model. Do not move meaning into external runtimes. Do not allow Visual Chat or model output to bypass validators. Do not present a generated or mocked artifact as evidence-grounded production output.

If another agent has changed the same shared file or contract, do not overwrite it. Compare the current worktree, record the collision, and stop when authority or merge ownership is ambiguous. Independently mergeable artifacts may continue.

## 8. Required work / implementation behavior

Implement in this order: brownfield inspection; authority mapping; smallest contract/data change; implementation; focused tests; evidence receipt; handoff. For external extraction, create an upstream→CAE mapping table and explicitly state what is excluded. For visual work, maintain the evidence-first priority `RETRIEVE → TRANSFORM → COMPOSE → GENERATE` and preserve source provenance.

Where Transformation or Motion is involved, the preferred path is `Editorial Intent → Narrative Editing Grammar → Editorial Expression Calculus → TransformationIntent → TransformationRecipe → primitives/keyframes`. The model may propose; deterministic code bounds geometry, motion and state.

Where operator feedback is involved, persist revisions and feedback immutably. Where candidate selection is involved, keep rejected candidates and provenance so later evaluation can distinguish automatic acceptance from human promotion.

## 9. Verification and evidence standard

Tests must establish the intended property rather than merely execute code. Include a normal success case and at least one contrastive good-looking-but-wrong case. Add negative authorization, stale, missing, malformed or source-quality cases where applicable. For stateful or compiled behavior, include deterministic replay/idempotence. For external runtimes, state environment-fidelity requirements and do not substitute mocks for native reachability proof.

Every material evidence claim must identify its evidence class, exact source path, exact command and observed result. A green local suite does not establish external runtime availability. A preview does not establish semantic correctness. A certificate cannot manufacture missing reality-contact evidence. Human/operator validation must be explicit wherever perceptual quality or final creative judgment is part of acceptance.

## 10. Completion and stop condition

Complete only when the requested artifact exists, tests pass, evidence is recorded, limitations are explicit, the exact commit SHA is known, and an operator decision is requested. Stop when authority conflicts, required source or runtime evidence is unavailable, scope must widen, or acceptance cannot be established honestly. A blocker is a valid completion state when it is documented and routed for operator decision.

## 11. Rollback / recovery

Rollback only changes introduced by this mandate. Preserve pre-existing work, source evidence, receipts and rejected artifacts. For database/state changes, follow existing CAE migration/recovery conventions. For cloned/extracted upstream content, preserve upstream history and isolate removal or disablement. For UI/runtime changes, disable the capability through its manifest/feature boundary when possible rather than destructively deleting unrelated state.

## 12. Operator decision

At close the operator must explicitly select `APPROVE`, `APPROVE-WITH-LIMITATIONS`, or `REJECT`. For visual output, the operator must inspect the real preview, confirm that the transformation serves meaning and does not create gratuitous attention, and verify source lineage. For external integrations, the operator must confirm that the external runtime remains downstream of CAE authority and is independently replaceable.

## 13. 200–300 word activation prompt

You are an execution agent assigned to execute M0092 for the Conscious Activation Engine at https://github.com/Remjohn/consciousactivation. Read the exact mandate file, the CAE Mandate Authoring Protocol, CAE Constitution, current PRD/CURRENT state, M65–M72 convergence evidence, and every subsystem/upstream file named by the mandate before editing.

Objective: the bounded mandate objective

Authority: CAE owns semantic meaning, Design System authority, contracts, state, provenance and promotion. Existing Programs and Atomic Harnesses define semantic intent and bounded execution. External repositories provide behavior or isolated runtime capabilities only. Models propose; deterministic CAE code validates and executes; Operators approve promotion.

Scope: execute only the exact files, artifacts, tests and behavior named by this mandate. For repository extraction, inspect exact upstream files/symbols and record URL, commit/tag, license, adopted behavior and excluded behavior. For visual work, preserve the evidence-first order RETRIEVE → TRANSFORM → COMPOSE → GENERATE only when justified.

Prohibitions: no unrelated refactor, no competing authority, no wholesale repository merge, no mock-as-production evidence, no placeholder success, no silent state mutation and no bypass of validators or operator gates. Stop on scope collision or ambiguous authority.

Verification must include a happy-path proof, a plausible good-looking-but-wrong counterexample, relevant negative/stale/unauthorized coverage, deterministic replay where applicable, exact commands/results, and explicit limitations. State what the tests do not prove and where operator validation is required.

Completion requires the requested artifact, passing focused tests, evidence/control updates, limitations, exact Git commit SHA and an explicit operator decision request. Return the required mandate bundle only. Operator decision: APPROVE, APPROVE-WITH-LIMITATIONS, or REJECT. Do not self-promote.

## Required delivery artifacts

The agent must return a bundle containing `AGENT_HANDOFF.md`, exact changed/new repository paths, tests, and any evidence/receipt files required by the mandate. The handoff must list files added/modified, rationale, exact commands, test results, external source commit/license information when relevant, evidence classes, limitations, exact commit SHA, and operator decision requested.
