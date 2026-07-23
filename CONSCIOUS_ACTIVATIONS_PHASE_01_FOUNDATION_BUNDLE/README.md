# Conscious Activations Phase 1 Foundation Bundle

Bundle ID: `CA-PHASE01-FOUNDATION-2026-07-23`

This bundle implements the first development phase of the Conscious Activations
application:

- a shared `activative-production-spine@0.1.0-dev.1` contract snapshot;
- generated Python and TypeScript declarations;
- strict canonical serialization and schema validation;
- local SQLite command/event/receipt persistence;
- AIR, AHP, Interview Expression, and Studio product shells;
- clean workspace installation, health, bootstrap, and validation tests.

## Claim boundary

This is a development-only foundation. It does not ratify the V2.1 candidate as
current authority, activate Format 02, begin VAE Stage 5, call external providers,
render media, establish production readiness, or grant certification.

## Recommended application

First verify the bundle:

```bash
python scripts/verify_bundle.py
```

Dry-run against the repository:

```bash
python scripts/apply_bundle.py \
  --repo D:/Work/CONSCIOUS_ACTIVATIONS \
  --dry-run
```

Apply on a dedicated branch and run all tests:

```bash
python scripts/apply_bundle.py \
  --repo D:/Work/CONSCIOUS_ACTIVATIONS \
  --create-branch implementation/phase-01-foundation
```

Apply and commit after validation:

```bash
python scripts/apply_bundle.py \
  --repo D:/Work/CONSCIOUS_ACTIVATIONS \
  --create-branch implementation/phase-01-foundation \
  --commit
```

Rollback:

```bash
python scripts/rollback_bundle.py \
  --repo D:/Work/CONSCIOUS_ACTIVATIONS
```

## Validation performed before delivery

The payload was applied to a clean copy of the supplied repository snapshot.

- 12 positive contract fixtures passed.
- 5 negative contract fixtures were rejected.
- 14 Python tests passed.
- isolated workspace installation passed;
- TypeScript compilation passed;
- Studio health passed;
- three product SQLite bootstrap flows passed;
- idempotent replay passed.

See `receipts/VALIDATION_REPORT.md` and `receipts/TEST_RESULTS.json`.
