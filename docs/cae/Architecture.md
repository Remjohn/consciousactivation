# CAE Architecture — Canonical Physical Architecture & Convergence Map

**Document ID:** `CAE-ARCH-001`  
**Status:** Normative physical architecture map for implementation  
**Scope:** Conscious Activation Engine product, operator surface, runtime, causal pipeline, persistence, evidence, agents, authorization, release, distribution, outcomes, and certification  
**Authority relationship:** This document translates the Product Brief, five PRD modules, Functional Requirements, and Master 57-Question Canon into a physical system map. It does not replace those authorities and does not itself prove implementation.  
**Primary principle:** Architecture must describe the system that makes the governed Operator experience and the 57 canonical decisions physically true.

---

## 1. Purpose

The Conscious Activation Engine is an evidence-grounded production system that transforms audience intelligence, subject interviews, source media, collision hypotheses, and operator decisions into broadcast-grade multi-format narrative activations.

The architecture must unify two dimensions:

1. **Causal product architecture:** the 17-stage activation lifecycle from Audience Context through Memory Write-back.
2. **Production execution architecture:** the runtime substrate that provides dispatch, state, persistence, agent execution, concurrency, security, provenance, receipts, live execution, and production authorization.

The architecture exists to prevent those dimensions from becoming separate systems.

The product contract says downstream realization cannot legitimately invent upstream meaning. The runtime contract says production execution must be real, governed, stateful, recoverable, and auditable. The UI contract says the Operator must be able to understand and control that system without becoming responsible for its internal infrastructure.

Therefore the architectural objective is:

**one causal model, one runtime state model, one authority model, one provenance model, one release model, many programs and many interaction surfaces.**

---

## 2. Architectural Authority

The hierarchy is:

```text
Master 57-Question Canon
        ↓
Product Brief
        ↓
PRD Modules
        ↓
Functional Requirements
        ↓
UI.md + Architecture.md
        ↓
Mandates
        ↓
Implementation
        ↓
Executable Evidence
```

The Canon determines what has been decided.

The Product Brief defines the product-level synthesis.

The PRDs define capability contracts.

The Functional Requirements define testable requirements.

UI.md defines what the Operator must be able to experience and control.

Architecture.md maps those contracts to physical components and boundaries.

Mandates authorize bounded implementation.

Code and executable evidence determine what is actually implemented.

Architecture.md must never convert a desired architecture into a false implementation claim.

---

## 3. System Boundary

The physical CAE system is composed of these major layers:

```text
Operator / External Interaction
            │
            ▼
      Web / API / Adapters
            │
            ▼
     Canonical Runtime
            │
   ┌────────┼─────────┐
   ▼        ▼         ▼
Programs  State     Authority
          Runtime    & Gates
   │        │         │
   └────────┼─────────┘
            ▼
     Agent / Workflow
        Execution
            │
   ┌────────┼─────────┐
   ▼        ▼         ▼
Evidence  Assets   External Tools
            │
            ▼
      Persistence /
      Receipts /
      Release
            │
            ▼
      Distribution
            │
            ▼
      Outcomes /
       Learning
```

The web application is a presentation and control layer. The API is a canonical boundary. The runtime is the authoritative execution substrate. Programs declare work. Agents perform bounded cognitive tasks. Persistence records state and artifacts. Receipts establish durable evidence of transitions. Release artifacts freeze what may leave the system.

---

## 4. Product Causal Architecture

The canonical product lifecycle contains 17 ordered stages:

1. Audience Context
2. Research & Evidence
3. Subject Baseline
4. Narrative Architecture
5. Declarative PreProduction
6. Structured Elicitation
7. Evidence Capture
8. Collision Analysis
9. Canonicalization
10. Composition
11. AIR Rendering
12. Human Authorization
13. Release Manifest
14. External Distribution
15. Outcome Measurement
16. Verification & Traceability
17. Memory Write-back

The order is causal, not cosmetic.

A downstream node cannot execute as though an upstream object existed when its required inputs, digests, evidence predicates, or authority conditions are absent.

Every stage therefore has five architectural concerns:

- declared inputs
- declared outputs
- authoritative artifacts
- admission predicates
- downstream lineage

The runtime enforces these relationships; the UI exposes them.

---

## 5. Capability Pillars

The five PRD pillars map into the physical architecture as follows.

