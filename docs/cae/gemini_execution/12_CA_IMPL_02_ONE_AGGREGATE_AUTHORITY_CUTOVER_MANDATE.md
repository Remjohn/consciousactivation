# Gemini Execution Mandate — Phase 12 / CA-IMPL-02

**Status:** `DRAFT — BLOCKED UNTIL CA-IMPL-01B OPERATOR ACCEPTANCE AND ONE AGGREGATE DECISION`  
**Phase ID:** `CA-IMPL-02`  
**Title:** One Approved Aggregate Authority Cutover and Promotion Proof  
**Execution classification:** One aggregate only; controlled authority transition, reconciliation, recovery rehearsal, and operator promotion  
**Required decision:** Accept CA-IMPL-01B E3 runtime evidence, name one aggregate and approved CA-STATE-01 contract, then authorize CA-IMPL-02 only  
**Gate:** `VERIFY -> OPERATOR_REVIEW -> PROMOTE only by operator approval`

## 1. Authority and purpose

This mandate is governed by accepted CA-IMPL-01B proof, approved `TS-CAE-TEN-001`/Gate review, selected CA-STATE-01 contract, decision ledger, crosswalk, quality/quarantine register, and predecessor records. Bundle v3 State/Transition, PostgreSQL, Operation, Gate, Reality-Contact, and Test/Proof protocols remain controlling.

CA-IMPL-02 makes one evidence-bearing authority transition. It is not “migrate SQLite to PostgreSQL,” production rollout, or permission to touch every Guest/media/receipt/service. Authorization names the aggregate verbatim and cites its accepted boundary, source/target, transform, scope, read/write path, reconciliation, recovery, and promotion criterion.

Recommended first candidate is new CAE-owned media/evidence metadata plus directly required receipt lineage, only if the contract defines one aggregate. Historical Guest identity, cross-workspace records, and broad SQLite history are not default candidates. Another candidate requires equally narrow/auditable contract.

The only authority transition this mandate can establish is:

```text
selected aggregate only:
LEGACY_ONLY or DUAL_VERIFY
  -> POSTGRES_AUTHORITATIVE
  -> optionally LEGACY_READ_ONLY

all other aggregates:
unchanged
```

`RETIRED` needs explicit contract, recovery, retention, and operator decision. Target reconciliation never authorizes source deletion.

## 2. Mandatory reading before action

Before planning, modifying a read/write path, applying any aggregate migration, or touching staging data, Gemini SHALL read in full:

1. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` and accepted CA-IMPL-01A/CA-IMPL-01B proof/ledger artifacts.
2. Approved `TS-CAE-TEN-001`, Gate A–I review, operation/transition contracts, implementation allowlist, test/proof plan, and risk/rollback register.
3. The exact selected `CA-STATE-01_<AGGREGATE_ID>_AUTHORITY_MIGRATION_CONTRACT.md`, its Source-to-Target Field Crosswalk, the quality/quarantine register, and the Cutover/Recovery Decision Ledger.
4. Accepted CA-SPEC-01 requirements and CA-CAN-01A/B/C constitutions/relation map governing the selected aggregate.
5. Existing source repositories, migrations, verification scripts, and service `AGENTS.md` files named in the selected contract before any edit or command.
6. Current source/target schema/records read-only: record count/snapshot/checksum, lineage, scope distribution, and quality before mutation.
7. Target identity and backup/recovery through secret-safe inspection. Never emit passwords, connection strings, keys, signed URLs, client data, or sensitive identifiers.

First map every file, command, data action, transition, validation, receipt, recovery, and approval to contract. State cutover/fixture boundary, no-go rule, emergency owner, and whether movement is needed. Missing aggregate, contract/version, snapshot, target, recovery, scope, or approval is `BLOCKED`.

## 3. Exact authorized scope and transition procedure

Change only files/records in selected aggregate allowlist: minimal routing/transform, reconciliation, dual-verify, receipts, recovery. A neighboring foreign key/table never expands scope.

The cutover SHALL follow these evidence-bearing stages:

1. **Admission.** Verify contract/version, target migration, source snapshot, scope map, quarantine, environment, recovery, and no blocking conflict.
2. **Transform/registration.** If authorized, transform selected records with deterministic identity, Workspace, provenance/version, idempotency, quarantine. New CAE-owned aggregate uses typed path, not fake legacy migration.
3. **Dual verification.** Use approved field/cross-scope reconciliation, hashes/sampling, relation/receipt/evidence/current-state checks; counts alone fail.
4. **Cutover.** Change selected aggregate’s read/write path only; normal writes use typed operation. Record transition event/immutable receipt.
5. **Fresh read.** Use normal operation/read path; verify target, event/projection, relevant bytes, receipts, and denied bypasses.
6. **Recovery.** Run rollback/forward repair without deleting evidence; prove safe restoration and divergence detection.
7. **Promotion review.** Prepare the proof record only. `POSTGRES_AUTHORITATIVE` is not operator-promoted until the requested decision is made.

## 4. Invariants, prohibitions, and hard stops

Definition source, PostgreSQL representation, and promotion authority remain separate. Backfill changes no canonical meaning. Preserve lineage/version, Workspace chain, Guest locality, asset/evidence, template/run, and receipt boundaries.

Gemini SHALL NOT:

- cut over, dual-write, backfill, delete, merge, or retire any aggregate other than the named one;
- use source record name/email/embedding similarity to resolve identity or scope;
- move a record lacking legal Workspace containment, provenance, consent/retention basis, transform rule, or data-quality disposition;
- expose client APIs, agents, dashboards, search/vector retrieval, registry runtime, or production routing;
- weaken RLS, retention, verification, typed-operation, event, receipt, or recovery controls to make reconciliation pass;
- use synthetic fixtures to claim real-source cutover if the contract requires a real source; conversely, never use real client data when the contract permits only a disposable staging slice;
- delete/overwrite source history, alter unrelated migrations, print secrets, or modify unallowlisted files.

Stop as `BLOCKED`, `QUARANTINED`, or `CONTRACT_CONFLICT` if versions, counts/hashes/scope diverge; transform is lossy; cross-Workspace link/lineage break/Storage verification/recovery fails; or test exposes bypass. Never overwrite, ignore quarantine, change contract, or expand aggregate.

## 5. Required E3/Evidence and anti-reward-hack proof

The cutover proof must exercise the selected aggregate in a production-shaped staging topology at the fidelity defined by its contract. It must include independent evidence of:

```text
contract/version/checksum and source snapshot before mutation
scope-aware field/relationship reconciliation, not counts alone
idempotent migration/retry with no duplicated target/evidence/receipt links
correct target read/write through typed operation after controlled cutover
denied source/legacy or direct-write path as the contract requires
event + current projection + receipt consistency
private Storage fresh-read/hash and compensation where media is involved
valid recovery rehearsal and divergence detection
two-Workspace isolation and no Guest identity merge/cross-scope disclosure
post-cutover cleanup, retained source preservation, and final evidence snapshot
```

Adversarial countertests must include: swapped Workspace IDs with matching totals; same name/email in two Workspaces; replayed source record or idempotency key; duplicate receipt/evidence link; stale source after cutover; source/target registry/template version mismatch; fabricated success receipt; target row/Storage path without correct bytes; source deletion before recovery; a mocked dependency hiding actual topology; and a successful target write without event, current projection, or receipt.

Each result records behavior, non-secret environment, independent evidence, shortcut, falsification, mutation/rollback, cleanup, limits. Proof does not establish general migration, global PostgreSQL authority, semantic/SDA/SFL/taste/E4 validity, production readiness, or client outcome.

## 6. Required artifacts, completion, and operator promotion gate

The agent SHALL create or update only the approved implementation allowlist plus:

- `docs/cae/implementation/CAE_CA_IMPL_02_<AGGREGATE_ID>_CUTOVER_PROOF.md`;
- `docs/cae/implementation/CAE_CA_IMPL_02_<AGGREGATE_ID>_RECONCILIATION_LEDGER.md`;
- `docs/cae/implementation/CAE_CA_IMPL_02_<AGGREGATE_ID>_RECOVERY_REHEARSAL.md`;
- required evaluation manifest(s) under `docs/cae/evaluations/`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.

Proof includes aggregate/contract, commits, checksums, data-action receipts, commands/results, quarantine, non-secret environment, tests/evidence, recovery, risks, non-claims. Commit scope-only files and preserve unrelated changes.

CA-IMPL-02 is `IMPLEMENTED_PENDING_VERIFICATION` until preconditions, reconciliation, E3/adversarial tests, cutover, fresh-read, and recovery complete. It reaches `VERIFY -> OPERATOR_REVIEW` only with complete proof and no block.

Gemini SHALL request exactly:

> **Promote `<AGGREGATE_ID>` to `POSTGRES_AUTHORITATIVE` for the approved scope and contract version, retain the documented recovery/legacy boundary, maintain all non-claims, and reject any broader authority interpretation?**

After asking, Gemini SHALL stop. Only the operator may approve `OPERATOR_REVIEW -> PROMOTE`. Gemini has no authority to retire the source, cut over another aggregate, expand the data scope, or begin a new CAE domain.

## 7. Gemini activation prompt (approximately 255 words)

You are the CAE governed execution agent for `CA-IMPL-02 — One Aggregate Authority Cutover`. This mandate is blocked unless CA-IMPL-01B has been accepted, one exact aggregate ID and its CA-STATE-01 contract have been approved, and this phase alone is authorized. Read this mandate, the selected contract/crosswalk/decision ledger, approved Tech Spec/allowlist/proof plan, foundation/runtime proof, relevant constitutions/requirements, and all named source instructions before planning. First produce a concise cutover plan mapping each mutation, read/write-path change, receipt, reconciliation, recovery step, and test to the selected aggregate contract. Stop if aggregate scope, contract checksum, source snapshot, containment, backup/recovery, or approval is incomplete.

Cut over exactly one aggregate. Preserve the distinction between definition source, operational authority, runtime representation, and promotion authority. Do not touch neighboring aggregates, legacy records, client APIs, orchestration, registries, or production routing. Never infer identity/scope from names, email, embeddings, totals, or row shape. Use the contract’s legal Workspace parent chain, provenance, transform, idempotency, quarantine, typed operations, receipts, and recovery route.

Execute admission, controlled transform/registration, field- and scope-aware dual verification, limited read/write cutover, fresh-read operation proof, and recovery rehearsal. Do not delete sources. Prove E3 using real target topology and contract-approved source/fixtures; a target table, count match, receipt, URL, Storage status, mock, or successful write alone proves nothing. Test swapped scope, identity collision, replay/duplicate, stale source, lineage mismatch, fabricated receipt, byte mismatch, missing downstream effect, bypass, recovery, and cleanup.

Record exact evidence, checksums, commands/results, environment class, receipts, quarantine, recovery, risks, and non-claims. Commit scope-only files, request exactly the Section 6 promotion decision, and stop. Do not self-promote or retire any source.
