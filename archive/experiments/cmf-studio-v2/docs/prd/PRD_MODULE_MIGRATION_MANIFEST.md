# PRD Module Migration Manifest

## Status

The canonical CMF Studio PRD module set has been transformed from `05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md`.

## Canonical Module Folder

`docs/prd/modules/` contains only the active CMF-native module family:

- `PRD_INDEX.md`
- `PRD_CMF_01_Strategy_Scope_Release_Gates.md`
- `PRD_CMF_02_Pipeline_Agent_Orchestration.md`
- `PRD_CMF_03_Workspace_Commercial_Consent_Source.md`
- `PRD_CMF_04_Legacy_Primitives_JIT_Spec_Governance.md`
- `PRD_CMF_05_Brand_Genesis_Context.md`
- `PRD_CMF_06_Interview_Expression_Routing.md`
- `PRD_CMF_07_Editing_Composition_Rendering.md`
- `PRD_CMF_08_Evaluation_Review_Publishing_Memory.md`
- `PRD_CMF_09_Non_Functional_Requirements.md`
- `PRD_CMF_10_Agent_Factory_Runtime.md`

## Demoted Legacy Lineage

These old CCP PRD modules are no longer canonical CMF modules:

- `reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md`
- `reference/conscious-rivers/docs/prd/modules/PRD_03_CMF_Media_Factory.md`
- `reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md`

They remain required lineage for migration, primitive registry interpretation, intentional orchestration recovery, and old CCF/CMF design rationale.

## Archived CMF Drafts

These earlier CMF extension drafts are archived as non-canonical drafts:

- `reference/cmf-drafts/prd-modules/PRD_10_CMF_Interview_Intelligence.md`
- `reference/cmf-drafts/prd-modules/PRD_11_CMF_JIT_Interview_Brief_Compiler.md`
- `reference/cmf-drafts/prd-modules/PRD_12_CMF_Primitive_Eval_Review_Workbench.md`
- `reference/cmf-drafts/prd-modules/PRD_13_CMF_Agent_Factory_Runtime.md`

Their product content has been folded into `PRD_CMF_04`, `PRD_CMF_06`, `PRD_CMF_08`, and `PRD_CMF_10`.

## Rule

New epics, stories, architecture, tech specs, evals, agent specs, and implementation work should cite the `PRD_CMF_*` module family as canonical product requirements. Legacy PRDs and archived drafts may be cited only as lineage or migration evidence.
