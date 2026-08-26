# CAE Migration 03 Schema Inventory

**Phase ID:** `CA-MIG-03`  
**Document ID:** `CAE_MIG_03_SCHEMA_INVENTORY`  
**Status:** `DESIGNED_AND_STATICALLY_REHEARSED_ONLY`  
**Date:** 2026-08-26  
**Governing Mandate:** `docs/cae/gemini_execution/15_CA_MIG_03_FORWARD_ONLY_MIGRATION_SAFETY_MANDATE.md`  

---

## 1. Inventory Methodology and Evidence Classes

This inventory documents all relational schema objects in the first-slice `cae.*` namespace. Each entry strictly distinguishes between:
1. **Desired Schema Source (Text Definition):** Defined in `TS-CAE-TEN-001`, `CA-CAN-01A/B/C`, `models/tenancy.py`.
2. **Recorded Staging Observation (E3 Proof):** Observed in `CAE_CA_IMPL_01A_FOUNDATION_PROOF.md` and `CAE_CA_IMPL_02_MC_CAE_MED_001_CUTOVER_PROOF.md`.
3. **Inspected Local Source:** Verified directly in `packages/ca_runtime/src/ca_runtime/models/tenancy.py` and `scripts/cae/implementation/apply_ca_impl_01a_scaffolding.py`.

---

## 2. Table-by-Table Relational Schema Inventory

### 2.1 `cae.workspace` (Tenant Isolation Root)
- **Purpose:** Primary tenant partition root entity.
- **Data Classification:** `OPERATIONAL_METADATA`
- **Primary Key:** `workspace_id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- **Unique Constraints:** `uq_workspace_slug UNIQUE (slug)` (VARCHAR(64))
- **Columns:**
  - `workspace_id UUID NOT NULL`
  - `slug VARCHAR(64) NOT NULL`
  - `display_name VARCHAR(255) NOT NULL`
  - `status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE'`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
  - `updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
- **RLS Policy:** Enabled; bypass for service role, workspace isolation for authenticated sessions.
- **Evidence Source:** Desired: `TS-CAE-TEN-001` Sec 3.1; Local Source: `models/tenancy.py#Workspace`; Staging: Verified Phase 10.

---

### 2.2 `cae.workspace_membership` (Actor Binding)
- **Purpose:** Binds actors to workspaces with granular roles (`ADMIN`, `MEMBER`, `OBSERVER`).
- **Data Classification:** `OPERATIONAL_METADATA`
- **Primary Key:** `membership_id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- **Foreign Keys:** `workspace_id REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE`
- **Unique Constraints:** `uq_workspace_membership_actor UNIQUE (workspace_id, actor_id)`
- **Columns:**
  - `membership_id UUID NOT NULL`
  - `workspace_id UUID NOT NULL`
  - `actor_id VARCHAR(128) NOT NULL`
  - `role VARCHAR(32) NOT NULL DEFAULT 'MEMBER'`
  - `status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE'`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
- **RLS Policy:** Enabled; isolation by `current_setting('app.current_workspace_id', true)`.
- **Evidence Source:** Desired: `TS-CAE-TEN-001` Sec 3.2; Local Source: `models/tenancy.py#WorkspaceMembership`.

---

### 2.3 `cae.operator_organization` (Governance Root)
- **Purpose:** Top-level platform operator organization envelope.
- **Data Classification:** `GOVERNANCE_METADATA`
- **Primary Key:** `operator_org_id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- **Columns:**
  - `operator_org_id UUID NOT NULL`
  - `org_name VARCHAR(255) NOT NULL`
  - `status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE'`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
- **RLS Policy:** Enabled; system operator administration.
- **Evidence Source:** Desired: `CA-CAN-01A` `OPERATOR_ORGANIZATION`; Local Source: `models/tenancy.py#OperatorOrganization`.

---

### 2.4 `cae.operator_access_grant` (Ephemeral Support Grant)
- **Purpose:** Time-bounded, justifiable support access to tenant workspaces.
- **Data Classification:** `GOVERNANCE_SECURITY`
- **Primary Key:** `grant_id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- **Foreign Keys:**
  - `operator_org_id REFERENCES cae.operator_organization(operator_org_id)`
  - `workspace_id REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE`
- **Columns:**
  - `grant_id UUID NOT NULL`
  - `operator_org_id UUID NOT NULL`
  - `operator_actor_id VARCHAR(128) NOT NULL`
  - `workspace_id UUID NOT NULL`
  - `justification TEXT NOT NULL`
  - `expires_at TIMESTAMPTZ NOT NULL`
  - `revoked_at TIMESTAMPTZ`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
- **RLS Policy:** Active grant permits cross-workspace read with valid justification.
- **Evidence Source:** Desired: `TS-CAE-TEN-001` Sec 3.4; Local Source: `models/tenancy.py#OperatorAccessGrant`.

---

### 2.5 `cae.engagement` (Project Envelope)
- **Purpose:** Encapsulates marketing campaigns and creative activations within a workspace.
- **Data Classification:** `TENANT_DATA`
- **Primary Key:** `engagement_id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- **Foreign Keys:** `workspace_id REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE`
- **Unique Constraints:** `uq_workspace_engagement UNIQUE (workspace_id, engagement_id)` (Composite key for child referencing)
- **Columns:**
  - `engagement_id UUID NOT NULL`
  - `workspace_id UUID NOT NULL`
  - `title VARCHAR(255) NOT NULL`
  - `lifecycle_state VARCHAR(32) NOT NULL DEFAULT 'PLANNED'`
  - `version BIGINT NOT NULL DEFAULT 1`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
  - `updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
