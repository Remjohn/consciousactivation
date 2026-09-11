# CAE-BMAD Method Rebuild Program

This bundle is a **method rebuild program**, not an application workflow.

Gemini is authorized to use the twelve mandates in `gemini_execution/mandates/` to rebuild the CAE-BMAD method itself.

The mandates are ordered but evidence may require revisiting earlier work.

## Rebuild target

The rebuilt method must be able to understand and operate deliberately across this engineering stack:

```text
PRODUCT / INTENT
        ↕
DOCUMENTATION
        ↕
PLAN
        ↕
AGENT
        ↕
AI WORKFLOW / FACTORY
        ↕
REPOSITORY
        ↕
APPLICATION
        ↕
SCRIPT / CLI
        ↕
DATABASE / TABLE
        ↕
MODULE / DIRECTORY
        ↕
FILE / TYPE / CLASS
        ↕
FUNCTION
        ↕
LINE / BLOCK
```

The arrows are intentionally bidirectional. A higher-level statement may need to be explained by a lower-level implementation fact, while repeated lower-level behavior may justify a higher-level abstraction.

## Hard requirement

The rebuilt method must not leave the missing implementation layer implicit.

For every product capability it studies, it must record:

- desired behavior
- documented behavior
- planned behavior
- existing implementation
- missing implementation
- duplicated implementation
- conflicting implementation
- unverified implementation
- proof status
- next action

## Required artifact families

1. Research corpus
2. Product reconstruction
3. Operating-level assessment
4. Decision/Grill system
5. Product Brief
6. PRD Index
7. PRD Modules
8. Functional Requirements
9. Architecture
10. Epics
11. Stories
12. UI/UX
13. Brownfield Reality Map
14. Implementation Handoff
15. Review and evolution records

## Required CAE-specific capabilities

The method must preserve and expose:

- CCP lineage
- CCF lineage
- CMF lineage
- Atomic Harnesses
- Visual Syntax
- Primitive systems
- Research/audit systems
- Programs
- Skills
- Harnesses
- Agents
- Sessions
- Workflows
- Runtime
- Evidence
- Receipts
- Operator decisions

Do not reduce these to generic "features".
