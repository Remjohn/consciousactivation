# Acceptance Criteria

## AC-01 - Validate the exact active definition

Given the PASS ST-07.02 receipt and exact active `AtomicHarnessDefinition`, when validation runs, then one immutable PASS validation report and receipt are committed against that definition.

## AC-02 - Prove target artifact completeness

Given the Atomic Content Harness target policy, when the definition is inspected, then every required section, lineage reference, capability, module, phase, context manifest, skill decision, input/output contract and acceptance declaration is present and attributable.

## AC-03 - Apply target-specific gates

Given the governed synthetic validation policy, when gates are evaluated, then artifact completeness, authority, lineage, determinism, portability, internal compatibility, target separation and non-certification each receive one explicit deterministic verdict.

## AC-04 - Prevent universal-profile flattening

Given the Atomic Content Harness-only branch, when validation resolves target semantics, then content target fields remain explicit and VAE or Delegation target fields, generic notes substitution and external runtime assumptions are rejected.

## AC-05 - Preserve conditional compatibility scope

Given BF-AM-008, when compatibility is reported, then internal Atomic Content Harness compatibility is PASS and external target compatibility is exactly `NOT_EVALUATED_EXTERNAL_TARGET_BRANCH`, never inherited or silently promoted.

## AC-06 - Enforce synthetic non-certification

Given the repository-owned synthetic proof, when gates are evaluated, then production eligibility and certification remain false and `synthetic_not_certifiable` remains mandatory.

## AC-07 - Preserve complete authority and lineage

Given the compiled definition and its governed parents, when the report is serialized, then the exact definition hash, run, Constitution, ratification, IR, artifacts, modules, phases, context and skill lineage remains reproducible.

## AC-08 - Fail closed without partial state

Given missing, altered, stale, invalidated, wrong-target, flattened, externally broadened, unauthorized or hash-invalid input, when validation is attempted, then a typed rejection occurs and no partial report, receipt, event, observation, command record or run reference is committed.

## AC-09 - Be deterministic and portable

Given identical governed inputs in fresh contexts, when validated, then report bytes, hashes, identity, ordering and receipt are identical and contain no machine-local state.

## AC-10 - Preserve replay and idempotency

Given a completed validation command, when repeated or restored through checkpoint replay, then the original receipt and state identity are returned without duplication; conflicting payload reuse fails closed.

## AC-11 - Propagate invalidation non-destructively

Given upstream invalidation, when cascade rules run, then the active validation becomes unusable through a descendant invalidation while historical bytes and receipts remain reproducible.

## AC-12 - Respect product and Story boundaries

Given the final change set, when architecture and scope tests run, then only allowlisted files changed and no Format 02, external target compiler/runtime, VAE, Delegation, workflow execution, ST-11.01 capsule generation, production certification or later-Story behavior exists.
