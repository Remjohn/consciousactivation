---
title: "CMF STUDIO Tech Specs MCDA Evaluation"
evaluated_artifact: "docs/tech-specs"
source_of_truth:
  - "docs/stories"
  - "docs/epics.md"
  - "THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md"
  - "docs/architecture.md"
supporting_artifacts:
  - "THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md"
  - "docs/cmf-studio-pipeline-map.md"
  - "docs/migration/legacy-inventory.md"
  - "docs/evals/05-story-files-mcda-eval.md"
evaluation_date: "2026-06-21"
criteria_count: 12
tech_spec_count: 61
pre_repair_weighted_score_10: 9.20
pre_repair_weighted_score_100: 92.0
post_repair_weighted_score_10: 9.38
post_repair_weighted_score_100: 93.8
status: "tech-specs-ready-after-repair"
---

# CMF STUDIO Tech Specs MCDA Evaluation

## Evaluation Standard

This MCDA evaluates the complete CMF STUDIO tech-spec corpus in `docs/tech-specs` as implementation-facing handoff material. The corpus must preserve the repaired PRD, architecture, pipeline map, story files, Legacy Inventory doctrine, Python/Pydantic/DSPy/Pi implementation authority, CBAR pressure, and full-system scope discipline.

The legacy ERA3 five-lens audit was adapted to CMF's greenfield standard: FR coverage, Pydantic object integrity, boundary precision, gate/CBAR completeness, and cross-spec consistency. DEP-ID language from older specs is treated as a legacy equivalent of CMF's current contract, command, receipt, and pipeline trace requirements.

## Scoring Summary

| Criterion | Weight | Pre-Repair Score | Weighted | Post-Repair Score | Weighted |
|---|---:|---:|---:|---:|---:|
| 1. Corpus completeness and index alignment | 8 | 9.6 | 76.8 | 9.6 | 76.8 |
| 2. Frontmatter and section schema completeness | 9 | 9.7 | 87.3 | 9.7 | 87.3 |
| 3. FR coverage and requirement trace integrity | 10 | 9.5 | 95.0 | 9.5 | 95.0 |
| 4. Pipeline trace, entry/exit object, validation contract, and receipt clarity | 10 | 9.6 | 96.0 | 9.6 | 96.0 |
| 5. Source-read discipline and required source anchors | 9 | 8.8 | 79.2 | 9.8 | 88.2 |
| 6. Legacy Inventory, JIT skill, and intentional orchestration fidelity | 9 | 8.7 | 78.3 | 9.5 | 85.5 |
| 7. Python/Pydantic/DSPy/Pi implementation specificity | 9 | 9.1 | 81.9 | 9.1 | 81.9 |
| 8. Commands, events, workflows, and receipts | 8 | 9.3 | 74.4 | 9.3 | 74.4 |
| 9. CBAR, RSCS, gates, and failure examples | 8 | 9.1 | 72.8 | 9.1 | 72.8 |
| 10. Cross-spec dependency and boundary consistency | 7 | 8.8 | 61.6 | 8.9 | 62.3 |
| 11. Provider, commercial, Neo4j, and no-drift guardrails | 6 | 9.4 | 56.4 | 9.4 | 56.4 |
| 12. Developer build readiness and verification detail | 7 | 8.6 | 60.2 | 8.8 | 61.6 |
| **Total** | **100** |  | **919.9** |  | **938.2** |

**Pre-repair verdict:** implementation-handoff ready with minor auditability defects. The corpus covered all 61 stories and retained the pipeline, CBAR, Python-first, and no-drift rules, but the first 22 specs used an older heading name for legacy mapping, two specs did not explicitly cite the Product Brief, and one Ideogram lineage spec did not explicitly cite the Legacy Inventory.

**Post-repair verdict:** tech-specs-ready-after-repair. The corpus now has consistent source anchors and a uniform `Legacy Intelligence Mapping` subsection across all 61 specs.

## Criterion Findings

### 1. Corpus Completeness And Index Alignment

The corpus contains 61 tech specs matching the 61 generated story files. `docs/tech-specs/README.md` lists TS-CMF-001 through TS-CMF-061, and `docs/bmm-workflow-status.yaml` records the same count.

### 2. Frontmatter And Section Schema Completeness

Every spec has the required 19 frontmatter fields and 14 top-level sections. Validation found 854 required section hits and 1159 required frontmatter field hits.

### 3. FR Coverage And Requirement Trace Integrity

Every spec carries FR IDs in frontmatter and a `Requirement Trace` section. The corpus covers FR-CMF-01 through FR-CMF-10, including cross-cutting coverage for orchestration, recovery, spec governance, provider operations, publishing, memory, and projection.

### 4. Pipeline Trace, Entry/Exit Object, Validation Contract, And Receipt Clarity

Every spec carries canonical pipeline stage, entry object, exit object, validation contract, and required receipt in frontmatter and in `Pipeline Stage Trace`. This preserves the PRD pipeline authority established during PRD and architecture repair.

### 5. Source-Read Discipline And Required Source Anchors

