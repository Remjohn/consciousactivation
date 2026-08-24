# TS-CAE-EVID-001 — Evidence to AIR Assessment Lifecycle

**Status:** `BROWNFIELD_RECONCILED`; staging implementation exists; API and legacy bridge are `DEFERRED`.
**FR trace:** FR-P05-04, 05, 07, 11, 12, 14; prerequisite for FR-P06-01/02.
**Scope:** the WP-03 lifecycle only. It does not issue questions, determine SDA/SFL direction, select Primitives, form Coalitions, or compile a SemanticProgram.

## 1. Files and evidence read

- Phase 5 PRD separates Guest speech from inference.
- Phase 6 PRD separates Primitive Definition/Candidate/Coalition/Edge.
- WP-01–04 records establish object, state, and registry boundaries.
- Interview Expression has local source/transcript/read-only handoff code.
- `0001`–`0004` and `verify_wp03_first_slice.py` establish staging behavior.

## 2. Architectural role and boundaries

This is an evidence/state transition contract from a verified source span to an operator-confirmed bounded assessment. Interview Expression retains raw interview-truth ownership; AIR retains future semantic-production ownership; PostgreSQL/Supabase owns durable CAE state. A receipt records an operation but cannot be independent evidence of its claim.

## 3. Brownfield reality

| Surface | Existing behavior | Disposition |
|---|---|---|
| Interview Expression source/transcript/inventory services | local SQLite evidence + read-only AIR handoff | ADAPT later; do not replace |
| `FirstSliceSemanticOperations` | staging PostgreSQL transitions/receipts | EXTEND only through approved bridge |
| AIR `SemanticAuthorityService` | local semantic/epistemic validation | READ; no automatic adoption |
| WP-04 `RegistryResolver` | pinned immutable registry reads | READ only in future validation |

## 4. Functional requirement traceability

P05-04 maps to verified-source preconditions; P05-05 capture; P05-07 independent authentication; P05-11 bounded proposal; P05-12 receipt. P05-09/10/13/16 and every Phase-6/7 selection requirement are deferred in WP-05.

## 5. Canonical object/schema contract

`media_asset`, `source_package`, `evidence_item`, `evidence_span`, `evidence_authentication`, `semantic_assessment`, `assessment_evidence_link`, `command`, `event`, and `receipt` own identity/state/relation fields. JSONB carries bounded versioned payloads. Canonical JSON plus SHA-256 are database-verified for command/event/receipt envelopes.

## 6. Relationships, state, events, and temporal rules

```text
verified source package + verified media asset
  -> EvidenceCaptured (CREATED -> CAPTURED)
  -> EvidenceAuthenticated (CAPTURED -> AUTHENTICATED)
  -> SemanticAssessmentProposed (CREATED -> PROPOSED)
  -> SemanticAssessmentValidated (PROPOSED -> VALIDATED)
  -> SemanticAssessmentOperatorConfirmed (VALIDATED -> OPERATOR_CONFIRMED)
```

Every transition uses expected-version concurrency, registered contract, scoped idempotency, atomic command/transition/event/receipt writes, and rollback on failure. Authentication requires a distinct evaluator; confirmation requires a non-empty decision. Current state never overwrites history.

## 7. Authorized operations and agent program contract

- `cae.evidence.capture@1.0.0`
- `cae.evidence.authenticate@1.0.0`
- `cae.air.propose-assessment@1.0.0`
- `cae.air.validate-assessment@1.0.0`
- `cae.air.confirm-assessment@1.0.0`

Inputs are typed arguments. Allowed reads are source/asset/actor, evidence links, contracts, and aggregate state. Writes are restricted to the named tables in one transaction. Errors include `EVIDENCE_ERROR`, `PROVENANCE_ERROR`, `STATE_ERROR`, `CONTRACT_ERROR`, and `VALIDATION_ERROR`. Normal agents may not directly mutate these tables.

## 8. IR / runtime contract

The output is `OperationReceipt`: receipt ID, outcome, idempotency marker, transition identity, evidence references, and decision when required. It is not a Phase-7 `SemanticProgram`, renderer instruction, or registry authority.

## 9. Validation and error taxonomy

Missing actor/source/span, non-verified media, self-authentication, unauthenticated assessment evidence, and absent decision are errors. Stale versions and changed-payload idempotency reuse are conflicts. A future registry-aware validator must add `REGISTRY_ERROR` and reject missing, quarantined, or ambiguous IDs.

## 10. Implementation plan

1. WP-06 designs runbook/harness invocation and review evidence without an API adapter.
2. A later bridge maps immutable Interview Expression references into verified-source inputs and proves compatibility.
3. A later AIR package binds a pinned SDA/Primitive resolver and validator.
4. Do not generalize Phase-6/7 objects from this lifecycle.

## 11. Backward compatibility / migration / rollback

SQLite Interview Expression and AIR paths remain authoritative for their running behavior. The staging adapter is isolated. A future rollback disables the bridge flag and preserves Postgres receipts for diagnosis; it never mutates local sources. No legacy record has been migrated.

## 12. Acceptance criteria

| Given | When | Then | Failure example | Contract |
|---|---|---|---|---|
| verified source asset/package | capture runs | span, transition, event, receipt atomically exist | unverified asset | STC-EVID-000 |
| captured evidence + distinct evaluator | authenticate runs | evidence authenticates | capture actor self-attests | STC-EVID-001 |
| authenticated evidence | assessment validates | expected-version transition occurs | stale version | STC-AIR-001 |
| validated assessment + decision | confirm runs | confirmed receipt exists | empty decision | STC-AIR-002 |
| stored envelope | mutation/mismatch attempted | database rejects it | hash has different JSON | immutable envelope |

## 13. Dependencies

WP-02a foundation, WP-03 operation contracts, and private Storage are required. WP-04 is only a future extension dependency. StateM is not used and no source code is borrowed.

## 14. Testing and verification

| Claim | Fidelity | Counter-test / anti-gaming | Evidence |
|---|---|---|---|
| state sequence/receipts | E3 staging | stale version creates no event/receipt | PASS WP-03 |
| independent authentication | E3 staging | capture actor rejected | PASS WP-03 |
| immutable evidence | E3 staging | update/hash-payload mismatch rejected | PASS WP-03 |
| private source linkage | E3 staging | temporary object upload and cleanup | PASS WP-03 |
| semantic correctness/taste | E4 required | external evaluator + contrastive corpus | MISSING; no claim made |

No structural or staging result is evidence of human truth, semantic direction, audience response, or anti-centroid quality.
