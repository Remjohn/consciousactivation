# CAE PostgreSQL/Supabase Migration Execution Plan

**Work package:** WP-02 — executable migration-plan design  
**Status:** `DRAFT_PENDING_OPERATOR_REVIEW`  
**Target authority:** PostgreSQL/Supabase for CAE durable operational state; Supabase Storage or S3-compatible object storage for raw media/artifact bytes.

## What “executable” means here

This is a runbook-shaped, evidence-bearing plan with concrete inputs, gates, rollback points, target tables, and reconciliation results. It is not permission to run a destructive bulk import. Execution begins only when the related bounded package is promoted.

No source table is copied wholesale. Each import is a deterministic transformation from an immutable source snapshot into an approved canonical target contract, recorded row-by-row in `cae.legacy_import_run` and `cae.legacy_import_record`.

## Packages and authorization boundaries

| Package | Purpose | May change | Must not change | Promotion proof |
|---|---|---|---|---|
| WP-02a | Provision a disposable foundation and apply reviewed DDL | disposable Supabase/Postgres, private storage buckets, migration ledger | legacy data and service write paths | structural + environment-fidelity proof packet |
| WP-02b | Import the interview-to-AIR first slice into disposable/shadow state | copied first-slice data and reconciliation ledger | production authority or local source data | count/hash/relationship reconciliation and real storage verification |
| WP-02c | Dual-read verification for the first slice | feature-flagged read adapter and comparison telemetry | destructive source changes or global write cutover | repeated zero-unexplained-difference runs |
| WP-02d | Controlled first-slice authority cutover | first-slice semantic-operation write path | remaining services and source archives | operator-approved cutover receipt and rollback drill |
| Subsequent slices | Pipeline, Campaign, VAE, registry, etc. | one named domain at a time | unrelated service authority | their own package-specific proof and operator gate |

## Phase 0 — source inventory and import contract

Before any provisioned environment receives data:

1. Identify the exact SQLite files, migration versions, table schemas, row counts, and source-record hashes.
2. Produce a read-only source manifest with a SHA-256 covering the inventory and per-table extraction manifests.
3. Map every source field to a target column, explicit derived value, or exclusion/quarantine reason. An unknown mapping is a failed migration-design item, not a nullable default.
4. Preserve legacy IDs, revisions, source timestamps, source hashes, source locations, and provenance as target identity or lineage attributes. Do not remint IDs merely for convenience.
5. Classify every record as importable, deferred, invalid, duplicate, or quarantined. Quarantine must retain diagnostics and source lineage.

**Exit evidence:** signed/hashed source manifest, field-mapping sheet, expected import counts by category, and a reviewed data-retention decision.

## Phase 1 — provision the disposable foundation (WP-02a)

1. Create a non-production Supabase/PostgreSQL environment with separate migration, application, read-only/auditor, and operations identities.
2. Create private media and artifact buckets. Disable public bucket access. Configure retention, encryption, backup, and lifecycle policy.
3. Apply `sql/0001_cae_foundation_draft.sql` only after converting it into the repository-selected migration mechanism and checksum convention.
4. Configure RLS policies from workspace/project membership. The first proof must show both an allowed and a denied read.
5. Create a short-lived service credential strategy; secrets never enter repository files, receipts, or public URLs.

**Exit evidence:** environment identifier, applied migration checksum, schema inspection, private-bucket policy verification, RLS allow/deny proof, backup/restore plan, and a foundation receipt.

**WP-02a staging result:** environment identity, applied migration checksums, private buckets, structural constraints, rollback-only RLS allow/deny proof, and temporary private-object upload/hash/denied-read/cleanup proof are recorded in [CAE_WP02A_FOUNDATION_PROOF.md](D:\Work\consciousactivation\docs\cae\implementation\CAE_WP02A_FOUNDATION_PROOF.md). Backup/restore and production operational proof remain future requirements.

## Phase 2 — first-slice extraction and transformation (WP-02b)

The source is Interview Expression plus only those AIR records needed to link authenticated evidence to a semantic eligibility assessment.