Pre-repair, TS-CMF-031 and TS-CMF-032 did not explicitly cite the Product Brief, and TS-CMF-038 did not explicitly cite the Legacy Inventory. These were repaired.

Post-repair source anchor counts:

- Product Brief cited in 61/61 specs.
- Legacy Inventory cited in 61/61 specs.
- Pipeline map cited in 61/61 specs.
- Files Read section present in 61/61 specs.

### 6. Legacy Inventory, JIT Skill, And Intentional Orchestration Fidelity

Pre-repair, the first 22 specs used `Greenfield Integration and Legacy Migration Context` instead of the later `Legacy Intelligence Mapping` heading. The content was present, but machine auditability was inconsistent.

Repair action: normalized the heading to `Legacy Intelligence Mapping` across all 61 specs.

### 7. Python/Pydantic/DSPy/Pi Implementation Specificity

The specs consistently use Python, Pydantic v2, FastAPI, durable workflows, DSPy programs, Pi orchestration, and generated TypeScript consumers where appropriate. TypeScript remains restricted to PWA, Telegram Mini App, Remotion, Motion Canvas, and generated contracts.

### 8. Commands, Events, Workflows, And Receipts

Every spec includes `Commands, Events, Workflows, and Receipts`. This is the strongest implementation-readiness feature of the corpus: state transitions are not left as UI behavior or agent chat.

### 9. CBAR, RSCS, Gates, And Failure Examples

Every spec includes CBAR tension, resolution demand, downstream proof, acceptance criteria with failure examples, and a spec audit receipt. RSCS appears explicitly in the areas where signal density and anti-genericity are central, especially interview intelligence, extraction, memory, and readiness.

### 10. Cross-Spec Dependency And Boundary Consistency

The dependency sections are consistent enough for a build executor to follow in dependency order. Residual build risk remains: implementation must still maintain an external Build Ledger so specs are built one at a time and dependencies are marked `BUILT`, `PENDING`, or `BLOCKED`.

### 11. Provider, Commercial, Neo4j, And No-Drift Guardrails

The corpus preserves the corrected provider stack, the two accepted pricing paths, no-newsletter policy, no-MVP/full-system discipline, and Neo4j as rebuildable projection only. Drift scan found no forbidden positive drift terms.

### 12. Developer Build Readiness And Verification Detail

Each spec names tasks, dependencies, test strategy, observability, recovery, rollback, and acceptance criteria. The next implementation executor should use TS-CMF-001 first and proceed dependency-first. If implementation reveals ambiguity, the build protocol should flag and halt rather than improvise beyond the spec.

## Repair Findings

| Priority | Finding | Repair | Status |
|---:|---|---|---|
| 1 | First 22 specs used a different legacy-mapping subsection title, making corpus-level audit less uniform | Normalized `Greenfield Integration and Legacy Migration Context` to `Legacy Intelligence Mapping` across tech specs | Completed |
| 2 | TS-CMF-031 and TS-CMF-032 lacked explicit Product Brief source rows | Added Product Brief source rows for dual extraction, JIT skill compiler, source-truth review, and evaluation doctrine | Completed |
| 3 | TS-CMF-038 lacked explicit Legacy Inventory source row | Added Legacy Inventory source row for scene reproducibility, beat-fingerprint, manifest lineage, and asset engine references | Completed |
| 4 | Workflow status did not yet include tech-spec MCDA result | Add this eval to workflow status | Pending in status update |

## Validation Results

- Tech specs generated: 61.
- Required section hits: 854.
- Required frontmatter field hits: 1159.
- Files Read sections: 61.
- Requirement Trace sections: 61.
- Pipeline Stage Trace sections: 61.
- Legacy Intelligence Mapping sections: 61.
- Product Brief source anchors: 61.
- Legacy Inventory source anchors: 61.
- Pipeline map source anchors: 61.
- Primary Output Schema sections: 61.
- Commands/events/workflows/receipts sections: 61.
- CBAR sections: 61.
- Acceptance criteria with failure examples: 61.
- Spec Audit Receipt sections: 61.
- Forbidden drift scan: clean for MVP, Minimum Releasable, RunningHub, Flux Kontext, extra pricing tiers, TypeScript source of truth, Neo4j as canonical, newsletter package, TODO/TBD, and conflict markers.

## Downstream Build Mandates

Implementation should now proceed through the legacy build-executor discipline adapted for CMF:

1. Build one spec at a time.
2. Start with TS-CMF-001, TS-CMF-002, and TS-CMF-003 before feature specs.
3. Treat the spec as law; if ambiguity appears, flag it rather than inventing behavior.
4. Confirm upstream dependencies before each build.
5. Emit build receipts with spec fidelity, AC coverage, contract integrity, receipt chain, and CBAR compliance evidence.
6. Preserve Python/Pydantic/DSPy/Pi implementation authority and keep TypeScript as a leaf/runtime consumer.
7. Keep the Legacy Inventory as read-only intelligence, fixture, eval, doctrine, or migration source; never as direct production runtime import.
