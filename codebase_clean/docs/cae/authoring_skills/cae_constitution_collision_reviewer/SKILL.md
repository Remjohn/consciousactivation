# CAE Constitution Collision Reviewer Skill

**Skill ID:** `cae_constitution_collision_reviewer`  
**Maturity:** `development_uncertified`  
**Authority:** Procedural control only; operates as an independent review gate against candidate constitutions.  

---

## 1. Purpose & Independence Law

The `cae_constitution_collision_reviewer` provides an independent, adversarial review procedure to evaluate candidate object constitutions against known failure modes, class conflations, and authority mismatches.

### Non-Negotiable Independence Rule
The collision reviewer is procedurally independent of the authoring skill. It SHALL NOT author and approve the same result. It does not resolve ambiguities silently; any detected conflict MUST be registered as `CONTRACT_CONFLICT`, `SPLIT_REQUIRED`, `PENDING_OPERATOR_DECISION`, or `BLOCKED`.

---

## 2. The Nine Collision Vectors

Every candidate constitution MUST be rigorously tested across nine vectors:

1. **Class Collision:** Conflating multiple artifact classes into a single object (e.g. Entity + Event + Packet).
2. **Plane Collision:** Mixing global canonical doctrine with operational tenant state.
3. **Scope & Tenancy Collision:** Treating `Guest` as a global tenancy key or proposing automatic cross-workspace data merges.
4. **Authority Axis Collision:** Declaring PostgreSQL/Supabase as the canonical definition source for inherited doctrine or registries.
5. **Lifecycle Collision:** Treating mutable stateful entities as immutable, or claiming unverified dynamic state is canonical.
6. **Relation & Directionality Collision:** Inverting foreign key hierarchies or omitting legal parent chains back to `Workspace`.
7. **Nearest-Neighbor Collision:** Failing to establish sharp boundaries with nearest semantic neighbors.
8. **Evidence & Receipt Collision:** Treating mechanical execution receipts as substantive proof of human truth, taste, or semantic validity (self-attestation).
9. **Storage Representation Collision:** Storing large immutable media payloads in relational database rows rather than private content-addressed object storage (ADR-003 violation).

---

## 3. Mandatory Conflation Challenges

The reviewer MUST explicitly check and reject the following specific conflations:
- `Guest = Tenant Boundary` -> REJECT (`CONTRACT_CONFLICT`)
- `Receipt = Qualitative Evaluation Proof` -> REJECT (`SPLIT_REQUIRED`)
- `MediaAsset = Raw Media Bytes in DB` -> REJECT (`SPLIT_REQUIRED`)
- `HarnessTemplate = HarnessRun` -> REJECT (`SPLIT_REQUIRED`)
- `OperatorAccessPolicy = OperatorAccessGrant` -> REJECT (`SPLIT_REQUIRED`)
- `Registry Source Archive = PostgreSQL Projection` -> REJECT (`CONTRACT_CONFLICT`)
- `Public URL = Verified Immutable Media` -> REJECT (`CONTRACT_CONFLICT`)

---

## 4. Inputs & Preconditions

- Input MUST conform to `input_schema.yaml`.
- Requires candidate constitution markdown and metadata.
- Requires CA-MAP-01 Collision Register as the baseline history.

---

## 5. Procedure

1. **Ingest Candidate Constitution:** Load and parse 26-dimension constitution.
2. **Execute 9-Vector Collision Sweep:** Apply automated and adversarial checks across all 9 vectors.
3. **Evaluate Specific Conflation Challenges:** Verify that prohibited conflations are absent.
4. **Formulate Verdict:**
   - `APPROVED_NO_COLLISIONS`: All 9 vectors clear, no conflations present.
   - `SPLIT_REQUIRED`: Candidate must be split into two or more distinct objects.
   - `CONTRACT_CONFLICT`: Violates core tenancy, plane, or authority invariants.
   - `PENDING_OPERATOR_DECISION`: Requires operator governance resolution.
   - `BLOCKED`: Upstream lineage defect or missing evidence prevents verification.
5. **Emit Review Record & Receipt:** Produce output conforming to `output_schema.yaml`.

---

## 6. Prohibitions

- MUST NOT silently edit, normalize, or repair a candidate constitution.
- MUST NOT waive any collision check for convenience.
- MUST NOT allow author and reviewer to share a single unverified execution cycle.

---

## 7. Escalation & Stop Conditions

- **Stop as `CONTRACT_CONFLICT`:** If the candidate proposes cross-workspace data merges or global guest authority.
- **Stop as `SPLIT_REQUIRED`:** If the candidate combines multiple primary classes or operational/canonical planes.
- **Stop as `BLOCKED`:** If missing evidence or unratified references prevent deterministic evaluation.

