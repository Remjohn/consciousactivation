---
purpose: Hand this directly to an implementing agent (Claude Code or similar)
  BEFORE implementing TS-APP-UI-002.md or TS-APP-UI-003.md. Do not implement
  either spec as currently written — both contain confirmed, concrete field
  and function mismatches against their real siblings, found by direct
  comparison, not inference.
scope: Edits TS-APP-UI-002.md and TS-APP-UI-003.md only. Touches no
  application code — those specs have not been implemented yet.
---

# Reconciliation Prompt — GAP-003 (Spec Gap Ledger)

## Your task

Reconcile `TS-APP-UI-002.md` against the real `TS-APP-API-002.md`, and
reconcile `TS-APP-UI-003.md` against the real `TS-APP-UI-001.md`. Both
target specs were written before their sibling existed and openly flagged
their own guesses as unconfirmed. Confirmed comparison below — patch the
target specs to match reality, do not redesign them.

Do not just skim for the word "assume" — every field name below was checked
character-for-character against the real spec.

---

## Reconciliation 1 — `TS-APP-UI-002.md` §6 `HarnessSummary` vs `TS-APP-API-002.md` §6 `HarnessSummary`

**Guessed (TS-APP-UI-002.md, current text):**
```ts
export interface HarnessSummary {
  harness_definition_id: string;
  category_id: string;
  format_profile_ids: string[];
  version: string;
  capability_ids: string[];
}
```

**Real (TS-APP-API-002.md §6, already written, do not change this one):**
```python
class HarnessSummary(BaseModel):
    definition_id: str
    definition_hash: str
    manifest_id: str
    manifest_version: str
    task_id: str
    mode: str                        # "generic" | "activative"
    category_id: str | None
    category_name: str | None
    classification: list[str]
    capability_requirements: list[str]
    production_ready: bool
    certified: bool
    package_file: str
    package_hash: str
    added_at: str | None
```

**Every field in the guess is wrong.** Not approximately wrong — every name
differs from its real counterpart, and one field was invented outright:

| Guessed field | Real field | Problem |
|---|---|---|
| `harness_definition_id` | `definition_id` | wrong name |
| `category_id: string` | `category_id: str \| None` | guess is non-nullable; real field is `null` for every generic-mode Harness — a UI built against the guess will crash or silently misrender the first generic Harness it encounters |
| `format_profile_ids: string[]` | *(does not exist)* | fabricated — no such field anywhere in the real response |
| `version: string` | `manifest_version` | wrong name |
| `capability_ids: string[]` | `capability_requirements: list[str]` | wrong name |
| *(missing entirely)* | `definition_hash`, `manifest_id`, `task_id`, `mode`, `category_name`, `classification`, `production_ready`, `certified`, `package_file`, `package_hash`, `added_at` | 11 real fields never accounted for |

**Required patch to `TS-APP-UI-002.md`:**

1. Replace the `HarnessSummary` TypeScript interface in §6 with the exact
   field set above, translated to TS types (`str | None` → `string | null`,
   `list[str]` → `string[]`).
2. Search `TS-APP-UI-002.md` §7 and §8 for every place that reads
   `harness.harness_definition_id`, `harness.version`,
   `harness.format_profile_ids`, or `harness.capability_ids` — rename to
   `harness.definition_id`, `harness.manifest_version`, remove the
   fabricated `format_profile_ids` usage entirely (check what UI need it
   was serving — if the Harness card was going to display a format profile,
   note that no such data exists yet and either drop that UI element or
   flag it as a new gap), and rename to `harness.capability_requirements`.
3. Anywhere the component renders `category_id` as if it's always present
   (e.g. a `<Badge>{category_id}</Badge>` with no null check), add a
   conditional: generic-mode Harnesses (`category_id === null`) must render
   something explicit like "Uncategorized" or be filtered from category-based
   groupings, not crash or render `"null"` as text.
4. Update the front-matter `quality_state` from `WRITTEN_PENDING_AUDIT` to
   `RECONCILED_PENDING_AUDIT` once done, and add a line to §1 (Files Read)
   recording that `TS-APP-API-002.md` §6 was read and reconciled against,
   with today's date.

---

## Reconciliation 2 — `TS-APP-UI-002.md`'s parallel fetch/error layer vs `TS-APP-UI-001.md`'s real one

**Guessed (TS-APP-UI-002.md §6, current text) — a second, self-built fetch layer:**
```ts
// apps/web/src/api/errors.ts
export class ApiError extends Error {
  readonly code: string;
  readonly status: number;
  constructor(status: number, body: ErrorResponse) { ... }
}
export async function parseJsonOrThrow<T>(response: Response): Promise<T> { ... }

// apps/web/src/api/campaigns.ts
export async function listCampaigns(filters): Promise<CampaignSummary[]> {
  const response = await fetch(`/api/campaigns?${params}`);
  return parseJsonOrThrow<CampaignSummary[]>(response);
}
```

**Real (TS-APP-UI-001.md Stage 5, already written, do not change this one):**
```ts
// apps/web/src/api/http.ts
export async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> { ... }

// apps/web/src/api/ApiError.ts
export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number | null,
    readonly errorCode: string | null,
    readonly service: string | null = null,
  ) { ... }
}
```

**The problem:** TS-APP-UI-002.md invents its own `ApiError` class (different
constructor signature — `(status, body)` vs the real
`(message, status, errorCode, service)`), its own `parseJsonOrThrow`
function, and calls `fetch()` directly instead of using the real, already-
built `apiFetch<T>`. If implemented as written, the app ends up with two
incompatible error types both named `ApiError`, and every UI-002 API call
bypasses the shared client UI-001 already built.

