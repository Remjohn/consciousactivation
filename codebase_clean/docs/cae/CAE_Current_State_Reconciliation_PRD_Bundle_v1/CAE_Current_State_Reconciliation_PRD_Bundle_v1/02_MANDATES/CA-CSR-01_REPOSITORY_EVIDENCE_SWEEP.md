# CA-CSR-01 — Repository Evidence Sweep

Status: `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`
Program: `CAE Current-State Reconciliation & PRD Synchronization`
Atomic boundary: establish the evidence base; do not reconcile or edit the canonical PRD.

## 1. Identity and status

**Mandate ID:** `CA-CSR-01`

**Objective:** Build one reproducible repository evidence inventory covering the current CAE control plane, executable implementation, tests, specifications, skills, mandates, program-status records, and current PRD claims.

**Completion state:** `EVIDENCE_BASE_READY`

## 2. Decision / objective being authorized

Determine what can be observed directly in the current repository and current checked-out revision. This phase creates the evidence inputs required by later reconciliation. It does not decide whether two artifacts are redundant and does not update `docs/PRD/CURRENT.md`.

## 3. Governing doctrine and authority sources

Mandatory authorities:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/skills/EVIDENCE_TO_AIR_FIRST_SLICE_SKILL.md`
- `docs/PRD/CURRENT.md`
- `governance/program-control/03_PROGRAM_STATUS/MASTER_STATUS.md`
- `governance/program-control/03_PROGRAM_STATUS/STATUS_TRUTH_RECONCILIATION.yaml`
- `docs/cae/cae_mandate_bundle/` current mandate authoring/execution material
- `docs/cae/editorial_intelligence/` current authority/dependency/object artifacts
- relevant current Tech Specs and object constitutions
- current `.zcode/plans/` records relevant to recently executed work

## 4. Mandatory reading before action

Read the full authorities above. Then inspect the repository at the exact checked-out commit using `git rev-parse HEAD`, `git status --short`, and repository-native inventory/search commands.

Inspect at minimum:

- `docs/PRD/`
- `docs/tech-specs/`
- `docs/cae/`
- `governance/program-control/`
- `.zcode/plans/`
- `services/`
- `api/`
- `packages/`
- `apps/`
- `tests/`
- `infra/`
- database migrations / schema surfaces
- authoring skills and mandate bundles

The agent must inspect code for claims that matter rather than treating status documents as executable proof.

## 5. Exact scope

Produce a single evidence packet under an existing repository status surface where possible. If no suitable target exists, use the scoped path:

`governance/program-control/03_PROGRAM_STATUS/RECONCILIATION_2026-08-30/`

The packet must contain:

- repository revision and working-tree state;
- artifact inventory;
- executable-surface inventory;
- test/verification inventory;
- current-state claims extracted from PRD and control-state documents;
- recent mandate/plan execution records located in the repository;
- evidence references sufficient for an independent verifier to reproduce the observations.

## 6. Allowed artifacts and file boundary

Allowed: the reconciliation evidence packet and necessary append-only status evidence in the designated reconciliation directory.

Prohibited: `docs/PRD/CURRENT.md`, production code, migrations, registries, canonical object definitions, shared runtime state, and unrelated documentation.

## 7. Prohibitions and collision procedure

Do not decide “implemented” from the existence of a file. Do not infer runtime behavior from a type or docstring. Do not delete or rewrite legacy artifacts. If two sources disagree, record both claims for CA-CSR-02.

Contrastive failure: a status table saying “implemented” with a matching filename but no executable path or test evidence is **not** sufficient proof.

## 8. Required work / implementation behavior

1. Establish exact repository revision.
2. Inventory current authority/status surfaces.
3. Trace each material current-state claim to executable/document/test/receipt evidence.
4. Locate evidence of completed CAE mandates, especially `CA-M00…CA-M12` and the most recent control-state updates.
5. Locate current Editor Intelligence objects and dependency chain.
6. Identify status records that are stale, newer than the PRD, or contradictory.
7. Capture limitations and unavailable environments.

## 9. Verification and evidence standard

For every material row capture:

`claim | evidence_class | exact_path_or_symbol | observed_fact | verification_command_or_read_method | limitation`

Do not use a score as proof. The environment must be identified for executed checks.

## 10. Completion and stop condition

Complete only when the evidence packet exists, the repository revision is recorded, and all high-materiality claims have an evidence class and source.

Stop before editing the PRD or resolving conflicts.

## 11. Rollback / recovery

If a write fails, leave existing repository status untouched. If evidence collection is incomplete, mark the packet `INCOMPLETE` and stop. Do not fabricate missing evidence.

## 12. Operator decision

Report whether the evidence base is sufficient for CA-CSR-02.

Operator question: **“Do you authorize reconciliation against this evidence base?”**

## 13. Activation prompt

Gemini: execute `CA-CSR-01` only. Load `01_CA_MANDATE_AUTHORING_PROTOCOL.md`, `02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`, `EVIDENCE_TO_AIR_FIRST_SLICE_SKILL.md`, the current PRD, current program-status records, current Editorial Intelligence authority artifacts, and the repository's current mandate/plan records. Inspect the exact checked-out repository revision before trusting any status claim. Your sole objective is to produce a reproducible evidence packet establishing what actually exists in code, tests, specifications, control-state records, skills, mandates, and plans. Do not reconcile conflicts, redesign architecture, update the PRD, or delete anything. For each material claim, record evidence class, exact path/symbol, observed fact, verification method, and limitation. Pay particular attention to evidence of completed CA-M00 through CA-M12 work and the current Editorial Intelligence chain, but do not assume their execution merely because mandate files exist. A green test proves only what it ran. A document proves only that the document says something. Leave an explicit record of missing or unavailable evidence. Use the governed sequence: load authority, verify preconditions, build a bounded plan, execute only within this mandate, verify, record evidence, update only the designated reconciliation record, commit, request the operator decision, and stop. Operator decision: whether this evidence base is sufficient for CA-CSR-02.
 The governing execution references are the full files `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` and `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`; load them verbatim before planning. Do not substitute a summary for either authority. If a repository source cannot be read, record the exact missing path and classify the dependency rather than guessing. 
