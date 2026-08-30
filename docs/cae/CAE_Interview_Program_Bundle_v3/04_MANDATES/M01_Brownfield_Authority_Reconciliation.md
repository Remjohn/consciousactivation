# M01 — Brownfield Authority Reconciliation

**Status:** PROPOSED
**Depends on:** ratified PRD delta + accepted Interview Program tech spec
**Primary requirement:** FR-IP-001

## Objective

Produce the evidence-backed implementation map for the Interview Program without writing code until the current repository has been reconciled.

## Verified repository starting points

The current repository exposes `services/interview-composer` as the relevant Composer boundary and `TS-APP-COMPOSER-001` as its current integration specification. The repository also contains explicit guidance that deeper AIR activation objects are not owned by Composer. These facts must be re-read from the current branch before execution.

## Required inspection

Inspect the actual current branch for:

- Composer package tree, `AGENTS.md`, README, domain/canonical/repository/application layers;
- current Brief and Session schemas and persistence;
- current Composer API routes/dependencies and UI route(s);
- AIR references and ownership for activation-hypothesis/portfolio/Matrix-of-Edging objects;
- current Question Intelligence audit corpus and any existing Question YAMLs;
- existing Operator identity/auth and UI component conventions;
- existing test/fixture/e2e patterns;
- PRD and tech-spec maintenance rules relevant to the change.

## Exact output

Create an implementation-ready reconciliation report containing:

1. actual source files inspected;
2. actual owning modules/services;
3. existing object contracts and fields relevant to the program;
4. current route/API boundaries;
5. exact gaps;
6. exact extension points;
7. objects/fields deliberately NOT to be created;
8. any contradiction between this bundle and the live repository;
9. updated execution sequence if the live repository differs.

## Prohibited work

Do not implement feature code in M01 unless the reconciliation itself requires a harmless documentation/test fixture. Do not invent symbols, routes, tables, or object owners.

## Acceptance criteria

- all referenced implementation symbols are confirmed in the current tree or explicitly marked absent;
- ownership map contains no unresolved “probably owned by” claims;
- any new persistent structure has an identified owner or is escalated;
- current Composer contract is quoted/linked from the actual source of truth;
- implementation plan is specific enough that M02–M05 do not need to re-discover the architecture.

## Required evidence

- file/path inventory;
- relevant source excerpts or line references in the execution receipt;
- tests, if any;
- commit hash only if changes were made.

## Stop conditions

Stop and return BLOCKED if the current branch has materially diverged from `TS-APP-COMPOSER-001` or the bundle assumptions in a way that affects ownership, Brief shape, or runtime integration.
