# CAE UI — Operator Experience & Control Surface Contract

**Document ID:** `CAE-UI-001`  
**Status:** Normative product/UI contract for implementation  
**Scope:** Operator web application and equivalent governed interaction surfaces  
**Authority relationship:** Derived from the CAE Product Brief, the 57-Question Decision & Convergence Canon, the five PRD modules, the Functional Requirements matrix, and the existing CAE web application.  
**Core law:** The UI is a control surface over the canonical runtime. It is not a second execution engine, a shadow state store, or an alternative authority system.

---

## 1. Purpose

The Conscious Activation Engine is operated by a human Operator who must continuously understand what CAE is doing, why it is doing it, what evidence supports the current recommendation, what is blocked, and what consequence follows from a decision.

The UI therefore exists to compress operational complexity without compressing away decision-critical information.

The Operator must be able to move through the complete CAE lifecycle:

**discover → inspect → configure → run → monitor → inspect evidence → resolve exceptions → approve/reject/repair → release → audit → learn.**

The interface must represent the canonical 17-stage causal activation pipeline and the production runtime beneath it. It must never create an alternate interpretation of campaign state.

The Product Brief defines CAE as a governed evidence transformation engine whose supreme causal law is that downstream realization cannot invent upstream meaning. The UI must make that law operationally visible: evidence, provenance, authority, version, and release state must remain inspectable at the point where decisions are made.

---

## 2. Product Definition of the Operator Experience

The Operator application is not a dashboard placed on top of CAE. It is the control surface through which human authority is exercised over the canonical production runtime.

The primary Operator manages campaigns and workspaces, coordinates interviews, inspects evidence, resolves recommendations, handles exceptions, and authorizes consequential transitions.

The UI succeeds when an Operator can answer, without consulting backend logs:

1. What is CAE currently doing?
2. What stage of the causal pipeline is active?
3. What object is waiting for me?
4. Why is it waiting?
5. What evidence supports the recommendation?
6. Which upstream objects produced it?
7. What policy and authority apply?
8. What will happen if I approve?
9. What will happen if I reject?
10. What can be repaired without invalidating the causal chain?
11. Which exact revision am I looking at?
12. Can I reconstruct what happened afterward?

The interface should optimize **decision latency and decision quality**, not raw click count. Automation should remove repetitive navigation and data handling, while preserving the information required for sound human judgment.

---

## 3. Constitutional UI Invariants

### UI-001 — Runtime authority

The runtime is authoritative. Browser state, React state, cached query state, optimistic UI state, notification state, and chat state are projections or interaction mechanisms only.

### UI-002 — One state, many surfaces

There is one campaign state, one authority model, one provenance chain, one release state, and one canonical production history. Web, chat, Mini App, and other future surfaces must converge on the same runtime identifiers and transitions.

### UI-003 — Typed consequential actions

The canonical operator actions are:

`DISCOVER`, `INSPECT`, `RUN`, `PAUSE`, `RESUME`, `APPROVE`, `REJECT`, `REPAIR`, `SHIP`, `EXPORT_AUDIT`.

These are not decorative buttons. Each corresponds to a governed runtime operation with preconditions, authorization, persistence, and evidence.

### UI-004 — No hidden approval semantics

A UI control must never create a local approval flag and assume that approval occurred. Approval is a runtime state transition producing its authoritative decision receipt.

### UI-005 — Freshness before authority

An approval is valid only against the exact object revision the Operator inspected. If the object changed after inspection, the UI must force reinspection or the runtime must reject the stale decision.

### UI-006 — Fail-closed presentation

When runtime policy or evidence gates block execution, the UI must communicate the actual contract failure and expose only permitted next actions. It must not disguise a governance failure as a generic AI error.

### UI-007 — Evidence before polish

Where a consequential creative decision is being reviewed, provenance and evidence must be accessible before or alongside visual polish. A beautiful artifact must never obscure the reason it is admissible.

### UI-008 — Natural language is not authority

Natural-language instructions may be interpreted into structured proposals, but the resulting action must still pass through the canonical runtime command and authority model.

---

## 4. Operator Mental Model

The Operator should think in production objects rather than infrastructure.

Primary objects are:

- Campaign
- Subject
- Audience Context
- Research Brief
- Narrative Plan
- Pre-Production Plan
- Activative
- Elicitation Unit
- Interview
- Evidence
- Collision
- Candidate
- Expression Moment
- Storyboard
- Composition
- Render
- QA result
- Approval
- Release Manifest
- Outcome
- Learning Candidate

