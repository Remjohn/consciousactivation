# Builder V1.2 Vertical Story Design Proposal

Status: `PROPOSED_AWAITING_HUMAN_CONFIRMATION`

Step: `3 — Vertical Story authoring`

Authority: confirmed 12-Epic Builder V1.2 design under Activative Intelligence Constitution V1.1.

- Stories: 69
- Confirmed obligations assigned to a primary Story: 410
- Story dependencies: backward-only by construction
- Step 4 coverage/readiness validation: not authorized
- Production implementation: prohibited while readiness is `FAIL`

Every Story is a complete, independently testable vertical increment sized for one fresh development-agent context. Stories preserve confirmed Epic ownership, use only earlier dependencies, carry unresolved human decisions and blockers, and do not implement Visual Asset Editor, Delegation Protocol, Interview Expression, or ReelCast product runtimes.

## EP-01 — Governed Run Intake and Evidence Readiness

**Epic outcome:** A Harness Architect can select exactly one compilation target, start or resume a constitutionally bounded run, lock target-specific evidence without source mutation, and receive an explicit readiness or saturation outcome before design decisions begin.

**Story count:** 4

### ST-01.01 — Start and Resume One Target-Profiled Builder Run

As a **Harness Architect**, I want to **select exactly one compilation target and starts or resumes its governed lifecycle**, so that **the run has stable identity, explicit authority, replay-safe state, and target-specific required work**

- Global order: `1`
- Dependencies: None
- Primary outcome: the run has stable identity, explicit authority, replay-safe state, and target-specific required work
- Primary obligations (15): `ADR-001`, `AG-001`, `AG-002`, `D001`, `D006`, `FR-001`, `FR-002`, `FR-003`, `FR-004`, `FR-005`, `FR-006`, `FR-007`, `FR-008`, `NFR-REL-002`, `NFR-SEC-003`
- Relevant FRs: `FR-001`, `FR-002`, `FR-003`, `FR-004`, `FR-005`, `FR-006`, `FR-007`, `FR-008`
- Relevant NFRs: `NFR-REL-002`, `NFR-SEC-003`
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `Product authority and architecture`, `TS-01`, `product_constitution`
- Component boundary: Run governance and configured evidence workspace; downstream design and execution remain outside this increment.
- Affected contracts: `RunLifecycle`, `EvidenceWorkspace`, `ConstitutionalReadinessReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ConstitutionalReadinessReceipt`
- Primary specifications: `TS-00`, `TS-01`, `TS-02`, `TS-07`, `TS-11`, `TS-13`, `TS-14`, `TS-15`
- Test seam: Target-profile lifecycle and evidence public-seam scenarios with fail-closed fixtures.
- Gate references: `HD-006`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject missing or multiple targets, invalid transitions, unauthorized waivers, and any resume that replays a human decision.
- Observability evidence: `ST-01.01:OutcomeVerified`, `ST-01.01:OutcomeRejected`
- Required tests: `ST-01.01-acceptance`, `ST-01.01-failure`, `ST-01.01-authority`, `ST-01.01-receipt`
- Completion receipt: `ST-01.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve shared lifecycle semantics while versioning target-specific source and state contracts.
- Fresh-context scope: One independently testable Start and Resume One Target-Profiled Builder Run increment covering 15 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-01.01 are accepted and the covered authority is available,
- When the Harness Architect selects exactly one compilation target and starts or resumes its governed lifecycle,
- Then the run has stable identity, explicit authority, replay-safe state, and target-specific required work
- And failure behavior is explicit: Reject missing or multiple targets, invalid transitions, unauthorized waivers, and any resume that replays a human decision.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve shared lifecycle semantics while versioning target-specific source and state contracts.

### ST-01.02 — Lock a Safe Target-Specific Evidence Workspace

As a **Harness Architect**, I want to **validate a real target boundary and creates an immutable target-specific source lock**, so that **source material is portable, safe to inspect, and protected from mutation**

- Global order: `2`
- Dependencies: `ST-01.01`
- Primary outcome: source material is portable, safe to inspect, and protected from mutation
- Primary obligations (10): `ADR-007`, `D005`, `FR-009`, `FR-010`, `FR-011`, `FR-012`, `FR-013`, `NFR-PORT-001`, `NFR-SEC-001`, `NFR-SEC-002`
- Relevant FRs: `FR-009`, `FR-010`, `FR-011`, `FR-012`, `FR-013`
- Relevant NFRs: `NFR-PORT-001`, `NFR-SEC-001`, `NFR-SEC-002`
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `Evidence architecture and source authority`, `TS-02`, `product_constitution`
- Component boundary: Run governance and configured evidence workspace; downstream design and execution remain outside this increment.
- Affected contracts: `RunLifecycle`, `EvidenceWorkspace`, `ConstitutionalReadinessReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ConstitutionalReadinessReceipt`
- Primary specifications: `TS-01`, `TS-02`, `TS-11`
- Test seam: Target-profile lifecycle and evidence public-seam scenarios with fail-closed fixtures.
- Gate references: `BD-004`, `BD-014`, `HD-006`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block invalid paths, unsafe archives, missing consent policy, unreadable authority, and any attempted source mutation.
- Observability evidence: `ST-01.02:OutcomeVerified`, `ST-01.02:OutcomeRejected`
- Required tests: `ST-01.02-acceptance`, `ST-01.02-failure`, `ST-01.02-authority`, `ST-01.02-receipt`
- Completion receipt: `ST-01.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve shared lifecycle semantics while versioning target-specific source and state contracts.
- Fresh-context scope: One independently testable Lock a Safe Target-Specific Evidence Workspace increment covering 10 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-01.02 are accepted and the covered authority is available,
- When the Harness Architect validates a real target boundary and creates an immutable target-specific source lock,
- Then source material is portable, safe to inspect, and protected from mutation
- And failure behavior is explicit: Block invalid paths, unsafe archives, missing consent policy, unreadable authority, and any attempted source mutation.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve shared lifecycle semantics while versioning target-specific source and state contracts.

### ST-01.03 — Index Every Evidence Specimen with Provenance

As a **Evidence steward**, I want to **index every target specimen and its relationships under immutable evidence identity**, so that **later decisions can query complete evidence and distinguish observation, status, and provenance**

- Global order: `3`
- Dependencies: `ST-01.02`
- Primary outcome: later decisions can query complete evidence and distinguish observation, status, and provenance
- Primary obligations (4): `FR-014`, `FR-015`, `NFR-SCALE-001`, `NFR-TRACE-004`
- Relevant FRs: `FR-014`, `FR-015`
- Relevant NFRs: `NFR-SCALE-001`, `NFR-TRACE-004`
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-02`
- Component boundary: Run governance and configured evidence workspace; downstream design and execution remain outside this increment.
- Affected contracts: `RunLifecycle`, `EvidenceWorkspace`, `ConstitutionalReadinessReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ConstitutionalReadinessReceipt`
- Primary specifications: `TS-02`
- Test seam: Target-profile lifecycle and evidence public-seam scenarios with fail-closed fixtures.
- Gate references: `BD-004`, `HD-006`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Fail when specimens are unaccounted for, identities collide, provenance is missing, or corpus processing loses knowledge status.
- Observability evidence: `ST-01.03:OutcomeVerified`, `ST-01.03:OutcomeRejected`
- Required tests: `ST-01.03-acceptance`, `ST-01.03-failure`, `ST-01.03-authority`, `ST-01.03-receipt`
- Completion receipt: `ST-01.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve shared lifecycle semantics while versioning target-specific source and state contracts.
- Fresh-context scope: One independently testable Index Every Evidence Specimen with Provenance increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-01.03 are accepted and the covered authority is available,
- When the Evidence steward indexes every target specimen and its relationships under immutable evidence identity,
- Then later decisions can query complete evidence and distinguish observation, status, and provenance
- And failure behavior is explicit: Fail when specimens are unaccounted for, identities collide, provenance is missing, or corpus processing loses knowledge status.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve shared lifecycle semantics while versioning target-specific source and state contracts.

### ST-01.04 — Decide Evidence Saturation Without Inventing Claims

As a **Harness Architect**, I want to **evaluate the target saturation contract and classifies gaps or authority conflicts**, so that **the run proceeds, pauses, or blocks through an evidence-backed typed outcome**

- Global order: `4`
- Dependencies: `ST-01.03`
- Primary outcome: the run proceeds, pauses, or blocks through an evidence-backed typed outcome
- Primary obligations (4): `FR-016`, `FR-017`, `FR-018`, `HG-002`
- Relevant FRs: `FR-016`, `FR-017`, `FR-018`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-02`, `evaluation_governance`
- Component boundary: Run governance and configured evidence workspace; downstream design and execution remain outside this increment.
- Affected contracts: `RunLifecycle`, `EvidenceWorkspace`, `ConstitutionalReadinessReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ConstitutionalReadinessReceipt`
- Primary specifications: `TS-02`, `TS-03`, `TS-10`, `TS-13`
- Test seam: Target-profile lifecycle and evidence public-seam scenarios with fail-closed fixtures.
- Gate references: `BD-004`, `HD-006`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block critical claims without evidence and prohibit readiness or semantic invention from incomplete sources.
- Observability evidence: `ST-01.04:OutcomeVerified`, `ST-01.04:OutcomeRejected`
- Required tests: `ST-01.04-acceptance`, `ST-01.04-failure`, `ST-01.04-authority`, `ST-01.04-receipt`
- Completion receipt: `ST-01.04:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve shared lifecycle semantics while versioning target-specific source and state contracts.
- Fresh-context scope: One independently testable Decide Evidence Saturation Without Inventing Claims increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-01.04 are accepted and the covered authority is available,
- When the Harness Architect evaluates the target saturation contract and classifies gaps or authority conflicts,
- Then the run proceeds, pauses, or blocks through an evidence-backed typed outcome
- And failure behavior is explicit: Block critical claims without evidence and prohibit readiness or semantic invention from incomplete sources.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve shared lifecycle semantics while versioning target-specific source and state contracts.


## EP-02 — Syntax-Grounded Understanding and Atomic Boundary

**Epic outcome:** A reviewer can derive typed visual or conversational syntax evidence before meaning, distinguish observation from hypothesis, compare candidate product boundaries, and ratify one atomic Draft Harness Model with explicit uncertainty and wrong-boundary risk.

**Story count:** 5

### ST-02.01 — Normalize Evidence into Typed Syntax Observations

As a **Constitutional reviewer**, I want to **normalize and deduplicates visual or conversational specimens into typed syntax observations**, so that **reviewers can compare reliable geometry, components, turns, and evidence identities**

- Global order: `5`
- Dependencies: `ST-01.04`
- Primary outcome: reviewers can compare reliable geometry, components, turns, and evidence identities
- Primary obligations (6): `ADR-008`, `FR-019`, `FR-020`, `FR-021`, `FR-022`, `FR-023`
- Relevant FRs: `FR-019`, `FR-020`, `FR-021`, `FR-022`, `FR-023`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-03`, `Visual architecture, category steward, and benchmark team`
- Component boundary: Evidence understanding and atomic-boundary decision support; no runtime production or semantic invention.
- Affected contracts: `SyntaxObservation`, `DraftHarnessModel`, `SharedActivativeCore`, `ConversationalActivationExpression`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-03`, `TS-04`
- Test seam: Golden specimen, conversational transcript, ambiguity, and wrong-boundary fixtures at parser and ratification seams.
- Gate references: `BD-004`, `BD-007`, `HD-006`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject unsupported parser outputs, duplicate inflation, provider-only claims, and observation fields contaminated by hypotheses.
- Observability evidence: `ST-02.01:OutcomeVerified`, `ST-02.01:OutcomeRejected`
- Required tests: `ST-02.01-acceptance`, `ST-02.01-failure`, `ST-02.01-authority`, `ST-02.01-receipt`
- Completion receipt: `ST-02.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve Visual Syntax First for development and keep category-specific parse schemas versioned.
- Fresh-context scope: One independently testable Normalize Evidence into Typed Syntax Observations increment covering 6 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-02.01 are accepted and the covered authority is available,
- When the Constitutional reviewer normalizes and deduplicates visual or conversational specimens into typed syntax observations,
- Then reviewers can compare reliable geometry, components, turns, and evidence identities
- And failure behavior is explicit: Reject unsupported parser outputs, duplicate inflation, provider-only claims, and observation fields contaminated by hypotheses.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve Visual Syntax First for development and keep category-specific parse schemas versioned.

### ST-02.02 — Build Spatial, Temporal, and Reading-Order Graphs

As a **Constitutional reviewer**, I want to **parse spatial relationships, hierarchy, reading order, composition variables, and temporal syntax**, so that **the candidate grammar is grounded in substrate-specific relationships rather than vague meaning**

- Global order: `6`
- Dependencies: `ST-02.01`
- Primary outcome: the candidate grammar is grounded in substrate-specific relationships rather than vague meaning
- Primary obligations (4): `FR-024`, `FR-025`, `FR-026`, `FR-027`
- Relevant FRs: `FR-024`, `FR-025`, `FR-026`, `FR-027`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-03`
- Component boundary: Evidence understanding and atomic-boundary decision support; no runtime production or semantic invention.
- Affected contracts: `SyntaxObservation`, `DraftHarnessModel`, `SharedActivativeCore`, `ConversationalActivationExpression`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-03`
- Test seam: Golden specimen, conversational transcript, ambiguity, and wrong-boundary fixtures at parser and ratification seams.
- Gate references: `BD-004`, `BD-007`, `HD-006`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Fail on dangling graph targets, impossible geometry, missing time states, or category-inappropriate parse fields.
- Observability evidence: `ST-02.02:OutcomeVerified`, `ST-02.02:OutcomeRejected`
- Required tests: `ST-02.02-acceptance`, `ST-02.02-failure`, `ST-02.02-authority`, `ST-02.02-receipt`
- Completion receipt: `ST-02.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve Visual Syntax First for development and keep category-specific parse schemas versioned.
- Fresh-context scope: One independently testable Build Spatial, Temporal, and Reading-Order Graphs increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-02.02 are accepted and the covered authority is available,
- When the Constitutional reviewer parses spatial relationships, hierarchy, reading order, composition variables, and temporal syntax,
- Then the candidate grammar is grounded in substrate-specific relationships rather than vague meaning
- And failure behavior is explicit: Fail on dangling graph targets, impossible geometry, missing time states, or category-inappropriate parse fields.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve Visual Syntax First for development and keep category-specific parse schemas versioned.

### ST-02.03 — Induce Grammar Only After Syntax Evidence

As a **Harness Architect**, I want to **separate observations from WHY hypotheses and induces cross-specimen, sequence, and Activative hypotheses**, so that **Visual Syntax First governs development discovery while unsupported meaning stays visibly provisional**

- Global order: `7`
- Dependencies: `ST-02.02`
- Primary outcome: Visual Syntax First governs development discovery while unsupported meaning stays visibly provisional
- Primary obligations (7): `AG-006`, `AG-007`, `D007`, `FR-028`, `FR-029`, `FR-030`, `FR-031`
- Relevant FRs: `FR-028`, `FR-029`, `FR-030`, `FR-031`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-03`, `product_constitution`
- Component boundary: Evidence understanding and atomic-boundary decision support; no runtime production or semantic invention.
- Affected contracts: `SyntaxObservation`, `DraftHarnessModel`, `SharedActivativeCore`, `ConversationalActivationExpression`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-00`, `TS-02`, `TS-03`, `TS-05`, `TS-06`, `TS-07`, `TS-11`, `TS-12`
- Test seam: Golden specimen, conversational transcript, ambiguity, and wrong-boundary fixtures at parser and ratification seams.
- Gate references: `BD-004`, `BD-007`, `BD-008`, `HD-006`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject meaning-first inference, unsupported knowledge promotion, and category grammar that erases conversational or temporal evidence.
- Observability evidence: `ST-02.03:OutcomeVerified`, `ST-02.03:OutcomeRejected`
- Required tests: `ST-02.03-acceptance`, `ST-02.03-failure`, `ST-02.03-authority`, `ST-02.03-receipt`
- Completion receipt: `ST-02.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve Visual Syntax First for development and keep category-specific parse schemas versioned.
- Fresh-context scope: One independently testable Induce Grammar Only After Syntax Evidence increment covering 7 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-02.03 are accepted and the covered authority is available,
- When the Harness Architect separates observations from WHY hypotheses and induces cross-specimen, sequence, and Activative hypotheses,
- Then Visual Syntax First governs development discovery while unsupported meaning stays visibly provisional
- And failure behavior is explicit: Reject meaning-first inference, unsupported knowledge promotion, and category grammar that erases conversational or temporal evidence.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve Visual Syntax First for development and keep category-specific parse schemas versioned.

### ST-02.04 — Compare Candidate Atomic Product Boundaries

As a **Harness Architect**, I want to **compare merge, split, variant, and family boundaries with typed risk and recommendations**, so that **human authority can see the consequence of each candidate before choosing the atomic product**

- Global order: `8`
- Dependencies: `ST-02.03`
- Primary outcome: human authority can see the consequence of each candidate before choosing the atomic product
- Primary obligations (5): `D008`, `FR-032`, `FR-033`, `FR-034`, `FR-035`
- Relevant FRs: `FR-032`, `FR-033`, `FR-034`, `FR-035`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-04`, `product_constitution`
- Component boundary: Evidence understanding and atomic-boundary decision support; no runtime production or semantic invention.
- Affected contracts: `SyntaxObservation`, `DraftHarnessModel`, `SharedActivativeCore`, `ConversationalActivationExpression`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-03`, `TS-04`, `TS-11`
- Test seam: Golden specimen, conversational transcript, ambiguity, and wrong-boundary fixtures at parser and ratification seams.
- Gate references: `BD-004`, `BD-007`, `BD-008`, `HD-006`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block a recommendation that lacks evidence, hides alternatives, or uses an uncalibrated protected-boundary claim as certainty.
- Observability evidence: `ST-02.04:OutcomeVerified`, `ST-02.04:OutcomeRejected`
- Required tests: `ST-02.04-acceptance`, `ST-02.04-failure`, `ST-02.04-authority`, `ST-02.04-receipt`
- Completion receipt: `ST-02.04:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve Visual Syntax First for development and keep category-specific parse schemas versioned.
- Fresh-context scope: One independently testable Compare Candidate Atomic Product Boundaries increment covering 5 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-02.04 are accepted and the covered authority is available,
- When the Harness Architect compares merge, split, variant, and family boundaries with typed risk and recommendations,
- Then human authority can see the consequence of each candidate before choosing the atomic product
- And failure behavior is explicit: Block a recommendation that lacks evidence, hides alternatives, or uses an uncalibrated protected-boundary claim as certainty.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve Visual Syntax First for development and keep category-specific parse schemas versioned.

### ST-02.05 — Ratify and Freeze the Draft Harness Boundary

As a **Product authority**, I want to **ratify one atomic boundary and freezes a transparent Draft Harness Model for Genesis**, so that **downstream constitutional decisions start from an explicit, reviewable, and stable product boundary**

