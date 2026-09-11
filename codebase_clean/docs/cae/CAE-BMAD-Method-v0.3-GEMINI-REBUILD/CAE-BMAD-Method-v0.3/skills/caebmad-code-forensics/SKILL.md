---
name: caebmad-code-forensics
description: Performs deep AST parsing, type signature extraction, line-by-line verification, and pytest evidence collection across Levels 11, 12, and 13.
version: 0.3.0-rebuild
agent: cae-code-forensics-analyst
---

# Skill: caebmad-code-forensics

## 1. Purpose & Invocation
The `caebmad-code-forensics` skill enables the `cae-code-forensics-analyst` to inspect exact classes, functions, and lines of code at `Levels 11-13` to provide empirical proof.

## 2. Invocation Preconditions
1. Python files accessible in workspace.
2. Python AST parser and pytest available.
3. Schema `schemas/code_forensics_report.schema.json` loaded.

## 3. Execution Logic
1. **AST Class & Function Inspection:** Parse Python source files into AST trees to extract classes, methods, and functions.
2. **Signature Extraction:** Extract parameter signatures, type annotations, and docstrings.
3. **Line-Level Proof Extraction:** Record verbatim code snippets with exact line number ranges.
4. **Report Assembly:** Emit `docs/cae-bmad/07_brownfield/CODE_FORENSICS_REPORT.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/07_brownfield/CODE_FORENSICS_REPORT.json`
- `docs/cae-bmad/07_brownfield/CODE_FORENSICS_REPORT.md`
