# Provider Live Testing Policy

Live provider tests are disabled by default.

Run them only when:

```text
RUN_PROVIDER_LIVE_TESTS=1
```

and the relevant API keys/endpoints exist.

Default CI should run unit tests and fake HTTP tests only.
