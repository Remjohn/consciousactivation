# TS-CAE-TEN-001 Risk and Rollback Register

**Document ID:** `TS-CAE-TEN-001_RISK_AND_ROLLBACK_REGISTER`  
**Phase ID:** `CA-TS-01`  
**Status:** `READY_FOR_DEVELOPMENT` (Authorizing `CA-IMPL-01A` Staging Only)  
**Date:** 2026-08-25  
**Author:** CAE Governed Execution Agent (Gemini 3.7 Flash High / Antigravity)  
**Governing Mandates:** `09_CA_TS_01_IMPLEMENTATION_GATE_TECH_SPEC_MANDATE.md`, `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`  

---

## 1. Executive Summary & Safety Philosophy

This document details the exhaustive risk taxonomy, failure modes, mitigation controls, and step-by-step deterministic rollback procedures for the implementation of the **Tenant/Guest Vertical Slice** (`TS-CAE-TEN-001` / `CA-IMPL-01A`).

### Core Safety Doctrine
1. **Parallel Non-Destructive Execution:** All staging implementations execute in dedicated schemas (`cae.*`) and private storage prefixes (`cae-media/staging/`) without touching legacy SQLite databases.
2. **Deterministic Rollback Rehearsal:** Every migration or deployment script must include an automated down-migration and cleanup path tested during CI.
3. **Fail-Closed Security Posture:** Any failure in tenant authorization, RLS context, or hash verification results in immediate transaction termination and fail-closed state.

---

## 2. Risk Assessment & Mitigation Matrix

| Risk ID | Risk Title & Description | Severity | Likelihood | Impact Area | Mitigation & Defensive Control | Trigger Condition for Rollback |
|---|---|---|---|---|---|---|
| **`RSK-TEN-001`** | **Tenant Context Leakage via Service Role**<br>Accidental query execution using administrative connection pooler bypassing RLS. | HIGH | LOW | Multi-tenant isolation | Strict role segregation: application endpoints use restricted database role (`cae_app_user`) with mandatory `FORCE ROW LEVEL SECURITY`. | Any query returning rows belonging to a different `workspace_id`. |
| **`RSK-TEN-002`** | **Storage URL Fabricated Without File Upload**<br>Registering a `MediaAsset` as `VERIFIED` with empty or mismatched storage object. | MEDIUM | LOW | Evidence integrity | Mandatory two-phase verification: `media.verify` downloads bytes and verifies SHA-256 before marking `VERIFIED`. | Hash mismatch or missing storage object during verification. |
| **`RSK-TEN-003`** | **Guest Cross-Workspace Merging**<br>Automated heuristic merging of guests with identical names across distinct client workspaces. | HIGH | LOW | Privacy & Tenancy | Anti-Auto-Merge Law: `cae.guest` primary key is `(workspace_id, guest_id)` with zero cross-tenant lookup indices. | Any cross-workspace guest lookup query executing at runtime. |
| **`RSK-TEN-004`** | **Optimistic Concurrency Lock Exhaustion**<br>Frequent version conflicts under high concurrent step execution. | LOW | MEDIUM | Run throughput | Exponential backoff retry loop with max 3 attempts on `SemanticOperationConflict`. | Stale version error persisting after 3 retries. |
| **`RSK-TEN-005`** | **Receipt Trigger Failure on High Concurrency**<br>Database trigger blocking high-throughput append-only receipt inserts. | MEDIUM | LOW | Audit logging | Optimized PostgreSQL append-only tables with partitioned storage indices. | Insert failure on `cae.receipt` during valid operation. |
| **`RSK-TEN-006`** | **Orphaned Staging Storage Objects**<br>Transient test files remaining in Supabase Storage after test run failures. | LOW | MEDIUM | Storage hygiene | Automated `finally:` cleanup blocks in all staging test fixtures with bucket pruning scripts. | > 100 MB of orphaned test files detected during CI audit. |

---

## 3. Step-by-Step Deterministic Rollback Procedures

### 3.1 Procedure RB-01: Staging PostgreSQL Schema Teardown
In the event of a fatal schema, RLS, or model defect during `CA-IMPL-01A` staging verification:

```bash
# Step 1: Terminate active connections to the staging schema
psql -d "$STAGING_DATABASE_URL" -c "
  SELECT pg_terminate_backend(pid) 
  FROM pg_stat_activity 
  WHERE datname = current_database() AND pid <> pg_backend_pid();
"

# Step 2: Drop the staging CAE schema with cascade
psql -d "$STAGING_DATABASE_URL" -c "DROP SCHEMA IF EXISTS cae CASCADE;"

# Step 3: Verify schema removal
psql -d "$STAGING_DATABASE_URL" -c "
  SELECT count(*) FROM information_schema.schemata WHERE schema_name = 'cae';
"
# Expected output: count = 0
```

### 3.2 Procedure RB-02: Private Storage Test Object Pruning
In the event of a failed media verification test or dirty staging bucket state:

```python
# scripts/cae/rollback/prune_staging_storage.py
import os
from supabase import create_client

def prune_staging_objects():
    supabase_url = os.environ["SUPABASE_URL"]
    supabase_key = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    client = create_client(supabase_url, supabase_key)
    
    bucket = "cae-media"
    test_prefixes = ["staging-test/", "test-run-"]
    
    for prefix in test_prefixes:
        files = client.storage.from_(bucket).list(prefix)
        for file in files:
            file_path = f"{prefix}{file['name']}"
            client.storage.from_(bucket).remove([file_path])
            print(f"Pruned orphaned staging object: {file_path}")

if __name__ == "__main__":
    prune_staging_objects()
```

### 3.3 Procedure RB-03: Control State Reset
To restore the repository control state to a clean pre-implementation baseline:

1. Revert `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` to `CA_STATE_01_ACCEPTED`.
2. Delete any unapproved draft Python files in `packages/ca_runtime/src/ca_runtime/models/`.
3. Re-run `python scripts/cae/state/verify_ca_state_01.py` to confirm baseline integrity.

---

## 4. Emergency Recovery Playbook

```text
+----------------------------------------------------------------------------------------------------+
| INCIDENT LEVEL 1: Staging RLS Leak Detected                                                        |
| Action: Disable test suite immediately; drop schema 'cae'; inspect policy definition in            |
|         scripts/cae/implementation/apply_ca_impl_01a_scaffolding.py.                              |
+----------------------------------------------------------------------------------------------------+
                                                  │
                                                  v
+----------------------------------------------------------------------------------------------------+
| INCIDENT LEVEL 2: Legacy DB Accidental Touch                                                       |
| Action: Terminate process; verify file modification timestamps on *.db; restore *.db from git HEAD |
|         if any bytes changed. Escalate security incident to operator.                              |
+----------------------------------------------------------------------------------------------------+
```
