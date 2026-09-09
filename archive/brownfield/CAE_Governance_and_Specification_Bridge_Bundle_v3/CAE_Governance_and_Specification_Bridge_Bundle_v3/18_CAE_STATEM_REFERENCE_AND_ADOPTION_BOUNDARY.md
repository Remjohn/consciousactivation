# CAE StateM Reference & Adoption Boundary v1.0

## 1. Why StateM is relevant

StateM is a recent external example of agent-native execution control built around durable states, phase-local context, checked transitions, recoverable runbooks, and versioned procedural practices. The public repository exposes a CLI state machine with explicit nodes, transition checks, dynamic checks, durable runtime history, and context lifecycle support. urlStateM GitHub repositoryhttps://github.com/henryqin1997/statem

The accompanying paper frames states as context-and-contract boundaries and distinguishes runtime control from reusable runbook/control profiles. urlStateM paper (arXiv:2608.15089)https://arxiv.org/abs/2608.15089

## 2. Adoption decision

CAE should **borrow the control semantics, not copy the storage architecture**.

### Borrow

- explicit phase/state boundaries;
- state-local context refresh;
- checked transitions;
- repair states/routes;
- durable execution history;
- versioned procedural practices;
- dynamic run-local checks with controlled promotion;
- explicit distinction between agent attestation and independent verification;
- stop/handoff semantics;
- failure-driven harness improvement.

### Adapt

- replace local authoritative state with PostgreSQL/Supabase;
- connect transitions to CAE ontology and object IDs;
- connect every consequential transition to receipts/events;
- expose operations through typed semantic APIs;
- add environment-fidelity, reward-hack, taste, and anti-centroid evidence;
- integrate Matrix of Edging, SDA, SFL, Primitive, Edge, and SemanticProgram contracts;
- use existing CAE receipt/memory infrastructure where present.

### Do not adopt automatically

- StateM's local `.statem` state directory as system authority;
- generic workflow states disconnected from CAE ontology;
- any benchmark-specific runbook rule as CAE law;
- any external evaluator convention as semantic truth;
- a universal runbook applied to every CAE mission.

## 3. Implementation relationship

StateM should initially be treated as an engineering reference implementation.

During the implementation phase, the coding agent may:

1. inspect the public repository for implementation patterns;
2. compare its state/transition model against CAE's typed state contracts;
3. selectively port useful runtime concepts where license, dependency, and architectural fit permit;
4. write a CAE-specific adapter rather than importing StateM wholesale unless a formal dependency decision authorizes it;
5. document every borrowed concept and its CAE mapping.

## 4. Required decision record before code reuse

If actual StateM code is reused, create:

```yaml
adoption_id:
source_repo:
source_commit:
license:
source_files:
borrowed_components:
why_borrowed:
cae_adapter_boundary:
cae_modifications:
test_coverage:
security_review:
maintenance_owner:
```

## 5. Evidence boundary

The StateM paper reports strong benchmark improvements but also explicitly discloses raw/adjudication and reward-hacking caveats. CAE should therefore treat the paper as evidence that stateful harness control is promising, not as proof that the exact StateM implementation will improve CAE. citeturn131455academia0

## 6. Core CAE rule

> **StateM may inform CAE execution design; CAE's own ontology, evidence, state model, and contracts remain authoritative.**
