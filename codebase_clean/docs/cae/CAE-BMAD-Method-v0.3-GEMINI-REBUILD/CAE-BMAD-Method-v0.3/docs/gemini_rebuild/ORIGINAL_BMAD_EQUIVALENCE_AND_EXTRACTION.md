# Original BMAD Equivalence and Extraction Contract

The CAE method is derived from the Remjohn BMAD fork but is not a complete copy.

Current fork structure verified from GitHub includes:

- `src/core-skills/`
- `src/bmm-skills/`
- `src/bmm-skills/agents/`
- `src/bmm-skills/plan/`
- `src/bmm-skills/ship/`
- `src/core-skills/bmad-help/`
- `src/core-skills/bmad-review/`
- `src/core-skills/bmad-deep-recon/`
- `src/core-skills/bmad-advanced-elicitation/`
- `docs/existing-codebases/`
- `docs/plan/`
- `docs/reference/`

The fork README states that BMAD covers product thinking, architecture, implementation, existing codebases, durable context, specialized perspectives and guided collaboration, and exposes `bmad-build` / `bmad-help`. 

CAE-BMAD must preserve equivalent capability, but rework the entry point around reconstruction and multi-level engineering investigation.

## Mandatory equivalence matrix

| Original capability | CAE-BMAD treatment |
|---|---|
| help/router | keep and CAE-specialize |
| deep recon | keep; becomes repository/product reconstruction |
| advanced elicitation | keep selectively; CAE Grill is stronger gate |
| review | keep; add evidence/lineage checks |
| product/PRD planning | keep |
| architecture planning | keep |
| epics/stories | keep |
| UX | keep |
| implementation/ship | keep as handoff, not duplicate CAE runtime |
| generic brainstorming | optional / non-default |
| party mode | optional / non-default |
| full generic module ecosystem | do not import wholesale |

The rebuild mandates must create **actual equivalent CAE agents and workflows**, not merely documents describing them.
