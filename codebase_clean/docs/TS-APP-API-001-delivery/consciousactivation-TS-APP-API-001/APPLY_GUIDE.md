# TS-APP-API-001 — apply guide

## 1. Apply

Unzip into the repo root (paths already match — `api/`, `infra/docker/`, `tests/api/`
are all new, nothing existing is overwritten):

```
unzip TS-APP-API-001-delivery.zip -d /path/to/consciousactivation-main
```

## 2. Install (needs network — this sandbox had none, see §4)

```bash
pip install -e packages/ca_contracts -e packages/ca_runtime \
            -e packages/ca_delegation_rc4 -e packages/ca_release \
            -e services/pipeline -e services/air -e services/vae \
            -e services/interview -e services/builder
pip install fastapi==0.115.0 "uvicorn[standard]==0.30.0" python-multipart==0.0.9 \
            pydantic==2.7.0 httpx pytest pytest-anyio --break-system-packages
```

Then:

```bash
python -c "import cmf_pipeline, cmf_activative_intelligence, cmf_vae, cmf_builder, conscious_activations_interview_expression, ca_contracts, ca_runtime"
python -m pytest tests/api/ -v
python -m pytest tests/ -q --tb=short --ignore=tests/phase1 --ignore=tests/phase2 --ignore=tests/phase3 --ignore=tests/phase4 --ignore=tests/phase8
```

## 3. What's actually in this zip vs. the spec text

The spec's Stage 2/3 sample code doesn't work as written against the real
`cmf_builder` and `conscious_activations_interview_expression` packages, and
`cmf_vae`'s status dict doesn't satisfy the documented schema. All three were
found by reading the real source and confirmed by running the fixed code
against the real classes (see §5). Everything else matches the spec as
written.

| File | vs. spec |
|---|---|
| `api/config.py` | matches spec |
| `api/dependencies.py` | matches spec, `+get_builder_repository` (needed by the builder fix below) |
| `api/errors.py` | `not_found_handler` now fills `service` from `request.path_params` — the spec's own Section 6 example shows `"service": "unknown"` in the 404 body, but its Stage 1 handler code never set it |
| `api/routers/health.py` | **rewritten status-collection layer** — see below |
| `api/main.py` | **builder construction fixed** — see below |
| `infra/docker/*`, `api/requirements.txt` | match spec |
| `tests/api/*` | written to spec's Section 10 intent; AC-004 uses a permission-independent failure trigger (see test docstring — chmod 000 doesn't fail for a root-run test suite) |