- **RLS Policy:** Enabled; strict workspace isolation.
- **Evidence Source:** Desired: `TS-CAE-TEN-001` Sec 3.5; Local Source: `models/tenancy.py#Engagement`.

---

### 2.6 `cae.guest` (Subject Entity)
- **Purpose:** Represents interview participants scoped to a workspace.
- **Data Classification:** `TENANT_DATA`
- **Primary Key:** `guest_id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- **Foreign Keys:** `workspace_id REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE`
- **Unique Constraints:** `uq_workspace_guest UNIQUE (workspace_id, guest_id)`
- **Columns:**
  - `guest_id UUID NOT NULL`
  - `workspace_id UUID NOT NULL`
  - `external_ref VARCHAR(128) NOT NULL`
  - `display_name VARCHAR(255) NOT NULL`
  - `status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE'`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
  - `updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
- **RLS Policy:** Enabled; strict workspace isolation.
- **Evidence Source:** Desired: `TS-CAE-TEN-001` Sec 3.6; Local Source: `models/tenancy.py#Guest`.

---

### 2.7 `cae.media_asset` (Cutover Media Entity)
- **Purpose:** Promoted aggregate entity (`MC-CAE-MED-001`) with fresh-read SHA-256 byte verification.
- **Data Classification:** `TENANT_DATA`
- **Primary Key:** `media_id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- **Foreign Keys:** `workspace_id REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE`
- **Unique Constraints:**
  - `uq_workspace_media UNIQUE (workspace_id, media_id)`
  - `uq_workspace_storage_path UNIQUE (workspace_id, storage_path)`
- **Columns:**
  - `media_id UUID NOT NULL`
  - `workspace_id UUID NOT NULL`
  - `engagement_id UUID`
  - `media_type VARCHAR(64) NOT NULL`
  - `storage_path VARCHAR(512) NOT NULL`
  - `byte_size BIGINT NOT NULL`
  - `sha256_checksum CHAR(64) NOT NULL`
  - `status VARCHAR(32) NOT NULL DEFAULT 'UNVERIFIED'`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
  - `updated_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
- **RLS Policy:** Enabled; strict workspace isolation.
- **Evidence Source:** Desired: `TS-CAE-TEN-001` Sec 3.7; Promotion Receipt: `rcpt_cae_receipt_commit_00c2b3f7341e59af1292fda7`.

---

### 2.8 `cae.harness_template` & `cae.harness_run` (Pipeline Execution)
- **Purpose:** Governs pipeline runs and deterministic execution parameters.
- **Data Classification:** `OPERATIONAL_METADATA`
- **Primary Keys:** `template_id UUID`, `run_id UUID`
- **Foreign Keys:**
  - `harness_template`: `workspace_id REFERENCES cae.workspace(workspace_id)`
  - `harness_run`: `(workspace_id, template_id) REFERENCES cae.harness_template(workspace_id, template_id)`
- **RLS Policy:** Enabled; strict workspace isolation.
- **Evidence Source:** Desired: `TS-CAE-TEN-001` Sec 3.8, 3.9; Local Source: `models/tenancy.py`.

---

### 2.9 `cae.receipt` (Immutable Execution Receipt)
- **Purpose:** Tamper-evident, append-only execution records.
- **Data Classification:** `IMMUTABLE_RECEIPT`
- **Primary Key:** `receipt_id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- **Foreign Keys:** `workspace_id REFERENCES cae.workspace(workspace_id) ON DELETE CASCADE`
- **Unique Constraints:** `uq_workspace_receipt UNIQUE (workspace_id, receipt_id)`
- **Triggers:** `trg_receipt_append_only` calling `cae.fn_prevent_receipt_mutation()` on UPDATE or DELETE (raises `EX_RECEIPT_IMMUTABLE`).
- **RLS Policy:** Enabled; append and select permitted; update and delete blocked at both RLS and trigger layers.
- **Evidence Source:** Desired: `TS-CAE-TEN-001` Sec 3.10; Local Source: `models/tenancy.py#Receipt`.

---

### 2.10 `cae.receipt_evidence_link` (Lineage Association)
- **Purpose:** Maps receipts to evidence objects (`media_asset`, `harness_run`).
- **Data Classification:** `IMMUTABLE_RECEIPT`
- **Primary Key:** `link_id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- **Foreign Keys (Current DDL):** `receipt_id REFERENCES cae.receipt(receipt_id) ON DELETE CASCADE` (Identified as `F-01`).
- **Target Composite FK (Future Repair):** `(workspace_id, receipt_id) REFERENCES cae.receipt(workspace_id, receipt_id)`.
- **Columns:**
  - `link_id UUID NOT NULL`
  - `workspace_id UUID NOT NULL`
  - `receipt_id UUID NOT NULL`
  - `evidence_type VARCHAR(64) NOT NULL`
  - `evidence_id UUID NOT NULL`
  - `created_at TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp()`
- **Evidence Source:** Desired: `TS-CAE-TEN-001` Sec 3.11; Finding: `F-01`.

---

## 3. Storage Bucket Inventory

- **Bucket Name:** `cae-media-private`
- **Public Access:** `FALSE` (Private only)
- **Allowed MIME Types:** `video/*`, `audio/*`, `image/*`, `application/json`
- **File Size Limit:** 500 MB per object
- **Storage Path Hierarchy:** `{workspace_id}/{engagement_id}/{media_id}.{ext}`
- **Security Policy:** Access token signing or service-role signed URL retrieval required.
