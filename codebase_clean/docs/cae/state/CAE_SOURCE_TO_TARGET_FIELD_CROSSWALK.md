# CAE Source-to-Target Field Crosswalk

**Document ID:** `CAE_SOURCE_TO_TARGET_FIELD_CROSSWALK`  
**Phase ID:** `CA-STATE-01`  
**Status:** `AUTHORED — PENDING OPERATOR REVIEW`  
**Date:** 2026-08-25  
**Governing Mandate:** `docs/cae/gemini_execution/08_CA_STATE_01_AGGREGATE_AUTHORITY_MIGRATION_MANDATE.md`  
**Authority References:** `14_CAE_STATE_AND_TRANSITION_CONTROL_PROTOCOL.md`, `15_CAE_POSTGRES_STATE_MODEL.md`, `PRD-CAE-TEN-001_TENANT_GUEST_OPERATIONAL_SLICE.md`  

---

## 1. Crosswalk Governance Principles

1. **Anti-"Same Name" Law:** Identical field naming across source and target schemas does NOT constitute a valid semantic mapping justification. Every mapping must declare its transformation rule, nullability contract, semantic owner, and data movement mode.
2. **Data Movement Modes:**
   - `COPIED` — Raw value transferred bit-for-bit with checksum verification.
   - `RECOMPUTED` — Target value calculated deterministically from source payload (e.g. SHA-256 hash or deterministic ID).
   - `REFERENCED` — Foreign key link established to an authoritative parent record.
   - `DISCARDED` — Ephemeral or non-authoritative source field intentionally abandoned with an explicit justification.
   - `QUARANTINED` — Defective, unverified, or unconsented source field blocked from runtime ingestion.
3. **Multi-Tenant Scope Derivation:** Every target record must explicitly inherit its `workspace_id` from a validated operational root. Global unpartitioned fields are strictly prohibited.

---

## 2. Detailed Field Crosswalk by Aggregate

### 2.1 Workspace & Actor (`MC-CAE-WS-001`)

| Source Store / Table / Field | Target Table / Field | Data Movement Mode | Transformation & Type Cast | Null / Invalid Handling | Scope Derivation | Lineage & Semantic Owner |
|---|---|---|---|---|---|---|
| Brownfield Config: `WORKSPACE_ID` | `cae.workspace.workspace_id` | `COPIED` | String validated against `^[a-z0-9_-]{3,64}$` | Rejects empty; fallback to `ws-default` with audit record | Universal Root | Platform Admin (`CA-ENT-001`) |
| Brownfield Config: `WORKSPACE_NAME` | `cae.workspace.name` | `COPIED` | UTF-8 String (max 255 chars) | Rejects empty; defaults to `workspace_id` | `workspace_id` | Platform Admin (`CA-ENT-001`) |
| System Timestamp: `now()` | `cae.workspace.created_at_utc` | `RECOMPUTED` | RFC3339 UTC ISO-8601 Timestamp | Rejects non-UTC; defaults to current system UTC | `workspace_id` | Platform Admin (`CA-ENT-001`) |
| Brownfield Auth: `USER_ID` | `cae.actor.actor_id` | `RECOMPUTED` | Deterministic ID `deterministic_id("act", {workspace_id, external_subject})` | Rejects null; raises `AuthenticationError` | `workspace_id` | Identity Provider Sync (`CA-ENT-005`) |
| Brownfield Auth: `USER_ROLE` | `cae.actor.role` | `COPIED` | Enum cast: `OPERATOR`, `WORKSPACE_ADMIN`, `ENGAGEMENT_LEAD`, `GUEST`, `SERVICE_RUNNER` | Unmapped roles quarantined as `SUSPENDED` | `workspace_id` | Workspace Admin (`CA-ENT-005`) |

---

### 2.2 Operator Access Governance (`MC-CAE-OPR-001`)