- Global order: `9`
- Dependencies: `ST-02.04`
- Primary outcome: downstream constitutional decisions start from an explicit, reviewable, and stable product boundary
- Primary obligations (6): `FR-036`, `FR-037`, `FR-038`, `FR-039`, `FR-040`, `HG-003`
- Relevant FRs: `FR-036`, `FR-037`, `FR-038`, `FR-039`, `FR-040`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-04`, `evaluation_governance`
- Component boundary: Evidence understanding and atomic-boundary decision support; no runtime production or semantic invention.
- Affected contracts: `SyntaxObservation`, `DraftHarnessModel`, `SharedActivativeCore`, `ConversationalActivationExpression`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-04`, `TS-11`, `TS-15`
- Test seam: Golden specimen, conversational transcript, ambiguity, and wrong-boundary fixtures at parser and ratification seams.
- Gate references: `BD-004`, `BD-007`, `HD-006`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject unratified promotion, freeze with unresolved critical boundary contradiction, and any later silent boundary rewrite.
- Observability evidence: `ST-02.05:OutcomeVerified`, `ST-02.05:OutcomeRejected`
- Required tests: `ST-02.05-acceptance`, `ST-02.05-failure`, `ST-02.05-authority`, `ST-02.05-receipt`
- Completion receipt: `ST-02.05:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve Visual Syntax First for development and keep category-specific parse schemas versioned.
- Fresh-context scope: One independently testable Ratify and Freeze the Draft Harness Boundary increment covering 6 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-02.05 are accepted and the covered authority is available,
- When the Product authority ratifies one atomic boundary and freezes a transparent Draft Harness Model for Genesis,
- Then downstream constitutional decisions start from an explicit, reviewable, and stable product boundary
- And failure behavior is explicit: Reject unratified promotion, freeze with unresolved critical boundary contradiction, and any later silent boundary rewrite.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve Visual Syntax First for development and keep category-specific parse schemas versioned.


## EP-03 — Human-Ratified Genesis and Canonical Harness Definition

**Epic outcome:** Human authority can answer only dependency-ready constitutional questions, preserve the evidence and recommendation trail, freeze ratified decisions, and compile one provenance-rich canonical Harness IR into consistent human and machine artifacts.

**Story count:** 5

### ST-03.01 — Ask Only Dependency-Ready Constitutional Questions

As a **Harness Architect**, I want to **open only dependency-ready Genesis decisions and presents one evidence-backed recommendation per turn**, so that **human attention is spent on the next consequential question with complete rationale**

- Global order: `10`
- Dependencies: `ST-01.04`, `ST-02.05`
- Primary outcome: human attention is spent on the next consequential question with complete rationale
- Primary obligations (7): `D009`, `D010`, `FR-041`, `FR-042`, `FR-043`, `FR-044`, `HG-001`
- Relevant FRs: `FR-041`, `FR-042`, `FR-043`, `FR-044`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-05`, `evaluation_governance`, `product_constitution`
- Component boundary: Genesis authority and canonical Harness IR compilation; no downstream product execution.
- Affected contracts: `GenesisDecisionReceipt`, `HarnessIR`, `SharedActivativeCore`, `ActivativeIntelligencePack`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`
- Primary specifications: `TS-01`, `TS-04`, `TS-05`, `TS-11`, `TS-12`, `TS-13`, `TS-14`
- Test seam: Decision-graph, receipt replay, canonical serialization, migration, and cross-artifact consistency seams.
- Gate references: `BD-004`, `BD-008`
- Implementation gate status: `EVIDENCE_GATED`
- Failure behavior: Block unsupported constitutional decisions, premature questions, or recommendations that omit relevant evidence and alternatives.
- Observability evidence: `ST-03.01:OutcomeVerified`, `ST-03.01:OutcomeRejected`
- Required tests: `ST-03.01-acceptance`, `ST-03.01-failure`, `ST-03.01-authority`, `ST-03.01-receipt`
- Completion receipt: `ST-03.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Use explicit IR schema migrations and preserve frozen authority, hashes, and Activative lineage.
- Fresh-context scope: One independently testable Ask Only Dependency-Ready Constitutional Questions increment covering 7 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-03.01 are accepted and the covered authority is available,
- When the Harness Architect opens only dependency-ready Genesis decisions and presents one evidence-backed recommendation per turn,
- Then human attention is spent on the next consequential question with complete rationale
- And failure behavior is explicit: Block unsupported constitutional decisions, premature questions, or recommendations that omit relevant evidence and alternatives.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Use explicit IR schema migrations and preserve frozen authority, hashes, and Activative lineage.

### ST-03.02 — Record Human Authority and Resume Genesis Safely

As a **Product authority**, I want to **record the human answer separately from the final decision, updates state transactionally, and resumes without replay**, so that **human authority remains explicit, auditable, and recoverable across sessions**

- Global order: `11`
- Dependencies: `ST-03.01`
- Primary outcome: human authority remains explicit, auditable, and recoverable across sessions
- Primary obligations (8): `ADR-005`, `D002`, `FR-045`, `FR-046`, `FR-047`, `FR-048`, `FR-049`, `FR-050`
- Relevant FRs: `FR-045`, `FR-046`, `FR-047`, `FR-048`, `FR-049`, `FR-050`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `Product authority, security, and architecture`, `TS-05`, `product_constitution`
- Component boundary: Genesis authority and canonical Harness IR compilation; no downstream product execution.
- Affected contracts: `GenesisDecisionReceipt`, `HarnessIR`, `SharedActivativeCore`, `ActivativeIntelligencePack`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`
- Primary specifications: `TS-01`, `TS-04`, `TS-05`, `TS-07`, `TS-12`, `TS-13`, `TS-14`
- Test seam: Decision-graph, receipt replay, canonical serialization, migration, and cross-artifact consistency seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Reject agent substitution for required human authority, partial decision commits, contradictory cascade locks, and replayed approvals.
- Observability evidence: `ST-03.02:OutcomeVerified`, `ST-03.02:OutcomeRejected`
- Required tests: `ST-03.02-acceptance`, `ST-03.02-failure`, `ST-03.02-authority`, `ST-03.02-receipt`
- Completion receipt: `ST-03.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Use explicit IR schema migrations and preserve frozen authority, hashes, and Activative lineage.
- Fresh-context scope: One independently testable Record Human Authority and Resume Genesis Safely increment covering 8 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-03.02 are accepted and the covered authority is available,
- When the Product authority records the human answer separately from the final decision, updates state transactionally, and resumes without replay,
- Then human authority remains explicit, auditable, and recoverable across sessions
- And failure behavior is explicit: Reject agent substitution for required human authority, partial decision commits, contradictory cascade locks, and replayed approvals.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Use explicit IR schema migrations and preserve frozen authority, hashes, and Activative lineage.

### ST-03.03 — Maintain One Provenance-Rich Canonical Harness IR

As a **Compiler maintainer**, I want to **write ratified values and frozen references into one versioned canonical Harness IR**, so that **all downstream artifacts share one source of truth with explicit schema evolution and Activative lineage**

- Global order: `12`
- Dependencies: `ST-03.02`
- Primary outcome: all downstream artifacts share one source of truth with explicit schema evolution and Activative lineage
- Primary obligations (8): `ADR-002`, `D011`, `FR-051`, `FR-052`, `FR-053`, `NFR-COMPAT-002`, `NFR-COMPAT-003`, `NFR-TRACE-001`
- Relevant FRs: `FR-051`, `FR-052`, `FR-053`
- Relevant NFRs: `NFR-COMPAT-002`, `NFR-COMPAT-003`, `NFR-TRACE-001`
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `Architecture`, `TS-06`, `product_constitution`
- Component boundary: Genesis authority and canonical Harness IR compilation; no downstream product execution.
- Affected contracts: `GenesisDecisionReceipt`, `HarnessIR`, `SharedActivativeCore`, `ActivativeIntelligencePack`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`
- Primary specifications: `TS-03`, `TS-04`, `TS-05`, `TS-06`, `TS-07`, `TS-11`, `TS-12`, `TS-13`, `TS-14`
- Test seam: Decision-graph, receipt replay, canonical serialization, migration, and cross-artifact consistency seams.
- Gate references: `BD-014`
- Implementation gate status: `EVIDENCE_GATED`
- Failure behavior: Fail on missing provenance, incompatible schema changes, local semantic copies, or divergence between Harness IR and Workflow IR ownership.
- Observability evidence: `ST-03.03:OutcomeVerified`, `ST-03.03:OutcomeRejected`
- Required tests: `ST-03.03-acceptance`, `ST-03.03-failure`, `ST-03.03-authority`, `ST-03.03-receipt`
- Completion receipt: `ST-03.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Use explicit IR schema migrations and preserve frozen authority, hashes, and Activative lineage.
- Fresh-context scope: One independently testable Maintain One Provenance-Rich Canonical Harness IR increment covering 8 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-03.03 are accepted and the covered authority is available,
- When the Compiler maintainer writes ratified values and frozen references into one versioned canonical Harness IR,
- Then all downstream artifacts share one source of truth with explicit schema evolution and Activative lineage
- And failure behavior is explicit: Fail on missing provenance, incompatible schema changes, local semantic copies, or divergence between Harness IR and Workflow IR ownership.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Use explicit IR schema migrations and preserve frozen authority, hashes, and Activative lineage.

### ST-03.04 — Compile Human and Machine Artifacts Deterministically

As a **Compiler maintainer**, I want to **compile sharded specifications, OpenSpec views, and machine artifacts from the same IR**, so that **maintainers receive reproducible, hash-bound outputs without duplicated authority**

- Global order: `13`
- Dependencies: `ST-03.03`
- Primary outcome: maintainers receive reproducible, hash-bound outputs without duplicated authority
- Primary obligations (10): `ADR-004`, `AG-018`, `FR-054`, `FR-055`, `FR-056`, `FR-057`, `FR-058`, `NFR-MAINT-001`, `NFR-REL-001`, `NFR-REL-003`
- Relevant FRs: `FR-054`, `FR-055`, `FR-056`, `FR-057`, `FR-058`
- Relevant NFRs: `NFR-MAINT-001`, `NFR-REL-001`, `NFR-REL-003`
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `Compiler and schema architecture`, `TS-06`, `product_constitution`
- Component boundary: Genesis authority and canonical Harness IR compilation; no downstream product execution.
- Affected contracts: `GenesisDecisionReceipt`, `HarnessIR`, `SharedActivativeCore`, `ActivativeIntelligencePack`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`
- Primary specifications: `TS-00`, `TS-06`, `TS-07`, `TS-09`, `TS-13`
- Test seam: Decision-graph, receipt replay, canonical serialization, migration, and cross-artifact consistency seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Reject manual drift, nondeterministic serialization, incomplete artifact sets, unresolved references, and non-idempotent recompilation.
- Observability evidence: `ST-03.04:OutcomeVerified`, `ST-03.04:OutcomeRejected`
- Required tests: `ST-03.04-acceptance`, `ST-03.04-failure`, `ST-03.04-authority`, `ST-03.04-receipt`
- Completion receipt: `ST-03.04:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Use explicit IR schema migrations and preserve frozen authority, hashes, and Activative lineage.
- Fresh-context scope: One independently testable Compile Human and Machine Artifacts Deterministically increment covering 10 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-03.04 are accepted and the covered authority is available,
- When the Compiler maintainer compiles sharded specifications, OpenSpec views, and machine artifacts from the same IR,
- Then maintainers receive reproducible, hash-bound outputs without duplicated authority
- And failure behavior is explicit: Reject manual drift, nondeterministic serialization, incomplete artifact sets, unresolved references, and non-idempotent recompilation.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Use explicit IR schema migrations and preserve frozen authority, hashes, and Activative lineage.

### ST-03.05 — Enforce Constitutional Precedence Across Compiled Artifacts

As a **Constitutional reviewer**, I want to **validate cross-artifact completeness and constitutional precedence before release**, so that **lower-authority artifacts cannot override Constitution V1.1 or lose semantic lineage**

- Global order: `14`
- Dependencies: `ST-03.04`
- Primary outcome: lower-authority artifacts cannot override Constitution V1.1 or lose semantic lineage
- Primary obligations (2): `CONST-001`, `FR-059`
- Relevant FRs: `FR-059`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-06`, `constitutional_alignment_and_mapped_spec_owners`
- Component boundary: Genesis authority and canonical Harness IR compilation; no downstream product execution.
- Affected contracts: `GenesisDecisionReceipt`, `HarnessIR`, `SharedActivativeCore`, `ActivativeIntelligencePack`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`
- Primary specifications: `TS-00`, `TS-01`, `TS-06`, `TS-13`
- Test seam: Decision-graph, receipt replay, canonical serialization, migration, and cross-artifact consistency seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Block any conflict, missing constitutional applicability, or artifact set that passes syntax while violating higher authority.
- Observability evidence: `ST-03.05:OutcomeVerified`, `ST-03.05:OutcomeRejected`
- Required tests: `ST-03.05-acceptance`, `ST-03.05-failure`, `ST-03.05-authority`, `ST-03.05-receipt`
- Completion receipt: `ST-03.05:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Use explicit IR schema migrations and preserve frozen authority, hashes, and Activative lineage.
- Fresh-context scope: One independently testable Enforce Constitutional Precedence Across Compiled Artifacts increment covering 2 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-03.05 are accepted and the covered authority is available,
- When the Constitutional reviewer validates cross-artifact completeness and constitutional precedence before release,
- Then lower-authority artifacts cannot override Constitution V1.1 or lose semantic lineage
- And failure behavior is explicit: Block any conflict, missing constitutional applicability, or artifact set that passes syntax while violating higher authority.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Use explicit IR schema migrations and preserve frozen authority, hashes, and Activative lineage.


## EP-04 — Owned Capability Graphs and Minimum Complete Context

**Epic outcome:** A maintainer can see who or what owns every capability, how responsibility-centered modules and phases connect, what each handoff may change, and the minimum complete context required for reliable work.

**Story count:** 5

### ST-04.01 — Assign Explicit Ownership to Every Required Capability

As a **Harness Architect**, I want to **inventory capabilities and assigns code, agent, human, external, or hybrid ownership using reliability and cost evidence**, so that **the design has accountable owners and no capability disappears between product intent and execution**

- Global order: `15`
- Dependencies: `ST-03.05`
- Primary outcome: the design has accountable owners and no capability disappears between product intent and execution
- Primary obligations (5): `D012`, `FR-060`, `FR-061`, `FR-062`, `FR-063`
- Relevant FRs: `FR-060`, `FR-061`, `FR-062`, `FR-063`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-07`, `product_constitution`
- Component boundary: Capability, module, phase, context, reference, and handoff architecture; no hidden orchestration implementation.
- Affected contracts: `CapabilityOwnership`, `PhaseContract`, `ContextContract`, `HandoffContract`, `ReferenceContract`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-03`, `TS-07`, `TS-08`, `TS-09`, `TS-14`
- Test seam: Ownership, graph integrity, handoff mutation, impact-analysis, and context-budget contract seams.
- Gate references: `BD-010`
- Implementation gate status: `EVIDENCE_GATED`
- Failure behavior: Reject unowned capabilities, unjustified agent ownership, universal-skill defaults, and hybrids without explicit handoff responsibility.
- Observability evidence: `ST-04.01:OutcomeVerified`, `ST-04.01:OutcomeRejected`
- Required tests: `ST-04.01-acceptance`, `ST-04.01-failure`, `ST-04.01-authority`, `ST-04.01-receipt`
- Completion receipt: `ST-04.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version graph and handoff contracts; reject silent downstream rewriting or required-context truncation.
- Fresh-context scope: One independently testable Assign Explicit Ownership to Every Required Capability increment covering 5 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-04.01 are accepted and the covered authority is available,
- When the Harness Architect inventories capabilities and assigns code, agent, human, external, or hybrid ownership using reliability and cost evidence,
- Then the design has accountable owners and no capability disappears between product intent and execution
- And failure behavior is explicit: Reject unowned capabilities, unjustified agent ownership, universal-skill defaults, and hybrids without explicit handoff responsibility.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version graph and handoff contracts; reject silent downstream rewriting or required-context truncation.

### ST-04.02 — Compile Responsibility-Centered Modules with Test Seams

As a **Architecture maintainer**, I want to **group capabilities into responsibility-centered modules with declared public test seams**, so that **each module can change and be tested without recreating horizontal technical layers**

- Global order: `16`
- Dependencies: `ST-04.01`
- Primary outcome: each module can change and be tested without recreating horizontal technical layers
- Primary obligations (3): `D015`, `FR-064`, `FR-065`
- Relevant FRs: `FR-064`, `FR-065`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-07`, `product_constitution`
- Component boundary: Capability, module, phase, context, reference, and handoff architecture; no hidden orchestration implementation.
- Affected contracts: `CapabilityOwnership`, `PhaseContract`, `ContextContract`, `HandoffContract`, `ReferenceContract`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-07`, `TS-12`, `TS-13`, `TS-14`
- Test seam: Ownership, graph integrity, handoff mutation, impact-analysis, and context-budget contract seams.
- Gate references: None
- Implementation gate status: `PLANNING_COMPLETE_IMPLEMENTATION_PROHIBITED`
- Failure behavior: Block mixed-authority modules, hidden side effects, missing seams, and modules defined only as database, API, UI, router, or agent layers.
- Observability evidence: `ST-04.02:OutcomeVerified`, `ST-04.02:OutcomeRejected`
- Required tests: `ST-04.02-acceptance`, `ST-04.02-failure`, `ST-04.02-authority`, `ST-04.02-receipt`
- Completion receipt: `ST-04.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version graph and handoff contracts; reject silent downstream rewriting or required-context truncation.
- Fresh-context scope: One independently testable Compile Responsibility-Centered Modules with Test Seams increment covering 3 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-04.02 are accepted and the covered authority is available,
- When the Architecture maintainer groups capabilities into responsibility-centered modules with declared public test seams,
- Then each module can change and be tested without recreating horizontal technical layers
- And failure behavior is explicit: Block mixed-authority modules, hidden side effects, missing seams, and modules defined only as database, API, UI, router, or agent layers.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version graph and handoff contracts; reject silent downstream rewriting or required-context truncation.

### ST-04.03 — Order Work Through an Executable Phase Graph

As a **Harness Architect**, I want to **compile sequential and dependency-independent phase relationships**, so that **the harness exposes what may run now, later, or safely in parallel**

- Global order: `17`
- Dependencies: `ST-04.02`
- Primary outcome: the harness exposes what may run now, later, or safely in parallel
- Primary obligations (3): `D013`, `FR-066`, `FR-067`
- Relevant FRs: `FR-066`, `FR-067`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-07`, `product_constitution`
- Component boundary: Capability, module, phase, context, reference, and handoff architecture; no hidden orchestration implementation.
- Affected contracts: `CapabilityOwnership`, `PhaseContract`, `ContextContract`, `HandoffContract`, `ReferenceContract`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-07`, `TS-12`, `TS-14`
- Test seam: Ownership, graph integrity, handoff mutation, impact-analysis, and context-budget contract seams.
- Gate references: None
- Implementation gate status: `PLANNING_COMPLETE_IMPLEMENTATION_PROHIBITED`
- Failure behavior: Reject cycles, undeclared dependencies, default parallelism, and phase edges that bypass required human or validation gates.
- Observability evidence: `ST-04.03:OutcomeVerified`, `ST-04.03:OutcomeRejected`
- Required tests: `ST-04.03-acceptance`, `ST-04.03-failure`, `ST-04.03-authority`, `ST-04.03-receipt`
- Completion receipt: `ST-04.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version graph and handoff contracts; reject silent downstream rewriting or required-context truncation.
- Fresh-context scope: One independently testable Order Work Through an Executable Phase Graph increment covering 3 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-04.03 are accepted and the covered authority is available,
- When the Harness Architect compiles sequential and dependency-independent phase relationships,
- Then the harness exposes what may run now, later, or safely in parallel
- And failure behavior is explicit: Reject cycles, undeclared dependencies, default parallelism, and phase edges that bypass required human or validation gates.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version graph and handoff contracts; reject silent downstream rewriting or required-context truncation.

