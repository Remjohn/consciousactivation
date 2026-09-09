# CAE Test Governance & Reward-Hacking Defense v2.0

## 1. Scope

This protocol governs how unit tests, integration tests, validators, contract tests, adversarial tests, taste checks, and runtime observations are designed so that passing tests represent meaningful evidence rather than proxy optimization.

## 2. Test taxonomy

Every CAE test MUST be assigned a primary test class:

| Class | Purpose |
|---|---|
| `STRUCTURAL` | schema/type/contract correctness |
| `RELATIONAL` | relationship/cardinality/direction correctness |
| `STATE` | state transition and temporal correctness |
| `EVIDENCE` | provenance/authentication/immutability correctness |
| `SEMANTIC` | SDA/edge/meaning integrity |
| `PERCEPTUAL` | SFL/realization/perception constraints |
| `ANTI_CENTROID` | resistance to genericizing drift |
| `REWARD_HACK` | resistance to proxy gaming |
| `ENVIRONMENT_FIDELITY` | verifies the test environment matches claim requirements |
| `RUNTIME` | integrated execution and receipt behavior |
| `OUTCOME` | observed external/human/world result |

A single test may have secondary tags, but one primary class is required.

## 3. Required test contract

Each material test record MUST identify:

```yaml
test_id:
claim_id:
class:
subject:
preconditions: []
fixture_source:
required_environment_fidelity:
actual_environment_fidelity:
execution_path:
assertions: []
expected_failure_mode:
reward_hacking_scenario:
taste_risk:
anticentroid_risk:
evidence_status:
receipt_required:
```

## 4. Proxy-to-intent mapping

For each material evaluator create a table:

| Proxy being measured | Intended property | Known gaming strategy | Counter-test | Residual risk |
|---|---|---|---|---|

The evaluator is incomplete until a known gaming strategy has been considered.

## 5. False-proof tests

A false-proof test is intentionally designed to produce a superficially positive result while violating the underlying intent.

Examples:

### Example A — Schema-valid but semantically empty

Fixture contains every required field but the fields are generic or contradictory.

Expected result: structural validator passes; semantic validator rejects.

### Example B — Anti-centroid gaming

System avoids all controversial or concrete claims so the output contains no obvious centroid markers.

Expected result: structural anti-centroid test may pass, but taste/specificity test fails because the system escaped edge rather than preserving it.

### Example C — Interview completion without truth

System generates a polished interview brief despite having no authenticated response evidence.

Expected result: brief generation is blocked from downstream rendering.

### Example D — SFL density gaming

System increases symbolic compression and repetition metrics until a target score is reached while reducing clarity and human congruence.

Expected result: SFL metric does not authorize promotion; perceptual/evidence tests reject.

## 6. Test environment declaration

Every integration test suite MUST declare its environment fidelity.

If a test claims to validate:

- repository wiring → `E2_REPOSITORY_INTEGRATED` minimum;
- production configuration → `E3_PRODUCTION_SHAPED` minimum;
- human response or audience resonance → `E4_REAL_WORLD_OBSERVED` evidence required.

## 7. Taste fixtures

CAE SHOULD maintain curated taste fixtures containing:

- strong positive examples;
- generic near-neighbors;
- semantically valid but perceptually dead outputs;
- overly polished outputs;
- overexplained outputs;
- false-depth outputs;
- anti-centroid successes;
- anti-centroid failures.

Taste fixtures are not universal truth. They are contrastive evidence for specific architectural claims.

## 8. Reward-hack regression suite

Each core evaluator MUST have a regression family that asks:

```text
Can I maximize this score while making the actual output worse?
```

At minimum test:

- field padding;
- vocabulary avoidance;
- metric gaming through verbosity/shortness;
- false evidence references;
- state mislabeling;
- semantic direction substitution;
- evaluator-specific phrase gaming;
- repetition inflation;
- edge-label inflation;
- fake authenticity markers;
- fake SFL density.

## 9. Promotion rule

A feature with a high structural test pass rate but failed reward-hack or taste tests MUST remain `IMPLEMENTED_PENDING_VERIFICATION`.

A developer may not weaken a test solely because it is difficult for the current implementation to pass. The implementation, fixture, or claim must be revised deliberately.

## 10. Mandatory review questions

Before promoting a test suite, reviewers must ask:

1. What real claim does this test prove?
2. What easier false claim could it accidentally prove instead?
3. How could an optimizing agent game this test?
4. What mutation would expose that gaming?
5. Does the test preserve the project's intended edge?
6. Is the environment representative of the claim?
7. What evidence would upgrade this from simulated proof to observed proof?

## 11. Test ownership

Test ownership is split:

- implementation tests: code owner;
- semantic tests: semantic architecture owner;
- anti-centroid tests: CAE governance/Anti-Centroid Patrol;
- registry integrity tests: registry owner;
- reality-contact/evidence tests: evidence/governance owner;
- outcome measurement: product/runtime owner.

No single implementation agent should be the sole authority over a proxy evaluator it can optimize against.
