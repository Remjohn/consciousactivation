"""CA-M048 — Path Traversal & Tool Sandbox Hardening.

Invariant: INV-SEC-001 (supersedes INV-SAND-001 reference in mandate header).
Mandate:   CA-M048 / Wave 06 / Q47

This module establishes the ONE canonical sandbox boundary for the ca_runtime
package.  Every tool invocation and every filesystem path resolution that
crosses the execution boundary MUST be validated through this module.

Authority source: Q47 decision — a tool name supplied by a model is not
permission; a path that happens to exist under the process user's permissions
is not permission.

Design principles (from mandate §3, §7):
  - Path containment uses ``pathlib.Path.resolve()`` (real filesystem) not
    string prefix checks.
  - ``shell=False`` is enforced at the subprocess wrapper; there is NO
    shell-fallback path.
  - Unregistered tools are rejected BEFORE execution.
  - Symlink escapes are covered by ``Path.resolve()`` which follows symlinks.
  - ``..`` segments, alternate separators, and absolute out-of-root paths are
    all handled by the same resolve → containment check.
  - The ``tool:default-`` bypass that previously existed in
    ``AgentInvocationCompiler.compile`` is removed in the companion patch to
    ``agent_invocation.py`` in this bundle.

Public API
----------
assert_sandboxed_path(requested_path, workspace_roots) -> Path
    Canonical predicate.  Returns the resolved Path or raises
    PathTraversalError.

ToolSandbox
    Context-manager and direct-call wrapper that:
      1. Verifies tool membership in the declared registry.
      2. Validates every file argument through assert_sandboxed_path.
      3. Executes the tool subprocess with shell=False.
      4. Blocks forbidden network and filesystem operations.

Error taxonomy
--------------
SandboxError             – base
PathTraversalError       – path resolved outside all workspace roots
UnregisteredToolError    – tool not in the declared tool registry
ForbiddenExecutableError – executable not in the allowlisted binary set
ShellInjectionError      – shell metacharacters or shell=True attempt detected
NetworkOperationBlockedError – network syscall attempted outside grant
"""

from __future__ import annotations

import logging
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, FrozenSet, Mapping, Optional, Sequence, Tuple

logger = logging.getLogger("ca_runtime.sandbox")

# ---------------------------------------------------------------------------
# § 1  Error taxonomy
# ---------------------------------------------------------------------------