| Source fact | Target result | Reject/quarantine condition |
|---|---|---|
| source media / transcript reference | `media_asset`, then `source_package` after provider HEAD + SHA verification | object unavailable, size/type mismatch, missing hash, or ambiguous ownership |
| interview local objects/session events | `interview_session`, `interview_turn`, source lineage | non-deterministic order, unresolved source package, broken identity/revision |
| source spans / observed evidence pack | `evidence_item` and `evidence_span` | no anchored source, invalid offsets, nonexistent media/turn |
| authentication decision | `evidence_authentication` plus STC-EVID-001 transition | same action self-attests authentication, evaluator/provenance missing |
| AIR eligibility/candidate assessment | revisioned `semantic_assessment` plus `assessment_evidence_link` | unauthenticated evidence, unresolved validator/registry reference, invalid payload hash |
| existing events/receipts | canonical command/event/receipt only when their causal/evidence links can be preserved | event sequence or receipt linkage cannot be reconciled |

Extraction must be read-only. Import is idempotent through the source manifest and `legacy_import_record` key. It writes no source SQLite rows and never deletes source media.

**Exit evidence:** source count = classified target count + quarantine count; sampled source/target hash equality; zero orphan foreign keys; replayable import log; real object-store read after import; intentional failure case proving hash mismatch becomes `QUARANTINED`.

## Phase 3 — shadow reads and reconciliation (WP-02c)

1. Keep local SQLite authoritative while a feature-flagged adapter reads the Postgres projection for the first slice.
2. Compare normalized result shape, object IDs, revisions, lifecycle/epistemic state, evidence links, and content hashes for the same requests.
3. Record each comparison as match, expected-difference, unexplained-difference, or failure. Never silently normalize away a mismatch.
4. Exercise concurrent/stale-write attempts against Postgres only in the disposable environment; confirm no duplicate event, receipt, or state version is produced.

**Promotion threshold:** no unexplained differences in the agreed representative corpus; all failures have receipts; a rollback drill restores the SQLite read path without data loss.

## Phase 4 — controlled first-slice cutover (WP-02d)

1. Require an operator decision that identifies the exact semantic operations moving to Postgres authority.
2. Enable Postgres writes only through typed semantic operations. During the bounded transition, local stores are read-only mirrors or explicitly non-authoritative adapters—not competing writers.
3. Monitor transition conflicts, outbox delivery, storage verification failures, RLS denials, query latency, and reconciliation drift.
4. Retain legacy SQLite databases read-only, checksummed, and recoverable until the retention period and reconciliation acceptance are complete.

**Rollback:** disable the feature flag, restore the previous read path, retain the Postgres evidence/receipts for diagnosis, and record a cutover rollback receipt. Do not delete imported data as part of rollback.

## Non-negotiable migration checks

- Every row has an original source locator and source hash in the import ledger.
- No media is declared verified from filename, URL, or mock response alone; provider metadata and SHA-256 must match.
- No evidence becomes authenticated through a self-attested receipt.
- No transition succeeds on stale aggregate version or without its registered transition contract.
- No signed URL is persisted as canonical identity. Stable application URLs resolve authorization at request time.
- No SDA/SFL data is imported until WP-04 validates schema, hashes, IDs, lineage, crosswalks, and all references; unresolved SFL family references remain quarantined.
- No source database is deleted, overwritten, or made nonrecoverable during any migration phase.

## Required implementation artifacts for execution

WP-02a through WP-02d must add and test, in their own bounded packages:

1. A database migration runner and checksum verifier.
2. Supabase/Postgres adapters implementing transaction, command, event, receipt, projection, and object-storage ports.
3. A deterministic extractor/importer with a `--dry-run` mode, source manifest writer, mapping report, and ledger writer.
4. A reconciliation reporter with row counts, hashes, relationship checks, sampling, and discrepancy receipts.
5. Feature flags and dual-read comparison telemetry.
6. Structural, integration, environment-fidelity, reality-contact, and anti-reward-hack tests described in the WP-02 state-model record.

## Risks requiring future operator decisions

- Supabase Storage versus external S3-compatible production object store, including egress, retention, jurisdiction, and signing behavior.
- Authentication/SSO identity mapping into `cae.actor` and workspace/project RLS policy.
- RPO/RTO, backup cadence, restoration ownership, and event/asset retention periods.
- PII/sensitive interview media classification, deletion/legal-hold policy, and whether immutable receipts need redacted evidence representations.
- The exact data corpus and acceptance threshold for the first dual-read comparison.
