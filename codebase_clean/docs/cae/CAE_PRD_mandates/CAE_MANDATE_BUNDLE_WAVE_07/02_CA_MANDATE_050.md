# CAE Mandate CA-M050 — Cryptographic Evidence DAG Construction, Pruning, and Acyclic Verification

**Status:** Proposed governed execution mandate for Wave 07.  
**Canonical decision:** Q49  
**Mandate ID:** `CA-M050`  
**Governing invariant:** `INV-DAG-001`  
**Primary implementation surface:** `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py (evidence topology and transition receipt handling)`

## 1. Identity and status

This mandate authorizes one bounded implementation phase in the final Wave 07 hardening tranche. It is an execution contract, not a design essay and not permission to redesign adjacent systems. The mandate remains subordinate to the repository constitutional layer and may not create runtime authority merely by adding prose, tests, metadata, or a new helper. Its status is **execution-ready when its mandatory-reading set and declared preconditions are satisfied**. Completion means the artifact exists, its proof standard is met, limitations are recorded, control state is updated, and an exact commit is captured.

The canonical decision is Q49; the execution identifier is CA-M050. The primary invariant is `INV-DAG-001`. This mandate consumes earlier decisions but does not reopen them. Any apparent collision with an earlier invariant must be treated as an authority conflict and escalated through the protocol’s collision procedure rather than resolved by convenience.

## 2. Decision / objective being authorized

The authorized objective is:

> **Establish the evidence topology as a durable, strictly acyclic, multi-parent causal DAG whose nodes point backward to authoritative evidence and whose rejected alternatives are explicitly pruned rather than silently discarded.**

This objective exists to convert an already-ratified runtime requirement into a physically verifiable implementation contract. The executor shall define the smallest change set capable of proving the objective at the actual boundary named below. “Improved,” “more robust,” “secure enough,” or “benchmark passed” are not completion predicates unless the evidence described later establishes the intended property. The executor may refactor inside the declared boundary when necessary for correctness, but may not use refactoring as a pretext to alter upstream meaning or downstream authority.

The intended outcome is a durable property of the system, not a screenshot, a narrative assertion, or a green test detached from the real boundary. The objective must survive process boundaries, persisted-state reopen, failure/recovery conditions, and adversarial negative cases where those conditions are material to the invariant.

## 3. Governing doctrine and authority sources

The governing doctrine is the CAE constitutional rule that downstream realization cannot legitimately invent upstream meaning and that runtime authority must be distinguished from source-of-meaning and change/promotion authority. The normative authoring grammar is `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`. The execution behavior is further constrained by `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` and the canonical decision evidence in `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`.

Meaning authority comes from the ratified Q decision, the Master 57-question canon, the decision ledger, Architecture, UI, and the applicable PRD/functional requirement. Runtime authority comes from the canonical persisted state, receipt, registry, dispatcher, or public API path named by this mandate. Change or promotion authority belongs to the permitted Operator or repository governance process; the executor cannot self-promote a result merely because validators pass.

The executor must not infer authority from a file merely because it exists. A test file does not authorize runtime behavior. A YAML manifest does not outrank a canonical registry. A UI projection does not become state authority. A receipt describes a committed state transition but cannot authorize an unrelated transition. Every material conclusion must identify its evidence class.

## 4. Mandatory reading before action

Before editing, running migrations, changing state, or declaring a verifier green, the executor SHALL read:

- docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md
- docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md
- docs/cae/cae-bmad/03_product/FUNCTIONAL_REQUIREMENTS.md
- Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md
- Context Chat/Architecture.md
- Context Chat/UI.md
- Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md
- Prior mandate bundles in working context: Wave 01, Wave 02, Wave 04, Wave 06


Additionally, the executor SHALL inspect the exact implementation/test files named in Sections 5–8 and the immediately preceding mandate outputs that materially constrain this boundary. The executor must verify the repository state before acting; stale assumptions, absent files, renamed symbols, or changed schema must be recorded rather than silently papered over.

Reading is not authorization to modify everything read. Mandatory reading establishes context and collision detection. Only Section 6 grants file/artifact authority.

## 5. Exact scope

**Objective:** Establish the evidence topology as a durable, strictly acyclic, multi-parent causal DAG whose nodes point backward to authoritative evidence and whose rejected alternatives are explicitly pruned rather than silently discarded.