### PIL-01 — Audience & Research Intelligence

Provides structured audience layers, convergence, research briefs, and strategic inputs.

### PIL-02 — Question & Interview Elicitation Intelligence

Provides Activatives, Elicitation Units, Subject Constitution, preparation graphs, interview programs, and pre-production snapshots.

### PIL-03 — Evidence & Receipt Provenance

Provides sovereign source media handling, temporal anchors, verbatim capture, reactions, evidence predicates, collisions, expression moments, and yield gates.

### PIL-04 — Editorial Composition & Storyboard Production

Provides composition, storyboard, AIR rendering, release manifests, and execution-only distribution.

### PIL-05 — Multi-Agent Runtime, Security & Certification

Provides dispatch, state, leases, CAS, WAL, context projection, tenant fencing, sandboxing, economics, model resilience, replay, telemetry, benchmarks, and production release sealing.

The pillars are not independent applications. They converge on the same runtime state, identifiers, provenance chain, and authority system.

---

## 6. Runtime Architecture

The repository's `ca_runtime` package is the central execution substrate.

Its major responsibilities include:

- program registration
- manifest resolution
- operator execution
- state management
- agent invocation
- context projection
- workflow dispatch
- gates
- recovery
- receipts
- tenancy
- observability

The runtime must provide infrastructure without embedding program-specific semantic decisions that belong in program contracts.

The key boundary is:

```text
Program contract
    ↓
declares what should happen
    ↓
Runtime
    ↓
enforces how execution occurs safely
```

Programs should not independently reinvent lease acquisition, authorization persistence, state hashing, tenant fencing, or receipt creation.

Likewise, the runtime should not invent campaign meaning.

---

## 7. Program and Manifest Architecture

A CAE program is a declared executable unit.

A program manifest describes, as applicable:

- identity
- revision
- inputs
- preconditions
- outputs
- state machine
- agents
- skills
- operations
- tools
- hooks
- evaluations
- operator gates
- recovery
- receipts
- dependencies

The repository already uses program manifests for important programs such as editorial storyboard and interview semantic execution.

The manifest is the program contract.

The runtime resolves and executes the declared contract.

This supports the production rule that real execution must resolve production agents and compiled skills from the manifest rather than using synthetic adapters as production behavior.

---

## 8. Operator Architecture

The Operator application is a control plane over the runtime.

The invariant is:

**One program state, many interaction surfaces.**

The web console, future Mini Apps, Slack, Telegram, and other adapters must all operate against the same canonical runtime.

No interaction surface may create:

- shadow campaign state
- independent approval semantics
- alternative identifiers
- separate release state
- local authority decisions

The Operator interacts with production objects such as Campaign, Subject, Interview, Evidence, Candidate, Composition, Release, and Outcome.

The runtime interacts with aggregates, state versions, leases, receipts, programs, agents, and persistence.

The UI translates between these views without creating a second system.

---

## 9. Campaign Architecture

Campaign is the primary operational aggregate.

A campaign binds, directly or indirectly:

- workspace
- operator
- source package
- harness/program
- output targets
- objective
- initial seed
- taste direction
- format profile
- autonomy policy
- budget
- execution identity
- revisions
- artifacts
- state
- receipts

Campaign creation must be idempotent.

Once created, a campaign's execution history is append-oriented and versioned rather than overwritten.

The Campaign Control Tower is the primary projection of this aggregate for human operators.

---

## 10. Causal Data Flow

The principal information flow is:

```text
Audience Context
      ↓
Research / Evidence
      ↓
Guest Genesis Semantic Territory
      +
Audience Tensions
      ↓
Converged Context
      ↓
Subject Baseline
      ↓
Narrative Architecture
      ↓
Format / Archetype Matchmaking
      ↓
Content Portfolio
      ↓
Pre-Production Snapshot
      ↓
Activatives
      ↓
Elicitation Units
      ↓
Interview
      ↓
Sovereign Source Media
      ↓
Evidence Moments
      ↓
Collision Analysis
      ↓
Canonicalization
      ↓
Expression Moments
      ↓
Composition
      ↓
AIR Rendering
      ↓
Human Authorization
      ↓
Release Manifest
      ↓
External Distribution
      ↓
Outcome Measurement
      ↓
Verification
      ↓
Learning Candidate
      ↓
Governed Memory Promotion
```

The system must retain explicit lineage between these objects.