### ST-04.04 — Protect Typed Phase and Context Handoffs

As a **Architecture maintainer**, I want to **compile phase-specific contexts and versioned handoffs with ownership and mutation limits**, so that **downstream work receives complete inputs without silently rewriting upstream truth**

- Global order: `18`
- Dependencies: `ST-04.03`
- Primary outcome: downstream work receives complete inputs without silently rewriting upstream truth
- Primary obligations (9): `D014`, `FR-068`, `FR-069`, `FR-070`, `FR-071`, `HG-004`, `HG-005`, `HG-007`, `NFR-ARCH-001`
- Relevant FRs: `FR-068`, `FR-069`, `FR-070`, `FR-071`
- Relevant NFRs: `NFR-ARCH-001`
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-07`, `evaluation_governance`, `product_constitution`
- Component boundary: Capability, module, phase, context, reference, and handoff architecture; no hidden orchestration implementation.
- Affected contracts: `CapabilityOwnership`, `PhaseContract`, `ContextContract`, `HandoffContract`, `ReferenceContract`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-01`, `TS-03`, `TS-05`, `TS-06`, `TS-07`, `TS-11`, `TS-12`, `TS-13`, `TS-14`
- Test seam: Ownership, graph integrity, handoff mutation, impact-analysis, and context-budget contract seams.
- Gate references: `BD-014`
- Implementation gate status: `EVIDENCE_GATED`
- Failure behavior: Block contract contradictions, missing authority, silent rewrites, dangling dependencies, and invalidation that reruns unaffected state.
- Observability evidence: `ST-04.04:OutcomeVerified`, `ST-04.04:OutcomeRejected`
- Required tests: `ST-04.04-acceptance`, `ST-04.04-failure`, `ST-04.04-authority`, `ST-04.04-receipt`
- Completion receipt: `ST-04.04:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version graph and handoff contracts; reject silent downstream rewriting or required-context truncation.
- Fresh-context scope: One independently testable Protect Typed Phase and Context Handoffs increment covering 9 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-04.04 are accepted and the covered authority is available,
- When the Architecture maintainer compiles phase-specific contexts and versioned handoffs with ownership and mutation limits,
- Then downstream work receives complete inputs without silently rewriting upstream truth
- And failure behavior is explicit: Block contract contradictions, missing authority, silent rewrites, dangling dependencies, and invalidation that reruns unaffected state.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version graph and handoff contracts; reject silent downstream rewriting or required-context truncation.

### ST-04.05 — Compile Minimum Complete Context Without Silent Truncation

As a **Context architect**, I want to **select references, SPR, progressive-disclosure pointers, and context budgets by functional necessity**, so that **each phase receives the minimum complete context plus a complete manifest**

- Global order: `19`
- Dependencies: `ST-04.04`
- Primary outcome: each phase receives the minimum complete context plus a complete manifest
- Primary obligations (13): `AG-012`, `AG-013`, `D016`, `D020`, `FR-072`, `FR-073`, `FR-074`, `FR-075`, `FR-076`, `FR-077`, `FR-078`, `FR-079`, `FR-080`
- Relevant FRs: `FR-072`, `FR-073`, `FR-074`, `FR-075`, `FR-076`, `FR-077`, `FR-078`, `FR-079`, `FR-080`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-07`, `product_constitution`
- Component boundary: Capability, module, phase, context, reference, and handoff architecture; no hidden orchestration implementation.
- Affected contracts: `CapabilityOwnership`, `PhaseContract`, `ContextContract`, `HandoffContract`, `ReferenceContract`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-00`, `TS-07`, `TS-08`, `TS-09`, `TS-12`, `TS-14`
- Test seam: Ownership, graph integrity, handoff mutation, impact-analysis, and context-budget contract seams.
- Gate references: `BD-010`
- Implementation gate status: `EVIDENCE_GATED`
- Failure behavior: Block missing required pointers, conversation-history substitution, silent truncation, unbounded loading, and budgets that hide omitted authority.
- Observability evidence: `ST-04.05:OutcomeVerified`, `ST-04.05:OutcomeRejected`
- Required tests: `ST-04.05-acceptance`, `ST-04.05-failure`, `ST-04.05-authority`, `ST-04.05-receipt`
- Completion receipt: `ST-04.05:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version graph and handoff contracts; reject silent downstream rewriting or required-context truncation.
- Fresh-context scope: One independently testable Compile Minimum Complete Context Without Silent Truncation increment covering 13 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-04.05 are accepted and the covered authority is available,
- When the Context architect selects references, SPR, progressive-disclosure pointers, and context budgets by functional necessity,
- Then each phase receives the minimum complete context plus a complete manifest
- And failure behavior is explicit: Block missing required pointers, conversation-history substitution, silent truncation, unbounded loading, and budgets that hide omitted authority.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version graph and handoff contracts; reject silent downstream rewriting or required-context truncation.


## EP-05 — Reusable Evaluated Skills and Deterministic JIT Capsules

**Epic outcome:** A maintainer can reuse, adapt, or justify new skills through capability-gap evidence, bind them to behavioral evaluation, and assemble deterministic phase-local capsules containing only the authority and context needed for the current task.

**Story count:** 5

### ST-05.01 — Operate a Versioned Canonical Skill Registry

As a **Skill maintainer**, I want to **register canonical skills by authority lane, maturity, plasticity, and evaluated identity**, so that **the team can distinguish stable reusable behavior from local adaptation and experimental capability**

- Global order: `20`
- Dependencies: `ST-04.05`
- Primary outcome: the team can distinguish stable reusable behavior from local adaptation and experimental capability
- Primary obligations (5): `D021`, `FR-081`, `FR-082`, `FR-083`, `NFR-MAINT-002`
- Relevant FRs: `FR-081`, `FR-082`, `FR-083`
- Relevant NFRs: `NFR-MAINT-002`
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-08`, `product_constitution`
- Component boundary: Canonical skill ecology and phase-local capsule compilation; production workflow ownership stays outside skills.
- Affected contracts: `SkillPackage`, `SkillRecipe`, `PhaseCapsule`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `IMPLEMENTATION_BASELINE`, `TS-06`, `TS-07`, `TS-08`, `TS-09`, `TS-10`, `TS-11`, `TS-12`, `TS-13`, `TS-14`
- Test seam: Capability-gap, no-guidance control, package validation, binding resolution, and deterministic capsule seams.
- Gate references: `BD-004`, `BD-008`, `BD-010`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject duplicate capability claims, maturity without receipts, stale evaluator pins, and skill sediment hidden as active behavior.
- Observability evidence: `ST-05.01:OutcomeVerified`, `ST-05.01:OutcomeRejected`
- Required tests: `ST-05.01-acceptance`, `ST-05.01-failure`, `ST-05.01-authority`, `ST-05.01-receipt`
- Completion receipt: `ST-05.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin skill, recipe, binding, evaluator, and source versions; preserve portable skill package contracts.
- Fresh-context scope: One independently testable Operate a Versioned Canonical Skill Registry increment covering 5 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-05.01 are accepted and the covered authority is available,
- When the Skill maintainer registers canonical skills by authority lane, maturity, plasticity, and evaluated identity,
- Then the team can distinguish stable reusable behavior from local adaptation and experimental capability
- And failure behavior is explicit: Reject duplicate capability claims, maturity without receipts, stale evaluator pins, and skill sediment hidden as active behavior.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin skill, recipe, binding, evaluator, and source versions; preserve portable skill package contracts.

### ST-05.02 — Prove a Skill Is Needed Before Designing It

As a **Harness Architect**, I want to **run the capability-gap test and prefers reuse, adaptation, or adapter composition**, so that **new skill work begins only where behavior evidence shows a real gap**

- Global order: `21`
- Dependencies: `ST-05.01`
- Primary outcome: new skill work begins only where behavior evidence shows a real gap
- Primary obligations (4): `AG-008`, `FR-084`, `FR-085`, `FR-086`
- Relevant FRs: `FR-084`, `FR-085`, `FR-086`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-08`, `product_constitution`
- Component boundary: Canonical skill ecology and phase-local capsule compilation; production workflow ownership stays outside skills.
- Affected contracts: `SkillPackage`, `SkillRecipe`, `PhaseCapsule`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-00`, `TS-07`, `TS-08`
- Test seam: Capability-gap, no-guidance control, package validation, binding resolution, and deterministic capsule seams.
- Gate references: `BD-010`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject skill creation when the control has no target failure, ownership belongs in code or workflow, or an existing capability is adequate.
- Observability evidence: `ST-05.02:OutcomeVerified`, `ST-05.02:OutcomeRejected`
- Required tests: `ST-05.02-acceptance`, `ST-05.02-failure`, `ST-05.02-authority`, `ST-05.02-receipt`
- Completion receipt: `ST-05.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin skill, recipe, binding, evaluator, and source versions; preserve portable skill package contracts.
- Fresh-context scope: One independently testable Prove a Skill Is Needed Before Designing It increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-05.02 are accepted and the covered authority is available,
- When the Harness Architect runs the capability-gap test and prefers reuse, adaptation, or adapter composition,
- Then new skill work begins only where behavior evidence shows a real gap
- And failure behavior is explicit: Reject skill creation when the control has no target failure, ownership belongs in code or workflow, or an existing capability is adequate.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin skill, recipe, binding, evaluator, and source versions; preserve portable skill package contracts.

### ST-05.03 — Package Portable Skills with Behavioral Anchors

As a **Skill maintainer**, I want to **compile tested leading words, progressive disclosure, evaluation links, and no-op detection into a portable package**, so that **skill behavior is attributable, maintainable, and reusable across compatible harnesses**

- Global order: `22`
- Dependencies: `ST-05.02`
- Primary outcome: skill behavior is attributable, maintainable, and reusable across compatible harnesses
- Primary obligations (6): `AG-010`, `D017`, `FR-087`, `FR-088`, `FR-089`, `FR-090`
- Relevant FRs: `FR-087`, `FR-088`, `FR-089`, `FR-090`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-08`, `product_constitution`
- Component boundary: Canonical skill ecology and phase-local capsule compilation; production workflow ownership stays outside skills.
- Affected contracts: `SkillPackage`, `SkillRecipe`, `PhaseCapsule`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-00`, `TS-07`, `TS-08`, `TS-09`, `TS-10`, `TS-12`, `TS-14`
- Test seam: Capability-gap, no-guidance control, package validation, binding resolution, and deterministic capsule seams.
- Gate references: `BD-010`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block packages without behavioral lift, evaluator assets, authority boundaries, or evidence that redundant instructions were removed.
- Observability evidence: `ST-05.03:OutcomeVerified`, `ST-05.03:OutcomeRejected`
- Required tests: `ST-05.03-acceptance`, `ST-05.03-failure`, `ST-05.03-authority`, `ST-05.03-receipt`
- Completion receipt: `ST-05.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin skill, recipe, binding, evaluator, and source versions; preserve portable skill package contracts.
- Fresh-context scope: One independently testable Package Portable Skills with Behavioral Anchors increment covering 6 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-05.03 are accepted and the covered authority is available,
- When the Skill maintainer compiles tested leading words, progressive disclosure, evaluation links, and no-op detection into a portable package,
- Then skill behavior is attributable, maintainable, and reusable across compatible harnesses
- And failure behavior is explicit: Block packages without behavioral lift, evaluator assets, authority boundaries, or evidence that redundant instructions were removed.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin skill, recipe, binding, evaluator, and source versions; preserve portable skill package contracts.

### ST-05.04 — Assemble a Deterministic Phase-Local JIT Capsule

As a **Capsule compiler maintainer**, I want to **resolve recipes, bindings, precedence, degradation rules, and minimum complete context into one capsule**, so that **an agent receives exactly the evaluated authority and context needed for the current phase**

- Global order: `23`
- Dependencies: `ST-05.03`
- Primary outcome: an agent receives exactly the evaluated authority and context needed for the current phase
- Primary obligations (14): `ADR-009`, `AG-009`, `D018`, `D019`, `FR-091`, `FR-092`, `FR-093`, `FR-094`, `FR-095`, `FR-096`, `FR-097`, `FR-098`, `FR-099`, `HG-006`
- Relevant FRs: `FR-091`, `FR-092`, `FR-093`, `FR-094`, `FR-095`, `FR-096`, `FR-097`, `FR-098`, `FR-099`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `Skill architecture`, `TS-09`, `evaluation_governance`, `product_constitution`
- Component boundary: Canonical skill ecology and phase-local capsule compilation; production workflow ownership stays outside skills.
- Affected contracts: `SkillPackage`, `SkillRecipe`, `PhaseCapsule`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-00`, `TS-05`, `TS-07`, `TS-08`, `TS-09`, `TS-10`, `TS-12`, `TS-13`, `TS-14`
- Test seam: Capability-gap, no-guidance control, package validation, binding resolution, and deterministic capsule seams.
- Gate references: `BD-010`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block unresolved bindings, untested required skills, authority conflicts, forbidden degradation, and confusion between canonical skills and runtime capsules.
- Observability evidence: `ST-05.04:OutcomeVerified`, `ST-05.04:OutcomeRejected`
- Required tests: `ST-05.04-acceptance`, `ST-05.04-failure`, `ST-05.04-authority`, `ST-05.04-receipt`
- Completion receipt: `ST-05.04:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin skill, recipe, binding, evaluator, and source versions; preserve portable skill package contracts.
- Fresh-context scope: One independently testable Assemble a Deterministic Phase-Local JIT Capsule increment covering 14 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-05.04 are accepted and the covered authority is available,
- When the Capsule compiler maintainer resolves recipes, bindings, precedence, degradation rules, and minimum complete context into one capsule,
- Then an agent receives exactly the evaluated authority and context needed for the current phase
- And failure behavior is explicit: Block unresolved bindings, untested required skills, authority conflicts, forbidden degradation, and confusion between canonical skills and runtime capsules.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin skill, recipe, binding, evaluator, and source versions; preserve portable skill package contracts.

### ST-05.05 — Pin and Dispose of Capsules Reproducibly

As a **Capsule compiler maintainer**, I want to **bind exact versions and hashes, executes within bounded stochastic policy, and treats capsules as ephemeral**, so that **a phase can be replayed without accumulating hidden conversational state or stale capsule sediment**

- Global order: `24`
- Dependencies: `ST-05.04`
- Primary outcome: a phase can be replayed without accumulating hidden conversational state or stale capsule sediment
- Primary obligations (3): `FR-100`, `FR-101`, `FR-102`
- Relevant FRs: `FR-100`, `FR-101`, `FR-102`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-09`
- Component boundary: Canonical skill ecology and phase-local capsule compilation; production workflow ownership stays outside skills.
- Affected contracts: `SkillPackage`, `SkillRecipe`, `PhaseCapsule`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-09`
- Test seam: Capability-gap, no-guidance control, package validation, binding resolution, and deterministic capsule seams.
- Gate references: `BD-010`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject unpinned inputs, persistent phase-local context, nondeterministic assembly, and reuse outside the declared capsule scope.
- Observability evidence: `ST-05.05:OutcomeVerified`, `ST-05.05:OutcomeRejected`
- Required tests: `ST-05.05-acceptance`, `ST-05.05-failure`, `ST-05.05-authority`, `ST-05.05-receipt`
- Completion receipt: `ST-05.05:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin skill, recipe, binding, evaluator, and source versions; preserve portable skill package contracts.
- Fresh-context scope: One independently testable Pin and Dispose of Capsules Reproducibly increment covering 3 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-05.05 are accepted and the covered authority is available,
- When the Capsule compiler maintainer binds exact versions and hashes, executes within bounded stochastic policy, and treats capsules as ephemeral,
- Then a phase can be replayed without accumulating hidden conversational state or stale capsule sediment
- And failure behavior is explicit: Reject unpinned inputs, persistent phase-local context, nondeterministic assembly, and reuse outside the declared capsule scope.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin skill, recipe, binding, evaluator, and source versions; preserve portable skill package contracts.


## EP-06 — Five-Category Activative Intelligence and Expression Compilation

**Epic outcome:** A category steward can preserve one Shared Activative Core and compile category-native syntax, sequence, runtime, evaluation, and repair contracts for all five canonical categories, including first-class Conversational Activation / Human Expression profiles.

**Story count:** 5

### ST-06.01 — Bind Every Harness to One of Five Canonical Categories

As a **Category steward**, I want to **compile the Shared Activative Core through one governed category and versioned category constitution**, so that **all five categories remain distinct while preserving shared meaning and atomic creative ownership**

- Global order: `25`
- Dependencies: `ST-02.05`, `ST-03.05`, `ST-04.05`
- Primary outcome: all five categories remain distinct while preserving shared meaning and atomic creative ownership
- Primary obligations (13): `AG-003`, `AG-004`, `CONST-002`, `D030`, `D031`, `FR-137`, `FR-138`, `FR-139`, `FR-140`, `FR-141`, `HG-015`, `NFR-CAT-001`, `NFR-CAT-002`
- Relevant FRs: `FR-137`, `FR-138`, `FR-139`, `FR-140`, `FR-141`
- Relevant NFRs: `NFR-CAT-001`, `NFR-CAT-002`
- Release 1 disposition: `RELEASE_1_FORMAT02_PRODUCTION_OTHER_CATEGORIES_STRUCTURAL_UNCERTIFIED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-11`, `constitutional_alignment_and_mapped_spec_owners`, `evaluation_governance`, `product_constitution`
- Component boundary: Five-category and conversational profile contract compilation; live Interview and ReelCast execution remain external.
- Affected contracts: `SharedActivativeCore`, `ActivativeIntelligencePack`, `ConversationalActivationExpression`, `ActivativeCall`, `ReactionReceipt`, `ExpressionMoment`, `IdentityDNAAmendmentProposal`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-00`, `TS-01`, `TS-03`, `TS-04`, `TS-06`, `TS-07`, `TS-10`, `TS-11`, `TS-12`, `TS-13`, `TS-15`
- Test seam: Category/profile schema, rich-to-sparse lineage, sequencing, Reaction Receipt, Expression Moment, and HG-015 seams.
- Gate references: `BD-004`, `BD-007`, `BD-008`, `BD-010`, `BD-014`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block unsupported categories, flattened category IDs, missing conversational category support, absent wrong-reading locks, and semantic stacks that fail HG-015.
- Observability evidence: `ST-06.01:OutcomeVerified`, `ST-06.01:OutcomeRejected`
- Required tests: `ST-06.01-acceptance`, `ST-06.01-failure`, `ST-06.01-authority`, `ST-06.01-receipt`
- Completion receipt: `ST-06.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve all five category IDs, four conversational profile IDs, Activation First runtime law, and Visual Syntax First development law.
- Fresh-context scope: One independently testable Bind Every Harness to One of Five Canonical Categories increment covering 13 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-06.01 are accepted and the covered authority is available,
- When the Category steward compiles the Shared Activative Core through one governed category and versioned category constitution,
- Then all five categories remain distinct while preserving shared meaning and atomic creative ownership
- And failure behavior is explicit: Block unsupported categories, flattened category IDs, missing conversational category support, absent wrong-reading locks, and semantic stacks that fail HG-015.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve all five category IDs, four conversational profile IDs, Activation First runtime law, and Visual Syntax First development law.

### ST-06.02 — Compile Category-Local Format and Performance Profiles

As a **Category steward**, I want to **map edited-video formats and Format 02 character-performance registries into their owning category profiles**, so that **each format inherits the correct substrate grammar rather than acting as a cosmetic theme**

- Global order: `26`
- Dependencies: `ST-06.01`
- Primary outcome: each format inherits the correct substrate grammar rather than acting as a cosmetic theme
- Primary obligations (4): `AG-005`, `FR-142`, `FR-143`, `FR-144`
- Relevant FRs: `FR-142`, `FR-143`, `FR-144`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_FORMAT02_PRODUCTION_OTHER_CATEGORIES_STRUCTURAL_UNCERTIFIED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-11`, `product_constitution`
- Component boundary: Five-category and conversational profile contract compilation; live Interview and ReelCast execution remain external.
- Affected contracts: `SharedActivativeCore`, `ActivativeIntelligencePack`, `ConversationalActivationExpression`, `ActivativeCall`, `ReactionReceipt`, `ExpressionMoment`, `IdentityDNAAmendmentProposal`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-00`, `TS-11`, `TS-15`
- Test seam: Category/profile schema, rich-to-sparse lineage, sequencing, Reaction Receipt, Expression Moment, and HG-015 seams.
- Gate references: `BD-004`, `BD-007`, `BD-008`, `BD-010`, `BD-014`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject cross-category registry reuse, missing character-performance state, and format mappings that claim certification they have not earned.
- Observability evidence: `ST-06.02:OutcomeVerified`, `ST-06.02:OutcomeRejected`
- Required tests: `ST-06.02-acceptance`, `ST-06.02-failure`, `ST-06.02-authority`, `ST-06.02-receipt`
- Completion receipt: `ST-06.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve all five category IDs, four conversational profile IDs, Activation First runtime law, and Visual Syntax First development law.
- Fresh-context scope: One independently testable Compile Category-Local Format and Performance Profiles increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-06.02 are accepted and the covered authority is available,
- When the Category steward maps edited-video formats and Format 02 character-performance registries into their owning category profiles,
- Then each format inherits the correct substrate grammar rather than acting as a cosmetic theme
- And failure behavior is explicit: Reject cross-category registry reuse, missing character-performance state, and format mappings that claim certification they have not earned.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve all five category IDs, four conversational profile IDs, Activation First runtime law, and Visual Syntax First development law.

