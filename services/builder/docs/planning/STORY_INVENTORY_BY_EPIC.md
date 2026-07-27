# Builder V1.2 Story Inventory Grouped by Epic

Status: `PROPOSED_AWAITING_HUMAN_CONFIRMATION`

- Stories: 69
- Primary obligation assignments: 410
- Step 4: `NOT_AUTHORIZED`
- Production implementation: `PROHIBITED_READINESS_FAIL`

## EP-01 — Governed Run Intake and Evidence Readiness

A Harness Architect can select exactly one compilation target, start or resume a constitutionally bounded run, lock target-specific evidence without source mutation, and receive an explicit readiness or saturation outcome before design decisions begin.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-01.01` Start and Resume One Target-Profiled Builder Run | the run has stable identity, explicit authority, replay-safe state, and target-specific required work | None | 15 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-01.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-01.02` Lock a Safe Target-Specific Evidence Workspace | source material is portable, safe to inspect, and protected from mutation | ST-01.01 | 10 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-01.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-01.03` Index Every Evidence Specimen with Provenance | later decisions can query complete evidence and distinguish observation, status, and provenance | ST-01.02 | 4 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-01.03:StoryCompletionReceipt:<artifact-hash>` |
| `ST-01.04` Decide Evidence Saturation Without Inventing Claims | the run proceeds, pauses, or blocks through an evidence-backed typed outcome | ST-01.03 | 4 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-01.04:StoryCompletionReceipt:<artifact-hash>` |
## EP-02 — Syntax-Grounded Understanding and Atomic Boundary

A reviewer can derive typed visual or conversational syntax evidence before meaning, distinguish observation from hypothesis, compare candidate product boundaries, and ratify one atomic Draft Harness Model with explicit uncertainty and wrong-boundary risk.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-02.01` Normalize Evidence into Typed Syntax Observations | reviewers can compare reliable geometry, components, turns, and evidence identities | ST-01.04 | 6 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-02.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-02.02` Build Spatial, Temporal, and Reading-Order Graphs | the candidate grammar is grounded in substrate-specific relationships rather than vague meaning | ST-02.01 | 4 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-02.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-02.03` Induce Grammar Only After Syntax Evidence | Visual Syntax First governs development discovery while unsupported meaning stays visibly provisional | ST-02.02 | 7 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-02.03:StoryCompletionReceipt:<artifact-hash>` |
| `ST-02.04` Compare Candidate Atomic Product Boundaries | human authority can see the consequence of each candidate before choosing the atomic product | ST-02.03 | 5 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-02.04:StoryCompletionReceipt:<artifact-hash>` |
| `ST-02.05` Ratify and Freeze the Draft Harness Boundary | downstream constitutional decisions start from an explicit, reviewable, and stable product boundary | ST-02.04 | 6 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-02.05:StoryCompletionReceipt:<artifact-hash>` |
## EP-03 — Human-Ratified Genesis and Canonical Harness Definition

Human authority can answer only dependency-ready constitutional questions, preserve the evidence and recommendation trail, freeze ratified decisions, and compile one provenance-rich canonical Harness IR into consistent human and machine artifacts.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-03.01` Ask Only Dependency-Ready Constitutional Questions | human attention is spent on the next consequential question with complete rationale | ST-01.04, ST-02.05 | 7 | `EVIDENCE_GATED` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-03.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-03.02` Record Human Authority and Resume Genesis Safely | human authority remains explicit, auditable, and recoverable across sessions | ST-03.01 | 8 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-03.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-03.03` Maintain One Provenance-Rich Canonical Harness IR | all downstream artifacts share one source of truth with explicit schema evolution and Activative lineage | ST-03.02 | 8 | `EVIDENCE_GATED` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-03.03:StoryCompletionReceipt:<artifact-hash>` |
| `ST-03.04` Compile Human and Machine Artifacts Deterministically | maintainers receive reproducible, hash-bound outputs without duplicated authority | ST-03.03 | 10 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-03.04:StoryCompletionReceipt:<artifact-hash>` |
| `ST-03.05` Enforce Constitutional Precedence Across Compiled Artifacts | lower-authority artifacts cannot override Constitution V1.1 or lose semantic lineage | ST-03.04 | 2 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-03.05:StoryCompletionReceipt:<artifact-hash>` |
## EP-04 — Owned Capability Graphs and Minimum Complete Context

A maintainer can see who or what owns every capability, how responsibility-centered modules and phases connect, what each handoff may change, and the minimum complete context required for reliable work.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-04.01` Assign Explicit Ownership to Every Required Capability | the design has accountable owners and no capability disappears between product intent and execution | ST-03.05 | 5 | `EVIDENCE_GATED` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-04.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-04.02` Compile Responsibility-Centered Modules with Test Seams | each module can change and be tested without recreating horizontal technical layers | ST-04.01 | 3 | `PLANNING_COMPLETE_IMPLEMENTATION_PROHIBITED` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-04.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-04.03` Order Work Through an Executable Phase Graph | the harness exposes what may run now, later, or safely in parallel | ST-04.02 | 3 | `PLANNING_COMPLETE_IMPLEMENTATION_PROHIBITED` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-04.03:StoryCompletionReceipt:<artifact-hash>` |
| `ST-04.04` Protect Typed Phase and Context Handoffs | downstream work receives complete inputs without silently rewriting upstream truth | ST-04.03 | 9 | `EVIDENCE_GATED` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-04.04:StoryCompletionReceipt:<artifact-hash>` |
| `ST-04.05` Compile Minimum Complete Context Without Silent Truncation | each phase receives the minimum complete context plus a complete manifest | ST-04.04 | 13 | `EVIDENCE_GATED` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-04.05:StoryCompletionReceipt:<artifact-hash>` |
## EP-05 — Reusable Evaluated Skills and Deterministic JIT Capsules

A maintainer can reuse, adapt, or justify new skills through capability-gap evidence, bind them to behavioral evaluation, and assemble deterministic phase-local capsules containing only the authority and context needed for the current task.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-05.01` Operate a Versioned Canonical Skill Registry | the team can distinguish stable reusable behavior from local adaptation and experimental capability | ST-04.05 | 5 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-05.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-05.02` Prove a Skill Is Needed Before Designing It | new skill work begins only where behavior evidence shows a real gap | ST-05.01 | 4 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-05.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-05.03` Package Portable Skills with Behavioral Anchors | skill behavior is attributable, maintainable, and reusable across compatible harnesses | ST-05.02 | 6 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-05.03:StoryCompletionReceipt:<artifact-hash>` |
| `ST-05.04` Assemble a Deterministic Phase-Local JIT Capsule | an agent receives exactly the evaluated authority and context needed for the current phase | ST-05.03 | 14 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-05.04:StoryCompletionReceipt:<artifact-hash>` |
| `ST-05.05` Pin and Dispose of Capsules Reproducibly | a phase can be replayed without accumulating hidden conversational state or stale capsule sediment | ST-05.04 | 3 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-05.05:StoryCompletionReceipt:<artifact-hash>` |
## EP-06 — Five-Category Activative Intelligence and Expression Compilation

A category steward can preserve one Shared Activative Core and compile category-native syntax, sequence, runtime, evaluation, and repair contracts for all five canonical categories, including first-class Conversational Activation / Human Expression profiles.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-06.01` Bind Every Harness to One of Five Canonical Categories | all five categories remain distinct while preserving shared meaning and atomic creative ownership | ST-02.05, ST-03.05, ST-04.05 | 13 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-06.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-06.02` Compile Category-Local Format and Performance Profiles | each format inherits the correct substrate grammar rather than acting as a cosmetic theme | ST-06.01 | 4 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-06.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-06.03` Compile Category-Native Syntax and Activative Sequencing | shared Activative meaning becomes category-native form without losing frozen rich-object lineage | ST-06.02 | 6 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-06.03:StoryCompletionReceipt:<artifact-hash>` |
| `ST-06.04` Own Category Runtime, Evaluation, Repair, and Migration Rules | each category can evolve without silently changing another category or inheriting certification | ST-06.03 | 4 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-06.04:StoryCompletionReceipt:<artifact-hash>` |
| `ST-06.05` Compile the Conversational Expression Feedback Chain | Public Comment, Reply or DM, ReelCast, and Interview profiles are first-class structural outputs while live execution stays external | ST-06.04 | 1 | `BLOCKED_PENDING_HUMAN_DECISION` | `CONVERSATIONAL_STRUCTURAL_SUPPORT_UNCERTIFIED` | `ST-06.05:StoryCompletionReceipt:<artifact-hash>` |
## EP-07 — Three-Target Product Compilation and Cross-Product Handoff