**Dependencies:** Q41–Q48, especially durable state transitions, parent-linked receipts, replay parity, tenant fencing, and registry pinning.

**Allowed runtime/code surface:** `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py (evidence topology and transition receipt handling)`

**Inputs:** canonical prior state/receipts, declared policy/configuration, persisted evidence, operator decisions where applicable, and test fixtures explicitly required by the functional requirement.

**Outputs:** evidence_refs serialization, DAG traversal/validation helpers, PRUNED_REJECTION markers, targeted tests and machine-readable evidence reports.

**Operators allowed:** the bounded CAE coding/execution agent may inspect, edit, test, and document within the allowed boundary; only the authorized Operator may approve, reject, or defer the completed mandate.

**Validators required:** repository tests plus the mandate-specific positive/negative tests and the false-proof countercase. Where a persistence or process-boundary invariant is material, validators must reopen persisted state or exercise separate worker/process connections rather than relying only on in-process behavior.

The executor shall preserve existing API compatibility unless the canonical requirement explicitly authorizes a contract change. Any unavoidable interface impact must be documented as a collision and stopped for Operator decision.

## 6. Allowed artifacts and file boundary

The executor may change only the primary implementation surface, directly associated tests, schema/migration artifacts needed to establish the declared invariant, and mandate evidence artifacts. Supporting documentation may be updated only when the changed behavior would otherwise contradict an already-ratified contract. Generated reports may be written under the bundle/evidence boundary.

For this mandate, the principal surface is `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py (evidence topology and transition receipt handling)`. The intended artifact class is `evidence_refs serialization, DAG traversal/validation helpers, PRUNED_REJECTION markers, targeted tests and machine-readable evidence reports.`. No change to unrelated UI surfaces, upstream semantic definitions, external integrations, deployment topology, or later-wave/question contracts is authorized unless a required dependency inside the declared surface makes the change unavoidable. In that case, stop and request an Operator collision decision rather than broadening scope unilaterally.

The executor shall keep generated evidence reproducible enough that another agent can distinguish repository behavior from test-only fixtures. When secrets, personal data, or sensitive operator material are encountered, they must not be copied into evidence artifacts.

## 7. Prohibitions and collision procedure

The mandate explicitly prohibits the following: Do not redefine evidence meaning, mutate immutable source media, collapse a DAG to a linear list, infer missing parents, or treat successful topological sorting as proof that semantic provenance is correct.

A collision occurs if the required implementation contradicts an earlier ratified invariant, depends on an unavailable authority, requires an undeclared file boundary, or would make a downstream artifact authoritative over an upstream source. On collision, **do not choose the locally convenient interpretation**. Freeze the conflicting change, document the two competing authorities, cite the exact file/decision lines, state the minimum consequence, and request an Operator decision. The collision record itself is evidence; the absence of a decision is a stop condition.

No shortcut is acceptable merely because it makes the test green. In particular, process-local synchronization cannot prove distributed storage semantics; in-memory registries cannot prove persistent immutability; synthetic outputs cannot prove live execution; high model scores cannot prove certification authority; and plausible generated preference pairs cannot prove that operators actually made the choices represented.

## 8. Required work / implementation behavior

The executor shall first inspect the current implementation and write a narrow implementation plan tied directly to the invariant. Next, implement the minimum behavior required to establish the contract at the real boundary. Preserve source-of-meaning and prior receipt lineage. Where state changes occur, record:

`source state → operation → target state`

and identify actor, preconditions, validators, postconditions, receipt, error route, and recovery path.

For this mandate, the specific required behavior is: Implement or harden graph construction from persisted receipt/evidence references; validate node identity, parent existence, workspace scope, deterministic ordering, cycle rejection, and explicit pruning semantics; provide negative tests for multi-parent, missing-parent, cycle, and cross-tenant contamination cases.

The executor must include a contrastive negative test for the following false-proof case:

> A report shows every node in a neat chronological list and a topological-sort routine returns success, but one branch references the wrong workspace or an inferred parent that was never persisted. The result looks organized yet violates backward provenance and evidence authority.

A passing result is insufficient if the verifier can be satisfied without physical contact with the intended runtime boundary. Tests must be explicit about what they measure and what they do not measure. Environment fidelity must be recorded whenever the property depends on separate processes, real persistence, real provider behavior, actual filesystem resolution, or a public API path.

## 9. Verification and evidence standard

