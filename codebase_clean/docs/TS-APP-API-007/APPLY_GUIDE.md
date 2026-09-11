# Applying this package (TS-APP-API-007)

1. **Copy the tree onto the repo root** — every path here is already
   relative to the repo root, so this is a straight overlay:

   ```
   cp -r api tests <path-to-repo>/
   ```

   New files created: `api/routers/air.py`, `api/schemas/__init__.py`,
   `api/schemas/air.py`, `api/schemas/interviews.py` (stand-in for
   TS-APP-API-003, not yet implemented in this codebase — see the
   docstring in that file), `api/services/__init__.py`,
   `api/services/air_adapter.py`, `api/services/air_projection.py`,
   `tests/api/fixtures/__init__.py`,
   `tests/api/fixtures/air_portfolio_fixture.py`,
   `tests/api/fixtures/air_script_fixture.py`, and the five
   `tests/api/test_air_*.py` files. Nothing here overwrites an existing
   file.

2. **Apply the one-line `api/main.py` change:**

   ```
   cd <path-to-repo>
   git apply api-main-py.diff        # or: patch -p1 < api-main-py.diff
   ```

   This adds exactly one line — the `include_router` call for the new
   router at prefix `/api/air` — and touches nothing else in
   `api/main.py`.

3. **Verify:**

   ```
   pip install --break-system-packages -e packages/ca_contracts -e packages/ca_runtime \
       -e packages/ca_delegation_rc4 -e packages/ca_release \
       -e services/pipeline -e services/air -e services/vae \
       -e services/interview -e services/builder
   pip install --break-system-packages -r api/requirements.txt pytest httpx
   python3 -m pytest tests/api/ -q
   ```

   Expect `23 passed` (15 new AC tests + 9 pre-existing, unchanged).

That's the whole change set. See the conversation for the full writeup of
what was verified against source, the three confirmed bugs fixed in the
spec's own sample code, and the one flagged (not fixed) mismatch between
the spec's error contract and this app's existing global 404 handler.