A cross-product architect can compile distinct Atomic Content Harness, Visual Asset Editor, and Content Asset Delegation Contract profiles from shared governance while preserving target-specific evidence, ownership, artifacts, evaluation, compatibility, and frozen semantic handoffs.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-07.01` Register Three Distinct Compilation Targets | one control plane can select the correct product outcome without flattening ownership or evidence needs | ST-03.05, ST-04.05, ST-06.05 | 3 | `EVIDENCE_GATED` | `THREE_TARGET_STRUCTURAL_SUPPORT_EXTERNAL_RUNTIME_EXCLUDED` | `ST-07.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-07.02` Compile a Target-Specific Atomic Content Harness | content-harness output preserves Activative ownership and its category-native contracts | ST-07.01 | 4 | `EVIDENCE_GATED` | `THREE_TARGET_STRUCTURAL_SUPPORT_EXTERNAL_RUNTIME_EXCLUDED` | `ST-07.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-07.03` Compile VAE and Delegation Handoffs Without Implementing Them | external products receive frozen, typed meaning while Builder stays within compile-validate-handoff ownership | ST-07.02 | 4 | `EVIDENCE_GATED` | `THREE_TARGET_STRUCTURAL_SUPPORT_EXTERNAL_RUNTIME_EXCLUDED` | `ST-07.03:StoryCompletionReceipt:<artifact-hash>` |
| `ST-07.04` Validate Target Artifacts, Gates, and Compatibility | each target can be reviewed and migrated independently with explicit certification scope | ST-07.03 | 4 | `EVIDENCE_GATED` | `THREE_TARGET_STRUCTURAL_SUPPORT_EXTERNAL_RUNTIME_EXCLUDED` | `ST-07.04:StoryCompletionReceipt:<artifact-hash>` |
## EP-08 — Behavioral Proof, Repair, and Readiness Authorization

Independent reviewers can measure whether the Builder, its skills, categories, profiles, and target artifacts improve behavior, reject wrong readings, repair only responsible layers, and issue immutable readiness or blocked authorization receipts.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-08.01` Measure Behavior Against Controls in Fresh Contexts | claimed behavioral improvements are attributable rather than prompt-history artifacts | ST-02.05, ST-03.05, ST-04.05, ST-05.05, ST-06.05, ST-07.04 | 6 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-08.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-08.02` Promote Maturity Only Through Protected Receipts | only the exact evaluated version can advance toward release | ST-08.01 | 9 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-08.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-08.03` Score Independent Dimensions and Controlled Mutations | quality dimensions remain visible and non-compensable rather than collapsing into one flattering score | ST-08.02 | 9 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-08.03:StoryCompletionReceipt:<artifact-hash>` |
| `ST-08.04` Diagnose Root Cause Before Selecting Repair | repair targets the responsible layer and preserves unaffected upstream truth | ST-08.03 | 5 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-08.04:StoryCompletionReceipt:<artifact-hash>` |
| `ST-08.05` Repair Selectively and Rerun Only Affected Regressions | the system can improve without restarting validated work or hiding recurring defects | ST-08.04 | 3 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-08.05:StoryCompletionReceipt:<artifact-hash>` |
| `ST-08.06` Issue Evidence-Backed Readiness and Authorization Receipts | implementation teams know exactly what is authorized and why | ST-08.05 | 10 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-08.06:StoryCompletionReceipt:<artifact-hash>` |
| `ST-08.07` Reject Wrong Readings and Evaluate Conversational Expression | role clarity, pattern interruption, prediction, payoff, affinity, anticipation, residue, anti-cliche, no-text survival, and rejection remain independently governed | ST-08.06 | 2 | `BLOCKED_PENDING_HUMAN_DECISION` | `CONVERSATIONAL_STRUCTURAL_SUPPORT_UNCERTIFIED` | `ST-08.07:StoryCompletionReceipt:<artifact-hash>` |
## EP-09 — Governed Builder Workflow Factory

