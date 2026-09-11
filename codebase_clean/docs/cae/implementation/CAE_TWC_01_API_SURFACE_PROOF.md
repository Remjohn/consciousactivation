# CAE Phase 25 (CA-TWC-01) API Surface Proof

**Phase ID:** `CA-TWC-01`  
**Mandate Sub-workstream:** `T3 — Versioned FastAPI Surface`  
**Execution Timestamp:** `2026-08-26T11:31:26Z`  
**Router Source:** `api/routers/v1_tenancy.py`  
**App Bootstrap:** `api/main.py` (`prefix="/api"`, tags `["tenancy-v1"]`)  
**Campaign Router Status:** `UNTOUCHED` (`api/routers/campaigns.py` byte-for-byte identical to baseline)

---

## 1. Exposed Versioned Endpoints

| HTTP Method | Route Path | Purpose | Success Code | Conflict / Denial Code |
|---|---|---|---|---|
| `POST` | `/api/v1/workspaces` | Provision new isolated workspace | `201 Created` | `409 Conflict` (Duplicate Slug) |
| `GET` | `/api/v1/workspaces/{workspace_id}` | Retrieve workspace metadata | `200 OK` | `404 Not Found` / `403 Forbidden` (RLS) |
| `PATCH` | `/api/v1/workspaces/{workspace_id}` | Update workspace display name/status | `200 OK` | `403 Forbidden` (Non-Admin) / `404 Not Found` |
| `POST` | `/api/v1/workspaces/{workspace_id}/memberships` | Add actor membership | `201 Created` | `409 Conflict` (Duplicate Membership) |
| `DELETE` | `/api/v1/workspaces/{workspace_id}/memberships/{actor_id}` | Revoke actor membership | `200 OK` | `404 Not Found` / `403 Forbidden` |
| `POST` | `/api/v1/workspaces/{workspace_id}/operator-grants` | Issue time-limited operator grant | `201 Created` | `409 Conflict` / `400 Bad Request` (Past exp) |
| `DELETE` | `/api/v1/workspaces/{workspace_id}/operator-grants/{grant_id}` | Revoke operator grant | `200 OK` | `404 Not Found` / `403 Forbidden` |

---

## 2. Live HTTP Interaction Log & Behavioral Verification

```text
1. POST /api/v1/workspaces (Provision)...
  Status: 201 | Body: {'workspace_id': 'bec86086-0378-4875-8ccc-d24d256b1052', 'slug': 'api-ws-2f5ea1e8', 'display_name': 'API Test Workspace', 'status': 'ACTIVE', 'receipt_id': 'd7c9789c-2096-412a-8a9b-e44969382f25'}

1b. POST /api/v1/workspaces duplicate slug conflict (409)...
  Status: 409 | Detail: {'detail': "Workspace slug 'api-ws-2f5ea1e8' already exists"}

2. GET /api/v1/workspaces/{workspace_id}...
  Status: 200 | Body: {'workspace_id': 'bec86086-0378-4875-8ccc-d24d256b1052', 'slug': 'api-ws-2f5ea1e8', 'display_name': 'API Test Workspace', 'status': 'ACTIVE', 'receipt_id': 'd7c9789c-2096-412a-8a9b-e44969382f25'}

2b. GET /api/v1/workspaces/{workspace_id} cross-tenant denial...
  Status: 404 | Detail: {'error_code': 'NOT_FOUND', 'message': '404: Workspace bec86086-0378-4875-8ccc-d24d256b1052 not found or inaccessible'}

3. PATCH /api/v1/workspaces/{workspace_id}...
  Status: 200 | Body: {'workspace_id': 'bec86086-0378-4875-8ccc-d24d256b1052', 'slug': 'api-ws-2f5ea1e8', 'display_name': 'API Updated Name', 'status': 'ACTIVE', 'receipt_id': 'ab6e260c-88ef-4095-8105-439a4a907ad1'}

4. POST /api/v1/workspaces/{workspace_id}/memberships...
  Status: 201 | Body: {'membership_id': '71b77ac8-1bc2-4086-8245-7e4f98d8ab44', 'workspace_id': 'bec86086-0378-4875-8ccc-d24d256b1052', 'actor_id': 'bob@api.test', 'role': 'MEMBER', 'status': 'ACTIVE', 'receipt_id': '87f62237-93bc-41fe-a76a-b302b31dce37'}

5. DELETE /api/v1/workspaces/{workspace_id}/memberships/{actor_id}...
  Status: 200 | Body: {'membership_id': '71b77ac8-1bc2-4086-8245-7e4f98d8ab44', 'workspace_id': 'bec86086-0378-4875-8ccc-d24d256b1052', 'actor_id': 'bob@api.test', 'role': 'MEMBER', 'status': 'REVOKED', 'receipt_id': '0910a02b-257b-4507-a491-82b9172bc15d'}

6. POST /api/v1/workspaces/{workspace_id}/operator-grants...
  Status: 201 | Body: {'grant_id': '4a2109d1-0087-4f88-98be-59aaeaf0f7ed', 'operator_org_id': 'f8232451-0ffa-40d8-82b1-6079fd3bb732', 'workspace_id': 'bec86086-0378-4875-8ccc-d24d256b1052', 'operator_actor_id': 'operator-charlie', 'justification': 'API support session', 'expires_at': '2026-08-26T21:31:22.379846Z', 'revoked_at': None, 'receipt_id': 'b4dd77a0-a987-4141-8f42-184d77b21575'}

7. DELETE /api/v1/workspaces/{workspace_id}/operator-grants/{grant_id}...
  Status: 200 | Body: {'grant_id': '4a2109d1-0087-4f88-98be-59aaeaf0f7ed', 'operator_org_id': 'f8232451-0ffa-40d8-82b1-6079fd3bb732', 'workspace_id': 'bec86086-0378-4875-8ccc-d24d256b1052', 'operator_actor_id': 'operator-charlie', 'justification': 'API support session', 'expires_at': '2026-08-26T21:31:22.379846Z', 'revoked_at': '2026-08-26T09:31:23.759168Z', 'receipt_id': 'e315e302-7a29-4d29-af21-c71f5b75beb0'}
```

---

## 3. Sub-workstream T3 Verification Verdict

```yaml
sub_workstream: T3_API_SURFACE
verdict: PASS
router_path: api/routers/v1_tenancy.py
campaign_router_preserved: true
response_validation: Pydantic_V2_Strict
receipt_ids_returned: true
http_status_conformance: EXACT
```
