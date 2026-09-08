# AGENT HANDOFF — CA-M048
## Path Traversal & Tool Sandbox Hardening / INV-SEC-001

**Mandate ID:** `CA-M048`
**Wave:** 06
**Canon question:** Q47
**Invariant:** `INV-SEC-001`
**Status:** EXECUTION COMPLETE — Operator decision required (see §6)

---

## 1. Summary Table

| File Changed / Created | What Changed | Invariant Proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/sandbox.py` | **NEW FILE** — Canonical path traversal predicate (`assert_sandboxed_path`), typed error taxonomy (`PathTraversalError`, `UnregisteredToolError`, `ForbiddenExecutableError`, `ShellInjectionError`, `NetworkOperationBlockedError`), `ToolSandboxPolicy`, `ToolSandbox` context-manager execution boundary, `reject_default_tool_bypass` helper, shell-injection pattern registry, `_looks_like_path` heuristic. | INV-SEC-001: single canonical containment predicate; path resolved via `Path.resolve()` (not string prefix); `shell=False` enforced at the subprocess call site; no bypass path reachable. |
| `packages/ca_runtime/src/ca_runtime/agent_invocation.py` | **MODIFIED** — Removed the `tool:default-` bypass clause (`not t.startswith("tool:default-")`) from `AgentInvocationCompiler.compile`. Added CA-M048 module-level docstring block. | INV-SEC-001: every requested tool must now be explicitly present in `all_allowed_tools`; no prefix exception is honoured. |
| `tests/cae/test_ca_m048_sandbox.py` | **NEW FILE** — 12 acceptance gates + false-proof defence tests + adversarial edge-case suite. Exercises both the `assert_sandboxed_path` helper and the `ToolSandbox.execute_tool` real runner path. Also exercises the production `AgentInvocationCompiler` (not a mock). | All gates; false-proof FP-1 through FP-4 satisfied. |

---

## 2. Exact Paste Instructions

These files must replace/create at the exact repo-relative paths shown below. No other files are touched.

### File 1 — New module (create)

```
packages/ca_runtime/src/ca_runtime/sandbox.py
```

**Action:** Copy `CA-M048_BUNDLE/packages/ca_runtime/src/ca_runtime/sandbox.py` into the repository at that path. The file does not exist in the current repo.

### File 2 — Modified file (replace)

```
packages/ca_runtime/src/ca_runtime/agent_invocation.py
```

**Action:** Replace the existing `agent_invocation.py` with `CA-M048_BUNDLE/packages/ca_runtime/src/ca_runtime/agent_invocation.py`.

**Diff summary (single semantic change):**

Before (line ~416):
```python
if t not in all_allowed_tools and not t.startswith("tool:default-"):
    raise UnauthorizedToolError(agent_id, t, "Tool is not in declared capabilities or agent tool list")
```

After:
```python
if t not in all_allowed_tools:
    raise UnauthorizedToolError(
        agent_id,
        t,
        "Tool is not in declared capabilities or agent tool list "
        "(CA-M048: tool:default- bypass removed per INV-SEC-001)",
    )
```

### File 3 — New test file (create)

```
tests/cae/test_ca_m048_sandbox.py
```

**Action:** Copy `CA-M048_BUNDLE/tests/cae/test_ca_m048_sandbox.py` into the repository at that path.

---

## 3. Manual Post-Apply Commands

```bash
# 1. Install/reinstall the ca_runtime package so sandbox.py is importable
pip install -e packages/ca_runtime --break-system-packages

# 2. Verify the new module imports cleanly
python -c "from ca_runtime.sandbox import assert_sandboxed_path, ToolSandbox, ToolSandboxPolicy; print('OK')"

# 3. Run the CA-M048 test suite
pytest tests/cae/test_ca_m048_sandbox.py -v

# 4. Run the existing M52 / M67 invocation tests to confirm no regression
pytest tests/cae/test_m52_canonical_agent_invocation_contract.py \
       tests/cae/test_m67_agentinvocation_execution_boundary_enforcement.py -v
