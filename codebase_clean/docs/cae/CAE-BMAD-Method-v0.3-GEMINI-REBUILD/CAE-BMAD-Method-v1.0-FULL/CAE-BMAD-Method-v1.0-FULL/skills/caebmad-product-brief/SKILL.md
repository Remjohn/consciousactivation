---
name: caebmad-product-brief
description: Create, update, or validate the reconstructed CAE Product Brief after the research and Grill gates have been satisfied, preserving historical lineage and separating current truth from proposed product direction.
---

# Caebmad Product Brief

## Operating Mode

This is a CAE-specific skill. It is not a generic prompt template.

The skill operates inside the CAE-BMAD method and must respect:

- the CAE source authority model
- the 216-source research corpus
- the historical lineage requirement
- the Agentic Operating Level Framework
- the one-question-at-a-time CAE Grill
- brownfield truth discipline
- explicit artifact state
- source-to-artifact traceability
- runtime reality contact
- the existing BMAD base
- the existing CAE execution primitives

## Invocation Contract

Before starting:

1. identify the current project root;
2. identify the CAE-BMAD workspace;
3. inspect project state;
4. inspect the relevant upstream artifact status;
5. inspect the required research sources;
6. determine whether this skill is actually the correct next step.

Never infer completion from a filename alone.

## Context Rules

Load only the context required by the current step.

Prefer:

- exact source documents
- exact implementation files
- exact source paths
- exact artifact references

Avoid copying entire unrelated documentation trees into the active context.

## Evidence Rules

Every consequential claim must be categorized as one of:

- KNOWN
- INHERITED
- VERIFIED
- PROPOSED
- INFERRED
- MISSING
- CONTRADICTED
- DEPRECATED

When a claim is repository-resolved, name the file and symbol where available.

When a claim comes from historical lineage, preserve its original path/title.

When the evidence is insufficient, say so.

## Brownfield Rules

Never:

- rename a legacy concept without documenting the mapping;
- treat current implementation as equivalent to desired architecture;
- declare a service obsolete only because a new component exists;
- invent implementation files;
- claim a provider was used without execution evidence.

## Completion

At completion:

1. validate the required artifact;
2. update its status;
3. update the CAE-BMAD project state;
4. record source/decision references;
5. provide the next valid workflow;
6. do not imply downstream work is complete.


## Required Reading

Read before execution:

1. `{project-root}/.caebmad/config/caebmad-config.yaml`
2. `{project-root}/.caebmad/method/CAE_BMAD_METHOD.md`
3. `{project-root}/.caebmad/method/CAE_BMAD_SOURCE_AUTHORITY.md`
4. `{project-root}/.caebmad/method/CAE_BMAD_ARTIFACT_GOVERNANCE.md`
5. `{project-root}/.caebmad/method/CAE_BMAD_UPSTREAM_POLICY.md`
6. the immediately upstream artifact required by this skill
7. only the research sources relevant to this invocation

Do not treat the baseline research inventory as a substitute for reading the actual sources.

## CAE Artifact Contract

This skill must produce or update the artifact(s) identified by its workflow manifest.

The output must contain:

- an explicit status
- source references
- decision references where applicable
- known/inherited/proposed/verified distinctions
- implementation references when the artifact is technical
- open issues where evidence remains incomplete

## Reviewer Behavior

Before finalizing the artifact, perform an internal adversarial pass.

Ask:

- Which claim is least supported?
- Which concept may have lost its lineage?
- Which requirement is accidentally an implementation decision?
- Which dependency is missing?
- What would falsify this conclusion?
- What current code could contradict the document?
- What operator decision has been smuggled in as an assumption?
- What is being inferred from file existence?
- What evidence would require moving down an operating level?

## Handoff

At the end, return:

1. artifact paths
2. artifact status
3. source coverage
4. unresolved decisions
5. downstream impact
6. next recommended CAE-BMAD skill

Do not claim implementation readiness unless the handoff and brownfield gates say so.
