---
title: 'PRD: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol'
status: draft_for_review
version: 0.1.0-draft
updated: '2026-07-13'
---

# PRD: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol

> Combined rendering of the authoritative shards. Do not edit independently.


---

# 0. Document Purpose and Authority

This sharded Product Requirements Document defines the **CMF Content Harness ↔ Visual Asset Editor Delegation Protocol**. It is intended for CMF product architects, protocol and platform engineers, Content Harness implementers, Visual Asset Editor implementers, security and operations owners, conformance engineers, and downstream composition-runtime maintainers.

The PRD is the product-level authority for the shared boundary only. It does not redesign either independent product. Technical realization belongs in the later Architecture package; implementation stories and feature specifications follow Architecture.

## Source-of-truth hierarchy

1. Locked product decisions in `governance/DECISION_REGISTER.*`
2. Product and protocol requirements in this PRD and `governance/REQUIREMENTS_REGISTRY.*`
3. Frozen upstream architecture in `governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml`
4. Architecture and ADRs, once approved
5. Epics, stories, feature specifications, and code

## Requirement conventions

- Functional Requirements use globally stable IDs `FR-001` through `FR-128`.
- Non-Functional Requirements use grouped IDs such as `NFR-AUTH-001`.
- User journeys use `UJ-01` through `UJ-14`.
- Every feature maps to one of the 16 locked decisions.
- No implementation detail may silently override an authority or lifecycle requirement.


---

# 1. Vision and Product Promise

## Vision

CMF Atomic Content Harnesses must be able to request visual assets from an independently evolving Visual Asset Editor without losing semantic sovereignty, production specialization, lifecycle clarity, or auditability. The boundary must remain stable even as category profiles, asset families, visual-production workflows, evaluators, compute runtimes, and product versions change.

## Canonical product promise

> **The CMF Content Harness ↔ Visual Asset Editor Delegation Protocol is an independently versioned, governed contract protocol with deterministic boundary services. It validates and routes immutable Visual Asset Demands and results, enforces field-level authority, negotiates semantic compatibility, projects a stable shared lifecycle, manages idempotency, supersession, cancellation, amendments, budgets, acknowledgements, invalidation and trust, and emits complete audit receipts—without becoming a third creative, Activative, composition, or visual-production authority.**

## Product value

The protocol makes it possible to:

- preserve Content Harness ownership of meaning, Activative purpose, sequence role and composition intent;
- preserve Visual Asset Editor ownership of production planning, models, workflows, candidates, evaluation and repair;
- evolve both products independently under explicit compatibility;
- resume from authoritative versions rather than shared mutable state;
- stop, supersede, repair, invalidate and replace work without losing history;
- prove cross-product behavior through executable conformance suites;
- observe one correlated lifecycle inside the validated Harness Control Tower.

## Release 1 proving ground

The first certified integration is the **Format 02 — Minimal Coach Theatre** reference slice within the `2d_character_animation` category. The protocol must support both single character/scene demands and multi-asset Delegation Sets through final Remotion-consumption acknowledgement.


---

# 2. Users, Systems, and Jobs To Be Done

## Primary actors

### Content Harness and Harness Maintainer
Owns demand meaning, sequence and composition authority, budget authorization, demand versions, amendments, cancellation, and result acknowledgement.

### Visual Asset Editor and Visual Production Maintainer
Owns production planning, resource selection, candidate generation, evaluation, repair, production acceptance, and production lineage.

### Delegation Protocol Maintainer
Maintains schemas, lifecycle machine, authority rules, compatibility, adapters, boundary services, audit, conformance, and release certification.

### Composition Runtime
Consumes only acknowledged, current Asset Results and records exact usage.

### Operations and Security Owner
Observes stalled or compromised delegations, trust failures, SLOs, audit chains, and incident response.

### Conformance and Release Engineer
Runs producer, consumer, authority, lifecycle, compatibility, migration, resilience, and Format 02 end-to-end suites.

## Non-users

The Delegation Protocol is not a manual art workstation, a ComfyUI workflow editor, a visual evaluator, a content ideation system, or an independent creative agent.

## Key user and system journeys

### UJ-01 — A Content Harness submits an authoritative demand

A registered Content Harness submits one immutable Visual Asset Demand through a compatible envelope and receives an idempotent submission receipt.

### UJ-02 — The boundary negotiates a safe protocol profile

The Delegation Layer checks versions, required features, category certification and authority before accepting the delegation.

### UJ-03 — The Visual Asset Editor reports progress without exposing internals

The editor emits product events that project into a stable external lifecycle while internal production nodes remain private.

### UJ-04 — The Content Harness acknowledges a current result

The editor returns a production-accepted result; the Content Harness validates current demand, sequence, composition and dependencies before automatic consumption acknowledgement.

### UJ-05 — A demand changes while production is in flight

The Content Harness submits a superseding version with typed changes; valid work is reused and only affected work is invalidated.

### UJ-06 — The editor proposes a feasible amendment

The editor returns structured amendment options with evidence and predicted effects; the owning authority accepts one through a new demand version or declines.

### UJ-07 — The editor requests more budget

The editor checkpoints and requests an immutable budget extension when the authorized envelope is insufficient; production resumes only after valid approval.

### UJ-08 — A no-longer-needed delegation is cancelled

The Content Harness requests cancellation; queued work stops, atomic work reaches a safe checkpoint, useful evidence is retained and stale promotion is prevented.

### UJ-09 — A scene coordinates several related assets

A Delegation Set coordinates independent character, background and prop demands with shared identity, palette, geometry and atomic completion policy.

### UJ-10 — A failure routes to the correct authority

A typed failure identifies the responsible system, retry class, decision owner, remaining valid artifacts and required next action.

### UJ-11 — Products interoperate across versions

A compatibility manifest and negotiation select a safe pinned profile, use a lossless adapter or produce an immutable migration.

### UJ-12 — A completed asset is invalidated and replaced

A later regression or constitution update triggers an impact notice, blocks unsafe use, preserves history and revalidates a replacement.

### UJ-13 — The protocol rejects a forged or replayed action

Identity, signature, authority and replay checks reject the message before lifecycle state changes and record a security incident receipt.

### UJ-14 — An operator observes and certifies the shared boundary

The Control Tower shows lifecycle, authority, compatibility, budget, events, exceptions, acknowledgements and audit-chain state while conformance suites prove behavior.


---

# 3. Product Doctrine and Authority Boundary

## 1. Boundary, not brain

The protocol enforces what each product may say, change, accept and revoke. It never invents visual meaning or production strategy.

## 2. Immutable messages, explicit evolution

Accepted demands, messages, results, acknowledgements, amendments and receipts are immutable. Change is represented through linked versions and governed notices.

## 3. Content Harness semantic sovereignty

The Content Harness exclusively owns semantic intent, Activative purpose, sequence role, asset role, composition intent, identity and continuity requirements, wrong-reading locks, delivery requirements and budget authorization.

## 4. Visual Asset Editor production sovereignty

The Visual Asset Editor exclusively owns Visual Production Plans, production routes, ComfyUI workflows, models, LoRAs, controls, candidate generation, visual evaluation, targeted repair, production acceptance and asset lineage.

## 5. Stable external lifecycle

The protocol projects a small, durable cross-product lifecycle from authoritative messages. Internal workflow nodes remain private to their owning products.

## 6. Semantic compatibility before syntactic compatibility

A message is compatible only when required meaning, authority, lifecycle, evaluation, category, geometry and failure behavior can be preserved.

## 7. Production acceptance is not consumption acknowledgement

The VAE proves that an asset satisfies the demand. The Content Harness proves that the certified result remains current and compatible for downstream composition.

## 8. Retry by failure class

Contract correction, infrastructure recovery, visual repair, migration, amendment and human exception are different flows. Blind unchanged retry is prohibited.

## 9. Historical truth survives current invalidation

Revoked, superseded and replaced results remain historically reproducible and may remain useful as negative evidence.

## 10. No silent degradation

Budget, timing, compatibility or feasibility pressure cannot silently weaken semantic authority, required evaluation or quality gates.

## 11. One correlated audit chain

Every state-changing action is attributable, integrity-checked, correlated, causally linked and preserved in the append-only audit history.

## Authority summary

| Domain | Owner | Protocol responsibility |
|---|---|---|
| Meaning and Activative intent | Content Harness | Validate and preserve |
| Sequence, asset and composition role | Content Harness | Validate, correlate and route proposals |
| Budget envelope | Content Harness | Validate and enforce |
| Visual Production Plan | Visual Asset Editor | Reference and correlate only |
| Workflows, models, LoRAs and controls | Visual Asset Editor | No creative decision |
| Visual evaluation and repair | Visual Asset Editor | Project shared failures and receipts |
| Production acceptance | Visual Asset Editor | Validate and route |
| Consumption acknowledgement | Content Harness / composition runtime | Validate and complete |
| Shared lifecycle, compatibility, integrity and audit | Delegation Protocol | Deterministically enforce |


---

# 4. Canonical Glossary

Downstream artifacts must use these terms consistently. Synonyms that blur authority are prohibited.

- **Delegation Protocol** — The governed contract protocol and deterministic boundary services connecting a Content Harness and Visual Asset Editor without becoming a third creative authority.

- **Delegation Envelope** — The common versioned metadata wrapper carrying message identity, correlation, causation, principals, authority, integrity, idempotency, and payload reference.

- **Visual Asset Demand** — The immutable, versioned, Content Harness-owned contract expressing semantic intent, Activative purpose, visual role, composition intent, continuity, delivery, evaluation, and budget authority.

- **Visual Asset Editor** — The independently versioned production authority that derives and executes Visual Production Plans and certifies production acceptance.

- **Content Harness** — The atomic product authority that owns the Visual Asset Demand and acknowledges current downstream consumption compatibility.

- **Delegation Correlation** — The complete lifecycle of one delegated visual request, identified by a correlation ID.

- **Causation ID** — The message identifier that directly caused a later message.

- **Submission Receipt** — The protocol acknowledgement that a submitted delegation was validated and accepted or rejected at the boundary.

- **Production Acceptance** — The Visual Asset Editor's certification that an asset satisfies the authorized demand and production gates.

- **Consumption Acknowledgement** — The Content Harness or composition runtime's confirmation that a production-accepted result is current and compatible for downstream use.

- **Delegation Set** — A versioned coordination contract grouping independent Visual Asset Demands under shared continuity, dependency, and completion constraints.

- **Supersession** — The authority-scoped replacement of one immutable demand version by a newer linked version.

- **Selective Invalidation** — The explicit preservation of unaffected artifacts and invalidation of only those results or nodes impacted by an authoritative change.

- **Amendment Proposal** — A typed, non-binding VAE proposal describing exact demand changes, authority class, evidence, and predicted consequences.

- **Budget Authorization** — The immutable Content Harness-owned envelope defining approved Budget Program, ceilings, purpose, and escalation policy.

- **Compatibility Manifest** — A machine-readable declaration of accepted/emitted protocol versions, message versions, features, profiles, and limitations.

- **Negotiated Delegation Profile** — The pinned protocol, message, feature, category, adapter, and migration configuration accepted for one delegation.

- **Lifecycle Projection** — The stable shared state derived from accepted authoritative messages, distinct from either product's internal state machine.

- **Failure Taxonomy** — The protocol-owned stable classification of unsuccessful conditions, responsibility, retry, invalidation, and next-authority semantics.

- **Invalidation Notice** — A post-completion message requiring current-use revalidation without necessarily declaring an asset defective.

- **Revocation Notice** — A post-completion message immediately blocking new or active consumption for a critical defect, integrity, security, or regression reason.

- **Replacement Notice** — A typed link from an affected result or asset to a new candidate for future use, still requiring compatibility validation.

- **Delegation Audit Receipt** — An append-only chained record of identity, integrity, schema, authority, lifecycle, and persistence validation for a message.

- **Protocol Principal** — A registered product, runtime, service, operator, or policy identity permitted to perform defined delegation actions.

- **Replay** — A previously valid signed message reused outside its permitted idempotent or lifecycle context.

- **Conformance Suite** — The shared executable producer, consumer, authority, lifecycle, compatibility, integrity, and resilience tests for the protocol.

- **Development Capsule** — The implementation-ready governed package containing approved product, architecture, contracts, fixtures, tests, migration, observability, and authorization evidence.


---

# F01 — Governed Protocol Boundary and Deterministic Boundary Services

## User outcome

Independent products can delegate visual work through an enforced boundary without creating a third creative authority.

## Product behavior

The protocol provides deterministic contract, authority, compatibility, lifecycle, routing, idempotency, and audit services while leaving semantic decisions with the Content Harness and production decisions with the Visual Asset Editor.

## Brownfield baseline

The validated Builder and Visual Asset Editor PRDs already establish three independent compilation targets and prohibit cross-product authority leakage. Their shared boundary remains provisional.