The Operator should not need to understand workers, Python modules, database tables, agent classes, queues, or internal service boundaries to complete normal production work.

Those details may be exposed through progressive disclosure when forensic inspection is required.

---

## 5. Primary Navigation

The UI should organize around a workspace/campaign control plane.

Recommended top-level structure:

1. **Workspaces**
2. **Campaigns**
3. **Attention / Exceptions**
4. **Evidence**
5. **Releases**
6. **Audit**
7. **Settings / Policy**

A campaign becomes the primary operational workspace once created.

The current repository already contains a Campaign List, Campaign New flow, Campaign Detail page, Control Tower, Run Graph, Timeline, Exception Queue, and Revision Composer. These are retained as the physical foundation rather than replaced with a competing navigation model.

---

## 6. Campaign Creation

Campaign creation establishes the production contract before execution.

The existing campaign creation surface already captures:

- source package
- harness
- output targets
- objective
- initial seed
- taste direction
- budget
- autonomy mode
- format profile
- operator
- workspace
- project
- idempotency key

The UI should preserve this conceptual sequence:

### Step 1 — Source

Identify the sovereign source package or interview package.

### Step 2 — Execution contract

Select the harness/program and output targets.

### Step 3 — Objective

Declare objective, seed, taste direction, and other strategic inputs.

### Step 4 — Governance

Select workspace, operator, autonomy/delegation policy, budget and relevant policy configuration.

### Step 5 — Review

Present a complete launch summary before creating the campaign.

### Step 6 — Launch

Create the governed campaign object through the canonical API.

Launch must not silently mutate an existing execution. It creates a new authoritative campaign/run identity and is protected by idempotency.

---

## 7. Campaign Control Tower

The Campaign Control Tower is the main operator workspace.

It should expose, at minimum:

- campaign identity
- current lifecycle state
- current causal stage
- progress
- active run
- required decisions
- blockers
- latest evidence
- latest artifacts
- exceptions
- action rail
- revision state
- release readiness

The current web implementation already establishes the Control Tower composition with:

- Campaign Header
- Run Progress Gauge
- Action Rail
- Run Graph
- Timeline
- Exception Queue
- Revision Composer

and tabs for:

- Overview
- Run Graph
- Timeline
- Exceptions
- Revise

This existing shape should be treated as the baseline UI architecture.

---

## 8. The 17-Stage Pipeline View

The Operator must be able to understand the complete causal lifecycle:

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

The pipeline visualization is not merely a progress bar.

Each stage must expose:

- state
- readiness
- inputs
- outputs
- evidence
- blockers
- relevant policy
- required operator action
- lineage
- revision
- next permitted transition

The Operator should be able to answer: **“Why can’t the campaign move forward?”**

---

## 9. Preparation Graph

Pre-production must expose an interactive, parameter-sensitive preparation graph.

The graph may be edited before execution. Every meaningful operator adjustment creates a new immutable graph revision.

Once an execution begins, the active graph is immutable.

The UI must therefore distinguish:

- Draft graph
- Candidate revision
- Sealed pre-production snapshot
- Active execution graph
- Historical graph revision

An active run must never appear to change because an Operator edited the preparation view.

The graph should display dependencies between audience context, research, hypotheses, narrative, portfolio, elicitation, and downstream production.

---

## 10. Audience, Research, and Narrative Inspection

Audience context is not an unstructured note. The Operator should see the three distinct layers:

- Market Macro Signals
- Segment Cultural Archetypes
- Live Audience Tensions

Each layer should expose its own revision/digest and provenance.

Research should be presented as a structured causal input, including citation provenance, authority tier, and falsification conditions where applicable.

The Operator should be able to inspect the convergence between Guest Genesis Semantic Territory and Audience Tensions before narrative work becomes executable.

Narrative architecture should visibly show which upstream objects it depends upon.

---

## 11. Subject Constitution

The Subject Baseline is derived from source/interview evidence and becomes immutable once signed.

The normal UI should show:

- current subject constitution
- source evidence
- voice characteristics
- boundaries
- confidence/validation state
- revision
- exceptions

If voice drift or forbidden-boundary conditions trigger an exception, the Operator receives an explicit review task.

