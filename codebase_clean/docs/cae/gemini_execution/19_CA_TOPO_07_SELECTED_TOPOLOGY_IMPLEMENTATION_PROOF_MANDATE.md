# Gemini Execution Mandate — Phase 19 / CA-TOPO-07

**Status:** `DRAFT — BLOCKED UNTIL CA-TOPO-06 OPERATOR SELECTION OF ONE OPTION AND DISPOSABLE-TARGET ADMISSION`  
**Phase ID:** `CA-TOPO-07`  
**Title:** Selected F-02 Canonical Topology Implementation and Disposable Proof  
**Execution classification:** One operator-selected topology/route implementation and E3 proof in one new isolated disposable PostgreSQL environment; no shared staging, client data, broad source migration, or authority change  
**Required prior decision:** “Select CA-TOPO-06 option `<OPTION_ID>`, its named canonical route/identity boundary, and authorize CA-TOPO-07 only for that selection in a named disposable target.”  
**Required completion gate:** `IMPLEMENT -> VERIFY -> OPERATOR_REVIEW`; no route/topology is admitted to shared staging without another mandate.

## 1. Authority, selected input, and non-negotiable boundary

CA-TOPO-07 is governed by the CAE Governance & Specification Bridge Bundle v3; accepted CA-AUDIT-01 through CA-TOPO-06 records; current control state; `TS-CAE-TEN-001`; CA-STATE-01 contracts; and the affected constitutions/requirements. It is legal only when the CA-TOPO-06 Operator Decision Packet identifies one exact option ID, one canonical relation family/namespace, one identity/key boundary, one route/contract outcome, one owner, and one decision record. If any of these inputs is absent or internally inconsistent, this phase is `BLOCKED`.

F-02 is not fixed by creating a new alias, adapter, table, or test that makes one fixture pass. It is resolved only if the selected topology makes the named canonical route and its dependent key, tenancy, receipt/evidence, state, and recovery semantics unambiguous—and proves the formerly conflicting/shadowed route cannot be silently selected in the disposable target.

The selected option must be copied verbatim into the CA-TOPO-07 admission record. Gemini may not refine a decision by changing its family, adding a different coexistence strategy, treating an unselected option as fallback, or replacing its canonical route with `verify_media_asset` merely because that route previously passed. If the decision specifies a temporary compatibility adapter, that adapter is a first-class runtime/contract boundary with a version, owner, expiry, and test burden; it is not “no change.”

The permitted transition is:

```text
F-02: TOPOLOGY_EVIDENCED_DECISION_REQUIRED
  -> SELECTED_TOPOLOGY_IMPLEMENTED_AND_E3_PROVEN_DISPOSABLE_ONLY

shared staging / production / aggregate authority:
unchanged
```

This phase does not apply the F-01 repair to shared staging, migrate legacy/client records, retire a table family in a shared environment, change SDA/SFL or Primitive Registry authority, enable production routing, or alter the scope of `MC-CAE-MED-001`.

## 2. Mandatory reading, disposable admission, and scope lock

Before planning, editing, connecting, or applying a migration, Gemini SHALL read in full:

1. The selected CA-TOPO-06 option, its decision record, topology inventory, contract-route matrix, collision analysis, optional staging metadata inspection, completion record, and current control state.
2. CA-MIG-03 forward migration package, CA-APPLY-04 proof, CA-INT-05 F-01 proof, all F-02 evidence, and the exact current schema/operation/bridge/test source affected by the chosen option.
3. `TS-CAE-TEN-001`, CA-STATE-01 contracts, affected CA-CAN constitutions/CA-SPEC requirements, the original WP-03 bridge semantics, CA-IMPL-01B typed operation semantics, and relevant Bundle v3 protocols.
4. Migration/runner/service conventions and all relevant `AGENTS.md` instructions.

A new `DISPOSABLE_POSTGRESQL_ONLY` admission is required. It must identify the database/project/container, prove it is not current CAE staging or production, attest to empty/synthetic-only data, identify its recreate/teardown route, validate the approved baseline migration IDs/checksums plus F-01 repair baseline where required by the selected option, and name a single execution owner. The target must use endpoint and checksum guards; it must reject a staging/production-like identity, an unapproved database, a missing disposable declaration, or a changed option/migration checksum before mutation.

