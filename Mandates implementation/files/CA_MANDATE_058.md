# CAE Mandate CA-M058 — Supabase Connection, Interview-Composer Docker Registration, and Operator Console Route Operability

**Mandate ID:** `CA-M058`
**Wave:** `08`
**Status:** `EXECUTION READY — bounded implementation mandate`
**Canonical question:** `Q57 / INV-PROD-001` (production operability precondition)
**Governing invariant:** `INV-PROD-001` — production authorization dynamically attests `true` only when the full runtime is reachable, not partially missing
**Collision primitive:** `COSTLY EXPOSURE`
**Prepared:** 2026-09-07

---

## 1. Identity and status

This mandate is not one of the 57 canonical questions. It is a **precondition blocker mandate**: five specific implementation gaps, confirmed absent from CA-M001 through CA-M057 by exhaustive search of all seven wave bundles, that together prevent the application from starting or being reached in a browser when the stack is run with Supabase as the database backend.

The five gaps are:

| Gap ID | Surface | What is missing |
|---|---|---|
| `GAP-A` | `infra/docker/docker-compose.yml` | `CAE_SUPABASE_DATABASE_URL` env var absent from `api` service |
| `GAP-B` | `infra/docker/dockerfile.api` | `services/interview-composer` absent from COPY and pip install |
| `GAP-C` | `apps/web/src/components/layout/Sidebar.tsx` | No nav link to `/operator` |
| `GAP-D` | `apps/web/src/routes/operator/index.tsx` | `workspaceId` hardcoded as `"ws-default"` instead of reading from `WorkspaceContext` |
| `GAP-E` | Repo root | No `.env.example` documenting `CAE_SUPABASE_DATABASE_URL` for contributors |

None of these gaps were created by this mandate author. Each was verified against the actual repository files extracted from `clean_codebase.zip` on 2026-09-07. None appear in any prior mandate's scope, allowed file boundary, required work section, or completion predicate.

This mandate is a **bounded execution contract**. It authorizes exactly these five changes and nothing else. It does not reopen any prior canonical decision, does not alter the runtime state machine, schema, receipts, or authority model, and does not implement any new feature. Its completion predicate is that all five gaps are closed with executable evidence and an Operator decision is received.

### Governing authority distinction

- **Source of meaning:** The architectural constraint that `INV-PROD-001` cannot be satisfied if the API container crashes on startup or the Operator Console is unreachable from the browser.
- **Runtime authority:** The Supabase staging project `evnxdssbxxrsesftdvgx` and its `CAE_SUPABASE_DATABASE_URL` session-pooler connection, the canonical `WorkspaceContext` as the source of `activeWorkspaceId`, and the TanStack Router routeTree as the sole registration mechanism for navigable routes.
- **Change/promotion authority:** The human Operator. This mandate does not self-promote. The executor cannot declare the gaps closed without the Operator decision in Section 12.

---

## 2. Decision / objective being authorized

Close five confirmed-absent implementation gaps that together block the application from being operated in a browser against the Supabase database backend. The application must be startable via `docker compose up`, reachable at `localhost:3000`, and the Operator Console must be navigable and functional against a real Supabase-backed workspace when this mandate is complete.

The objective is not to improve the application, refactor it, secure it further, or implement any new capability. The objective is to close exactly these five gaps and no others.

---

## 3. Governing doctrine and authority sources

