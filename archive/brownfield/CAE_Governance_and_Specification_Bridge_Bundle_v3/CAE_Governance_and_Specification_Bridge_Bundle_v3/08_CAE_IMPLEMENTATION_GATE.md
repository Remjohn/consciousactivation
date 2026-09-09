# CAE Implementation Gate v2.0

A CAE implementation task may begin only when ALL applicable gates pass.

## Gate A — Architecture

- [ ] Relevant phase validation status is `BROWNFIELD VALIDATED` or better.
- [ ] Object role is resolved.
- [ ] Artifact class is resolved.
- [ ] Ontological plane is resolved.
- [ ] Nearest neighbors and semantic boundary are documented.

## Gate B — Evidence

- [ ] Stable claims are traceable to authoritative evidence.
- [ ] Immutable evidence is identified.
- [ ] Hypotheses are explicitly marked as such.
- [ ] Inherited registry lineage is preserved.

## Gate C — Data model

- [ ] Canonical schema exists.
- [ ] Relations are typed.
- [ ] State machine is defined where applicable.
- [ ] Event model is defined where applicable.
- [ ] Storage representation is explicit.

## Gate D — Runtime program

- [ ] Authorized operations are defined.
- [ ] Query/view/function access is defined where applicable.
- [ ] Agent execution plan exists.
- [ ] Output IR/packet is typed.
- [ ] Receipt lineage is defined.

## Gate E — Error and protection

- [ ] Error taxonomy exists.
- [ ] Validators exist or are explicitly scheduled.
- [ ] Anti-centroid requirements are preserved.
- [ ] Fatality behavior is defined.
- [ ] Repair/escalation path is defined.

## Gate F — Brownfield implementation

- [ ] Existing services/files/tables have been inspected.
- [ ] NEW/EXTEND/ADAPT/REPLACE decisions are explicit.
- [ ] Migration/rollback path exists where needed.
- [ ] No duplicate service has been introduced without architectural approval.

## Gate G — Verification

- [ ] Unit tests named.
- [ ] Integration tests named.
- [ ] Registry integrity tests named where applicable.
- [ ] Hard-negative/regression tests named where applicable.
- [ ] Environment fidelity level declared for each material claim.
- [ ] Reward-hacking / false-proof tests named for each material evaluator.
- [ ] Taste / anti-centroid regression tests named where applicable.
- [ ] Measurable acceptance criteria exist.

## Gate H — Reality Contact

- [ ] The test environment is sufficient for the claim being made.
- [ ] Structural test success is not being reported as semantic or human-quality proof.
- [ ] Known evaluator gaming strategies have been exercised.
- [ ] Contrastive taste fixtures exist for material meaning/perceptual claims.
- [ ] Runtime receipt captures the relevant input/output/environment snapshots.
- [ ] Human/world outcome claims identify an E4 evidence path.
- [ ] Any unresolved proof gap is explicitly marked rather than inferred away.

## Gate I — Anti-Centroid Patrol

- [ ] Validator changes were regression-tested against anti-centroid fixtures.
- [ ] No repair step introduces generic corporate smoothing to achieve a pass.
- [ ] Matrix of Edging constraints remain intact.
- [ ] Legitimate sharpness is not rejected merely because it is uncomfortable or uncommon.


## Final status

```text
BLOCKED
READY_FOR_DEVELOPMENT
IMPLEMENTED_PENDING_VERIFICATION
VERIFIED
```

`READY_FOR_DEVELOPMENT` is the only status that authorizes coding from the spec.

`IMPLEMENTED_PENDING_VERIFICATION` MUST NOT be promoted to `VERIFIED` until Gates H and I pass for all applicable claims.


## State-control gate added in v3.0

A stateful implementation cannot reach `READY_FOR_DEVELOPMENT` until the spec identifies:

- authoritative PostgreSQL/Supabase state source;
- current-state projection;
- state history/event model;
- legal transitions;
- authorized semantic operations;
- validation/evidence contract;
- receipt contract;
- recovery path;
- reward-hack countertest;
- environment-fidelity target.

If StateM is cited, the implementation gate must also state whether it is: `REFERENCE_ONLY`, `ADAPTED_CONCEPT`, `SELECTIVE_CODE_REUSE`, or `DIRECT_DEPENDENCY`.
