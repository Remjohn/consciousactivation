# CA-M058 — Agent Handoff: Pre-Executed Bundle

**Mandate ID:** `CA-M058`
**Bundle status:** WORK ALREADY DONE — paste only, do not re-implement
**Prepared:** 2026-09-07

---

## What this bundle is

CA-M058 has already been executed and verified. The five corrected files are in
this bundle. Your only job is to **copy each file to its exact destination path
in the repository**. Do not rewrite, refactor, or improve any of them.

---

## The five changes made and why

| Gap | File changed | What changed |
|-----|-------------|--------------|
| GAP-A | `infra/docker/docker-compose.yml` | Added `CAE_SUPABASE_DATABASE_URL: ${CAE_SUPABASE_DATABASE_URL}` to the `api` service `environment` block. Docker Compose reads this from `.env` at the repo root automatically. |
| GAP-B | `infra/docker/dockerfile.api` | Added `COPY services/interview-composer services/interview-composer` after line 17 and `services/interview-composer \` to the pip install block after `services/interview`. Distribution name confirmed from `services/interview-composer/pyproject.toml`: `conscious-activations-interview-composer`. |
| GAP-C | `apps/web/src/components/layout/Sidebar.tsx` | Added `{ to: "/operator", label: "Program Operator" }` as the last entry in `NAV_ITEMS`. Nothing else changed. |
| GAP-D | `apps/web/src/routes/operator/index.tsx` | Replaced hardcoded `workspaceId="ws-default"` with a named `OperatorRoute` component that reads `activeWorkspaceId` from `useWorkspace()` imported from `WorkspaceContext`. |
| GAP-E | `.env.example` *(new file at repo root)* | Documents `CAE_SUPABASE_DATABASE_URL` with a placeholder value for contributors. `.env` is already in `.gitignore` — confirmed, no change needed to `.gitignore`. |

---

## Exact paste instructions — one action per file

### 1. `infra/docker/dockerfile.api`
Replace the entire existing file with the file at:
`CA_MANDATE_058_BUNDLE/infra/docker/dockerfile.api`

### 2. `infra/docker/docker-compose.yml`
Replace the entire existing file with the file at:
`CA_MANDATE_058_BUNDLE/infra/docker/docker-compose.yml`

### 3. `apps/web/src/components/layout/Sidebar.tsx`
Replace the entire existing file with the file at:
`CA_MANDATE_058_BUNDLE/apps/web/src/components/layout/Sidebar.tsx`

### 4. `apps/web/src/routes/operator/index.tsx`
Replace the entire existing file with the file at:
`CA_MANDATE_058_BUNDLE/apps/web/src/routes/operator/index.tsx`

### 5. `.env.example` (new file)
Copy `CA_MANDATE_058_BUNDLE/.env.example` to the **repository root**.

---

## After pasting — three manual steps required

**Step 1 — Create your `.env` file at repo root (not committed)**
Copy `.env.example` to `.env` and fill in the real Supabase session-pooler URL:
```
CAE_SUPABASE_DATABASE_URL=postgresql://postgres.evnxdssbxxrsesftdvgx:<your-db-password>@aws-0-eu-west-1.pooler.supabase.com:5432/postgres
```
Get the password from: Supabase Dashboard → Project Settings → Database → Reset database password (if needed).

**Step 2 — Restart the frontend dev server**
```bash
cd apps/web && npm run dev
```
TanStack Router's Vite plugin auto-regenerates `routeTree.gen.ts` on startup.
Do **not** manually edit `routeTree.gen.ts` — it is in `.gitignore` and will be overwritten.
After restart, "Program Operator" will appear in the sidebar and `/operator` will route correctly.

**Step 3 — Rebuild the Docker image before next `docker compose up`**
```bash
docker compose -f infra/docker/docker-compose.yml build api
docker compose -f infra/docker/docker-compose.yml up
```
The image rebuild is required because `dockerfile.api` changed.

---

## Verification checklist (run after pasting)

- [ ] `docker compose build api` exits 0 with no pip errors
- [ ] `docker compose up` starts; `curl localhost:8000/api/health` returns HTTP 200
- [ ] `curl localhost:8000/api/v1/workspaces -H "X-Actor-Id: dev-operator-local"` returns 200 or 404 (not 500)
- [ ] Browser at `localhost:3000` shows "Program Operator" in the left sidebar
- [ ] Clicking "Program Operator" renders the console without a crash
- [ ] Browser network tab shows NO request with `workspace_id: "ws-default"`
- [ ] `grep "^\.env$" .gitignore` returns a match
- [ ] `cat .env.example` contains only placeholder values (no real password)

---

## What NOT to do

- Do not edit `routeTree.gen.ts` — it is auto-generated
- Do not add any real credentials to `.env.example`
- Do not modify any file not listed above
- Do not run any database migrations — none are needed for these changes
- Do not rotate Supabase keys via this task (that is a separate Operator action)

---

## Operator decision required

After verifying all checklist items, the Operator must explicitly approve or reject CA-M058:

**"Do you approve CA-M058?"**

The mandate is not complete until this decision is recorded.