An operator can route a Builder request through a versioned, actor-explicit workflow; run deterministic and agent work at isolated public seams; recover from bounded failures; and promote only workflows that pass end-to-end and fault tests.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-09.01` Compile an Actor-Explicit Builder Workflow | every request has reproducible routing and explicit responsibility | ST-01.04, ST-03.05, ST-04.05, ST-05.05, ST-06.05, ST-07.04, ST-08.07 | 9 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-09.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-09.02` Route Through a Manual Shadow Before Automation | automation begins from observed expert behavior and evaluated phase-local capsules | ST-09.01 | 5 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-09.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-09.03` Validate Node Outputs and Contain Failure Feedback | failures stay local, diagnosable, and unable to leak invalid output downstream | ST-09.02 | 9 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-09.03:StoryCompletionReceipt:<artifact-hash>` |
| `ST-09.04` Checkpoint, Isolate, and Resume Work Safely | the workflow can resume after failure without duplicating side effects or widening access | ST-09.03 | 12 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-09.04:StoryCompletionReceipt:<artifact-hash>` |
| `ST-09.05` Race Candidates and Route Compute Under Human Authority | compute is spent proportionally while consequential decisions stay human-governed | ST-09.04 | 6 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-09.05:StoryCompletionReceipt:<artifact-hash>` |
| `ST-09.06` Observe Queues and Prove Workflow Recovery | operators can see cost, latency, quality, interventions, and recovery behavior at public seams | ST-09.05 | 9 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-09.06:StoryCompletionReceipt:<artifact-hash>` |
| `ST-09.07` Promote, Migrate, Roll Back, and Hotfix Workflow Profiles | workflow changes remain reversible and operationally governed | ST-09.06 | 7 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-09.07:StoryCompletionReceipt:<artifact-hash>` |
| `ST-09.08` Measure Workflow Outcomes and Reject Monolithic Orchestration | the workflow remains an explicit, testable factory rather than an opaque agent prompt | ST-09.07 | 5 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-09.08:StoryCompletionReceipt:<artifact-hash>` |
## EP-10 — Evidence-Derived Human Control Tower

A human can supervise the full Builder run from one approved Control Tower, understand evidence and authority behind every status, inspect category or profile lineage and workflow state, and issue only governed commands without creating a second source of truth.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-10.01` Open a Trustworthy Run Index and Overview | the current target, category, stage, status, and next governed action are immediately understandable | ST-01.04, ST-03.05, ST-04.05, ST-05.05, ST-06.05, ST-07.04, ST-08.07, ST-09.08 | 6 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.02` Explore Phase, Context, and Dependency Graphs | the architect can trace what is ready, blocked, upstream, or affected without losing context | ST-10.01 | 3 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.03` Inspect Evidence and Syntax Behind Decisions | every critical claim can be inspected at its originating evidence and parse seam | ST-10.02 | 3 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.03:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.04` Review Genesis Decisions and Human Authority | constitutional authority remains understandable and resumable from the Control Tower | ST-10.03 | 2 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.04:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.05` Trace Skills, Recipes, and Runtime Capsules | the maintainer can explain which behavior and context entered a phase | ST-10.04 | 2 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.05:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.06` Inspect Ownership, Modules, and Contracts | responsibility and permitted mutation remain clear before change or handoff | ST-10.05 | 2 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.06:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.07` Judge Evaluations, Repairs, and Authorization Trajectory | the reviewer can see why readiness advanced, regressed, or remains blocked | ST-10.06 | 4 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.07:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.08` Monitor Workflow, Incidents, Cost, and Context | operational pressure and intervention needs are visible before they become silent failure | ST-10.07 | 3 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.08:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.09` Execute Governed Commands and Export Receipts | human actions remain least-privilege, conflict-aware, and auditable | ST-10.08 | 10 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.09:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.10` Use a Stable, Accessible, Evidence-Backed Shell | the Control Tower remains usable without becoming a second source of truth | ST-10.09 | 12 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.10:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.11` Preserve Workspace Context Across Inspectors and Layouts | dense operational review stays coherent across screen sizes and interaction modes | ST-10.10 | 5 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.11:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.12` Represent Loading, Empty, Stale, and Disconnected State Honestly | the interface communicates evidence age and availability without optimistic authority | ST-10.11 | 11 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.12:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.13` Contain Partial, Redacted, Failed, and Invalidated Projections | the interface preserves security and truth while exposing what can be retried or inspected | ST-10.12 | 6 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.13:StoryCompletionReceipt:<artifact-hash>` |
| `ST-10.14` Operate Large Collections Within Interaction Budgets | the interface remains responsive and measurable at Release 1 scale | ST-10.13 | 4 | `CONDITIONAL_EXTERNAL_DEPENDENCY` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-10.14:StoryCompletionReceipt:<artifact-hash>` |
## EP-11 — Traceable Development Capsule and Implementation Handoff