Amendment must occur through a versioned amendment packet, never through silent editing of the signed baseline.

---

## 12. Interview and Elicitation Workspace

The interview experience is built around Elicitation Units derived from Activatives.

An Elicitation Unit should show:

- objective
- Activative linkage
- evidence required
- primary question
- suggested follow-ups
- desired depth
- fallback
- exit criterion
- evidence already obtained
- remaining evidence gap

The system should support adaptive sequencing, but the Operator remains the human conducting the relationship.

CAE should assist before capture through planning and after capture through analysis. It should not silently become an autonomous interviewer that overrides the Operator's judgment.

Interview completion is based on holistic yield sufficiency, not mechanical completion of every scripted question.

---

## 13. Evidence Workspace

Evidence is a first-class operator object.

For every evidence moment the UI should expose:

- sovereign source media identity
- source media hash
- temporal start/end
- transcript span
- exact spoken wording
- speaker identity
- evidence classification
- provenance
- collision/tension linkage
- downstream uses
- validation state

The source media is sovereign. Transcript and model-derived observations are derivatives.

A floating quote without an admissible temporal anchor should not be presented as equivalent to verified evidence.

Where useful, the interface should provide side-by-side media and transcript inspection, with synchronized playback and the exact anchored span highlighted.

---

## 14. Collision and Candidate Review

A Collision should be understandable as a grounded relationship between:

- Guest DNA / Subject reality
- Audience Tension
- World Signal

The UI should not present a collision as a mysterious AI score.

It should show:

- grounding
- tension matrix
- paradox or latent truth
- supporting evidence
- falsification conditions
- downstream implications
- candidate ranking
- operator-relevant risks

Autonomous collision discovery must halt at its approval gate before downstream portfolio composition when the governing contract requires operator signoff.

---

## 15. Recommendation Review

Every recommendation must answer:

**What is proposed?**

**Why?**

**What evidence supports it?**

**Which upstream objects does it depend on?**

**What validation has passed?**

**What remains uncertain?**

**What happens if I approve?**

**What happens if I reject?**

**What repair paths are available?**

The interface should make the authority lane legible:

- Hunter: discovery
- Analyst: interpretation/ranking
- Composer: evidence-backed production contract
- Commander: consequential state transition

The Operator should not need to understand internal software architecture, but should understand the epistemic role of the recommendation.

---

## 16. Exception Queue

Exceptions are operational work, not log entries.

Each exception should display:

- severity
- stage
- affected object
- exact failure
- contract/invariant violated
- evidence
- current state
- available recovery actions
- recommended repair
- consequences
- operator decision
- resulting receipt/state

The UI must not offer actions that the runtime will necessarily reject.

Fail-closed behavior should be actionable rather than opaque.

---

## 17. Revision and Repair

Revision is immutable versioning, not in-place editing.

The Revision Composer should represent:

**Current revision → proposed change → derived revision → validation → execution/approval**

The Operator should see impact before executing a revision.

A revision must retain lineage to its parent.

If a change invalidates downstream objects, the UI should show the affected dependency set rather than allowing a misleading partial update.

---

## 18. Authorization

Authorization is a major operator surface.

Before approval, the UI must show:

- exact object
- revision identifier
- state version/hash
- evidence
- policy revision
- operator authority
- validation results
- consequences
- next state
- receipt that will be generated

Approval must be fail-closed if the object changed since inspection.

Authorization decisions are durable runtime facts, not browser events.

Campaign autonomy modes may change how much routine work requires operator intervention, but constitutional invariants remain non-waivable.

---

## 19. Release and Ship

The release surface must expose readiness as a governed checklist.

At minimum:

- evidence sufficiency
- composition validity
- QA
- provenance
- authorization
- release manifest
- integrity/seal
- distribution readiness
- policy compliance

`SHIP` should only become available when the runtime reports that all mandatory gates pass.

External distribution consumes the sealed release artifact. The UI must not imply that distribution may rewrite semantic content.

---

## 20. Outcome and Memory

After distribution, the Operator should be able to connect outcomes to:

- campaign objective
- audience hypothesis
- tension hypothesis
- exact release manifest
- creative revision
- distribution result

Raw outcomes do not directly overwrite canonical memory.

The UI should present Learning Candidates as governed proposals for memory promotion, including evidence and attribution rather than presenting every observed metric as learned truth.

---

## 21. Timeline and Audit

