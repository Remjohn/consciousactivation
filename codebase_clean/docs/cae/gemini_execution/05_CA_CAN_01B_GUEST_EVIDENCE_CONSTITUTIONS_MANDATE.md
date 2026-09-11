# Gemini Execution Mandate — Phase 05 / CA-CAN-01B

**Status:** `DRAFT — BLOCKED UNTIL CA-CAN-01A OPERATOR ACCEPTANCE`  
**Phase ID:** `CA-CAN-01B`  
**Title:** Guest, Identity-Link, and Media/Evidence-Boundary Object Constitutions  
**Execution classification:** Canonical object-definition authoring only; no schema, migration, or runtime implementation  
**Required prior decision:** Ratify CA-CAN-01A and authorize CA-CAN-01B only  
**Required gate on completion:** `OPERATOR_REVIEW`

## 1. Authority and purpose

This mandate is governed by CAE Governance & Specification Bridge Bundle v3, the Phase 0 Object Constitution Protocol, the Conscious Activation Definition Grammar Bundle, accepted CA-MAP-01 and CA-AUTH-01 artifacts, ratified CA-CAN-01A constitutions, [the CAE Multi-Tenant Authority and Canonicalization Plan](../implementation/CAE_MULTI_TENANT_AUTHORITY_AND_CANONICALIZATION_PLAN.md), and [the 12-phase Gemini execution program](00_GEMINI_12_PHASE_EXECUTION_PROGRAM.md).

The purpose is to define the next operational-plane group without confusing a participant, evidence record, and object-store asset:

```text
Workspace / Engagement
       ↓
Guest (workspace-local entity)
       ├── GuestIdentityLink (exceptional mapping relation)
       └── source / immutable evidence boundary
              └── MediaAsset metadata and verification identity
                   ↔ private Storage/S3 bytes
```

The outputs must state meaning, boundaries, relations, and evidence requirements. They preserve client isolation and prevent historical contamination. They do not create a person master registry, merge Guests, authenticate semantic truth, establish E4 outcomes, implement media storage, or authorize PostgreSQL/Storage changes or a live bridge.

Guest is a semantic Entity known within a Workspace. It is not a tenant, not a universal human identity, and not permission to retrieve all records that look similar. A `GuestIdentityLink`, if justified, is an explicit, versioned relationship with limited disclosure semantics; it is not an automatic merge. A `MediaAsset` is not automatically the same thing as immutable evidence: the record describing a stored asset, its provenance, and verification lifecycle may need to be distinguished from the evidence claim supported by its bytes. The class and boundary must be settled by the approved authoring and collision-review controls.

## 2. Mandatory reading before action

Gemini SHALL read in full before planning, editing, or validation:

1. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.
2. The accepted CA-MAP-01 Scope & Authority Matrix, Plane Map, Source Crosswalk, Collision Register, and completion record.
3. The accepted CA-AUTH-01 authoring-control package.
4. All ratified CA-CAN-01A constitution files and review record.
5. `docs/cae/implementation/CAE_WP09_FIRST_VERTICAL_RUNTIME_SLICE.md` and its evaluation suite, especially the verified-byte and source-bridge boundaries.
6. `docs/cae/implementation/CAE_WP02A_FOUNDATION_PROOF.md`, `CAE_WP03_SEMANTIC_OPERATION_PROOF.md`, `CAE_WP07_EXECUTION_RECEIPTS_EVIDENCE_LINEAGE.md`, and `CAE_WP08_REALITY_CONTACT_AND_REWARD_HACKING.md`.
7. `Conscious Activation Engine Brownfield/cae_phase0/phase0/CA_ENGINE_OBJECT_CONSTITUTION.md`.
8. The Definition Grammar Bundle meta constitution, Entity, Relation, Evidence, Derived Artifact, Adversarial Asset, Receipt, and relevant class grammar files, plus its checklist and class matrix.
9. Bundle v3 `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`, `15_CAE_POSTGRES_STATE_MODEL.md`, `16_CAE_SEMANTIC_OPERATION_API_PROTOCOL.md`, and `21_CAE_STATE_CONTROL_TEST_AND_PROOF_PROTOCOL.md`.
10. Brownfield Interview/legacy source artifacts identified by the accepted Source Crosswalk. Read their executable models and repository behavior where a mapping claim depends on them.

