# CAE-M05 — Evidence Segmentation Mandate

**Status:** `GOVERNED EXECUTION MANDATE — OPERATOR AUTHORIZATION REQUIRED`  
**Prepared:** 2026-08-28  
**Program:** CAE Editorial Intelligence Mandate Bundle

## 1. Decision / Objective

**Objective:** Transform authenticated interview transcripts into semantically coherent EvidenceSegment objects without prematurely captioning the entire transcript.

This mandate is intentionally narrow. It exists to establish one executable boundary in the CAE editorial-intelligence chain without authorizing unrelated architecture work.

## 2. Governing doctrine and authority

The agent SHALL treat the following as governing inputs for this phase:

- `M04`\n- `authenticated interview transcript path`\n- `CAE evidence/source bridge`\n- `OLD CMF interview intelligence`\n- `Story Arc heritage`\n- `semantic segmentation conventions.`\n

Authority is separated into three axes:

- **Definition authority:** the artifact/version that defines what the object means.
- **Runtime authority:** the verified representation used by typed operations.
- **Change/promotion authority:** the person/process authorized to alter or promote the definition or implementation.

These axes SHALL NOT be inferred from convenience.

## 3. Mandatory reading before action

Before planning or editing, the execution agent SHALL read the full mandate and every source listed in Section 2 that is actually present in the repository or supplied execution bundle. Missing sources become a documented `EVIDENCE_ERROR` or `DEPENDENCY_BLOCK`, not an invitation to invent content.

The agent SHALL inspect current executable brownfield reality wherever this mandate claims an existing service, table, registry, parser, pipeline, or API. A document describing an implementation is not proof that the implementation exists.

## 4. Exact scope

Build segmentation logic and schema for semantic boundaries, timing, speaker, thought completion, emotional shifts, rhetorical beats, story/mechanism boundaries, and context dependencies. Preserve transcript lineage and exact media time ranges.

The intended deliverables are bounded to this mandate's object boundary and any existing service integration explicitly required by those deliverables. Adjacent improvements may be recorded as `DEFERRED`, `BLOCKED`, or `NEXT_PHASE`, but SHALL NOT be implemented inside this mandate.

## 5. Explicit prohibitions

No deep annotation of every word, no candidate scoring in the segmentation step, no rewriting the Guest’s language, no lossy chunking based only on fixed token counts.

The agent SHALL NOT widen the scope because a nearby inconsistency is discovered. A collision must be recorded and routed to the correct authority rather than silently resolved for convenience.

## 6. Required artifacts and semantic obligations

Segments must remain evidence-bearing excerpts. Later stages may select them for annotation. A segment can be reused as evidence without being treated as a publishable asset.

The artifact SHALL preserve stable identifiers, provenance, version references, and lineage to upstream evidence. Where an inherited registry already supplies an identifier, that identifier SHALL be reused rather than recreated.

## 7. Execution behavior

The agent SHALL operate through the CAE governed sequence:

```text
READ AUTHORITY
→ VERIFY PRECONDITIONS
→ PLAN
→ EXECUTE WITHIN SCOPE
→ VALIDATE
→ RECORD EVIDENCE
→ UPDATE CONTROL STATE
→ COMMIT
→ OPERATOR GATE
→ STOP
```

For stateful operations, the normal path SHALL use typed semantic operations and SHALL emit the appropriate receipt. Direct ad-hoc state writes are prohibited unless this mandate explicitly delegates them as a controlled migration or repair action.

## 8. Verification, fidelity, and reward-hacking resistance

False-proof case: fixed 30-second chunks pass structural tests but cut a story mid-thought. Test semantic-boundary failure. Another test must prove transcript bytes/timecodes remain verifiable.

### Evidence requirements

