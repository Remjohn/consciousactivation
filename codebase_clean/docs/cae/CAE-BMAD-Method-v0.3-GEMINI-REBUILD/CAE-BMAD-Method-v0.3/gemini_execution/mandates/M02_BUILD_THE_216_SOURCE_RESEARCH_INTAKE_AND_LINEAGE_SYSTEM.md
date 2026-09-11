# M02 — Build the 216-Source Research Intake and Lineage System

## 1. Assignment

Turn the research library into a governed, scored, lineage-aware corpus that feeds the method without flattening historical sources.

This mandate REBUILDS part of the CAE-BMAD method. It is not a product-feature implementation mandate unless an implementation is required to make the method executable.

The final method must preserve the bidirectional engineering operating model:

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

## 2. Authority

Primary authority:
- CAE-BMAD rebuild program
- CAE method specification
- CAE Research Protocol
- CAE Grill Protocol
- Operating-Level Framework
- current CAE repository and its actual implementation
- original BMAD fork where equivalence is explicitly required
- CCP documentation where lineage is required

The Gemini agent is an execution worker, not the constitutional owner of unresolved product decisions.

## 3. Mandatory reading

Before editing or generating anything, read:

- `docs/gemini_rebuild/README.md`
- `docs/gemini_rebuild/ORIGINAL_BMAD_EQUIVALENCE_AND_EXTRACTION.md`
- `gemini_execution/agents/AGENT_REGISTRY.md`
- all upstream CAE method files relevant to this mandate
- the existing CAE Research Library
- relevant original BMAD surfaces in `Remjohn/BMAD-METHOD`
- relevant current CAE repository files
- prior mandate outputs and the execution ledger

When a referenced source cannot be accessed, record the access failure. Do not substitute a summary and label it read.

## 4. Scope

The mandate may:
- inspect repository files
- inspect existing CAE method files
- compare original BMAD structures
- create or update CAE-BMAD method files
- create agent specifications and skills
- create schemas and validators
- create tests for method behavior
- create traceability records
- create activation prompts
- create operator gate documents
- create migration/compatibility notes

The mandate must not:
- silently redefine CAE product identity
- delete historical lineage
- canonize an unverified concept
- mark an implementation complete because a file exists
- treat a test that does not touch the relevant runtime/data surface as proof
- silently replace CAE runtime primitives with generic BMAD machinery
- ask the operator questions that repository/document evidence can answer
- write a future-state architecture as if it were current truth

## 5. Required agent roles

Use the smallest set of agents needed.

At minimum consult or invoke, where applicable:
- `cae-method-orchestrator`
- one relevant operating-level analyst
- `cae-brownfield-auditor`
- `cae-adversarial-reviewer`

Specialized agents must be used when their operating level is involved.

## 6. Required execution pattern

### Step 1 — Establish current truth

List:
- relevant files
- relevant BMAD equivalent surfaces
- current CAE method artifacts
- current implementation status
- existing tests
- existing missing/partial behavior

### Step 2 — Select operating levels

State:
- initial level
- minimum required descent
- why descent is required
- stop condition for descent
- ascent condition

### Step 3 — Construct the change

Do not write generic prose. Create the actual method artifacts.

Where an original BMAD artifact has an equivalent requirement, document:
- original surface
- capability
- CAE adaptation
- deletion/exclusion if not applicable
- resulting CAE file
- agent/skill that executes it

### Step 4 — Validate behavior

Run:
- schema checks
- file/reference checks
- workflow routing checks
- prompt/skill loading checks
- repository inspection checks
- negative tests for false-proof behavior

### Step 5 — Evidence

Record exact:
- files created
- files modified
- references
- tests run
- observed outputs
- unresolved gaps

## 7. Evidence and fidelity

Each completed assertion gets one of:

`KNOWN / INHERITED / VERIFIED / PROPOSED / INFERRED / MISSING / CONTRADICTED / DEPRECATED`

A method artifact is not “implemented” if only a Markdown file exists.

A Skill is implemented only when it can be loaded and its execution contract is explicit.

An Agent is implemented only when role, instruction, boundaries, inputs, outputs and routing are defined and loadable.

A Workflow is implemented only when entry/exit conditions, steps, handoffs, artifacts and gates exist.

## 8. False-proof defenses

Every mandate must include:
- a positive test
- a negative/countertest
- a stale-reference test
- a missing-artifact test
- a wrong-level test where applicable
- a forbidden-action test

Examples:

`green test + missing runtime integration = FAIL`

`agent prompt exists + agent not routable = FAIL`

`PRD exists + source lineage missing = FAIL`

`brownfield claim exists + implementation surface uninspected = FAIL`

## 9. Error taxonomy

Use explicit errors such as:

`MANDATE_INPUT_MISSING`
`SOURCE_UNAVAILABLE`
`SOURCE_UNVERIFIED`
`BMAD_EQUIVALENCE_UNRESOLVED`
`AGENT_NOT_ROUTABLE`
`SKILL_NOT_LOADABLE`
`WORKFLOW_UNDER_SPECIFIED`
`TRACEABILITY_BROKEN`
`MISSING_IMPLEMENTATION`
`FALSE_PROOF`
`CONTRADICTION_UNRESOLVED`
`OPERATOR_DECISION_REQUIRED`

## 10. Completion criteria

The mandate is complete only when:
1. all required artifacts exist,
2. all required references resolve,
3. all involved agents are routable,
4. all workflows are loadable,
5. negative/countertests pass,
6. missing implementation is explicitly recorded,
7. the operator gate is passed,
8. the execution ledger is updated.

## 11. Rollback

Rollback must remove or quarantine:
- artifacts created by this mandate,
- generated routing entries,
- invalid or superseded agent/skill definitions,
- state entries claiming completion.

Do not delete historical evidence. Mark it superseded or rejected.

## 12. Operator gate

Before promotion, show:
- what changed,
- what was inherited,
- what was rebuilt,
- what is actually executable,
- what remains missing,
- which original BMAD capabilities were retained,
- which were intentionally excluded.

The operator must explicitly approve promotion.

## 13. Activation prompt

Execute this mandate locally in the coding-agent environment.

Read the mandate in full before action.

Do not summarize the task and stop. Inspect the repository and the referenced method surfaces, select the necessary operating levels, build the required artifacts, run the prescribed checks, record evidence, and stop at the operator gate.

Return:
- execution summary
- files created/modified
- tests and countertests
- evidence ledger updates
- missing implementation
- unresolved decisions
- operator gate packet
