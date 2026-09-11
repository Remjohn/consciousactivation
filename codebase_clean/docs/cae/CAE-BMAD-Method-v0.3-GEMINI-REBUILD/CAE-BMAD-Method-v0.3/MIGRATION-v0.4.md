# CAE Agent Kernel v0.4 Migration

## Changes
- Every agent becomes a behavioral expert persona.
- Every agent has explicit heuristics, activation, investigation, evidence, uncertainty, quality, boundaries, and handoff.
- Natural-language routing is primary; menus remain discoverability.
- Existing CAE taxonomy and operating levels are preserved.
- Each agent targets 500–700 words of substantive content.

## Adoption
1. Install the kernel.
2. Install the `cae-author-agent` skill and template.
3. Replace the v0.3 registry with the v0.4 registry.
4. Replace/review the 19 agent files.
5. Ensure the runtime loads kernel + agent content on activation.
6. Add the validator gate before publishing agents.
7. Have the adversarial reviewer inspect each agent.
8. Exercise product, analysis, architecture, delivery, and brownfield workflows.

This package is a migration baseline and has not been committed to GitHub.