**Authoring authority:**
- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`

**Constitutional authority:**
- `docs/cae/cae_master_57_question_convergence_canon.md` — Q57 / `INV-PROD-001`
- `docs/cae/Architecture.md`
- `docs/cae/UI.md`

**Runtime authority:**
- `infra/docker/docker-compose.yml` — the canonical container composition file
- `infra/docker/dockerfile.api` — the canonical API image build definition
- `apps/web/src/context/WorkspaceContext.tsx` — the canonical source of `activeWorkspaceId`
- `apps/web/src/routes/operator/index.tsx` — the TanStack Router route file for `/operator`
- `apps/web/src/components/layout/Sidebar.tsx` — the canonical navigation surface

**Evidence of gap:**
- `GAP-A`: `infra/docker/docker-compose.yml` lines 10–14 — `CAE_SUPABASE_DATABASE_URL` is absent; `packages/ca_runtime/src/ca_runtime/database.py` line 318 names it as the required env var.
- `GAP-B`: `infra/docker/dockerfile.api` lines 12–17 COPY block and lines 19–28 pip install block — `services/interview-composer` is absent; `api/main.py` line 100 imports `conscious_activations_interview_composer.application` unconditionally.
- `GAP-C`: `apps/web/src/components/layout/Sidebar.tsx` lines 3–8 — NAV_ITEMS has no entry for `/operator`.
- `GAP-D`: `apps/web/src/routes/operator/index.tsx` line 10 — `workspaceId="ws-default"` is hardcoded.
- `GAP-E`: No `.env.example` exists at the repository root documenting `CAE_SUPABASE_DATABASE_URL`.

---

## 4. Mandatory reading before action

The executor SHALL read each of these before editing any file:

1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
2. `infra/docker/docker-compose.yml` — full file
3. `infra/docker/dockerfile.api` — full file
4. `api/main.py` — lines 95–150 (service initialization and router registration block)
5. `packages/ca_runtime/src/ca_runtime/database.py` — lines 315–370 (`get_staging_postgres_connection`, `STAGING_DATABASE_ENV_VAR`, `STAGING_PROJECT_REF`)
6. `apps/web/src/context/WorkspaceContext.tsx` — full file (understand `activeWorkspaceId`, `useWorkspace` hook export)
7. `apps/web/src/routes/operator/index.tsx` — full file
8. `apps/web/src/components/layout/Sidebar.tsx` — full file
9. `.gitignore` at repo root — confirm `.env` is listed

Reading is not authorization to modify. Only Section 6 grants file authority.

---

## 5. Exact scope

**Objective:** Close GAP-A through GAP-E.

**Dependencies:** None from prior mandates. This mandate has no runtime state machine, schema, receipt, or migration dependency. All changes are to configuration files, a Dockerfile, and two frontend source files.

**Allowed files (complete list — no other file may be touched):**
- `infra/docker/docker-compose.yml`
- `infra/docker/dockerfile.api`
- `apps/web/src/components/layout/Sidebar.tsx`
- `apps/web/src/routes/operator/index.tsx`
- `.env.example` (new file at repo root)
- `.gitignore` (only if `.env` is not already listed — add it if absent, touch nothing else)

**Inputs:**
- Current files at the paths above as they exist in the repository.
- The Supabase connection URL pattern: `postgresql://postgres.<project_ref>:<password>@aws-1-eu-west-1.pooler.supabase.com:5432/postgres`
- The `useWorkspace` hook exported from `apps/web/src/context/WorkspaceContext.tsx`

**Outputs:**
- Modified `docker-compose.yml` with `CAE_SUPABASE_DATABASE_URL` in the `api` service environment block (value sourced from `.env` file, not hardcoded)
- Modified `dockerfile.api` with `services/interview-composer` in both COPY and pip install blocks
- Modified `Sidebar.tsx` with `/operator` nav item added to `NAV_ITEMS`
- Modified `operator/index.tsx` with `workspaceId` sourced from `useWorkspace().activeWorkspaceId`
- New `.env.example` at repo root with placeholder value for `CAE_SUPABASE_DATABASE_URL`

**Operators allowed:** The human Operator/Commander only.

**Validators required:** See Section 9.

**Stop condition:** All five gaps closed with evidence, no prohibited file changed, Operator decision requested.

---

## 6. Allowed artifacts and file boundary

The allowed change surface is exactly the five files listed in Section 5 plus `.env.example` (new) and `.gitignore` (only if `.env` is not already listed). No other file may be created or modified.

Specifically prohibited from being touched by this mandate:
- Any file in `packages/ca_runtime/`
- Any file in `api/routers/`
- Any file in `api/main.py`
- Any migration file
- Any test file (existing or new)
- Any file in `apps/web/src/` except `Sidebar.tsx` and `routes/operator/index.tsx`
- `apps/web/src/routeTree.gen.ts` — this file is auto-generated by TanStack Router on dev server start; the executor must NOT manually edit it

