---
story_id: "11.5"
story_title: "Skill Bindings and JIT Compiler Modes"
epic_id: 11
epic_title: "Agent Factory Persona Runtime"
status: "ready-for-tech-spec"
source_epics_file: "docs/epics.md"
generated_at: "2026-06-22"
fr_ids: []
module_requirement_ids:
  - "PRD-CMF-10.05"
pipeline_stage: "stages 3-8 and 13"
entry_object: "agent role and skill need"
exit_object: "`SkillBinding`, JIT compiler mode binding"
validation_contract: "stable-vs-JIT distinction and invocation record requirement"
required_receipt: "skill binding receipt"
requires_legacy_inventory: true
requires_pipeline_trace: true
requires_cbar: true
---

# Story 11.5: Skill Bindings and JIT Compiler Modes

**Epic:** 11 - Agent Factory Persona Runtime
**Status:** Ready for Tech Spec
**Source:** `docs/epics.md`

## Story Definition

As a Factory operator, I want stable skills and JIT skills bound differently, so that daily operational procedures and context-compiled intelligence are both governed correctly.

**Acceptance Criteria:**

- Given a stable operational skill is bound to an Agent, when used, then it references a versioned skill manifest and allowed procedure.
- Given a JIT skill compiler is bound to an Agent, when invoked, then it requires saturation context, registry snapshot, compiler fingerprint, contrastive prompt layer, critic result, synthesis result, and `SkillInvocationRecord`.
- Given a skill is needed for interview engineering, when compiled, then it supports Interview Briefs, induction moves, contrast questions, extraction lenses, route support, or eval support.
- Given a skill only contains generic few-shot examples, when activation is requested, then the activation is blocked.
- Given `EXT-JITCOMP-AG` emits extraction candidates, when routing consumes them, then source context and eval state remain attached.

**Technical Notes:** Extend skill binding contracts to distinguish stable `SK` and JIT `JS` entities, allowed use modes, invocation receipts, and readiness evals.

**Legacy and Primitive Mapping:** Adapts old JIT skill modules from scripts/visual prompts into interview brief, induction, extraction, and evaluation compilers. Active families: STR, PSY, TRG, VSG, VOC, FBK.

**Prerequisites:** Stories 3.3, 5.5, 6.3, 11.2.

## Tech Spec Handoff Requirements

- Include files-read evidence for legacy JIT skill documentation and the CMF Skill System Contract.
- Define stable skill binding, JIT compiler mode binding, validation rules, invocation receipts, and tests.
