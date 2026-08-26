# Gemini Execution Mandate — Phase 25 / CA-TWC-01

**Status:** `DRAFT — BLOCKED UNTIL OPERATOR AUTHORIZES THIS MANDATE`  
**Phase ID:** `CA-TWC-01`  
**Title:** Tenant & Workspace Core (Honest Staging Redeploy + Law-Complete Typed Tenancy)  
**Execution classification:** One guarded shared-staging schema deployment plus bounded implementation of typed workspace/membership/access-grant operations and their API surface; no production deployment, no client data (none exists), no campaign-router changes (F-03 stays open), no media/evidence ingestion (Phase 26 boundary), no authority promotion beyond what this mandate states  
**Required prior decision:** “Accept the CA-CAN-02 post-reading decision record (constitution set accepted; OP-Q1 relational registry tables; OP-Q2 deferred; OP-Q3 Tenant & Workspace Core first, Media & Evidence Ingestion follow-on) and authorize CA-TWC-01 as defined.”  
**Required completion gate:** `IMPLEMENT -> VERIFY -> OPERATOR_REVIEW`; Phase 26 (Media & Evidence Ingestion) begins only under a separately authorized mandate.

## 1. Authority, purpose, and boundary

CA-TWC-01 is governed by the CAE Governance & Specification Bridge Bundle v3 and inherits: accepted WP-00 through CA-UPTL-01 records; the operator’s CA-CAN-02 post-reading decision record; ratified constitutions `CA-CAN-01A/B/C` and the fifteen `CA-CAN-02_*` constitutions; `TS-CAE-TEN-001` operation and transition contracts; `CAE_STATE_01` authority matrices; and the typed-runtime precedents of CA-IMPL-01A/01B.

**Prior-chain qualification:** CA-STAGE-09 and CA-ACCEPT-10 remain `CLAIMS_UNVERIFIED_BY_OPERATOR`. This mandate executes the deployment they claimed but never performed. It inherits nothing from them except lessons, codified in Section 4.

**Purpose:** make the canonical UUID tenancy substrate REAL on shared staging, then bind law-complete typed workspace/membership/operator-grant operations to it. After this phase, `MC-CAE-WS-001` (Workspace tenancy context), `MC-CAE-MEM-001` (membership), and `MC-CAE-OPR-001` (operator organization/grants) are `POSTGRES_AUTHORITATIVE_STAGING_ONLY`. Every other aggregate keeps its current authority. No production claim may be recorded.

The permitted transition is:

```text
real staging (WP-era foundation, old topology, verified empty)
  -> admission + identity lock + emptiness proof
  -> PITR/backup checkpoint
  -> MIG-0000R foundation reset (drop enumerated EMPTY WP-era objects only)
  -> MIG-0001 .. MIG-0008 (existing approved drafts, exact bytes)
  -> MIG-0009 RLS completion (harness_template, operator_organization)
  -> structural proof suite (live countertests)
  -> typed workspace/membership/grant operations + API surface
  -> regression + adversarial proof
  -> OPERATOR_REVIEW

media/evidence ingestion, guest lifecycle implementation,
engagement/campaign wiring, F-03 repair, SQLite retirement: NOT_STARTED
```

## 2. Mandatory reading

Before planning or editing, the executing agent SHALL read in full:

1. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` — especially the `CLAIMS_UNVERIFIED_BY_OPERATOR` reclassification and retained-staging evidence block.
2. All eight draft files under `packages/ca_runtime/src/ca_runtime/migrations/drafts/` and `packages/ca_runtime/src/ca_runtime/migration_runner.py` (checksum semantics, guard headers, prohibited statements).
3. `TS-CAE-TEN-001_TENANT_GUEST_VERTICAL_SLICE.md` plus `TS-CAE-TEN-001_OPERATION_AND_TRANSITION_CONTRACTS.yaml` and `IMPLEMENTATION_FILE_ALLOWLIST.md`.
4. Constitutions governing this phase’s objects: `CA-CAN-01A_WORKSPACE.yaml`, `CA-CAN-01A_WORKSPACE_MEMBERSHIP.yaml`, `CA-CAN-01A_OPERATOR_ORGANIZATION.yaml`, `CA-CAN-01A_OPERATOR_ACCESS_GRANT.yaml`, `CA-CAN-01A_OPERATOR_ACCESS_POLICY.yaml`, `CA-CAN-01A_ENGAGEMENT.yaml`; and `CA-CAN-02_COMMAND.yaml`, `CA-CAN-02_EVENT.yaml`, `CA-CAN-02_STATE_TRANSITION.yaml`, `CA-CAN-02_STATE_TRANSITION_CONTRACT.yaml`, `CA-CAN-02_STATE_AGGREGATE.yaml`.
5. `FR-CAE-TEN-001` through `FR-CAE-TEN-005` and the corresponding sections of `PRD-CAE-TEN-001`.
6. Existing typed-runtime sources: `packages/ca_runtime/src/ca_runtime/database.py`, the tenant models/context from CA-IMPL-01A, `TenantScopedSemanticOperations` patterns from CA-IMPL-01B, and `api/main.py` router mounting.
7. Git history and working-tree state, identifying commits actually inspected.

If any input contradicts another, stop the affected item and route the contradiction to the operator — never self-resolve.

## 3. Exact scope: four sub-workstreams

### T0 — Admission, identity lock, emptiness proof

Record the staging target using its TRUE identity: host `aws-1-eu-west-1.pooler.supabase.com`, port `5432`, database `postgres`, project ref parsed from the connection username (`postgres.<ref>`), server version queried live. Secret-safe validation only — never print passwords or keys. Compare the live identity against the operator-approved identity block recorded in the admission record; any mismatch stops the mandate before mutation.

Then prove reset safety: for EVERY relation slated for replacement by MIG-0000R, commit raw row-count query output demonstrating zero rows (data classification `EMPTY_OR_SYNTHETIC_ONLY`). If ANY table contains unexpected rows, stop as `BLOCKED_ON_OPERATOR_INPUT` — do not drop non-empty tables under any circumstances.

### T1 — Honest staging redeploy (STAGE-09R)

Execute in order, each step evidenced per Section 4:

1. **Recovery checkpoint:** verify an executable backup/restore route exists for the target (Supabase PITR status or explicit snapshot procedure), record it, and confirm the restore path is runnable by the designated owner WITHOUT actually restoring.
2. **MIG-0000R foundation reset:** author one NEW forward-only draft `0000R_staging_foundation_reset.sql` that drops ONLY the enumerated, proven-empty WP-era relations (old text-keyed family and WP-03-era objects) inside a single transaction with post-condition checks. Prohibited: `DROP SCHEMA`, `DROP ... CASCADE` on unenumerated objects, TRUNCATE, DELETE FROM. The reset must be idempotent-safe (fail loudly if any enumerated object is non-empty).
3. **Apply MIG-0001 through MIG-0008** exactly as committed (byte-exact; checksums computed live per Section 4). Update the drafts’ status markers only AFTER successful application, per the established draft-lifecycle convention.
4. **MIG-0009 RLS completion:** author and apply a new draft enabling and enforcing RLS with appropriate policies on `cae.harness_template` and `cae.operator_organization` (closing the gap found by independent review), consistent with `0005_cae_row_level_security.sql` conventions.
5. **Structural proof suite — LIVE against the real database:** (a) composite FK `fk_workspace_receipt` present and rejecting a cross-workspace link with SQLSTATE `23503`; (b) `cae.guest_profile` exists with UUID PKs; (c) legacy WP-03 tables renamed/quarantined per MIG-0008 expectations; (d) unauthenticated/no-context session reads ZERO rows under RLS; (e) receipt UPDATE/DELETE rejected by trigger; (f) migration ledger rows read back verbatim matching applied versions and checksums.

### T2 — Typed tenancy core (law-complete)

Implement typed semantic operations for Workspace, WorkspaceMembership, and OperatorAccessGrant lifecycles strictly conforming to `TS-CAE-TEN-001` contracts and the constitutions: creation with legal parent enforcement, membership role binding/revocation, time-bounded grant lifecycle (active/expired/revoked), optimistic concurrency, immutable receipts on every transition with honest epistemic fields. Reuse and extend the CA-IMPL-01A/01B patterns (`tenancy context manager`, strongly-typed operations, error taxonomy per TS-CAE-TEN-001 Section 9). Unit/integration tests run locally (disposable SQLite/Postgres fixtures); staging is used read-write ONLY for the bounded synthetic proof in T4.

### T3 — API surface

Expose the T2 operations through a versioned FastAPI router (workspace-scoped request context, constitution-conformant error mapping, no tenant leakage in responses). Mount it in `api/main.py` alongside existing surfaces. Explicitly out of scope: the campaign router (F-03 remains open), interviews, media upload endpoints, Storage buckets, web UI changes beyond what mounting requires.

### T4 — Proof, regression, cleanup

Two-workspace isolation proof executed LIVE on staging with `syn_` prefixed synthetic tokens: cross-workspace denial matrix, grant-expiry denial, forged-scope denial, direct-insert bypass denial (as a DB-role limitation finding if the pooler role cannot be restricted — record honestly rather than claiming coverage), replay/idempotency check, one bounded failure/rollback rehearsal. Complete transient cleanup with count receipts. Full local regression green including all prior suites. Control state updated: findings F-01/F-02/F-04 dispositions become `SHARED_STAGING_REPAIRED_AND_VERIFIED` (F-01, F-02) and `RESOLVED_BY_MIG_0000R` (F-04) ONLY IF the corresponding live proofs pass; otherwise they keep their current status.

## 4. Evidence protocol (anti-fabrication — the STAGE-09 rules)

These rules exist because phases 21–22 recorded deployments that never happened:

1. **Checksums:** every migration checksum cited must be produced by running the hash command IN-SESSION against the committed file, with the command and raw output pasted. A checksum value written from memory or copied between documents is fabrication.
2. **Target identity:** record the true pooler host and username-derived project ref, obtained from a live `SELECT current_user, inet_server_addr(), version()` whose raw output is pasted. Never reconstruct a plausible-looking hostname from a ref.
3. **DDL effects:** every schema change followed immediately by an `information_schema`/`pg_catalog` read-back query with raw result rows pasted into the evidence record.
4. **Countertests:** executed against the REAL database with raw error messages/SQLSTATEs pasted — not against mocks. Mock-based probes may complement but never substitute.
5. **Validators:** `verify_ca_twc_01.py` must itself execute live probes (connect, assert constraint existence, attempt denials, hash files). Presence-only document checks are non-compliant.
6. **No invented ratification:** operator decisions are recorded only from operator text. The agent never writes “the operator has ratified” without a verbatim quoted decision to cite.
7. Reviewer reproducibility: an independent lane must be able to re-run every committed probe byte-for-byte. Anything less is `UNPROVEN` by default.

## 5. Authorized artifacts and prohibitions

Gemini MAY create or update only:

- `docs/cae/gemini_execution/25_CA_TWC_01_TENANT_WORKSPACE_CORE_MANDATE.md` (this document, if correction needed);
- `docs/cae/implementation/CAE_TWC_01_ADMISSION_RECORD.md`;
- `docs/cae/implementation/CAE_TWC_01_DEPLOYMENT_EVIDENCE.md` (T1 traces, read-backs, checksums);
- `docs/cae/implementation/CAE_TWC_01_TYPED_CORE_PROOF.md` (T2);
- `docs/cae/implementation/CAE_TWC_01_API_SURFACE_PROOF.md` (T3);
- `docs/cae/implementation/CAE_TWC_01_ISOLATION_AND_ADVERSARIAL_RESULTS.md` (T4);
- `docs/cae/implementation/CAE_TWC_01_COMPLETION_RECORD.md`;
- new drafts `0000R_staging_foundation_reset.sql` and `0009_cae_rls_completion.sql` under `packages/ca_runtime/src/ca_runtime/migrations/drafts/`;
- typed-core source within: `packages/ca_runtime/src/ca_runtime/**`, the tenancy models/operations modules established by CA-IMPL-01A/01B, one new router module under `api/routers/`, and minimal `api/main.py` mounting;
- tests under `tests/cae/` and `tests/api/` for these surfaces;
- `scripts/cae/audit/verify_ca_twc_01.py`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` (status, dispositions per T4, current-phase fields only).

Gemini SHALL NOT: touch production or any environment other than the admitted staging target; migrate client data (none exists — preserve that fact); modify the eight existing approved draft files’ SQL content (status markers excepted); alter the brownfield SQLite services or retire any source; touch the campaign router (F-03); begin media/evidence ingestion, Storage provisioning, guest lifecycle, or engagement implementation; change `.env`; promote authority beyond `MC-CAE-WS-001`/`MEM-001`/`OPR-001` to `POSTGRES_AUTHORITATIVE_STAGING_ONLY`; print or commit secrets; or cite any phase 20–22 artifact as proof.

## 6. Adversarial challenges (each must be answered in the Completion Record)

1. Deployment is claimed while the migration ledger shows no new entries. — Ledger read-back required, verbatim.
2. Checksums recorded differ from live-computed hashes of committed files. — Automatic fabrication verdict; mandate stops.
3. MIG-0000R drops more than the enumerated empty objects, or runs against a non-empty table. — Emptiness proofs must precede; post-drop relation inventory required.
4. RLS “verified” via policy catalog presence instead of a live no-context denial returning zero rows. — Behavioral proof only.
5. F-01 called repaired because the typed path refuses, while the raw SQL-level cross-workspace insert still succeeds. — Constraint-level rejection with SQLSTATE required.
6. Typed operations bypass receipts or set epistemic fields to anything other than `UNVERIFIED`. — Receipt payloads inspected.
7. Isolation proof uses two workspaces created by the same session context rather than genuinely distinct scopes. — Distinct-context proof required.
8. Cleanup asserted without count queries. — Count receipts mandatory.
9. Regression suites left red while completion is declared. — Full-suite output pasted.
10. Authority promoted beyond the three named aggregates, or staging facts upgraded to production claims. — Non-claims restated verbatim in the packet.

## 7. Completion, rollback, and operator gate

CA-TWC-01 completes only when: admission identity matches the approved block; emptiness proofs precede reset; the full chain MIG-0000R→MIG-0009 applies with live read-backs; the structural proof suite passes against the real database; typed operations and API surface pass their tests; the isolation matrix passes live; transient cleanup is receipted; the FULL local regression suite is green; and every dynamic claim carries Section 4-grade evidence.

The Completion Record provides Sections A–H in the established form, including reviewer-independence declaration and the falsification routes for every accepted claim.

**Rollback:** pre-deployment checkpoint (T1 step 1) defines the recovery route: forward compensating drafts are preferred; actual restore only on operator instruction. Implementation code lands in independently revertable commits.

Gemini SHALL request exactly:

> **Accept CA-TWC-01 as the completed Tenant & Workspace Core: staging redeploy verified live (F-01/F-02 repaired and F-04 resolved at shared-staging level, RLS complete), typed workspace/membership/grant operations bound under ratified law, MC-CAE-WS-001/MEM-001/OPR-001 now POSTGRES_AUTHORITATIVE_STAGING_ONLY, all other aggregates unchanged, no production or client-data claims — and authorize CA-NEXT (Media & Evidence Ingestion mandate drafting) only?**

It SHALL stop after this question.

## 8. Gemini activation prompt (approximately 270 words)

You are the CAE governed execution agent for `CA-TWC-01 — Tenant & Workspace Core`. Blocked until the operator authorizes it following the CA-CAN-02 post-reading decision record. Read the control state, both admission-critical records from the failed phases 20–22 (to know what fabrication looks like), all eight approved migration drafts plus the migration runner, TS-CAE-TEN-001 with its contracts and allowlist, the governing constitutions and FRs 001–005, the CA-IMPL-01A/01B typed-runtime sources, and the API bootstrap.

Sub-workstreams in order. T0: admit the true staging identity from a live probe — real pooler host, username-derived project ref, server version — and paste raw row-count outputs proving every object slated for reset is empty; any mismatch or non-empty table stops the mandate. T1: verify a recovery route, author MIG-0000R (enumerated empty-object reset only, no DROP SCHEMA/CASCADE), apply MIG-0001..0008 byte-exact with in-session checksums, add MIG-0009 completing RLS, then prove everything live: composite-FK 23503 rejection, UUID guest_profile, quarantine renames, zero-row no-context reads, immutable receipts, verbatim ledger. T2: implement law-complete typed workspace/membership/grant operations per contracts, receipts on every transition, epistemic fields UNVERIFIED. T3: expose them via one new versioned FastAPI router; campaign router untouched. T4: live two-workspace isolation matrix, rollback rehearsal, receipted cleanup, full regression green.

Evidence rules are absolute: commands and raw outputs pasted, checksums computed in-session, behavioral proofs not mock proofs, no invented ratifications. No production, no client data, no media ingestion, no F-03, no secrets printed. Commit only allowed artifacts, request the exact Section 7 decision, and stop.