The TanStack Router routeTree regeneration is a side-effect of running `npm run dev` against the corrected route file, not a manual edit. The mandate is complete when the route file is correct; regeneration is the dev server's responsibility.

---

## 7. Prohibitions and collision procedure

**Prohibitions:**

- Do not hardcode the actual `CAE_SUPABASE_DATABASE_URL` value (the live database password) into any committed file. It goes in `.env` only, which is already listed in `.gitignore`.
- Do not add `CAE_SUPABASE_SECRET_KEY` or any other Supabase credential to `docker-compose.yml` as a hardcoded value. If the API requires the secret key, add it to `.env.example` with a placeholder and reference it via `env_file` or `${VAR}` substitution.
- Do not change the `STAGING_PROJECT_REF` value in `database.py`. That constant is outside this mandate's allowed surface.
- Do not add a `useEffect`, new context provider, or new API call to `WorkspaceContext.tsx`. Read the existing `useWorkspace` hook output; do not modify the hook.
- Do not implement workspace auto-creation logic in the route file. `WorkspaceContext` already handles first-login auto-create. The route file must only consume the already-resolved `activeWorkspaceId`.
- Do not add any other nav items to the sidebar beyond `/operator`. Do not reorder existing items.
- Do not refactor the Sidebar component's rendering logic, className strings, or Link usage.
- Do not add loading spinners, error boundaries, or fallback UI to the operator route beyond what is needed to safely handle `activeWorkspaceId` being an empty string while workspace initialization is in progress.

**Collision procedure:**

If the executor encounters any of the following, it must stop before making the conflicting change:
1. A collision between the `services/interview-composer` package name and the actual installable package name (e.g., the `pyproject.toml` inside `services/interview-composer/` may declare a different distribution name). The executor must read `services/interview-composer/pyproject.toml` before writing the Dockerfile. Use the `name` field from `[project]` or `[tool.poetry]` as the pip install target, not the directory name.
2. A missing or empty `services/interview-composer/` directory. If the directory does not exist in the repository, stop, record the blocker, and do not invent a placeholder.
3. A `useWorkspace` export not found in `WorkspaceContext.tsx`. If the hook is named differently, use the actual export name and record the mapping.

In each case: stop, identify the controlling source, record the collision, do not resolve it by widening scope.

### Contrastive failure — the good-looking but wrong result

A passing-looking result that hardcodes the real Supabase password in `docker-compose.yml`, manually edits `routeTree.gen.ts` instead of fixing the route file, adds a new workspace fetch call inside the route component instead of reading `WorkspaceContext`, or copies `services/interview-composer` into the Dockerfile under a wrong distribution name is not completion. It may appear to work initially but will either expose credentials, break on routeTree regeneration, duplicate workspace API calls causing race conditions, or fail to install the correct package. Each of those outcomes violates the mandate's constraint against inventing upstream meaning.

---

## 8. Required work / implementation behavior

Execute in this exact order. Do not parallelize. Each step must be verified before moving to the next.

**Step 1 — Read `services/interview-composer/pyproject.toml`**

Before touching the Dockerfile, read `services/interview-composer/pyproject.toml` (or `setup.cfg` / `setup.py` if `pyproject.toml` is absent). Extract the exact distribution name from the `[project] name` field (or `[tool.poetry] name`). Record it. This is the value that goes in the `pip install` line, not the directory name.

State transition:
```
source state: Dockerfile does not COPY or install services/interview-composer
→ operation: add COPY and pip install using verified distribution name
→ target state: Dockerfile COPYs services/interview-composer and pip installs it by correct distribution name
```

**Step 2 — Update `infra/docker/dockerfile.api`**

Add `COPY services/interview-composer services/interview-composer` after the last existing `COPY services/...` line (currently line 17, after `COPY services/vae services/vae`).