Timeline provides the chronological production history.

It should include:

- state transitions
- agent actions
- operator actions
- approvals/rejections
- revisions
- evidence admissions
- exceptions
- recovery
- releases
- outcomes

`EXPORT_AUDIT` produces the authoritative audit representation.

The Operator should be able to reconstruct not only what happened but why a consequential action was allowed.

---

## 22. Status and Attention Model

The UI should use a canonical runtime-derived status vocabulary.

Candidate states include:

`READY`, `RUNNING`, `WAITING`, `BLOCKED`, `AWAITING_APPROVAL`, `APPROVED`, `REJECTED`, `REPAIR_REQUIRED`, `PAUSED`, `FAILED`, `COMPLETED`, `CANCELLED`, `RELEASE_READY`, `RELEASED`.

The final enumeration must be derived from the canonical runtime state machine before implementation. UI.md does not independently create state semantics.

Attention should prioritize:

1. blocking failures
2. required human decisions
3. stale/invalidated reviews
4. approaching policy/budget limits
5. ordinary progress

---

## 23. Progressive Disclosure

Routine Operators need concise decision surfaces.

Expert Operators need complete lineage.

The same canonical object must support both.

Default presentation should show:

- what
- why
- evidence
- state
- action

Advanced inspection may reveal:

- hashes
- agent/model invocation
- context projection
- policy revision
- receipt chain
- runtime node
- raw payload
- diagnostic details

Progressive disclosure is a presentation strategy, not a second data model.

---

## 24. Multi-Channel Interaction

Web is the primary rich control surface.

Slack, Telegram, Mini Apps, and future channels are adapters.

A notification may tell an Operator that an interview is ready. A lightweight channel may support a simple disposition. A richer channel may open an asset inspection view.

All consequential operations must call the same canonical runtime.

A “yes” from chat and an approval click in the web console must resolve to the same governed action, subject to the same authorization and freshness checks.

---

## 25. Accessibility of Decisions

Every consequential action should be understandable without relying solely on color or visual polish.

The interface must make visible:

- current state
- blocked reason
- evidence status
- authority status
- freshness
- consequences
- available actions

Dangerous actions such as reject, repair, or ship should expose their consequence before confirmation.

---

## 26. UI-to-Runtime Action Contract

| UI action | Runtime meaning |
|---|---|
| DISCOVER | Find or inspect available work/objects |
| INSPECT | Retrieve authoritative object and supporting evidence |
| RUN | Request execution of a declared program/workflow |
| PAUSE | Request governed suspension |
| RESUME | Request continuation from an eligible paused state |
| APPROVE | Record authorized human decision |
| REJECT | Record authorized rejection disposition |
| REPAIR | Create or apply a governed recovery/revision path |
| SHIP | Advance an eligible sealed release toward distribution |
| EXPORT_AUDIT | Produce the authoritative audit representation |

The UI must never implement these actions by mutating local state directly.

---

## 27. Completion Standard

The UI contract is satisfied when an Operator can operate a real CAE campaign from intake through production and audit while remaining inside one canonical runtime authority model.

A complete implementation must demonstrate:

- campaign creation
- pipeline visibility
- preparation graph revisioning
- execution monitoring
- evidence inspection
- exception resolution
- stale-state protection
- authorization
- revision/repair
- release readiness
- shipping
- audit export
- outcome visibility

The UI is complete when it exposes the runtime's actual guarantees rather than simulating them.

---

## 28. Relationship to Architecture.md and the 57 Mandates

UI.md defines the Operator-facing contract.

Architecture.md defines the physical system required to make that contract true.

The 57 mandates implement the canonical decisions underneath both.

Therefore:

**Canon → Product Brief → PRDs/FRs → UI contract + physical architecture → mandates → implementation → executable evidence.**

UI.md must never silently change a constitutional requirement. When a UI need exposes a missing runtime capability, the required change belongs in the appropriate mandate and runtime architecture rather than being hidden in frontend logic.

---

## 29. Final UI Principle

CAE should feel to the Operator like a **production operating console for a governed evidence transformation engine**.

The Operator sees what matters.

The UI explains why.

Evidence remains inspectable.

Authority remains explicit.

Runtime state remains canonical.

Agents propose and execute within their authority.

Humans make consequential decisions.

Every action converges on the same state graph.

**One program state. Many interaction surfaces. No shadow authority.**