All edited files, SQL drafts, adapters, route code, migration IDs, tests, and fixture prefixes must be enumerated in a Scope Lock before the first change. A new consumer, attribute, table family, data transformation, or contract not enumerated by the chosen option is `SCOPE_VIOLATION`, not an invitation to broaden the phase.

## 3. Exact authorized implementation and execution sequence

Gemini may implement only the selected option’s minimum schema/namespace/compatibility route and the necessary guarded runner, tests, and evidence artifacts. Any migration must be forward-only, checksum-locked, preflighted, dependency-ordered, and reversible only through a declared forward compensating migration or disposable target recreation. It must never drop/rebuild existing `cae.*` tables or use destructive bootstrap DDL.

The required sequence is:

1. **Admission and baseline.** Verify target/scope/checksums; inspect baseline topology, F-01 constraint, RLS, receipt trigger, and current route bindings. Capture non-secret metadata and prove synthetic-only state.
2. **Selected implementation.** Apply only the topology/route delta authorized by `<OPTION_ID>`. If it includes a namespace, adapter, compatibility view, key translation, or route binding, make that boundary explicit and versioned. Do not write a hidden dual-write or fallback path.
3. **Structural topology proof.** Independently inspect relation family names/namespaces, keys/types, constraints, RLS, triggers, migration history, and route registration. Prove there is one declared canonical route for the selected operation and that unselected/shadowed family selection is detectable/denied as defined by the option.
4. **Canonical operation proof.** Exercise the selected route against synthetic data through its normal approved contract/typed boundary. Verify input key shape, correct target relation, Workspace parent chain, state transition, and the required receipt/evidence result. If the selected decision declares `register_verified_interview_source` as canonical, this exact operation must run; a substituted media route fails the phase.
5. **Cross-family and scope countertests.** Attempt wrong family/key-shape calls, a shadowed/legacy route call, swapped Workspace IDs, duplicate/replay inputs, and a valid route call. Record which must fail, which may be accepted through a named adapter, and why. No ambiguity or silent fallback is allowed.
6. **Containment and integrity regression.** Re-prove RLS/no-context denial, F-01 structural cross-workspace link rejection when in baseline, receipt immutability, contract/version mismatch rejection, and no unapproved data/table mutation.
7. **Replay, failure, recovery, and teardown.** Re-run the selected migration/route according to its idempotency law; induce one bounded failure; verify no false history/receipt/state; use only the declared forward-repair/recreation route; then remove run-prefixed synthetic fixtures or destroy the disposable target.

## 4. Required proof and adversarial countertests

The proof must state the environment class, engine/version, selected option/decision/checksums, exact operation/contract, independent schema inspection, synthetic fixture class, command results, rollback/cleanup result, and all non-claims. A successful database connection, route registration, table count, migration-history record, mocked consumer, or self-authored receipt does not establish topology correctness.

At minimum, prove or reject these cases:

1. selected option/draft checksum differs from operator-approved input;
2. target identity is current staging/production-like or not disposable;
3. selected route resolves to the wrong/shadowed relation family;
4. a deprecated/unselected bridge route silently falls through to a different route;
5. an adapter accepts a wrong text/UUID key without explicit identity mapping/version/provenance;
6. the selected route writes a target row without required state/receipt/evidence effect;
7. a swapped Workspace chain or F-01 cross-workspace receipt link succeeds;
8. RLS/no-context access or receipt mutation becomes possible after topology change;
9. duplicate/replay creates two relations, two records, or two receipts when the contract requires one;
10. a failed migration/route leaves a false applied history, partially active adapter, or ambiguous canonical route;
11. repeat execution changes schema/data despite a claimed no-op/idempotency path;
12. teardown can target data outside the run prefix/approved disposable environment.

Stop as `BLOCKED`, `CONTRACT_CONFLICT`, `REPAIR_REQUIRED`, or `SCOPE_VIOLATION` if the selected option requires unapproved client/legacy transformation; identity mapping is undefined; more than one route remains canonical; a consumer cannot be brought into the selected boundary; the F-01 baseline is missing where needed; a required receipt/state effect is absent; RLS/immutability weakens; recovery/cleanup is uncertain; or shared staging/prod is reached. Do not use a compatibility shortcut to call the result “resolved.”

