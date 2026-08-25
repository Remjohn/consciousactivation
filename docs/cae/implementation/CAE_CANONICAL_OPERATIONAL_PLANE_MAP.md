# CAE Canonical & Operational Plane Map — CA-MAP-01

**Status:** `MODEL_MAPPED_PENDING_OPERATOR_REVIEW`  
**Phase ID:** `CA-MAP-01`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/02_CA_MAP_01_SCOPE_AUTHORITY_MAPPING_MANDATE.md`  
**Authority Reference:** CAE Governance & Specification Bridge Bundle v3; Multi-Tenant Authority and Canonicalization Plan §2–§4  

---

## 1. Architectural Plane Separation

The Conscious Activation Engine enforces an absolute separation between the **Canonical Plane** (what CAE is allowed to mean and do across all installations) and the **Operational Plane** (what actually happened inside an isolated client workspace).

```text
+===================================================================================+
|                                  CANONICAL PLANE                                  |
|  (Global Vocabulary, Geometric Direction, Perceptual Delivery, Procedural Rules) |
|                                                                                   |
|  +---------------------+   +---------------------+   +-------------------------+  |
|  |    SDA Registry     |   |    SFL Registry     |   |   Primitive Registry    |  |
|  | (Direction/Geometry)|   | (Perceptual Delivery|   | (Semantic Primitives &  |  |
|  |  13 YAMLs (Pinned)  |   | 28 YAMLs (5 Quarant)|   |  Archetypes - 241/243)  |  |
|  +----------+----------+   +----------+----------+   +------------+------------+  |
|             |                         |                           |               |
|             +-------------------------+---------------------------+               |
|                                       |                                           |
|                     +-----------------+-----------------+                         |
|                     |     Harness & Runbook Templates   |                         |
|                     | (Procedural Doctrine, Contracts)  |                         |
|                     +-----------------+-----------------+                         |
+=======================================|===========================================+
                                        | (Read-Only Reference via Pinned Snapshot)
                                        v
+===================================================================================+
|                                 OPERATIONAL PLANE                                 |
|         (Client Isolation, Tenant Evidence, State Transitions, Audit Proof)       |
|                                                                                   |
|   +---------------------------------------------------------------------------+   |
|   |                       OPERATOR AUDIT & GOVERNANCE                         |   |
|   |   OperatorOrganization -> OperatorAccessPolicy -> OperatorAccessGrant     |   |
|   +-------------------------------------+-------------------------------------+   |
|                                         |                                         |
|                                         v                                         |
|   +---------------------------------------------------------------------------+   |
|   |                        WORKSPACE (TENANT BOUNDARY)                        |   |
|   |                                                                           |   |
|   |   +------------------------+             +----------------------------+   |   |
|   |   |  WorkspaceMembership   |             |           Guest            |   |   |
|   |   |   (Actor / Principal)  |             |  (Workspace-Local Entity)  |   |   |
|   |   +-----------+------------+             +--------------+-------------+   |   |
|   |               |                                         |                 |   |
|   |               +--------------------+--------------------+                 |   |
|   |                                    |                                      |   |
|   |                                    v                                      |   |
|   |                 +--------------------------------------+                  |   |
|   |                 |              Engagement              |                  |   |
|   |                 |         (Project / Campaign)         |                  |   |
|   |                 +------------------+-------------------+                  |   |
|   |                                    |                                      |   |
|   |             +----------------------+----------------------+               |   |
|   |             |                                             |               |   |
|   |             v                                             v               |   |
|   |   +-------------------+                         +-------------------+     |   |
|   |   |   MediaAsset /    |                         |    HarnessRun     |     |   |
|   |   | Immutable Evidence|                         | (Operational Run) |     |   |
|   |   | (Object Store S3) |                         +---------+---------+     |   |
|   |   +---------+---------+                                   |               |   |
|   |             |                                             |               |   |
|   |             v                                             v               |   |
|   |   +-------------------+                         +-------------------+     |   |
|   |   |  SourcePackage &  |                         |  StateAggregate & |     |   |
|   |   |   EvidenceItem    |                         | StateTransitions  |     |   |
|   |   +---------+---------+                         +---------+---------+     |   |
|   |             |                                             |               |   |
|   |             +----------------------+----------------------+               |   |
|   |                                    |                                      |   |
|   |                                    v                                      |   |
|   |                 +--------------------------------------+                  |   |
|   |                 |         AIR Semantic Assessment      |                  |   |
|   |                 +------------------+-------------------+                  |   |
|   |                                    |                                      |   |
|   |                                    v                                      |   |
|   |                 +--------------------------------------+                  |   |
|   |                 |     Receipt & ExecutionReceipt       |                  |   |
|   |                 |  (Cryptographic Audit & Proof Links) |                  |   |
|   |                 +--------------------------------------+                  |   |
|   +---------------------------------------------------------------------------+   |
+===================================================================================+
```

---

## 2. Plane Invariants & Boundary Laws

### 2.1 Canonical Plane Laws
1. **No Tenant Data:** The Canonical Plane contains zero client identifiers, guest data, interview transcripts, or operational evidence.
2. **Deterministic Versioning:** All canonical assets are addressed by immutable snapshot identifiers and SHA-256 hashes.
3. **Subordination Law:** SFL (Sensory Friction / Perceptual Functions) is strictly subordinate to SDA (Semantic Direction Authority) geometry. SFL cannot replace or override Primitive Registry primitives.
4. **Read-Only Resolution:** Operational processes read canonical registries strictly through pinned, read-only resolvers (`RegistryResolver`). Direct mutation during runtime is impossible.

### 2.2 Operational Plane Laws
1. **Workspace Tenancy Root:** `Workspace` is the sole candidate tenant boundary. Every operational entity, relation, evidence span, run, and receipt MUST include a foreign key anchoring it to its parent `workspace_id`.
2. **Local Guest Entity:** `Guest` is an entity scoped strictly to a single `Workspace`. `Guest` is NOT a global identity, tenancy key, or cross-workspace pointer.
3. **No Automatic Cross-Workspace Operations:** Automatic merging, shared vector searches, cross-workspace evidence reuse, and ambient tenant leakage are structurally prohibited by database RLS and application architecture.
4. **Anti-Self-Attesting Receipts:** Consequential state transitions produce append-only receipts (`cae.receipt`, `cae.execution_receipt`) that link to independent evidence spans. A receipt cannot serve as sole proof of its own validity.

---

## 3. The Three Authority Axes

For every object in both planes, CAE tracks three independent axes of authority:

```text
+-----------------------------------------------------------------------------------+
|                            THREE AXES OF AUTHORITY                                |
+-----------------------------------------------------------------------------------+
|  1. CANONICAL DEFINITION SOURCE                                                   |
|     - What reviewed artifact/manifest defines the semantic meaning and boundary?  |
|     - Examples: Git-tracked YAML/ZIP archives, versioned Skill markdown files.    |
+-----------------------------------------------------------------------------------+
|  2. TARGET RUNTIME REPRESENTATION                                                 |
|     - What verified relational schema or object store holds operational truth?    |
|     - Examples: PostgreSQL 17.6 relational tables (`cae.*`), private Storage.     |
+-----------------------------------------------------------------------------------+
|  3. CHANGE & PROMOTION AUTHORITY                                                  |
|     - Who is the governed role, process, or gate permitted to modify/promote it?  |
|     - Examples: Platform Architecture Lead, Workspace Admin, Gate Evaluator.      |
+-----------------------------------------------------------------------------------+
```

---

## 4. Legal Parent Chains & Containment

Every operational object must belong to a legal, unbroken parent chain anchored at `Workspace` or `OperatorOrganization`:

```text
[Administrative Governance]
OperatorOrganization
  ├── OperatorAccessPolicy
  └── OperatorAccessGrant (joins OperatorOrganization + Workspace)

[Tenant Operational Isolation]
Workspace (Tenant Root)
  ├── WorkspaceMembership (Actor)
  ├── MediaAsset (Metadata)
  │     └── Immutable Media Evidence Bytes (Object Storage Payload)
  │           └── SourcePackage
  │                 └── EvidenceItem
  │                       ├── EvidenceSpan
  │                       └── EvidenceAuthentication
  ├── Guest (Workspace-Local Entity)
  └── Engagement (Project / Campaign)
        ├── InterviewSession
        │     └── InterviewTurn
        │           └── EvidenceSpan (Anchor)
        ├── HarnessRun
        │     ├── Command
        │     ├── StateAggregate
        │     │     ├── StateTransition
        │     │     └── Event
        │     ├── SemanticAssessment
        │     │     └── AssessmentEvidenceLink (Links to EvidenceItem)
        │     └── Receipt
        │           └── ExecutionReceipt (Links to EvidenceItem via receipt_evidence_link)
        └── [Future] GuestIdentityLink (Exceptional dual-consented bridge)
```

---

## 5. Scope Classification Taxonomy

| Scope Class | Definition | Parent Anchor | Access Boundary |
|---|---|---|---|
| `GLOBAL_CANONICAL` | Platform-wide canonical doctrine, geometry, or contracts. No tenant data. | Root (No parent) | Read-only across all workspaces via pinned snapshot ID |
| `OPERATOR_AUDIT` | Cross-boundary platform governance, security policies, and administrative audit trails. | `OperatorOrganization` | Platform Security Officer only; strictly audited |
| `WORKSPACE_SCOPED` | Core tenant entity, access membership, media asset, or aggregate. | `Workspace` | Authenticated actors belonging to the specified `workspace_id` |
| `ENGAGEMENT_SCOPED`| Project, campaign, interview session, or workflow execution run. | `Workspace` -> `Engagement` | Workspace actors assigned to or authorized for the engagement |
| `GUEST_SCOPED` | Participant identity, profile, and interaction history within a workspace. | `Workspace` -> `Guest` | Local workspace operations only; no cross-workspace leakage |
| `EPHEMERAL_NONAUTHORITATIVE` | Transient cache, local scratch data, or unauthenticated candidate proposals. | Calling process | Discarded upon completion; creates no durable state |
