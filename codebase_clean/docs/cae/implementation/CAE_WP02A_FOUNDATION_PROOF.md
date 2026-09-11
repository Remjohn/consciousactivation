# CAE WP-02a Foundation Proof

**Work package:** WP-02a — Disposable Staging Foundation
**Status:** `COMPLETE_PENDING_OPERATOR_REVIEW`
**Environment:** Supabase staging project `evnxdssbxxrsesftdvgx`; PostgreSQL 17.6; session pooler
**Applied:** 2026-08-24

## Authorized scope executed

1. Applied the guarded CAE relational foundation migration to the previously empty staging project.
2. Created private Supabase Storage buckets `cae-media` and `cae-artifacts`.
3. Ran ledger, structural, bucket-privacy, and adversarial referential-integrity proof.
4. Applied workspace-scoped RLS scaffolding and ran rollback-only allowed/denied identity proof.

## Evidence and results

| Evidence | Result |
|---|---|
| Read-only staging identity probe | `postgres` database, PostgreSQL 17.6, and no pre-existing `cae` schema verified before application. |
| Migration result | `0001_cae_foundation` applied once with SHA-256 `b9ac25e8bd81abab2f01af828d3ab209b4d2e7308a2f698272f720e944430b91`. |
| Migration-ledger recheck | `migration_status=APPLIED`. |
| Bucket check | `cae-media=PRIVATE`; `cae-artifacts=PRIVATE`. |
| Required-table structural check | Passed for all 22 required CAE foundation tables. |
| Anti-reward-hack referential check | An intentionally orphaned `evidence_span` was rejected by a foreign-key constraint inside a forced-rollback transaction. No test row persisted. |
| RLS migration result | `0002_cae_workspace_rls` applied once with SHA-256 `6067550621e78a3aa4f645e84e9be34b907df4441cd0d1851a1b8c8bc28d095d`. |
| Authorized RLS check | A temporary authenticated identity mapped to the workspace read exactly its own workspace. Fixture transaction was forced to roll back. |
| Denied RLS check | A distinct authenticated identity read zero rows from that workspace. Fixture transaction was forced to roll back. |
| Real private Storage proof | Temporary object upload to `cae-media` passed; authorized download SHA-256 matched the uploaded bytes; unauthenticated retrieval was denied; the temporary proof object was deleted. |

## What is now true

- PostgreSQL/Supabase hosts the first CAE relational foundation in staging.
- Raw-media and artifact buckets exist and are private by default.
- The migration runner is checksum guarded and refuses a conflicting foundation state.
- First-slice typed entities, relational links, import ledger, transition records, commands/events/receipts, and storage metadata tables exist.
- RLS is enabled on every CAE foundation table. Authenticated direct reads are workspace-scoped; normal direct writes remain default-deny/server-only.
- A real server-only Storage credential successfully exercised private-object upload, byte-level hash verification, access denial, and cleanup.

## What is not yet proven

- Stable application URL resolution and its integration with a future CAE `media_asset` semantic operation.
- Typed semantic-operation service adapters; database tables do not by themselves establish authorized normal writes.
- Legacy-source inventory, extraction, import, reconciliation, dual-read behavior, or any authority cutover.
- Production readiness, backup/restore, retention, PII policy, performance, or disaster recovery.

## Risks and next decision

The staging foundation is intentionally not yet opened to application traffic. The RLS scaffold relies on the Supabase Auth JWT `sub` matching `cae.actor.external_subject`; production identity provisioning and policy ownership remain to be implemented through typed semantic operations.

**Exact decision required:** **Promote WP-02a and authorize WP-03 to define the typed semantic-operation layer for the first evidence-to-AIR transition, without importing legacy data or redirecting existing service writes?**