## 5. Files, data, authority, and hard prohibitions

Gemini MAY create/update only the selected, scope-locked migration/adapter/route/test files plus:

- `docs/cae/implementation/CAE_TOPO_07_ADMISSION_RECORD.md`;
- `docs/cae/implementation/CAE_TOPO_07_SELECTED_OPTION_IMPLEMENTATION.md`;
- `docs/cae/implementation/CAE_TOPO_07_CANONICAL_ROUTE_PROOF.md`;
- `docs/cae/implementation/CAE_TOPO_07_ADVERSARIAL_AND_RECOVERY_RESULTS.md`;
- `docs/cae/implementation/CAE_TOPO_07_TEARDOWN_RECEIPT.md`;
- `docs/cae/implementation/CAE_TOPO_07_COMPLETION_RECORD.md`;
- scoped runner/tests under the established migration/implementation and `tests/cae/` locations;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md`.

Gemini SHALL NOT access/update shared staging, production, SQLite, Supabase Storage, client/Guest/media/registry data, object constitutions, PRD/FR/contract doctrine, unrelated services/APIs, `.env`, existing authority records, or F-02-unrelated operations. It shall not retire/drop/rename a shared family, run an unscoped cleanup, add background orchestration, turn a staging proof into production authority, or begin an E3 replay of shared staging.

## 6. Completion, rollback, and operator gate

CA-TOPO-07 completes only when the selected option is fully scope-locked, all migration/route changes apply in the named disposable target, independent topology/route inspection and canonical operation proof pass, all countertests/replay/failure/recovery/teardown evidence pass, and the final record distinguishes disposable proof from any shared-staging/production claim. Control state may record `F02_SELECTED_TOPOLOGY_E3_PROVEN_DISPOSABLE_ONLY`; it must retain F-01/shared-staging/production limitations.

**Rollback/recovery:** The target is disposable. Use its documented recreation/destruction route or a checksum-controlled forward compensating migration. Never invoke destructive bootstrap DDL against shared state. If failure leaves topology uncertainty, preserve the target for inspection, mark it contaminated, and deny reuse; do not retry against another target without a new admission record.

Gemini SHALL request exactly:

> **Accept CA-TOPO-07 as disposable proof of the operator-selected F-02 canonical topology and route only, preserve all shared-staging/production and data-migration limitations, and authorize CA-E3-08 only to independently replay the bounded foundation, F-01, and selected F-02 proof chain in a network-permitted staging-equivalent environment—without promoting any new authority?**

It SHALL stop after this question.

## 7. Gemini activation prompt (approximately 270 words)

You are the CAE governed execution agent for `CA-TOPO-07 — Selected F-02 Canonical Topology Implementation and Disposable Proof`. This mandate is blocked until the operator selects one exact CA-TOPO-06 option, canonical relation family/namespace, identity boundary, and canonical route. Read this mandate, selected decision, all topology/audit/migration/F-01 evidence, current source, contracts, conventions, and instructions before planning or connecting.

Implement only the chosen topology and its minimum explicit route/adapter/migration surface in one newly admitted disposable PostgreSQL target. First create a scope lock and admission record proving checksums, target identity, synthetic-only data, recovery, baseline migrations, and F-01 baseline when required. If the option, route, identity mapping, consumer list, target, or preconditions are unclear, stop—never pick a fallback family or silently substitute `verify_media_asset`.

Make one canonical route unambiguous. Independently inspect relation families, key shapes, constraints, RLS, triggers, migration history, and registration after applying the change. Exercise the exact selected normal operation with synthetic data; if the decision names `register_verified_interview_source`, prove that operation, not a different route. Test wrong/shadowed family selection, wrong key shape, unversioned adapter mapping, scope swap, replay, missing receipt/state effects, RLS/no-context access, F-01 link integrity, receipt immutability, failure/recovery, repeat safety, and scoped teardown.

Do not touch shared staging, production, Storage, SQLite, client or registry data, authority records, unrelated runtime/API surfaces, or doctrine. Never call disposable proof a production/staging cutover. Commit only scope-locked artifacts, update control state only after proof, ask the exact Section 6 decision, and stop.
