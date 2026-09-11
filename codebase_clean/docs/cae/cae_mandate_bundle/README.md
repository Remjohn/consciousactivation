# CAE Editorial Intelligence Mandate Bundle — README

This bundle is the executable-documentation layer for the next CAE development program.

Use one mandate at a time. Do not give Gemini the whole bundle as authorization to implement everything. Give it the selected mandate, the complete referenced authority set, the activation prompt embedded in that mandate, and the current CAE control-state record.

The bundle intentionally separates:

- mandate authoring doctrine;
- mandate execution skill;
- each bounded mandate;
- operator review;
- activation-prompt indexing.

The mandates are not equivalent to Tech Specs. They are the governed bridge that tells the coding agent what it is authorized to do before a PRD/FR/Tech-Spec or implementation stage is allowed to expand.

The editorial pipeline is deliberately split into two major semantic programs:

```text
WORLD → RELATIONAL STATE → COLLISION → INTERVIEW → HUMAN EVIDENCE

HUMAN EVIDENCE → SEGMENT → ATTRIBUTE → CANDIDATE → SCORE/CLUSTER
→ OPERATOR SELECT → ASSET INTELLIGENCE → SEMANTIC PROGRAM → CMF/IR
```

The Operator gate is intentionally retained between machine candidate formation and full production.
