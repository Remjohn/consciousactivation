---
title: F11 — Semantic Compatibility, Negotiation, Adapters, Migration, and Deprecation
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F11
decision_id: D011
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
