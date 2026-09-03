# CAE-BMAD Method v0.3 — Gemini Rebuild Edition

A usable CAE-specific product-development method built from three sources of discipline:

1. **BMAD** — progressive product/development artifacts and workflow handoffs.
2. **CAE's own lineage** — CCP/CCF/CMF, Atomic Harnesses, visual syntax, research, transcripts, Programs, governance, and runtime.
3. **Agentic Operating Levels + CAE Grill** — decide where to inspect, what to automate, and what requires human judgment.

## What this is

CAE-BMAD is a brownfield product-development method for a long-lived product with substantial historical research and an existing codebase.

It is intentionally **not** a copy of the full BMAD workflow inventory.

It provides a complete usable path:

```text
RESEARCH / RECONSTRUCT
        ↓
OPERATING-LEVEL ASSESSMENT
        ↓
CAE GRILL
        ↓
PRODUCT BRIEF
        ↓
PRD INDEX + PRD MODULES
        ↓
FUNCTIONAL REQUIREMENTS
        ↓
ARCHITECTURE
        ↓
EPICS + STORIES
        ↓
UI / UX
        ↓
BROWNFIELD HANDOFF
        ↓
IMPLEMENTATION / PROOF
        ↓
REVIEW / EVOLUTION
```

## Installation

Copy the `skills/` directory into the skill directory supported by your agentic IDE.

For Claude Code:

```text
.claude/skills/
```

For Cursor/Windsurf-style skill layouts:

```text
.agents/skills/
```

Then copy `config/`, `templates/`, `workflows/`, `method/`, `schemas/`, and `docs/` into a project-local `.caebmad/` directory.

Run:

```bash
python scripts/init_caebmad.py
```

This initializes the project working area without modifying your application code.

## First command

Use:

```text
caebmad-help
```

Then:

```text
caebmad-reconstruct
```

The method intentionally starts with reconstruction rather than immediately writing a new PRD.

## Required research corpus

The target research corpus is **216 sources**.

The bundle currently carries the previously assembled 144-source baseline as a governed starting point. The remaining sources must be verified and added before calling the corpus complete.

The corpus is not treated as uniformly authoritative. Each source is scored and classified independently.

## Artifact contract

CAE-BMAD produces:

```text
Product Brief
PRD Index
PRD Modules
Functional Requirements
Architecture
Epics
Stories
UI/UX
Decision Ledger
Brownfield Reality Map
Implementation / Handoff Packet
Review Record
```

## Non-negotiable CAE rules

- Do not erase historical lineage.
- Do not silently replace inherited concepts.
- Do not treat file existence as proof.
- Do not treat green tests as proof without reality contact.
- Do not ask the operator a question that repository/document research can resolve.
- Ask one CAE Grill question at a time.
- Preserve unresolved contradictions until a decision resolves them.
- Move down the engineering operating levels when evidence or understanding is weak.
- Move up when repetition, understanding, and evidence justify leverage.
- Product definition and runtime implementation are separate truth surfaces.
- Programs/Workflows/Agents/Skills/Harnesses/Session/Runtime remain CAE execution primitives; CAE-BMAD does not duplicate them.

## External lineage

- BMAD-METHOD: https://github.com/bmad-code-org/BMAD-METHOD
- CAE BMAD fork: https://github.com/Remjohn/BMAD-METHOD
- grill-with-docs: https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs
- SSSF: https://github.com/disler/super-simple-software-factory


## Important: Method Rebuild Mandates

This edition includes `gemini_execution/`, containing twelve mandatory Gemini mandates.

These mandates are the mechanism for rebuilding the method itself.

The target is not just a collection of documents. The target is a usable agentic method with real routing across:

```text
PRODUCT / INTENT ↔ DOCUMENTATION ↔ PLAN ↔ AGENT ↔ AI WORKFLOW / FACTORY
↕
REPOSITORY ↔ APPLICATION ↔ SCRIPT / CLI ↔ DATABASE / TABLE
↕
MODULE / DIRECTORY ↔ FILE / TYPE / CLASS ↔ FUNCTION ↔ LINE / BLOCK
```

The missing codebase/implementation layer must be visible throughout the method. Every product artifact must eventually be reconcilable against implementation reality.

### Execute the rebuild

Start with:

```text
gemini_execution/mandates/M01_*.md
```

and use the corresponding:

```text
gemini_execution/prompts/GEMINI_M01_ACTIVATION_PROMPT.md
gemini_execution/gates/OPERATOR_GATE_M01.md
```

Advance only after the operator gate is passed.

The twelve mandates create and wire the actual CAE-BMAD agents rather than merely documenting that they should exist.
