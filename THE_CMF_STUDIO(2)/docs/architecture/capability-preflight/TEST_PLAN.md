# Test Plan

Tests verify:

```text
provider availability validates missing secrets
provider menu counts configured/missing/degraded/blocked
runtime availability reports configured/unavailable states
sample-first policy blocks batch
pipeline status passes when required tools available
pipeline status blocks when required tools missing
setup offers are generated for missing capabilities
preflight report does not execute providers
```