## Required product delta

Formalize the shared boundary as a product-level protocol with explicit owned and prohibited responsibilities.

## Traceability

- **Locked decision:** `D001`

- **User journeys:** `UJ-01`, `UJ-03`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

## Functional Requirements

### FR-001 — Canonical delegation boundary

**Requirement:** The system shall expose a versioned Delegation Protocol as the sole supported production boundary between registered Content Harnesses and registered Visual Asset Editors.

**Testable consequences:**

- A conformant submission enters through a registered protocol endpoint or transport adapter.

- Direct unvalidated production invocation is rejected and receipted.

**Failure examples:**

- A harness calls a ComfyUI worker directly and bypasses authority validation.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-002 — Deterministic boundary responsibilities

**Requirement:** The protocol shall deterministically perform schema validation, authority validation, compatibility negotiation, idempotency resolution, lifecycle validation, routing, and audit persistence.

**Testable consequences:**

- Each responsibility emits a machine-readable result.

- No model judgment is required for a valid/invalid boundary decision.

**Failure examples:**

- An LLM decides whether an unsupported contract version is acceptable.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-003 — No third creative authority

**Requirement:** The protocol shall not originate, reinterpret, rank, or amend semantic intent, Activative purpose, sequence role, composition intent, or visual-production strategy.

**Testable consequences:**

- Protocol outputs contain only validations, projections, receipts, and routed product messages.

- A creative change is rejected unless authored by the owning product.

**Failure examples:**

- The boundary service rewrites a character action to improve feasibility.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-004 — Independent product preservation

**Requirement:** The protocol shall preserve independent versioning, deployment, state machines, and internal implementation authority for the Content Harness and Visual Asset Editor.

**Testable consequences:**

- Internal VAE node names are not required in the public lifecycle.

- A VAE patch can deploy without a Builder release when contracts remain compatible.

**Failure examples:**

- The shared protocol requires identical product version numbers.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-005 — Canonical shared ABI

**Requirement:** The protocol shall publish a machine-readable registry of every supported message type, version, producer, consumer, and authority scope.

**Testable consequences:**

- Unregistered message types are rejected.

- The registry identifies the canonical schema URI and hash.

**Failure examples:**

- A product invents a new status payload without registration.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-006 — Boundary receipts

**Requirement:** Every accepted or rejected boundary action shall emit an immutable validation or audit receipt linked to the triggering message.

**Testable consequences:**

- The receipt records every performed validation.

- Rejected messages do not mutate lifecycle state.

**Failure examples:**

- A malformed submission is only written to an application log.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-007 — Transport independence

**Requirement:** The protocol shall preserve identical semantics across supported HTTP, queue, event-stream, local-process, and fixture transports.

**Testable consequences:**

- Transport adapters pass the same conformance suite.

- No transport may weaken integrity or authority checks.

**Failure examples:**

- Local file fixtures bypass signature and lifecycle validation in production mode.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

### FR-008 — Architecture-preservation enforcement

**Requirement:** The protocol shall evaluate proposed schemas and services against the frozen Builder and Visual Asset Editor Architecture Preservation Contracts.

**Testable consequences:**

- A conflicting change produces an upstream amendment requirement.

- The preservation check is a release hard gate.

**Failure examples:**

- A delegation release locally changes Content Harness semantic authority.

**Traceability:** `D001` · `UJ-01`, `UJ-03`, `UJ-14` · `NFR-GOV-001`, `NFR-REL-001`, `NFR-TRACE-001`, `NFR-SEC-001`

## Feature failure conditions

- Boundary logic performs creative inference.

- A product bypasses protocol validation.

- Protocol state diverges from authoritative product messages.

## Explicitly out of scope

- Content-generation reasoning

- Visual-production planning

- ComfyUI orchestration

- Final composition authoring


---

# F02 — Visual Asset Demand Ownership, Immutability, and Authority

## User outcome

The Content Harness can express and evolve visual intent without production systems silently changing it.

## Product behavior

The Content Harness exclusively owns Visual Asset Demand meaning and versions; the protocol validates ownership while the VAE may derive plans, annotate feasibility, and propose amendments.

## Brownfield baseline

The VAE PRD defines Visual Asset Demand as authoritative input and semantic non-mutation as a constitutional law.

## Required product delta

Add field-level ownership, immutable acceptance, version identity, and prohibited mutation tests at the shared boundary.

## Traceability

- **Locked decision:** `D002`

- **User journeys:** `UJ-01`, `UJ-05`, `UJ-06`

- **Cross-cutting NFRs:** `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

## Functional Requirements

### FR-009 — Exclusive demand ownership

**Requirement:** Only the registered owning Content Harness shall create or supersede authoritative Visual Asset Demand versions.

**Testable consequences:**

- The demand owner is recorded in the envelope and payload.

- Submissions from non-owners are rejected as authority failures.

**Failure examples:**

- The VAE publishes a modified demand as authoritative.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-010 — Immutable accepted demand

**Requirement:** An accepted demand version shall be immutable and addressed by request ID, version, payload hash, and canonical reference.

**Testable consequences:**

- In-place updates are rejected.

- Every execution pins the exact accepted demand identity.

**Failure examples:**

- A database row is overwritten while production is in progress.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-011 — Field-level authority map

**Requirement:** Every authoritative demand field shall map to an owner and authority class covering Activative semantic lineage, Activation Contract, Expression Moment lineage, Visual Semantics, Visual Narrative, Feature Contracts, somatic route, sequence, composition, identity, continuity, wrong-reading locks, delivery, and budget domains.

**Testable consequences:**

- The boundary can reject an unauthorized field change deterministically.

- Unknown authoritative fields block acceptance until registered.

**Failure examples:**

- An adapter drops a wrong-reading lock, Expression Moment reference, recognition carrier, viewer role, or Visual Narrative field because it does not recognize the field.

**RC2 consumer-conformance correction:** Every Visual Asset Demand carries
mandatory governed `source_provenance.source_kind`. `interview_expression`
requires non-empty Reaction Receipt and Expression Moment reference
collections. Other governed kinds may omit those collections, but supplied
references remain fully validated. Protocols and adapters preserve these fields
and never infer or manufacture missing interview provenance.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-012 — Optional notes separation

**Requirement:** Free-form notes shall be treated as non-authoritative enrichment and shall never override typed demand fields.

**Testable consequences:**

- Conflicts are resolved in favor of typed fields.

- Notes are preserved with provenance for specialist context.

**Failure examples:**

- A note saying 'ignore the BBOX' changes the composition contract.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-013 — Permitted derived artifacts

**Requirement:** The VAE may derive Visual Production Plans, geometry recommendations, feasibility reports, evaluations, and amendment proposals without acquiring demand ownership.

**Testable consequences:**

- Derived artifacts cite the exact demand version.

- They declare their own producer and authority.

**Failure examples:**

- A production plan is presented as a new demand version.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-014 — Amendment-only feedback

**Requirement:** Any VAE-requested change to a demand-owned field shall be expressed through a typed non-binding Amendment Proposal.

**Testable consequences:**

- No accepted demand is changed by the proposal.

- The Content Harness may accept, reject, or supersede.

**Failure examples:**

- The VAE relaxes continuity because generation is difficult.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-015 — Demand identity propagation

**Requirement:** Every submission, event, result, failure, amendment, and receipt shall carry or resolve to the exact demand ID, version, and hash.

**Testable consequences:**

- Stale events can be detected.

- Audit reconstruction identifies the governing demand.

**Failure examples:**

- A result identifies only the request ID, not the demand version.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

### FR-016 — No implicit authority transfer

**Requirement:** Submission, acceptance, execution, or budget escalation shall not transfer semantic or composition authority to the VAE or protocol.

**Testable consequences:**

- Authority remains stable through the lifecycle.

- Any proposed ownership change requires upstream governance.

**Failure examples:**

- The service assumes that production acceptance makes it owner of the composition role.

**Traceability:** `D002` · `UJ-01`, `UJ-05`, `UJ-06` · `NFR-AUTH-001`, `NFR-CONTRACT-001`, `NFR-TRACE-002`, `NFR-GOV-002`

## Feature failure conditions

- Accepted demand mutated in place.

- Untyped note overrides authoritative contract.

- VAE output masquerades as demand authority.

## Explicitly out of scope

- Internal VAE planning

- Content Harness idea-generation workflow

- Human art-direction UI


---

# F03 — Immutable Contract Family and Common Delegation Envelope

## User outcome

Every cross-product interaction is unambiguous, attributable, versioned, and independently validatable.

## Product behavior

The protocol uses single-purpose immutable payloads wrapped in a common envelope for identity, versions, authority, correlation, causation, integrity, and references.

## Brownfield baseline

VAE PRD contains provisional demand, event, result, conflict, and related schemas, but shared authority belongs to this protocol.

## Required product delta

Create the canonical shared contract family and a message registry with conformance fixtures.

## Traceability

- **Locked decision:** `D003`

- **User journeys:** `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13`

- **Cross-cutting NFRs:** `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

## Functional Requirements

### FR-017 — Common delegation envelope

**Requirement:** Every protocol message shall use a common envelope containing protocol version, message type/version, IDs, sender, recipient, authority scope, timestamps, idempotency, hashes, and payload reference.

**Testable consequences:**

- Envelope validation precedes payload routing.

- All message types share stable correlation semantics.

**Failure examples:**

- One message omits sender authority because it travels on an internal queue.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-018 — Single-purpose immutable payloads

**Requirement:** Each lifecycle action shall use an immutable payload dedicated to one purpose rather than a shared mutable delegation record.

**Testable consequences:**

- Submission and cancellation are separate messages.

- History is reconstructed from messages, not overwritten state.

**Failure examples:**

- A single JSON object is edited by both products.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-019 — Correlation and causation

**Requirement:** Messages shall identify correlation ID and, when caused by another message, causation ID.

**Testable consequences:**

- A complete delegation chain can be traversed.

- Retries remain distinguishable from new actions.

**Failure examples:**

- An amendment response cannot be tied to its proposal.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-020 — Authority-scoped envelope

**Requirement:** The envelope shall declare the authority exercised by the sender, and the boundary shall validate it against the principal registry.

**Testable consequences:**

- Unauthorized action is rejected before payload effects.

- Authority evidence is retained in audit receipts.

**Failure examples:**

- A Content Harness emits a production-acceptance message.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-021 — Reference-and-hash payload transport

**Requirement:** Large or canonical payloads shall be exchanged through stable references plus content hashes rather than duplicated mutable bodies.

**Testable consequences:**

- Recipients verify payload integrity.

- Object storage and contract storage remain decoupled from messaging.

**Failure examples:**

- A video binary is embedded in an event message.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-022 — Independent message versioning

**Requirement:** Protocol, envelope, and payload message types shall be independently versioned under governed compatibility rules.

**Testable consequences:**

- An optional event extension does not force a major protocol version.

- Pinned delegations retain their negotiated versions.

**Failure examples:**

- All contracts inherit the product version number.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-023 — Mandatory semantic-field protection

**Requirement:** Unknown or unsupported mandatory fields shall block compatibility rather than be silently ignored.

**Testable consequences:**

- Required-feature support is negotiated.

- Loss of authority-bearing fields produces INCOMPATIBLE.

**Failure examples:**

- A consumer ignores a required continuity constraint.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

### FR-024 — Message Type Registry

**Requirement:** The protocol shall maintain a canonical registry for message names, schemas, owners, lifecycle effects, idempotency behavior, and compatibility status.

**Testable consequences:**

- Every schema in the package has a registry entry.

- Deprecated types list replacements and timelines.

**Failure examples:**

- A new cancellation variant is deployed without registry metadata.

**Traceability:** `D003` · `UJ-01`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-CONTRACT-001`, `NFR-SEC-002`, `NFR-TRACE-003`, `NFR-COMPAT-001`

## Feature failure conditions

- Mutable cross-product record.

- Uncorrelated messages.

- Unknown mandatory semantics ignored.

## Explicitly out of scope

- Transport-specific implementation details

- Internal product event schemas not crossing the boundary


---

# F04 — Stable External Lifecycle and Deterministic Projection

## User outcome

Both products and operators can understand the shared commitment without coupling to internal production nodes.

## Product behavior

The protocol owns a compact external lifecycle projected from authoritative product messages and validates every transition, timeout, and terminal state.

## Brownfield baseline

Content Harness and VAE each own richer internal state machines. The VAE PRD already defines production stages and events.

## Required product delta

Define the public lifecycle, transition table, product-to-protocol projections, timeout semantics, and illegal-transition tests.

## Traceability

- **Locked decision:** `D004`

- **User journeys:** `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

## Functional Requirements

### FR-025 — Canonical external states

**Requirement:** The protocol shall define stable states including DRAFT, SUBMITTED, ACCEPTED, IN_PROGRESS, RESULT_READY, COMPLETED, and governed exceptional states.

