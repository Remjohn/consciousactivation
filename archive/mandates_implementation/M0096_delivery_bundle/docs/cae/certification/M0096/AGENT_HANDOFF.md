# AGENT_HANDOFF.md — CAE-M0096

**Mandate:** `M0096 — Partner-Ready Evidence-First Visual Production Vertical Slice and Certification`  
**Status:** `BLOCKED — OPERATOR DECISION REQUIRED`  
**Campaign batch:** `E2 CERTIFICATION`  
**Execution date:** 2026-09-11

## Result

The bounded M0096 certification bundle is complete as a **blocked** evidence package. No out-of-boundary production implementation was performed. The supplied archive lacks native runtime reachability, real source media, complete Python dependencies, and exact Git provenance, so the terminal partner-ready claim cannot be made honestly.

## Files added by M0096

- `tests/e2e/test_m0096_partner_ready_vertical_slice.py`
- `docs/cae/evidence/M0096/M0096_UPSTREAM_TO_CAE_MAPPING.md`
- `docs/cae/evidence/M0096/M0096_M067_LIVE_BLOCKER_EVIDENCE.json`
- `docs/cae/evidence/M0096/M0096_COMMAND_LOG.txt`
- `docs/cae/evidence/M0096/M0096_EVIDENCE_MANIFEST.json`
- `docs/cae/certification/M0096/M0096_PARTNER_READY_CERTIFICATION.md`
- `docs/cae/certification/M0096/AGENT_HANDOFF.md`

No existing repository file outside the allowed M0096 boundary was modified.

## Rationale

The brownfield audit found reusable canonical objects and controls already in place:

- Storyboard session/revision state and immutable operator feedback in `packages/ca_runtime/src/ca_runtime/storyboard_session.py`.
- Shared storyboard program vocabulary in `packages/ca_runtime/src/ca_runtime/storyboard_programs.py`.
- Deterministic TransformationIntent → TransformationRecipe compilation in `packages/ca_runtime/src/ca_runtime/transformation_recipe.py`.
- Evidence-first Visual Asset Studio projection in `api/routers/visual_studio.py`.
- M0067 real-campaign fail-closed runtime harness in `tests/e2e/m067_real_campaign_harness.py`.
- Existing M0079 “good-looking but wrong” rejection coverage.

M0096 therefore adds only a certification audit and evidence bundle; it does not create a duplicate authority or duplicate runtime.

## Authority mapping

The literal requested constitution and precedence paths are absent from the root of the supplied snapshot. The current canonical equivalents are located under:

- `governance/program-control/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
- `governance/program-control/00_CONSTITUTION/current-v1.1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`

The four 2026-09-10 visual-production authority files are present at `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/`. M0096 does not copy the authority files to the missing literal paths because doing so could create a competing authority surface.

## External source

- OpenChatCut: `https://github.com/0xsline/OpenChatCut`
- Current upstream `main` commit observed on 2026-09-11: `607e0fcc2b755a92a659deb54305ba8164930ae3`
- License: `AGPL-3.0-or-later`
- Exact local file paths and local hashes: `docs/cae/evidence/M0096/M0096_UPSTREAM_TO_CAE_MAPPING.md`
- Local vendored revision is not claimed to match the observed upstream commit because the supplied repository has no `.git` metadata.

## Verification commands and results

### M0096 audit

```bash
python -m pytest -q tests/e2e/test_m0096_partner_ready_vertical_slice.py
```

Observed result: `5 passed in 0.05s`.

### Syntax

```bash
python -m py_compile tests/e2e/test_m0096_partner_ready_vertical_slice.py
```

Observed result: pass (exit code 0).

### Native live campaign preflight

```bash
python tests/e2e/m067_real_campaign_harness.py preflight --artifact-root /tmp/m0096-preflight
```

Observed: exit code `2`; OpenChatCut connection refused; real source media absent; Git metadata absent.

### Native live campaign

```bash
python tests/e2e/m067_real_campaign_harness.py live --artifact-root /tmp/m0096-live
```

Observed: exit code `2`; `REAL_CAMPAIGN_BLOCKED`; terminal state `BLOCKED`.

### Dependency-backed focused product test attempt

Observed first collection blocker: `ModuleNotFoundError: No module named 'psycopg'`. Package installation could not reach the configured index. A temporary shim exposed the next missing repository dependency `cmf_builder`; nothing was committed and no success was inferred.

## Evidence classes

`EXECUTABLE`: live environment probe and existing runtime gate behavior.  
`TEST`: M0096 audit tests and referenced existing countertests.  
`MIGRATION`: relocated current canonical authority files used instead of creating duplicates.  
`REGISTRY_SOURCE`: exact OpenChatCut upstream/source inspection.  
`DOCUMENT`: certification and mapping records.  
`HYPOTHESIS`: optional SAM3 availability is not treated as proven.  
`OPERATOR_DECISION_REQUIRED`: terminal partner-readiness and visual/semantic approval.

## Limitations

1. No real governed source media artifact was available.
2. Native OpenChatCut runtime was unreachable.
3. No live operator correction/revision, native render, QA, release authorization or final receipt was produced.
4. No current exact CAE Git SHA is available in the uploaded archive.
5. Dependency-complete product test execution was not reproducible in this environment.
6. No live SAM3 evidence was available; it was not used to manufacture a success claim.
7. Human perceptual, semantic and rights/source-lineage approval remains outstanding.

## Provenance

Supplied source archive SHA-256:

`ac7212df149488353130ee0e6c275d1c4fb35da52826d005dbe4924789f6beee`

Exact current CAE Git commit SHA:

`UNAVAILABLE — supplied archive contains no .git metadata.`

## Operator decision requested

At close, operator must select exactly one: `APPROVE`, `APPROVE-WITH-LIMITATIONS`, or `REJECT`.

The execution agent does not self-promote the blocked campaign to partner-ready.
