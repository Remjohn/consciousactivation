---
name: caebmad-cli-investigate
description: Audits executable scripts, CLI command suites, argument parser contracts, and execution exit codes at Level 08.
version: 0.3.0-rebuild
agent: cae-cli-script-analyst
---

# Skill: caebmad-cli-investigate

## 1. Purpose & Invocation
The `caebmad-cli-investigate` skill enables the `cae-cli-script-analyst` to audit executable scripts, test CLI suites, and verify argument parsing contracts at `Level 08: SCRIPT / CLI`.

## 2. Invocation Preconditions
1. Script directories (`scripts/`, `tools/`) accessible.
2. Console script entrypoints in `pyproject.toml` readable.
3. Schema `schemas/command_control_map.schema.json` loaded.

## 3. Execution Logic
1. **Script Cataloging:** Scan `scripts/` and `tools/` for Python, Bash, and PowerShell scripts.
2. **Execution Test Check:** Verify syntax and parameter parsing for administrative CLI utilities.
3. **CLI Entrypoint Extraction:** Map console scripts to Python callable symbols.
4. **Executable Verification:** Flag scripts as verified executable only when tested or syntax-checked.
5. **Map Assembly:** Emit `docs/cae-bmad/07_brownfield/COMMAND_CONTROL_MAP.json` and `.md`.

## 4. Output Contract
- `docs/cae-bmad/07_brownfield/COMMAND_CONTROL_MAP.json`
- `docs/cae-bmad/07_brownfield/COMMAND_CONTROL_MAP.md`