---

## 11. Audience and Research Architecture

Audience Context is divided into three immutable layers:

- Market Macro Signals
- Segment Cultural Archetypes
- Live Audience Tensions

These are separately versioned/digested.

Research is a structured causal object rather than a free-form note.

Research claims must carry their required provenance, authority information, and falsification conditions.

The convergence layer combines Guest Genesis Semantic Territory with Audience Tensions before narrative generation.

Narrative generation must fail closed if the required convergence is absent or invalid.

---

## 12. Subject and Elicitation Architecture

The Subject Constitution is formed from source/interview evidence and governed by an exception lifecycle.

Once signed, the baseline is immutable.

Changes occur through versioned operator amendment packets.

Activatives are derived strategic execution objects. They are not arbitrary prompts manually inserted downstream.

Elicitation Units maintain explicit many-to-many relationships with Activatives.

An Elicitation Unit carries an objective, desired evidence, questions, follow-ups, depth, fallback, and exit condition.

Interview completion is evaluated through holistic yield sufficiency.

The architecture therefore separates:

```text
Strategic intent
     ↓
Activative
     ↓
Elicitation Unit
     ↓
Human interview
     ↓
Physical evidence
```

rather than treating the interview as a generic question-answering step.

---

## 13. Pre-Production Snapshot

Before physical evidence acquisition and downstream execution, the system creates a sealed Pre-Production Snapshot.

It freezes relevant upstream state including:

- research
- hypotheses
- content portfolio
- elicitation guides
- format requirements
- applicable policy
- required execution configuration

The snapshot is cryptographically sealed.

If required inputs no longer match the sealed snapshot, execution initialization must fail rather than silently continuing against changed upstream meaning.

---

## 14. Evidence Architecture

Source media bytes are sovereign.

Transcripts, diarization, LLM observations, summaries, and semantic extractions are derivative representations.

The source package must retain immutable source identity and digest.

Evidence moments require precise temporal anchoring.

The architecture must preserve:

```text
source media
   ↓
media identity/hash
   ↓
temporal span
   ↓
verbatim transcript
   ↓
evidence classification
   ↓
evidence predicate
   ↓
semantic observation
```

Verbatim spoken capture is not editorial prose.

Disfluencies, cadence, exact wording, and character-exact spans remain distinguishable from semantic interpretation.

Cross-window transcript processing must preserve continuity across chunk boundaries.

---

## 15. Evidence Admission

Evidence admission is a multi-dimensional predicate.

It must not collapse to a single confidence number.

The relevant dimensions include, as defined by the product contract:

- fidelity
- epistemic legality
- identity fit
- domain fit

Only admitted evidence can become a valid upstream dependency for downstream composition.

An evidence object should therefore carry its admission status and the reasons for failure.

---

## 16. Collision Architecture

A Collision is a multi-pole semantic relation between:

- Guest/Subject DNA
- Audience Tension
- World Signal

It expresses a grounded paradox, latent truth, or meaningful tension.

Collision discovery may be autonomous, but the architecture must enforce the appropriate operator gate before downstream portfolio composition when the policy requires it.

A collision should retain:

- grounding
- source evidence
- tension vectors
- falsification conditions
- receipt
- revision
- downstream dependencies

The UI exposes this causal structure; the runtime enforces admission.

---

## 17. Yield and Expression Architecture

Yield gating determines whether acquired evidence is sufficient for the declared Content Portfolio.

If evidence yield is insufficient, downstream costly production must halt fail closed.

Expression Moments are the admissible units from which downstream composition can be constructed.

They retain lineage back to evidence.

This produces:

```text
Evidence
   ↓
Admitted evidence
   ↓
Collision / interpretation
   ↓
Expression Moment
   ↓
Composition
```

The system must not allow a downstream writer or composer to manufacture factual content merely because the desired format needs more material.

---

## 18. Composition Architecture

Composition is downstream realization.

Every substantive factual or semantic claim must be anchored to admitted upstream evidence or explicitly declared as an authorized connective transformation.

The composition system should retain:

- evidence references
- expression moments
- narrative purpose
- composition revision
- validation state
- artifact identity
- downstream release dependencies

This is the physical implementation of the supreme causal law.

---

## 19. Rendering and Release Architecture

AIR rendering produces executable media/artifact outputs.

Rendering does not create semantic authority.

