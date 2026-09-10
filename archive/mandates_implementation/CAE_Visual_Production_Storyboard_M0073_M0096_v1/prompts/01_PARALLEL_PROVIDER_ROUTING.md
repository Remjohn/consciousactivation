# Parallel Provider Routing

## Recommended allocation

### Claude
M0073, M0074, M0078, M0081, M0083, M0084, M0086, M0089, M0090, M0092

Best for structured contracts, evidence matrices, grammar/calculus, vision contracts and narrow domain components.

### ChatGPT
M0075, M0077, M0079, M0082, M0085, M0087, M0091, M0093, M0094, M0096

Best for broad repository inspection, UI integration, component assembly-facing work and final certification narrative.

### Grok
M0076, M0088, M0095

Use for exploratory external-repo inspection, Visual Chat design, and the controlled final assembly pass.

## Parallel execution rule

Only mandates in the same declared parallel group may run concurrently. Each concurrent mandate receives the frozen Authority Pack plus only the specific accepted bundles explicitly declared as inputs. They must not write to the same shared canonical files.

M0095 and M0096 are never parallel with any other implementation mandate.
