# Gemini Execution Mandate — Phase 23 / CA-UPTL-01

**Status:** `DRAFT — BLOCKED UNTIL OPERATOR AUTHORIZES THIS MANDATE`  
**Phase ID:** `CA-UPTL-01`  
**Title:** Upstream Intelligence Completion (Registries, Reasoning Module, Semantic Chain Proof, AIR Generation Logic)  
**Execution classification:** Bounded implementation and synthetic-only proof on brownfield SQLite/repository surfaces; no live interview content, no real guests/workspaces/brands, no production deployment, no client data, no shared-staging mutation, no authority promotion  
**Required prior decision:** “Authorize CA-UPTL-01 as defined, and reclassify the CA-E3-08, CA-STAGE-09, and CA-ACCEPT-10 evidence records as `CLAIMS_UNVERIFIED_BY_OPERATOR` pending live-probe reproduction.”  
**Required completion gate:** `IMPLEMENT -> VERIFY -> OPERATOR_REVIEW`; no live testing, constitution authoring, or aggregate cutover begins within this mandate.

## 1. Authority, purpose, and boundary

CA-UPTL-01 is governed by the CAE Governance & Specification Bridge Bundle v3, particularly Implementation Gate, Reality-Contact Evaluation, Test Governance and Reward-Hacking, State/Transition Control, and Coding-Agent State-Control rules. It inherits accepted WP-00 through CA-GOV-02 records, the CA-MAP-01 scope/authority matrix, TS-CAE-TEN-001, and `docs/MASTER_SEQUENCING_PLAN.md` workstreams 0-D/1-A/2-A.

**Prior-chain qualification:** Independent operator-side verification on 2026-08-26 established that CA-E3-08, CA-STAGE-09, and CA-ACCEPT-10 recorded deployments, checksums, constraints, topology changes, and backup snapshots that could not be reproduced against any reachable environment (wrong target identity, non-matching SHA-256 values, absent composite FK, absent legacy quarantine, absent migration ledger entries). Those three phases are therefore **not accepted prior gates**. This mandate inherits from CA-GOV-02 and earlier only. Where this mandate cites a phase 20–22 artifact, it must cite it as `CLAIMS_UNVERIFIED_BY_OPERATOR`, never as proof.

The purpose is to complete the upstream intelligence substrate so that downstream constitutions, specs, and eventual live testing rest on working semantic machinery, per the operator’s ordered doctrine: upstream intelligence first, object constitutions second, operator reading pause third, implementation fourth.

The permitted transition is:

```text
brownfield registries + stubbed AIR services + SQLite-authoritative runtime
  -> registry defect dispositions (operator-supplied inputs; no invention)
  -> one real reasoning module bound via ProgrammedModelRegistry
  -> one demonstrated World -> Context -> SDA -> Edging chain on synthetic input
  -> real generation logic behind existing AIR capture/store services
  -> OPERATOR_REVIEW

constitution authoring (CA-CAN-02): NOT_STARTED until separately authorized
live video-interview testing: NOT_STARTED (no live project exists)
```

## 2. Mandatory reading

Before planning or editing, the executing agent SHALL read in full:

1. `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` (current truth record) and `CAE_GOVERNANCE_STATUS_MATRIX.md`.
2. `docs/PRD/CURRENT.md` (§1.3a execution-engine gap; §1.4a F17/F28/F29/F30 rows) and `docs/MASTER_SEQUENCING_PLAN.md` (workstreams 0-D, 1-A, 2-A briefs).
3. `CAE_WP04_REGISTRY_MIGRATION_PROOF.md` and the quarantine register: SFL failure-corpus references to absent families (`SFL-FAM-005`, `006`, `007`, `009`, `012`), duplicate primitive source ID `EXP-TRG-001`, and the 23 manifest-version-inherited SFL records.
4. Current registry/resolver source under the controlled staging snapshot code, `services/air/src/**` service modules named in Section 3, `services/pipeline/.../programmed_model_engine.py` and the `ProgrammedModelRegistry` contract.
5. `TS-CAE-EVID-001_EVIDENCE_TO_AIR_FIRST_SLICE.md`, applicable constitutions, and the WP-08 evaluation suite conventions for reward-hack non-claims.
6. Git history and working-tree state, identifying commits actually inspected and any unrelated changes.

If a required input is missing or contradictory, stop that sub-workstream as `BLOCKED_ON_OPERATOR_INPUT` — never infer, synthesize, or fabricate a substitute.

## 3. Exact scope: four sub-workstreams

### U1 — Registry defect dispositions (operator-input-gated)

