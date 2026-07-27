# Test Plan

Tests verify:

```text
safe client slug
safe run id
workspace path policy prevents traversal
workspace folders compile deterministically
run artifact directory has required folders
service can materialize directories
artifact refs cannot escape workspace
artifact versions require hashes
manifests require artifact refs
lineage requires source and derived refs
receipts cannot pass with blockers
```