**Testable consequences:**

- States have explicit definitions and owners.

- Arbitrary product status strings cannot become protocol state.

**Failure examples:**

- The public lifecycle exposes 'model_loading_flux'.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-026 — Authoritative state projection

**Requirement:** A shared-state change shall be derived only from an accepted authoritative product message mapped through a registered projection rule.

**Testable consequences:**

- The protocol never invents progress.

- Projection records the source message.

**Failure examples:**

- The boundary marks RESULT_READY because a timeout estimate elapsed.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-027 — Transition validation

**Requirement:** Every state transition shall be checked against a deterministic lifecycle machine before persistence.

**Testable consequences:**

- Illegal forward and backward transitions are rejected.

- Transition receipts record from-state, to-state, and rule.

**Failure examples:**

- COMPLETED transitions directly back to IN_PROGRESS.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-028 — Terminal-state enforcement

**Requirement:** Terminal states shall reject ordinary progress messages and require explicit post-completion notice types for invalidation, revocation, or replacement.

**Testable consequences:**

- Late events do not reopen completed delegations.

- Post-completion governance remains auditable.

**Failure examples:**

- A late candidate event changes a completed result.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-029 — Exceptional lifecycle paths

**Requirement:** The lifecycle shall govern rejection, amendment, supersession, budget approval, capability gap, human review, cancellation, partial result, invalidation, revocation, and replacement.

**Testable consequences:**

- Each exception has allowed entry and exit transitions.

- Decision authority is explicit.

**Failure examples:**

- CAPABILITY_GAP is emitted as an arbitrary string with no next action.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-030 — Timeout semantics

**Requirement:** The protocol shall distinguish target miss, heartbeat loss, production estimate overrun, approval timeout, hard cutoff, and expiry.

**Testable consequences:**

- Timeouts emit typed events.

- Timeout does not silently lower quality or cancel unless policy says so.

**Failure examples:**

- A soft deadline automatically accepts a degraded candidate.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-031 — Lifecycle reconstruction

**Requirement:** The current projection shall be reproducible from the accepted append-only message and audit sequence.

**Testable consequences:**

- Projection rebuild matches stored state.

- Corrupt projections can be repaired without product mutation.

**Failure examples:**

- The lifecycle exists only as a mutable row with no event history.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

### FR-032 — Lifecycle receipts and observability

**Requirement:** Each accepted transition shall emit a lifecycle receipt and update the Control Tower projection within the defined freshness SLO.

**Testable consequences:**

- Operators can identify the latest authoritative cause.

- Stalled states are detectable.

**Failure examples:**

- A transition occurs without an observable event or receipt.

**Traceability:** `D004` · `UJ-01`, `UJ-03`, `UJ-05`, `UJ-08`, `UJ-14` · `NFR-LIFE-001`, `NFR-REL-002`, `NFR-OBS-001`, `NFR-TRACE-004`

## Feature failure conditions

- Public state couples to internal workflow nodes.

- Illegal transition accepted.

- Terminal state reopened by ordinary event.

## Explicitly out of scope

- Internal VAE production graph

- Internal Content Harness sequencing states


---

# F05 — Demand Supersession, Impact Analysis, and Selective Invalidation

## User outcome

An updated demand can replace an in-flight or completed version without discarding unaffected work or promoting stale results.

## Product behavior

The protocol validates explicit supersession and authority-declared change sets; the VAE computes plan-level reuse and invalidation; shared state prevents stale promotion.

## Brownfield baseline

Both upstream PRDs define immutable versioning and repair/invalidation, but their cross-product supersession semantics are provisional.

## Required product delta

Specify change classes, impact receipts, stale-result controls, and resumable handoff behavior.

## Traceability

- **Locked decision:** `D005`

- **User journeys:** `UJ-05`, `UJ-09`, `UJ-12`

- **Cross-cutting NFRs:** `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

## Functional Requirements

### FR-033 — Explicit supersession link

**Requirement:** A new demand version shall explicitly identify the prior version it supersedes and shall be authored by the owning Content Harness.

**Testable consequences:**

- The old version enters SUPERSEDED through a valid message.

- Unlinked replacement submissions are treated as separate demands.

**Failure examples:**

- The same request ID is reused with a new body and no version link.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-034 — Typed changed-field declaration

**Requirement:** The supersession message shall enumerate changed field paths, change classes, and unchanged authority domains.

**Testable consequences:**

- Impact analysis can distinguish meaning, composition, delivery, and execution-policy changes.

- False unchanged declarations are detected against payload diffs.

**Failure examples:**

- A semantic action changes but the message claims 'delivery only'.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-035 — Supersession authority validation

**Requirement:** The boundary shall validate that every changed field is owned by the sender and allowed in a superseding demand.

**Testable consequences:**

- Unauthorized changes are rejected.

- Constitutional changes route upstream.

**Failure examples:**

- A composition runtime changes a wrong-reading lock.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-036 — Selective invalidation request

**Requirement:** The protocol shall request a VAE impact analysis that identifies reusable outputs, invalidated outputs, affected nodes, and safe resume point.

**Testable consequences:**

- The result is typed and linked to the new demand.

- Uncertainty blocks unsafe reuse.

**Failure examples:**

- The protocol itself guesses which ComfyUI nodes can be reused.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-037 — Stale-promotion prevention

**Requirement:** Once supersession is accepted, no asset result produced solely against the old demand may be promoted as satisfying the new version without revalidation.

**Testable consequences:**

- Old results remain historical.

- The lifecycle projection blocks stale acknowledgement.

**Failure examples:**

- An old result arrives late and is automatically consumed.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-038 — Reusable-work preservation

**Requirement:** The protocol shall preserve immutable evidence and VAE-certified reusable outputs that remain valid under the declared change set.

**Testable consequences:**

- Identity references may survive a composition change.

- Preserved artifacts retain original lineage.

**Failure examples:**

- Every new version forces complete asset regeneration.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-039 — Resumable execution correlation

**Requirement:** A resumed execution shall link the prior execution, new demand, invalidation receipt, and new Visual Production Plan version.

**Testable consequences:**

- Audit can explain exactly what was reused.

- Budget accounting distinguishes prior and resumed work.

**Failure examples:**

- A new run silently copies files from the old run.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

### FR-040 — Completed-result revalidation

**Requirement:** A completed result affected by supersession shall enter revalidation or replacement handling rather than being deleted or silently retained as current.

**Testable consequences:**

- Downstream consumers receive an invalidation notice.

- Published historical uses remain reproducible.

**Failure examples:**

- A previously consumed asset reference is overwritten.

**Traceability:** `D005` · `UJ-05`, `UJ-09`, `UJ-12` · `NFR-LIFE-002`, `NFR-REL-003`, `NFR-TRACE-005`, `NFR-CONTRACT-002`

## Feature failure conditions

- Stale result promoted against new demand.

- Impact analysis lacks field-level basis.

- Unaffected work discarded without reason.

## Explicitly out of scope

- VAE internal node invalidation algorithm

- Content Harness content-revision workflow


---

# F06 — Production Acceptance and Downstream Consumption Acknowledgement

## User outcome

A production-certified asset enters composition only when it is still valid for current downstream state.

## Product behavior

The VAE owns production acceptance; the Content Harness or composition runtime owns compatibility acknowledgement; the protocol validates both without duplicating visual evaluation.

## Brownfield baseline

The VAE PRD defines layered asset effectiveness and Asset Result Contracts. The Content Harness owns sequence and composition state.

## Required product delta

Formalize RESULT_READY, acknowledgement, stable rejection reasons, and completion semantics.

## Traceability

- **Locked decision:** `D006`

- **User journeys:** `UJ-04`, `UJ-12`

- **Cross-cutting NFRs:** `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

## Functional Requirements

### FR-041 — VAE production acceptance authority

**Requirement:** Only the VAE shall assert production acceptance for assets that passed its certified evaluation and delivery gates.

**Testable consequences:**

- Result contracts reference evaluation and production receipts.

- The protocol validates VAE authority.

**Failure examples:**

- The Content Harness marks a raw candidate as production accepted.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-042 — Consumption acknowledgement authority

**Requirement:** Only the owning Content Harness or authorized composition runtime shall acknowledge downstream consumption compatibility.

**Testable consequences:**

- Acknowledgement identifies current demand, sequence, and composition versions.

- The result is not consumable before acknowledgement.

**Failure examples:**

- The VAE unilaterally inserts an asset into Remotion.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-043 — Automatic acknowledgement

**Requirement:** The Content Harness shall automatically acknowledge results when demand identity, dependencies, role, geometry, receipts, references, and non-supersession checks pass.

**Testable consequences:**

- Routine completion requires no human.

- Each check is machine-readable.

**Failure examples:**

- An operator must click approve for every accepted character pose.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-044 — Stable rejection taxonomy

**Requirement:** A result rejection shall use protocol codes such as stale version, missing receipt, incompatible geometry, unavailable asset, or invalidated dependency.

**Testable consequences:**

- Rejection identifies the next action.

- Unstructured aesthetic preference is not a valid rejection.

**Failure examples:**

- The harness returns 'I don't like it'.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-045 — No duplicate visual evaluation

**Requirement:** The Content Harness shall not re-run the VAE's full semantic, Activative, or visual-quality evaluation as part of acknowledgement.

**Testable consequences:**

- Only downstream compatibility is checked.

- Quality disputes route through demand amendment or evaluator-dispute flows.

**Failure examples:**

- The harness launches a second general VLM and overrides the certified evaluator.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-046 — Current dependency verification

**Requirement:** Acknowledgement shall validate the result against current demand, sequence, composition, category profile, and required upstream dependencies.

**Testable consequences:**

- Stale composition geometry is detected.

- Pinned versions appear in the receipt.

**Failure examples:**

- A result is consumed after the scene layout changed.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-047 — Immutable acknowledgement record

**Requirement:** Acknowledgement or rejection shall be an immutable message linked to the exact result and downstream state.

**Testable consequences:**

- Repeated identical acknowledgement is idempotent.

- Later invalidation creates a new notice.

**Failure examples:**

- An acknowledgement field is toggled in place.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

### FR-048 — Completion after acknowledgement

**Requirement:** The shared lifecycle shall reach COMPLETED only after a valid production-accepted result is acknowledged or a declared terminal partial-completion policy is satisfied.

**Testable consequences:**

- RESULT_READY remains non-terminal.

- Completion receipts identify consumed assets.

**Failure examples:**

- The protocol marks complete as soon as the VAE finishes packaging.

**Traceability:** `D006` · `UJ-04`, `UJ-12` · `NFR-AUTH-002`, `NFR-LIFE-003`, `NFR-COMPAT-002`, `NFR-REL-004`

## Feature failure conditions

- Production acceptance confused with consumption authority.

- Subjective duplicate review blocks result.

- Stale composition accepted.

## Explicitly out of scope

- VAE quality-scoring internals

- Final publication approval


---

# F07 — Budget Authorization, Allocation, Escalation, and Cost Receipts

## User outcome

The requester controls maximum spend and policy purpose while the VAE autonomously optimizes production within that authority.

## Product behavior

The Content Harness authorizes a budget envelope; the VAE chooses internal allocation; the protocol validates programs, ceilings, escalation, checkpointing, and final receipts.

## Brownfield baseline

The VAE PRD defines six Budget Programs and candidate portfolios. The Content Harness controls demand policy.

## Required product delta

Create immutable budget authorization and escalation contracts with no silent overrun or quality degradation.

## Traceability

- **Locked decision:** `D007`

- **User journeys:** `UJ-07`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

## Functional Requirements

### FR-049 — Budget-envelope ownership

**Requirement:** The Content Harness shall authorize the Budget Program, policy priority, cost/time/GPU ceilings, experimental policy, and escalation rules.

**Testable consequences:**

- Authorization is signed and versioned.

- Unauthorized Premium or Capability Learning requests are rejected.

**Failure examples:**

- The VAE chooses an unlimited budget based on asset importance.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-050 — VAE allocation autonomy

**Requirement:** The VAE may allocate candidate count, parallelism, workflows, providers, models, evaluators, and repairs inside the authorized envelope.

**Testable consequences:**

- Internal choices need not be specified by the harness.

- Actual usage remains observable.

**Failure examples:**

- The harness dictates exact GPU model and seed count in the shared contract.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-051 — Budget Program validation

**Requirement:** The protocol shall validate selected programs against the canonical registry, caller authority, category certification, and supported VAE capabilities.

**Testable consequences:**

- Unknown or incompatible programs block acceptance.

- Custom programs require complete bounds.

**Failure examples:**

- A free-form 'ultra' budget string is accepted.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-052 — Typed escalation request and response

**Requirement:** Predicted budget insufficiency shall produce a typed escalation with evidence, requested extension, expected outcome, and alternatives.

