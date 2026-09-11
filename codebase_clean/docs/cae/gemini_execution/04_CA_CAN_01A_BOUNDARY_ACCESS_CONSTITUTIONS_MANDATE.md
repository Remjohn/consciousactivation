# Gemini Execution Mandate — Phase 04 / CA-CAN-01A

**Status:** `DRAFT — BLOCKED UNTIL CA-AUTH-01 OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-CAN-01A`  
**Title:** Boundary, Access, and Engagement Object Constitutions  
**Execution classification:** Canonical object-definition authoring only; no schema or runtime implementation  
**Required prior decision:** Authorize the development-uncertified CA-AUTH-01 controls for pilot constitution work  
**Required gate on completion:** `OPERATOR_REVIEW`

## 1. Authority and purpose

This mandate is governed by CAE Governance & Specification Bridge Bundle v3, the Phase 0 Object Constitution Protocol, the Conscious Activation Definition Grammar Bundle, the accepted CA-MAP-01 artifacts, the accepted CA-AUTH-01 authoring-control package, [the CAE Multi-Tenant Authority and Canonicalization Plan](../implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md), and [the Gemini 12-Phase Execution Program](00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md).

The purpose is to author the first bounded constitutional group for the operational-plane boundary:

```text
OperatorOrganization
  -> Workspace
       -> WorkspaceMembership
       -> Engagement
  + OperatorAccessPolicy / OperatorAccessGrant
```

These definitions establish what client isolation, internal operator authority, and engagement grouping mean before any table, RLS policy, API, migration, or runtime operation is designed. They do not implement multi-tenancy. They do not make an operator a tenant, a Guest a global person, or PostgreSQL a definition source. They must preserve the three authority axes already mapped:

1. canonical definition source;
2. canonical runtime representation;
3. change/promotion authority.

The constitutional output is versioned object law. It is not a database schema disguised as prose. Each object must have one primary artifact class selected through the accepted class matrix. If the evidence does not support a class, the object remains `PENDING` and downstream work is blocked.

## 2. Mandatory reading before action

Gemini SHALL read in full before planning or editing:

1. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.
2. `docs/cae/implementation/CAE_SCOPE_AND_AUTHORITY_MATRIX.md`.
3. `docs/cae/implementation/CAE_OBJECT_SCOPE_COLLISION_REGISTER.md`.
4. `docs/cae/implementation/CAE_CANONICAL_OPERATIONAL_PLANE_MAP.md`.
5. `docs/cae/implementation/CAE_CA_MAP_01_SOURCE_CROSSWALK.md` and `CAE_CA_MAP_01_COMPLETION_RECORD.md`.
6. The accepted CA-AUTH-01 authoring Skill package, especially the constitution author and independent collision reviewer.
7. `docs/cae/implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md`.
8. `Conscious Activation Engine Brownfield/cae_phase0/phase0/CA_ENGINE_OBJECT_CONSTITUTION.md`.
9. `Conscious Activation Engine Brownfield/Conscious_Activation_Definition_Grammar_Bundle/00_META_OBJECT_CONSTITUTION.md`, the Entity, Relation, Policy/Contract, and any relevant Crosswalk grammar, plus `16_OBJECT_DEFINITION_CHECKLIST.md` and `18_OBJECT_CLASS_MATRIX.md`.
10. Relevant brownfield sources cited by the CA-MAP source crosswalk, including existing identity, campaign/project, authorization, and repository records.

If CA-AUTH-01 is not accepted, a matrix row is missing, or a collision affecting this group remains `BLOCKED`, Gemini SHALL stop and report the exact dependency. It SHALL not invent a class from the desired database shape.

## 3. Exact object scope

The phase may author constitutions for:

