# CAE Scope & Authority Mapper Skill

**Skill ID:** `cae_scope_authority_mapper`  
**Maturity:** `development_uncertified`  
**Authority:** Procedural control only; operates under CA-MAP-01 Scope & Authority Matrix.  

---

## 1. Purpose & Lane

The `cae_scope_authority_mapper` provides a strictly bounded procedure to evaluate a candidate object's plane, tenancy scope, and three distinct authority axes before any object constitution is authored.

It enforces the fundamental CAE multi-tenant invariants:
1. `Workspace` is the sole candidate tenant boundary.
2. `Guest` is a workspace-local entity, never a global tenancy key.
3. PostgreSQL/Supabase is a runtime representation, never the canonical definition source for inherited doctrine or registries.
4. Operational objects MUST NOT be declared `GLOBAL_CANONICAL`.
5. Canonical objects MUST NOT reference tenant-scoped evidence or parent chains.

---

## 2. Inputs & Preconditions

- Input MUST conform to `input_schema.yaml`.
- Requires candidate object name, proposed plane, proposed scope class, candidate primary class, brownfield source references, target runtime representation, and proposed parent chain.
- CA-MAP-01 Scope & Authority Matrix must be loaded as the baseline reference.

---

## 3. Procedure

1. **Verify Plane Classification:** Determine whether the object represents platform-wide canonical meaning (`CANONICAL_PLANE`) or tenant-isolated operational execution (`OPERATIONAL_PLANE`).
2. **Evaluate Scope Class:** Assign exactly one valid scope class (`GLOBAL_CANONICAL`, `WORKSPACE_SCOPED`, `ENGAGEMENT_SCOPED`, `GUEST_SCOPED`, `OPERATOR_AUDIT`, `EPHEMERAL_NONAUTHORITATIVE`).
3. **Disentangle Three Authority Axes:**
   - Define the **Canonical Definition Source** (Git artifact, YAML archive, PRD).
   - Define the **Target Runtime Representation** (PostgreSQL table, object store URI).
   - Define the **Change and Promotion Authority** (Governance committee, Workspace Admin).
4. **Validate Legal Parent Chain:**
   - Operational objects must trace to `Workspace` or `OperatorOrganization`.
   - Canonical objects must be root-level (no parent).
5. **Detect Scope Collisions:** If candidate mixes global and local semantics (e.g., Guest as global identity), force a collision record and mark status as `CONTRACT_CONFLICT` or `SPLIT_REQUIRED`.
6. **Emit Mapping Record & Receipt:** Output structured mapping conforming to `output_schema.yaml` and record execution receipt.

---

## 4. Prohibitions

- MUST NOT classify `Guest` as a tenancy root or global identity.
- MUST NOT classify operational runtime state as `GLOBAL_CANONICAL`.
- MUST NOT treat PostgreSQL tables as the definition source for canonical doctrine.
- MUST NOT silently resolve missing parent chains or ambiguous authority.
- MUST NOT author SQL, create schemas, or modify runtime code.

---

## 5. Escalation & Stop Conditions

- **Stop as `CONTRACT_CONFLICT`:** If the candidate proposes cross-workspace automatic merges or ambient tenant access.
- **Stop as `PENDING_OPERATOR_DECISION`:** If promotion authority or tenant ownership is ambiguous.
- **Stop as `BLOCKED`:** If required brownfield source evidence cannot be located.