### ST-06.03 — Compile Category-Native Syntax and Activative Sequencing

As a **Category steward**, I want to **load category-specific syntax, temporal, conversational, and sequence parsers and compiles adapted Activative Sequencing Intelligence**, so that **shared Activative meaning becomes category-native form without losing frozen rich-object lineage**

- Global order: `27`
- Dependencies: `ST-06.02`
- Primary outcome: shared Activative meaning becomes category-native form without losing frozen rich-object lineage
- Primary obligations (6): `CONST-003`, `CONST-006`, `FR-145`, `FR-146`, `FR-147`, `NFR-CAT-003`
- Relevant FRs: `FR-145`, `FR-146`, `FR-147`
- Relevant NFRs: `NFR-CAT-003`
- Release 1 disposition: `RELEASE_1_FORMAT02_PRODUCTION_OTHER_CATEGORIES_STRUCTURAL_UNCERTIFIED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-11`, `constitutional_alignment_and_mapped_spec_owners`
- Component boundary: Five-category and conversational profile contract compilation; live Interview and ReelCast execution remain external.
- Affected contracts: `SharedActivativeCore`, `ActivativeIntelligencePack`, `ConversationalActivationExpression`, `ActivativeCall`, `ReactionReceipt`, `ExpressionMoment`, `IdentityDNAAmendmentProposal`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-00`, `TS-03`, `TS-05`, `TS-06`, `TS-07`, `TS-09`, `TS-11`, `TS-14`, `TS-15`
- Test seam: Category/profile schema, rich-to-sparse lineage, sequencing, Reaction Receipt, Expression Moment, and HG-015 seams.
- Gate references: `BD-004`, `BD-007`, `BD-008`, `BD-010`, `BD-014`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject generic parser output, sparse tokens without rich references, Activation First violations, and development parsing that invents runtime semantics.
- Observability evidence: `ST-06.03:OutcomeVerified`, `ST-06.03:OutcomeRejected`
- Required tests: `ST-06.03-acceptance`, `ST-06.03-failure`, `ST-06.03-authority`, `ST-06.03-receipt`
- Completion receipt: `ST-06.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve all five category IDs, four conversational profile IDs, Activation First runtime law, and Visual Syntax First development law.
- Fresh-context scope: One independently testable Compile Category-Native Syntax and Activative Sequencing increment covering 6 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-06.03 are accepted and the covered authority is available,
- When the Category steward loads category-specific syntax, temporal, conversational, and sequence parsers and compiles adapted Activative Sequencing Intelligence,
- Then shared Activative meaning becomes category-native form without losing frozen rich-object lineage
- And failure behavior is explicit: Reject generic parser output, sparse tokens without rich references, Activation First violations, and development parsing that invents runtime semantics.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve all five category IDs, four conversational profile IDs, Activation First runtime law, and Visual Syntax First development law.

### ST-06.04 — Own Category Runtime, Evaluation, Repair, and Migration Rules

As a **Category steward**, I want to **compile category-owned runtime, evaluator, repair, atomic ownership, and profile migration contracts**, so that **each category can evolve without silently changing another category or inheriting certification**

- Global order: `28`
- Dependencies: `ST-06.03`
- Primary outcome: each category can evolve without silently changing another category or inheriting certification
- Primary obligations (4): `FR-148`, `FR-149`, `FR-150`, `NFR-MAINT-003`
- Relevant FRs: `FR-148`, `FR-149`, `FR-150`
- Relevant NFRs: `NFR-MAINT-003`
- Release 1 disposition: `RELEASE_1_FORMAT02_PRODUCTION_OTHER_CATEGORIES_STRUCTURAL_UNCERTIFIED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-11`
- Component boundary: Five-category and conversational profile contract compilation; live Interview and ReelCast execution remain external.
- Affected contracts: `SharedActivativeCore`, `ActivativeIntelligencePack`, `ConversationalActivationExpression`, `ActivativeCall`, `ReactionReceipt`, `ExpressionMoment`, `IdentityDNAAmendmentProposal`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-11`
- Test seam: Category/profile schema, rich-to-sparse lineage, sequencing, Reaction Receipt, Expression Moment, and HG-015 seams.
- Gate references: `BD-004`, `BD-007`, `BD-008`, `BD-010`, `BD-014`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block incompatible profile migration, cross-category repair, missing evaluator ownership, and atomic creative ownership transfer.
- Observability evidence: `ST-06.04:OutcomeVerified`, `ST-06.04:OutcomeRejected`
- Required tests: `ST-06.04-acceptance`, `ST-06.04-failure`, `ST-06.04-authority`, `ST-06.04-receipt`
- Completion receipt: `ST-06.04:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve all five category IDs, four conversational profile IDs, Activation First runtime law, and Visual Syntax First development law.
- Fresh-context scope: One independently testable Own Category Runtime, Evaluation, Repair, and Migration Rules increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-06.04 are accepted and the covered authority is available,
- When the Category steward compiles category-owned runtime, evaluator, repair, atomic ownership, and profile migration contracts,
- Then each category can evolve without silently changing another category or inheriting certification
- And failure behavior is explicit: Block incompatible profile migration, cross-category repair, missing evaluator ownership, and atomic creative ownership transfer.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve all five category IDs, four conversational profile IDs, Activation First runtime law, and Visual Syntax First development law.

### ST-06.05 — Compile the Conversational Expression Feedback Chain

As a **Conversational category steward**, I want to **compile Activative Calls into Reaction Receipts, Expression Moments, post-expression recompilation, and final Content Type Contract handoffs**, so that **Public Comment, Reply or DM, ReelCast, and Interview profiles are first-class structural outputs while live execution stays external**

- Global order: `29`
- Dependencies: `ST-06.04`
- Primary outcome: Public Comment, Reply or DM, ReelCast, and Interview profiles are first-class structural outputs while live execution stays external
- Primary obligations (1): `CONST-004`
- Relevant FRs: None
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_FORMAT02_PRODUCTION_OTHER_CATEGORIES_STRUCTURAL_UNCERTIFIED`
- Release 1 role: `CONVERSATIONAL_STRUCTURAL_SUPPORT_UNCERTIFIED`
- Implementation owners: `constitutional_alignment_and_mapped_spec_owners`
- Component boundary: Five-category and conversational profile contract compilation; live Interview and ReelCast execution remain external.
- Affected contracts: `SharedActivativeCore`, `ActivativeIntelligencePack`, `ConversationalActivationExpression`, `ActivativeCall`, `ReactionReceipt`, `ExpressionMoment`, `IdentityDNAAmendmentProposal`
- Affected schemas: `docs/contracts/schemas/shared-activative-core.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-02`, `TS-06`, `TS-07`, `TS-10`, `TS-11`, `TS-12`, `TS-14`
- Test seam: Category/profile schema, rich-to-sparse lineage, sequencing, Reaction Receipt, Expression Moment, and HG-015 seams.
- Gate references: `BD-004`, `BD-008`, `BD-010`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block missing consent authority, scripted guest landings, Reaction Receipt or Expression Moment provenance loss, premature Identity DNA merge, and local Interview product invention.
- Observability evidence: `ST-06.05:OutcomeVerified`, `ST-06.05:OutcomeRejected`
- Required tests: `ST-06.05-acceptance`, `ST-06.05-failure`, `ST-06.05-authority`, `ST-06.05-receipt`
- Completion receipt: `ST-06.05:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve all five category IDs, four conversational profile IDs, Activation First runtime law, and Visual Syntax First development law.
- Fresh-context scope: One independently testable Compile the Conversational Expression Feedback Chain increment covering 1 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-06.05 are accepted and the covered authority is available,
- When the Conversational category steward compiles Activative Calls into Reaction Receipts, Expression Moments, post-expression recompilation, and final Content Type Contract handoffs,
- Then Public Comment, Reply or DM, ReelCast, and Interview profiles are first-class structural outputs while live execution stays external
- And failure behavior is explicit: Block missing consent authority, scripted guest landings, Reaction Receipt or Expression Moment provenance loss, premature Identity DNA merge, and local Interview product invention.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve all five category IDs, four conversational profile IDs, Activation First runtime law, and Visual Syntax First development law.


## EP-07 — Three-Target Product Compilation and Cross-Product Handoff

**Epic outcome:** A cross-product architect can compile distinct Atomic Content Harness, Visual Asset Editor, and Content Asset Delegation Contract profiles from shared governance while preserving target-specific evidence, ownership, artifacts, evaluation, compatibility, and frozen semantic handoffs.

**Story count:** 4

### ST-07.01 — Register Three Distinct Compilation Targets

As a **Cross-product architect**, I want to **register versioned Atomic Content Harness, Visual Asset Editor, and Content Asset Delegation Contract profiles**, so that **one control plane can select the correct product outcome without flattening ownership or evidence needs**

- Global order: `30`
- Dependencies: `ST-03.05`, `ST-04.05`, `ST-06.05`
- Primary outcome: one control plane can select the correct product outcome without flattening ownership or evidence needs
- Primary obligations (3): `ADR-013`, `D004`, `FR-170`
- Relevant FRs: `FR-170`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_THREE_TARGET_STRUCTURAL_FORMAT02_STUBBED_EXTERNAL_HANDOFF`
- Release 1 role: `THREE_TARGET_STRUCTURAL_SUPPORT_EXTERNAL_RUNTIME_EXCLUDED`
- Implementation owners: `Cross-product architecture`, `TS-11`, `product_constitution`
- Component boundary: Three Builder target compilers and frozen cross-product handoffs; VAE and Delegation runtimes remain external.
- Affected contracts: `TargetProfile`, `VisualSemanticAndNarrativeHandoff`, `TVRouteRequest`, `DelegationHandoff`, `AssetDemandSemanticLineage`
- Affected schemas: `docs/contracts/schemas/visual-semantic-handoff.schema.json`
- Primary specifications: `TS-01`, `TS-11`, `TS-15`
- Test seam: Target-profile separation, artifact-set completeness, lineage round-trip, compatibility, and external-port contract seams.
- Gate references: `BD-014`
- Implementation gate status: `EVIDENCE_GATED`
- Failure behavior: Reject unknown targets, multiple targets, universal-profile assumptions, and target records without required extensions or prohibitions.
- Observability evidence: `ST-07.01:OutcomeVerified`, `ST-07.01:OutcomeRejected`
- Required tests: `ST-07.01-acceptance`, `ST-07.01-failure`, `ST-07.01-authority`, `ST-07.01-receipt`
- Completion receipt: `ST-07.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version all three target profiles and require lossless migrations without universal-profile flattening.
- Fresh-context scope: One independently testable Register Three Distinct Compilation Targets increment covering 3 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-07.01 are accepted and the covered authority is available,
- When the Cross-product architect registers versioned Atomic Content Harness, Visual Asset Editor, and Content Asset Delegation Contract profiles,
- Then one control plane can select the correct product outcome without flattening ownership or evidence needs
- And failure behavior is explicit: Reject unknown targets, multiple targets, universal-profile assumptions, and target records without required extensions or prohibitions.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version all three target profiles and require lossless migrations without universal-profile flattening.

### ST-07.02 — Compile a Target-Specific Atomic Content Harness

As a **Harness Architect**, I want to **apply content-harness source, IR, Genesis, and category extensions to compile one atomic harness profile**, so that **content-harness output preserves Activative ownership and its category-native contracts**

- Global order: `31`
- Dependencies: `ST-07.01`
- Primary outcome: content-harness output preserves Activative ownership and its category-native contracts
- Primary obligations (4): `FR-171`, `FR-174`, `FR-175`, `FR-176`
- Relevant FRs: `FR-171`, `FR-174`, `FR-175`, `FR-176`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_THREE_TARGET_STRUCTURAL_FORMAT02_STUBBED_EXTERNAL_HANDOFF`
- Release 1 role: `THREE_TARGET_STRUCTURAL_SUPPORT_EXTERNAL_RUNTIME_EXCLUDED`
- Implementation owners: `TS-11`
- Component boundary: Three Builder target compilers and frozen cross-product handoffs; VAE and Delegation runtimes remain external.
- Affected contracts: `TargetProfile`, `VisualSemanticAndNarrativeHandoff`, `TVRouteRequest`, `DelegationHandoff`, `AssetDemandSemanticLineage`
- Affected schemas: `docs/contracts/schemas/visual-semantic-handoff.schema.json`
- Primary specifications: `TS-11`
- Test seam: Target-profile separation, artifact-set completeness, lineage round-trip, compatibility, and external-port contract seams.
- Gate references: `BD-014`
- Implementation gate status: `EVIDENCE_GATED`
- Failure behavior: Block missing category binding, borrowed VAE authority, incomplete source profile, or Genesis decisions copied from another target.
- Observability evidence: `ST-07.02:OutcomeVerified`, `ST-07.02:OutcomeRejected`
- Required tests: `ST-07.02-acceptance`, `ST-07.02-failure`, `ST-07.02-authority`, `ST-07.02-receipt`
- Completion receipt: `ST-07.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version all three target profiles and require lossless migrations without universal-profile flattening.
- Fresh-context scope: One independently testable Compile a Target-Specific Atomic Content Harness increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-07.02 are accepted and the covered authority is available,
- When the Harness Architect applies content-harness source, IR, Genesis, and category extensions to compile one atomic harness profile,
- Then content-harness output preserves Activative ownership and its category-native contracts
- And failure behavior is explicit: Block missing category binding, borrowed VAE authority, incomplete source profile, or Genesis decisions copied from another target.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version all three target profiles and require lossless migrations without universal-profile flattening.

### ST-07.03 — Compile VAE and Delegation Handoffs Without Implementing Them

As a **Cross-product architect**, I want to **compile VAE and Delegation target profiles plus visual-semantic, Composition Asset Pack, T or V route, and Asset Demand handoffs**, so that **external products receive frozen, typed meaning while Builder stays within compile-validate-handoff ownership**

- Global order: `32`
- Dependencies: `ST-07.02`
- Primary outcome: external products receive frozen, typed meaning while Builder stays within compile-validate-handoff ownership
- Primary obligations (4): `ADR-018`, `CONST-005`, `FR-172`, `FR-173`
- Relevant FRs: `FR-172`, `FR-173`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_THREE_TARGET_STRUCTURAL_FORMAT02_STUBBED_EXTERNAL_HANDOFF`
- Release 1 role: `THREE_TARGET_STRUCTURAL_SUPPORT_EXTERNAL_RUNTIME_EXCLUDED`
- Implementation owners: `Product lead and cross-product architecture`, `TS-11`, `constitutional_alignment_and_mapped_spec_owners`
- Component boundary: Three Builder target compilers and frozen cross-product handoffs; VAE and Delegation runtimes remain external.
- Affected contracts: `TargetProfile`, `VisualSemanticAndNarrativeHandoff`, `TVRouteRequest`, `DelegationHandoff`, `AssetDemandSemanticLineage`
- Affected schemas: `docs/contracts/schemas/visual-semantic-handoff.schema.json`
- Primary specifications: `TS-03`, `TS-06`, `TS-07`, `TS-10`, `TS-11`, `TS-13`, `TS-14`, `TS-15`
- Test seam: Target-profile separation, artifact-set completeness, lineage round-trip, compatibility, and external-port contract seams.
- Gate references: `BD-007`, `BD-008`, `BD-014`
- Implementation gate status: `EVIDENCE_GATED`
- Failure behavior: Block semantic mutation, local external-runtime behavior, incompatible Delegation fields, missing lineage, and unstubbed Release 1 production dependencies.
- Observability evidence: `ST-07.03:OutcomeVerified`, `ST-07.03:OutcomeRejected`
- Required tests: `ST-07.03-acceptance`, `ST-07.03-failure`, `ST-07.03-authority`, `ST-07.03-receipt`
- Completion receipt: `ST-07.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version all three target profiles and require lossless migrations without universal-profile flattening.
- Fresh-context scope: One independently testable Compile VAE and Delegation Handoffs Without Implementing Them increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-07.03 are accepted and the covered authority is available,
- When the Cross-product architect compiles VAE and Delegation target profiles plus visual-semantic, Composition Asset Pack, T or V route, and Asset Demand handoffs,
- Then external products receive frozen, typed meaning while Builder stays within compile-validate-handoff ownership
- And failure behavior is explicit: Block semantic mutation, local external-runtime behavior, incompatible Delegation fields, missing lineage, and unstubbed Release 1 production dependencies.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version all three target profiles and require lossless migrations without universal-profile flattening.

### ST-07.04 — Validate Target Artifacts, Gates, and Compatibility

As a **Cross-product reviewer**, I want to **compile target artifact sets and applies target-specific evaluation, authorization, non-flattening, and compatibility checks**, so that **each target can be reviewed and migrated independently with explicit certification scope**

