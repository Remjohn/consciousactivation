# TS-02: Configured Evidence Workspace

Status: `IMPLEMENTATION_SPEC_COMPLETE_PENDING_BD-004`

## Traceability

- Owned: FR-009 through FR-018; NFR-TRACE-004, NFR-SEC-001, NFR-SEC-002, NFR-PORT-001, NFR-SCALE-001.
- Decisions: D003, D005, D006, D007, D023, D025, D027, D028.

## Responsibility And Authority

Own target-specific source profiles, readiness diagnostics, immutable source locks, specimen/evidence identity, gap/conflict records, and saturation mechanics. It does not infer visual meaning or authorize atomicity. Deterministic code owns acquisition, hashing, normalization metadata, indexing, and policy checks. Agents may propose semantic tags with provenance. Humans resolve authority conflicts and source waivers.

## Modules And Components

`evidence/profiles.py`, `evidence/adapters/{filesystem,archive,media}.py`, `evidence/index.py`, `evidence/saturation.py`, `evidence/conflicts.py`, `application/evidence_commands.py`, and `adapters/artifact_store.py`.

## Canonical Data Structures

- `SourceProfile { profile_id, target_kind, required_roles, allowed_media, discovery_rules, safety_limits, saturation_contract_ref }`
- `SourceDescriptor { source_id, uri, role, authority, license, privacy_class, media_type, size, sha256, discovered_from }`
- `SourceLock { lock_id, profile_ref, target_candidate_ref, ordered_source_hashes, created_at, created_by, aggregate_hash }`
- `Specimen { specimen_id, source_id, media_identity, dimensions, duration, page_or_frame_count, duplicate_cluster?, status }`
- `EvidenceClaim { claim_id, knowledge_status, subject_ref, value, source_spans, confidence, authority }`
- `EvidenceGap { gap_id, required_role, severity, affected_requirements, resolution }`
- `SaturationContract { required_roles, minimum_diversity, contradiction_policy, visual_coverage, stopping_rules }`

Source bytes never enter mutable database columns; they are read-only inputs or immutable content-addressed artifacts.

## APIs, Commands, Events, Persistence

- Commands: `DiagnoseSources`, `RegisterSource`, `BuildSourceLock`, `IndexEvidence`, `ResolveAuthorityConflict`, `EvaluateSaturation`.
- Queries: source readiness, source graph, specimen inventory, claim lookup, gaps/conflicts, saturation result.
- Events: `SourceDiagnosed`, `SourceRegistered`, `SourceRejected`, `SourceLockCreated`, `SpecimenIndexed`, `EvidenceIndexed`, `AuthorityConflictRaised`, `SaturationEvaluated`.
- Persistence: immutable descriptors/locks in relational state; extracted metadata and indexes versioned by lock; media/artifacts in CAS.
- Idempotency key: `(source_uri, observed_size, observed_mtime, sha256, adapter_version)`; final identity is SHA-256, never path alone.

## Dependency, Invalidation, And Resume

Any changed source hash creates a new lock and invalidates visual parse, saturation, atomicity, Genesis, evaluations, and generated artifacts that depend on it. Unchanged specimens reuse cached normalization by content hash and parser version. Partial indexing resumes from per-source checkpoints.

## Security And Isolation

Reject archive traversal, absolute members, symlink escape, recursive archive depth above two, decompression ratio above 100:1, aggregate extraction above configured budget, unsupported media, and mutable network sources without a captured copy. Evidence mounts are read-only. Secrets, protected labels, and unrelated repositories are excluded by profile.

## Observability, Cost, And Performance

Report bytes/files/specimens processed, cache hit rate, adapter failures, duplicate ratio, unresolved conflicts, coverage by required role, elapsed time, and estimated model work. Scale acceptance is empirical: test 100,000 descriptors and representative large media without unbounded memory.

## Failures And Recovery

Unsafe sources are quarantined with typed reasons. Hash mismatch aborts lock creation. Adapter failure preserves completed checkpoints and retries only within profile bounds. A critical authority conflict produces `SATURATION_BLOCKED`; it cannot be downgraded by an agent.

## Acceptance Tests

1. Directory and archive ingestion never mutates originals.
2. Traversal, symlink escape, recursive bombs, and budget overflow are rejected.
3. Identical bytes at different paths share content identity but preserve provenance.
4. A changed byte produces a new source lock and exact downstream invalidation.
5. Every target specimen has stable identity and status.
6. Missing required roles and contradictory authorities block saturation.
7. Resume skips verified sources and reprocesses stale adapter versions.
8. Format 02 profile rejects sources lacking authority/license metadata.

## Implementation Tasks

1. Define source, lock, specimen, claim, gap, conflict, and saturation schemas.
2. Implement safe filesystem/archive/media adapters and CAS port.
3. Implement deterministic index and query API.
4. Implement target-profile diagnostics and saturation evaluator.
5. Add security, property, scale, resume, and invalidation tests.
6. Bind the Format 02 corpus after BD-004.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Govern conversational reaction evidence | evidence_workspace_owner | Originating content harness captures truth; Builder registers immutable references and applies policy | `ReactionReceipt`, `ExpressionMoment`, `ConsentPolicyRef`, evidence span and withdrawal state | Quarantine missing consent/provenance; withdrawal invalidates dependent moments and proposals | consent, redaction, timecode, revocation, and recompile fixtures | Every conversational span is source-addressable, policy-bound, and revocable | New V1.2 source-profile fields; production use stays blocked by HD-006 and expanded BD-004 |

## Non-Goals And Migration

No multimodal inference, semantic category decision, external editor ingestion runtime, or V2.1 importer is included.
