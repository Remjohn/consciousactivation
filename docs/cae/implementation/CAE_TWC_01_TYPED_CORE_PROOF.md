# CAE Phase 25 (CA-TWC-01) Typed Tenancy Core Proof

**Phase ID:** `CA-TWC-01`  
**Mandate Sub-workstream:** `T2 — Law-Complete Typed Tenancy Core`  
**Execution Timestamp:** `2026-08-26T11:29:09Z`  
**Implementation Source:** `packages/ca_runtime/src/ca_runtime/workspace_core.py`  
**Governing Specifications:** `TS-CAE-TEN-001`, `FR-CAE-TEN-001` through `FR-CAE-TEN-005`

---

## 1. Implemented Typed Operations & Contracts

| Operation Name | Input Contract (Pydantic V2) | Output Contract | Action Type | Epistemic Status |
|---|---|---|---|---|
| `create_workspace` | `CreateWorkspaceInput` (`slug`, `display_name`) | `WorkspaceResult` | `WORKSPACE_CREATED` | `UNVERIFIED` |
| `get_workspace` | `workspace_id: UUID` | `WorkspaceResult` | N/A (Read) | N/A |
| `update_workspace` | `UpdateWorkspaceInput` (`workspace_id`, `display_name`, `status`) | `WorkspaceResult` | `WORKSPACE_UPDATED` | `UNVERIFIED` |
| `add_workspace_membership` | `AddMembershipInput` (`workspace_id`, `actor_id`, `role`) | `MembershipResult` | `MEMBERSHIP_ADDED` | `UNVERIFIED` |
| `remove_workspace_membership` | `RemoveMembershipInput` (`workspace_id`, `actor_id`) | `MembershipResult` | `MEMBERSHIP_REMOVED` | `UNVERIFIED` |
| `issue_operator_grant` | `IssueOperatorGrantInput` (`operator_org_id`, `workspace_id`, `operator_actor_id`, `justification`, `expires_at`) | `OperatorGrantResult` | `OPERATOR_GRANT_ISSUED` | `UNVERIFIED` |
| `revoke_operator_grant` | `RevokeOperatorGrantInput` (`grant_id`, `workspace_id`) | `OperatorGrantResult` | `OPERATOR_GRANT_REVOKED` | `UNVERIFIED` |

---

## 2. In-Session Verification & Countertest Results

All typed core operations were executed and verified against live Supabase PostgreSQL staging (`aws-1-eu-west-1.pooler.supabase.com:5432`).

### 1. `create_workspace`
- **Action:** Created workspace `test-ws-d94eafa4` ("Test Workspace Alpha").
- **Verification:** Workspace record created with `status = 'ACTIVE'`, creator bound as initial `ADMIN` membership, immutable receipt emitted.
- **Countertest (Duplicate Slug):** Attempted creation of second workspace with identical slug `test-ws-d94eafa4`.
  - **Result:** Raised `WorkspaceConflictError: Workspace slug 'test-ws-d94eafa4' already exists`.

### 2. `get_workspace`
- **Action:** Retrieved workspace `8eb15bee-6935-416e-b088-b83da3603fbe` under authorized workspace context.
- **Verification:** Returned `WorkspaceResult` with matching fields.
- **Countertest (Cross-Tenant Scope Forgery):** Foreign workspace actor requested workspace `8eb15bee-...`.
  - **Result:** Access denied with `WorkspaceNotFoundError: Workspace 8eb15bee-6935-416e-b088-b83da3603fbe not found or inaccessible`.

### 3. `update_workspace`
- **Action:** Updated display name to `"Updated Alpha Name"` under `ADMIN` session.
- **Verification:** Updated row committed and receipt emitted.
- **Countertest (Unauthorized Non-Admin Update):** Actor with `role = 'MEMBER'` attempted update.
  - **Result:** Raised `UnauthorizedAccessError: Only workspace ADMIN or system operator can update workspace settings`.

### 4. `add_workspace_membership`
- **Action:** Added `alice@example.com` with `role = 'MEMBER'`.
- **Verification:** Membership committed with `status = 'ACTIVE'` and receipt emitted.
- **Countertest (Duplicate Membership):** Re-attempted addition of `alice@example.com`.
  - **Result:** Raised `MembershipExistsError: Actor 'alice@example.com' is already an ACTIVE member`.

### 5. `remove_workspace_membership`
- **Action:** Removed `alice@example.com` from workspace.
- **Verification:** Membership updated to `status = 'REVOKED'` and receipt emitted.

### 6. `issue_operator_grant`
- **Action:** Issued 24-hour operator grant for `operator-alice` from operator organization `Platform Support Org Alpha`.
- **Verification:** Grant record committed with future `expires_at` timestamp and receipt emitted.
- **Countertest (Past Expiration Rejection):** Attempted to issue grant with expiration in the past.
  - **Result:** Raised `OperatorGrantExpiredError: Grant expiration time must be in the future`.

### 7. `revoke_operator_grant`
- **Action:** Revoked active grant.
- **Verification:** Grant `revoked_at` set to current timestamp, receipt emitted.

---

## 3. Emitted Receipts Audit (Live DB Read-Back)

```text
Receipt ID                           | Action Type             | Status  | Payload Hash (SHA-256)           | Timestamp (UTC)
-------------------------------------+-------------------------+---------+----------------------------------+---------------------------
78510335-292b-471e-badd-134b89c35713 | WORKSPACE_CREATED       | SUCCESS | 7738f55cdc237b31...              | 2026-08-26 09:29:06+00:00
3a2657c5-3c84-4fb0-a926-26b938cf467c | WORKSPACE_UPDATED       | SUCCESS | 46c8f7c45cbfc2c3...              | 2026-08-26 09:29:07+00:00
52d650a0-7141-438c-b527-611a0b9d864e | MEMBERSHIP_ADDED        | SUCCESS | 4756bdfa592f3f8a...              | 2026-08-26 09:29:07+00:00
62579733-2449-48e4-982d-d2d135918a88 | MEMBERSHIP_REMOVED      | SUCCESS | 2e9270ee93dcd750...              | 2026-08-26 09:29:08+00:00
af785780-57ec-48d6-8809-31e87b70b666 | OPERATOR_GRANT_ISSUED   | SUCCESS | c185044d957c19f7...              | 2026-08-26 09:29:08+00:00
9c134062-dd0e-48ec-bcbe-b38f52e844c2 | OPERATOR_GRANT_REVOKED  | SUCCESS | eea8a8262e6e1697...              | 2026-08-26 09:29:08+00:00
```

---

## 4. Sub-workstream T2 Verification Verdict

```yaml
sub_workstream: T2_TYPED_TENANCY_CORE
verdict: PASS
typed_models: Pydantic_V2_Strict
rls_session_enforcement: APPLIED_ON_ALL_OPERATIONS
receipt_emission: 100_PERCENT_TRANSITIONS_RECEIPTED
epistemic_boundaries: ALL_FIELDS_UNVERIFIED_OR_NOT_APPLICABLE
```
