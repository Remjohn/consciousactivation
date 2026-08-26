# CAE CA-CAN-02 Operator Reading Packet
# Mandate: Phase 24 / CA-CAN-02 — Constitution Set Completion

**Document ID**: `CAE-CAN-02-READING-PACKET-001`  
**Status**: `READY_FOR_OPERATOR_READING`  
**Date**: `2026-08-26`  
**Governing Mandate**: `24_CA_CAN_02_CONSTITUTION_SET_COMPLETION_MANDATE.md`  

---

## 1. Executive Summary & Coverage Ledger

This Operator Reading Packet compiles the complete 30-constitution specification governing the Conscious Activation Engine (CAE). It provides the structured foundation for the Operator Reading Pause ahead of Phase 25+ implementation authorization.

### Coverage Ledger Overview (40 Total Objects/Concepts)
- **`COVERED_BY_EXISTING` (16 items)**: 15 ratified Phase 23 constitutions + `WorkspaceMembership` (CA-REL-001).
- **`REQUIRES_CONSTITUTION` (15 items)**: All 15 newly authored in Phase 24 with 26-dimension completeness.
- **`DEFERRED_WITH_OPERATOR_SIGNOFF_REQUIRED` (9 items)**: `semantic_operation`, `registry_snapshot`, `registry_item`, `registry_reference`, `registry_disposition`, `execution_receipt` (vs `receipt`), `Candidate`, `Coalition`, `Edge`, `SemanticProgram`.

