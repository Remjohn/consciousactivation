---
type: prd-module
project: CMF STUDIO
module_id: PRD-CMF-04
status: canonical
source_prd: 05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
source_sections:
  - Legacy Migration Acceptance Gate
  - FR-CMF-03
last_updated: 2026-06-22
legacy_lineage:
  - reference/conscious-rivers/docs/prd/modules/PRD_02_CCF_Content_Factory.md
  - reference/conscious-rivers/docs/prd/modules/PRD_03_CMF_Media_Factory.md
  - reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md
---

# PRD-CMF-04 - Legacy, Primitives, JIT Skills, and Spec Governance

## Module Purpose

This module transforms legacy CCF/CMF intelligence into CMF STUDIO product requirements. The old CCP PRDs, registry specs, prompt systems, JIT skills, CMF engines, primitive registries, SDA/SFL files, CBAR gates, TTT methods, ComfyUI templates, and BMAD/ERA3 protocols are not canonical CMF modules by copy-paste. They are lineage sources that must be converted into typed CMF registries, compilers, fixtures, worker assets, evals, and approval gates.

## Product Requirements

### PR-CMF-04.01 Migration Ledger

Migration Stewards can inventory, classify, hash, map, convert, validate, approve, deprecate, block, and inspect legacy assets. Every migrated asset must carry source path, content hash, legacy type, registry family, source owner, known defects, target Pydantic contract, target DSPy program when applicable, fixture target, evaluation target, reviewer, status, and replacement target.

### PR-CMF-04.02 Primitive Registry Authority

The 244 cognitive primitives, Meaning Plane families, Experience Plane families, SDA ontology files, SFL function libraries, crosswalks, failure corpora, and primitive coalition logic must be imported as project-owned registry assets under `registries/`.

Primitives are production quality standards. They must influence interview engineering, extraction, archetype routing, scene orchestration, evaluation rubrics, and review blockers. They cannot become loose tone labels.

### PR-CMF-04.03 Intentional Orchestration Preservation

Legacy modules often encode why a process exists, not only what it outputs. Any migrated orchestration-bearing module must preserve:

- organism layer and product responsibility;
- required inputs;
- emitted packets;
- ordering constraints;
- gates and blockers;
- downstream consumers;
- failure modes;
- proof obligations.

This is required for old CCF, CMF, primitive, scene intelligence, asset engine, SVRE/Aurore, CRAL/SCRE, and JIT skill modules.

### PR-CMF-04.04 JIT Skill Compiler System

JIT Skill Compiler modules must support extraction, narrative induction, interview engineering, route selection, drafting, contrastive prompting, anti-draft calibration, Voice DNA, Emotional DNA, and evaluation. They are not generic few-shot prompts.

Each invocation must create a `SkillInvocationRecord` with:

- source context and transcript or pre-session evidence;
- registry snapshot;
- compiler fingerprint;
- contrastive prompt layer;
- critic result;
- synthesis result;
- accepted or rejected downstream use.

Some skills are stable operational skills bound to agents. JIT skills are context-compiled for specialized creative reasoning, especially interview briefs, induction moves, extraction lenses, and output shaping.

The Conscious Interview Brief Skill is the canonical interview-first JIT compiler. It must preserve old CCF orchestration as an intelligence stack: SCRE/CRAL signal discovery, primary signal packets, edge selection, pressure framing, authenticated response logic, primitive candidates, coalition survival, route recommendation, and source artifact discipline. In CMF, that stack is rebuilt through Guest Truth, Interviewer Resonance, Audience Reality, Context Premise, Matrix of Edging pressure, target expression states, First-Line Anchors, Depth Anchors, landing evaluation, and route targets. It cannot emit Interview Asset Contract candidates unless CRAL evidence, audience conversation/comment evidence, Context Premise, Interviewer Resonance Context, Matrix pressure, primitive candidates, invariants or coalition refs when available, hard negatives, and evaluation history are present.

### PR-CMF-04.05 Spec Governance

PRD, epic/story, architecture, and tech-spec workflows must use the BMAD/ERA3 discipline updated for Python, Pydantic, DSPy, Pi, CMF greenfield constraints, CBAR, RSCS signal-density checks, and legacy migration proof.

Generated specs must include files-read evidence, FR trace, pipeline trace, CBAR check, acceptance criteria trace, migration notes, eval target, and receipt chain.

### PR-CMF-04.06 Legacy Runtime Boundary

Direct imports from old runtime modules into production packages are blocked. ComfyUI JSON files may become worker assets. Prompt stacks may become registry entries or JIT compilers. Service behavior may become Pydantic contracts, deterministic services, DSPy programs, fixtures, or evals.

## Functional Requirements Covered

- FR-CMF-03.01 through FR-CMF-03.09.

## Canonical Project Assets

- `registries/primitives/`
- `registries/sda/`
- `registries/sfl/`
- `registries/cmf-assembler-schemas/`
- `docs/registry-specs/`
- `docs/migration/legacy-inventory.md`
- `src/ccp_studio/services/jit_skill_compiler_service.py`
- `src/ccp_studio/services/registry_service.py`
- `src/ccp_studio/services/evaluation_target_service.py`

## Acceptance Gates

- A legacy asset cannot influence production until ledgered, mapped, reviewed, and evaluated.
- A primitive cannot become active without schema validity, examples, cross-references, and evaluation rubric.
- A JIT skill cannot emit production influence without a `SkillInvocationRecord`.
- A spec cannot pass if it omits legacy inventory, pipeline trace, FR trace, CBAR, or Python/Pydantic/DSPy/Pi boundary.

