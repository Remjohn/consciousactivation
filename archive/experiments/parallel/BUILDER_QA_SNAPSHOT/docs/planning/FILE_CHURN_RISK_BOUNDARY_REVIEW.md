# Builder V1.2 Step 4 File-Churn and Risk-Boundary Review

Date: 2026-07-14  
Scope: confirmed 69-Story planning inventory  
Production implementation: prohibited

## Result

The Story decomposition is sufficiently bounded for implementation planning, but it is not implementation-ready. Every Story has at least one technical-specification assignment, all assignments resolve to TS-00 through TS-15 or `IMPLEMENTATION_BASELINE`, and no Story changes its confirmed primary Epic or obligation ownership.

This review predicts churn and coupling; it does not authorize or perform source-code changes. The repository currently has no `src/`, `tests/`, dependency manifest, Dockerfile, or CI workflow, so all implementation file paths remain future Development Capsule inputs.

## Assignment and hotspot summary

| Measure | Result |
|---|---:|
| Confirmed Stories | 69 |
| Stories with technical-specification assignments | 69 |
| Stories without a technical-specification assignment | 0 |
| Valid specification handles | TS-00..TS-15 plus `IMPLEMENTATION_BASELINE` |
| Unique planned contract handles | 42 |
| Unique planned schema references | 6 |
| Cross-repository dependencies | 6 |

The highest shared-specification hotspots are TS-14 (37 Stories), TS-12 (32), TS-13 (25), TS-07 and TS-11 (24 each), TS-10 (20), and TS-00/TS-06 (19 each). These files define workflow, Control Tower, authorization, graph, category/target and evaluation seams; future change control must treat them as coordination boundaries rather than convenient shared dumping grounds.

## Highest combined risk Stories

The risk score counts specification breadth, contract/schema surfaces, cross-repository dependencies and unresolved blockers. It is a planning prioritization aid, not a readiness score.

| Story | Epic | Risk | Primary drivers |
|---|---|---:|---|
| ST-08.06 | EP-08 | 41 | 15 specs, five external dependencies, five blockers, contract/schema evaluation breadth |
| ST-06.01 | EP-06 | 40 | complete constitutional semantic stack, seven contracts, seven blockers |
| ST-06.03 | EP-06 | 38 | Reaction/Expression lineage, seven contracts, seven blockers |
| ST-12.04 | EP-12 | 37 | all six external dependencies and all seven carried gates |
| ST-12.03 | EP-12 | 35 | full Format 02 spine, nine specs, all six external dependencies |
| ST-08.02 | EP-08 | 34 | evaluator/benchmark boundary, five external dependencies and five blockers |
| ST-06.02 | EP-06 | 32 | seven semantic contracts and seven unresolved decisions/blockers |
| ST-06.05 | EP-06 | 32 | semantic handoff completeness and external authority |
| ST-08.04 | EP-08 | 32 | independent evaluation, protected evidence and five external dependencies |
| ST-06.04 | EP-06 | 30 | seven semantic contracts despite a narrow primary spec assignment |

## Mandatory risk boundaries

1. **Canonical IR and generated artifacts:** JSON Schema, Markdown, OpenSpec and target packages compile from canonical IR/registries; Stories may not author duplicate truths.
2. **External products:** Builder may consume VAE, Delegation, Interview, ReelCast and Activation Compiler interface evidence, but never implement their production behavior or fork their authority.
3. **Semantic ownership:** Runtime Activation First and development-time Visual Syntax First remain distinct. Models cannot invent source class, Reaction Receipt, Expression Moment, activation direction, viewer role or wrong-reading authority.
4. **Workflow and state:** Temporal, PostgreSQL and content-addressed storage stay behind ports; domain/application code cannot import adapters or UI state.
5. **Evaluation:** Generator access is separated from protected labels. Scores cannot compensate for failed hard gates or unresolved authority.
6. **Human decisions:** HD-006, HD-007, BD-004, BD-007, BD-008, BD-010 and BD-014 remain blocking where referenced.
7. **Completion receipts:** All 69 StoryCompletionReceipts remain `PLANNED_NOT_ISSUED`; document completion cannot be treated as executable acceptance.

## Implementation sequencing rule

Future implementation must follow the 1–69 dependency order and may start only after a Development Capsule identifies the exact bounded Story subset whose blockers, dependencies, contracts, tests, rollback and authority are satisfied. No Story may depend on a future Story, and no high-risk shared file may be changed without rerunning all consuming Story tests.

