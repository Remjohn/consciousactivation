# Bundle Manifest

## Phase allocation

| Phase | Mandates | Focus | Required close |
|---|---:|---|---|
| 1 | 1–12 | Truth, inventory, contracts, Program model, state/runtime design | M12 |
| 2 | 13–24 | Pi runtime, Harnesses, Agents, Skills, Hooks, State execution | M24 |
| 3 | 25–36 | Research/KB, Workspace/Guest, Audience, Collision, Interview, Evidence→Editorial | M36 |
| 4 | 37–48 | Editorial→Production, visual/video, operator UI, E2E pilot, hardening | M48 |

## Mandatory close behavior

M12, M24, M36 and M48 MUST:
1. verify the phase evidence ledger;
2. reconcile code/spec/PRD status;
3. update the relevant `docs/PRD/CURRENT.md` sections in the same execution session;
4. update the phase control-state record;
5. record the exact commit SHA;
6. request operator acceptance or identify a blocking decision;
7. STOP.

## No silent architectural invention

The current repository already contains a substantial workflow kernel, Harness authoring
machinery, typed state/receipt system, Editorial Intelligence object model and 49-harness
Stage 1/2 visual evidence. The production program must connect these systems before
creating replacements.

## Success language

`DOCUMENTED` != `CODE_EXISTS` != `TEST_VERIFIED` != `RUNTIME_VERIFIED` != `OPERATOR_ACCEPTED`.

Only the latter three may support implementation/production claims.