- Global order: `33`
- Dependencies: `ST-07.03`
- Primary outcome: each target can be reviewed and migrated independently with explicit certification scope
- Primary obligations (4): `FR-177`, `FR-178`, `FR-179`, `FR-180`
- Relevant FRs: `FR-177`, `FR-178`, `FR-179`, `FR-180`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_THREE_TARGET_STRUCTURAL_FORMAT02_STUBBED_EXTERNAL_HANDOFF`
- Release 1 role: `THREE_TARGET_STRUCTURAL_SUPPORT_EXTERNAL_RUNTIME_EXCLUDED`
- Implementation owners: `TS-11`
- Component boundary: Three Builder target compilers and frozen cross-product handoffs; VAE and Delegation runtimes remain external.
- Affected contracts: `TargetProfile`, `VisualSemanticAndNarrativeHandoff`, `TVRouteRequest`, `DelegationHandoff`, `AssetDemandSemanticLineage`
- Affected schemas: `docs/contracts/schemas/visual-semantic-handoff.schema.json`
- Primary specifications: `TS-11`
- Test seam: Target-profile separation, artifact-set completeness, lineage round-trip, compatibility, and external-port contract seams.
- Gate references: `BD-014`
- Implementation gate status: `EVIDENCE_GATED`
- Failure behavior: Reject missing artifacts, cross-target field leakage, lossy migrations, unpinned external contracts, and certification inherited from another target.
- Observability evidence: `ST-07.04:OutcomeVerified`, `ST-07.04:OutcomeRejected`
- Required tests: `ST-07.04-acceptance`, `ST-07.04-failure`, `ST-07.04-authority`, `ST-07.04-receipt`
- Completion receipt: `ST-07.04:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version all three target profiles and require lossless migrations without universal-profile flattening.
- Fresh-context scope: One independently testable Validate Target Artifacts, Gates, and Compatibility increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-07.04 are accepted and the covered authority is available,
- When the Cross-product reviewer compiles target artifact sets and applies target-specific evaluation, authorization, non-flattening, and compatibility checks,
- Then each target can be reviewed and migrated independently with explicit certification scope
- And failure behavior is explicit: Reject missing artifacts, cross-target field leakage, lossy migrations, unpinned external contracts, and certification inherited from another target.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version all three target profiles and require lossless migrations without universal-profile flattening.


## EP-08 — Behavioral Proof, Repair, and Readiness Authorization

**Epic outcome:** Independent reviewers can measure whether the Builder, its skills, categories, profiles, and target artifacts improve behavior, reject wrong readings, repair only responsible layers, and issue immutable readiness or blocked authorization receipts.

**Story count:** 7

### ST-08.01 — Measure Behavior Against Controls in Fresh Contexts

As a **Independent evaluator**, I want to **evaluate every skill-system layer with no-guidance controls, repeated fresh-context trials, and adversarial cases**, so that **claimed behavioral improvements are attributable rather than prompt-history artifacts**

- Global order: `34`
- Dependencies: `ST-02.05`, `ST-03.05`, `ST-04.05`, `ST-05.05`, `ST-06.05`, `ST-07.04`
- Primary outcome: claimed behavioral improvements are attributable rather than prompt-history artifacts
- Primary obligations (6): `FR-103`, `FR-104`, `FR-105`, `FR-106`, `NFR-EVAL-002`, `NFR-EVAL-003`
- Relevant FRs: `FR-103`, `FR-104`, `FR-105`, `FR-106`
- Relevant NFRs: `NFR-EVAL-002`, `NFR-EVAL-003`
- Release 1 disposition: `RELEASE_1_INCLUDED_CERTIFICATION_BLOCKED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-10`
- Component boundary: Independent behavioral evaluation, selective repair, and authorization receipts; thresholds remain human-governed.
- Affected contracts: `EvaluationCase`, `ConstitutionalEvaluationReceipt`, `ConstitutionalReadinessReceipt`, `RepairReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-10`
- Test seam: Protected benchmark, fresh-context, mutation, wrong-reading, repair, regression, and readiness decision seams.
- Gate references: `BD-004`, `BD-008`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject non-independent evaluation, missing controls, reused generator context, insufficient repetitions, and cases without protected expected behavior.
- Observability evidence: `ST-08.01:OutcomeVerified`, `ST-08.01:OutcomeRejected`
- Required tests: `ST-08.01-acceptance`, `ST-08.01-failure`, `ST-08.01-authority`, `ST-08.01-receipt`
- Completion receipt: `ST-08.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.
- Fresh-context scope: One independently testable Measure Behavior Against Controls in Fresh Contexts increment covering 6 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-08.01 are accepted and the covered authority is available,
- When the Independent evaluator evaluates every skill-system layer with no-guidance controls, repeated fresh-context trials, and adversarial cases,
- Then claimed behavioral improvements are attributable rather than prompt-history artifacts
- And failure behavior is explicit: Reject non-independent evaluation, missing controls, reused generator context, insufficient repetitions, and cases without protected expected behavior.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.

### ST-08.02 — Promote Maturity Only Through Protected Receipts

As a **Evaluation steward**, I want to **verify artifact identity and stores staged benchmark, corpus, and maturity receipts**, so that **only the exact evaluated version can advance toward release**

- Global order: `35`
- Dependencies: `ST-08.01`
- Primary outcome: only the exact evaluated version can advance toward release
- Primary obligations (9): `ADR-010`, `D022`, `D023`, `FR-107`, `FR-108`, `FR-109`, `FR-110`, `NFR-EVAL-001`, `NFR-TRACE-003`
- Relevant FRs: `FR-107`, `FR-108`, `FR-109`, `FR-110`
- Relevant NFRs: `NFR-EVAL-001`, `NFR-TRACE-003`
- Release 1 disposition: `RELEASE_1_INCLUDED_CERTIFICATION_BLOCKED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `Evaluation governance and architecture`, `TS-10`, `product_constitution`
- Component boundary: Independent behavioral evaluation, selective repair, and authorization receipts; thresholds remain human-governed.
- Affected contracts: `EvaluationCase`, `ConstitutionalEvaluationReceipt`, `ConstitutionalReadinessReceipt`, `RepairReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `IMPLEMENTATION_BASELINE`, `TS-02`, `TS-03`, `TS-08`, `TS-10`, `TS-13`, `TS-14`, `TS-15`
- Test seam: Protected benchmark, fresh-context, mutation, wrong-reading, repair, regression, and readiness decision seams.
- Gate references: `BD-004`, `BD-007`, `BD-008`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block benchmark leakage, artifact hash mismatch, unprotected release cases, missing source authority, and maturity promotion without complete receipts.
- Observability evidence: `ST-08.02:OutcomeVerified`, `ST-08.02:OutcomeRejected`
- Required tests: `ST-08.02-acceptance`, `ST-08.02-failure`, `ST-08.02-authority`, `ST-08.02-receipt`
- Completion receipt: `ST-08.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.
- Fresh-context scope: One independently testable Promote Maturity Only Through Protected Receipts increment covering 9 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-08.02 are accepted and the covered authority is available,
- When the Evaluation steward verifies artifact identity and stores staged benchmark, corpus, and maturity receipts,
- Then only the exact evaluated version can advance toward release
- And failure behavior is explicit: Block benchmark leakage, artifact hash mismatch, unprotected release cases, missing source authority, and maturity promotion without complete receipts.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.

### ST-08.03 — Score Independent Dimensions and Controlled Mutations

As a **Independent evaluator**, I want to **run controlled mutations, category-appropriate scorecards, stability analysis, and downstream result ingestion**, so that **quality dimensions remain visible and non-compensable rather than collapsing into one flattering score**

- Global order: `36`
- Dependencies: `ST-08.02`
- Primary outcome: quality dimensions remain visible and non-compensable rather than collapsing into one flattering score
- Primary obligations (9): `D024`, `FR-111`, `FR-112`, `FR-113`, `FR-114`, `FR-115`, `FR-116`, `HG-008`, `NFR-EVAL-004`
- Relevant FRs: `FR-111`, `FR-112`, `FR-113`, `FR-114`, `FR-115`, `FR-116`
- Relevant NFRs: `NFR-EVAL-004`
- Release 1 disposition: `RELEASE_1_INCLUDED_CERTIFICATION_BLOCKED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-10`, `evaluation_governance`, `product_constitution`
- Component boundary: Independent behavioral evaluation, selective repair, and authorization receipts; thresholds remain human-governed.
- Affected contracts: `EvaluationCase`, `ConstitutionalEvaluationReceipt`, `ConstitutionalReadinessReceipt`, `RepairReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-10`, `TS-11`, `TS-12`, `TS-14`
- Test seam: Protected benchmark, fresh-context, mutation, wrong-reading, repair, regression, and readiness decision seams.
- Gate references: `BD-004`, `BD-008`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject leaked cases, category-inappropriate rubrics, hidden minimum failures, unstable repeated results, and downstream evidence without identity.
- Observability evidence: `ST-08.03:OutcomeVerified`, `ST-08.03:OutcomeRejected`
- Required tests: `ST-08.03-acceptance`, `ST-08.03-failure`, `ST-08.03-authority`, `ST-08.03-receipt`
- Completion receipt: `ST-08.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.
- Fresh-context scope: One independently testable Score Independent Dimensions and Controlled Mutations increment covering 9 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-08.03 are accepted and the covered authority is available,
- When the Independent evaluator runs controlled mutations, category-appropriate scorecards, stability analysis, and downstream result ingestion,
- Then quality dimensions remain visible and non-compensable rather than collapsing into one flattering score
- And failure behavior is explicit: Reject leaked cases, category-inappropriate rubrics, hidden minimum failures, unstable repeated results, and downstream evidence without identity.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.

### ST-08.04 — Diagnose Root Cause Before Selecting Repair

As a **Repair reviewer**, I want to **classify failure and compiles a repair and invalidation graph from root-cause evidence**, so that **repair targets the responsible layer and preserves unaffected upstream truth**

- Global order: `37`
- Dependencies: `ST-08.03`
- Primary outcome: repair targets the responsible layer and preserves unaffected upstream truth
- Primary obligations (5): `AG-014`, `D026`, `FR-127`, `FR-128`, `FR-129`
- Relevant FRs: `FR-127`, `FR-128`, `FR-129`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED_CERTIFICATION_BLOCKED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-13`, `product_constitution`
- Component boundary: Independent behavioral evaluation, selective repair, and authorization receipts; thresholds remain human-governed.
- Affected contracts: `EvaluationCase`, `ConstitutionalEvaluationReceipt`, `ConstitutionalReadinessReceipt`, `RepairReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-00`, `TS-05`, `TS-07`, `TS-10`, `TS-11`, `TS-12`, `TS-13`, `TS-14`
- Test seam: Protected benchmark, fresh-context, mutation, wrong-reading, repair, regression, and readiness decision seams.
- Gate references: `BD-004`, `BD-008`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject repair-by-symptom, cross-layer mutation, missing failure evidence, and invalidation scopes broader than the demonstrated cause.
- Observability evidence: `ST-08.04:OutcomeVerified`, `ST-08.04:OutcomeRejected`
- Required tests: `ST-08.04-acceptance`, `ST-08.04-failure`, `ST-08.04-authority`, `ST-08.04-receipt`
- Completion receipt: `ST-08.04:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.
- Fresh-context scope: One independently testable Diagnose Root Cause Before Selecting Repair increment covering 5 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-08.04 are accepted and the covered authority is available,
- When the Repair reviewer classifies failure and compiles a repair and invalidation graph from root-cause evidence,
- Then repair targets the responsible layer and preserves unaffected upstream truth
- And failure behavior is explicit: Reject repair-by-symptom, cross-layer mutation, missing failure evidence, and invalidation scopes broader than the demonstrated cause.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.

### ST-08.05 — Repair Selectively and Rerun Only Affected Regressions

As a **Repair operator**, I want to **apply bounded repair, preserves unaffected state, reruns targeted regressions, and escalates repeated constitutional failures**, so that **the system can improve without restarting validated work or hiding recurring defects**

- Global order: `38`
- Dependencies: `ST-08.04`
- Primary outcome: the system can improve without restarting validated work or hiding recurring defects
- Primary obligations (3): `FR-130`, `FR-131`, `FR-132`
- Relevant FRs: `FR-130`, `FR-131`, `FR-132`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED_CERTIFICATION_BLOCKED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-13`
- Component boundary: Independent behavioral evaluation, selective repair, and authorization receipts; thresholds remain human-governed.
- Affected contracts: `EvaluationCase`, `ConstitutionalEvaluationReceipt`, `ConstitutionalReadinessReceipt`, `RepairReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-13`
- Test seam: Protected benchmark, fresh-context, mutation, wrong-reading, repair, regression, and readiness decision seams.
- Gate references: `BD-008`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block repairs that skip regression, change protected upstream state, exceed retry limits, or suppress escalation after repeated failure.
- Observability evidence: `ST-08.05:OutcomeVerified`, `ST-08.05:OutcomeRejected`
- Required tests: `ST-08.05-acceptance`, `ST-08.05-failure`, `ST-08.05-authority`, `ST-08.05-receipt`
- Completion receipt: `ST-08.05:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.
- Fresh-context scope: One independently testable Repair Selectively and Rerun Only Affected Regressions increment covering 3 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-08.05 are accepted and the covered authority is available,
- When the Repair operator applies bounded repair, preserves unaffected state, reruns targeted regressions, and escalates repeated constitutional failures,
- Then the system can improve without restarting validated work or hiding recurring defects
- And failure behavior is explicit: Block repairs that skip regression, change protected upstream state, exceed retry limits, or suppress escalation after repeated failure.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.

### ST-08.06 — Issue Evidence-Backed Readiness and Authorization Receipts

As a **Product authority**, I want to **evaluate hard gates and issues full, prototype-only, or blocked authorization with immutable receipts**, so that **implementation teams know exactly what is authorized and why**

- Global order: `39`
- Dependencies: `ST-08.05`
- Primary outcome: implementation teams know exactly what is authorized and why
- Primary obligations (10): `AG-015`, `AG-022`, `D027`, `D033`, `FR-133`, `FR-134`, `FR-135`, `FR-136`, `HG-009`, `HG-010`
- Relevant FRs: `FR-133`, `FR-134`, `FR-135`, `FR-136`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED_CERTIFICATION_BLOCKED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-13`, `evaluation_governance`, `product_constitution`
- Component boundary: Independent behavioral evaluation, selective repair, and authorization receipts; thresholds remain human-governed.
- Affected contracts: `EvaluationCase`, `ConstitutionalEvaluationReceipt`, `ConstitutionalReadinessReceipt`, `RepairReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-00`, `TS-01`, `TS-02`, `TS-04`, `TS-05`, `TS-06`, `TS-07`, `TS-08`, `TS-09`, `TS-10`, `TS-11`, `TS-12`, `TS-13`, `TS-14`, `TS-15`
- Test seam: Protected benchmark, fresh-context, mutation, wrong-reading, repair, regression, and readiness decision seams.
- Gate references: `BD-004`, `BD-008`, `BD-014`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject false readiness from document completeness, anti-goal violations, missing thresholds, unresolved blockers, and authority outcomes without evidence.
- Observability evidence: `ST-08.06:OutcomeVerified`, `ST-08.06:OutcomeRejected`
- Required tests: `ST-08.06-acceptance`, `ST-08.06-failure`, `ST-08.06-authority`, `ST-08.06-receipt`
- Completion receipt: `ST-08.06:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.
- Fresh-context scope: One independently testable Issue Evidence-Backed Readiness and Authorization Receipts increment covering 10 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-08.06 are accepted and the covered authority is available,
- When the Product authority evaluates hard gates and issues full, prototype-only, or blocked authorization with immutable receipts,
- Then implementation teams know exactly what is authorized and why
- And failure behavior is explicit: Reject false readiness from document completeness, anti-goal violations, missing thresholds, unresolved blockers, and authority outcomes without evidence.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.

### ST-08.07 — Reject Wrong Readings and Evaluate Conversational Expression

As a **Conversational evaluation steward**, I want to **test dominant wrong-reading locks and the constitutional conversational dimensions across protected cases**, so that **role clarity, pattern interruption, prediction, payoff, affinity, anticipation, residue, anti-cliche, no-text survival, and rejection remain independently governed**

- Global order: `40`
- Dependencies: `ST-08.06`
- Primary outcome: role clarity, pattern interruption, prediction, payoff, affinity, anticipation, residue, anti-cliche, no-text survival, and rejection remain independently governed
- Primary obligations (2): `CONST-007`, `CONST-008`
- Relevant FRs: None
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED_CERTIFICATION_BLOCKED`
- Release 1 role: `CONVERSATIONAL_STRUCTURAL_SUPPORT_UNCERTIFIED`
- Implementation owners: `constitutional_alignment_and_mapped_spec_owners`
- Component boundary: Independent behavioral evaluation, selective repair, and authorization receipts; thresholds remain human-governed.
- Affected contracts: `EvaluationCase`, `ConstitutionalEvaluationReceipt`, `ConstitutionalReadinessReceipt`, `RepairReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`, `docs/contracts/schemas/conversational-expression.schema.json`
- Primary specifications: `TS-03`, `TS-06`, `TS-10`, `TS-11`, `TS-12`, `TS-13`, `TS-15`
- Test seam: Protected benchmark, fresh-context, mutation, wrong-reading, repair, regression, and readiness decision seams.
- Gate references: `BD-008`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block conversational certification while HD-007 thresholds or HD-006 evidence governance remain open, or when one dimension compensates for a hard failure.
- Observability evidence: `ST-08.07:OutcomeVerified`, `ST-08.07:OutcomeRejected`
- Required tests: `ST-08.07-acceptance`, `ST-08.07-failure`, `ST-08.07-authority`, `ST-08.07-receipt`
- Completion receipt: `ST-08.07:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.
- Fresh-context scope: One independently testable Reject Wrong Readings and Evaluate Conversational Expression increment covering 2 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-08.07 are accepted and the covered authority is available,
- When the Conversational evaluation steward tests dominant wrong-reading locks and the constitutional conversational dimensions across protected cases,
- Then role clarity, pattern interruption, prediction, payoff, affinity, anticipation, residue, anti-cliche, no-text survival, and rejection remain independently governed
- And failure behavior is explicit: Block conversational certification while HD-007 thresholds or HD-006 evidence governance remain open, or when one dimension compensates for a hard failure.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.


## EP-09 — Governed Builder Workflow Factory

**Epic outcome:** An operator can route a Builder request through a versioned, actor-explicit workflow; run deterministic and agent work at isolated public seams; recover from bounded failures; and promote only workflows that pass end-to-end and fault tests.

**Story count:** 8

### ST-09.01 — Compile an Actor-Explicit Builder Workflow

As a **Workflow architect**, I want to **compile approved product graphs into versioned Workflow IR nodes, conditions, actors, and profiles**, so that **every request has reproducible routing and explicit responsibility**

- Global order: `41`
- Dependencies: `ST-01.04`, `ST-03.05`, `ST-04.05`, `ST-05.05`, `ST-06.05`, `ST-07.04`, `ST-08.07`
- Primary outcome: every request has reproducible routing and explicit responsibility
- Primary obligations (9): `ADR-006`, `FR-181`, `FR-182`, `FR-183`, `FR-184`, `FR-185`, `NFR-WORKFLOW-001`, `NFR-WORKFLOW-002`, `NFR-WORKFLOW-003`
- Relevant FRs: `FR-181`, `FR-182`, `FR-183`, `FR-184`, `FR-185`
- Relevant NFRs: `NFR-WORKFLOW-001`, `NFR-WORKFLOW-002`, `NFR-WORKFLOW-003`
- Release 1 disposition: `RELEASE_1_INCLUDED_MANUAL_SHADOW_BEFORE_AUTOMATION`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-14`, `Workflow architecture and operations`
- Component boundary: Builder workflow routing and execution control plane; no monolithic skill-owned or external product workflow.
- Affected contracts: `WorkflowIR`, `WorkflowNodeContract`, `CheckpointReceipt`, `PromotionReceipt`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-14`
- Test seam: Manual-shadow parity, node contract, isolation, retry, resume, fault-injection, promotion, and rollback seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Reject missing actors, ambiguous node ownership, graph cycles, undeclared handoffs, and workflow definitions not derived from approved product graphs.
- Observability evidence: `ST-09.01:OutcomeVerified`, `ST-09.01:OutcomeRejected`
- Required tests: `ST-09.01-acceptance`, `ST-09.01-failure`, `ST-09.01-authority`, `ST-09.01-receipt`
- Completion receipt: `ST-09.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version workflow profiles and adapters; require migration and rollback evidence before promotion.
- Fresh-context scope: One independently testable Compile an Actor-Explicit Builder Workflow increment covering 9 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-09.01 are accepted and the covered authority is available,
- When the Workflow architect compiles approved product graphs into versioned Workflow IR nodes, conditions, actors, and profiles,
- Then every request has reproducible routing and explicit responsibility
- And failure behavior is explicit: Reject missing actors, ambiguous node ownership, graph cycles, undeclared handoffs, and workflow definitions not derived from approved product graphs.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version workflow profiles and adapters; require migration and rollback evidence before promotion.