Add the distribution name (from Step 1) to the `pip install --no-cache-dir` block after `services/vae \`.

Do not change any other line in the Dockerfile.

**Step 3 — Update `infra/docker/docker-compose.yml`**

Add `CAE_SUPABASE_DATABASE_URL` to the `environment` block of the `api` service using `${CAE_SUPABASE_DATABASE_URL}` substitution syntax (Docker Compose reads this from the `.env` file at the repo root automatically when it is listed there).

The result must look like:
```yaml
    environment:
      CA_DATA_ROOT: /state
      CA_MEDIA_ROOT: /media
      CA_DELEGATION_ROOT: /app/packages/ca_delegation_rc4
      CA_STUDIO_RPC_ENTRYPOINT: /app/services/studio/dist/rpc.js
      CAE_SUPABASE_DATABASE_URL: ${CAE_SUPABASE_DATABASE_URL}
```

Do not add any other environment variable. Do not change the `web` service.

**Step 4 — Create `.env.example` at repo root**

Create a new file `.env.example` at the repository root with exactly this content (no real credentials):

```
# Supabase session-pooler connection URL.
# Format: postgresql://postgres.<project_ref>:<password>@aws-0-eu-west-1.pooler.supabase.com:5432/postgres
# Required: the API container will refuse to start without this value.
CAE_SUPABASE_DATABASE_URL=postgresql://postgres.<project_ref>:<password>@aws-0-eu-west-1.pooler.supabase.com:5432/postgres
```

Then confirm `.env` is present in `.gitignore`. If it is already there (confirmed in Step pre-check), record that as evidence. If it is absent, add `.env` on its own line and record the change.

**Step 5 — Fix `apps/web/src/routes/operator/index.tsx`**

Read `apps/web/src/context/WorkspaceContext.tsx` and identify the name of the exported hook that exposes `activeWorkspaceId`. In the current codebase this is `useWorkspace` returning `{ activeWorkspaceId, ... }`.

Change line 10 of `routes/operator/index.tsx` from:
```tsx
  component: () => <ProgramOperatorConsole workspaceId="ws-default" />,
```
to a component that reads from context:
```tsx
  component: OperatorRoute,
```

And add above the route definition:
```tsx
import { useWorkspace } from "../../context/WorkspaceContext";