The Release Manifest freezes the release package.

It should bind:

- artifact identities
- artifact hashes
- evidence lineage
- composition revisions
- authorization decisions
- relevant policy revision
- release metadata
- integrity/seal

External Distribution consumes the release package.

Distribution adapters may perform required container/codec or destination transformations but cannot alter the semantic content.

---

## 20. Authority Architecture

Authority must be separated into distinct concepts.

### Semantic authority

Determines what the product means and what decisions have been established.

### Runtime authority

Determines what state transitions the execution substrate may perform.

### Mutation authority

Determines who or what may change an object.

### Promotion authority

Determines who may move an object into a more consequential lifecycle state.

### Evidence authority

Determines what counts as admissible support.

An artifact does not become authoritative merely because it exists in the repository or database.

A model output is not automatically a source of truth.

A UI state is not runtime authority.

A notification is not an approval.

---

## 21. Authorization Architecture

Campaign policy can configure delegation modes such as YOLO, Checkpoint, Strict, or Custom, subject to constitutional invariants.

Policies are versioned declarative packages.

Active executions bind to the policy revision under which they were authorized.

Policy updates apply prospectively.

Every consequential human authorization produces a durable authorization decision receipt containing actor identity, object/revision information, and the required integrity data.

The runtime, not the UI, determines whether the approval is valid.

---

## 22. State Architecture

Runtime state should be represented as versioned authoritative state.

The fundamental relationship is:

```text
aggregate
   ↓
version
   ↓
state
   ↓
transition
   ↓
receipt
   ↓
next version
```

State mutation must be concurrency-safe.

Where CAS is required, the architectural contract is an atomic conditional update against the expected version, with success determined by the affected-row count.

The system must distinguish:

- expected version mismatch
- missing aggregate
- duplicate request
- invalid transition
- authorization failure
- stale decision
- recovery conflict

---

## 23. Execution Dispatch Architecture

Production execution requires two-phase dispatch.

### Phase 1

Register the execution aggregate at its initial version and enqueue the execution lease.

### Phase 2

Acquire the lease atomically, verify expected state, refresh required context, and invoke the declared workflow.

The lease prevents competing workers from simultaneously owning the same execution.

The architecture must support crash/retry behavior without producing ambiguous duplicate execution.

Synthetic deterministic adapters may remain useful for tests where explicitly permitted, but production execution must use the declared real workflow/agent dispatch path.

---

## 24. Agent Architecture

Agents are bounded cognitive workers, not authority systems.

A production workflow resolves agents from the program manifest and supplies only the context declared for the active node.

Context projection must:

- expose only declared inputs
- mask fields outside the active authority lane
- preserve state/hash integrity
- prevent accidental access to unrelated aggregate data

Agent output becomes a candidate or transformation result that must still pass schema, policy, evidence, and state validation.

---

## 25. Persistence Architecture

SQLite is the current core persistence mechanism.

Production persistence must support:

- WAL mode
- busy timeout
- connection management
- migrations
- aggregate state
- append-oriented history
- receipts
- artifact metadata
- release metadata
- tenant/workspace isolation

Migrations require an append-only schema migration ledger.

Health checks should verify that the persistence layer is operational rather than merely that the process is alive.

---

## 26. Receipt and Integrity Architecture

Every consequential transition should produce durable receipt evidence.

The Product Brief currently describes parent-receipt chaining and replay verification.

Before implementation of the final cryptographic layer, the architecture must distinguish a simple hash chain from a true Merkle tree and specify the canonical serialization of receipt payloads.

The intended structure is:

```text
transition
   ↓
canonical payload
   ↓
digest
   ↓
parent relationship
   ↓
receipt
```

Receipt fields must be deterministic and sufficient to establish:

- actor
- operation
- object
- revision/version
- parent relationship
- timestamp/sequence as required
- canonical payload digest
- resulting state/digest
- authorization context

No UI event alone constitutes a receipt.

---

## 27. Tenant and Security Architecture

Workspace identity is part of the security boundary.

Every request and execution must remain fenced to its authorized workspace/tenant.

The architecture must protect:

- campaign state
- source media
- evidence
- credentials
- tools
- artifacts
- receipts
- release packages

Tool execution must be sandboxed according to the production policy.

Economic controls such as spend ceilings must be enforced by the runtime rather than displayed merely as UI warnings.

---