```

No database migrations are required. No npm scripts are required. No schema files are changed.

---

## 4. New Automated Tests Included in This Bundle

**Test file:** `tests/cae/test_ca_m048_sandbox.py`

| Test Class | Gate / Purpose |
|---|---|
| `TestGate1_NestedAllowedPath` | Gate 1 — positive: nested allowed path passes containment |
| `TestGate2_DotDotTraversalBlocked` | Gate 2 — negative: `..` traversal blocked |
| `TestGate3_AbsoluteOutOfRootBlocked` | Gate 3 — negative: absolute out-of-root path blocked |
| `TestGate4_SymlinkEscapeBlocked` | Gate 4 — negative: real symlink escape blocked (disk fixture) |
| `TestGate5_UnregisteredToolRejected` | Gate 5 — negative: unregistered tool name rejected |
| `TestGate6_ForbiddenBinaryRejected` | Gate 6 — negative: binary not in allowlist rejected |
| `TestGate7_ShellMetacharsRejected` | Gate 7 — negative: shell metacharacters blocked (8 patterns) |
| `TestGate8_AllowedToolExecutesSuccessfully` | Gate 8 — positive: real subprocess with shell=False succeeds |
| `TestGate9_DefaultToolBypassRemovedFromCompiler` | Gate 9 — negative: `tool:default-` rejected by production compiler |
| `TestGate10_ShellTrueNeverReachable` | Gate 10 — negative: no `shell=True` path reachable |
| `TestGate11_PolicyResolvesRootsAtConstruction` | Gate 11 — schema: policy eagerly resolves roots |
| `TestGate12_EmptyWorkspaceRootsRejected` | Gate 12 — negative: empty roots raises ValueError |
| `TestAdversarialEdgeCases` | Edge cases: string-prefix trick, unicode, network, cwd |
| `TestFalseProofDefence` | FP-1 through FP-4: subprocess never called before guards fire |

---

## 5. Evidence Record

| Claim | Evidence Class | Locator |
|---|---|---|
| `assert_sandboxed_path` uses `Path.resolve()` for containment (not string prefix) | `EXECUTABLE` | `sandbox.py` line ~148 (`resolved.is_relative_to(resolved_root)`) |
| `tool:default-` bypass removed from compiler | `EXECUTABLE` | `agent_invocation.py` — `AgentInvocationCompiler.compile`, tool reconciliation block |
| `shell=False` invariant at subprocess call site | `EXECUTABLE` | `sandbox.py` `ToolSandbox.execute_tool` — `subprocess.run(..., shell=False)` |
| Shell injection patterns caught before exec | `TEST` | `test_ca_m048_sandbox.py::TestGate7_ShellMetacharsRejected` |
| Real symlink escape caught by resolve | `EXECUTABLE` | `test_ca_m048_sandbox.py::TestGate4_SymlinkEscapeBlocked` (creates real `tmp_path` symlink) |
| Production compiler rejects `tool:default-exec` | `EXECUTABLE` | `test_ca_m048_sandbox.py::TestGate9_DefaultToolBypassRemovedFromCompiler::test_tool_default_prefix_rejected_by_compiler` |
| subprocess.run never reached for traversal path | `EXECUTABLE` | `test_ca_m048_sandbox.py::TestFalseProofDefence::test_full_adversarial_sequence_blocked_before_exec` |
| No `shell` parameter on `execute_tool` | `SCHEMA` | `test_ca_m048_sandbox.py::TestGate10_ShellTrueNeverReachable::test_no_shell_true_parameter_exists_in_execute_tool` |

### False-proof result (mandate §9)

> "Reject the false proof where the helper is tested but production has another bypass path."

The `TestFalseProofDefence` class monkeypatches `subprocess.run` and asserts it is NOT called before each guard fires. `TestGate9` runs through the production `AgentInvocationCompiler` (not a stub). This satisfies the false-proof requirement: we exercise the real runner/dispatcher for at least one representative invocation per guard class.

---

## 6. Residual Limitations

1. **Kernel/container isolation not tested.** The sandbox module enforces declared-capability containment. OS-level process isolation (seccomp, namespaces, cgroups) is outside the scope of CA-M048 and is not claimed.
2. **Windows symlink tests may require elevated privileges.** The Gate 4 symlink tests are conditionally skipped on Windows configurations that do not support unprivileged symlink creation.
3. **`sandbox.py` is not yet exported from `ca_runtime/__init__.py`.** The module is importable via `from ca_runtime.sandbox import …` but is not yet in the `__all__` list. Adding it to `__init__.py` is a separate, non-conflicting change that can be done by the operator as a follow-on (it does not affect INV-SEC-001 enforcement).
4. **Network enforcement is declaration-level only.** `assert_network_allowed` validates against the declared policy before execution but does not perform kernel-level egress blocking.
5. **Existing tools using `tool:default-` prefix.** If any legitimate production tool currently depends on the `tool:default-` bypass, it will now raise `UnauthorizedToolError`. Per mandate §11, such tools must be adapted to use the explicit tool registry rather than restoring the bypass. The operator must identify and remediate any such tools before deploying this bundle.

---

## 7. Control-State Impact

| State dimension | Before CA-M048 | After CA-M048 |
|---|---|---|
| `tool:default-` bypass | Present in `AgentInvocationCompiler.compile` | **Removed** |
| Canonical path predicate | None — no module-level `assert_sandboxed_path` | `sandbox.py::assert_sandboxed_path` |
| `shell=False` enforcement | Implicit (no subprocess runner existed) | **Explicit** at `ToolSandbox.execute_tool` |
| Unregistered tool error message | Generic | Includes `CA-M048: tool:default- bypass removed per INV-SEC-001` |

---

## 8. Operator Decision Required

**Request:** Approve or reject `CA-M048` based on executable proof that:
1. Tool names must be explicitly in the declared registry — no `tool:default-` bypass.
2. All filesystem path arguments resolve within declared workspace roots using `Path.resolve()` containment.
3. System RPC is restricted to an explicit binary allowlist via `ToolSandboxPolicy.binary_allowlist`.
4. `shell=False` is a non-overridable invariant at the `ToolSandbox.execute_tool` call site.
5. Shell injection patterns in arguments are blocked before execution.

**Operator must also decide:** Whether any currently deployed tools depend on the `tool:default-` prefix bypass and how to migrate them (adapt to explicit registry, or record as a compatibility collision per mandate §7).
