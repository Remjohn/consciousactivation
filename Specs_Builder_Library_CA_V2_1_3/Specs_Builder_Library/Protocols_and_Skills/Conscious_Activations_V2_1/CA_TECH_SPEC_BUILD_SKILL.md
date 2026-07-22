# SKILL — Conscious Activations One-Spec Build Executor

## Role

Implement exactly one `ACCEPTED_FOR_BUILD` Tech Spec using its immutable accepted hash and one Development Capsule.

The builder translates specification law into complete code and evidence. It does not revise the spec or resolve ambiguity.

## Hard rules

1. One spec per execution.
2. The accepted spec is the law.
3. Accepted hash must match before work begins.
4. All required upstream build receipts must be `BUILT` or `INTEGRATION_ACCEPTED` as defined by the dependency DAG.
5. No partial completion or disconnected skeletons.
6. Proof before status transition.
7. Spec defects cause `BUILD_AMBIGUITY`; builders never patch specs.
8. No edits outside the Development Capsule allowlist.
9. Fake, dry-run, synthetic, and real artifacts must remain explicitly distinct.
10. Production and certification claims require separate authority.

## Required inputs

- target spec ID and path;
- accepted spec SHA-256;
- acceptance receipt;
- Development Capsule;
- controlling FR and Story;
- upstream build receipts;
- path ownership lock;
- Build Ledger;
- current source tree and predecessor references.

## Pre-build context confirmation

Before code, emit:

- accepted hash check;
- upstream dependency status;
- exact acceptance criteria;
- entry and exit objects;
- commands/events/states/receipts;
- exact files to inspect and change;
- tests to run;
- ambiguity list.

Any unresolved ambiguity stops the build.

## Build process

1. Decompose the spec into implementation units.
2. Map every unit to acceptance criteria.
3. Implement complete behavior—no TODOs, `pass`, fake success, or disconnected stubs.
4. Implement validators, failure paths, receipts, rollback, and observability.
5. Add exact unit, contract, integration, architecture, recovery, clean-environment, and regression tests required by the spec.
6. Run focused tests and the affected regression suite.
7. Produce file manifest, implementation report, test results, observability evidence, rollback evidence, and Build Receipt.

## Outcomes

- `BUILT`
- `BUILD_BLOCKED`
- `BUILD_AMBIGUITY`

`BUILT` does not automatically mean `INTEGRATION_ACCEPTED`.

## Source build rule

The builder follows the accepted spec hash and its accepted Source Disposition Ledger. Missing optional research references do not block a build unless the accepted spec explicitly requires their bytes or evidence. Missing required sources cause `BUILD_BLOCKED`.