### ST-09.02 — Route Through a Manual Shadow Before Automation

As a **Builder operator**, I want to **route a request through the selected profile and proves manual-shadow parity before agent automation**, so that **automation begins from observed expert behavior and evaluated phase-local capsules**

- Global order: `42`
- Dependencies: `ST-09.01`
- Primary outcome: automation begins from observed expert behavior and evaluated phase-local capsules
- Primary obligations (5): `FR-186`, `FR-187`, `FR-188`, `FR-189`, `NFR-PORT-002`
- Relevant FRs: `FR-186`, `FR-187`, `FR-188`, `FR-189`
- Relevant NFRs: `NFR-PORT-002`
- Release 1 disposition: `RELEASE_1_INCLUDED_MANUAL_SHADOW_BEFORE_AUTOMATION`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-14`
- Component boundary: Builder workflow routing and execution control plane; no monolithic skill-owned or external product workflow.
- Affected contracts: `WorkflowIR`, `WorkflowNodeContract`, `CheckpointReceipt`, `PromotionReceipt`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-14`
- Test seam: Manual-shadow parity, node contract, isolation, retry, resume, fault-injection, promotion, and rollback seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Block unmatched profiles, missing manual shadow evidence, agent execution outside evaluated capsules, and deterministic work delegated to an agent.
- Observability evidence: `ST-09.02:OutcomeVerified`, `ST-09.02:OutcomeRejected`
- Required tests: `ST-09.02-acceptance`, `ST-09.02-failure`, `ST-09.02-authority`, `ST-09.02-receipt`
- Completion receipt: `ST-09.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version workflow profiles and adapters; require migration and rollback evidence before promotion.
- Fresh-context scope: One independently testable Route Through a Manual Shadow Before Automation increment covering 5 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-09.02 are accepted and the covered authority is available,
- When the Builder operator routes a request through the selected profile and proves manual-shadow parity before agent automation,
- Then automation begins from observed expert behavior and evaluated phase-local capsules
- And failure behavior is explicit: Block unmatched profiles, missing manual shadow evidence, agent execution outside evaluated capsules, and deterministic work delegated to an agent.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version workflow profiles and adapters; require migration and rollback evidence before promotion.

### ST-09.03 — Validate Node Outputs and Contain Failure Feedback

As a **Workflow operator**, I want to **validate each node and returns structured failure context only to the responsible node under bounded control flow**, so that **failures stay local, diagnosable, and unable to leak invalid output downstream**

- Global order: `43`
- Dependencies: `ST-09.02`
- Primary outcome: failures stay local, diagnosable, and unable to leak invalid output downstream
- Primary obligations (9): `AG-020`, `FR-190`, `FR-191`, `FR-192`, `FR-193`, `HG-012`, `HG-013`, `NFR-REL-004`, `NFR-WORKFLOW-004`
- Relevant FRs: `FR-190`, `FR-191`, `FR-192`, `FR-193`
- Relevant NFRs: `NFR-REL-004`, `NFR-WORKFLOW-004`
- Release 1 disposition: `RELEASE_1_INCLUDED_MANUAL_SHADOW_BEFORE_AUTOMATION`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-14`, `evaluation_governance`, `product_constitution`
- Component boundary: Builder workflow routing and execution control plane; no monolithic skill-owned or external product workflow.
- Affected contracts: `WorkflowIR`, `WorkflowNodeContract`, `CheckpointReceipt`, `PromotionReceipt`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-00`, `TS-14`
- Test seam: Manual-shadow parity, node contract, isolation, retry, resume, fault-injection, promotion, and rollback seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Reject unvalidated release, unbounded retries, broad conversational feedback, repair without root cause, and output emitted after a circuit breaker opens.
- Observability evidence: `ST-09.03:OutcomeVerified`, `ST-09.03:OutcomeRejected`
- Required tests: `ST-09.03-acceptance`, `ST-09.03-failure`, `ST-09.03-authority`, `ST-09.03-receipt`
- Completion receipt: `ST-09.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version workflow profiles and adapters; require migration and rollback evidence before promotion.
- Fresh-context scope: One independently testable Validate Node Outputs and Contain Failure Feedback increment covering 9 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-09.03 are accepted and the covered authority is available,
- When the Workflow operator validates each node and returns structured failure context only to the responsible node under bounded control flow,
- Then failures stay local, diagnosable, and unable to leak invalid output downstream
- And failure behavior is explicit: Reject unvalidated release, unbounded retries, broad conversational feedback, repair without root cause, and output emitted after a circuit breaker opens.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version workflow profiles and adapters; require migration and rollback evidence before promotion.

### ST-09.04 — Checkpoint, Isolate, and Resume Work Safely

As a **Workflow operator**, I want to **checkpoint idempotently, isolates tasks and secrets, grants least privilege, and parallelizes only independent work**, so that **the workflow can resume after failure without duplicating side effects or widening access**

- Global order: `44`
- Dependencies: `ST-09.03`
- Primary outcome: the workflow can resume after failure without duplicating side effects or widening access
- Primary obligations (12): `ADR-012`, `AG-021`, `FR-194`, `FR-195`, `FR-196`, `FR-197`, `NFR-PERF-004`, `NFR-SEC-004`, `NFR-WORKFLOW-005`, `NFR-WORKFLOW-006`, `NFR-WORKFLOW-007`, `NFR-WORKFLOW-008`
- Relevant FRs: `FR-194`, `FR-195`, `FR-196`, `FR-197`
- Relevant NFRs: `NFR-PERF-004`, `NFR-SEC-004`, `NFR-WORKFLOW-005`, `NFR-WORKFLOW-006`, `NFR-WORKFLOW-007`, `NFR-WORKFLOW-008`
- Release 1 disposition: `RELEASE_1_INCLUDED_MANUAL_SHADOW_BEFORE_AUTOMATION`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `Security and workflow architecture`, `TS-14`, `product_constitution`
- Component boundary: Builder workflow routing and execution control plane; no monolithic skill-owned or external product workflow.
- Affected contracts: `WorkflowIR`, `WorkflowNodeContract`, `CheckpointReceipt`, `PromotionReceipt`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-00`, `TS-02`, `TS-03`, `TS-14`
- Test seam: Manual-shadow parity, node contract, isolation, retry, resume, fault-injection, promotion, and rollback seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Block unsafe sandbox access, duplicate replay, shared secret leakage, dependency-unsafe parallelism, and recovery that corrupts protected state.
- Observability evidence: `ST-09.04:OutcomeVerified`, `ST-09.04:OutcomeRejected`
- Required tests: `ST-09.04-acceptance`, `ST-09.04-failure`, `ST-09.04-authority`, `ST-09.04-receipt`
- Completion receipt: `ST-09.04:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version workflow profiles and adapters; require migration and rollback evidence before promotion.
- Fresh-context scope: One independently testable Checkpoint, Isolate, and Resume Work Safely increment covering 12 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-09.04 are accepted and the covered authority is available,
- When the Workflow operator checkpoints idempotently, isolates tasks and secrets, grants least privilege, and parallelizes only independent work,
- Then the workflow can resume after failure without duplicating side effects or widening access
- And failure behavior is explicit: Block unsafe sandbox access, duplicate replay, shared secret leakage, dependency-unsafe parallelism, and recovery that corrupts protected state.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version workflow profiles and adapters; require migration and rollback evidence before promotion.

### ST-09.05 — Race Candidates and Route Compute Under Human Authority

As a **Workflow operator**, I want to **use quality-gated candidate races, risk-aware model routing, independent evaluators, and authority-placed human gates**, so that **compute is spent proportionally while consequential decisions stay human-governed**

- Global order: `45`
- Dependencies: `ST-09.04`
- Primary outcome: compute is spent proportionally while consequential decisions stay human-governed
- Primary obligations (6): `AG-011`, `FR-198`, `FR-199`, `FR-200`, `FR-201`, `NFR-WORKFLOW-009`
- Relevant FRs: `FR-198`, `FR-199`, `FR-200`, `FR-201`
- Relevant NFRs: `NFR-WORKFLOW-009`
- Release 1 disposition: `RELEASE_1_INCLUDED_MANUAL_SHADOW_BEFORE_AUTOMATION`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-14`, `product_constitution`
- Component boundary: Builder workflow routing and execution control plane; no monolithic skill-owned or external product workflow.
- Affected contracts: `WorkflowIR`, `WorkflowNodeContract`, `CheckpointReceipt`, `PromotionReceipt`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-00`, `TS-07`, `TS-14`
- Test seam: Manual-shadow parity, node contract, isolation, retry, resume, fault-injection, promotion, and rollback seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Reject winner selection before evaluation, generator-context evaluators, risk-blind model routing, or automation that removes required human gates.
- Observability evidence: `ST-09.05:OutcomeVerified`, `ST-09.05:OutcomeRejected`
- Required tests: `ST-09.05-acceptance`, `ST-09.05-failure`, `ST-09.05-authority`, `ST-09.05-receipt`
- Completion receipt: `ST-09.05:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version workflow profiles and adapters; require migration and rollback evidence before promotion.
- Fresh-context scope: One independently testable Race Candidates and Route Compute Under Human Authority increment covering 6 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-09.05 are accepted and the covered authority is available,
- When the Workflow operator uses quality-gated candidate races, risk-aware model routing, independent evaluators, and authority-placed human gates,
- Then compute is spent proportionally while consequential decisions stay human-governed
- And failure behavior is explicit: Reject winner selection before evaluation, generator-context evaluators, risk-blind model routing, or automation that removes required human gates.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version workflow profiles and adapters; require migration and rollback evidence before promotion.

### ST-09.06 — Observe Queues and Prove Workflow Recovery

As a **Workflow maintainer**, I want to **expose queues and node telemetry and runs end-to-end plus fault-injection recovery tests**, so that **operators can see cost, latency, quality, interventions, and recovery behavior at public seams**

- Global order: `46`
- Dependencies: `ST-09.05`
- Primary outcome: operators can see cost, latency, quality, interventions, and recovery behavior at public seams
- Primary obligations (9): `FR-202`, `FR-203`, `FR-204`, `FR-205`, `NFR-PERF-002`, `NFR-PERF-003`, `NFR-TEST-001`, `NFR-WORKFLOW-010`, `NFR-WORKFLOW-011`
- Relevant FRs: `FR-202`, `FR-203`, `FR-204`, `FR-205`
- Relevant NFRs: `NFR-PERF-002`, `NFR-PERF-003`, `NFR-TEST-001`, `NFR-WORKFLOW-010`, `NFR-WORKFLOW-011`
- Release 1 disposition: `RELEASE_1_INCLUDED_MANUAL_SHADOW_BEFORE_AUTOMATION`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-14`
- Component boundary: Builder workflow routing and execution control plane; no monolithic skill-owned or external product workflow.
- Affected contracts: `WorkflowIR`, `WorkflowNodeContract`, `CheckpointReceipt`, `PromotionReceipt`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-14`
- Test seam: Manual-shadow parity, node contract, isolation, retry, resume, fault-injection, promotion, and rollback seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Block hidden budget overflow, missing telemetry, untested failure modes, private-seam-only tests, and recovery claims without fault evidence.
- Observability evidence: `ST-09.06:OutcomeVerified`, `ST-09.06:OutcomeRejected`
- Required tests: `ST-09.06-acceptance`, `ST-09.06-failure`, `ST-09.06-authority`, `ST-09.06-receipt`
- Completion receipt: `ST-09.06:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version workflow profiles and adapters; require migration and rollback evidence before promotion.
- Fresh-context scope: One independently testable Observe Queues and Prove Workflow Recovery increment covering 9 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-09.06 are accepted and the covered authority is available,
- When the Workflow maintainer exposes queues and node telemetry and runs end-to-end plus fault-injection recovery tests,
- Then operators can see cost, latency, quality, interventions, and recovery behavior at public seams
- And failure behavior is explicit: Block hidden budget overflow, missing telemetry, untested failure modes, private-seam-only tests, and recovery claims without fault evidence.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version workflow profiles and adapters; require migration and rollback evidence before promotion.

### ST-09.07 — Promote, Migrate, Roll Back, and Hotfix Workflow Profiles

As a **Release maintainer**, I want to **promote versioned profiles through CI, migration, rollback, incident, and hotfix gates**, so that **workflow changes remain reversible and operationally governed**

- Global order: `47`
- Dependencies: `ST-09.06`
- Primary outcome: workflow changes remain reversible and operationally governed
- Primary obligations (7): `ADR-016`, `ADR-017`, `FR-206`, `FR-207`, `FR-208`, `HG-014`, `NFR-WORKFLOW-012`
- Relevant FRs: `FR-206`, `FR-207`, `FR-208`
- Relevant NFRs: `NFR-WORKFLOW-012`
- Release 1 disposition: `RELEASE_1_INCLUDED_MANUAL_SHADOW_BEFORE_AUTOMATION`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `Operations, security, and architecture`, `Product lead, Builder maintainer, and workflow architecture`, `TS-14`, `evaluation_governance`
- Component boundary: Builder workflow routing and execution control plane; no monolithic skill-owned or external product workflow.
- Affected contracts: `WorkflowIR`, `WorkflowNodeContract`, `CheckpointReceipt`, `PromotionReceipt`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-10`, `TS-12`, `TS-14`
- Test seam: Manual-shadow parity, node contract, isolation, retry, resume, fault-injection, promotion, and rollback seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Reject promotion without end-to-end and fault tests, incompatible migration, absent rollback, unsigned profile authority, and hotfixes that bypass receipts.
- Observability evidence: `ST-09.07:OutcomeVerified`, `ST-09.07:OutcomeRejected`
- Required tests: `ST-09.07-acceptance`, `ST-09.07-failure`, `ST-09.07-authority`, `ST-09.07-receipt`
- Completion receipt: `ST-09.07:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version workflow profiles and adapters; require migration and rollback evidence before promotion.
- Fresh-context scope: One independently testable Promote, Migrate, Roll Back, and Hotfix Workflow Profiles increment covering 7 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-09.07 are accepted and the covered authority is available,
- When the Release maintainer promotes versioned profiles through CI, migration, rollback, incident, and hotfix gates,
- Then workflow changes remain reversible and operationally governed
- And failure behavior is explicit: Reject promotion without end-to-end and fault tests, incompatible migration, absent rollback, unsigned profile authority, and hotfixes that bypass receipts.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version workflow profiles and adapters; require migration and rollback evidence before promotion.

### ST-09.08 — Measure Workflow Outcomes and Reject Monolithic Orchestration

As a **Workflow maintainer**, I want to **measure cost, latency, quality, and intervention while detecting production workflows hidden inside skills or sessions**, so that **the workflow remains an explicit, testable factory rather than an opaque agent prompt**

- Global order: `48`
- Dependencies: `ST-09.07`
- Primary outcome: the workflow remains an explicit, testable factory rather than an opaque agent prompt
- Primary obligations (5): `AG-019`, `FR-209`, `FR-210`, `HG-011`, `NFR-ARCH-002`
- Relevant FRs: `FR-209`, `FR-210`
- Relevant NFRs: `NFR-ARCH-002`
- Release 1 disposition: `RELEASE_1_INCLUDED_MANUAL_SHADOW_BEFORE_AUTOMATION`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-14`, `evaluation_governance`, `product_constitution`
- Component boundary: Builder workflow routing and execution control plane; no monolithic skill-owned or external product workflow.
- Affected contracts: `WorkflowIR`, `WorkflowNodeContract`, `CheckpointReceipt`, `PromotionReceipt`
- Affected schemas: None; planned contract shapes remain owned by the cited technical specifications
- Primary specifications: `TS-00`, `TS-07`, `TS-14`
- Test seam: Manual-shadow parity, node contract, isolation, retry, resume, fault-injection, promotion, and rollback seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Block monolithic skill-owned production workflows, hidden state, unbounded self-correction, missing public adapters, and architecture that cannot be replayed.
- Observability evidence: `ST-09.08:OutcomeVerified`, `ST-09.08:OutcomeRejected`
- Required tests: `ST-09.08-acceptance`, `ST-09.08-failure`, `ST-09.08-authority`, `ST-09.08-receipt`
- Completion receipt: `ST-09.08:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Version workflow profiles and adapters; require migration and rollback evidence before promotion.
- Fresh-context scope: One independently testable Measure Workflow Outcomes and Reject Monolithic Orchestration increment covering 5 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-09.08 are accepted and the covered authority is available,
- When the Workflow maintainer measures cost, latency, quality, and intervention while detecting production workflows hidden inside skills or sessions,
- Then the workflow remains an explicit, testable factory rather than an opaque agent prompt
- And failure behavior is explicit: Block monolithic skill-owned production workflows, hidden state, unbounded self-correction, missing public adapters, and architecture that cannot be replayed.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Version workflow profiles and adapters; require migration and rollback evidence before promotion.


## EP-10 — Evidence-Derived Human Control Tower

**Epic outcome:** A human can supervise the full Builder run from one approved Control Tower, understand evidence and authority behind every status, inspect category or profile lineage and workflow state, and issue only governed commands without creating a second source of truth.

**Story count:** 14

### ST-10.01 — Open a Trustworthy Run Index and Overview

As a **Harness Architect**, I want to **open the stable Control Tower shell and selects a run from operational tables into a complete overview**, so that **the current target, category, stage, status, and next governed action are immediately understandable**

