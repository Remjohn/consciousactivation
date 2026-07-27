# TS-06: Canonical Harness IR And Artifact Compilation

Status: `SPEC_RATIFIED_PENDING_STORY_MAPPING`

## Traceability

- Owned: FR-051 through FR-059; NFR-REL-001, NFR-REL-003, NFR-TRACE-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-MAINT-001.
- Decisions: D003, D007, D011, D021, D027, D028, D029, D033.

## Responsibility And Authority

Own the canonical Harness IR aggregate, value provenance, schema/version migration, deterministic serialization, artifact compilers, manifests, drift protection, hashes, and cross-artifact validation. It does not own Workflow IR, source acquisition, human decisions, or target runtime behavior.

Deterministic code exclusively owns serialization, migration, compilation, hashing, and consistency checks. Agents may propose typed patches but cannot write IR or generated authoritative artifacts directly. Humans ratify patches where field authority requires it.

## Modules And Components

`domain/harness_ir/{root,values,identity,versions}.py`, `application/ir_commands.py`, `compilers/{markdown,openspec,machine,target}.py`, `compilers/manifest.py`, `compilers/drift.py`, `schemas/generation.py`, and `migrations/harness_ir/`.

## Canonical Data Structures

`HarnessIR { ir_id, schema_version, revision, run_id, target_profile_ref, source_lock_ref, boundary, constitution, evidence_refs, decisions, category, capabilities, modules, phase_graph, context_graph, contract_graph, reference_graph, loading_graph, skills, recipes, evaluation_plan, repair_graph, authorization, extensions }`

Every material leaf uses `GovernedValue<T> { value, knowledge_status, authority, evidence_refs, decision_ref?, confidence?, created_by, created_at }`.

`ArtifactManifest { manifest_id, ir_hash, compiler_id, compiler_version, target_profile_ref, source_lock_hash, workflow_profile_hash, artifacts[], generated_at, nondeterminism_exceptions[] }`

`ArtifactEntry { logical_id, media_type, schema_ref?, sha256, size, authority, derived_from_paths }`

Unknown fields are rejected in authoritative sections and allowed only under versioned extension namespaces. Canonical JSON uses deterministic key order, number/string normalization, UTF-8, and no timestamps inside identity hashes.

## APIs, Commands, Events, Persistence

- Commands: `CreateHarnessIR`, `ApplyTypedPatch`, `MigrateHarnessIR`, `CompileArtifactSet`, `ValidateArtifactSet`, `AcceptNondeterminismException`.
- Queries: revision/history, path provenance, dependency impact, artifact manifest, drift report.
- Events: `HarnessIRCreated`, `HarnessIRPatched`, `HarnessIRMigrated`, `ArtifactSetCompiled`, `ArtifactDriftDetected`, `ArtifactSetValidated`.
- Persistence: event stream plus immutable IR snapshots; generated artifacts in CAS; relational projection for path/provenance queries.
- Public compiler interface: `compile(ir_snapshot, target_profile, compiler_config) -> ArtifactManifest`.

## Dependency, Invalidation, Idempotency, Resume

Each compiler declares consumed IR paths and emitted artifacts. A patch computes affected paths and invalidates only manifests whose dependency selectors intersect. Compilation key is `(ir_hash, compiler_id/version, target_profile_hash, config_hash)`. Repeating it returns byte-identical artifacts or a declared, approved nondeterminism exception. Partial outputs remain quarantined until one manifest transaction commits.

## Security And Isolation

Compilers receive immutable IR snapshots and an empty output directory. They have no network, secret, source-write, or unrelated repository access. Generated output is scanned for secrets and undeclared external references. Manual edits never update canonical IR.

## Observability, Cost, And Performance

Record IR size/revision, patch paths, migration duration, compiler cache hits, artifact count/bytes, byte reproducibility, drift incidents, and validation failures. Release 1 compilation target is p95 under 30 seconds excluding model/evaluation stages; larger limits require an explicit budget receipt.

## Failures And Recovery

Schema-invalid patches fail before events. Failed migration preserves the prior revision. Compiler crashes leave no authoritative manifest. Drift quarantines the affected artifact and offers regeneration or a governed IR patch; importing manual edits is prohibited unless parsed through a typed proposal and ratification path.

## Acceptance Tests

1. Same inputs compile byte-identical artifacts and manifest hashes.
2. Every material output value traces to IR paths and evidence/decision authority.
3. A manual generated-file edit triggers drift and never mutates IR.
4. Invalid migrations are atomic and reversible.
5. Changing one IR section invalidates only declared dependent artifacts.
6. Markdown, OpenSpec, JSON Schema, and machine packages agree on shared values.
7. Compiler sandboxes cannot access network, secrets, or source writes.
8. An artifact cannot claim evaluated identity if its hash differs from the evaluation receipt.

## Implementation Tasks

1. Define root IR, governed-value, identity, manifest, and patch schemas.
2. Implement canonical serializer and hash contract with golden vectors.
3. Implement event/snapshot repository and optimistic patches.
4. Implement compiler registry, dependency selectors, staging, and atomic manifest commit.
5. Implement schema migration registry and rollback tests.
6. Add Markdown/OpenSpec/machine compiler contract tests and drift guard.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Compile rich Activative lineage, conversational receipts, and downstream visual handoffs | harness_ir_and_compiler_owner | Canonical IR owns references and compiled artifacts; downstream products own execution | `SharedActivativeCore`, `ActivativeCall`, `ReactionReceipt`, `ExpressionMoment`, visual-semantic handoff schemas | Compilation fails on missing versions, semantic mutation, or out-of-order chain | canonical serialization, schema round-trip, and non-mutation fixtures | Deterministic output preserves exact source hashes through conversation or visual handoff | Schema-version bump is additive; explicit upgrader required for V1.1 IR lacking new refs |

## Non-Goals And Migration

No V2.1 schema migration is implemented. Future schema migration within Builder Next is required; external target execution is not.
