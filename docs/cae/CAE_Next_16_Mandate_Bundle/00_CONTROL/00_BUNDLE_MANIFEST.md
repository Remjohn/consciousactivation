# CAE Next 16 Mandate Bundle

## Purpose

This bundle is the next governed execution wave after M01–M48. It is deliberately centered on the **Agent execution seam + Workflow Engineering + Software Development Life Cycle (SDLC) Factory + operator observability**.

## Phase allocation

| Phase | Mandates | Focus | Close |
|---|---:|---|---|
| 5 | M49–M52 | Agent object, package, portable context, AgentInvocation | M52 |
| 6 | M53–M56 | Program/Agent binding, typed results/gates, repair, standalone sessions | M56 |
| 7 | M57–M60 | Workflow primitives, IR, control-flow compiler, Step Contracts | M60 |
| 8 | M61–M64 | SDLC factory, isolation, operator commands/observability, certification | M64 |

## Mandatory close behavior

M52, M56, M60 and M64 MUST:
1. verify the phase evidence ledger;
2. reconcile implementation/spec/PRD status;
3. update `docs/PRD/CURRENT.md` in the same execution session;
4. update affected local current-state files where applicable;
5. record exact commit SHA;
6. record operator acceptance or explicit blocker;
7. STOP.

## Core doctrine

- Program is an operator-addressable unit of supervised work.
- Agent is a reusable reasoning object; Program assigns Agents to workflow steps.
- Skill is a passive reusable capability; no Skill invokes another Skill.
- Hook is deterministic event enforcement/observation.
- Harness provides execution guarantees.
- Workflow is executable control flow, not merely prose.
- Code owns deterministic sequencing, conditions, loops, validation and persistence where appropriate.
- Agents operate inside bounded steps and cannot redefine canonical authority.
- Typed handoffs and receipts are mandatory evidence boundaries.
- `CAE.md` is portable local governance/context and inherits from higher authority; it is never a parallel Civil Code.

## SSSF adoption rule

SSSF is a reference implementation of the agents-plus-code software factory pattern. Adopt its **execution principles**—explicit agent roster, code-owned workflow, typed handoffs, gates, same-session repair, traceability, operator-friendly commands—without replacing CAE's domain, constitutional, state, evidence or authority architecture.