Prepare a **Custodian Disposition Packet** covering: each absent SFL family reference, the duplicate `EXP-TRG-001` records, and each versionless SFL record class. For every defect, present exactly two decidable routes: (a) operator supplies authoritative corrected source bytes/lineage, or (b) operator ratifies permanent quarantine and the precise runtime refusal semantics. Implement only routes the operator has ratified in writing. The resolver SHALL emit typed, specific refusal reasons. Inventing a missing family, merging duplicates by heuristic, or synthesizing versions is prohibited.

### U2 — One real reasoning module via ProgrammedModelRegistry

Implement one genuine model-backed reasoning module bound through `ProgrammedModelRegistry` (Sequencing Plan 1-A; CURRENT.md §1.3a). It SHALL perform real inference over real inputs in the local development environment using operator-configured provider credentials from the approved runtime environment, and SHALL fail loudly when unavailable. Deterministic fakes, canned responses, or unconditional-success stubs presented as the module are prohibited. Record provider class, model identifier, invocation counts, token/latency metadata, and one full verbatim request/response transcript (synthetic content only) as evidence.

### U3 — One demonstrated semantic chain on synthetic input

Execute World → Context → SDA → Edging once end-to-end on a fresh synthetic specimen through the typed runtime path, producing command/event/receipt effects with payload SHA-256 integrity, immutable receipt append, and honest epistemic fields (`reward_hack_result: UNVERIFIED`). E2 repository-integrated fidelity minimum; a disposable E3 replay is permitted under the admission rules of prior E3 phases, with target identity, engine version, and teardown receipt recorded. No shared-staging writes. Complete transient cleanup with row/object-count receipts.

### U4 — Real generation logic behind existing AIR services

Replace the stubbed generation paths behind the existing capture/store services for F17/F28/F29/F30 (archetype, coalition, primitive, brand, learning services) with logic that calls the U2 module, honoring existing service contracts and persistence. Each feature ships with contrastive tests distinguishing real output from stub output, and a documented failure route when the model layer is unavailable.

Sub-workstream order is U1 → U2 → U3 → U4; U3 depends on U2; U4 depends on U2. If any sub-workstream outgrows this mandate, stop and propose a split for operator approval instead of expanding scope silently.

## 4. Evidence protocol (live-probe mandatory — applies to every dynamic claim)

Following the phase 20–22 failure, no dynamic claim is proven by prose. Every executed action MUST commit verbatim probe artifacts:

1. The exact command or SQL executed, plus raw stdout/stderr, pasted unedited into the evidence record and committed.
2. For any database effect: a post-state read-back query and its raw result rows/counts.
3. For any checksum claim: the hash computed in the same session from the exact committed bytes, with the command shown.
4. For any external call: redacted request shape and full response body (secrets removed), or the failure output.
5. Static validators introduced by this mandate MUST execute probes (run tests, query state, compute hashes) — a validator that only confirms document presence or status strings is non-compliant and must not be written.

An evidence record whose probe artifacts cannot be re-executed by an independent reviewer byte-for-byte is `UNPROVEN` by default.

## 5. Authorized artifacts and prohibitions

Gemini MAY create or update only:

- `docs/cae/implementation/CAE_UPTL_01_ADMISSION_RECORD.md`;
- `docs/cae/implementation/CAE_UPTL_01_CUSTODIAN_DISPOSITION_PACKET.md` (U1);
- `docs/cae/implementation/CAE_UPTL_01_REASONING_MODULE_PROOF.md` (U2);
- `docs/cae/implementation/CAE_UPTL_01_SEMANTIC_CHAIN_EVIDENCE.md` (U3);
- `docs/cae/implementation/CAE_UPTL_01_AIR_GENERATION_PROOF.md` (U4);
- `docs/cae/implementation/CAE_UPTL_01_COMPLETION_RECORD.md`;
- `docs/cae/implementation/CAE_IMPLEMENTATION_CONTROL_STATE.md` (status + phase 20–22 reclassification only);
- implementation/test source strictly within: the AIR service modules named in Section 3, the pipeline programmed-model engine surface, registry resolver refusal semantics, and new tests under `tests/` for these surfaces;
- one probe-executing validator under `scripts/cae/audit/verify_ca_uptl_01.py`.

Gemini SHALL NOT: touch live media, real guests, real workspaces, brands, or any interview transcript resembling a natural person; deploy to production or shared staging; mutate `.env`; promote any aggregate authority; modify migrations already applied to any persistent environment; delete or rewrite historical evidence records (annotate classifications only); begin CA-CAN-02; or represent any deterministic fake as model-backed inference.

