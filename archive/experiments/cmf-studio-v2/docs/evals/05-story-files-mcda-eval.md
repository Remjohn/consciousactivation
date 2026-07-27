---
title: "CMF STUDIO Generated Story Files MCDA Evaluation"
evaluated_artifact: "docs/stories"
source_of_truth:
  - "docs/epics.md"
  - "THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md"
  - "docs/architecture.md"
supporting_artifacts:
  - "docs/cmf-studio-pipeline-map.md"
  - "docs/migration/legacy-inventory.md"
  - "docs/evals/04-epics-stories-mcda-eval.md"
evaluation_date: "2026-06-21"
criteria_count: 12
story_file_count: 61
pre_repair_weighted_score_10: 9.01
pre_repair_weighted_score_100: 90.1
post_repair_weighted_score_10: 9.44
post_repair_weighted_score_100: 94.4
status: "story-files-ready-after-repair"
---

# CMF STUDIO Generated Story Files MCDA Evaluation

## Evaluation Standard

This MCDA evaluates the generated files in `docs/stories` as independent artifacts for tech-spec generation. Each story file must preserve FR coverage, canonical pipeline trace, entry/exit objects, validation contract, required receipt, epic context, story definition, acceptance criteria, technical notes, legacy/primitive mapping, prerequisites, CBAR pressure, and tech-spec handoff requirements.

## Scoring Summary

| Criterion | Weight | Pre-Repair Score | Weighted | Post-Repair Score | Weighted |
|---|---:|---:|---:|---:|---:|
| 1. Story count and index completeness | 8 | 9.8 | 78.4 | 9.8 | 78.4 |
| 2. Frontmatter and trace schema completeness | 10 | 9.4 | 94.0 | 9.6 | 96.0 |
| 3. FR trace preservation | 9 | 9.3 | 83.7 | 9.3 | 83.7 |
| 4. Pipeline trace preservation | 10 | 9.4 | 94.0 | 9.4 | 94.0 |
| 5. Self-contained story context | 8 | 7.8 | 62.4 | 9.4 | 75.2 |
| 6. Acceptance criteria and CBAR pressure | 8 | 9.2 | 73.6 | 9.2 | 73.6 |
| 7. Tech-spec handoff readiness | 9 | 9.3 | 83.7 | 9.4 | 84.6 |
| 8. Legacy and primitive mapping preservation | 8 | 9.2 | 73.6 | 9.2 | 73.6 |
| 9. Orchestration/spec compiler anchor coverage | 8 | 9.4 | 75.2 | 9.4 | 75.2 |
| 10. Provider, commercial, Neo4j, and format guardrails | 7 | 9.5 | 66.5 | 9.5 | 66.5 |
| 11. Structural hygiene and boundary integrity | 8 | 7.0 | 56.0 | 9.7 | 77.6 |
| 12. Independent usability by tech-spec agents | 7 | 8.6 | 60.2 | 9.4 | 65.8 |
| **Total** | **100** |  | **901.3** |  | **944.2** |

**Pre-repair verdict:** the first generated story set was largely complete, but the splitter allowed the final story of each epic to retain the next epic separator/preamble. That made some files less clean as independent artifacts.

**Post-repair verdict:** story-files-ready. The regenerated files have clean story boundaries, complete trace metadata, no empty FR lists, and consistent tech-spec handoff requirements.

## Repair Findings

| Priority | Finding | Repair | Status |
|---:|---|---|---|
| 1 | Last-story files at epic boundaries could inherit the next epic prelude | Regenerated all story files with story boundaries stopping at next story, next epic, or FR coverage section | Completed |
| 2 | Story files needed validation as independent tech-spec inputs | Verified count, frontmatter, trace fields, sections, and handoff requirements | Completed |
| 3 | Status metadata needed to reflect the generated story set | Updated workflow status with story directory, count, and MCDA result | Completed |

## Validation Results

- Story files generated: 61.
- Frontmatter delimiters: 122, exactly two per story file.
- Required frontmatter fields checked: 610.
- Required story sections checked: 244.
- Tech-spec handoff sections: 61.
- Empty FR lists: 0.
- `TBD` trace metadata: 0.
- Stray `## Epic` headings inside story files: 0.
- Conflict markers: 0.
- Forbidden drift terms checked: no `Wave`, `MVP`, `Minimum Releasable`, wrong provider names, or positive RunningHub/newsletter references.

## Downstream Mandates

Tech specs may now be generated from the story files. Each tech spec must use:

1. The story file itself as a source.
2. `FilesReadReceipt` for PRD, architecture, Product Brief, Legacy Inventory, pipeline map, and feature-specific sources.
3. `RequirementTrace` for the story's FR IDs.
4. `PipelineStageTrace` for the story's pipeline metadata.
5. CBAR tension, failure scenario, resolution demand, and downstream proof.
6. Pydantic contracts, commands/events, workflows/services, tests, observability, and recovery notes before implementation.
