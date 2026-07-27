---
purpose: Trivial one-line front-matter fix. Hand to any agent, no code
  context needed — this touches spec metadata only.
---

# Fix Prompt — GAP-004 (Spec Gap Ledger)

## Task

Open `TS-APP-UI-003.md`. In the YAML front matter at the top of the file,
find this line:

```yaml
module: apps/web
```

Replace it with:

```yaml
module: web
```

## Why

Every other spec in the set uses two-value module naming:
`api` (TS-APP-API-001 through TS-APP-API-006) or `web`
(TS-APP-UI-001, TS-APP-UI-002, TS-APP-UI-004). `TS-APP-UI-003.md` is the
only spec using the longer directory-style value `apps/web`. The directory
itself is still `apps/web/` — only the front-matter label changes, to keep
the module taxonomy consistent for any future `SPEC_INDEX.yaml` grouping or
tooling that filters specs by module.

## Verify

After the edit, confirm no other field or path reference inside
`TS-APP-UI-003.md` was accidentally changed — this is a front-matter-only
edit. Run:

```bash
grep -n "^module:" TS-APP-*.md
```

Expected output: every line reads `module: api` or `module: web`, with no
remaining `apps/web` value anywhere in the front matter.
