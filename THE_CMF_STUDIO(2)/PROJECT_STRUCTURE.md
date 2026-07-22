# THE CMF STUDIO Project Structure

This folder is the CMF Studio project workspace. New CMF product, architecture, story, spec, eval, UI, and agent-factory work belongs here.

`D:\Work\Conscious_Rivers` outside this folder is treated as reference-only unless Emilio explicitly asks to edit it.

## Primary Project Areas

| Path | Purpose |
|---|---|
| `05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md` | Main interview-first CMF Studio PRD |
| `product-brief-CMF_STUDIO-2026-06-19.md` | Primary product brief source |
| `docs/prd/modules/` | Canonical CMF-native PRD modules derived from the current PRD (`PRD_CMF_*`) |
| `docs/architecture.md` | CMF Studio architecture |
| `docs/cmf-studio-pipeline-map.md` | End-to-end pipeline and object spine |
| `docs/epics.md` | CMF epics and stories source |
| `docs/stories/` | Individual story files |
| `docs/tech-specs/` | TS-CMF technical specifications |
| `docs/evals/` | MCDA and evaluation architecture docs |
| `docs/implementation/` | Execution plans and build sequencing |
| `docs/ui/` | UI/workbench specifications |
| `docs/methodology/` | Methodology dependencies and CMF implementation map |
| `docs/migration/` | Legacy inventory copy required by CMF project docs |
| `docs/analysis/` | Supporting research/analysis artifacts |
| `reference/conscious-rivers/` | Legacy lineage references from the old/reference workspace, including old CCP PRD modules |
| `reference/cmf-drafts/` | Earlier CMF PRD extension drafts superseded by the canonical `PRD_CMF_*` modules |

## Boundary Rule

All new CMF Studio work should be created inside this folder. If old CCP/Conscious Rivers material is needed, copy it into `reference/conscious-rivers/` or a matching `docs/...` dependency path and cite it from there. Do not write new CMF project artifacts into the parent `docs/` folder.

## Current Migration

The migration consolidated:

- 4 new CMF modular PRDs;
- 61 story files;
- 61 TS-CMF technical specs;
- 7 eval documents;
- CMF architecture, epics, pipeline, agent factory, skill, intelligence, and implementation docs;
- key methodology and legacy inventory references;
- SCRE/CRAL, SVRE/Aurore, and April audit/build/revision framework references;
- 10 canonical CMF-native PRD modules transformed from the current CMF Studio PRD.

## PRD Module Rule

`docs/prd/modules/` is now CMF-native. The canonical router is `docs/prd/modules/PRD_INDEX.md`, and the canonical module family is `PRD_CMF_01` through `PRD_CMF_10`.

Old CCP modules such as `PRD_02_CCF_Content_Factory.md`, `PRD_03_CMF_Media_Factory.md`, and `PRD_08_Conscious_Primitives.md` are lineage references under `reference/conscious-rivers/docs/prd/modules/`. They may inform migration and registry design, but new CMF requirements must be written against the `PRD_CMF_*` module family.