*(Full ledger details: [`CAE_CAN_02_COVERAGE_LEDGER.md`](file:///d:/Work/consciousactivation/docs/cae/implementation/CAE_CAN_02_COVERAGE_LEDGER.md))*

---

## 2. Plain-Language Summaries Ordered for Operator Reading

### Order of Reading:
1. **Canonical Plane Doctrines** (Global System Law)
2. **Operational Plane: Platform & Security Roots**
3. **Operational Plane: Workspace & Tenancy Hierarchy**
4. **Operational Plane: State Control & Concurrency Mechanics**
5. **Operational Plane: Dialogue & Media Ingestion**
6. **Operational Plane: Evidence & Grounding Substrates**
7. **Operational Plane: Qualitative Intelligence & Semantic Inference**

---

### Part I: Canonical Plane Doctrines (Global System Law)

#### 1. `StateTransitionContract` (`CA-POL-002`)
- **What it is**: The immutable canonical specification defining valid lifecycle states, edge transitions, and invariants for domain aggregates.
- **What it forbids**: Forbids non-deterministic transitions, unreachable non-terminal states, outbound transitions on terminal states, and embedding tenant IDs in canonical contracts.
- **What an enforcing agent refuses**: Refuses any state mutation request whose operation or target state is not explicitly defined in the active contract.

#### 2. `OperatorAccessPolicy` (`CA-POL-001`)
- **What it is**: The canonical specification defining allowable operator maintenance access, role escalation tiers, and audit rules.
- **What it forbids**: Forbids ambient, unlogged operator access to tenant workspace data.
- **What an enforcing agent refuses**: Refuses unauthenticated or out-of-policy operator elevation requests.

#### 3. `HarnessTemplate` (`CA-STR-001`)
- **What it is**: Pinned canonical runbook workflow template defining multi-step procedural execution sequences.
- **What it forbids**: Forbids runtime modification of template steps; forbids storing operational execution state in the template.
- **What an enforcing agent refuses**: Refuses execution requests referencing modified or unpinned template hashes.

#### 4. `SDARegistry` (`CA-REG-001`)
- **What it is**: Canonical ontology defining 13 semantic dimensions and polarities, inheriting manifest version `1.0` under ratified custodian ruling.
- **What it forbids**: Forbids inline mutation of dimension YAML files, tenant leakage into global archives, and rejecting records for lacking inline version tags.
- **What an enforcing agent refuses**: Refuses resolution if the `sda.zip` archive SHA-256 does not match pinned snapshot digest.

#### 5. `SFLRegistry` (`CA-REG-002`)
- **What it is**: Canonical registry of Sensory Function Language assets, embedding operator-ratified Route B permanent quarantine for absent families (`SFL-FAM-005, 006, 007, 009, 012`).
- **What it forbids**: Forbids silent fallback to other families, heuristic in-memory invention of missing families, and unquarantining absent families without formal RFC.
- **What an enforcing agent refuses**: Refuses resolution of absent family IDs by raising `RegistryItemQuarantinedError(reason="ABSENT_SFL_FAMILY")`.

#### 6. `PrimitiveRegistry` (`CA-REG-003`)
- **What it is**: Canonical catalog of 243 psychological primitives across 26 families, embedding operator-ratified Route A disambiguation (line 194 is `EXP-TRG-001`; line 231 is `EXP-TRG-010`).
- **What it forbids**: Forbids duplicate ID collisions, last-write-wins overwrites during loading, and injecting ungoverned tenant primitives.
- **What an enforcing agent refuses**: Refuses duplicate primitive registration by raising `RegistryItemAmbiguousError`.

---

### Part II: Operational Plane Roots & Tenancy

#### 7. `OperatorOrganization` (`CA-ENT-001`)
- **What it is**: Operational root entity representing the platform provider organization.
- **What it forbids**: Forbids deletion while active workspaces exist.
- **What an enforcing agent refuses**: Refuses cross-organization tenant data access.

#### 8. `OperatorAccessGrant` (`CA-SEC-001`)
- **What it is**: Time-bounded, justified operator session grant for tenant support/audit.
- **What it forbids**: Forbids indefinite or unjustified operator access tokens.
- **What an enforcing agent refuses**: Refuses operator access after grant expiry timestamp.

#### 9. `Workspace` (`CA-ENT-002`)
- **What it is**: Primary multi-tenant isolation root in PostgreSQL (`cae.workspace`), enforcing Row Level Security (RLS).
- **What it forbids**: Forbids cross-tenant data visibility or foreign key references across workspaces.
- **What an enforcing agent refuses**: Refuses queries and writes lacking valid `workspace_id` session context.

#### 10. `WorkspaceMembership` (`CA-REL-001`)
- **What it is**: Relational association binding users/agents to specific workspaces with explicit roles.
- **What it forbids**: Forbids role escalation without administrator authorization.
- **What an enforcing agent refuses**: Refuses tenant actions from unassigned actors.

#### 11. `Engagement` (`CA-ENT-003`)
- **What it is**: Lifecycle container for customer advisory/commercial engagement projects.
- **What it forbids**: Forbids creating sessions or runs outside an active engagement.
- **What an enforcing agent refuses**: Refuses asset attachments to archived engagements.

#### 12. `Guest` (`CA-ENT-004`)
- **What it is**: Individual guest identity within an engagement.
- **What it forbids**: Forbids unconsented PII exposure across engagements.
- **What an enforcing agent refuses**: Refuses guest data export without explicit consent token.

#### 13. `GuestIdentityLink` (`CA-MAP-001`)
- **What it is**: Privacy-preserving cross-workspace pseudonymous linkage for returning guests.
- **What it forbids**: Forbids plaintext cross-tenant identity merging.
- **What an enforcing agent refuses**: Refuses unhashed identity resolution requests.

---

### Part III: State Control & Concurrency Mechanics

#### 14. `StateAggregate` (`CA-STA-001`)
- **What it is**: Operational concurrency and sequence root tracking current lifecycle state and `aggregate_version`.
- **What it forbids**: Forbids optimistic locking bypass, sequence skipping, and unjournaled state mutations.
- **What an enforcing agent refuses**: Refuses state transition requests where `expected_version != aggregate_version` (`ERR_OPTIMISTIC_LOCK_CONFLICT`).

#### 15. `StateTransition` (`CA-EVT-004`)
- **What it is**: Immutable journal record in `cae.state_transition` capturing before/after states and version increments (`to_version = from_version + 1`).
- **What it forbids**: Forbids updating or deleting historical transitions; forbids unassigned `command_id`.
- **What an enforcing agent refuses**: Refuses non-sequential transition insertions.

#### 16. `Command` (`CA-EXE-002`)
- **What it is**: Idempotent intent execution packet in `cae.command` binding caller `actor_id` to operational parameters.
- **What it forbids**: Forbids duplicate execution of identical idempotency keys; forbids parameter mutations post-submission.
- **What an enforcing agent refuses**: Refuses unattributed commands or concurrent duplicate key submissions.

#### 17. `Event` (`CA-EVT-002`)
- **What it is**: Transactional domain event broadcast in `cae.event` notifying asynchronous workers and projections of state side-effects.
- **What it forbids**: Forbids modifying broadcast payloads; forbids routing conversational speech turns into system event bus.
- **What an enforcing agent refuses**: Refuses cross-workspace event distribution without explicit bridge authorization.

#### 18. `HarnessRun` (`CA-EXE-001`)
- **What it is**: Stateful execution instance of a HarnessTemplate within an engagement.
- **What it forbids**: Forbids skipping mandatory harness stages.
- **What an enforcing agent refuses**: Refuses step execution out of defined template order.

#### 19. `Receipt` (`CA-REC-001`)
- **What it is**: Cryptographic execution proof in `cae.receipt` certifying that a command or step executed.
- **What it forbids**: Forbids mutating receipt payload hash or execution timestamps.
- **What an enforcing agent refuses**: Refuses marking commands COMPLETED without an attributable receipt.

#### 20. `ReceiptEvidenceLink` (`CA-REL-005`)
- **What it is**: Relational binding connecting execution receipts to produced evidence artifacts.
- **What it forbids**: Forbids ungrounded receipt claims.
- **What an enforcing agent refuses**: Refuses cross-tenant receipt-evidence bindings.

---

### Part IV: Media, Evidence & Semantic Intelligence

#### 21. `InterviewSession` (`CA-ENT-005`)
- **What it is**: Operational container managing live or synthetic interview execution.
- **What it forbids**: Forbids multi-guest sessions (strictly 1:1 with Guest); forbids turn insertion into non-ACTIVE sessions.
- **What an enforcing agent refuses**: Refuses recording turns in PLANNED or COMPLETED sessions.

#### 22. `InterviewTurn` (`CA-EVT-003`)
- **What it is**: Immutable conversational dialogue utterance turn (`cae.interview_turn`) with monotonic ordinals and millisecond offsets.
- **What it forbids**: Forbids in-place text edits for acoustic cleanup; forbids publishing dialogue into `cae.event`.
- **What an enforcing agent refuses**: Refuses out-of-order or duplicate turn ordinals.

#### 23. `MediaAsset` (`CA-MED-001`)
- **What it is**: Verified operational container for uploaded audio/video media recordings.
- **What it forbids**: Forbids storing raw binary blobs in PostgreSQL tables (must use private object storage).
- **What an enforcing agent refuses**: Refuses processing media files before cryptographic verification.

#### 24. `ImmutableMediaEvidence` (`CA-EVI-001`)
- **What it is**: Raw media file hash evidence certifying byte integrity.
- **What it forbids**: Forbids modifying byte size or SHA-256 after capture.
- **What an enforcing agent refuses**: Refuses mismatched media checksum submissions.

#### 25. `EvidenceSource` (`CA-REL-004`)
- **What it is**: Ingestion envelope binding evidence items to raw source packages.
- **What it forbids**: Forbids orphaned evidence items without source packages.
- **What an enforcing agent refuses**: Refuses evidence extraction from unverified source packages.

#### 26. `EvidenceItem` (`CA-EVI-002`)
- **What it is**: Discrete qualitative observation extracted from interview transcripts/media, guarded by DB triggers.
- **What it forbids**: Forbids in-place payload edits; forbids unanchored evidence lacking spans.
- **What an enforcing agent refuses**: Refuses self-authentication by capturing agents.

#### 27. `EvidenceSpan` (`CA-REL-003`)
- **What it is**: Physical millisecond/character coordinate interval anchoring evidence claims to raw media/turns.
- **What it forbids**: Forbids inverted offsets (`start > end`); forbids cross-workspace media links.
- **What an enforcing agent refuses**: Refuses span links exceeding asset duration.

#### 28. `EvidenceAuthentication` (`CA-REC-003`)
- **What it is**: Qualitative attestation record by an independent evaluator certifying evidence truth.
- **What it forbids**: Forbids self-attestation (`evaluator == capturer`); forbids empty rationale strings.
- **What an enforcing agent refuses**: Refuses self-certified evidence promotions to AUTHENTICATED.

#### 29. `SemanticAssessment` (`CA-DSA-001`)
- **What it is**: Derived qualitative psychological insight (role tensions, polarities) requiring causal evidence grounding.
- **What it forbids**: Forbids ungrounded assessments; forbids automated self-promotion to `epistemic_status: ESTABLISHED`.
- **What an enforcing agent refuses**: Refuses activation of assessments lacking supporting evidence links.

#### 30. `AssessmentEvidenceLink` (`CA-REL-006`)
- **What it is**: Causal relation binding a SemanticAssessment to supporting EvidenceItems with relevance weights.
- **What it forbids**: Forbids cross-workspace links; forbids out-of-bounds relevance scores.
- **What an enforcing agent refuses**: Refuses linking assessments to evidence in different workspaces.

---

## 3. Open Questions Requiring Operator Rulings

The reading packet isolates the following non-blocking design questions for operator determination during the reading pause:

1. **Question OP-Q1 (Storage Projection for Deferred Infrastructure)**: Should the 5 registry-infrastructure concepts (`registry_snapshot`, `registry_item`, `registry_reference`, `registry_disposition`, `registry_version_link`) be formally modeled as relational tables in `cae.*` during Phase 25, or maintained purely in-memory within `RegistryResolver`?
2. **Question OP-Q2 (Multi-Party Interview Sessions)**: Should future interview formats supporting panel/focus-group sessions introduce a new object (`MultiPartyInterviewSession`), or should `InterviewSession` be amended post-pilot with an explicit multi-guest policy?
3. **Question OP-Q3 (First Implementation Package Target)**: Post-reading pause, which slice should become the first authorized implementation package: (A) Tenant & Workspace Core, (B) Media & Evidence Ingestion, or (C) Canonical Registry Binding?

---

## 4. Constitution Amendment Request Template

If the Operator identifies required modifications during the reading pause, amendments should be submitted using the following structured format:

```markdown
### Constitution Amendment Request
- **Target Constitution**: `CA-CAN-02_<NAME>.yaml`
- **Target Dimension**: `[e.g., 15_invariants, 17_authorized_operations]`
- **Current Text / Rule**: `[Quoted existing rule]`
- **Proposed Amendment**: `[Exact replacement text]`
- **Architectural Rationale**: `[Why this modification is necessary]`
- **Downstream Impact Analysis**: `[Impact on state machine, RLS, or evidence pipeline]`
```