If CA-CAN-01A is not accepted, the parent chain is unclear, or a Guest/evidence collision is blocked, the agent SHALL stop as `BLOCKED`; it may not resolve the conflict through a constitution file.

## 3. Exact object scope

The phase may author constitutions for:

- `Guest` — candidate `Entity`, locally known within one Workspace and optionally participating in multiple Engagements under approved rules;
- `GuestIdentityLink` — candidate `Crosswalk / Mapping Object` or `Relation`, explicitly linking two Guest records only under an approved basis;
- `MediaAsset` — candidate asset identity/evidence-adjacent record containing storage reference, provenance, verification lifecycle, and content metadata;
- immutable media evidence boundary — a separate `Immutable Evidence` object only if the class review establishes that the evidence claim and asset identity have distinct roles;
- a minimal `EvidenceSource` or `SourcePackage` object only if existing brownfield evidence requires it and the accepted map lists it as a direct dependency.

No constitution may be authored for Audience, GuestState, ContextPremise, Assessment, PrimitiveActivation, Harness, Receipt, Outcome, or a global Person object in this phase. Those may be named as nearest neighbors or dependencies only. A media byte, a URL, a hash, an evidence claim, and a Guest are not interchangeable concepts.

## 4. Authorized artifacts and file boundary

The agent MAY create or update only:

- `docs/cae/constitutions/CA-CAN-01B_GUEST.yaml`
- `docs/cae/constitutions/CA-CAN-01B_GUEST_IDENTITY_LINK.yaml`
- `docs/cae/constitutions/CA-CAN-01B_MEDIA_ASSET.yaml`
- `docs/cae/constitutions/CA-CAN-01B_IMMUTABLE_MEDIA_EVIDENCE.yaml` if the class review requires a split;
- `docs/cae/constitutions/CA-CAN-01B_EVIDENCE_SOURCE.yaml` only if justified by the source crosswalk;
- `docs/cae/implementation/CAE_CA_CAN_01B_CONSTITUTION_REVIEW.md`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.

Each constitution SHALL preserve all 26 Phase 0 dimensions, marked `APPLICABLE`, `INAPPLICABLE_WITH_REASON`, or `PENDING_WITH_BLOCKER`. Files cite source/version/lineage, authority axes, scope/parent chain, operations, validators, typed errors, examples, hard negatives, and version history. They contain no SQL or unevidenced runtime claim.

## 5. Constitutional laws for Guest and evidence

`Guest` SHALL be defined as a Workspace-local persistent identity for the participant as known in a bounded client context. The definition must distinguish identity continuity from dynamic GuestState, observations, interview responses, evidence, and derived interpretations. A Guest may participate in multiple Engagements only if that relation is defined without turning Engagement into a tenant boundary. Guest history is not globally reusable by default.

`Guest` SHALL not be identified or merged solely by name, email, likeness, transcript similarity, or an embedding. Such attributes may be evidence or candidates for review; they are not authorization or identity proof. Cross-workspace retrieval of Guest history is forbidden unless a separate, receipted identity-link policy is ratified. The constitution must state what the system answers about a Guest and what it must refuse to infer.

`GuestIdentityLink`, if ratified, SHALL identify subject Guest, target Guest, direction/symmetry, basis, scope, validity, disclosure limits, approval authority, revocation, and receipt. It must define whether it represents same-person likelihood, an administrative alias, a source-system crosswalk, or another relation. It must not silently merge histories, transfer evidence ownership, grant Workspace access, or make a probabilistic match canonical. A hard negative must show two Guests with matching contact fields remaining separate.

`MediaAsset` SHALL distinguish the metadata identity of private object-store bytes from the claim that those bytes support. It must define object key/reference, content version, byte count, MIME/type, hash, acquisition context, provenance, lifecycle/verification status, access boundary, retention, and derivative rules only as applicable to its class. A URL is a locator, not authenticity. A `VERIFIED` lifecycle state is not evidence unless the defined acquisition/readback/hash boundary has been satisfied.

