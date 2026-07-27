---
title: "CMF Methodology Implementation Map"
status: "draft-canonical"
created_at: "2026-06-22"
source_files:
  - "docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md"
  - "reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md"
  - "THE CMF STUDIO/Matrix of Edging.md"
  - "reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md"
  - "docs/tech-specs/TS-CMF-025-matrix-of-edging-brief.md"
  - "docs/tech-specs/TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md"
---

# CMF Methodology Implementation Map

## 1. Purpose

This map defines how CMF Studio methodologies become runtime behavior. Methodologies are not decoration and they are not hidden prompts. They become:

- typed contracts;
- registry entries;
- DSPy program specs;
- primitive obligations;
- JIT compiler modes;
- validation gates;
- eval definitions;
- review read-model evidence.

## 2. Core Rule

Primitives are the production quality standard. They define what "good" means inside CMF Studio because they are the canonical transformation operators for meaning and experience.

An asset can be visually polished and still fail CMF quality if its intended primitive coalition collapses, its edge product is flattened, its evidence cannot support the activation, or its route no longer matches the source expression.

## 3. Methodology to Runtime Map

| Methodology | Runtime entry point | Primary objects | Responsible agents | Evaluation use |
|---|---|---|---|---|
| RSCS Law 1 - Saturation | CRAL, Context Premise, Matrix, JIT skills | `ResearchSnapshot`, `ContextPremise`, `SaturationContextBundle` | SCRE/CRAL Research Agent, Context Premise Agent, JIT Skill Compiler Agent | Checks evidence density, source diversity, missing context, and premature compression |
| RSCS Law 2 - Collision | Matrix of Edging, induction, extraction | `TensionSite`, `PrimitiveCandidatePacket`, `EdgeProduct` | Matrix Agent, Narrative Induction Agent, Extraction Agent | Checks contradiction, prediction violation, costly exposure, latent pattern articulation |
| RSCS Law 3 - Compression | Context Premise, route selection, SceneSpec | `AudienceDeepTriggerMap`, `RouteCandidate`, `SceneSpec` | Context Premise Agent, Route Candidate Agent, SceneSpec Compiler | Checks whether complexity becomes a precise artifact without generic flattening |
| RSCS Law 4 - Reality Contact | Evaluation and review | `EvaluationReceipt`, `ReviewEvidenceState` | Evaluation Agent, Review Workbench Agent | Checks source truth, evidence, consent, routeability, and human review readiness |
| Conscious Primitives | All production stages | `PrimitiveCandidatePacket`, `CoalitionSignature`, `EdgeProduct` | Matrix Agent, JIT Skill Compiler Agent, Evaluation Agent | Quality standard for transformation operators, family fit, sparsity, and anti-centroid pressure |
| Matrix of Edging | Interview preparation | `MatrixOfEdgingBrief`, `MatrixReceipt` | Matrix of Edging Agent | Pass completeness, saturation, collision strength, specificity, routeability |
| CRAL / SCRE | Research and context | `CRALFinding`, `ResearchEvidence`, `ResearchSnapshot` | SCRE/CRAL Research Agent, Evidence Critic | Source hierarchy, freshness, epistemic friction, source discipline, contradiction handling |
| Context Premise | Research to induction | `ContextPremise`, `AudienceRealityBrief`, `AudienceDeepTriggerMap` | Context Premise Agent | Audience truth, hermeneutical gap, trigger depth, moral-emotional vector |
| JIT Skill Compiler | Saturated specialist execution | `SkillInvocationRecord`, `CalibrationReport` | JIT Skill Compiler Agent | Evidence grounding, contrastive candidates, anti-draft calibration, primitive survival |
| Expression Extraction | Post-session extraction | `ExpressionMoment`, `RouteCandidate` | Expression Extraction Agent | Source truth, quote boundaries, depth, primitive activation, route readiness |
| SVRE / Aurore | Asset research | `VisualResearchQuery`, `VisualCandidate`, `AssetResearchManifest` | SVRE/Aurore Agent | Visual fit, source provenance, licensing, T-Score, known-person validity |

## 4. Primitive Eval Obligations

Every eval definition may carry primitive obligations:

- required primitive refs;
- required primitive families;
- expected coalition signature;
- expected edge product;
- anti-centroid pressure statement;
- route implication;
- evidence refs that justify activation;
- hard negatives or counterexamples;
- forbidden over-activation or family saturation.

Primitive failures must be visible in the Review Workbench. They should not be hidden behind a generic "style failed" score.

## 5. Where Methodology Should Not Be Used

Methodology must not:

- override consent, source truth, role policy, cost policy, or human approval;
- be exposed as jargon to customer-facing review surfaces unless an operator needs diagnostic detail;
- authorize a route or content format that is absent from active registries;
- become memory without evidence admission;
- create new primitive definitions outside the primitive registry flow;
- substitute for actual CRAL/SVRE research.

## 6. Minimum Implementation Targets

1. `EvalDefinition` supports primitive obligations.
2. `EvalTargetSelection` selects required evals by object type, pipeline stage, route refs, and primitive refs.
3. `EvaluationReceipt` supports object types upstream of render output.
4. `EvaluationApprovalBlocker` can cite primitive failure categories.
5. `ReviewEvidenceState` exposes primitive failures with evidence refs and repair actions.
6. JIT skill invocations cite the primitive obligations they attempted to satisfy.