- `Workspace` — candidate `Entity`, the initial client isolation boundary;
- `WorkspaceMembership` — candidate `Relation`, binding an authenticated principal to a Workspace role;
- `Engagement` — candidate `Entity`, grouping a bounded project inside one Workspace;
- `OperatorAccessPolicy` — candidate `Policy / Contract`, defining conditions and permissions for internal cross-workspace access;
- `OperatorAccessGrant` — candidate `Relation` or policy-governed grant record, whose exact class must be resolved by the Collision Register rather than assumed;
- `OperatorOrganization` only if CA-MAP-01 identifies it as necessary to distinguish administrative ownership from Workspace scope.

`OperatorAccessPolicy` and `OperatorAccessGrant` must not be merged merely because both contain authorization fields. If one stable rule and one time/reason/actor-specific application are semantically distinct, author two constitutions. If evidence supports one object, record why the split is not valid. `WorkspaceMembership` is not an implicit cross-workspace operator bypass.

No Guest, media, Harness, Receipt, identity-link, registry, or state constitution may be authored in this phase except as a cited nearest neighbor or unresolved dependency. Do not author a generic “Tenant” object unless the accepted map explicitly contains it; CAE’s current proposed boundary is Workspace.

## 4. Authorized artifacts and file boundary

The agent MAY create or update only:

- `docs/cae/constitutions/CA-CAN-01A_WORKSPACE.yaml`
- `docs/cae/constitutions/CA-CAN-01A_WORKSPACE_MEMBERSHIP.yaml`
- `docs/cae/constitutions/CA-CAN-01A_ENGAGEMENT.yaml`
- `docs/cae/constitutions/CA-CAN-01A_OPERATOR_ACCESS_POLICY.yaml`
- `docs/cae/constitutions/CA-CAN-01A_OPERATOR_ACCESS_GRANT.yaml` if the class reviewer requires a separate object;
- `docs/cae/constitutions/CA-CAN-01A_OPERATOR_ORGANIZATION.yaml` only if justified by the map;
- `docs/cae/implementation/CAE_CA_CAN_01A_CONSTITUTION_REVIEW.md`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.

The constitution format SHALL preserve all 26 dimensions from the Phase 0 protocol. For each dimension, write `APPLICABLE`, `INAPPLICABLE_WITH_REASON`, or `PENDING_WITH_BLOCKER`. It must include canonical identity, artifact class, plane, role, definition, semantic boundary, nearest neighbors, taxonomy, lifecycle/canonicality, attributes, relationships, state, events, provenance, invariants, authority/owner, authorized and prohibited operations, validators, error taxonomy, storage representation, runtime consumers, questions answered, examples/hard negatives, and version history. The class-specific grammar governs the required content; no dimension may be filled with generic filler.

The review record SHALL contain an object-to-matrix crosswalk, source evidence, class decisions, unresolved collisions, independent reviewer result, hard-negative result, and exact operator decision request. It must not claim schema or runtime implementation.

## 5. Constitutional laws for this group

`Workspace` SHALL be defined as a client operational boundary, not as a synonym for Guest, Engagement, or OperatorOrganization. Its identity, owner, lifecycle, allowed relationships, retention boundary, and cross-workspace prohibition must be explicit. It must not inherit another client’s evidence or history.

`WorkspaceMembership` SHALL define subject, Workspace, role, temporal validity, authorization meaning, and revocation behavior. It must not imply access to every workspace, global identity merge, or permission to bypass typed semantic operations.

`Engagement` SHALL be subordinate to exactly one Workspace. It groups work but does not become a second tenant boundary. Its constitution must define whether a Guest may participate in multiple Engagements within one Workspace and what that relation does not imply.

`OperatorAccessPolicy` SHALL state jurisdiction, obligations, permissions, prohibitions, precedence, exceptions, evidence, and failure handling. It must preserve least privilege and auditable purpose. It must not silently authorize bulk export, cross-workspace semantic retrieval, model training, identity resolution, or source-data merging.

`OperatorAccessGrant`, if separate, SHALL define the specific actor, Workspace scope, purpose/reason, validity period, policy reference, revocation, and receipt requirement. It must not be confused with a client membership or permanent administrative identity.

