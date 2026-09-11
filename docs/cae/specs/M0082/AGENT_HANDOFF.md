# M0082 Agent Handoff

Status: IMPLEMENTED — focused and integration tests pass.

The Editorial Expression Calculus is a pure deterministic projection from bounded NarrativeEditingGrammar to integer/fixed-point expression values. It covers pace, shot/hold/cut timing, occupancy, scale, motion amplitude/velocity, visual/caption density, contrast, salience, and intervention frequency. It does not persist state, retrieve assets, render, invoke providers, or approve promotion.

Exact destinations:
- packages/ca_runtime/src/ca_runtime/editorial_expression_calculus.py
- packages/ca_runtime/src/ca_runtime/__init__.py
- tests/cae/test_m0082_editorial_expression_calculus.py

The 4x6 format/scene profile registry is deterministic and every output is evidence-grounded, quality-floored, bounded, and canonically hashed. Unsupported source quality, missing/duplicate evidence, and unsupported profiles fail closed.

Focused result: 8 passed.
Implementation commit: 582fbb75288042d6b85ca856c4109c63e47665b4.

The literal requested CAE-M0082 bundle path and COMPONENT_CONTRACT.yaml were absent. The delivered M0082 change bundle, canonical mandate, existing CAE authority files, and campaign Authority Pack were used; numeric profile constants remain calibration hypotheses pending operator/perceptual review.
