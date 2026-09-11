# Phase 2 — Agent Package Compilation Contract

Eve-like packaging is the authoring convention; Pi is the runtime; CAE is the authority.

## Package
agent/
    CAE.md
    AGENTS.md                 # project/agent operating guidance where the repository uses it
    instructions.md
    skills/<skill>/SKILL.md
    subagents/<agent>/...
    tools/
    connections/
    hooks/
    extensions/
    evals/

## Context precedence
CAE constitutions > operator authorization > Program/Harness policy > local CAE.md/AGENTS.md > agent instructions > Skill content.

The implementation must reconcile the repository's existing AGENTS.md conventions before adding another local control file.

## Compilation
- resolve references;
- validate Skill maturity/hash;
- resolve subagent packages;
- resolve capability projections;
- resolve hooks/extensions;
- bind workspace and lane;
- emit deterministic package manifest;
- fail closed on missing/ambiguous authority or capability.

Filesystem contents are not canonical CAE state.
