# Path Safety

Hard rules:

```text
client_slug must be safe
run_id must be safe
artifact_id must be safe
relative paths cannot contain ..
relative paths cannot be absolute
artifact paths must resolve under workspace root
```

No path traversal is allowed.
