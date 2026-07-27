# Test Plan

Test complete node validation, deterministic graph identity, exact ready/locked
classification, stable one-question ordering, evidence and dependency gates, model
path support, complete recommendations, fact/inference separation and explicit
non-ratification. Negative tests cover HG-001, unsupported paths, missing evidence,
premature nodes, multiple active questions, wrong authority, stale/invalidated inputs,
command conflicts and injected atomic failure. Verify replay, outbox retry,
invalidation, historical reproduction and fresh-context byte equality.

Run Story tests twice, affected architecture/correction suites, then the full suite.
Compile every Python file. No mandatory skip or external dependency is permitted.
