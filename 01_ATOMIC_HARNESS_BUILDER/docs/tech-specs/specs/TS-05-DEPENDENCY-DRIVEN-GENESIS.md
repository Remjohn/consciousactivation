# TS-05: Dependency-Driven Genesis

Status: `SPEC_RATIFIED_PENDING_STORY_MAPPING`

## Traceability

- Owned: FR-041 through FR-050.
- Decisions: D002, D010, D011, D019, D025, D026, D027.
- Supporting NFRs: NFR-OBS-002, NFR-REL-002, NFR-TRACE-002, NFR-TRACE-004, NFR-UX-002.

## Responsibility And Authority

Own typed constitutional decision nodes, dependencies, one-question interaction, evidence-backed recommendations, separate human answers/final decisions, transactional Harness IR updates, contradiction reopening, provisional drafting, cascade lock, receipts, and resumable memory.

Deterministic code owns graph eligibility, transaction validation, dependency/invalidation, and receipts. Agents generate bounded recommendations from declared evidence/capsules. Humans own final constitutional decisions and ratification.

## Modules And Components

`genesis/definitions.py`, `genesis/graph.py`, `genesis/recommendations.py`, `genesis/transactions.py`, `genesis/ratification.py`, and `application/genesis_commands.py`.

## Canonical Data Structures

- `DecisionDefinition { decision_key, question, owned_ir_paths, dependencies, evidence_requirements, allowed_options, authority, invalidates }`
- `DecisionInstance { instance_id, definition_ref, status, recommendation_ref?, human_answer_ref?, final_value_ref?, version }`
- `Recommendation { option, rationale, evidence_refs, alternatives, risks, confidence, model_and_capsule_identity }`
- `DecisionReceipt { before_ir_hash, after_ir_hash, answer, final_value, actor, reason, evidence_refs, invalidated_nodes, signed_at }`
- Status: `LOCKED`, `READY`, `QUESTIONED`, `PROVISIONAL`, `RATIFIED`, `REOPENED`, `CASCADE_LOCKED`.

## APIs, Commands, Events, Persistence

- Commands: `StartGenesis`, `GetNextQuestion`, `RecordRecommendation`, `RecordHumanAnswer`, `CommitDecision`, `ReopenDecision`, `RatifyProvisionalGraph`, `CascadeLockGenesis`.
- Events: `GenesisStarted`, `DecisionBecameReady`, `QuestionIssued`, `RecommendationRecorded`, `HumanAnswerRecorded`, `DecisionCommitted`, `DecisionReopened`, `GenesisCascadeLocked`.
- Persistence: definitions as versioned policy artifacts; instances in Harness IR; receipts in event ledger/CAS.
- Transaction: expected Harness IR revision and decision version are mandatory. One commit atomically appends events and writes the new IR revision.

## Dependency, Invalidation, Idempotency, Resume

Only nodes whose dependencies are ratified may be questioned. Exactly one primary question is active per run. A reopened node traverses declared dependency edges, preserves unaffected decisions, and marks descendants `REOPENED` with reasons. Command IDs prevent duplicate answers or decisions. Resume reconstructs active question and provisional state from events.

## Security And Isolation

Recommendation agents receive only the decision-specific capsule and evidence. They cannot inspect protected benchmark labels, sign decisions, alter dependencies, or issue waivers. Human actions require authenticated identity and explicit confirmation of the final value.

## Observability, Cost, And Performance

Track ready/locked/reopened counts, question latency, recommendation cost, human edit distance from recommendation, contradiction frequency, transaction conflicts, and invalidation fan-out. Graph operations must remain linear in nodes plus edges.

## Failures And Recovery

Missing evidence keeps a node locked. Concurrent commits return a typed conflict and refresh current state. A malformed recommendation is discarded without changing the graph. Contradictions route to the owning upstream node. Cascade lock fails if any required node is non-ratified or any hard gate is unresolved.

## Acceptance Tests

1. At most one primary question is active.
2. Dependency-locked nodes cannot be answered or committed.
3. Human answer and final decision are distinct immutable fields.
4. A commit atomically updates IR, decision state, events, and receipt.
5. Reopening invalidates all and only declared descendants.
6. Provisional values cannot satisfy implementation authorization.
7. Resume restores the exact active question without replaying prior decisions.
8. Cascade lock fails on unresolved contradictions or provisional nodes.

## Implementation Tasks

1. Define decision graph, statuses, recommendation, and receipt schemas.
2. Implement pure dependency and invalidation algorithms.
3. Implement transactional command handlers and persistence port.
4. Implement bounded recommendation capsule interface.
5. Add human ratification/API/Control Tower command contracts.
6. Add graph property, concurrency, replay, and authority tests.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Preserve constitution-complete Shared Activative Core lineage in Genesis decisions | genesis_owner | Genesis may propose decisions; Activation Compiler source objects and human ratification retain truth authority | frozen refs for Identity DNA, Context Premise, Resonance, Matrix of Edging, Activative Intelligence Pack, wrong-reading locks | Block ratification on missing rich refs or sparse-token-only evidence | sparse-to-rich resolution and stale-version fixture | Every affected decision resolves exact rich objects and versions | Existing sparse fields remain readable but cannot authorize V1.2 output without rich refs |
| Route Identity DNA updates as proposals only | genesis_owner | Builder proposes; human identity authority merges | `IdentityDNAAmendmentProposal` | Reject automatic merge or unsigned disposition | agent-authority negative test | proposal remains pending until human-signed approval/rejection | New additive proposal contract; no mutation of existing Identity DNA records |

## Non-Goals And Migration

Genesis does not choose product authority, evaluate downstream quality, or migrate any absent V2.1 decision graph.