| Source Store / Table / Field | Target Table / Field | Data Movement Mode | Transformation & Type Cast | Null / Invalid Handling | Scope Derivation | Lineage & Semantic Owner |
|---|---|---|---|---|---|---|
| Platform Design: `ORG_ID` | `cae.operator_organization.operator_org_id` | `COPIED` | String validated against `^org-[a-z0-9_-]+$` | Rejects invalid; requires formal charter | Governance Root | Platform Security Officer (`CA-ENT-000`) |
| Policy Design: `POLICY_ID` | `cae.operator_access_policy.policy_id` | `COPIED` | String validated against `^pol-[a-z0-9_-]+$` | Rejects empty | `operator_org_id` | Compliance Committee (`CA-POL-001`) |
| Grant Request: `TICKET_ID` | `cae.operator_access_grant.ticket_id` | `COPIED` | External ITSM ticket reference (e.g. `SEC-10492`) | Rejects empty; mandatory for grant issuance | `operator_org_id` | Requesting Operator (`CA-REL-002`) |
| Grant Request: `DURATION` | `cae.operator_access_grant.expires_at_utc` | `RECOMPUTED` | `granted_at_utc + INTERVAL (duration_minutes)` (max 240m) | Rejects durations > 240 min | `operator_org_id` | Authorizing Security Lead (`CA-REL-002`) |
| Ephemeral Session: `TOKEN` | *(None / Ephemeral)* | `DISCARDED` | Ephemeral session token discarded after cryptographic signature verification | N/A | N/A | Auth Gateway (Discarded) |

---

### 2.3 Engagement (`MC-CAE-ENG-001`)

| Source Store / Table / Field | Target Table / Field | Data Movement Mode | Transformation & Type Cast | Null / Invalid Handling | Scope Derivation | Lineage & Semantic Owner |
|---|---|---|---|---|---|---|
| SQLite `campaign_orders.workspace_id` | `cae.project.workspace_id` | `COPIED` | String trim & validation | Rejects null or mismatch with context | Root Partition | Workspace Admin (`CA-ENT-004`) |
| SQLite `campaign_orders.project_id` | `cae.project.project_id` | `COPIED` | String trim & validation | Rejects empty; preserves deterministic ID | `workspace_id` | Engagement Lead (`CA-ENT-004`) |
| SQLite `campaign_orders.payload_json` | `cae.project.configuration_payload` | `COPIED` | Canonical JSON text parsed to PostgreSQL JSONB | Rejects invalid JSON; validates schema | `workspace_id` | Engagement Lead (`CA-ENT-004`) |
| SQLite `campaign_orders.canonical_sha256` | `cae.project.configuration_sha256` | `COPIED` | 64-char lowercase hexadecimal SHA-256 | Recomputed and verified on import | `workspace_id` | Engagement Lead (`CA-ENT-004`) |
| SQLite `campaign_states.lifecycle_state` | `cae.project.lifecycle_state` | `COPIED` | Enum cast: `DRAFT`, `LAUNCHED`, `RUNNING`, `AWAITING_REVIEW`, `BLOCKED_EXCEPTION`, `READY_TO_SHIP`, `SHIPPED`, `CANCELLED` | Unmapped states quarantined | `workspace_id` | Engagement State Machine (`CA-ENT-004`) |
| SQLite `campaign_states.version` | `cae.project.version` | `COPIED` | Integer monotonically increasing version | Rejects values < 1 | `workspace_id` | Optimistic Concurrency Engine (`CA-ENT-004`) |

---

### 2.4 Guest & Identity Link (`MC-CAE-GST-001`)