**Testable consequences:**

- Approval creates a new immutable authorization version.

- Denial preserves checkpointed work.

**Failure examples:**

- The editor silently spends above the ceiling then reports it.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-053 — No silent overrun

**Requirement:** The boundary shall prevent starting work that would exceed a hard authorized ceiling without an accepted extension.

**Testable consequences:**

- The execution enters COST_APPROVAL_REQUIRED.

- No new expensive nodes begin while awaiting approval.

**Failure examples:**

- A third-party provider invoice exceeds the ceiling because actual use was not checked.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-054 — Capability Learning authorization

**Requirement:** Transition into a Capability Learning purpose shall require explicit Content Harness policy or operator authority.

**Testable consequences:**

- Ordinary production cannot silently become experimentation.

- Learning receipts state controlled variables.

**Failure examples:**

- A failed image triggers a 30-candidate experiment automatically.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-055 — Quality-gate preservation

**Requirement:** Budget exhaustion or deadline pressure shall not permit the protocol or VAE to lower constitutional quality gates without a new authorized demand or degradation decision.

**Testable consequences:**

- Stopping without an asset is permitted.

- A passing existing candidate may be returned.

**Failure examples:**

- The system accepts a wrong action to remain under budget.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

### FR-056 — Final budget receipt

**Requirement:** Every terminal delegation shall include authorization versions, actual spend, GPU/time usage, candidate counts, repairs, compliance, and avoided cost where measurable.

**Testable consequences:**

- Receipt reconciles to VAE execution data.

- Control Tower exposes budget state.

**Failure examples:**

- Only estimated cost is retained after completion.

**Traceability:** `D007` · `UJ-07`, `UJ-14` · `NFR-AUTH-003`, `NFR-PERF-001`, `NFR-TRACE-005`, `NFR-GOV-003`

## Feature failure conditions

- Silent budget overrun.

- Content Harness leaks internal compute control.

- Capability Learning begins without authority.

## Explicitly out of scope

- Cloud-provider billing implementation

- Project-wide financial accounting outside delegation


---

# F08 — Cancellation, Deadlines, Safe Checkpointing, and Race Resolution

## User outcome

Obsolete delegated work stops safely, preserves valuable evidence, and cannot produce a stale consumable result.

## Product behavior

The Content Harness authoritatively requests cancellation; the protocol orders races; the VAE stops at a safe boundary and returns a disposition receipt.

## Brownfield baseline

The VAE PRD defines resumable node graphs and immutable artifacts, but cross-product cancellation remains shared protocol behavior.

## Required product delta

Specify request/receipt contracts, deadline policies, disposition classes, and deterministic ordering.

## Traceability

- **Locked decision:** `D008`

- **User journeys:** `UJ-08`, `UJ-05`

- **Cross-cutting NFRs:** `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

## Functional Requirements

### FR-057 — Cancellation authority

**Requirement:** The owning Content Harness or authorized operator policy shall be able to request cancellation of a delegation or permitted Delegation Set scope.

**Testable consequences:**

- Authority is validated before state change.

- Unauthorized cancellation is rejected.

**Failure examples:**

- An unrelated harness cancels a GPU job.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-058 — Block new work on acceptance

**Requirement:** Once a valid cancellation is accepted, the VAE shall stop scheduling new production and candidate-expansion nodes for the affected scope.

**Testable consequences:**

- Queued jobs are cancelled where safe.

- The shared state becomes CANCELLATION_REQUESTED.

**Failure examples:**

- The system continues Exploration candidates after cancellation.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-059 — Nearest safe checkpoint

**Requirement:** In-flight work shall stop at the nearest safe atomic boundary according to the declared stop policy.

**Testable consequences:**

- Partial files are not promoted.

- Atomic completion under a small remaining-time threshold may be allowed.

**Failure examples:**

- A container is killed mid-write and corrupts shared storage.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-060 — Artifact disposition classification

**Requirement:** The cancellation receipt shall classify accepted assets, candidates, references, masks, geometry, learning evidence, caches, and incomplete artifacts.

**Testable consequences:**

- Reusable evidence can enter governed memory.

- Cancelled outputs are not consumption-authorized.

**Failure examples:**

- All files are deleted, including a validated identity mask.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-061 — Deadline policy semantics

**Requirement:** The protocol shall distinguish target completion, hard cutoff, and expiry, with explicit behavior for each.

**Testable consequences:**

- Soft misses notify but do not mutate quality gates.

- Expiry can trigger cancellation.

**Failure examples:**

- Every deadline miss destroys the run.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-062 — Deterministic race ordering

**Requirement:** Cancellation, supersession, result readiness, and acknowledgement races shall resolve from accepted message order, causation, and precedence rules.

**Testable consequences:**

- A valid supersession outranks ordinary cancellation when specified.

- A result emitted after cancellation cannot be promoted.

**Failure examples:**

- Whichever network response arrives first wins.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-063 — Stale-promotion prevention

**Requirement:** A cancelled delegation shall prohibit downstream consumption authorization for subsequently produced outputs under that correlation.

**Testable consequences:**

- Historical candidates remain traceable.

- A new demand may reuse them only through explicit validation.

**Failure examples:**

- A late VAE result is acknowledged because it passed quality.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

### FR-064 — Cancellation and compute receipt

**Requirement:** Terminal cancellation shall report stopped execution, last checkpoint, retained artifacts, consumed/avoided cost, and downstream authorization state.

**Testable consequences:**

- The Control Tower projection closes cleanly.

- Receipts support operational review.

**Failure examples:**

- Cancellation is represented only as an HTTP 204.

**Traceability:** `D008` · `UJ-08`, `UJ-05` · `NFR-LIFE-004`, `NFR-REL-005`, `NFR-RES-001`, `NFR-TRACE-005`

## Feature failure conditions

- Unsafe hard kill.

- Late stale asset promoted.

- Cancellation loses evidence and compute accountability.

## Explicitly out of scope

- Internal GPU cancellation primitives

- User-facing content-project deletion


---

# F09 — Protocol Failure Taxonomy, Responsibility, and Recovery Semantics

## User outcome

Every unsuccessful condition routes to the correct owner and recovery path without blind retries or cross-product confusion.

## Product behavior

The protocol owns stable failure families/codes and required semantics; products attach diagnostics without redefining shared meaning.

## Brownfield baseline

The VAE PRD distinguishes contract, authority, compatibility, infrastructure, quality, budget, human, and integrity failures.

## Required product delta

Create a canonical taxonomy, typed failure envelope, retry/round rules, invalidation semantics, and partial-result behavior.

## Traceability

- **Locked decision:** `D009`

- **User journeys:** `UJ-10`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

## Functional Requirements

### FR-065 — Canonical failure families

**Requirement:** The protocol shall define stable families for contract, authority, compatibility, staleness, feasibility, infrastructure, quality, budget/timing, human exception, and security/integrity failures.

**Testable consequences:**

- Every registered code belongs to one family.

- Unknown product diagnostics map to a stable fallback family.

**Failure examples:**

- All failures are returned as FAILED with prose.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-066 — Stable failure codes

**Requirement:** Each protocol code shall have an immutable semantic definition, severity range, terminality rule, and recovery class.

**Testable consequences:**

- Clients can branch deterministically.

- Deprecated codes publish replacements.

**Failure examples:**

- The same code means retryable in one product and terminal in another.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-067 — Responsibility and decision ownership

**Requirement:** Every failure message shall identify detector, responsible system, next-decision owner, and enforcement owner.

**Testable consequences:**

- Cross-product responsibility is explicit.

- The Control Tower displays the next owner.

**Failure examples:**

- A VAE feasibility failure has no indication that the Content Harness must decide.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-068 — Retry classification

**Requirement:** Failures shall state whether retry is permitted, whether payload changes are required, and which retry class applies.

**Testable consequences:**

- Contract failures require corrected immutable messages.

- Infrastructure failures may use operational retries.

**Failure examples:**

- An unchanged authority violation is retried three times.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-069 — Quality-round accounting

**Requirement:** The protocol shall distinguish infrastructure recovery from VLM-directed quality-repair rounds and shall enforce the declared remaining quality rounds.

**Testable consequences:**

- GPU restart does not consume a quality round.

- A semantic-fidelity repair does.

**Failure examples:**

- Every error decrements the same retry counter.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-070 — Invalidation and preservation semantics

**Requirement:** Failure contracts shall identify affected artifacts or nodes, preserved valid outputs, and downstream state impact.

**Testable consequences:**

- Targeted repair can reuse unaffected work.

- Terminal failures block inappropriate promotion.

**Failure examples:**

- A pose failure invalidates the background plate without explanation.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-071 — Partial-result protocol

**Requirement:** The protocol shall support typed partial results with accepted roles, unresolved roles, failures, and an original completion policy.

**Testable consequences:**

- Partial consumption is allowed only when predeclared.

- Unresolved members retain independent lifecycle.

**Failure examples:**

- The VAE returns two of three assets and the harness guesses whether they are usable.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

### FR-072 — Product diagnostic extensions

**Requirement:** Products may attach detailed diagnostics through stable references while preserving the protocol-level classification and privacy boundary.

**Testable consequences:**

- Deep VLM evidence remains in VAE storage.

- The shared message stays bounded and parseable.

**Failure examples:**

- A product invents a new top-level failure meaning in a diagnostics blob.

**Traceability:** `D009` · `UJ-10`, `UJ-14` · `NFR-CONTRACT-003`, `NFR-REL-005`, `NFR-RES-002`, `NFR-OBS-002`

## Feature failure conditions

- Generic failure without recovery semantics.

- Infrastructure retry consumes quality rounds.

- Failure lacks responsible owner.

## Explicitly out of scope

- Internal stack traces

- VAE-specific evaluator taxonomies beyond shared mappings


---

# F10 — Delegation Sets, Shared Continuity, Dependencies, and Group Evaluation

## User outcome

Related assets can be produced independently while preserving scene-level identity, continuity, geometry, and completion guarantees.

## Product behavior

A Delegation Set coordinates member demands, shared constraints, dependency edges, completion policy, assembled evaluation, cancellation, and selective invalidation.

## Brownfield baseline

The VAE PRD supports multi-asset composition and immutable asset lineage. Format 02 requires characters, backgrounds, props, and overlays to work together.

## Required product delta

Define a shared set contract without merging member demands or lifecycles.

## Traceability

- **Locked decision:** `D010`

- **User journeys:** `UJ-09`, `UJ-04`, `UJ-12`

- **Cross-cutting NFRs:** `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

## Functional Requirements

### FR-073 — Typed Delegation Set

**Requirement:** The Content Harness shall be able to create an immutable versioned Delegation Set referencing independently versioned member demands.

**Testable consequences:**

- Every member retains its own correlation and asset lineage.

- The set has a stable owner and context.

**Failure examples:**

- One giant demand embeds all assets as mutable children.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-074 — Member lifecycle independence

**Requirement:** Each member shall retain independent submission, execution, evaluation, repair, result, and acknowledgement state.

**Testable consequences:**

- One failed prop does not erase an accepted background.

- Set status is derived from member states and policy.

**Failure examples:**

- All members share one undifferentiated status.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-075 — Shared constraint authority

**Requirement:** The set may define identity, environment, palette, lighting, camera axis, scale, world state, and Visual Syntax constraints that members may refine but not contradict.

**Testable consequences:**

- Contradictions produce a typed set conflict.

- Shared constraints cite their authority source.

**Failure examples:**

- Two characters use incompatible lighting without a conflict.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-076 — Typed dependency edges

**Requirement:** The set shall express directional relationships such as lighting reference, interaction geometry, identity continuity, or ordered production.

**Testable consequences:**

- Dependency changes drive selective invalidation.

- Cycles are detected or explicitly supported.

**Failure examples:**

- A character relies on a prop geometry that is not declared.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-077 — Completion policies

**Requirement:** The set shall support independent, partial_allowed, atomic_required, and ordered_release policies with required-role definitions.

**Testable consequences:**

- Consumption behavior is deterministic.

- The policy is fixed by the Content Harness.

**Failure examples:**

- The VAE decides to return a partial set because one asset is hard.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-078 — Set-level composition evaluation

**Requirement:** Required members shall be assembled in a composition simulation and evaluated for cross-asset consistency and Activative effectiveness where policy requires.

**Testable consequences:**

- Individual passes cannot hide group interaction failure.

- The set evaluation emits a typed receipt.

**Failure examples:**

- A hand and prop each pass separately but never align in composition.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-079 — Set-level selective invalidation

**Requirement:** A changed or failed member shall invalidate only dependent members and set evaluations supported by the dependency graph.

**Testable consequences:**

- Unrelated accepted members remain valid.

- A shared palette change can invalidate all affected members.

**Failure examples:**

- Any member update restarts the entire set.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

### FR-080 — Set cancellation and supersession

