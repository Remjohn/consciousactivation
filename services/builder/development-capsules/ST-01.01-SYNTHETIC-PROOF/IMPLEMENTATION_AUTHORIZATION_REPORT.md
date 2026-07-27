# ST-01.01-SYNTHETIC-PROOF Bounded Implementation Authorization Report

Gate verdict: **PASS**  
Bounded implementation readiness: **PASS**  
Implementation authorized now: **No**

The branch is independently implementable in one focused Codex context. Its only completed Story dependency is the valid PASS receipt for `ST-01.01`; the amendment confirmation and limited BD-010 policy are governed and hash-pinned. It needs no later Story, Format 02 evidence, VAE or Delegation runtime, GPU, evaluator, provider, visual baseline, conversational policy, or production certification.

Exact implementation scope:

- Modify `src/cmf_builder/domain/target_profile.py` only to add the immutable authorized-profile expression needed by the fixture while retaining Format 02 behavior.
- Modify `src/cmf_builder/adapters/__init__.py` only to export the new adapter.
- Create `src/cmf_builder/adapters/synthetic_proof_target_profile_repository.py` to load and verify only the pinned synthetic fixture.
- Create the six test files listed in `ALLOWED_FILE_SCOPE.yaml`.
- On completion, create only the five listed evidence files under `development-capsules/ST-01.01-SYNTHETIC-PROOF/completion/`.

No schema, canonical registry, authority, planning, ADR, technical specification, contract, original capsule, Format 02 reference artifact, or external repository may be changed. Any need outside this allowlist closes the gate and requires new human authority.

The gate remains `AWAITING_HUMAN_AUTHORIZATION`. To authorize only this supplemental branch, the human must state exactly:

`AUTHORIZE BUILDER ST-01.01-SYNTHETIC-PROOF BOUNDED IMPLEMENTATION`

That phrase does not authorize `ST-01.02`, the remaining Builder Core track, Release 1, the full product, or production deployment.