| Source Store / Table / Field | Target Table / Field | Data Movement Mode | Transformation & Type Cast | Null / Invalid Handling | Scope Derivation | Lineage & Semantic Owner |
|---|---|---|---|---|---|---|
| SQLite `interview_sessions.participant_id` | `cae.guest.guest_id` | `RECOMPUTED` | `deterministic_id("gst", {workspace_id, participant_id})` | Rejects null | `workspace_id` | Engagement Lead (`CA-ENT-003`) |
| SQLite `interview_sessions.workspace_id` | `cae.guest.workspace_id` | `COPIED` | String validation | Rejects null | Root Partition | Workspace Admin (`CA-ENT-003`) |
| SQLite `interview_sessions.participant_name` | `cae.guest.display_name` | `COPIED` | UTF-8 String (max 255 chars) | Defaults to "Anonymous Participant" | `workspace_id` | Interview Lead (`CA-ENT-003`) |
| Brownfield Global Identity Match | `cae.guest_identity_link` | `QUARANTINED` | Cross-workspace link resolution is deferred | Automatic linking prohibited; quarantined | Dual Workspaces | Privacy Officer (`CA-MAP-001`) |

---

### 2.5 Media Asset & Evidence Lineage (`MC-CAE-MED-001`) — *First Cutover Candidate*

| Source Store / Table / Field | Target Table / Field | Data Movement Mode | Transformation & Type Cast | Null / Invalid Handling | Scope Derivation | Lineage & Semantic Owner |
|---|---|---|---|---|---|---|
| Legacy Disk Path: `interviews/{ws}/{proj}/{file}` | `Supabase Storage Object Key` | `RECOMPUTED` | `cae/interview-expression/{bridge_id}/{sha256}.bin` | Rejects non-workspace paths | `workspace_id` | Source Bridge (`CA-EVI-001`) |
| Legacy Media File Bytes | `Supabase Storage Object Bytes` | `COPIED` | Raw binary upload with `x-upsert: false` | Byte hash mismatch aborts bridge | `workspace_id` | Storage Ingestion Gateway (`CA-EVI-001`) |
| Legacy Source Manifest: `sha256` | `cae.media_asset.content_sha256` | `COPIED` | 64-char hex string re-verified from raw disk bytes | Rejects if recomputed hash differs | `workspace_id` | Source Bridge (`CA-ENT-002`) |
| Legacy Source Manifest: `bytes` | `cae.media_asset.byte_size` | `COPIED` | Integer byte count re-verified from disk | Rejects if byte count differs | `workspace_id` | Source Bridge (`CA-ENT-002`) |
| Legacy Source Manifest: `media_type` | `cae.media_asset.media_type` | `COPIED` | Standard MIME type (e.g. `audio/wav`) | Rejects unapproved MIME types | `workspace_id` | Media Ingestion Service (`CA-ENT-002`) |
| SQLite `ie_objects.payload_json` | `cae.source_package.payload` | `COPIED` | JSONB parse with canonical SHA-256 verification | Rejects schema invalidity | `workspace_id` | Source Bridge (`CA-REL-004`) |
| SQLite `ie_edges.child_id` (Audio Segments) | `cae.evidence_item.evidence_id` | `RECOMPUTED` | `deterministic_id("evi", {workspace_id, source_pkg_id, segment})` | Rejects orphans | `workspace_id` | Evidence Capture Engine (`CA-EVI-002`) |
| SQLite `ie_edges.relation` | `cae.evidence_span.span_type` | `COPIED` | Textual relation (e.g. `TRANSCRIPT_SEGMENT`, `AUDIO_CLIP`) | Unmapped relations quarantined | `workspace_id` | Semantic Span Analyzer (`CA-REL-003`) |
| Ephemeral Media Temp Files | *(None / Ephemeral)* | `DISCARDED` | Temporary audio resample buffers discarded with audit record | N/A | N/A | Ingestion Audio Transcoder (Discarded) |

---

### 2.6 Harness Run & Execution State (`MC-CAE-RUN-001`)