Every material claim SHALL identify the evidence class used to support it. Recommended classes are `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, and `OPERATOR_DECISION_REQUIRED`.

A green test is only proof of what the test actually measures. It is not proof of the wider architectural property unless the environment, data, and verifier faithfully represent that property.

### Taste / anti-centroid requirement

Where the mandate produces content candidates, editorial structures, annotations, or perceptual decisions, automated structural correctness SHALL be supplemented by project-specific contrastive examples. A candidate can pass a schema and score while still being generic, contextually wrong, narratively incomplete, or aesthetically dead. Such a result is not a successful CAE outcome.

## 9. Error taxonomy

At minimum, failures SHALL be classifiable as applicable:

- `AUTHORITY_ERROR`
- `SCOPE_ERROR`
- `TAXONOMY_ERROR`
- `SCHEMA_ERROR`
- `RELATION_ERROR`
- `STATE_ERROR`
- `EVIDENCE_ERROR`
- `PROVENANCE_ERROR`
- `SEMANTIC_DRIFT`
- `EDITORIAL_DRIFT`
- `FORMAT_DRIFT`
- `COMPOSITION_ERROR`
- `RUNTIME_ERROR`
- `REWARD_HACK`
- `ENVIRONMENT_FIDELITY_ERROR`

A structured error SHOULD identify the violated contract, affected object, evidence that exposed the failure, and allowed repair route. “Try again” is not a sufficient failure description.

## 10A. Contract, lineage, and inspection requirements

This mandate is an architectural execution boundary, so the agent must leave behind artifacts that another agent can inspect without reopening the entire terminal history. The output must identify the exact upstream inputs used, their versions or hashes where available, and the exact transformation performed in this phase. A later agent must be able to determine whether the result was derived from real project evidence or from model interpretation alone.

Where the phase creates or changes a typed object, record its canonical identity, artifact class, ontological plane, scope class, owner, authority axes, lifecycle, and direct upstream lineage. Where it creates a relation, identify both endpoints, direction, cardinality where relevant, temporal scope, and evidence needed to assert that relation. Where it creates state, identify the source state, operation, target state, preconditions, postconditions, validator, receipt, and recovery route. Where it creates an execution artifact, identify the source contract/version and the downstream consumer that is authorized to interpret it.

The agent SHALL keep three records separate:

```text
FACT
  verified from repository, runtime, schema, registry, test, or operator record

HYPOTHESIS
  useful interpretation not yet independently proven

DECISION REQUIRED
  architectural or product authority that only the Operator may ratify
```

A phase may produce hypotheses and proposals, but it may not disguise them as canonical definitions, runtime authority, or proof. If the phase encounters conflicting existing implementations, the conflict must be preserved with both sides represented. Do not normalize away a discrepancy merely to make validation green.

For every material automated test, capture the command, environment identity, fixture or data source, result, and limitation. For any evaluator that outputs a score, record the evaluator version and whether the score is advisory, gating, or descriptive. A score is never a substitute for evidence. For editorial phases, the agent must preserve at least one representative positive case and one project-specific hard negative so later regression tests can distinguish real quality from structural compliance.

If a required dependency is unavailable, the phase ends in `BLOCKED` with an explicit dependency record rather than fabricating a substitute. If an implementation choice would alter a higher-order constitutional rule, stop and route that decision to the Operator.

## 10B. Safe parallel work

Parallel read-only investigation is permitted when it cannot establish competing authority. Any parallel findings must be merged into the single phase record before the agent makes a decision. Shared canonical registries, PostgreSQL state, RLS, Storage, migrations, and runtime contracts have one write owner. Parallel agents must not independently “fix” the same object, relation, or control-state record.

## 10. Completion condition

This mandate is complete only when:

1. the scoped artifacts exist;
2. the required validation passes;
3. evidence and limitations are recorded;
4. the CAE control state is updated;
5. the exact git commit is recorded; and
6. the operator gate is explicitly requested.

The existence of code or documentation alone does not constitute completion.

## 11. Rollback / recovery

Documentation and canonical artifacts are versioned and superseded rather than silently rewritten. Runtime changes, where authorized, MUST retain receipts and rollback/recovery instructions. External side effects are non-transactional unless the implementation can prove otherwise; cleanup must be independently verified.

## 12. Operator gate

**Operator decision:** Approve M05 and authorize M06.

Until that decision is recorded, the next mandate is unauthorized.

## 13. Gemini activation prompt

```text
Execute CAE-M05 — Evidence Segmentation. Read every required reference before editing. Build a transcript-to-EvidenceSegment layer that preserves source identity, speaker, exact start/end times, transcript text, semantic boundary, context dependency, and evidence provenance. Do not caption or deeply annotate the full transcript. The next stage will select high-value segments for semantic attribution; segmentation must therefore be lossless enough to permit later reconstruction and auditable enough to locate the original media. Use semantic boundaries—thought completion, story turns, mechanism transitions, contradiction, reveal, emotional movement—not fixed-size chunks as the primary criterion. Preserve exact source hashes or equivalent provenance where the existing evidence bridge supports them. Test false proofs including technically valid fixed windows that cut a sentence or narrative beat, duplicated transcript fragments, shifted timecodes, and altered transcript text. A segmenting run is not successful merely because it produced the expected count. Record actual environment, verifier limitations, and receipts. Update control state, commit only permitted changes, request M05 approval and M06 authorization, then stop. Preserve the distinction between facts, hypotheses, and decisions throughout the work. Any inherited artifact that disagrees with the target architecture must be documented as a collision with evidence rather than silently rewritten. For every test, record what property it genuinely proves and what remains outside its proof boundary. For content-facing work, include a concrete anti-centroid or false-proof case so a structurally green result cannot be mistaken for taste, authenticity, novelty, or narrative completeness. Do not weaken a validator to make a failing implementation pass. Do not begin the next mandate, even if its work appears obvious.
```
