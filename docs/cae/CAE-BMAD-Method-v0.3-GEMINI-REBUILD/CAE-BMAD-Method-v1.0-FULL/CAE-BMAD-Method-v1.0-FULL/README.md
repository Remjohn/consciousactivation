# CAE-BMAD Method v1.0-FULL

## Purpose

This bundle is the **CAE adaptation layer on top of the real BMAD-METHOD repository**.

It is deliberately not a miniature reimplementation of BMAD.

The installation model is:

```text
REAL BMAD-METHOD
    +
CAE mandatory method layer
    +
CAE research / reconstruction rules
    +
CAE Grill
    +
Agentic Operating Levels
    +
CAE product-documentation lineage
```

The user's BMAD fork is the preferred upstream base:

`https://github.com/Remjohn/BMAD-METHOD`

The original BMAD repository is itself a fork lineage from:

`https://github.com/bmad-code-org/BMAD-METHOD`

The current BMAD repository documents a skill-based architecture in which workflows, agents,
tasks, and tools are represented as installable `SKILL.md` entrypoints. The current repository
also retains the core skill family and the BMM planning/solutioning/implementation families.
CAE-BMAD deliberately rides on that structure rather than creating a competing tiny runtime.

## Critical principle

**The original BMAD files are not optional source material.**

The CAE method must preserve the substantive upstream BMAD skill tree.

The installer therefore validates mandatory upstream families before installing CAE-BMAD:

- `src/core-skills/`
- `src/bmm-skills/`
- `src/scripts/`
- `tools/`
- `docs/`

and checks for the key BMM/Core skills used by the CAE workflow chain.

If the required upstream structure is not present, installation fails.

## CAE workflow

```text
00 Product Reconstruction
        ↓
01 Operating-Level Assessment
        ↓
02 CAE Grill
        ↓
03 Product Brief
        ↓
04 Modular PRD
        ↓
05 Functional Requirements
        ↓
06 Architecture
        ↓
07 Epics + Stories
        ↓
08 UI / UX
        ↓
09 Brownfield Reconciliation
        ↓
10 Implementation Handoff
        ↓
11 Review
```

The CAE layer does not eliminate BMAD's native help, deep research, review, specification,
product brief, PRD, architecture, UX, epic/story, sprint, development, or code-review capabilities.
Instead it establishes the **mandatory CAE entry conditions, source discipline, lineage rules,
and handoff contracts** for the CAE product.

## What changes from vanilla BMAD

The major change is the front door.

Vanilla BMAD can begin from an idea or change request and scale the planning depth to the work.
CAE begins from a historically accumulated product and requires reconstruction before major
rewrites.

Therefore:

```text
generic idea → brief
```

becomes:

```text
research corpus
+
historical lineage
+
existing repository
+
product artifacts
+
runtime reality
    ↓
reconstruction
    ↓
grill
    ↓
product brief
```

## Required artifacts

The CAE workflow chain produces:

- Product Reconstruction
- Product Lineage Map
- Product Evidence Ledger
- Contradiction Register
- Operating-Level Assessment
- Decision Ledger
- Product Brief
- PRD Index
- PRD Modules
- Functional Requirements
- Architecture
- Architecture Decisions
- Epics
- Stories
- UI / UX
- Brownfield Reality Map
- Implementation Handoff
- Proof Plan
- Review Record

## Research library

The target library is **216 sources**.

The current bundle carries the verified/working 144-source baseline as a starting inventory and
requires that it be extended and verified to 216 before a project may mark `research_complete: true`.

This corpus must include the product roots that are easy to lose when reading only `docs/cae`:

- CCP
- CCF
- CMF
- Conscious Primitives
- Conscious Reactions
- SDA/SFL
- Matrix of Edging
- JIT Skill Compiler
- CRAL
- visual research
- Atomic Harnesses
- Visual Syntax
- production formats
- book/audit research
- question/interview intelligence
- sound/music/voice research
- historical transcripts
- current CAE Program/Workflow/Runtime documentation
- engineering reality

## Mandatory truth rules

- A filename is not evidence of completion.
- A passing test is not production proof without reality contact.
- Historical truth and current implementation truth must remain distinct.
- Proposed architecture cannot silently become current-state truth.
- A contradiction is a first-class research result.
- An unresolved human decision stays unresolved until the operator decides or explicitly accepts deferral.
- One CAE Grill question at a time.
- Inspect before asking.
- Go down the operating levels when evidence is weak.
- Go up when repetition, stable contracts, and evidence justify leverage.
- Preserve source lineage when rewriting product documents.
- Do not duplicate existing CAE Programs, Workflows, Skills, Harnesses, Sessions, or Runtime.

## Installation

### Preferred: add to your existing BMAD fork

Run from your `Remjohn/BMAD-METHOD` checkout:

```bash
bash /path/to/CAE-BMAD-Method-v1.0-FULL/scripts/install_into_bmad.sh
```

or on PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_into_bmad.ps1 -Target "C:\path\to\BMAD-METHOD"
```

The installer:

1. validates the original BMAD tree,
2. verifies required original skill families,
3. copies the CAE module and mandatory overlay,
4. writes a CAE manifest,
5. runs structural validation,
6. does not delete or replace original BMAD skills.

### Fresh bootstrap

The shell/PowerShell bootstrap can clone the user's BMAD fork first when requested.

## Start

After installation, use:

```text
caebmad-help
```

Then, for this product-reconstruction effort:

```text
caebmad-product-reconstruction
```

Do not jump directly to a PRD for the CAE rewrite until reconstruction is complete.

## Versioning

This package version is independent of BMAD's version.
The BMAD base SHA/tag is recorded in `.caebmad/_config/upstream-manifest.yaml` after installation.