| Source Store / Table / Field | Target Table / Field | Data Movement Mode | Transformation & Type Cast | Null / Invalid Handling | Scope Derivation | Lineage & Semantic Owner |
|---|---|---|---|---|---|---|
| Git Runbook YAMLs | `cae.harness_template.definition_payload` | `REFERENCED` | Pinned git commit snapshot to PostgreSQL JSONB | Rejects uncommitted runbooks | Global Canonical | Architecture Governance (`CA-STR-001`) |
| SQLite `pipeline_runs.run_id` | `cae.harness_run.run_id` | `COPIED` | String validation (New CAE runs only; legacy retained) | Rejects null | `workspace_id` | Pipeline Scheduler (`CA-EXE-001`) |
| SQLite `pipeline_runs.state` | `cae.harness_run.state` | `COPIED` | Enum: `PENDING`, `RUNNING`, `PAUSED`, `COMPLETED`, `FAILED`, `CANCELLED` | Unmapped states raise error | `workspace_id` | Pipeline Runner (`CA-EXE-001`) |
| SQLite `pipeline_node_states.node_id` | `cae.harness_run_step.node_id` | `COPIED` | String matching DAG node identity | Rejects unmapped nodes | `workspace_id` | DAG Dispatcher (`CA-EXE-001`) |
| SQLite `pipeline_checkpoints.snapshot_json` | `cae.harness_run.checkpoint_payload` | `COPIED` | JSONB snapshot with SHA-256 verification | Corrupt JSON quarantined | `workspace_id` | State Machine Checkpointer (`CA-EXE-001`) |

---

### 2.7 Receipts & State Transitions (`MC-CAE-REC-001`) — *First Cutover Candidate*

| Source Store / Table / Field | Target Table / Field | Data Movement Mode | Transformation & Type Cast | Null / Invalid Handling | Scope Derivation | Lineage & Semantic Owner |
|---|---|---|---|---|---|---|
| SQLite `commands.command_id` | `cae.command.command_id` | `COPIED` | String trim & validation | Rejects empty | `workspace_id` | Transaction Adapter (`CA-CMD-001`) |
| SQLite `commands.idempotency_key` | `cae.command.idempotency_key` | `COPIED` | String trim & uniqueness enforcement | Rejects empty | `workspace_id` | Transaction Adapter (`CA-CMD-001`) |
| SQLite `events.event_id` | `cae.event.event_id` | `COPIED` | Deterministic event ID | Rejects null | `workspace_id` | Transition Engine (`CA-EVT-001`) |
| SQLite `receipts.receipt_id` | `cae.receipt.receipt_id` | `COPIED` | Cryptographic receipt identifier `rec-[a-z0-9_-]+` | Rejects null | `workspace_id` | Receipt Seal Engine (`CA-REC-001`) |
| SQLite `receipts.previous_receipt_sha256`| `cae.receipt.previous_receipt_sha256`| `COPIED` | 64-char lowercase hex SHA-256 | Hash break raises integrity alarm | `workspace_id` | Receipt Seal Engine (`CA-REC-001`) |
| Evaluator Assertion Payload | `cae.execution_receipt.evaluator_actor_id`| `REFERENCED` | Foreign key referencing distinct evaluator in `cae.actor` | Rejects if evaluator == command actor | `workspace_id` | Independent Evaluator (`CA-REC-002`) |
| Evaluator Evidence References | `cae.receipt_evidence_link` | `REFERENCED` | Composite foreign key `(receipt_id, evidence_id)` | Rejects unverified evidence items | `workspace_id` | Causal Lineage Anchor (`CA-REL-005`) |
| SQLite `product_metadata.version` | `cae.state_aggregate.version` | `COPIED` | Monotonically increasing state version integer | Version conflict aborts transaction | `workspace_id` | Concurrency Controller (`CA-STA-001`) |

---

## 3. Crosswalk Quality and Governance Guarantees

1. **Deterministic Verification:** Every field transform in Section 2 is deterministically reversible or cryptographically verifiable by automated static and staging test suites.
2. **Zero Inferred Authority:** No source field is mapped to a target column based on field name similarity alone.
3. **Data Loss Record:** Ephemeral intermediate audio buffers and temporary session tokens are the only fields discarded, and both are formally recorded in Section 2.
