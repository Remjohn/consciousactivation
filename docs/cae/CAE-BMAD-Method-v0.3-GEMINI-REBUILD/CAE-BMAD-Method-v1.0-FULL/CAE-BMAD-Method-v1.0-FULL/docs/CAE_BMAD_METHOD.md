# CAE-BMAD Method

## 1. Why this exists

CAE is not a greenfield product.

Its current form sits on a long chain of product and engineering work:

```text
research
→ audits
→ CCP
→ CCF
→ CMF
→ primitives
→ experience/reaction systems
→ visual syntax
→ Atomic Harnesses
→ questions/interviews
→ CAE architecture
→ Programs
→ runtime
```

A conventional product process that begins by asking for a new Product Brief loses that history.

CAE-BMAD therefore inserts a **reconstruction phase** before the standard product-development artifact chain.

## 2. What is borrowed from BMAD

The following BMAD mechanisms are retained:

- skill-based invocation
- progressive artifacts
- planning depth that fits the task
- explicit handoffs
- document workspaces
- product brief
- PRD
- architecture
- epic/story decomposition
- UX
- implementation readiness
- developer/code review
- sprint and retrospective capabilities
- core help
- deep research
- advanced elicitation
- customization
- review

The current BMAD command/reference documentation explicitly describes `SKILL.md` as the installed interface for agents,
workflows, tasks, and tools and identifies `bmad-product-brief`, `bmad-prd`, `bmad-ux`,
`bmad-architecture`, and `bmad-create-epics-and-stories` as key workflow skills.

## 3. What CAE adds

### 3.1 Product reconstruction

Before rewriting product definition, establish:

- what has historically existed
- why it existed
- what survived
- what changed
- what was abandoned
- what is currently implemented
- what is documented but not implemented
- what is implemented but undocumented
- what is contradictory
- what remains unknown

### 3.2 Operating-level assessment

The engineer and agent choose the level at which to inspect a problem.

Possible levels:

```text
line
block
function
type
class
file
module
directory
database
table
script
CLI
application
repository
product
documentation
plan
agent
AI developer workflow
software factory
```

Move downward when control/understanding is required.

Move upward when leverage/repetition/evidence justify abstraction.

### 3.3 CAE Grill

The Grill is not a brainstorming engine.

It is a decision discipline:

```text
inspect
→ collect evidence
→ identify the unresolved decision
→ recommend
→ ask one question
→ record answer
→ propagate consequences
```

### 3.4 Lineage preservation

A CAE document must identify important inherited concepts.

For example:

```text
Inherited from CCP:
  concept

CCP source:
  exact document

CAE transformation:
  exact current interpretation

Current implementation:
  files/symbols

Status:
  inherited / verified / proposed / deprecated
```

## 4. The artifact chain

```text
Research
→ Reconstruction
→ Operating-Level Assessment
→ Grill
→ Product Brief
→ PRD Index
→ PRD Modules
→ FR
→ Architecture
→ Epics
→ Stories
→ UI/UX
→ Brownfield Reality
→ Handoff
→ Implementation
→ Proof
→ Review
```

## 5. The artifact contracts

### Product Brief

The brief explains what CAE is, whom it serves, the outcomes it creates, the major capabilities,
the boundaries, and the product promise.

### PRD Index

The index routes the PRD modules and records cross-module dependencies.

### PRD Module

A module owns a coherent product boundary and declares sources, requirements, implementation references,
acceptance, and conflicts.

### Functional Requirement

An FR expresses a testable product behavior independently of a specific implementation.

### Architecture

Architecture defines how approved requirements are realized inside the actual brownfield system.

### Epic

An Epic groups product value and delivery work.

### Story

A Story is implementation-ready and traceable to source, module, FR, architecture, repository impact,
acceptance, recovery, and proof.

### UI/UX

UI is derived from approved product behavior and operator journey, not used to invent backend semantics.

### Handoff

Handoff routes approved work into the actual CAE execution surface.

## 6. Truth states

```text
KNOWN
INHERITED
VERIFIED
PROPOSED
INFERRED
MISSING
CONTRADICTED
DEPRECATED
```

No workflow may silently upgrade one state into another.

## 7. Human decision boundary

The agent may recommend.

The operator decides.

The repository may resolve code-level questions.

The research corpus may resolve historical/source questions.

The method should not ask the operator a question that code or documentation can answer.