An implementation team can receive one versioned Development Capsule containing only justified scaffolding, typed contracts, fixtures, dependency ordering, acceptance evidence, and frozen authority needed to implement a complete vertical slice without inventing product decisions.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-11.01` Generate a Versioned Traceable Development Capsule | an implementation team receives complete authority without inventing missing product decisions | ST-03.05, ST-04.05, ST-05.05, ST-06.05, ST-07.04, ST-08.07, ST-09.08, ST-10.14 | 6 | `BLOCKED_PENDING_HUMAN_DECISION` | `IMPLEMENTATION_HANDOFF_PLANNING_ONLY` | `ST-11.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-11.02` Plan Dependency-Ordered Vertical Implementation Increments | implementation can deliver user-observable value without horizontal layer sequencing or future-story dependencies | ST-11.01 | 2 | `BLOCKED_PENDING_HUMAN_DECISION` | `IMPLEMENTATION_HANDOFF_PLANNING_ONLY` | `ST-11.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-11.03` Govern Implementation Deltas and Certification Feedback | validated authority can evolve without silent drift between planning and implementation | ST-11.02 | 2 | `BLOCKED_PENDING_HUMAN_DECISION` | `IMPLEMENTATION_HANDOFF_PLANNING_ONLY` | `ST-11.03:StoryCompletionReceipt:<artifact-hash>` |
## EP-12 — Brownfield Migration and Release 1 Reference Proof

The team can preserve proven V2.1 behavior, migrate only with evidence and receipts, dual-compile eligible targets, and prove the complete Builder spine through one Format 02 reference path without overstating category or target certification.

| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |
|---|---|---|---:|---|---|---|
| `ST-12.01` Inventory and Map Proven V2.1 Behavior | migration starts from proven assets rather than a greenfield rewrite | ST-06.05, ST-07.04, ST-08.07, ST-09.08, ST-10.14, ST-11.03 | 4 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-12.01:StoryCompletionReceipt:<artifact-hash>` |
| `ST-12.02` Dual-Compile and Migrate Through Regression Receipts | retained behavior changes only through evidence-backed, reversible increments | ST-12.01 | 6 | `BLOCKED_PENDING_HUMAN_DECISION` | `RELEASE_1_FORMAT_02_REFERENCE_SUPPORT` | `ST-12.02:StoryCompletionReceipt:<artifact-hash>` |
| `ST-12.03` Prove the Complete Builder Spine Through Format 02 | Release 1 demonstrates a coherent vertical product outcome instead of disconnected infrastructure | ST-12.02 | 3 | `BLOCKED_PENDING_HUMAN_DECISION` | `FORMAT_02_REFERENCE_PATH_PROOF` | `ST-12.03:StoryCompletionReceipt:<artifact-hash>` |
| `ST-12.04` Publish Bounded Certification Claims Across Categories and Targets | proven Release 1 scope is explicit while unproven transfer outcomes remain uncertified | ST-12.03 | 4 | `BLOCKED_PENDING_HUMAN_DECISION` | `FORMAT_02_CERTIFICATION_SCOPE_AND_GENERAL_DEFERRAL` | `ST-12.04:StoryCompletionReceipt:<artifact-hash>` |