**Required patch to `TS-APP-UI-002.md`:**

1. Delete `apps/web/src/api/errors.ts` from this spec's file list entirely —
   it duplicates `apps/web/src/api/ApiError.ts`, which already exists per
   `TS-APP-UI-001.md`.
2. Rewrite `apps/web/src/api/campaigns.ts` (and the equivalent interview
   functions) to import and call the real `apiFetch<T>` from
   `apps/web/src/api/http.ts`, not raw `fetch()`:
   ```ts
   import { apiFetch } from "./http";

   export async function listCampaigns(filters: CampaignListFilters): Promise<CampaignSummary[]> {
     const params = new URLSearchParams(Object.entries(filters).filter(([, v]) => v) as [string, string][]);
     return apiFetch<CampaignSummary[]>(`/api/campaigns?${params.toString()}`);
   }

   export async function createCampaign(payload: CampaignCreateRequest): Promise<CampaignDetailResponse> {
     return apiFetch<CampaignDetailResponse>("/api/campaigns", {
       method: "POST",
       body: JSON.stringify(payload),
     });
   }
   ```
3. Anywhere UI-002 catches errors and reads `error.code` — rename to
   `error.errorCode`, matching the real `ApiError` field name.
4. Update `quality_state` and §1 the same way as Reconciliation 1.

---

## Reconciliation 3 — `TS-APP-UI-003.md`'s assumed scaffold vs `TS-APP-UI-001.md`'s real one

TS-APP-UI-003.md's own §1 already names this gap honestly
(`ASSUMED_INTERFACE_PENDING_UI_001`) — do the confirmation pass it asked for.

| UI-003 assumed | UI-001 real | Match? |
|---|---|---|
| `apiGet<T>(path)` and `apiPost<T>(path, body)` — **two separate functions** | `apiFetch<T>(path, init?)` — **one function**, method passed via `init.method` | **MISMATCH — must patch** |
| `ApiError { error_code, message, service, timestamp }` | `ApiError(message, status, errorCode, service)` — a class with constructor params, not a plain object shape; field name is `errorCode` not `error_code` | **MISMATCH — must patch** |
| File-based routes under `apps/web/src/pages/`, `/campaigns/$campaignId` | Confirmed: TanStack Router file-based routing via `@tanstack/router-plugin/vite`, generating `routeTree.gen.ts`. Verify the exact source directory name (`pages/` vs a `routes/` convention some TanStack Router setups use) and the exact file-naming pattern for a dynamic segment (e.g. `campaigns.$campaignId.tsx` vs `campaigns/$campaignId.tsx`) directly against UI-001's Stage 4 file list before assuming the path string alone is sufficient | **PARTIAL — verify exact file-naming convention, don't just assume the route string** |
| `QueryClientProvider` mounted at app root, reachable via `useQueryClient()` | Confirmed: UI-001 mounts `QueryClientProvider` wrapping `RouterProvider` at the app root | **MATCH — no patch needed** |

**Required patch to `TS-APP-UI-003.md`:**

1. Everywhere `apiGet<T>(...)` is called, replace with
   `apiFetch<T>(path)`. Everywhere `apiPost<T>(path, body)` is called,
   replace with `apiFetch<T>(path, { method: "POST", body: JSON.stringify(body) })`.
2. Replace every reference to `error.error_code` with `error.errorCode`
   (the real `ApiError` class exposes camelCase properties, not a snake_case
   plain object).
3. Import `ApiError` from `../api/ApiError`, not assume a plain interface
   shape.
4. Confirm the exact route file name for the dynamic campaign-detail
   segment against `TS-APP-UI-001.md` Stage 4's file list (read it, do not
   guess a second time) and correct the path in §7/§8 if it differs from
   `campaigns.$campaignId.tsx`.
5. Update `quality_state` from `WRITTEN_PENDING_AUDIT` to
   `RECONCILED_PENDING_AUDIT`, and update §1 recording that
   `TS-APP-UI-001.md` was read in full and reconciled against.

---

## Reconciliation 4 — `TS-APP-UI-003.md` vs `TS-APP-UI-002.md` (link contract)

Check one more thing not yet verified: does `CampaignList.tsx` (built by
UI-002) link to campaign detail using the same route path
`CampaignDetail.tsx` (built by UI-003) expects to receive? Read UI-002 §7's
`<Link>` target and UI-003 §7's route registration side by side. If they
don't match exactly (including trailing slashes and param name —
`$campaignId` vs `$id` would break this silently), patch whichever spec has
the less-authoritative claim (UI-003 owns the route since it defines the
page; UI-002 should be patched to link to whatever UI-003 actually
registers).

---

## When you're done

All four reconciliations should result in:
- `TS-APP-UI-002.md` — `quality_state: RECONCILED_PENDING_AUDIT`, no more
  references to `harness_definition_id`, `format_profile_ids`, `version`
  (on a Harness object), `capability_ids`, a self-built `ApiError`, or
  `parseJsonOrThrow`
- `TS-APP-UI-003.md` — `quality_state: RECONCILED_PENDING_AUDIT`, no more
  references to `apiGet`/`apiPost`, `error_code` (snake_case), or an
  unverified route file name

Only after both are reconciled should either spec be handed to an
implementing agent for actual code generation.
