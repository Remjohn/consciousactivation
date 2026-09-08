# CA-M037 Agent Host Runner — Agent Handoff

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/agent_host_runner.py` | Added the CA-M037 host runner: process-isolated external provider/tool calls, strict wall-clock and UTF-8 byte quotas, structured input sanitization, deterministic provider failover, five-turn maximum, SideEffectClass enforcement, and deterministic token/receipt accounting. | `INV-HOST-001`: external invocations are bounded and isolated; malformed/oversized inputs fail closed; provider failure routes deterministically; unauthorized side effects and open-ended tool loops fail closed; token totals are deterministic. |
| `tests/cae/test_ca_m037_agent_host_runner.py` | Added executable positive, negative, regression, timeout, quota, failover, side-effect, five-turn, sanitization, and false-proof-countercase coverage at the Host Runner boundary. | Executable evidence covers each CA-M037 acceptance dimension and demonstrates that configuration/name presence alone does not prove execution. |

## Exact paste instructions

Replace/add the repository files exactly as follows:

1. Replace/add `packages/ca_runtime/src/ca_runtime/agent_host_runner.py` with the bundled file at `CA-M037_BUNDLE/packages/ca_runtime/src/ca_runtime/agent_host_runner.py`.
2. Replace/add `tests/cae/test_ca_m037_agent_host_runner.py` with the bundled file at `CA-M037_BUNDLE/tests/cae/test_ca_m037_agent_host_runner.py`.

No other repository files are authorized or included in this bundle.

## Manual post-apply commands

The user explicitly requested that tests not be run by the execution agent, so no tests were executed while producing this bundle.

After applying the two files, the operator may run:

```bash
python -m pytest tests/cae/test_ca_m037_agent_host_runner.py -v
```

This suite assumes the repository's existing `ca_runtime` package is importable in the same way as its existing CAE tests.

No database migration, npm script, generated asset, or dependency installation is required.

## New automated tests included

- `TestPositiveLiveHostRunner.test_real_provider_call_completes_inside_isolated_runtime`
- `TestPositiveLiveHostRunner.test_deterministic_token_accounting_is_provider_independent`
- `TestProviderFailover.test_primary_failure_fails_over_to_next_provider`
- `TestProviderFailover.test_all_provider_failures_fail_closed`
- `TestStrictRuntimeLimits.test_wall_clock_timeout_terminates_slow_external_call`
- `TestStrictRuntimeLimits.test_isolated_container_exposes_direct_timeout_contract`
- `TestStrictRuntimeLimits.test_provider_output_byte_quota_fails_closed`
- `TestStrictRuntimeLimits.test_large_input_is_rejected_before_external_execution`
- `TestStructuredInputSanitization.test_nul_is_rejected`
- `TestStructuredInputSanitization.test_non_string_object_keys_are_rejected`
- `TestStructuredInputSanitization.test_unicode_normalization_is_deterministic`
- `TestToolPolicyAndTurnBound.test_allowed_read_only_tool_executes_and_returns_to_model`
- `TestToolPolicyAndTurnBound.test_disallowed_side_effect_class_fails_closed_before_tool_execution`
- `TestToolPolicyAndTurnBound.test_tool_loop_cannot_exceed_five_turns`
- `TestToolPolicyAndTurnBound.test_undeclared_tool_fails_closed`
- `TestFalseProofCountercases.test_provider_name_in_configuration_is_not_success_without_execution`

## Implementation note

The isolated runtime boundary uses a child process from Python's `multiprocessing` standard library. It is intentionally dependency-free and enforces termination from the parent on a hard deadline. The boundary is process isolation rather than an external Docker/container runtime service.

CA-M037's mandate document separately states that multi-provider routing belongs to CA-M038. The user's supplied acceptance contract for `INV-HOST-001` explicitly requires provider failover and deterministic token accounting; this bundle implements those requested acceptance properties within the two authorized CA-M037 files without modifying the existing CA-M038 router.
