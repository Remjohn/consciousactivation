# CAE Harness & Runbook Integration Protocol v1.0

## 1. Purpose

The CAE harness is not merely an instruction dispatcher. It is the procedural execution surface that teaches agents how to operate the canonical ontology, query the authoritative state, invoke legal operations, satisfy transition contracts, and preserve receipts.

## 2. Two-layer control model

Separate:

### Authoritative operational state

Stored in PostgreSQL/Supabase.

### Procedural control artifact

Stored in versioned `Skills.md`, runbooks, reasoning programs, and harness configuration.

This prevents a local runbook from becoming a shadow database while preserving the advantages of explicit state-aware control.

## 3. StateM-inspired runbook structure

The harness MAY use StateM-like concepts:

```yaml
name:
version:
initial_state:
states:
  - state_id
  - context_requirements
  - local_instructions
  - allowed_operations
  - before_transfer_checks
  - recovery_routes
transitions:
  - source
  - target
  - guard
  - required_evidence
  - receipt
```

The CAE runbook does not replace PostgreSQL state. It tells the agent and runtime how to interact with that state.

## 4. Skills.md implication

Each object-specific and procedure-specific skill should teach three things:

1. **Recognition** — what object/state/relationship the agent is dealing with.
2. **Procedure** — which semantic functions and queries are authorized.
3. **Transition discipline** — what evidence/validation must exist before the next state.

## 5. Recommended harness loop

```text
LOAD CURRENT STATE
        ↓
LOAD STATE-LOCAL CONTRACT
        ↓
SCHEMA LINK
        ↓
RETRIEVE AUTHORIZED CONTEXT
        ↓
PLAN
        ↓
EXECUTE SEMANTIC OPERATIONS
        ↓
VALIDATE
        ↓
WRITE EVIDENCE / RECEIPT
        ↓
REQUEST TRANSITION
        ↓
IF FAIL → CLASSIFY ERROR → REPAIR
        ↓
ENTER NEXT STATE
```

## 6. No agentic soup

The harness should preserve one coherent reasoning loop where appropriate. State boundaries are for durable context and consequential contracts, not arbitrary micro-agent decomposition.

Use separate agents only where independence, permission separation, context isolation, or adversarial review provides a material architectural benefit.

## 7. Dynamic checks

The harness may permit run-local checks when discovered from the active task, but:

- they cannot weaken constitutional rules;
- they cannot overwrite canonical schemas;
- they must be persisted as evidence;
- promotion to reusable skill/runbook practice requires review and regression testing.

## 8. Stop handling

The harness must distinguish:

- `COMPLETE`
- `BLOCKED`
- `WAITING`
- `REPAIR_REQUIRED`
- `FAILED`

A generic stop command must not equal successful completion.

## 9. Harness Builder requirements

The future harness/skill builder should generate or validate:

- state bindings;
- semantic operation bindings;
- transition contracts;
- validator bindings;
- receipt requirements;
- typed error recovery routes;
- environment fidelity requirements;
- reward-hack countertests;
- taste/anti-centroid checks.

The builder should treat these as compilation targets, not prose suggestions.