## 28. Model Resilience and Evaluation

Model invocation is an infrastructure dependency with failure modes.

The runtime must support the configured resilience behavior, including retry/fallback policies where authorized.

Model output is not considered successful merely because a provider returned text.

Success requires:

- valid invocation
- schema validity
- policy validity
- evidence validity where required
- state transition validity
- receipt persistence

CSEB/golden benchmark evaluation provides a separate production-readiness signal from ordinary functional tests.

---

## 29. Live Execution Architecture

Live execution must be materially different from synthetic test execution.

A live proof must demonstrate:

- real worker/lease acquisition
- real model inference
- actual program execution
- gate suspension
- human approval where required
- receipt persistence
- replay behavior
- non-synthetic execution identity

The CLI and API live paths must converge on the same runtime semantics.

The UI must display the real state produced by that execution rather than simulating progress.

---

## 30. Production Certification

Production authorization must be dynamically derived from verifiable release evidence.

The desired architecture uses a signed `ProductionReleaseSeal` or equivalent authoritative release proof.

The system should not claim:

`production_authorized: true`

merely because a configuration file or document says so.

Certification is a state backed by evidence.

The distinction is:

```text
Specified
   ↓
Implemented
   ↓
Tested
   ↓
Integration Verified
   ↓
Live Verified
   ↓
Production Verified
   ↓
Certified
   ↓
Promoted
```

Documentation must not collapse these states.

---

## 31. UI and Runtime Boundary

UI.md defines operator-facing behavior.

Architecture.md defines the runtime that supports it.

The boundary is:

```text
UI
 ↓
API / canonical command
 ↓
Authorization / validation
 ↓
Runtime transition
 ↓
Persistence
 ↓
Receipt
 ↓
Event/projection
 ↓
UI refresh
```

The browser must not bypass the canonical command layer.

A stale UI action must fail safely.

A successful action must be observable from the authoritative runtime state.

---

## 32. External Interaction Adapters

Slack, Telegram, Mini Apps, and future channels are adapters.

They may:

- notify
- summarize
- request a decision
- display evidence
- initiate a typed action

They may not:

- create alternative campaign state
- bypass authority
- invent approval semantics
- maintain an independent release lifecycle

All roads return to the canonical runtime.

---

## 33. Observability Architecture

Observability must expose production behavior without becoming a second source of truth.

Required operational dimensions include:

- execution identity
- campaign
- program
- stage
- worker/lease
- state version
- policy revision
- model/provider
- duration
- cost
- error
- retry
- gate
- operator decision
- receipt

Operator-facing views should translate these into actionable production information.

Forensic views may expose the raw details.

---

## 34. Outcome and Learning Architecture

Outcome telemetry must remain attributable to exact production objects.

Metrics should link to:

- campaign objective
- audience/tension hypothesis
- creative revision
- release manifest
- distribution event

Raw outcome observations are not automatically canonical memory.

They become Learning Candidates subject to evidence, attribution, and confidence requirements.

Memory promotion is therefore a governed state transition, not an automatic database write.

---

## 35. Architecture of Failure

The system is designed to fail closed at consequential boundaries.

Important fail-closed boundaries include:

- missing upstream convergence
- invalid pre-production snapshot
- inadmissible evidence
- insufficient yield
- unanchored semantic invention
- stale approval
- authorization failure
- policy mismatch
- lease conflict
- CAS failure
- tenant mismatch
- sandbox violation
- release integrity failure
- production seal failure

Every failure should preserve enough state to explain:

1. what failed
2. why
3. which invariant was involved
4. what object was affected
5. what recovery paths exist
6. whether retry is safe

---

## 36. Physical Repository Mapping

The current repository provides major architectural surfaces:

### Web

`apps/web`

Owns operator presentation, campaign workflows, Control Tower views, interaction hooks, and API-facing types.

### API

`api`

Owns HTTP boundaries and runtime-facing routes.

### Runtime

`packages/ca_runtime`

Owns execution, program operation, state, agent invocation, registry, context projection, gates, recovery, and runtime infrastructure.

### Intelligence

`cae_collision_intelligence`

Owns domain-level collision, evidence, verification, and composition-related intelligence.

### Programs

`programs/*`

Own declared program manifests and program-specific contracts.

### Pipeline/services

`services/pipeline/*` and related service domains

Own pipeline/application concerns, artifact processing, distribution, and related production services.