function OperatorRoute() {
  const { activeWorkspaceId } = useWorkspace();
  return <ProgramOperatorConsole workspaceId={activeWorkspaceId ?? ""} />;
}
```

Do not change any other line in the route file. Do not add loading state, error boundary, or redirect logic beyond this.

**Step 6 — Add nav link in `apps/web/src/components/layout/Sidebar.tsx`**

Add `{ to: "/operator", label: "Program Operator" }` as the last item in `NAV_ITEMS`:

```tsx
const NAV_ITEMS = [
  { to: "/workspace", label: "Workspace" },
  { to: "/interviews/compose", label: "Interview Composer" },
  { to: "/campaigns", label: "Campaigns" },
  { to: "/campaigns/new", label: "New Campaign" },
  { to: "/harnesses", label: "Harnesses" },
  { to: "/operator", label: "Program Operator" },
] as const;
```

Do not change anything else in this file.

---

## 9. Verification and evidence standard

All six verifiers below are required. A green result on a verifier that does not measure what it claims does not constitute completion.

**V1 — Docker build passes (GAP-B)**
- What it measures: The API image builds without error after the interview-composer addition.
- Command: `docker compose -f infra/docker/docker-compose.yml build api`
- Expected: exit code 0, no `ModuleNotFoundError` or pip resolution failure.
- Does not measure: Whether the API starts or the Supabase connection works.
- False-proof countercase: A build that succeeds because the `pip install` line uses a wrong package name that happens to be a different valid package. Mitigate: confirm the installed package provides `conscious_activations_interview_composer.application` by checking `pip show <distribution-name>` inside a throwaway container shell.
- Evidence locator: Terminal output of `docker compose build api` showing exit 0.

**V2 — API starts and health endpoint responds (GAP-A + GAP-B)**
- What it measures: The API container starts with `CAE_SUPABASE_DATABASE_URL` set and returns 200 from `GET /api/health`.
- Command: `docker compose up api` with `.env` at repo root containing the real URL; then `curl -s localhost:8000/api/health`.
- Expected: HTTP 200, JSON body does not contain `"status": "error"` at the top level.
- Does not measure: Whether every sub-service is fully healthy; only that the container starts and health responds.
- False-proof countercase: Health returns 200 but the workspace router is still broken because `CAE_SUPABASE_DATABASE_URL` was not passed through correctly. Mitigate: also call `GET /api/v1/workspaces` with `X-Actor-Id: dev-operator-local` and confirm it returns 200 or 404 (not 500).
- Evidence locator: `curl` output showing 200 from `/api/health` and non-500 from `/api/v1/workspaces`.
- Environment fidelity: Must run inside Docker, not a bare `uvicorn` invocation, because the Dockerfile change is what is being verified.
- Operator validation required: Yes — the Operator must confirm the `.env` file at repo root contains the real `CAE_SUPABASE_DATABASE_URL` before this verifier can run.

**V3 — Operator Console route is navigable (GAP-C + GAP-D)**
- What it measures: A browser opened to `localhost:3000` shows "Program Operator" in the sidebar, clicking it renders `ProgramOperatorConsole` without a crash, and the network tab shows API calls going to `/api/programs` with a real workspace UUID (not `ws-default`) in the request body or query.
- Steps: `npm run dev` in `apps/web`, open browser, observe sidebar, click "Program Operator", inspect network calls.
- Expected: Component renders; no `workspace_id: "ws-default"` appears in any network request.
- Does not measure: Whether the program list API returns data (that depends on Supabase having data).
- False-proof countercase: The sidebar link appears but clicking it returns a 404 route because `routeTree.gen.ts` was not regenerated. Mitigate: confirm `npm run dev` was restarted after the route file change, which triggers TanStack Router's Vite plugin to regenerate the tree. The executor must not manually edit `routeTree.gen.ts`.
- Evidence locator: Browser screenshot or description of the rendered route; `routeTree.gen.ts` grep for `/operator` after dev server restart.
- Human validation required: Yes — the Operator must visually confirm the sidebar link and the rendered console.

**V4 — No credentials committed (GAP-E)**
- What it measures: `.env` is in `.gitignore` and `.env.example` contains only placeholder values.
- Commands:
  - `grep "^\.env$" .gitignore` → must return a match
  - `grep -E "Mitano|postgres\." .env.example` → must return empty (no real password or project ref)
- Does not measure: Whether the credentials have already been rotated after the prior exposure in `.env`. That is a separate Operator action.
- Evidence locator: Terminal output of both grep commands.

**V5 — interview-composer package name verified (GAP-B, Step 1)**
- What it measures: The distribution name used in the Dockerfile `pip install` line matches the `[project] name` in `services/interview-composer/pyproject.toml`.
- Command: `grep "^name" services/interview-composer/pyproject.toml` and compare with the Dockerfile pip install line.
- Evidence locator: Output of grep command and the Dockerfile line, side by side in the completion report.

**V6 — No prohibited file changed**
- What it measures: Git diff touches only the six allowed files.
- Command: `git diff --name-only HEAD`
- Expected: Output contains only the allowed file paths and no others.
- Evidence locator: Terminal output of `git diff --name-only HEAD`.

---

## 10. Completion and stop condition

Stop when all six verifiers in Section 9 produce the declared evidence, no prohibited file is in the diff, and the completion report is assembled. The executor must not begin any work beyond these five gaps. It must not implement new features, refactor adjacent code, add loading states, add error boundaries, update other environment variables, or start any subsequent mandate.

Completion requires:
1. All six verifiers pass with evidence as described.
2. The completion report lists every changed file, the exact diff for each, and the evidence output for each verifier.
3. Residual limitations are recorded (see below).
4. The exact commit SHA is captured.
5. The Operator decision is explicitly requested.

**Residual limitations to record in the completion report:**
- `routeTree.gen.ts` regeneration is a dev-server side-effect and cannot be verified without running `npm run dev`. If the executor is running in a non-browser environment, it must record that V3 partial evidence (network call inspection) requires Operator manual verification in the browser.
- The Supabase credential rotation (the `.env` file was previously committed with live credentials) is outside this mandate's scope. The executor must record this as a separate required Operator action and must not rotate keys or change the Supabase project configuration.
- If `services/interview-composer/` is absent from the repository, the executor must stop at Step 1 and record this as a blocking dependency. CA-M058 cannot be marked complete in that condition.

---

## 11. Rollback / recovery

**GAP-A (docker-compose):** Revert by removing the `CAE_SUPABASE_DATABASE_URL: ${CAE_SUPABASE_DATABASE_URL}` line from the environment block. No data is mutated; this is a configuration-only change.

**GAP-B (Dockerfile):** Revert by removing the added `COPY` line and the distribution name from the `pip install` block. Rebuild the image. No running containers are affected until the image is rebuilt and redeployed.

**GAP-C (Sidebar):** Revert by removing the `/operator` entry from `NAV_ITEMS`. No state is affected.

**GAP-D (operator route):** Revert by restoring `component: () => <ProgramOperatorConsole workspaceId="ws-default" />,` and removing the `OperatorRoute` function and `useWorkspace` import. No state is affected.

**GAP-E (.env.example):** Delete the file. Add `.env.example` to `.gitignore` if deletion alone is insufficient.

None of these rollbacks require a database migration, state machine change, or receipt issuance.

---

## 12. Operator decision

The Operator must approve or reject CA-M058 based on whether all six verifiers produce the declared evidence, no prohibited file was changed, and the completion report is complete.

The executor must not infer approval from the absence of errors or from any prior Operator statement. The Operator must receive a completion report containing:
- list of changed files with exact diffs
- terminal output for each verifier
- browser evidence for V3 (screenshot or Operator self-verification instruction)
- the exact commit SHA
- recorded residual limitations
- the explicit approval/rejection question: **"Do you approve CA-M058?"**

The executor must not proceed to any other work until the Operator responds.

---

## 13. Activation prompt (200–300 words)

> You are executing CAE mandate `CA-M058` only. Before editing anything, read in full: `01_CA_MANDATE_AUTHORING_PROTOCOL.md`; `infra/docker/docker-compose.yml`; `infra/docker/dockerfile.api`; `api/main.py` lines 95–150; `packages/ca_runtime/src/ca_runtime/database.py` lines 315–370; `apps/web/src/context/WorkspaceContext.tsx`; `apps/web/src/routes/operator/index.tsx`; `apps/web/src/components/layout/Sidebar.tsx`; and `.gitignore`.
>
> Your authorized scope is exactly five file changes: add `CAE_SUPABASE_DATABASE_URL: ${CAE_SUPABASE_DATABASE_URL}` to the `api` service environment block in `docker-compose.yml`; add `services/interview-composer` to the COPY and pip install blocks in `dockerfile.api` using the distribution name from `services/interview-composer/pyproject.toml`; add `{ to: "/operator", label: "Program Operator" }` as the last item in `NAV_ITEMS` in `Sidebar.tsx`; replace the hardcoded `workspaceId="ws-default"` in `routes/operator/index.tsx` with a component that reads `activeWorkspaceId` from `useWorkspace()`; and create `.env.example` at repo root with a placeholder `CAE_SUPABASE_DATABASE_URL` value.
>
> Do not touch any other file. Do not edit `routeTree.gen.ts` manually — it regenerates on `npm run dev`. Do not hardcode any real credential. Do not rotate Supabase keys. Do not add loading states, error boundaries, or new API calls. If `services/interview-composer/` does not exist, stop and report the blocker.
>
> Execute in the order of Steps 1–6 in Section 8. After all steps, run all six verifiers in Section 9 and assemble the completion report with changed files, diffs, verifier outputs, commit SHA, and residual limitations. Then stop and request the Operator decision: **"Do you approve CA-M058?"**