## 6. Adversarial challenges (each must be answered in the Completion Record)

1. A stub, mock, or canned response is presented as the U2 reasoning module. — Prove real inference via verbatim transcript and failure-on-unavailable behavior.
2. The semantic chain (U3) is claimed proven because tables received rows, without receipts, integrity fields, or honest epistemic states. — Show receipt payloads and SHA-256 verification.
3. Registry defects (U1) quietly disappear — merged, renamed, or ignored — instead of operator-ratified dispositions. — Reconcile every registered defect ID to a disposition.
4. Probe outputs are generated once, then hand-edited. — Reviewer must reproduce every artifact byte-for-byte from the committed commands.
5. Local E2 success is upgraded to an E3 or staging claim without admission records. — Classify fidelity per claim; no upgrades.
6. Cleanup is asserted without counts. — Commit post-teardown count queries showing zero residue.
7. F17–F30 pass tests that cannot distinguish real from stubbed behavior. — Show the contrastive tests failing against the old stubs.
8. Scope expands into constitution authoring, live testing, or cutover. — Any such work invalidates the mandate.
9. Phase 20–22 records are cited as accepted priors. — Every citation must carry `CLAIMS_UNVERIFIED_BY_OPERATOR`.
10. Provider credentials are printed, logged, or committed. — Secret-safe redaction required; violation stops the mandate.

## 7. Completion, rollback, and operator gate

CA-UPTL-01 completes only when: all four sub-workstreams reach their stated gates or are explicitly `BLOCKED_ON_OPERATOR_INPUT` with the blocking question isolated; every dynamic claim carries reproducible probe artifacts; the probe-executing validator passes against the committed tree; transient state is purged with count receipts; and the control state records only truthful statuses including the phase 20–22 reclassification.

The Completion Record must provide Sections A–H in the established form: what changed; what is proven versus limited/blocked; observed-versus-inherited evidence; fidelity classes; falsification routes; registry-disposition ledger; reviewer-independence declaration (implementer cannot self-accept; name the independent review lane); and the one next decision required.

**Rollback:** Implementation occurs on branch or committable units such that each sub-workstream can be reverted independently without touching inherited evidence. No persistent-environment mutation occurs in this mandate; therefore no infrastructure rollback route is required.

Gemini SHALL request exactly:

> **Accept CA-UPTL-01 upstream-intelligence completion evidence as stated (or its explicitly blocked subset), preserve all UNVERIFIED/non-claim boundaries including `reward_hack_result: UNVERIFIED`, confirm the `CLAIMS_UNVERIFIED_BY_OPERATOR` reclassification of CA-E3-08/CA-STAGE-09/CA-ACCEPT-10, and authorize CA-CAN-02 for constitution-set authoring only — with no live testing, production deployment, or authority change?**

It SHALL stop after this question.

## 8. Gemini activation prompt (approximately 270 words)

You are the CAE governed execution agent for `CA-UPTL-01 — Upstream Intelligence Completion`. This mandate is blocked until the operator authorizes it and confirms the reclassification of CA-E3-08/CA-STAGE-09/CA-ACCEPT-10 as `CLAIMS_UNVERIFIED_BY_OPERATOR`. Read the control state, PRD §1.3a/§1.4a, Master Sequencing Plan workstreams 0-D/1-A/2-A, the registry quarantine records, AIR service sources, ProgrammedModelRegistry contract, and governing Bundle protocols before planning.

Execute four gated sub-workstreams in order. U1: build a Custodian Disposition Packet for every SFL/primitive registry defect and implement only operator-ratified routes; never invent families or merge duplicates heuristically. U2: bind one real model-backed reasoning module through ProgrammedModelRepository conventions; deterministic fakes presented as inference are prohibited; capture one full verbatim synthetic transcript. U3: demonstrate World → Context → SDA → Edging once on synthetic input with immutable receipts and honest `UNVERIFIED` epistemic fields; E2 minimum, disposable E3 permitted, no shared-staging writes. U4: replace F17/F28/F29/F30 stubs with real generation logic behind existing services, with contrastive tests that fail against stubs.

Every dynamic claim requires committed live-probe artifacts: exact commands, raw outputs, read-back queries, session-computed hashes. Validators must execute reality probes; presence-only validators are non-compliant. If an input is missing, stop that item as `BLOCKED_ON_OPERATOR_INPUT` — never fabricate. No live interviews, real guests, production, `.env` changes, or authority promotions. Commit only allowed artifacts, request the exact Section 7 decision, and stop.