**Requirement:** The protocol shall support cancelling or superseding one member, optional members, or the complete set according to completion policy.

**Testable consequences:**

- Remaining members' consumability is recomputed.

- Every action is authority-validated.

**Failure examples:**

- Cancelling an optional overlay cancels a completed character asset.

**Traceability:** `D010` · `UJ-09`, `UJ-04`, `UJ-12` · `NFR-CONTRACT-004`, `NFR-LIFE-005`, `NFR-REL-005`, `NFR-DATA-001`

## Feature failure conditions

- Set erases member lineage.

- Shared constraints conflict silently.

- Individual passes bypass required assembled evaluation.

## Explicitly out of scope

- VAE internal asset batch scheduling

- Final scene composition runtime


---

# F11 — Semantic Compatibility, Negotiation, Adapters, Migration, and Deprecation

## User outcome

Independently released products interoperate only when required meaning and behavior can be preserved safely.

## Product behavior

Products publish compatibility manifests; the protocol negotiates pinned versions and features; adapters and migrations are deterministic, lossless for authority, and fully tested.

## Brownfield baseline

Builder and VAE PRDs require independent versioning and compatibility manifests, but their shared negotiation is not yet canonical.

## Required product delta

Define semantic compatibility verdicts, feature negotiation, adapter rules, migration artifacts, deprecation, and shared fixtures.

## Traceability

- **Locked decision:** `D011`

- **User journeys:** `UJ-02`, `UJ-11`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-COMPAT-001`, `NFR-CONTRACT-005`, `NFR-REL-005`, `NFR-GOV-004`

## Functional Requirements

### FR-081 — Product compatibility manifests

**Requirement:** Each participating release shall publish accepted/emitted protocol and message versions, supported features, certified profiles, and unsupported required capabilities.

**Testable consequences:**

- Manifests are machine-readable and signed.

- The boundary resolves them before acceptance.

**Failure examples:**

- Compatibility is inferred from product names.

**Traceability:** `D011` · `UJ-02`, `UJ-11`, `UJ-14` · `NFR-COMPAT-001`, `NFR-CONTRACT-005`, `NFR-REL-005`, `NFR-GOV-004`

### FR-082 — Semantic capability negotiation

**Requirement:** The protocol shall negotiate schema, authority, lifecycle, failure, asset-family, category-profile, geometry, Budget Program, and receipt support.

**Testable consequences:**

- Parsing without enforcement yields INCOMPATIBLE.

- Required features are pinned.

**Failure examples:**

- The VAE accepts wrong-reading locks but has no evaluator support.

**Traceability:** `D011` · `UJ-02`, `UJ-11`, `UJ-14` · `NFR-COMPAT-001`, `NFR-CONTRACT-005`, `NFR-REL-005`, `NFR-GOV-004`

### FR-083 — Pinned delegation profile

**Requirement:** Every accepted delegation shall record negotiated protocol/message versions, features, category profile, and adapters for its entire lifecycle.

**Testable consequences:**

- Running work does not silently upgrade.

- Receipts reproduce the negotiated profile.

**Failure examples:**

- A service deploy changes contract behavior mid-run.

**Traceability:** `D011` · `UJ-02`, `UJ-11`, `UJ-14` · `NFR-COMPAT-001`, `NFR-CONTRACT-005`, `NFR-REL-005`, `NFR-GOV-004`

### FR-084 — Canonical compatibility verdicts

**Requirement:** The protocol shall return COMPATIBLE, COMPATIBLE_WITH_ADAPTER, COMPATIBLE_WITH_DECLARED_DEGRADATION, MIGRATION_REQUIRED, or INCOMPATIBLE with reasons.

**Testable consequences:**

- Clients know the safe next action.

- Declared degradation requires owner authority.

**Failure examples:**

- An unknown field is ignored and treated as compatible.

**Traceability:** `D011` · `UJ-02`, `UJ-11`, `UJ-14` · `NFR-COMPAT-001`, `NFR-CONTRACT-005`, `NFR-REL-005`, `NFR-GOV-004`

### FR-085 — Lossless deterministic adapters

**Requirement:** Adapters may perform approved representational transformations but shall not drop or weaken semantic, Activative, authority, continuity, composition, or quality requirements.

**Testable consequences:**

- Adapters are versioned and testable.

- The original payload remains immutable.

**Failure examples:**

- An adapter removes an unsupported wrong-reading constraint.

**Traceability:** `D011` · `UJ-02`, `UJ-11`, `UJ-14` · `NFR-COMPAT-001`, `NFR-CONTRACT-005`, `NFR-REL-005`, `NFR-GOV-004`

### FR-086 — Immutable contract migration

**Requirement:** Migration shall create a new linked artifact with explicit transformations, authority-effect analysis, source/target validation, and semantic-equivalence result.

**Testable consequences:**

- The original contract is preserved.

- Unsafe migration returns incompatible.

**Failure examples:**

- A migration script overwrites the v1 demand.

**Traceability:** `D011` · `UJ-02`, `UJ-11`, `UJ-14` · `NFR-COMPAT-001`, `NFR-CONTRACT-005`, `NFR-REL-005`, `NFR-GOV-004`

### FR-087 — Version and deprecation policy

**Requirement:** Protocol and contracts shall use governed patch/minor/major semantics and active→discouraged→deprecated→read_only→retired states.

**Testable consequences:**

- Deprecation declares replacement and dates.

- Accepted active delegations remain valid.

**Failure examples:**

- A version is removed while an in-flight delegation uses it.

**Traceability:** `D011` · `UJ-02`, `UJ-11`, `UJ-14` · `NFR-COMPAT-001`, `NFR-CONTRACT-005`, `NFR-REL-005`, `NFR-GOV-004`

### FR-088 — Shared compatibility fixture suite

**Requirement:** Every claimed compatibility path shall pass producer, consumer, adapter, migration, unsupported-feature, and deprecated-version fixtures.

**Testable consequences:**

- Format 02 is a mandatory release suite.

- Results are attached to release certification.

**Failure examples:**

- A manifest claims compatibility without executing fixtures.

**Traceability:** `D011` · `UJ-02`, `UJ-11`, `UJ-14` · `NFR-COMPAT-001`, `NFR-CONTRACT-005`, `NFR-REL-005`, `NFR-GOV-004`

## Feature failure conditions

- JSON parsing treated as compatibility.

- Lossy semantic adapter.

- Running delegation silently upgrades.

## Explicitly out of scope

- Internal model/workflow compatibility inside VAE

- Builder target-profile migration outside shared contracts


---

# F12 — Typed Amendment Proposals and Authority-Governed Resolution

## User outcome

Feasibility evidence can lead to precise, reviewable changes without the VAE silently relaxing the demand.

## Product behavior

The VAE proposes immutable field-level options with authority class and predicted consequences; the Content Harness or bounded policy accepts or rejects; acceptance creates a new demand version.

## Brownfield baseline

The VAE PRD defines Constraint Conflicts and non-binding amendment proposals.

## Required product delta

Canonicalize proposal/response contracts, authority classes, auto-policy bounds, and resulting supersession.

## Traceability

- **Locked decision:** `D012`

- **User journeys:** `UJ-06`, `UJ-07`, `UJ-05`

- **Cross-cutting NFRs:** `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

## Functional Requirements

### FR-089 — Typed Amendment Proposal

**Requirement:** The VAE shall express requested demand changes as immutable options containing exact paths, current/proposed values, trigger evidence, and rationale.

**Testable consequences:**

- Options are independently identifiable.

- Free-form prose cannot change authority.

**Failure examples:**

- The editor returns 'make the box bigger' with no field path.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-090 — Authority-class classification

**Requirement:** Each proposed change shall be classified as internal production, execution policy, composition authority, semantic/Activative authority, or constitutional.

**Testable consequences:**

- The protocol routes to the correct owner.

- Misclassified fields are rejected by the authority matrix.

**Failure examples:**

- A subject change is labeled internal workflow adjustment.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-091 — Predicted consequence model

**Requirement:** Each option shall declare expected semantic, Activative, composition, cost, timing, reuse, and invalidation effects with uncertainty.

**Testable consequences:**

- The Content Harness can compare trade-offs.

- Predictions cite evidence and model version.

**Failure examples:**

- An option promises success with no basis.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-092 — Non-binding behavior

**Requirement:** An Amendment Proposal shall not mutate demand, budget, lifecycle authority, or production plan until a valid response is accepted.

**Testable consequences:**

- The original execution checkpoints safely.

- Unaccepted options expire without effect.

**Failure examples:**

- The VAE applies its preferred option while waiting.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-093 — Bounded policy-based approval

**Requirement:** The Content Harness may register narrow deterministic policies for specified fields/ranges that do not affect semantic or constitutional authority.

**Testable consequences:**

- Automatic approval cites the exact policy.

- Out-of-range changes require explicit authority.

**Failure examples:**

- A generic 'minor changes allowed' policy approves a role change.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-094 — Immutable Amendment Response

**Requirement:** Acceptance, rejection, or request-for-alternative shall be an immutable response linked to proposal and selected option.

**Testable consequences:**

- The decision owner is authenticated.

- Duplicate responses are idempotent.

**Failure examples:**

- An option selection is toggled in a mutable UI record.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-095 — Accepted amendment creates new demand

**Requirement:** Any accepted demand-owned change shall produce a new Visual Asset Demand version with supersession, source proposal, and impact analysis.

**Testable consequences:**

- The original remains unchanged.

- Selective invalidation begins from the new version.

**Failure examples:**

- The existing demand is patched in place.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

### FR-096 — Constitutional routing

**Requirement:** Proposals affecting category grammar, hard gates, authority boundaries, canonical ontology, or Builder doctrine shall be blocked from ordinary delegation and routed upstream.

**Testable consequences:**

- The protocol emits a constitutional-amendment requirement.

- No local approval can bypass it.

**Failure examples:**

- A VAE amendment alters the Minimal Coach Theatre category law.

**Traceability:** `D012` · `UJ-06`, `UJ-07`, `UJ-05` · `NFR-AUTH-004`, `NFR-CONTRACT-005`, `NFR-TRACE-005`, `NFR-GOV-005`

## Feature failure conditions

- Proposal mutates demand before acceptance.

- Authority class misroutes decision.

- Constitutional change approved locally.

## Explicitly out of scope

- Creative ranking of amendment options by the protocol

- Builder governance implementation


---

# F13 — Post-Completion Invalidation, Revocation, Supersession, and Replacement

## User outcome

Previously accepted assets remain historically reproducible while current and future consumption responds correctly to new evidence.

## Product behavior

The protocol preserves immutable results and changes only their authorization state through typed invalidation, revocation, supersession, replacement, and recall-review notices.

## Brownfield baseline

The VAE PRD defines immutable asset versions, Visual Asset Memory, regression detection, and revocation needs. The Content Harness owns current sequence use.

## Required product delta

Create post-completion notices, impact graph traversal, replacement compatibility, and acknowledgement tracking.

## Traceability

- **Locked decision:** `D013`

- **User journeys:** `UJ-12`, `UJ-04`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

## Functional Requirements

### FR-097 — Typed invalidation notice

**Requirement:** An owning product shall be able to mark a result as requiring revalidation when dependencies or authority context change without asserting that the asset is defective.

**Testable consequences:**

- New and active consumption can be blocked pending review.

- Historical use remains intact.

**Failure examples:**

- The asset file is deleted when a composition version changes.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-098 — Typed revocation notice

**Requirement:** The VAE or authorized integrity owner shall be able to revoke an asset for critical defect, integrity, security, evaluator-regression, or withdrawn-capability reasons.

**Testable consequences:**

- New consumption is blocked immediately.

- Severity and effective time are explicit.

**Failure examples:**

- A critical identity mismatch is only logged as a warning.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-099 — Supersession and replacement notices

**Requirement:** The protocol shall distinguish a newer preferred result from a mandatory replacement and link old/new assets and results.

**Testable consequences:**

- Older versions remain historical.

- Future retrieval uses current authorization state.

**Failure examples:**

- A new binary overwrites the old asset URI.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-100 — Downstream impact analysis

**Requirement:** The protocol shall traverse consumption links from result to variants, compositions, scenes/slides, sequences, outputs, and publications.

**Testable consequences:**

- Affected active and published scopes are reported separately.

- Required actions are typed.

**Failure examples:**

- An invalidation cannot identify where the asset was used.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-101 — Replacement compatibility validation

**Requirement:** A replacement shall be checked against current demand, geometry, masks, timing, Visual Syntax context, and composition before substitution.

**Testable consequences:**

- Replacement is not assumed drop-in.

- Selective composition reevaluation is triggered.

**Failure examples:**

- A character replacement with different BBOX is swapped without testing.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-102 — Historical reproducibility

**Requirement:** Invalidated or revoked artifacts, hashes, receipts, and actual historical consumption links shall remain retained under policy.