- Global order: `49`
- Dependencies: `ST-01.04`, `ST-03.05`, `ST-04.05`, `ST-05.05`, `ST-06.05`, `ST-07.04`, `ST-08.07`, `ST-09.08`
- Primary outcome: the current target, category, stage, status, and next governed action are immediately understandable
- Primary obligations (6): `FR-117`, `NFR-PERF-001`, `UXC-101`, `UXC-102`, `UXC-201`, `UXC-202`
- Relevant FRs: `FR-117`
- Relevant NFRs: `NFR-PERF-001`
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-12`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-12`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Show explicit empty or unavailable state rather than optimistic status when no run or projection exists.
- Observability evidence: `ST-10.01:OutcomeVerified`, `ST-10.01:OutcomeRejected`
- Required tests: `ST-10.01-acceptance`, `ST-10.01-failure`, `ST-10.01-authority`, `ST-10.01-receipt`
- Completion receipt: `ST-10.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Open a Trustworthy Run Index and Overview increment covering 6 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.01 are accepted and the covered authority is available,
- When the Harness Architect opens the stable Control Tower shell and selects a run from operational tables into a complete overview,
- Then the current target, category, stage, status, and next governed action are immediately understandable
- And failure behavior is explicit: Show explicit empty or unavailable state rather than optimistic status when no run or projection exists.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.02 — Explore Phase, Context, and Dependency Graphs

As a **Harness Architect**, I want to **navigate phase, context, ownership, and dependency graphs with addressable selections**, so that **the architect can trace what is ready, blocked, upstream, or affected without losing context**

- Global order: `50`
- Dependencies: `ST-10.01`
- Primary outcome: the architect can trace what is ready, blocked, upstream, or affected without losing context
- Primary obligations (3): `FR-118`, `UXC-103`, `UXC-203`
- Relevant FRs: `FR-118`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-12`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-12`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Reject dangling graph navigation, hidden dependency states, inaccessible keyboard traversal, and graph views that invent authority.
- Observability evidence: `ST-10.02:OutcomeVerified`, `ST-10.02:OutcomeRejected`
- Required tests: `ST-10.02-acceptance`, `ST-10.02-failure`, `ST-10.02-authority`, `ST-10.02-receipt`
- Completion receipt: `ST-10.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Explore Phase, Context, and Dependency Graphs increment covering 3 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.02 are accepted and the covered authority is available,
- When the Harness Architect navigates phase, context, ownership, and dependency graphs with addressable selections,
- Then the architect can trace what is ready, blocked, upstream, or affected without losing context
- And failure behavior is explicit: Reject dangling graph navigation, hidden dependency states, inaccessible keyboard traversal, and graph views that invent authority.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.03 — Inspect Evidence and Syntax Behind Decisions

As a **Constitutional reviewer**, I want to **open evidence specimens, source locks, knowledge status, syntax observations, and hypotheses from the run**, so that **every critical claim can be inspected at its originating evidence and parse seam**

- Global order: `51`
- Dependencies: `ST-10.02`
- Primary outcome: every critical claim can be inspected at its originating evidence and parse seam
- Primary obligations (3): `FR-119`, `UXC-104`, `UXC-204`
- Relevant FRs: `FR-119`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-12`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-02`, `TS-12`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Redact unauthorized evidence, show missing or stale projections honestly, and prohibit the UI from upgrading hypotheses into facts.
- Observability evidence: `ST-10.03:OutcomeVerified`, `ST-10.03:OutcomeRejected`
- Required tests: `ST-10.03-acceptance`, `ST-10.03-failure`, `ST-10.03-authority`, `ST-10.03-receipt`
- Completion receipt: `ST-10.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Inspect Evidence and Syntax Behind Decisions increment covering 3 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.03 are accepted and the covered authority is available,
- When the Constitutional reviewer opens evidence specimens, source locks, knowledge status, syntax observations, and hypotheses from the run,
- Then every critical claim can be inspected at its originating evidence and parse seam
- And failure behavior is explicit: Redact unauthorized evidence, show missing or stale projections honestly, and prohibit the UI from upgrading hypotheses into facts.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.04 — Review Genesis Decisions and Human Authority

As a **Product authority**, I want to **review dependency state, recommendations, answers, final decisions, and receipts and invokes only available human actions**, so that **constitutional authority remains understandable and resumable from the Control Tower**

- Global order: `52`
- Dependencies: `ST-10.03`
- Primary outcome: constitutional authority remains understandable and resumable from the Control Tower
- Primary obligations (2): `FR-120`, `UXC-105`
- Relevant FRs: `FR-120`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-12`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-12`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Block actions without server-described authority, hide no contradiction, and show a conflict instead of overwriting concurrent decisions.
- Observability evidence: `ST-10.04:OutcomeVerified`, `ST-10.04:OutcomeRejected`
- Required tests: `ST-10.04-acceptance`, `ST-10.04-failure`, `ST-10.04-authority`, `ST-10.04-receipt`
- Completion receipt: `ST-10.04:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Review Genesis Decisions and Human Authority increment covering 2 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.04 are accepted and the covered authority is available,
- When the Product authority reviews dependency state, recommendations, answers, final decisions, and receipts and invokes only available human actions,
- Then constitutional authority remains understandable and resumable from the Control Tower
- And failure behavior is explicit: Block actions without server-described authority, hide no contradiction, and show a conflict instead of overwriting concurrent decisions.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.05 — Trace Skills, Recipes, and Runtime Capsules

As a **Skill maintainer**, I want to **inspect canonical skills, local adaptations, recipes, binding versions, evaluators, and capsule manifests**, so that **the maintainer can explain which behavior and context entered a phase**

- Global order: `53`
- Dependencies: `ST-10.04`
- Primary outcome: the maintainer can explain which behavior and context entered a phase
- Primary obligations (2): `FR-121`, `UXC-106`
- Relevant FRs: `FR-121`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-12`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-10`, `TS-12`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Show missing evaluator or hash as blocked, distinguish canonical skills from capsules, and never expose secrets or hidden prompt history.
- Observability evidence: `ST-10.05:OutcomeVerified`, `ST-10.05:OutcomeRejected`
- Required tests: `ST-10.05-acceptance`, `ST-10.05-failure`, `ST-10.05-authority`, `ST-10.05-receipt`
- Completion receipt: `ST-10.05:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Trace Skills, Recipes, and Runtime Capsules increment covering 2 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.05 are accepted and the covered authority is available,
- When the Skill maintainer inspects canonical skills, local adaptations, recipes, binding versions, evaluators, and capsule manifests,
- Then the maintainer can explain which behavior and context entered a phase
- And failure behavior is explicit: Show missing evaluator or hash as blocked, distinguish canonical skills from capsules, and never expose secrets or hidden prompt history.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.06 — Inspect Ownership, Modules, and Contracts

As a **Architecture maintainer**, I want to **trace capabilities through owners, modules, phases, contracts, and cross-product boundaries**, so that **responsibility and permitted mutation remain clear before change or handoff**

- Global order: `54`
- Dependencies: `ST-10.05`
- Primary outcome: responsibility and permitted mutation remain clear before change or handoff
- Primary obligations (2): `FR-122`, `UXC-107`
- Relevant FRs: `FR-122`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-12`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-06`, `TS-12`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Reject views that merge product ownership, hide contract versions, or allow UI-side edits to authoritative architecture.
- Observability evidence: `ST-10.06:OutcomeVerified`, `ST-10.06:OutcomeRejected`
- Required tests: `ST-10.06-acceptance`, `ST-10.06-failure`, `ST-10.06-authority`, `ST-10.06-receipt`
- Completion receipt: `ST-10.06:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Inspect Ownership, Modules, and Contracts increment covering 2 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.06 are accepted and the covered authority is available,
- When the Architecture maintainer traces capabilities through owners, modules, phases, contracts, and cross-product boundaries,
- Then responsibility and permitted mutation remain clear before change or handoff
- And failure behavior is explicit: Reject views that merge product ownership, hide contract versions, or allow UI-side edits to authoritative architecture.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.07 — Judge Evaluations, Repairs, and Authorization Trajectory

As a **Independent reviewer**, I want to **compare benchmark receipts, hard gates, failures, repair history, and authorization outcomes**, so that **the reviewer can see why readiness advanced, regressed, or remains blocked**

- Global order: `55`
- Dependencies: `ST-10.06`
- Primary outcome: the reviewer can see why readiness advanced, regressed, or remains blocked
- Primary obligations (4): `FR-123`, `UXC-108`, `UXC-109`, `UXC-113`
- Relevant FRs: `FR-123`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-12`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-10`, `TS-12`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Never render missing thresholds as a pass, never hide failed dimensions, and distinguish prototype-only from production authorization.
- Observability evidence: `ST-10.07:OutcomeVerified`, `ST-10.07:OutcomeRejected`
- Required tests: `ST-10.07-acceptance`, `ST-10.07-failure`, `ST-10.07-authority`, `ST-10.07-receipt`
- Completion receipt: `ST-10.07:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Judge Evaluations, Repairs, and Authorization Trajectory increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.07 are accepted and the covered authority is available,
- When the Independent reviewer compares benchmark receipts, hard gates, failures, repair history, and authorization outcomes,
- Then the reviewer can see why readiness advanced, regressed, or remains blocked
- And failure behavior is explicit: Never render missing thresholds as a pass, never hide failed dimensions, and distinguish prototype-only from production authorization.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.08 — Monitor Workflow, Incidents, Cost, and Context

As a **Builder operator**, I want to **monitor workflow queues, nodes, incidents, retries, latency, model usage, and context budgets**, so that **operational pressure and intervention needs are visible before they become silent failure**

- Global order: `56`
- Dependencies: `ST-10.07`
- Primary outcome: operational pressure and intervention needs are visible before they become silent failure
- Primary obligations (3): `FR-124`, `UXC-110`, `UXC-111`
- Relevant FRs: `FR-124`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-12`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-12`, `TS-14`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Show partial telemetry and disconnection explicitly, flag budget overflow, and prevent hidden retries or parallel work.
- Observability evidence: `ST-10.08:OutcomeVerified`, `ST-10.08:OutcomeRejected`
- Required tests: `ST-10.08-acceptance`, `ST-10.08-failure`, `ST-10.08-authority`, `ST-10.08-receipt`
- Completion receipt: `ST-10.08:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Monitor Workflow, Incidents, Cost, and Context increment covering 3 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.08 are accepted and the covered authority is available,
- When the Builder operator monitors workflow queues, nodes, incidents, retries, latency, model usage, and context budgets,
- Then operational pressure and intervention needs are visible before they become silent failure
- And failure behavior is explicit: Show partial telemetry and disconnection explicitly, flag budget overflow, and prevent hidden retries or parallel work.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.09 — Execute Governed Commands and Export Receipts

As a **Authorized operator**, I want to **preflight, confirms, submits, resolves, and exports through server-described typed commands**, so that **human actions remain least-privilege, conflict-aware, and auditable**

- Global order: `57`
- Dependencies: `ST-10.08`
- Primary outcome: human actions remain least-privilege, conflict-aware, and auditable
- Primary obligations (10): `FR-125`, `NFR-OBS-004`, `UXC-112`, `UXC-301`, `UXC-302`, `UXC-303`, `UXC-304`, `UXC-305`, `UXC-306`, `UXC-307`
- Relevant FRs: `FR-125`
- Relevant NFRs: `NFR-OBS-004`
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-12`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-01`, `TS-06`, `TS-12`, `TS-14`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Reject unauthorized commands, require confirmation where declared, preserve conflicts, and export only governed redacted evidence with receipts.
- Observability evidence: `ST-10.09:OutcomeVerified`, `ST-10.09:OutcomeRejected`
- Required tests: `ST-10.09-acceptance`, `ST-10.09-failure`, `ST-10.09-authority`, `ST-10.09-receipt`
- Completion receipt: `ST-10.09:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Execute Governed Commands and Export Receipts increment covering 10 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.09 are accepted and the covered authority is available,
- When the Authorized operator preflights, confirms, submits, resolves, and exports through server-described typed commands,
- Then human actions remain least-privilege, conflict-aware, and auditable
- And failure behavior is explicit: Reject unauthorized commands, require confirmation where declared, preserve conflicts, and export only governed redacted evidence with receipts.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.10 — Use a Stable, Accessible, Evidence-Backed Shell

As a **Any authorized Control Tower user**, I want to **operate the approved shell through progressive disclosure, keyboard access, honest uncertainty, and responsive continuity**, so that **the Control Tower remains usable without becoming a second source of truth**

- Global order: `58`
- Dependencies: `ST-10.09`
- Primary outcome: the Control Tower remains usable without becoming a second source of truth
- Primary obligations (12): `NFR-UX-001`, `NFR-UX-002`, `UXC-001`, `UXC-002`, `UXC-003`, `UXC-004`, `UXC-005`, `UXC-006`, `UXC-007`, `UXC-008`, `UXC-009`, `UXC-010`
- Relevant FRs: None
- Relevant NFRs: `NFR-UX-001`, `NFR-UX-002`
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-12`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-01`, `TS-02`, `TS-06`, `TS-12`, `TS-14`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Fail accessibility or authority checks rather than hiding controls, fabricating status, or losing addressable context.
- Observability evidence: `ST-10.10:OutcomeVerified`, `ST-10.10:OutcomeRejected`
- Required tests: `ST-10.10-acceptance`, `ST-10.10-failure`, `ST-10.10-authority`, `ST-10.10-receipt`
- Completion receipt: `ST-10.10:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Use a Stable, Accessible, Evidence-Backed Shell increment covering 12 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.10 are accepted and the covered authority is available,
- When the Any authorized Control Tower user operates the approved shell through progressive disclosure, keyboard access, honest uncertainty, and responsive continuity,
- Then the Control Tower remains usable without becoming a second source of truth
- And failure behavior is explicit: Fail accessibility or authority checks rather than hiding controls, fabricating status, or losing addressable context.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.11 — Preserve Workspace Context Across Inspectors and Layouts

As a **Control Tower user**, I want to **move among tables, inspectors, dialogs, notices, and compact layouts while preserving selection and context**, so that **dense operational review stays coherent across screen sizes and interaction modes**

- Global order: `59`
- Dependencies: `ST-10.10`
- Primary outcome: dense operational review stays coherent across screen sizes and interaction modes
- Primary obligations (5): `UXC-205`, `UXC-206`, `UXC-207`, `UXC-208`, `UXC-209`
- Relevant FRs: None
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-12`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Reject context-destructive navigation, inaccessible dialogs, missing status notices, and compact layouts that hide required authority.
- Observability evidence: `ST-10.11:OutcomeVerified`, `ST-10.11:OutcomeRejected`
- Required tests: `ST-10.11-acceptance`, `ST-10.11-failure`, `ST-10.11-authority`, `ST-10.11-receipt`
- Completion receipt: `ST-10.11:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Preserve Workspace Context Across Inspectors and Layouts increment covering 5 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.11 are accepted and the covered authority is available,
- When the Control Tower user moves among tables, inspectors, dialogs, notices, and compact layouts while preserving selection and context,
- Then dense operational review stays coherent across screen sizes and interaction modes
- And failure behavior is explicit: Reject context-destructive navigation, inaccessible dialogs, missing status notices, and compact layouts that hide required authority.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.12 — Represent Loading, Empty, Stale, and Disconnected State Honestly

As a **Control Tower user**, I want to **encounter loading, empty, stale, or disconnected projections**, so that **the interface communicates evidence age and availability without optimistic authority**

- Global order: `60`
- Dependencies: `ST-10.11`
- Primary outcome: the interface communicates evidence age and availability without optimistic authority
- Primary obligations (11): `ADR-003`, `ADR-011`, `D025`, `NFR-OBS-001`, `NFR-OBS-002`, `NFR-OBS-003`, `NFR-TRACE-002`, `UXC-401`, `UXC-402`, `UXC-403`, `UXC-404`
- Relevant FRs: None
- Relevant NFRs: `NFR-OBS-001`, `NFR-OBS-002`, `NFR-OBS-003`, `NFR-TRACE-002`
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `Architecture and operations`, `TS-12`, `UX, architecture, and operations`, `product_constitution`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `IMPLEMENTATION_BASELINE`, `TS-01`, `TS-02`, `TS-05`, `TS-06`, `TS-07`, `TS-10`, `TS-12`, `TS-13`, `TS-14`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Never substitute cached success for disconnected truth, hide stale timestamps, or enable commands against unavailable authoritative state.
- Observability evidence: `ST-10.12:OutcomeVerified`, `ST-10.12:OutcomeRejected`
- Required tests: `ST-10.12-acceptance`, `ST-10.12-failure`, `ST-10.12-authority`, `ST-10.12-receipt`
- Completion receipt: `ST-10.12:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Represent Loading, Empty, Stale, and Disconnected State Honestly increment covering 11 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.12 are accepted and the covered authority is available,
- When the Control Tower user encounters loading, empty, stale, or disconnected projections,
- Then the interface communicates evidence age and availability without optimistic authority
- And failure behavior is explicit: Never substitute cached success for disconnected truth, hide stale timestamps, or enable commands against unavailable authoritative state.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.13 — Contain Partial, Redacted, Failed, and Invalidated Projections

As a **Control Tower user**, I want to **encounter partial, unauthorized, failed, or invalidated data and follows its recovery path**, so that **the interface preserves security and truth while exposing what can be retried or inspected**

- Global order: `61`
- Dependencies: `ST-10.12`
- Primary outcome: the interface preserves security and truth while exposing what can be retried or inspected
- Primary obligations (6): `AG-016`, `FR-126`, `UXC-405`, `UXC-406`, `UXC-407`, `UXC-408`
- Relevant FRs: `FR-126`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `TS-12`, `product_constitution`, `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-00`, `TS-12`, `TS-14`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Do not leak redacted content, collapse partial state into success, suppress query failure, or retain invalidated projections as current.
- Observability evidence: `ST-10.13:OutcomeVerified`, `ST-10.13:OutcomeRejected`
- Required tests: `ST-10.13-acceptance`, `ST-10.13-failure`, `ST-10.13-authority`, `ST-10.13-receipt`
- Completion receipt: `ST-10.13:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Contain Partial, Redacted, Failed, and Invalidated Projections increment covering 6 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.13 are accepted and the covered authority is available,
- When the Control Tower user encounters partial, unauthorized, failed, or invalidated data and follows its recovery path,
- Then the interface preserves security and truth while exposing what can be retried or inspected
- And failure behavior is explicit: Do not leak redacted content, collapse partial state into success, suppress query failure, or retain invalidated projections as current.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.

### ST-10.14 — Operate Large Collections Within Interaction Budgets

As a **Control Tower user**, I want to **query and navigates large evidence, event, and run collections under declared budgets**, so that **the interface remains responsive and measurable at Release 1 scale**

- Global order: `62`
- Dependencies: `ST-10.13`
- Primary outcome: the interface remains responsive and measurable at Release 1 scale
- Primary obligations (4): `UXC-501`, `UXC-502`, `UXC-503`, `UXC-504`
- Relevant FRs: None
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `ux_architecture`
- Component boundary: Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.
- Affected contracts: `ControlTowerConstitutionalProjection`, `GovernedCommand`, `ProjectionReceipt`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection`
- Primary specifications: `TS-12`, `TS-14`
- Test seam: Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.
- Gate references: None
- Implementation gate status: `CONDITIONAL_EXTERNAL_DEPENDENCY`
- Failure behavior: Reject unbounded queries, hidden pagination loss, interaction-budget violations, and missing UX telemetry for degraded operations.
- Observability evidence: `ST-10.14:OutcomeVerified`, `ST-10.14:OutcomeRejected`
- Required tests: `ST-10.14-acceptance`, `ST-10.14-failure`, `ST-10.14-authority`, `ST-10.14-receipt`
- Completion receipt: `ST-10.14:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.
- Fresh-context scope: One independently testable Operate Large Collections Within Interaction Budgets increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-10.14 are accepted and the covered authority is available,
- When the Control Tower user queries and navigates large evidence, event, and run collections under declared budgets,
- Then the interface remains responsive and measurable at Release 1 scale
- And failure behavior is explicit: Reject unbounded queries, hidden pagination loss, interaction-budget violations, and missing UX telemetry for degraded operations.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.


