# CAE Reality-Contact Evaluation Protocol v2.0

**Status:** Mandatory governance protocol  
**Scope:** Phase validation, FRs, Tech Specs, implementation tests, runtime receipts, promotion, and learning

## 1. Purpose

A passing automated test is evidence only for the proposition that the test actually measures. In CAE, structural validity can coexist with semantic drift, reward hacking, environment mismatch, and centroid collapse. Therefore CAE adopts a separate Reality-Contact Evaluation layer.

The governing distinction is:

```text
TEST PASS ≠ PROOF OF QUALITY
TEST PASS = EVIDENCE FOR A DEFINED PROPOSITION
```

A CAE implementation is not considered verified merely because unit tests are green. Meaningful verification requires evidence that the implementation:

1. behaves correctly;
2. behaves correctly in a sufficiently faithful environment;
3. cannot easily obtain a high score by gaming the evaluator;
4. preserves the intended semantic/taste properties;
5. produces traceable runtime evidence;
6. survives real-world observation when the claim concerns real-world behavior.

## 2. Three mandatory evaluation gates

Every material CAE capability MUST distinguish three gates.

### Gate A — Environment Fidelity

**Question:** Did we test the capability under conditions sufficiently representative of the environment in which the claim is made?

### Gate B — Reward-Hacking Resistance

**Question:** Can the implementation score well by optimizing the test proxy while violating the underlying intent?

### Gate C — Taste / Reality Contact Integrity

**Question:** Does the artifact preserve the human quality the architecture was explicitly designed to preserve, rather than merely satisfying formal checks?

A gate may be marked `PASS`, `FAIL`, `NOT_APPLICABLE`, or `UNVERIFIED`. `UNVERIFIED` is not equivalent to `PASS`.

## 3. Environment Fidelity Scale

Use the following minimum levels:

| Level | Environment | Meaning |
|---|---|---|
| `E0_SYNTHETIC` | pure unit fixtures/mocks | proves local mechanics only |
| `E1_REALISTIC_FIXTURE` | high-fidelity representative fixtures | proves behavior against realistic shapes |
| `E2_REPOSITORY_INTEGRATED` | real services, schemas, registries, routes | proves integration behavior inside the actual repository |
| `E3_PRODUCTION_SHAPED` | production configuration/data-shape without relying on live external outcomes | proves deployment-shaped behavior |
| `E4_REAL_WORLD_OBSERVED` | live human/environment outcome | proves observed field behavior |

Every acceptance claim MUST declare a minimum required fidelity level.

Rules:

- `E0` MUST NOT prove architecture-level runtime claims.
- `E1` MUST NOT prove inherited-registry compatibility unless the real registry shape is present.
- `E2` MUST be required for claims about actual CAE orchestration over repository services, schemas, registries, or receipts.
- `E3` SHOULD be required before production deployment of material runtime paths.
- `E4` is required for claims about human response, audience resonance, taste, engagement, or real-world effectiveness.

## 4. Reward-Hacking Model

A reward-hacking condition exists when the evaluator's measurable target can be satisfied without satisfying the underlying design intent.

Common CAE examples:

- a validator rewards the presence of required fields while the content is generic;
- an anti-centroid score is improved by avoiding all distinctive claims;
- a test passes because forbidden phrases were removed while the underlying corporate-smoothing structure remains;
- a schema passes because values are syntactically valid but semantically meaningless;
- an SFL evaluator rewards density while the result becomes over-compressed and unreadable;
- an interview pipeline passes because it produces a transcript even though the guest never supplied authenticated evidence;
- an Edge validator passes because the edge label exists while the underlying tension is weak or unsupported.

Every material evaluator MUST therefore include at least one adversarial `GOOD_PROXY / BAD_INTENT` test.

## 5. Taste Integrity

Taste Integrity is not a generic “looks good” score.

It is the evaluation of whether the implementation preserves architecture-specific qualities such as:

- specificity;
- recognizability;
- semantic tension;
- authenticated human evidence;
- appropriate asymmetry;
- anti-centroid behavior;
- Matrix of Edging pressure;
- SDA directional integrity;
- SFL perceptual aliveness;
- archetypal fit;
- non-overexplained expression;
- preservation of the intended human editing decision.

Taste Integrity MUST be decomposed into observable propositions wherever practical.

A single scalar `taste_score` MUST NOT be the sole gate for promotion.

Instead use a profile such as:

```yaml
taste_integrity:
  edge_preservation: pass
  recognition_density: pass
  specificity: pass
  human_congruence: pass
  semantic_direction: pass
  anti_centroid: pass
  overexplanation_risk: pass
  archetype_fit: pass
  sfl_aliveness: pass
```

## 6. Anti-Centroid / RLHF-Style Drift Patrol

CAE MUST maintain an explicit evaluation role for detecting genericizing pressure.

This role is called the **Anti-Centroid Patrol**. It is a governance function, not a content author.

Its job is to identify whether validation, prompts, schemas, examples, or repair logic are progressively pushing the system toward:

- polite averaging;
- safety-shaped neutrality;
- corporate smoothing;
- hedge inflation;
- flattening of conflict;
- excessive explanation;
- loss of concrete human language;
- replacement of edge with generic approval-seeking prose.

The patrol MUST be invoked:

- during phase validation;
- during Tech Spec review;
- after material evaluator changes;
- after changes to validators or reward functions;
- after repeated repair cycles;
- during regression testing of high-value content pathways.

A finding is not a style disagreement. It is a governance finding when a new constraint reduces the architecture's ability to preserve explicitly ratified edge or signal density.

## 7. Evaluation Evidence Object

Every material evaluation should emit an evidence record containing at least:

```yaml
evaluation_id:
claim_id:
subject_id:
evaluator_id:
environment_fidelity:
required_fidelity:
structural_result:
semantic_result:
taste_result:
reward_hacking_result:
anti_centroid_result:
evidence_refs: []
input_snapshot_hash:
registry_snapshot_hash:
output_snapshot_hash:
test_code_ref:
observed_at:
evidence_status:
limitations: []
```

This record is evidence of evaluation, not a claim that the subject is universally correct.

## 8. Promotion Rules

A material capability may be marked `VERIFIED` only when:

```text
Structural Pass
AND
Required Environment Fidelity Pass
AND
Reward-Hacking Resistance Pass
AND
Taste/Reality-Contact Pass
AND
Traceable Evidence
```

If any required gate is `UNVERIFIED`, the overall result is `IMPLEMENTED_PENDING_VERIFICATION`.

If any required gate is `FAIL`, the implementation cannot be promoted.

## 9. Regression and Mutation Testing

Material evaluators MUST include contrastive and mutation tests where appropriate.

Minimum mutation families include:

- remove evidence;
- replace human-specific language with generic language;
- flatten tension;
- increase corporate smoothing;
- alter semantic direction while preserving syntax;
- alter state while preserving entity identity;
- substitute an adjacent but invalid primitive;
- remove required lineage;
- replay the same output under a different environment;
- optimize only the measurable metric while intentionally violating taste or intent.

The expected behavior must be explicit for each mutation.

## 10. Test-to-Claim Rule

Every test MUST name the claim it is intended to prove.

A test description such as `test_content_generation_success` is insufficient.

Prefer:

```text
test_guest_evidence_gate_rejects_render_without_authenticated_response
```

and:

```text
Claim:
No downstream artifact is authorized before authenticated human evidence exists.
```

The test is then evaluated for environment fidelity and reward-hacking resistance separately.

## 11. Reality-Contact Ladder

CAE uses the following evidence ladder for important claims:

```text
E0 structural assertion
↓
E1 realistic behavior
↓
E2 repository-integrated behavior
↓
E3 production-shaped behavior
↓
E4 observed human/world outcome
```

No lower level may silently be reported as a higher level.

## 12. Fatal Conditions

A verification attempt MUST be blocked or quarantined when:

- a test passes only because the evaluator is weaker than the claim;
- a metric is clearly gameable and no adversarial test exists;
- taste is inferred from structural validity alone;
- a synthetic fixture is presented as real-world proof;
- an anti-centroid failure is repaired by adding generic smoothing;
- a validator rewards avoidance rather than successful realization;
- a runtime receipt cannot identify the environment or input snapshot;
- evidence lineage is missing for an outcome claim.

## 13. Relationship to Existing CAE Governance

This protocol extends, rather than replaces:

- `CAE_PHASE_VALIDATION_PROTOCOL`;
- `CAE_TECH_SPEC_WRITING_PROTOCOL`;
- `CAE_SPEC_ACCEPTANCE_AND_EVIDENCE_MATRIX`;
- `CAE_IMPLEMENTATION_GATE`;
- RSCS;
- CBAR;
- SDA;
- SFL;
- Matrix of Edging;
- inherited registry migration rules.

Its governing law is:

> **Reality contact outranks proxy satisfaction.**

A green test is valuable. It is never permission to stop thinking.