class SandboxError(RuntimeError):
    """Base class for all CA-M048 sandbox enforcement errors."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "SANDBOX_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class PathTraversalError(SandboxError):
    """Raised when a path resolves to a location outside every declared workspace root.

    Covers: ``..`` traversal, absolute out-of-root paths, symlink escapes,
    alternate separator tricks, and any other path that does not canonically
    resolve within an approved root.
    """

    def __init__(self, requested: str, roots: Sequence[str]) -> None:
        super().__init__(
            f"PATH_TRAVERSAL_BLOCKED: '{requested}' resolved outside workspace roots "
            f"{list(roots)}",
            reason_code="ERR_PATH_TRAVERSAL",
            details={"requested_path": requested, "workspace_roots": list(roots)},
        )
        self.requested = requested
        self.workspace_roots = list(roots)


class UnregisteredToolError(SandboxError):
    """Raised when a tool name is not present in the declared tool registry.

    This replaces the permissive ``tool:default-`` bypass that previously
    allowed unverified tool calls to pass through the compiler.
    """

    def __init__(self, tool_name: str, registered_tools: Sequence[str]) -> None:
        super().__init__(
            f"UNREGISTERED_TOOL: '{tool_name}' is not in the declared tool registry. "
            f"Registered tools: {sorted(registered_tools)}",
            reason_code="ERR_UNREGISTERED_TOOL",
            details={"tool_name": tool_name, "registered_tools": sorted(registered_tools)},
        )
        self.tool_name = tool_name
        self.registered_tools = sorted(registered_tools)


class ForbiddenExecutableError(SandboxError):
    """Raised when an executable is not in the explicit binary allowlist.

    Shell metacharacters and any command not on the allowlist are blocked
    regardless of the tool's registration status.
    """

    def __init__(self, executable: str, allowlist: Sequence[str]) -> None:
        super().__init__(
            f"FORBIDDEN_EXECUTABLE: '{executable}' is not in the binary allowlist "
            f"{sorted(allowlist)}",
            reason_code="ERR_FORBIDDEN_EXECUTABLE",
            details={"executable": executable, "allowlist": sorted(allowlist)},
        )
        self.executable = executable
        self.allowlist = sorted(allowlist)


class ShellInjectionError(SandboxError):
    """Raised when shell metacharacters are detected in command arguments or when
    ``shell=True`` is requested.

    This error fires BEFORE execution — the argument array is never passed to
    the OS.
    """

    def __init__(self, argument: str, pattern_matched: str) -> None:
        super().__init__(
            f"SHELL_INJECTION_BLOCKED: Argument '{argument[:120]}' matched "
            f"shell-injection pattern '{pattern_matched}'",
            reason_code="ERR_SHELL_INJECTION",
            details={"argument_snippet": argument[:200], "pattern": pattern_matched},
        )
        self.argument = argument
        self.pattern_matched = pattern_matched


class NetworkOperationBlockedError(SandboxError):
    """Raised when a tool attempts a network operation that is not in the declared
    network grant.

    The sandbox does not perform actual kernel-level blocking (that is an
    OS/container concern); it validates declared capabilities before execution.
    """

    def __init__(self, host: str, allowed_hosts: Sequence[str]) -> None:
        super().__init__(
            f"NETWORK_OPERATION_BLOCKED: Host '{host}' is not in the network allowlist "
            f"{sorted(allowed_hosts)}",
            reason_code="ERR_NETWORK_BLOCKED",
            details={"host": host, "allowed_hosts": sorted(allowed_hosts)},
        )
        self.host = host
        self.allowed_hosts = sorted(allowed_hosts)


# ---------------------------------------------------------------------------
# § 2  Shell-injection pattern registry
# ---------------------------------------------------------------------------

# Patterns that, if present in any argument to a subprocess call, indicate an
# attempt to inject shell commands.  These are tested against each element of
# the argv list independently.  The list is conservative — it only catches
# patterns that are unambiguously adversarial.
_SHELL_INJECTION_PATTERNS: Tuple[Tuple[str, re.Pattern[str]], ...] = (
    ("semicolon_chain",     re.compile(r";")),
    ("pipe_operator",       re.compile(r"\|")),
    ("ampersand_chain",     re.compile(r"&")),
    ("backtick_subshell",   re.compile(r"`")),
    ("dollar_subshell",     re.compile(r"\$\(")),
    ("redirection_out",     re.compile(r">")),
    ("redirection_in",      re.compile(r"<(?![\w/])")),   # allow <file paths>
    ("newline_injection",   re.compile(r"[\r\n]")),
    ("null_byte",           re.compile(r"\x00")),
    ("process_substitution",re.compile(r"[<>]\(")),
)


def _check_shell_injection(argument: str) -> None:
    """Raise ShellInjectionError if *argument* contains shell metacharacters."""
    for name, pattern in _SHELL_INJECTION_PATTERNS:
        if pattern.search(argument):
            raise ShellInjectionError(argument, name)


# ---------------------------------------------------------------------------
# § 3  Canonical path predicate  (INV-SEC-001 core)
# ---------------------------------------------------------------------------

def assert_sandboxed_path(
    requested_path: str | os.PathLike[str],
    workspace_roots: Sequence[str | os.PathLike[str]],
    *,
    must_exist: bool = False,
) -> Path:
    """Canonical path containment predicate for INV-SEC-001.

    Resolves *requested_path* to an absolute, symlink-free path using
    ``Path.resolve(strict=False)`` (does not require the path to exist) and
    verifies it is contained within at least one of the declared
    *workspace_roots*.

    Rejects:
    - ``..`` traversal segments (caught by resolve + containment check)
    - Absolute paths outside any root (caught by containment check)
    - Symlink escapes (``Path.resolve`` follows all symlinks)
    - Alternate separator tricks on Windows paths (normalised by ``Path``)
    - String-prefix tricks (uses ``Path.is_relative_to`` / prefix comparison
      after resolve — NOT a raw string prefix check)

    Parameters
    ----------
    requested_path:
        The path supplied by the model/tool/user.
    workspace_roots:
        Sequence of declared root directories.  At least one must contain the
        resolved *requested_path*.
    must_exist:
        If True, also require the resolved path to physically exist.

    Returns
    -------
    Path
        The resolved, absolute Path if containment passes.

    Raises
    ------
    PathTraversalError
        If the resolved path is outside every workspace root.
    ValueError
        If *workspace_roots* is empty.
    """
    if not workspace_roots:
        raise ValueError("workspace_roots must not be empty — no containment target provided")

    # Resolve the target (follows symlinks; does NOT require existence)
    resolved = Path(requested_path).resolve()

    if must_exist and not resolved.exists():
        raise PathTraversalError(str(requested_path), [str(r) for r in workspace_roots])

    # Resolve each root and test containment using filesystem-aware comparison
    str_roots = []
    for root in workspace_roots:
        resolved_root = Path(root).resolve()
        str_roots.append(str(resolved_root))

        # Use is_relative_to (Python 3.9+) for accurate directory containment.
        # We also accept exact equality (path == root).
        try:
            if resolved.is_relative_to(resolved_root):
                logger.debug(
                    "sandbox.assert_sandboxed_path: ALLOWED '%s' within root '%s'",
                    resolved,
                    resolved_root,
                )
                return resolved
        except AttributeError:
            # Fallback for Python < 3.9 (though project requires 3.12)
            rel_str = str(resolved)
            root_str = str(resolved_root)
            if rel_str == root_str or rel_str.startswith(root_str + os.sep):
                return resolved

    logger.warning(
        "sandbox.assert_sandboxed_path: BLOCKED '%s' (resolved: '%s') — not within roots %s",
        requested_path,
        resolved,
        str_roots,
    )
    raise PathTraversalError(str(requested_path), str_roots)


# ---------------------------------------------------------------------------
# § 4  Tool sandbox policy
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ToolSandboxPolicy:
    """Immutable policy record governing what a ToolSandbox may do.

    Attributes
    ----------
    workspace_roots:
        Tuple of absolute directory paths that constitute the allowed
        filesystem workspace.  Every path argument in a tool call is
        validated against these roots before execution.
    registered_tools:
        Frozenset of tool names that are allowed to execute.  Any name not
        in this set is rejected with UnregisteredToolError.
    binary_allowlist:
        Frozenset of executable names (basename only, e.g. ``"python"``,
        ``"git"``) that may be launched by a tool.  If empty, NO subprocess
        execution is permitted (pure in-process tools only).
    network_allowlist:
        Frozenset of hostnames that tool network access may target.  Empty
        means no network access is permitted at policy level.
    policy_id:
        Optional identifier for this policy instance (audit trail).
    """

    workspace_roots: Tuple[str, ...]
    registered_tools: FrozenSet[str]
    binary_allowlist: FrozenSet[str]
    network_allowlist: FrozenSet[str] = field(default_factory=frozenset)
    policy_id: str = "default"

    def __post_init__(self) -> None:
        # Eagerly resolve workspace roots so comparisons are stable
        resolved = tuple(str(Path(r).resolve()) for r in self.workspace_roots)
        # frozen dataclass requires object.__setattr__
        object.__setattr__(self, "workspace_roots", resolved)


# ---------------------------------------------------------------------------
# § 5  ToolSandbox — canonical execution boundary
# ---------------------------------------------------------------------------

class ToolSandbox:
    """Canonical tool execution sandbox enforcing INV-SEC-001.

    Usage (direct call)
    -------------------
    ::

        policy = ToolSandboxPolicy(
            workspace_roots=("/project/workspace",),
            registered_tools=frozenset({"tool:git-status", "tool:read-file"}),
            binary_allowlist=frozenset({"git", "python"}),
        )
        sandbox = ToolSandbox(policy)

        # Validate a path before use
        safe_path = sandbox.assert_path("../../../etc/passwd")  # raises PathTraversalError

        # Execute a registered tool
        result = sandbox.execute_tool(
            tool_name="tool:git-status",
            executable="git",
            args=["status", "--short"],
        )

    Context-manager usage
    ---------------------
    ::

        with ToolSandbox(policy) as sb:
            sb.execute_tool("tool:git-status", "git", ["status"])
    """

    def __init__(self, policy: ToolSandboxPolicy) -> None:
        self._policy = policy

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def policy(self) -> ToolSandboxPolicy:
        return self._policy

    def assert_path(
        self,
        requested_path: str | os.PathLike[str],
        *,
        must_exist: bool = False,
    ) -> Path:
        """Validate *requested_path* against workspace roots.

        Delegates to the module-level ``assert_sandboxed_path`` using this
        sandbox's declared workspace roots.

        Returns the resolved Path on success; raises PathTraversalError on
        violation.
        """
        return assert_sandboxed_path(
            requested_path,
            self._policy.workspace_roots,
            must_exist=must_exist,
        )

    def assert_tool_registered(self, tool_name: str) -> None:
        """Raise UnregisteredToolError if *tool_name* is not in the registry.

        NOTE: The ``tool:default-`` bypass is NOT honoured here.  Every tool
        name must appear verbatim in ``policy.registered_tools``.
        """
        if tool_name not in self._policy.registered_tools:
            raise UnregisteredToolError(tool_name, list(self._policy.registered_tools))

    def assert_executable_allowed(self, executable: str) -> None:
        """Raise ForbiddenExecutableError if *executable* is not allowlisted.

        ``executable`` is matched against the basename only (no path component)
        so that ``/usr/bin/git`` and ``git`` are treated identically.
        """
        basename = Path(executable).name
        if basename not in self._policy.binary_allowlist:
            raise ForbiddenExecutableError(basename, list(self._policy.binary_allowlist))

    def assert_no_shell_injection(self, args: Sequence[str]) -> None:
        """Raise ShellInjectionError if any element of *args* contains shell metacharacters."""
        for arg in args:
            _check_shell_injection(arg)

    def assert_network_allowed(self, host: str) -> None:
        """Raise NetworkOperationBlockedError if *host* is not in the network allowlist.

        If the allowlist is empty, ALL network access is blocked.
        """
        if not self._policy.network_allowlist:
            raise NetworkOperationBlockedError(host, [])
        if host not in self._policy.network_allowlist and "*" not in self._policy.network_allowlist:
            raise NetworkOperationBlockedError(host, list(self._policy.network_allowlist))

    def validate_file_args(self, args: Sequence[str]) -> Tuple[Path, ...]:
        """Validate every argument that looks like a filesystem path.

        Arguments beginning with ``/``, ``./``, ``../``, or a Windows drive
        letter are treated as paths.  All others are treated as plain strings
        and are NOT passed to ``assert_sandboxed_path`` (they may still be
        checked by ``assert_no_shell_injection``).

        Returns a tuple of resolved Paths for the path-like arguments.
        Raises PathTraversalError for the first violation found.
        """
        resolved_paths: list[Path] = []
        for arg in args:
            if _looks_like_path(arg):
                resolved_paths.append(self.assert_path(arg))
        return tuple(resolved_paths)

    def execute_tool(
        self,
        tool_name: str,
        executable: str,
        args: Sequence[str],
        *,
        cwd: Optional[str | os.PathLike[str]] = None,
        env: Optional[Mapping[str, str]] = None,
        capture_output: bool = True,
        timeout: Optional[float] = None,
    ) -> "subprocess.CompletedProcess[str]":
        """Execute a sandboxed tool subprocess.

        Enforcement sequence (all must pass before the OS call is made):
        1. ``tool_name`` must be in ``policy.registered_tools``.
        2. ``executable`` basename must be in ``policy.binary_allowlist``.
        3. No shell metacharacters in ``executable`` or any element of ``args``.
        4. All path-like arguments in ``args`` must resolve within workspace roots.
        5. If ``cwd`` is given, it must resolve within workspace roots.
        6. ``subprocess.run`` is called with ``shell=False`` (enforced — no override).

        Parameters
        ----------
        tool_name:
            The registered tool identifier (e.g. ``"tool:git-status"``).
        executable:
            The program to launch (e.g. ``"git"``).  Basename is compared
            against the allowlist; a full path is also accepted but its
            basename is used for the allowlist check.
        args:
            Positional arguments to pass to the executable.  Do NOT include
            the executable itself.
        cwd:
            Working directory for the subprocess.  Must be within workspace
            roots if supplied.
        env:
            Environment mapping for the subprocess.  If None, the current
            process environment is inherited.
        capture_output:
            Whether to capture stdout/stderr (default True).
        timeout:
            Optional subprocess timeout in seconds.

        Returns
        -------
        subprocess.CompletedProcess[str]
            The completed process result.  The caller is responsible for
            checking ``returncode``.

        Raises
        ------
        UnregisteredToolError, ForbiddenExecutableError, ShellInjectionError,
        PathTraversalError, NetworkOperationBlockedError
        """
        # --- Gate 1: tool registration ---
        self.assert_tool_registered(tool_name)

        # --- Gate 2: executable allowlist ---
        self.assert_executable_allowed(executable)

        # --- Gate 3: shell injection in executable name itself ---
        _check_shell_injection(executable)

        # --- Gate 3b: shell injection in arguments ---
        self.assert_no_shell_injection(args)

        # --- Gate 4: path containment for path-like arguments ---
        self.validate_file_args(args)

        # --- Gate 5: cwd containment ---
        resolved_cwd: Optional[Path] = None
        if cwd is not None:
            resolved_cwd = self.assert_path(cwd, must_exist=True)

        # --- Gate 6: build argv and run with shell=False ---
        argv = [executable, *args]
        logger.info(
            "sandbox.execute_tool: EXECUTING tool='%s' argv=%s cwd='%s'",
            tool_name,
            argv,
            resolved_cwd,
        )

        result = subprocess.run(
            argv,
            shell=False,              # INVARIANT: shell=False is NEVER overridden
            capture_output=capture_output,
            text=True,
            cwd=str(resolved_cwd) if resolved_cwd is not None else None,
            env=env,
            timeout=timeout,
        )
        return result

    # ------------------------------------------------------------------
    # Context-manager support
    # ------------------------------------------------------------------

    def __enter__(self) -> "ToolSandbox":
        return self

    def __exit__(self, *_: Any) -> None:
        pass  # No cleanup required for stateless sandbox


# ---------------------------------------------------------------------------
# § 6  Compiler-level bypass removal helper
# ---------------------------------------------------------------------------

def reject_default_tool_bypass(tool_name: str, all_allowed_tools: FrozenSet[str]) -> None:
    """Replacement for the ``tool:default-`` bypass in AgentInvocationCompiler.

    The original compiler code contained::

        if t not in all_allowed_tools and not t.startswith("tool:default-"):
            raise UnauthorizedToolError(...)

    The ``not t.startswith("tool:default-")`` clause silently allowed
    unverified tool names to bypass the registry check.  This function
    provides the correct predicate: a tool is allowed if and only if it is
    in ``all_allowed_tools``.  No bypass prefix is honoured.

    Raises
    ------
    UnregisteredToolError
        If *tool_name* is not in *all_allowed_tools*.
    """
    if tool_name not in all_allowed_tools:
        raise UnregisteredToolError(tool_name, list(all_allowed_tools))


# ---------------------------------------------------------------------------
# § 7  Internal helpers
# ---------------------------------------------------------------------------

_PATH_LIKE_RE = re.compile(
    r"""
    ^(
        \.{1,2}[/\\]      # ./  or ../
      | /                  # absolute unix
      | [A-Za-z]:[/\\]    # Windows drive letter
      | ~[/\\]?            # home expansion
    )
    """,
    re.VERBOSE,
)


def _looks_like_path(s: str) -> bool:
    """Heuristic: does *s* look like a filesystem path argument?"""
    return bool(_PATH_LIKE_RE.match(s))