If immutable media evidence is a separate object, it SHALL define original source, acquisition event, authenticity boundary, immutability, permitted derivatives, limits, and how it links to—but does not become identical with—the MediaAsset record. External Storage effects are not transactional database facts; the constitution must state the fresh-read verification and cleanup/repair boundary for later operations without implementing it.

All evidence objects must preserve Workspace/Engagement/Guest lineage where their scope requires it. Global canonical definitions must not reference a tenant’s evidence ID, private Storage key, or receipt. Any derived interpretation must declare provenance and non-canonical status unless separately promoted.

## 6. Required independent review and proof

The constitution author and collision reviewer SHALL run as separate passes. Hard negatives must include:

- Guest treated as a global Person or tenant;
- same name/email/embedding automatically merging Guests;
- GuestIdentityLink granting access or transferring evidence ownership;
- a link treated as semantic certainty without basis/approval;
- a MediaAsset URL treated as verified evidence;
- a database `VERIFIED` flag without Storage byte readback/hash;
- two content versions sharing an identity without version/provenance rules;
- a deleted/revoked asset still returning a valid client-scoped access path;
- global canonical objects referencing a Workspace evidence ID;
- an evidence claim being rewritten when source bytes remain unchanged;
- immutable evidence silently being replaced by a derived transcript or interpretation.

The review record SHALL include source references, class decisions, dimension statuses, parent-chain checks, authority axes, validator output, negative-fixture verdicts, unresolved issues, and artifact hashes/versions. This is E1 constitutional proof with E2 repository evidence where mapped sources are inspected; it does not prove Storage/RLS enforcement, semantic correctness, consent, E4 outcomes, or migration safety.

## 7. Completion and operator gate

CA-CAN-01B completes only when each authorized object has one primary class or an explicit blocker, every constitutional dimension is accounted for, Guest locality and no-implicit-merge law are explicit, the asset/evidence boundary is resolved or deferred, independent collision review passes, hard negatives execute, and no runtime/DDL claim is smuggled into prose.

The agent SHALL request exactly:

> **Ratify the CA-CAN-01B Guest, identity-link, and media/evidence constitutions, including the no-implicit-merge and verified-byte boundary, and authorize CA-CAN-01C only?**

After asking, Gemini SHALL stop. It has no authority to author Harness, Receipt, PRD, FR, migration, Tech Spec, schema, RLS, Storage policy, or runtime operations.

## 8. Gemini activation prompt (approximately 250 words)

You are the CAE governed execution agent for `CA-CAN-01B — Guest, Identity-Link, and Media/Evidence-Boundary Constitutions`. This mandate is blocked unless CA-CAN-01A has been explicitly ratified and its review record is complete. Read this mandate and all required references before planning or editing. You may author only the Guest, GuestIdentityLink, MediaAsset, and—if independently justified—immutable media evidence/source-package constitutions and the review record. You are not authorized to create schemas, SQL, RLS, Storage policies, migrations, APIs, runtime code, PRDs, FRs, Tech Specs, Harness/Receipt constitutions, or data changes.

Use the accepted matrix and collision register, not convenience. Guest is a Workspace-local Entity, not a tenant, global Person, or permission boundary. Do not merge Guests by name, email, similarity, or embedding. A GuestIdentityLink must have an explicit basis, scope, approval, validity, disclosure limit, revocation, and receipt; it must never silently merge histories or grant access. Treat MediaAsset identity, immutable evidence bytes, evidence claims, URLs, hashes, and derived interpretations as potentially distinct roles. A URL or database flag is not verified evidence without the defined byte-readback boundary.

Apply the correct class grammar and account for all 26 dimensions with applicable, inapplicable-with-reason, or pending-with-blocker statuses. Run constitution authoring and independent collision review separately. Execute the hard negatives in Section 6 and preserve blocked findings. Record lineage, versions, validator results, maturity, limitations, and non-claims. Update control state, commit only allowed files, ask exactly the Section 7 operator decision, and stop before CA-CAN-01C.
