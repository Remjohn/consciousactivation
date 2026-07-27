# ST-05.02 Implementation Report

## Outcome

`ST-05.02 / SYNTHETIC_SKILL_NECESSITY` is implemented for the repository-owned, category-neutral synthetic Builder Core proof. The Builder now evaluates each of the five governed capability requirements independently and emits an immutable `NO_NEW_SKILL_REQUIRED` decision only when explicit deterministic Builder-owned implementation and ownership evidence satisfies every capability.

This is distinct from ST-05.01: an empty registry is an input, not proof of non-necessity. A capability gap, unregistered requirement, unverifiable ownership claim, conflicting evidence, material adaptation, prohibited operation, stale lineage, or invalid authority fails closed.

## Governed result

All five capabilities receive exactly one `BUILDER_OWNED_CODE` verdict:

| Capability | Owning module | Owning phase | Evidence |
|---|---|---|---|
| `deterministic_contract_validation` | `governed_contract_module` | `governed_contract_ready` | ST-05.01 declaration plus deterministic validation implementation evidence |
| `governed_run_lifecycle` | `atomic_boundary_module` | `ratified_boundary_ready` | ST-05.01 declaration plus governed lifecycle implementation evidence |
| `governed_task_acceptance` | `atomic_boundary_module` | `ratified_boundary_ready` | ST-05.01 declaration plus governed acceptance implementation evidence |
| `immutable_receipt_emission` | `governed_contract_module` | `governed_contract_ready` | ST-05.01 declaration plus immutable receipt implementation evidence |
| `synthetic_target_profile_binding` | `atomic_boundary_module` | `ratified_boundary_ready` | ST-05.01 declaration plus synthetic profile binding implementation evidence |

Each decision records the required behavior, implementation evidence hash, reliability evidence, authority boundary, context, failure responsibility, justification, policy, and complete lineage. The governed alternative order is recorded for every capability before selecting deterministic code.

The aggregate result is:

- external skills required: `0`
- missing required skills: `0`
- adaptations required: `0`
- experiments required: `0`
- JIT capsules required: `0`
- skill execution required: `false`
- production skill certification: `false`
- Skill Design Brief disposition: `NOT_APPLICABLE_NO_GAP`

## Requirement satisfaction

- `AG-008`: deterministic code and all governed alternatives are considered before any skill proposal.
- `FR-084`: a formal capability-by-capability necessity test and attributable receipt precede any JIT skill work.
- `FR-085`: exact reuse, local adaptation, and bounded composition are explicitly assessed before new canonical capability authorization.
- `FR-086`: a material gap or adaptation requires a typed Skill Design Brief; no brief is fabricated for the proven no-gap result.

## Implementation boundaries

The change adds typed domain contracts, an application command service, in-memory development/test persistence, run attachment/replay, descendant invalidation, atomic commit behavior, and deterministic observations. It adds no external dependency, database, transport, runtime execution, schema file, shared-contract fork, real skill, discovery, packaging, model/provider invocation, workflow execution, Atomic Harness Definition compilation, Format 02 behavior, VAE/Delegation behavior, conversational behavior, or production claim.

## Validation

- preimplementation regression: `380/380 PASS`, no mandatory skips
- ST-05.02 Story suite: `24/24 PASS` twice
- complete repository regression: `404/404 PASS` twice, no skips
- Python source compilation: PASS
- architecture boundaries: PASS
- deterministic fresh-context equality: PASS
- atomic failure and clean retry: PASS
- replay, resume, idempotency, invalidation, and historical reproduction: PASS

The only emitted warning is the repository's pre-existing `pytest-asyncio` loop-scope deprecation warning.