**Testable consequences:**

- Past outputs can be rebuilt exactly.

- Restricted access may apply for integrity/security.

**Failure examples:**

- Revocation removes evidence of what shipped.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-103 — Negative-evidence retention

**Requirement:** Revoked, rejected, or superseded assets may remain available to evaluators and learning systems as negative or historical evidence but shall be excluded from ordinary reuse.

**Testable consequences:**

- Memory query respects authorization state.

- Failure lessons retain provenance.

**Failure examples:**

- A revoked pose is retrieved as a normal reuse candidate.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-104 — Recall-review support

**Requirement:** For already-published outputs, the protocol shall issue review recommendations and track acknowledgement without silently editing publication records.

**Testable consequences:**

- Human or policy owner decides recall action.

- Audit shows unresolved published impacts.

**Failure examples:**

- The protocol automatically republishes edited content.

**Traceability:** `D013` · `UJ-12`, `UJ-04`, `UJ-14` · `NFR-LIFE-005`, `NFR-DATA-002`, `NFR-TRACE-005`, `NFR-REL-005`

## Feature failure conditions

- Historical artifact overwritten or deleted.

- Revoked asset reused normally.

- Replacement assumed composition-compatible.

## Explicitly out of scope

- Publication-management system

- VAE internal asset-regression investigation


---

# F14 — Principal Identity, Message Integrity, Replay Protection, and Audit Chain

## User outcome

Only authorized systems can create state changes, and every accepted action can be verified and reconstructed.

## Product behavior

The protocol registers principals and scopes, verifies signatures/hashes/nonces/expiry, distinguishes idempotent retry from replay, minimizes payloads, and emits append-only chained receipts.

## Brownfield baseline

Both upstream PRDs require receipts, hashes, provenance, and event sourcing, but the shared trust model is not yet canonical.

## Required product delta

Define principal registry, integrity envelope, validation order, replay rules, audit chain, and security incidents.

## Traceability

- **Locked decision:** `D014`

- **User journeys:** `UJ-13`, `UJ-01`, `UJ-14`

- **Cross-cutting NFRs:** `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

## Functional Requirements

### FR-105 — Registered delegation principals

**Requirement:** Every state-changing sender and recipient shall be a registered principal with product type, version, permitted actions, prohibited actions, credential reference, and status.

**Testable consequences:**

- Inactive principals are rejected.

- Scope can be evaluated deterministically.

**Failure examples:**

- Any internal service account can submit demands.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-106 — Message signing and hashing

**Requirement:** State-changing messages shall include verifiable envelope/payload hashes and an authenticated signature or equivalent architecture-approved integrity proof.

**Testable consequences:**

- Tampering is detected before state mutation.

- Signing identity is in the audit receipt.

**Failure examples:**

- Payload hash is optional on the internal queue.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-107 — Replay protection

**Requirement:** The protocol shall use message ID, nonce, expiry, idempotency key, payload hash, correlation, and lifecycle context to distinguish benign retries from replay.

**Testable consequences:**

- A retry returns the existing receipt.

- A replay produces a security failure.

**Failure examples:**

- The same signed cancellation is accepted twice in different states.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-108 — Deterministic validation order

**Requirement:** Boundary services shall verify identity, integrity, replay/expiry, protocol compatibility, schema, authority, and lifecycle before persistence or routing.

**Testable consequences:**

- Failure stage is receipted.

- No later validation can compensate for an earlier failure.

**Failure examples:**

- Schema-valid forged messages change state before signature verification.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-109 — Append-only audit chain

**Requirement:** Every accepted or rejected state-changing message shall create an append-only audit receipt with sequence, previous hash, validations, and resulting transition.

**Testable consequences:**

- A chain can detect gaps or reordering.

- Projection can be reconstructed.

**Failure examples:**

- Audit is a mutable table with deleted rejection rows.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-110 — Data minimization

**Requirement:** Messages shall carry only required contractual data and stable references/hashes, excluding secrets, large media, unnecessary prompts, weights, and private traces.

**Testable consequences:**

- Recipients retrieve authorized resources separately.

- Payload policies are testable.

**Failure examples:**

- A ComfyUI prompt history and model credential are embedded in an event.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-111 — Credential lifecycle

**Requirement:** Architecture shall support principal credential issuance, rotation, revocation, and overlap without invalidating historical signature verification.

**Testable consequences:**

- Rotation events are audited.

- Compromised principals can be disabled.

**Failure examples:**

- Rotating a key makes old audit receipts unverifiable.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

### FR-112 — Security-incident behavior

**Requirement:** Identity, integrity, replay, or isolation violations shall block state change, preserve forensic metadata, and emit a typed incident outside ordinary repair flows.

**Testable consequences:**

- No automatic production retry occurs.

- Control Tower escalates severity.

**Failure examples:**

- A signature failure is treated as a transient provider timeout.

**Traceability:** `D014` · `UJ-13`, `UJ-01`, `UJ-14` · `NFR-SEC-001`, `NFR-SEC-003`, `NFR-TRACE-005`, `NFR-DATA-003`

## Feature failure conditions

- Unsigned message changes state.

- Retry confused with replay.

- Audit chain has gaps or mutable history.

## Explicitly out of scope

- Organization-wide IAM platform

- Encryption implementation details reserved for Architecture


---

# F15 — Delegation Observability, SLOs, Conformance, and Resilience

## User outcome

Operators and release gates can prove that cross-product delegation is healthy, compatible, secure, and recoverable.

## Product behavior

The validated Harness Control Tower gains protocol projections; explicit SLOs and executable producer/consumer, authority, lifecycle, compatibility, resilience, and Format 02 suites protect the boundary.

## Brownfield baseline

The Builder and VAE PRDs already mandate event-sourced Control Tower views and benchmark-based certification.

## Required product delta

Specify protocol projections, metrics/SLOs, conformance suites, failure injection, and incident integration.

## Traceability

- **Locked decision:** `D015`

- **User journeys:** `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13`

- **Cross-cutting NFRs:** `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

## Functional Requirements

### FR-113 — Control Tower delegation projection

**Requirement:** The protocol shall project correlation lifecycle, products, negotiated versions, authority, budget, timing, latest event, exceptions, acknowledgements, and invalidation impact into the existing Control Tower.

**Testable consequences:**

- Projection references canonical messages and receipts.

- No separate operational source of truth is created.

**Failure examples:**

- A standalone dashboard maintains its own delegation status.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-114 — Reliability and health metrics

**Requirement:** The system shall measure acceptance, delivery, duplicate suppression, transition validity, acknowledgement, event delivery, audit completeness, and stalled/orphaned work.

**Testable consequences:**

- Metrics are dimensioned by product and version.

- Release gates can consume them.

**Failure examples:**

- Only HTTP request count is measured.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-115 — Latency and freshness SLOs

**Requirement:** The protocol shall define and report SLOs for submission receipt, event delivery, projection freshness, acknowledgement, cancellation, amendment, and critical invalidation propagation.

**Testable consequences:**

- Breaches create operational events.

- Quality thresholds are not weakened to meet SLOs.

**Failure examples:**

- Latency is measured only for completed happy paths.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-116 — Producer and consumer contract tests

**Requirement:** Every product shall pass executable fixtures for all message versions it claims to emit or consume.

**Testable consequences:**

- Fixtures include valid and invalid cases.

- Contract release is blocked on failure.

**Failure examples:**

- Schemas are reviewed manually without runtime tests.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-117 — Authority and lifecycle tests

**Requirement:** The conformance suite shall exercise prohibited actors, illegal transitions, stale messages, idempotency, replay, and terminal-state behavior.

**Testable consequences:**

- Every prohibited action is rejected deterministically.

- Expected audit receipts are asserted.

**Failure examples:**

- Only valid happy-path submissions are tested.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-118 — Compatibility and migration tests

**Requirement:** The suite shall cover same-version, minor compatibility, lossless adapter, migration-required, unsupported feature, and deprecated-version behavior.

**Testable consequences:**

- Manifest claims are evidence-backed.

- Semantic preservation is asserted.

**Failure examples:**

- A migration is tested only for JSON validity.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-119 — Resilience and fault-injection tests

**Requirement:** The suite shall inject duplicate/out-of-order messages, bus interruption, service restart, audit-store interruption, timeouts, and delayed acknowledgement.

**Testable consequences:**

- No duplicate production or illegal state results.

- Recovery receipts identify actions.

**Failure examples:**

- Boundary restart loses correlations.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

### FR-120 — Format 02 end-to-end conformance

**Requirement:** Release 1 shall include single-asset, Delegation Set, supersession, escalation, amendment, cancellation, acknowledgement, invalidation/replacement, authority, and migration scenarios for Minimal Coach Theatre.

**Testable consequences:**

- All scenarios are automated and traceable to requirements.

- Downstream Remotion consumption is represented.

**Failure examples:**

- Format 02 certification covers only one successful asset.

**Traceability:** `D015` · `UJ-14`, `UJ-02`, `UJ-10`, `UJ-13` · `NFR-OBS-001`, `NFR-PERF-002`, `NFR-RES-003`, `NFR-GOV-006`

## Feature failure conditions

- Control Tower projection diverges from audit history.

- Compatibility claimed without tests.

- Fault injection creates duplicate VAE production.

## Explicitly out of scope

- VAE internal GPU monitoring

- Builder-wide observability beyond delegation


---

# F16 — Delegation Readiness, Development Capsule, and Production Certification

## User outcome

Implementation begins only when the shared boundary is complete, testable, architecture-preserving, and proven across both products.

## Product behavior

The formal gate requires product-boundary proof, full contract family, authority/lifecycle/compatibility artifacts, Format 02 fixtures, integrity/resilience evidence, Control Tower projection, conformance suite, and Development Capsule.

## Brownfield baseline

The upstream PRDs both define formal Implementation Authorization Gates and explicitly defer final shared contract ownership to this PRD.

## Required product delta

Compile delegation-specific readiness states, hard gates, prohibitions, Development Capsule requirements, and production certification path.

## Traceability

- **Locked decision:** `D016`

- **User journeys:** `UJ-14`, `UJ-01`, `UJ-02`