### Bug 1 — `BuilderProductizationService()` takes no zero-arg form
Spec's `main.py` calls it with no arguments. The real class
(`cmf_builder/application/productization_service.py`) requires keyword-only
`repository`, `compiler`, `exporter` — confirmed by re-running the exact call
and catching the `TypeError`. Fixed construction (mirrors
`cmf_builder/cli/bootstrap.py`, the package's own bootstrap):

```python
builder_repository = SQLiteProductizationRepository(db_path / "builder.db")
builder = BuilderProductizationService(
    repository=builder_repository,
    compiler=PortableAtomicHarnessCompiler(),
    exporter=DeterministicPortableExportService(builder_repository),
)
```

### Bug 2 — `BuilderProductizationService` and `InterviewExpressionApplication` have no `.status()`
The spec's health router calls `getattr(app_state, service_name).status()`
generically for all five services. `InterviewExpressionApplication` has no
`.status()` at all (use `interview.repository.health()` instead — confirmed
it returns the full canonical field set). `BuilderProductizationService` has
neither `.status()` nor `.health()`; `api/routers/health.py` now builds one
from its repository's `verify_integrity()` plus a direct count of
`durable_command_receipts` rows — confirmed this returns `integrity: "ok"`
against a real, freshly-initialized repository.

Run generically as the spec describes, both of these come back
`integrity: "error"` on **every** request (`AttributeError`, caught and
turned into an error entry) — meaning AC-002 could never pass as originally
written, permanently returning 503. This isn't a hypothetical; I reproduced
it.

### Bug 3 — `VAEApplication.status()` doesn't match the documented schema
It never includes `product_id`, `product_version`, `authority_state`,
`command_count`, or `receipt_count` (confirmed by reading
`cmf_vae/repository.py::health()` and `application.py::status()`). VAE has
no command/receipt concept, so the adapter reports those two counts as `0`
rather than inventing values, and fills `product_id`/`product_version` from
package metadata. Flagged in code comments — worth a product decision on
whether that's the right semantics for VAE going forward.

## 4. What I could not verify — this sandbox had no network access

`curl -I https://pypi.org` returned `403 host_not_allowed` and `apt-get
update` failed the same way; nothing in the fastapi/pytest/jsonschema
dependency chain was pre-installed. **I did not fabricate pytest output.**
Enable network access and re-run §2 to get real pass/fail for AC-001 through
AC-007 and the full regression suite — the fixes above should be verified in
that pass too, not just trusted from this write-up.

What I *could* do without those dependencies:
- Installed all 9 local packages editable (`pip install -e ... --no-deps`,
  pure local dependency graph, no PyPI needed).
- Ran the literal `python -c "import cmf_pipeline, ..."` check: 5 of 7 import
  cleanly (`ca_contracts`, `ca_runtime`, `cmf_activative_intelligence`,
  `conscious_activations_interview_expression`, `cmf_builder`).
  `cmf_pipeline` and `cmf_vae` both fail — both pull in `ca_delegation_rc4`,
  which does `from jsonschema import ...` at module load, and `jsonschema`
  isn't installable here either. This is purely an environment gap; nothing
  about the code needs fixing for this specific failure.
- Re-implemented and ran the corrected `air`/`interview`/`builder`
  status-collection logic directly against the real classes (bypassing
  FastAPI, which isn't importable here) — all three pass.
- `py_compile`'d every new Python file, bash-`-n`'d the smoke test script,
  and YAML-parsed the compose file. All clean.

## 5. A fourth, unrelated bug this surfaced — not fixed here, on purpose

Running `air.load_registries()` (called by the spec's own `main.py` at
startup) raises:

```
AirRepositoryError: Primitive source hash mismatch for PRM-HUM-006
```

I checked all 243 rows in `services/air/.../governance/PRIMITIVE_INVENTORY.csv`
against their `snapshot_path` files' real SHA-256: **12 of 243 mismatch**
(`PRM-HUM-006`, `PRM-HUM-016`, `PRM-HUM-024`, `PRM-HUM-029`, `PRM-PRS-001`,
`PRM-PRS-004`, `PRM-PRS-008`, `PRM-PRS-011`, `PRM-PRS-014`, `PRM-PRS-019`,
and two more). `air.status()` alone (what the health endpoint actually calls
per request) works fine — this only breaks the one-time `load_registries()`
call at startup, so it will crash server startup for the `air` service once
network/jsonschema are available, independent of anything in this delivery.

I did not touch it: it's inside `cmf_activative_intelligence`'s own bundled
data, TS-APP-API-001's AC-007 explicitly rules out modifying existing service
packages, and I can't tell from here whether the CSV or the YAML files are
the stale side — that's a call for whoever owns the AIR package's data.

## 6. Honest AC status

| AC | Status |
|---|---|
| AC-001 (clean startup) | **Blocked** here (no network); additionally will fail for `air` today because of §5 until that's fixed, independent of this delivery |
| AC-002 (all 5 `integrity: ok`) | **Blocked** here; logic fixed and unit-verified for air/interview/builder (§4); pipeline/vae untestable here (jsonschema) |
| AC-003 (per-service + 404) | **Blocked** here; 404 path exercised by code review only |
| AC-004 (degraded on failure) | **Blocked** here; test written, uses a root-safe failure trigger |
| AC-005 (CORS) | **Blocked** here (needs fastapi) |
| AC-006 (docker compose up) | **Blocked** here (no docker daemon / no network for build) |
| AC-007 (no regressions) | **Blocked** here (pytest unavailable) |

None of these are reported as passing. Re-run §2 once network is available
for real numbers.
