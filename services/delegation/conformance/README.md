---
title: Delegation Conformance Suites
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# Delegation Conformance Suites

The protocol is certified through executable suites rather than schema review alone.

- [Authority tests](./authority-tests/README.md)
- [Lifecycle tests](./lifecycle-tests/README.md)
- [Compatibility tests](./compatibility-tests/README.md)
- [Resilience tests](./resilience-tests/README.md)
- [Format 02 end-to-end](./format02-end-to-end/README.md)

All suites must assert expected audit receipts and absence of unauthorized state mutation.

The `1.1.0-rc.1` conformance overlay adds the five constitutional proof
families: protected-field authority rejection, Expression Moment adapter-loss
rejection, wrong-reading behavioral support, evaluator evidence, and
Activative lineage preservation through migration and replay. These extend the
existing suites without changing their lifecycle expectations.