Architecture mandates should identify the correct physical ownership rather than allowing every requirement to accumulate inside one runtime file.

---

## 37. Dependency Direction

The preferred dependency direction is:

```text
Product contract
      ↓
Program contract
      ↓
Runtime execution
      ↓
Persistence / infrastructure
```

The UI depends on API contracts and runtime projections.

The runtime does not depend on the UI.

Program semantics should not depend on browser behavior.

Persistence should not encode presentation logic.

External adapters should not own campaign truth.

This direction keeps the system convergent as new surfaces are added.

---

## 38. 57-Question Convergence Model

The 57 questions form two tightly coupled sets.

### Questions 01–33

These establish the causal product architecture:

- audience
- convergence
- subject
- causal ordering
- format/archetype
- elicitation
- activatives
- portfolio
- preparation graph
- research
- snapshot
- source media
- temporal anchoring
- continuity
- verbatim capture
- collisions
- evidence admission
- context hierarchy
- expression moments
- reactions
- anchoring
- yield
- authorization
- policy
- prospective policy
- no invention
- release
- distribution
- outcomes
- memory
- verification

### Questions 34–57

These establish the production engine:

- atomic dispatch
- real workflow dispatch
- context projection
- deterministic state
- tenant fencing
- tool sandboxing
- economic controls
- model resilience
- receipts
- replay
- CAS
- leases
- telemetry
- collision gates
- WAL concurrency
- live execution
- production authorization

The architecture must connect these two sets rather than treating them as separate backlogs.

---

## 39. Mandate Execution Model

Every mandate should map to:

- one or more canonical questions
- one architectural node
- one or more physical repository surfaces
- dependencies
- authority boundary
- expected state transition
- evidence standard
- tests
- recovery path

A mandate must never be allowed to redesign the architecture implicitly.

If a mandate discovers that the physical repository cannot satisfy its contract without architectural change, that collision must be surfaced explicitly rather than solved by silent local invention.

---

## 40. Architecture-to-Mandate Traceability

The eventual 57-mandate map should follow this pattern:

```text
Q01 → Audience architecture → audience contracts/state → M01
Q02 → Context convergence → convergence program → M02
...
Q34 → Atomic dispatch → operator/state runtime → M34
...
Q56 → Live execution → live harness/API/CLI → M56
Q57 → Production seal → release/health/certification → M57
```

One question may require several implementation mandates. Several questions may share one physical implementation surface.

The mapping must preserve both relationships.

---

## 41. Current-State vs Target-State Discipline

Architecture.md distinguishes:

### CURRENT

What is physically present in the repository now.

### TARGET

What the 57-question canon requires the repository to become.

### EVIDENCED

What has been proven by executable evidence.

This distinction is mandatory because the Product Brief and Canon contain production-authorized language while the repository itself may still contain implementation gaps.

A document statement cannot substitute for runtime proof.

---

## 42. Definition of Architectural Completion

Architecture is complete when a competent implementation agent can determine:

- where each product capability belongs
- what object owns each piece of state
- which layer is authoritative
- how data moves through the causal pipeline
- where operator authority enters
- where evidence is admitted
- where releases are sealed
- how runtime state changes
- how concurrency is controlled
- how receipts are generated
- how failures recover
- how live execution differs from synthetic execution
- how production authorization is proven
- which physical repository surfaces must change for each mandate

The architecture document is therefore a map for implementation, not merely an explanation of concepts.

---

## 43. Final Architectural Principle

CAE must converge on a single system:

```text
ONE CAUSAL PIPELINE
ONE RUNTIME
ONE STATE MODEL
ONE AUTHORITY MODEL
ONE PROVENANCE CHAIN
ONE RELEASE MODEL
ONE PRODUCTION HISTORY

MANY PROGRAMS
MANY AGENTS
MANY VIEWS
MANY INTERACTION CHANNELS
```

The Operator controls the system through governed actions.

Programs define executable work.

Agents perform bounded cognitive operations.

Runtime enforces state, authority, concurrency, security, and recovery.

Evidence establishes what may be claimed.

Receipts establish what happened.

Release manifests establish what may leave the system.

Outcomes establish what happened after release.

Memory promotion establishes what may become durable learning.

Nothing downstream is permitted to silently become the source of upstream meaning.

That is the architecture the 57 mandates must converge toward.