All objects must identify canonical source artifact/version, runtime representation status, and promotion authority without claiming that PostgreSQL is already the runtime authority for an unverified object. Relations must preserve parent-chain containment. Any cross-workspace relation requires explicit classification and operator decision; default behavior is forbidden.

## 6. Required review and proof

The authoring Skill SHALL run a constitution completeness validator and the independent collision reviewer SHALL run separately. At minimum, hard negatives must test:

- Workspace defined as merely an alias for Guest or Engagement;
- WorkspaceMembership granting access outside its Workspace;
- Engagement becoming a hidden tenant boundary;
- OperatorAccessPolicy authorizing unrestricted admin behavior;
- OperatorAccessGrant being treated as permanent membership;
- operator access existing without purpose, expiry, or receipt;
- a class selected from a proposed SQL table;
- PostgreSQL projection silently overriding an unresolved canonical source;
- a relation crossing Workspaces without a declared link and policy.

The review must record validator commands, source references, hashes/versions of constitution artifacts, reviewer identity, unresolved findings, and maturity. This is E1 constitutional proof. It does not prove RLS, database constraints, API enforcement, Storage isolation, migration safety, or production authority.

If the independent reviewer finds a collision, the output SHALL be `PENDING`, `SPLIT`, `CONTRACT_CONFLICT`, or `BLOCKED`; Gemini may not repair the constitution and approve it in the same pass. If a proposed definition cannot distinguish Workspace from Guest, Engagement, or operator administration, it is not complete.

## 7. Completion and operator gate

CA-CAN-01A completes only when every authorized object has a primary class or an explicit pending/blocker status, all 26 dimensions are accounted for, class-specific grammar requirements pass, the independent collision review is recorded, hard negatives execute, source lineage is cited, and no downstream schema claim is implied.

The agent SHALL request exactly:

> **Ratify the CA-CAN-01A boundary/access constitutions, including the Workspace boundary and operator-access split, and authorize CA-CAN-01B only for Guest and evidence constitutions?**

After asking, Gemini SHALL stop. It has no authority to author Guest/media constitutions, PRDs, FRs, migration contracts, Tech Specs, schemas, RLS, or runtime operations.

## 8. Gemini activation prompt (approximately 245 words)

You are the CAE governed execution agent for `CA-CAN-01A — Boundary, Access, and Engagement Object Constitutions`. This mandate is blocked unless CA-AUTH-01 has been explicitly accepted and its authoring controls are available. Read this mandate and every required reference in full before planning or editing. Your authorization is only to author and independently review the Workspace, WorkspaceMembership, Engagement, OperatorAccessPolicy, and—only if the collision review requires it—OperatorAccessGrant/OperatorOrganization constitutions. You are not authorized to create SQL, schemas, RLS, Storage policies, migrations, API routes, runtime models, PRDs, FRs, Tech Specs, Guest/media/Harness/Receipt constitutions, or data changes.

Use the accepted Scope & Authority Matrix and Collision Register. Apply the correct class-specific grammar; never select a class because it is convenient for a table. Every constitution must account for all 26 dimensions using applicable, inapplicable-with-reason, or pending-with-blocker statuses. Preserve the three authority axes: canonical source, runtime projection, and change/promotion authority. Do not silently make PostgreSQL the semantic source or turn Workspace into Guest, Engagement, or OperatorOrganization.

Keep OperatorAccessPolicy separate from a specific OperatorAccessGrant unless evidence proves they are one object. Test hard negatives for cross-workspace membership, unbounded operator access, hidden tenant boundaries, implicit identity merging, and source/projection mismatch. Run the independent collision reviewer as a separate pass; a finding must remain pending, split, conflicted, or blocked rather than being silently repaired.

Create only the permitted constitution files and review record. Record evidence paths, source versions, validator results, maturity, limitations, and non-claims. Update control state, make a scoped commit, ask exactly the Section 7 decision, and stop before CA-CAN-01B.