- **Cross-cutting NFRs:** `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

## Functional Requirements

### FR-121 — Architecture-preservation gate

**Requirement:** Implementation authorization shall require a passing machine-readable preservation check against the validated Builder, Content Harness, and VAE authority boundaries.

**Testable consequences:**

- Conflicts block authorization.

- Amendment routes are documented.

**Failure examples:**

- A protocol service acquires creative ranking authority.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-122 — Decision and requirements completeness

**Requirement:** All 16 decisions, FRs, NFRs, non-goals, traceability, glossary, assumptions, and success metrics shall be complete and mechanically validated.

**Testable consequences:**

- No orphan requirement remains.

- Open blockers are explicit.

**Failure examples:**

- Implementation starts from conversation notes only.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-123 — Shared contract-family gate

**Requirement:** All required message schemas, examples, owners, versions, and registry entries shall validate before authorization.

**Testable consequences:**

- Representative positive and negative fixtures exist.

- Provisional contracts are marked accurately.

**Failure examples:**

- The result-acknowledgement contract is designed during coding.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-124 — Authority and lifecycle executable proof

**Requirement:** The Authority Matrix and Lifecycle Machine shall be executable and pass prohibited-action and illegal-transition tests.

**Testable consequences:**

- Field-level authority is covered.

- Every exceptional path has a terminal or recovery route.

**Failure examples:**

- Authority exists only as prose.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-125 — Compatibility and integrity proof

**Requirement:** At least one reference Content Harness and VAE compatibility manifest, negotiation, adapter, migration, signature, replay, and audit-chain path shall pass.

**Testable consequences:**

- Pinned versions are demonstrated.

- Failure cases are included.

**Failure examples:**

- Only same-version unsigned fixtures are tested.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-126 — Format 02 cross-product fixture readiness

**Requirement:** The Minimal Coach Theatre reference slice shall provide the complete scenario portfolio and valid contracts needed by both products.

**Testable consequences:**

- Fixtures use real Visual Syntax and character/scene roles.

- Set-level and replacement flows are included.

**Failure examples:**

- Reference fixtures are generic stock-image examples.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-127 — Development Capsule completeness

**Requirement:** The package shall define the required approved PRD, Architecture/ADRs, schemas, matrices, lifecycle, taxonomy, fixtures, conformance suite, deployment, observability, migration, rollback, epics, stories, specs, and authorization receipt.

**Testable consequences:**

- Each artifact traces to requirements.

- Implementation teams do not invent shared semantics.

**Failure examples:**

- A repository scaffold is delivered without authority or compatibility artifacts.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

### FR-128 — Staged certification states

**Requirement:** The protocol shall progress through PRD approval, Architecture, contract validation, cross-product fixtures, passing conformance, implementation authorization, Format 02 certification, and production certification.

**Testable consequences:**

- No state is skipped silently.

- Certification scope and limitations are explicit.

**Failure examples:**

- One successful request is labeled production-certified.

**Traceability:** `D016` · `UJ-14`, `UJ-01`, `UJ-02` · `NFR-GOV-001`, `NFR-GOV-006`, `NFR-TRACE-005`, `NFR-REL-005`

## Feature failure conditions

- Implementation authorized without complete contract family.

- Protocol changes frozen architectures.

- Certification scope overstated.

## Explicitly out of scope

- Implementing final products

- Certifying non-Format02 categories in Release 1


---

# 6. Cross-Cutting Non-Functional Requirements

These requirements apply across all protocol features and product implementations.

## NFR-AUTH — Authority and sovereignty

### NFR-AUTH-001

Every authority-bearing field and action shall map to exactly one owning product or protocol service.

### NFR-AUTH-002

Authority validation shall be deterministic and complete before any lifecycle mutation.

### NFR-AUTH-003

Budget, cancellation, amendment, result, and revocation actions shall require an authenticated permitted principal.

### NFR-AUTH-004

Automatic policy decisions shall be bounded by explicit fields, ranges, versions, and owning authority.

### NFR-AUTH-005

No adapter, migration, projection, or transport shall transfer creative or production authority implicitly.

## NFR-CONTRACT — Contract quality and schema discipline

### NFR-CONTRACT-001

All state-changing payloads shall be immutable, versioned, schema-validatable, and hash-addressable.

### NFR-CONTRACT-002

Every authoritative reference shall identify its exact version and content hash.

### NFR-CONTRACT-003

Failure and exception contracts shall contain stable classification, ownership, recovery, and invalidation semantics.

### NFR-CONTRACT-004

Delegation Set schemas shall preserve member-level identity and lifecycle while expressing shared constraints.

### NFR-CONTRACT-005

Compatibility and migration shall preserve all mandatory semantics, not merely syntactic parseability.

## NFR-LIFE — Lifecycle correctness

### NFR-LIFE-001

The shared lifecycle shall be represented by an executable deterministic transition machine.

### NFR-LIFE-002

Supersession shall prevent stale result promotion and preserve valid reusable work.

### NFR-LIFE-003

COMPLETED shall require valid production acceptance and downstream consumption acknowledgement.

### NFR-LIFE-004

Cancellation shall stop new work promptly, checkpoint safely, and prevent later stale promotion.

### NFR-LIFE-005

Delegation Set status shall be derived from member state and declared completion policy.

## NFR-REL — Reliability, idempotency, and consistency

### NFR-REL-001

Every accepted state change shall be idempotent under legitimate duplicate delivery.

### NFR-REL-002

Shared lifecycle projection shall be reconstructible from accepted immutable messages and receipts.

### NFR-REL-003

Selective invalidation shall preserve unaffected evidence and outputs with explicit lineage.

### NFR-REL-004

Automatic result acknowledgement shall be deterministic for identical current dependencies.

### NFR-REL-005

Message races shall resolve through accepted order, causation, precedence, and lifecycle state rather than network timing.

## NFR-COMPAT — Compatibility and evolution

### NFR-COMPAT-001

Products shall publish signed machine-readable compatibility manifests for every release.

### NFR-COMPAT-002

Negotiation shall verify required behaviors, authority, profiles, and receipts in addition to schema versions.

### NFR-COMPAT-003

Running delegations shall pin negotiated versions and shall not silently upgrade.

### NFR-COMPAT-004

Adapters and migrations shall be deterministic, versioned, fixture-tested, and semantically lossless for required fields.

### NFR-COMPAT-005

Deprecation shall preserve accepted in-flight delegations and publish replacement and retirement timelines.

## NFR-SEC — Security and integrity

### NFR-SEC-001

Every state-changing principal shall be authenticated and authorized for the exact requested action.

### NFR-SEC-002

Message and payload integrity shall be verifiable before persistence or routing.

### NFR-SEC-003

Replay protection shall distinguish benign idempotent retry from unauthorized message replay.

### NFR-SEC-004

Credentials shall support issuance, rotation, revocation, and historical verification.

### NFR-SEC-005

Integrity and authority failures shall block state change and emit a security incident without ordinary retry.

## NFR-TRACE — Traceability and auditability

### NFR-TRACE-001

Every protocol action shall trace to source decision, requirement, message, principal, and resulting lifecycle effect.

### NFR-TRACE-002

Demand-owned values shall retain evidence of owner, version, hash, and supersession lineage.

### NFR-TRACE-003

Correlation and causation shall connect every message and receipt in a delegation.

### NFR-TRACE-004

Lifecycle projections shall identify the authoritative message and transition rule.

### NFR-TRACE-005

Selective invalidation shall explain field changes, preserved artifacts, invalidated artifacts, and resume point.

## NFR-OBS — Observability and operations

### NFR-OBS-001

Delegation state shall be visible through the validated Harness Control Tower, not a second source of truth.

### NFR-OBS-002

Every non-terminal failure shall expose responsible owner, next action, retry class, and remaining quality rounds.

### NFR-OBS-003

Control Tower projections shall expose compatibility, authority, budget, timing, latest event, exceptions, and acknowledgements.

### NFR-OBS-004

Stalled, orphaned, superseded-but-producing, and unacknowledged delegations shall be detectable.

### NFR-OBS-005

Critical invalidation, revocation, integrity, and audit-chain incidents shall trigger operational escalation.

## NFR-PERF — Performance and service levels

### NFR-PERF-001

Budget validation and escalation shall prevent unapproved work from exceeding hard ceilings.

### NFR-PERF-002

The protocol shall define measurable SLOs for acceptance, event delivery, projection freshness, acknowledgement, and critical notice propagation.

### NFR-PERF-003

Boundary validation shall add bounded overhead independent of asset-generation duration.

### NFR-PERF-004

Large media shall be referenced rather than copied through protocol messages.

## NFR-RES — Resilience and recovery

### NFR-RES-001

Cancellation, restart, and transport interruption shall preserve safe checkpoints and immutable receipts.

### NFR-RES-002

Infrastructure failures shall be recoverable without consuming visual quality-repair rounds.

### NFR-RES-003

Duplicate, delayed, out-of-order, and temporarily undeliverable messages shall not create duplicate production or illegal transitions.

### NFR-RES-004

Boundary-service restart shall restore projections and idempotency state from durable records.

### NFR-RES-005

Audit-store interruption shall fail safely and prevent unaudited state-changing acceptance.

## NFR-DATA — Data retention, privacy, and historical truth

### NFR-DATA-001

Delegation Sets and member contracts shall retain independent lineage and exact consumed versions.

### NFR-DATA-002

Invalidated, revoked, superseded, and replaced artifacts shall remain historically reproducible under retention policy.

### NFR-DATA-003

Protocol messages shall minimize data and exclude secrets, large media, and unnecessary private reasoning traces.

### NFR-DATA-004

Large resources shall use access-controlled stable references and hashes with retention and availability policies.

### NFR-DATA-005

Negative and revoked evidence may support diagnosis and evaluation but shall be excluded from ordinary production reuse.

## NFR-GOV — Governance, quality, and certification

### NFR-GOV-001

The protocol shall preserve the validated Builder, Content Harness, and Visual Asset Editor architectures.

### NFR-GOV-002

Semantic, Activative, sequence, composition, identity, and continuity authority shall not be silently weakened.

### NFR-GOV-003

Cost, latency, or convenience shall never override constitutional quality or authority gates.

### NFR-GOV-004

Compatibility claims shall require executable evidence against declared fixtures.

### NFR-GOV-005

Constitutional amendments shall route upstream and cannot be approved through ordinary delegation.

### NFR-GOV-006

Production certification shall declare exact product versions, contract versions, profile scope, limitations, rollback, and conformance evidence.


---

# 7. Shared Delegation Lifecycle

The external lifecycle describes the cross-product commitment. It does not expose Visual Asset Editor production nodes or Content Harness internal sequencing states.

## States

- **`DRAFT`** — Demand exists under Content Harness authority but has not been submitted. Owner: `content_harness`. Terminal: `false`.

- **`SUBMITTED`** — A valid submission message is under boundary validation or has entered routing. Owner: `content_harness`. Terminal: `false`.

- **`REJECTED`** — Submission failed contract, authority, integrity, compatibility, or admission validation. Owner: `delegation_protocol`. Terminal: `true`.

- **`ACCEPTED`** — The VAE accepted the negotiated demand for execution. Owner: `visual_asset_editor`. Terminal: `false`.

- **`IN_PROGRESS`** — Production is active; internal details remain product-private. Owner: `visual_asset_editor`. Terminal: `false`.

- **`RESULT_READY`** — A production-accepted Asset Result awaits downstream acknowledgement. Owner: `visual_asset_editor`. Terminal: `false`.

- **`RESULT_REJECTED`** — The current result failed downstream compatibility acknowledgement for a stable protocol reason. Owner: `content_harness`. Terminal: `false`.

- **`COMPLETED`** — A valid result was acknowledged and the delegation completed. Owner: `delegation_protocol`. Terminal: `true`.

- **`AMENDMENT_REQUIRED`** — Execution cannot continue without a demand-owned or policy-owned change. Owner: `visual_asset_editor`. Terminal: `false`.

- **`SUPERSEDED`** — This demand version was replaced by a newer authoritative version. Owner: `content_harness`. Terminal: `true`.

- **`COST_APPROVAL_REQUIRED`** — Further work requires a new budget authorization. Owner: `visual_asset_editor`. Terminal: `false`.

- **`CAPABILITY_GAP`** — No certified production capability can satisfy the current demand. Owner: `visual_asset_editor`. Terminal: `false`.

- **`HUMAN_REVIEW_REQUIRED`** — Automation reached a governed exception boundary. Owner: `visual_asset_editor`. Terminal: `false`.

- **`CANCELLATION_REQUESTED`** — A validated cancellation request blocks new work pending safe stop. Owner: `content_harness`. Terminal: `false`.

- **`CANCELLED`** — Production stopped safely and a disposition receipt was emitted. Owner: `visual_asset_editor`. Terminal: `true`.

- **`PARTIAL_RESULT_READY`** — A typed subset is ready under the declared completion policy. Owner: `visual_asset_editor`. Terminal: `false`.

- **`INVALIDATED`** — The result requires revalidation for current use; history remains valid. Owner: `owning_product`. Terminal: `true`.

- **`REVOKED`** — The result or asset is blocked for new and active consumption. Owner: `visual_asset_editor_or_integrity_authority`. Terminal: `true`.

- **`REPLACED`** — A governed replacement was validated for future use. Owner: `owning_product`. Terminal: `true`.

## Canonical transitions

| From | To | Authoritative trigger | Authority |

|---|---|---|---|

| `DRAFT` | `SUBMITTED` | `visual_asset_submission` | `content_harness` |

| `SUBMITTED` | `REJECTED` | `submission_receipt.rejected` | `delegation_protocol` |

| `SUBMITTED` | `ACCEPTED` | `submission_receipt.accepted` | `visual_asset_editor` |

| `ACCEPTED` | `IN_PROGRESS` | `visual_asset_event.execution_started` | `visual_asset_editor` |

| `IN_PROGRESS` | `RESULT_READY` | `asset_result_contract` | `visual_asset_editor` |

| `IN_PROGRESS` | `PARTIAL_RESULT_READY` | `asset_result_contract.partial` | `visual_asset_editor` |

| `RESULT_READY` | `COMPLETED` | `result_acknowledgement.accepted` | `content_harness` |

| `RESULT_READY` | `RESULT_REJECTED` | `result_acknowledgement.rejected` | `content_harness` |

| `RESULT_REJECTED` | `IN_PROGRESS` | `visual_asset_event.revalidation_started` | `visual_asset_editor` |

| `ACCEPTED` | `AMENDMENT_REQUIRED` | `amendment_proposal` | `visual_asset_editor` |

| `IN_PROGRESS` | `AMENDMENT_REQUIRED` | `amendment_proposal` | `visual_asset_editor` |

| `AMENDMENT_REQUIRED` | `SUPERSEDED` | `demand_supersession` | `content_harness` |

| `ACCEPTED` | `COST_APPROVAL_REQUIRED` | `budget_escalation_request` | `visual_asset_editor` |

| `IN_PROGRESS` | `COST_APPROVAL_REQUIRED` | `budget_escalation_request` | `visual_asset_editor` |

| `COST_APPROVAL_REQUIRED` | `IN_PROGRESS` | `budget_escalation_response.approved` | `content_harness` |

| `COST_APPROVAL_REQUIRED` | `CAPABILITY_GAP` | `budget_escalation_response.denied_capability_gap` | `content_harness` |

| `ACCEPTED` | `CAPABILITY_GAP` | `delegation_failure.capability_gap` | `visual_asset_editor` |

| `IN_PROGRESS` | `CAPABILITY_GAP` | `delegation_failure.capability_gap` | `visual_asset_editor` |

| `ACCEPTED` | `HUMAN_REVIEW_REQUIRED` | `delegation_failure.human_exception` | `visual_asset_editor` |

| `IN_PROGRESS` | `HUMAN_REVIEW_REQUIRED` | `delegation_failure.human_exception` | `visual_asset_editor` |

| `SUBMITTED` | `CANCELLATION_REQUESTED` | `cancellation_request` | `content_harness` |

| `ACCEPTED` | `CANCELLATION_REQUESTED` | `cancellation_request` | `content_harness` |

| `IN_PROGRESS` | `CANCELLATION_REQUESTED` | `cancellation_request` | `content_harness` |

| `CANCELLATION_REQUESTED` | `CANCELLED` | `cancellation_receipt` | `visual_asset_editor` |

| `SUBMITTED` | `SUPERSEDED` | `demand_supersession` | `content_harness` |

| `ACCEPTED` | `SUPERSEDED` | `demand_supersession` | `content_harness` |

| `IN_PROGRESS` | `SUPERSEDED` | `demand_supersession` | `content_harness` |

| `COMPLETED` | `INVALIDATED` | `invalidation_notice` | `owning_product` |

| `COMPLETED` | `REVOKED` | `revocation_notice` | `visual_asset_editor_or_integrity_authority` |

| `COMPLETED` | `REPLACED` | `replacement_notice_and_ack` | `owning_product` |

| `INVALIDATED` | `REPLACED` | `replacement_notice_and_ack` | `owning_product` |

| `REVOKED` | `REPLACED` | `replacement_notice_and_ack` | `owning_product` |

## Projection rules

- Product events change shared state only after envelope, schema, authority, compatibility and transition validation.
- Internal progress events may update observability while preserving the same shared state.
- Terminal states reject ordinary progress events.
- Post-completion invalidation, revocation and replacement use dedicated message types.
- The projection must be reconstructible from the append-only audit sequence.


---

# 8. Success Metrics and Counter-Metrics

## SM-01 — Valid submission acceptance

**Definition:** Share of valid, compatible, authorized submissions accepted without manual intervention.

**Target:** >= 99.5%

**Validates:** `FR-001`, `FR-017`, `FR-113`

## SM-02 — Unauthorized mutation rejection

**Definition:** Recall for attempts to change fields outside the sender's authority.

**Target:** 100% in conformance suite

**Validates:** `FR-009`, `FR-014`, `FR-106`

## SM-03 — Duplicate production prevention

**Definition:** Rate at which duplicate or replayed submissions avoid starting duplicate VAE executions.

**Target:** 100%

**Validates:** `FR-022`, `FR-109`, `FR-124`

## SM-04 — Lifecycle transition validity

**Definition:** Accepted shared transitions conforming to the lifecycle machine.

**Target:** 100%

**Validates:** `FR-027`, `FR-030`, `FR-119`

## SM-05 — Automatic result acknowledgement

**Definition:** Eligible RESULT_READY messages acknowledged automatically within the SLO.

**Target:** >= 99%

**Validates:** `FR-043`, `FR-046`, `FR-120`

## SM-06 — Selective reuse precision

**Definition:** Preserved artifacts later confirmed valid after supersession or repair.

**Target:** >= 98%

**Validates:** `FR-036`, `FR-038`

## SM-07 — Stale result prevention

**Definition:** Superseded, cancelled, invalidated, or incompatible results entering current composition.

**Target:** 0

**Validates:** `FR-037`, `FR-062`, `FR-045`

## SM-08 — Compatibility truthfulness

**Definition:** Declared compatibility paths that pass semantic conformance fixtures.

**Target:** 100%

**Validates:** `FR-081`, `FR-088`, `FR-121`

## SM-09 — Audit completeness

**Definition:** State-changing messages with complete chained audit receipts.

**Target:** 100%

**Validates:** `FR-006`, `FR-110`, `FR-118`

## SM-10 — Cancellation response

**Definition:** Time from accepted cancellation to blocking new work and producing disposition receipt.

**Target:** p99 <= 10 seconds for boundary actions

**Validates:** `FR-058`, `FR-064`

## SM-11 — Critical notice propagation

**Definition:** Time to project critical revocation/invalidation to affected active consumers.

**Target:** p99 <= 10 seconds

**Validates:** `FR-099`, `FR-103`, `FR-116`

## SM-12 — Format 02 conformance

**Definition:** Mandatory reference scenarios passing for the pinned product/protocol versions.

**Target:** 100% before production certification

**Validates:** `FR-120`, `FR-126`

## SM-C1 — Message count *(counter-metric)*

Do not optimize for generating more messages; prefer the minimum complete auditable exchange.

**Counterbalances:** SM-01, SM-04

## SM-C2 — Adapter usage *(counter-metric)*

Do not optimize for high adapter use; direct compatible contracts are preferable.

**Counterbalances:** SM-08

## SM-C3 — Protocol-owned decisions *(counter-metric)*

Do not optimize for more decisions inside the protocol; creative and production authority must remain in products.

**Counterbalances:** SM-02


---

# 9. Non-Goals and Architectural Anti-Goals

These are binding product boundaries, not optional preferences.

- **AP-001:** The protocol must not become a third creative, Activative, composition, or production authority.

- **AP-002:** The protocol must not mutate an accepted Visual Asset Demand or completed result in place.

- **AP-003:** The Visual Asset Editor must not redefine Content Harness semantic, Activative, sequence, composition, identity, continuity, or wrong-reading authority.

- **AP-004:** The Content Harness must not dictate internal ComfyUI, model, LoRA, candidate, or repair execution through the shared protocol.

- **AP-005:** The protocol must not duplicate visual-quality evaluation or rank creative amendments.

- **AP-006:** Unsupported mandatory fields or features must not be silently ignored.

- **AP-007:** Arbitrary product status strings must not alter shared lifecycle state.

- **AP-008:** Historical contracts, messages, results, assets, and receipts must not be overwritten.

- **AP-009:** Idempotent retry and replay must not be treated as the same condition.

- **AP-010:** Unsigned, corrupted, expired, replayed, or unauthorized messages must not affect protocol state.

- **AP-011:** Stale, cancelled, superseded, invalidated, or revoked results must not enter current composition without governed revalidation.

- **AP-012:** Budget Programs, ceilings, quality gates, or required evaluations must not be silently reduced.

- **AP-013:** Adapters and migrations must not be lossy for semantic, Activative, authority, continuity, composition, or hard-gate fields.

- **AP-014:** Revoked or invalidated artifacts must not be deleted from historical evidence solely to simplify current state.

- **AP-015:** Internal VAE production nodes must not become public lifecycle states.

- **AP-016:** Compatibility must not be claimed solely because JSON parses.

- **AP-017:** Cancellation must not destructively erase reusable evidence or permit late stale promotion.

- **AP-018:** A Delegation Set must not erase independent member demand, asset, evaluation, or repair lineage.

- **AP-019:** The protocol must not authorize constitutional changes that belong to Builder governance.

- **AP-020:** Implementation must not be authorized without cross-product fixtures and a passing conformance suite.


---

# 10. Release 1 Scope and Certification

## In scope

Release 1 implements and certifies the shared protocol through the Format 02 Minimal Coach Theatre reference integration:

- a registered Content Harness principal and Visual Asset Editor principal;
- immutable demand submission and receipt;
- pinned compatibility negotiation;
- one successful single-asset delegation;
- one multi-asset Delegation Set;
- one demand supersession and selective invalidation;
- one budget escalation;
- one constraint conflict and accepted amendment;
- one safe cancellation;
- one result acknowledgement;
- one post-completion invalidation and replacement;
- one authority violation;
- one replay test;
- one contract migration;
- one complete append-only audit chain;
- Control Tower lifecycle projection;
- downstream Remotion-consumption acknowledgement.

## Structurally defined but not production-certified in Release 1

- categories and format profiles beyond the Format 02 reference path;
- multi-shot temporal asset sets;
- cross-organization federation;
- broad external marketplace interoperability;
- automatic recall of already-published media.

## Certification sequence

```text
PROTOCOL_PRD_DRAFT
→ PROTOCOL_PRD_APPROVED
→ ARCHITECTURE_IN_PROGRESS
→ CONTRACT_FAMILY_VALIDATED
→ CROSS_PRODUCT_FIXTURES_READY
→ CONFORMANCE_SUITE_PASSING
→ IMPLEMENTATION_AUTHORIZED
→ FORMAT02_INTEGRATION_CERTIFIED
→ PRODUCTION_PROTOCOL_CERTIFIED
```

A release receipt must name exact Content Harness, VAE, protocol, message, category-profile, adapter, migration and conformance-suite versions.


---

# 11. Risks and Mitigations

| Risk | Failure mode | Primary mitigation |
|---|---|---|

| Authority leakage | A boundary service gradually starts making semantic or production choices. | Executable Authority Matrix, prohibited-action tests, preservation gate. |

| Contract sprawl | Many message variants become difficult to understand or maintain. | Single-purpose registry, version discipline, deprecation and conformance. |

| Lifecycle divergence | Projection, product state and audit history disagree. | Event-sourced reconstruction tests and projection freshness SLO. |

| False compatibility | Consumers parse messages but fail to enforce required behavior. | Semantic negotiation and feature-level conformance. |

| Stale result consumption | Late results enter a newer sequence or composition. | Version/hash acknowledgement, supersession and invalidation gates. |

| Duplicate production | Retry or replay starts multiple expensive VAE runs. | Idempotency, nonce/replay controls and durable submission receipts. |

| Cancellation corruption | Hard stops damage artifacts or permit stale promotion. | Nearest-safe-checkpoint policy and disposition receipt. |

| Audit gaps | State changes occur while audit storage is unavailable. | Fail-safe acceptance gate and chained receipts. |

| Excessive protocol coupling | Internal VAE nodes leak into the public lifecycle. | Stable projection layer and privacy boundary. |

| Migration drift | Adapters or migrations drop authority-bearing information. | Lossless transformation rules, equivalence fixtures and owner review. |

| Operational overload | Too many events or controls make the boundary expensive. | Minimum Complete Contract, references for large payloads, SLO tuning. |

| Premature certification | A happy-path demo is mistaken for production readiness. | Format 02 scenario portfolio, resilience and authority suites. |


---

# 12. Assumptions and Open Questions

- **A-01** `accepted` — The validated Builder and Visual Asset Editor PRDs remain authoritative upstream architecture sources. Owner: `product governance`.

- **A-02** `accepted` — The first production cross-product reference slice is Format 02 Minimal Coach Theatre. Owner: `Release 1`.

- **A-03** `architecture_required` — The Content Harness and VAE will have independently authenticated product identities. Owner: `security architecture`.

- **A-04** `architecture_required` — Large assets and canonical contracts will reside in governed storage reachable through stable references and hashes. Owner: `data architecture`.

- **A-05** `accepted` — The shared protocol may use HTTP, queues, event streams, or local fixtures without changing semantics. Owner: `protocol architecture`.

- **A-06** `accepted` — Final public schemas from the VAE PRD remain provisional until this protocol package validates them. Owner: `delegation product`.

- **A-07** `open_non_blocking` — Exact SLO thresholds will be tuned in Architecture and benchmark phases. Owner: `operations`.

- **A-08** `accepted` — Cryptographic algorithms and key-management implementation remain Architecture decisions, while identity/integrity behavior is a product requirement. Owner: `security architecture`.

- **A-09** `accepted` — Published media cannot be silently rewritten by protocol invalidation or replacement. Owner: `Content Harness`.

- **A-10** `implementation_gate` — A complete shared conformance suite will be executable by both reference product implementations before authorization. Owner: `cross-product engineering`.

## Architecture-phase open questions

1. Which transport combination is canonical for Release 1: direct HTTP plus event bus, or queue-first?
2. Which signature algorithm, trust root, credential store and rotation interval will be used?
3. Which durable audit/event store guarantees append order and recovery?
4. How are stable resource URIs authorized and resolved across local and cloud environments?
5. What exact p95/p99 SLOs are realistic after the Format 02 compute proof?
6. Which fields are mandatory in protocol `1.0` versus reserved for `1.1`?
7. Which composition runtime principal owns automatic result acknowledgement in Release 1?


---

# 13. Source Register

The authoritative source inventory, paths, roles, hashes, and availability status are maintained in:

- [`governance/SOURCE_REGISTER.md`](../governance/SOURCE_REGISTER.md)
- [`governance/SOURCE_REGISTER.json`](../governance/SOURCE_REGISTER.json)

The principal upstream product sources are the validated Atomic Harness Builder Sharded PRD V1.1 and Visual Asset Editor Sharded PRD V1. The 16 locked decisions in this package are the canonical source for the Delegation Protocol product boundary.
