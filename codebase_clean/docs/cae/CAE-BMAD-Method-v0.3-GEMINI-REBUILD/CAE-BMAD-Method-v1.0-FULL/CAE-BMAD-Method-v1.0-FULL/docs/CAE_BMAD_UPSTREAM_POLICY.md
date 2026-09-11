# CAE-BMAD Upstream Policy

## Purpose

Prevent the CAE adaptation from silently turning into a reduced or disconnected copy of BMAD.

## Mandatory principle

The CAE layer is an overlay.

It does not replace the original BMAD repository.

## Required original tree

The installed base must include:

```text
src/core-skills/
src/bmm-skills/
src/scripts/
tools/
docs/
```

## Required key BMAD capabilities

At minimum, the base must expose the equivalent of:

### Core

- bmad-help
- bmad-deep-recon
- bmad-advanced-elicitation
- bmad-review
- bmad-customize
- bmad-brainstorming
- bmad-forge-idea
- bmad-party-mode

### BMM planning / solutioning

- bmad-product-brief
- bmad-prd
- bmad-spec
- bmad-ux
- bmad-architecture
- bmad-create-epics-and-stories
- bmad-check-implementation-readiness
- bmad-project-context

### BMM implementation

- bmad-create-story
- bmad-dev-story
- bmad-code-review
- bmad-correct-course
- bmad-sprint-planning
- bmad-sprint-status
- bmad-retrospective

The exact directory organization may change across BMAD versions, so the validator accepts current
equivalent locations declared in the manifest.

## Why retain these

They contain mature execution knowledge that should not be discarded simply because CAE adds a
specialized discovery/reconstruction layer.

## CAE override policy

Where a CAE skill and an original BMAD skill address the same product-development artifact,
the CAE workflow owns the **entry conditions** and source discipline.

The original BMAD skill remains available as a reusable execution capability.

Example:

```text
CAE Research/Reconstruction
      ↓
CAE Product Brief gate
      ↓
BMAD Product Brief mechanics
      ↓
CAE evidence/lineage validation
```

## Do not fork the whole universe

CAE may adopt only the BMAD components it needs.

However, removing original components from the base is prohibited unless an explicit
deprecation record explains what replaces them and a validator checks the replacement.