Every substantive result shall be tagged using one or more evidence classes: `EXECUTABLE, SCHEMA, TEST, REGISTRY_SOURCE, OPERATOR_DECISION_REQUIRED`. The verifier must establish the intended property, not merely a correlated symptom.

Required proof includes positive acceptance, negative/blocked behavior, the stated false-proof countercase, and the environment-fidelity condition relevant to the runtime boundary. If the implementation depends on persisted state, reopen the state from durable storage. If it depends on cryptographic lineage, recompute from the canonical persisted payload. If it depends on tenant or sandbox fencing, attempt a forbidden cross-boundary access. If it depends on live execution, prove that actual worker/model/tool activity occurred rather than only observing an aggregate row.

The evidence packet shall contain: changed-file list; commands/tests executed; pass/fail results; invariant-specific observations; limitations; relevant hashes/identifiers; and the exact commit SHA. Semantic conclusions may be written as HYPOTHESIS until an executable or schema/test artifact verifies them.

## 10. Completion and stop condition

The mandate is complete only when the intended artifact exists, the required positive and negative proofs pass, the false-proof countercase is rejected, limitations are recorded, the control-state record is updated, and the exact commit SHA is captured.

Stop immediately when: a mandatory authority source is unavailable; a dependency is not in the expected state; a migration is unsafe or irreversible without decision; a validator would require adjacent work; a required environment cannot be faithfully exercised; evidence contradicts a prior ratified rule; or the executor reaches the end of the declared scope. Do not continue into Q57 or any other later decision under the guise of cleanup.

The final action is not “ship.” The final action is to present the evidence packet and request the Operator decision: **approve**, **reject with findings**, or **defer pending named remediation**.

## 11. Rollback / recovery

Rollback must restore the last known authoritative state without deleting immutable evidence. Code changes shall be reverted through normal version control. Schema changes shall use the repository-supported migration/recovery mechanism; the executor shall not rewrite an append-only migration ledger. Persisted state changes must use the same canonical transition path that created them whenever possible. If a partially completed migration or runtime mutation has occurred, stop execution, record source and target states, preserve receipts/logs, and use the declared recovery mechanism rather than manual database surgery.

Recovery evidence must state whether any receipts, telemetry, benchmark records, or derived artifacts were created before failure and whether they remain valid, invalidated, or merely incomplete. No recovery action may erase evidence of an unsafe attempt merely to make the workspace look clean.

## 12. Operator decision

The executor is authorized to complete only the bounded work in Sections 5–8. After verification, the executor shall report the exact artifact set, evidence classes, negative-test results, limitations, rollback status, and commit SHA. The Operator must explicitly choose one of:

**APPROVE** — the invariant is physically evidenced within scope.  
**REJECT** — the evidence is insufficient or the implementation violates the contract.  
**DEFER** — named remediation or an authority decision is required before further execution.

No Operator decision may be inferred from silence, a green CI result, or the existence of a mergeable commit. Approval of this mandate does not approve Q57 or any unrelated work.

## 13. 200–300 word activation prompt

Execute CA-M050 (Q49) only. Read 01_CA_MANDATE_AUTHORING_PROTOCOL.md, 02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md, FUNCTIONAL_REQUIREMENTS.md FR-049, CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md, Architecture.md, UI.md, the implementation-readiness assessment, and the relevant prior Wave 06 mandates before action. Meaning authority is the ratified Q49 decision and evidence doctrine; runtime authority is the persisted receipt/state path; promotion authority remains with the Operator. Objective: establish a durable, strictly acyclic, multi-parent evidence DAG with explicit PRUNED_REJECTION branches. Work only in the named program_operator_runtime.py surface, its directly required tests/schema/evidence artifacts. Do not invent parents, flatten the DAG, mutate immutable source evidence, or treat topological sorting alone as proof. Verify persisted node identity, parent existence, workspace binding, deterministic traversal, cycle rejection, and explicit pruning. Include positive and negative tests, especially a false-proof case where a neat chronological list or successful sort hides an inferred or cross-tenant parent. Record evidence classes, changed files, commands, limitations, control-state update, and exact commit SHA. Stop on authority collision, missing dependency, undeclared file boundary, unsafe migration, or any need to alter later questions. Completion requires executable proof and rejection of the false-proof countercase. Request Operator decision: APPROVE, REJECT with findings, or DEFER with named remediation. Do not execute Q57 or adjacent work. Preserve canonical parent references exactly as persisted and do not treat ordering convenience as provenance.