## EP-11 — Traceable Development Capsule and Implementation Handoff

**Epic outcome:** An implementation team can receive one versioned Development Capsule containing only justified scaffolding, typed contracts, fixtures, dependency ordering, acceptance evidence, and frozen authority needed to implement a complete vertical slice without inventing product decisions.

**Story count:** 3

### ST-11.01 — Generate a Versioned Traceable Development Capsule

As a **Implementation lead**, I want to **compile requirements, architecture, contracts, justified scaffolding, examples, fixtures, and acceptance evidence into one capsule**, so that **an implementation team receives complete authority without inventing missing product decisions**

- Global order: `63`
- Dependencies: `ST-03.05`, `ST-04.05`, `ST-05.05`, `ST-06.05`, `ST-07.04`, `ST-08.07`, `ST-09.08`, `ST-10.14`
- Primary outcome: an implementation team receives complete authority without inventing missing product decisions
- Primary obligations (6): `D029`, `FR-151`, `FR-152`, `FR-153`, `FR-154`, `FR-155`
- Relevant FRs: `FR-151`, `FR-152`, `FR-153`, `FR-154`, `FR-155`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED_HANDOFF_ONLY_NO_IMPLEMENTATION_AUTHORIZATION`
- Release 1 role: `IMPLEMENTATION_HANDOFF_PLANNING_ONLY`
- Implementation owners: `TS-13`, `product_constitution`
- Component boundary: Development Capsule and implementation handoff planning; no implementation execution in this increment.
- Affected contracts: `DevelopmentCapsule`, `StoryCompletionReceipt`, `ImplementationDeltaProposal`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`
- Primary specifications: `TS-01`, `TS-06`, `TS-11`, `TS-13`, `TS-14`
- Test seam: Capsule completeness, traceability, contract example, fixture, dependency-order, and feedback-ingestion seams.
- Gate references: `BD-008`, `BD-014`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block incomplete traceability, unjustified scaffolding, missing test fixtures, unresolved contract versions, and capsules without immutable hashes.
- Observability evidence: `ST-11.01:OutcomeVerified`, `ST-11.01:OutcomeRejected`
- Required tests: `ST-11.01-acceptance`, `ST-11.01-failure`, `ST-11.01-authority`, `ST-11.01-receipt`
- Completion receipt: `ST-11.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Hash-bind every capsule to authority and contract versions; govern all later implementation-discovered deltas.
- Fresh-context scope: One independently testable Generate a Versioned Traceable Development Capsule increment covering 6 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-11.01 are accepted and the covered authority is available,
- When the Implementation lead compiles requirements, architecture, contracts, justified scaffolding, examples, fixtures, and acceptance evidence into one capsule,
- Then an implementation team receives complete authority without inventing missing product decisions
- And failure behavior is explicit: Block incomplete traceability, unjustified scaffolding, missing test fixtures, unresolved contract versions, and capsules without immutable hashes.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Hash-bind every capsule to authority and contract versions; govern all later implementation-discovered deltas.

### ST-11.02 — Plan Dependency-Ordered Vertical Implementation Increments

As a **Implementation lead**, I want to **derive one working vertical-slice plan and dependency-ordered Stories from the accepted capsule**, so that **implementation can deliver user-observable value without horizontal layer sequencing or future-story dependencies**

- Global order: `64`
- Dependencies: `ST-11.01`
- Primary outcome: implementation can deliver user-observable value without horizontal layer sequencing or future-story dependencies
- Primary obligations (2): `FR-156`, `FR-157`
- Relevant FRs: `FR-156`, `FR-157`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED_HANDOFF_ONLY_NO_IMPLEMENTATION_AUTHORIZATION`
- Release 1 role: `IMPLEMENTATION_HANDOFF_PLANNING_ONLY`
- Implementation owners: `TS-13`
- Component boundary: Development Capsule and implementation handoff planning; no implementation execution in this increment.
- Affected contracts: `DevelopmentCapsule`, `StoryCompletionReceipt`, `ImplementationDeltaProposal`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`
- Primary specifications: `TS-13`
- Test seam: Capsule completeness, traceability, contract example, fixture, dependency-order, and feedback-ingestion seams.
- Gate references: `BD-008`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject stories that exceed one fresh context, depend on future work, omit acceptance evidence, or authorize implementation while readiness is FAIL.
- Observability evidence: `ST-11.02:OutcomeVerified`, `ST-11.02:OutcomeRejected`
- Required tests: `ST-11.02-acceptance`, `ST-11.02-failure`, `ST-11.02-authority`, `ST-11.02-receipt`
- Completion receipt: `ST-11.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Hash-bind every capsule to authority and contract versions; govern all later implementation-discovered deltas.
- Fresh-context scope: One independently testable Plan Dependency-Ordered Vertical Implementation Increments increment covering 2 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-11.02 are accepted and the covered authority is available,
- When the Implementation lead derives one working vertical-slice plan and dependency-ordered Stories from the accepted capsule,
- Then implementation can deliver user-observable value without horizontal layer sequencing or future-story dependencies
- And failure behavior is explicit: Reject stories that exceed one fresh context, depend on future work, omit acceptance evidence, or authorize implementation while readiness is FAIL.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Hash-bind every capsule to authority and contract versions; govern all later implementation-discovered deltas.

### ST-11.03 — Govern Implementation Deltas and Certification Feedback

As a **Harness Architect**, I want to **ingest implementation discoveries, evaluation results, and certification feedback as typed amendment proposals**, so that **validated authority can evolve without silent drift between planning and implementation**

- Global order: `65`
- Dependencies: `ST-11.02`
- Primary outcome: validated authority can evolve without silent drift between planning and implementation
- Primary obligations (2): `FR-158`, `FR-159`
- Relevant FRs: `FR-158`, `FR-159`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_INCLUDED_HANDOFF_ONLY_NO_IMPLEMENTATION_AUTHORIZATION`
- Release 1 role: `IMPLEMENTATION_HANDOFF_PLANNING_ONLY`
- Implementation owners: `TS-13`
- Component boundary: Development Capsule and implementation handoff planning; no implementation execution in this increment.
- Affected contracts: `DevelopmentCapsule`, `StoryCompletionReceipt`, `ImplementationDeltaProposal`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`
- Primary specifications: `TS-13`
- Test seam: Capsule completeness, traceability, contract example, fixture, dependency-order, and feedback-ingestion seams.
- Gate references: `BD-008`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block direct mutation of frozen authority, untraceable feedback, incompatible capsule changes, and acceptance of downstream results without artifact identity.
- Observability evidence: `ST-11.03:OutcomeVerified`, `ST-11.03:OutcomeRejected`
- Required tests: `ST-11.03-acceptance`, `ST-11.03-failure`, `ST-11.03-authority`, `ST-11.03-receipt`
- Completion receipt: `ST-11.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Hash-bind every capsule to authority and contract versions; govern all later implementation-discovered deltas.
- Fresh-context scope: One independently testable Govern Implementation Deltas and Certification Feedback increment covering 2 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-11.03 are accepted and the covered authority is available,
- When the Harness Architect ingests implementation discoveries, evaluation results, and certification feedback as typed amendment proposals,
- Then validated authority can evolve without silent drift between planning and implementation
- And failure behavior is explicit: Block direct mutation of frozen authority, untraceable feedback, incompatible capsule changes, and acceptance of downstream results without artifact identity.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Hash-bind every capsule to authority and contract versions; govern all later implementation-discovered deltas.


## EP-12 — Brownfield Migration and Release 1 Reference Proof

**Epic outcome:** The team can preserve proven V2.1 behavior, migrate only with evidence and receipts, dual-compile eligible targets, and prove the complete Builder spine through one Format 02 reference path without overstating category or target certification.

**Story count:** 4

### ST-12.01 — Inventory and Map Proven V2.1 Behavior

As a **Brownfield maintainer**, I want to **inventory repository-local V2.1 capabilities and maps each concept into retain, adapt, replace, or defer evidence**, so that **migration starts from proven assets rather than a greenfield rewrite**

- Global order: `66`
- Dependencies: `ST-06.05`, `ST-07.04`, `ST-08.07`, `ST-09.08`, `ST-10.14`, `ST-11.03`
- Primary outcome: migration starts from proven assets rather than a greenfield rewrite
- Primary obligations (4): `ADR-015`, `FR-160`, `FR-161`, `NFR-COMPAT-001`
- Relevant FRs: `FR-160`, `FR-161`
- Relevant NFRs: `NFR-COMPAT-001`
- Release 1 disposition: `RELEASE_1_FORMAT02_REFERENCE_PROOF_GENERAL_CERTIFICATION_DEFERRED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `Architecture and repository authority`, `IMPLEMENTATION_BASELINE`
- Component boundary: Brownfield migration and bounded Release 1 proof; no general certification from the Format 02 reference path.
- Affected contracts: `MigrationReceipt`, `CertificationMatrix`, `ConstitutionalReadinessReceipt`, `DelegationHandoff`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`, `docs/contracts/schemas/visual-semantic-handoff.schema.json`
- Primary specifications: `IMPLEMENTATION_BASELINE`
- Test seam: Dual-compilation, regression, migration receipt, compatibility alias, reference-path, and certification-scope seams.
- Gate references: `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block migration claims without accessible authoritative artifacts, evidence, owner, or an explicit no-local-baseline disposition.
- Observability evidence: `ST-12.01:OutcomeVerified`, `ST-12.01:OutcomeRejected`
- Required tests: `ST-12.01-acceptance`, `ST-12.01-failure`, `ST-12.01-authority`, `ST-12.01-receipt`
- Completion receipt: `ST-12.01:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Retain or deprecate V2.1 behavior only through evidence and receipts; keep unproven categories and targets uncertified.
- Fresh-context scope: One independently testable Inventory and Map Proven V2.1 Behavior increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-12.01 are accepted and the covered authority is available,
- When the Brownfield maintainer inventories repository-local V2.1 capabilities and maps each concept into retain, adapt, replace, or defer evidence,
- Then migration starts from proven assets rather than a greenfield rewrite
- And failure behavior is explicit: Block migration claims without accessible authoritative artifacts, evidence, owner, or an explicit no-local-baseline disposition.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Retain or deprecate V2.1 behavior only through evidence and receipts; keep unproven categories and targets uncertified.

### ST-12.02 — Dual-Compile and Migrate Through Regression Receipts

As a **Brownfield maintainer**, I want to **dual-compile eligible targets, applies incremental migration, runs regressions, and emits compatibility and deprecation receipts**, so that **retained behavior changes only through evidence-backed, reversible increments**

- Global order: `67`
- Dependencies: `ST-12.01`
- Primary outcome: retained behavior changes only through evidence-backed, reversible increments
- Primary obligations (6): `D028`, `FR-162`, `FR-163`, `FR-164`, `FR-165`, `FR-166`
- Relevant FRs: `FR-162`, `FR-163`, `FR-164`, `FR-165`, `FR-166`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_FORMAT02_REFERENCE_PROOF_GENERAL_CERTIFICATION_DEFERRED`
- Release 1 role: `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT`
- Implementation owners: `IMPLEMENTATION_BASELINE`, `product_constitution`
- Component boundary: Brownfield migration and bounded Release 1 proof; no general certification from the Format 02 reference path.
- Affected contracts: `MigrationReceipt`, `CertificationMatrix`, `ConstitutionalReadinessReceipt`, `DelegationHandoff`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`, `docs/contracts/schemas/visual-semantic-handoff.schema.json`
- Primary specifications: `IMPLEMENTATION_BASELINE`, `TS-02`, `TS-06`, `TS-10`, `TS-13`, `TS-14`
- Test seam: Dual-compilation, regression, migration receipt, compatibility alias, reference-path, and certification-scope seams.
- Gate references: `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject lossy aliases, untested deprecation, missing rollback, silent schema drift, and migration that regresses a protected baseline.
- Observability evidence: `ST-12.02:OutcomeVerified`, `ST-12.02:OutcomeRejected`
- Required tests: `ST-12.02-acceptance`, `ST-12.02-failure`, `ST-12.02-authority`, `ST-12.02-receipt`
- Completion receipt: `ST-12.02:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Retain or deprecate V2.1 behavior only through evidence and receipts; keep unproven categories and targets uncertified.
- Fresh-context scope: One independently testable Dual-Compile and Migrate Through Regression Receipts increment covering 6 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-12.02 are accepted and the covered authority is available,
- When the Brownfield maintainer dual-compiles eligible targets, applies incremental migration, runs regressions, and emits compatibility and deprecation receipts,
- Then retained behavior changes only through evidence-backed, reversible increments
- And failure behavior is explicit: Reject lossy aliases, untested deprecation, missing rollback, silent schema drift, and migration that regresses a protected baseline.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Retain or deprecate V2.1 behavior only through evidence and receipts; keep unproven categories and targets uncertified.

### ST-12.03 — Prove the Complete Builder Spine Through Format 02

As a **Release reviewer**, I want to **run one complete Format 02 reference path from evidence through implementation handoff, evaluation, repair, and certification evidence**, so that **Release 1 demonstrates a coherent vertical product outcome instead of disconnected infrastructure**

- Global order: `68`
- Dependencies: `ST-12.02`
- Primary outcome: Release 1 demonstrates a coherent vertical product outcome instead of disconnected infrastructure
- Primary obligations (3): `ADR-014`, `D003`, `FR-167`
- Relevant FRs: `FR-167`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_FORMAT02_REFERENCE_PROOF_GENERAL_CERTIFICATION_DEFERRED`
- Release 1 role: `FORMAT_02_REFERENCE_PATH_PROOF`
- Implementation owners: `Product lead and category steward`, `TS-15`, `product_constitution`
- Component boundary: Brownfield migration and bounded Release 1 proof; no general certification from the Format 02 reference path.
- Affected contracts: `MigrationReceipt`, `CertificationMatrix`, `ConstitutionalReadinessReceipt`, `DelegationHandoff`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`, `docs/contracts/schemas/visual-semantic-handoff.schema.json`
- Primary specifications: `TS-02`, `TS-04`, `TS-06`, `TS-07`, `TS-10`, `TS-11`, `TS-13`, `TS-14`, `TS-15`
- Test seam: Dual-compilation, regression, migration receipt, compatibility alias, reference-path, and certification-scope seams.
- Gate references: `BD-004`, `BD-008`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Block the reference proof when any required stage, target stub, hard gate, evaluator, or receipt is missing; do not implement in this planning step.
- Observability evidence: `ST-12.03:OutcomeVerified`, `ST-12.03:OutcomeRejected`
- Required tests: `ST-12.03-acceptance`, `ST-12.03-failure`, `ST-12.03-authority`, `ST-12.03-receipt`
- Completion receipt: `ST-12.03:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Retain or deprecate V2.1 behavior only through evidence and receipts; keep unproven categories and targets uncertified.
- Fresh-context scope: One independently testable Prove the Complete Builder Spine Through Format 02 increment covering 3 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-12.03 are accepted and the covered authority is available,
- When the Release reviewer runs one complete Format 02 reference path from evidence through implementation handoff, evaluation, repair, and certification evidence,
- Then Release 1 demonstrates a coherent vertical product outcome instead of disconnected infrastructure
- And failure behavior is explicit: Block the reference proof when any required stage, target stub, hard gate, evaluator, or receipt is missing; do not implement in this planning step.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Retain or deprecate V2.1 behavior only through evidence and receipts; keep unproven categories and targets uncertified.

### ST-12.04 — Publish Bounded Certification Claims Across Categories and Targets

As a **Product authority**, I want to **publish a certification matrix for five categories, four conversational profiles, and three targets**, so that **proven Release 1 scope is explicit while unproven transfer outcomes remain uncertified**

- Global order: `69`
- Dependencies: `ST-12.03`
- Primary outcome: proven Release 1 scope is explicit while unproven transfer outcomes remain uncertified
- Primary obligations (4): `AG-017`, `D032`, `FR-168`, `FR-169`
- Relevant FRs: `FR-168`, `FR-169`
- Relevant NFRs: None
- Release 1 disposition: `RELEASE_1_FORMAT02_REFERENCE_PROOF_GENERAL_CERTIFICATION_DEFERRED`
- Release 1 role: `FORMAT_02_CERTIFICATION_SCOPE_AND_GENERAL_DEFERRAL`
- Implementation owners: `TS-15`, `product_constitution`
- Component boundary: Brownfield migration and bounded Release 1 proof; no general certification from the Format 02 reference path.
- Affected contracts: `MigrationReceipt`, `CertificationMatrix`, `ConstitutionalReadinessReceipt`, `DelegationHandoff`
- Affected schemas: `docs/contracts/schemas/constitutional-evaluation.schema.json`, `docs/contracts/schemas/visual-semantic-handoff.schema.json`
- Primary specifications: `TS-00`, `TS-10`, `TS-13`, `TS-14`, `TS-15`
- Test seam: Dual-compilation, regression, migration receipt, compatibility alias, reference-path, and certification-scope seams.
- Gate references: `BD-004`, `BD-007`, `BD-008`, `BD-010`, `BD-014`, `HD-006`, `HD-007`
- Implementation gate status: `BLOCKED_PENDING_HUMAN_DECISION`
- Failure behavior: Reject general Builder readiness from one harness, inherited Interview or ReelCast certification, and production claims while any required decision or blocker remains open.
- Observability evidence: `ST-12.04:OutcomeVerified`, `ST-12.04:OutcomeRejected`
- Required tests: `ST-12.04-acceptance`, `ST-12.04-failure`, `ST-12.04-authority`, `ST-12.04-receipt`
- Completion receipt: `ST-12.04:StoryCompletionReceipt:<artifact-hash>` (`PLANNED_NOT_ISSUED`)
- Migration or compatibility: Retain or deprecate V2.1 behavior only through evidence and receipts; keep unproven categories and targets uncertified.
- Fresh-context scope: One independently testable Publish Bounded Certification Claims Across Categories and Targets increment covering 4 primary obligations; no production implementation is authorized by this plan.

Acceptance criteria:

- Given all dependency outputs for ST-12.04 are accepted and the covered authority is available,
- When the Product authority publishes a certification matrix for five categories, four conversational profiles, and three targets,
- Then proven Release 1 scope is explicit while unproven transfer outcomes remain uncertified
- And failure behavior is explicit: Reject general Builder readiness from one harness, inherited Interview or ReelCast certification, and production claims while any required decision or blocker remains open.
- And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.
- And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.
- And compatibility behavior is enforced: Retain or deprecate V2.1 behavior only through evidence and receipts; keep unproven categories and targets uncertified.



## Step boundary

- Vertical Story proposal: `AWAITING_HUMAN_CONFIRMATION`.
- Step 4 full coverage and implementation-readiness validation: `NOT_AUTHORIZED`.
- Production implementation: `PROHIBITED_READINESS_FAIL`.
- Next action: human confirms or corrects the Story inventory before Step 4 begins.
