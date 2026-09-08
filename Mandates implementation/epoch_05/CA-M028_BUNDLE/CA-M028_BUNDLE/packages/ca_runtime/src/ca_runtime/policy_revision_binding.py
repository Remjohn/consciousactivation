"""Policy Revision Binding for Conscious Activation Engine (CAE).

Mandate: CA-M028 / Q27 / FR-POL-002 / INV-POL-001
Stage: 12 Human Authorization

Binds active policy revision hashes (identity digests) directly to program
execution leases and dispatch payloads. An in-flight execution remains pinned
to the exact policy revision under which it was authorized. Later campaign
policy changes are prospective only and do not rebind active executions.

Critical invariants:
- Execution-bound policy != current campaign prospective policy.
- Historical policy revisions remain immutable and addressable.
- Drift or stale/unknown revision snapshots fail closed and abort the
  in-flight execution lease / dispatch path.
- Binding is durable for the lifetime of the execution record; restart
  recovery reloads the bound digest without reading live campaign policy.

State grammar:
  UNBOUND
    → bind(policy revision digest) at lease/dispatch creation
    → BOUND (execution_id, lease_id, policy_identity_digest, revision)
    → (optional) DRIFT_DETECTED → ABORTED (fail-closed)
    → COMPLETED / TERMINAL (binding retained for audit)

Prohibitions (mandate-scoped):
- Do not mutate historical policy packages or authorization receipts.
- Do not rebind an active execution to a newer prospective revision.
- Do not invent release / distribution / outcome authority.
"""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.policy_package import (
    LoadedPolicyPackage,
    PolicyPackageError,
    PolicyPackageNotFoundError,
    PolicyPackageRegistry,
    get_policy_package_registry,
)

logger = logging.getLogger("ca_runtime.policy_revision_binding")


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BINDING_SCHEMA_ID = "cae.policy_revision_binding"
BINDING_SCHEMA_VERSION = "1.0.0"

# Payload keys injected into lease / dispatch envelopes
LEASE_POLICY_BINDING_KEY = "policy_revision_binding"
DISPATCH_POLICY_BINDING_KEY = "policy_revision_binding"


# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class PolicyRevisionBindingError(RuntimeError):
    """Base error for policy-revision ↔ execution binding violations."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "POLICY_REVISION_BINDING_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class PolicyDriftDetectedError(PolicyRevisionBindingError):
    """Raised when the bound policy digest no longer matches the registry
    snapshot or a prospective campaign policy has been applied to an
    in-flight execution."""

    def __init__(
        self,
        execution_id: str,
        bound_digest: str,
        observed_digest: Optional[str],
        reason: str = "",
    ):
        super().__init__(
            f"POLICY_DRIFT_DETECTED: Execution '{execution_id}' is bound to "
            f"policy digest {bound_digest[:16]}… but observed "
            f"{(observed_digest or 'MISSING')[:16]}…. {reason}".strip(),
            reason_code="POLICY_DRIFT_DETECTED",
            details={
                "execution_id": execution_id,
                "bound_digest": bound_digest,
                "observed_digest": observed_digest,
                "reason": reason,
            },
        )
        self.execution_id = execution_id
        self.bound_digest = bound_digest
        self.observed_digest = observed_digest


class StalePolicySnapshotError(PolicyRevisionBindingError):
    """Raised when a binding references a revision that is no longer
    resolvable or whose content has changed under the same identity key."""

    def __init__(
        self,
        execution_id: str,
        package_id: str,
        version: Optional[str],
        revision: Optional[int],
        reason: str = "",
    ):
        super().__init__(
            f"STALE_POLICY_SNAPSHOT: Execution '{execution_id}' references "
            f"policy {package_id}@{version or '?'} rev={revision} which is "
            f"unresolvable or mutated. {reason}".strip(),
            reason_code="STALE_POLICY_SNAPSHOT",
            details={
                "execution_id": execution_id,
                "package_id": package_id,
                "version": version,
                "revision": revision,
                "reason": reason,
            },
        )


class BindingNotFoundError(PolicyRevisionBindingError):
    """Raised when no binding exists for the requested execution / lease."""

    def __init__(self, execution_id: str):
        super().__init__(
            f"BINDING_NOT_FOUND: No policy revision binding for execution '{execution_id}'",
            reason_code="BINDING_NOT_FOUND",
            details={"execution_id": execution_id},
        )


class BindingAlreadyExistsError(PolicyRevisionBindingError):
    """Raised when an attempt is made to rebind an already-bound active execution."""

    def __init__(self, execution_id: str, existing_digest: str):
        super().__init__(
            f"BINDING_ALREADY_EXISTS: Execution '{execution_id}' is already "
            f"bound to digest {existing_digest[:16]}…; rebinding is prohibited",
            reason_code="BINDING_ALREADY_EXISTS",
            details={
                "execution_id": execution_id,
                "existing_digest": existing_digest,
            },
        )


class BindingAbortedError(PolicyRevisionBindingError):
    """Raised when an operation is attempted against an already-aborted binding."""

    def __init__(self, execution_id: str, abort_reason: str):
        super().__init__(
            f"BINDING_ABORTED: Execution '{execution_id}' was previously "
            f"aborted due to policy drift/stale snapshot: {abort_reason}",
            reason_code="BINDING_ABORTED",
            details={"execution_id": execution_id, "abort_reason": abort_reason},
        )


# ---------------------------------------------------------------------------
# Status enum
# ---------------------------------------------------------------------------

class BindingStatus(str, Enum):
    BOUND = "BOUND"
    DRIFT_DETECTED = "DRIFT_DETECTED"
    ABORTED = "ABORTED"
    COMPLETED = "COMPLETED"


# ---------------------------------------------------------------------------
# Core record
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PolicyRevisionBinding:
    """Immutable execution ↔ policy-revision binding record.

    The identity_digest is the canonical sha256 of the normalized policy
    package body at the moment of binding. It is the sole authority for
    subsequent authorization decisions on this execution.
    """

    binding_id: str
    execution_id: str  # typically aggregate_id
    lease_id: Optional[str]
    program_id: str
    package_id: str
    package_version: str
    revision: int
    identity_digest: str
    bound_at: str  # RFC3339
    status: BindingStatus = BindingStatus.BOUND
    abort_reason: Optional[str] = None
    aborted_at: Optional[str] = None
    # Optional campaign prospective pointer at bind time (for audit contrast)
    campaign_prospective_digest_at_bind: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_id": BINDING_SCHEMA_ID,
            "schema_version": BINDING_SCHEMA_VERSION,
            "binding_id": self.binding_id,
            "execution_id": self.execution_id,
            "lease_id": self.lease_id,
            "program_id": self.program_id,
            "package_id": self.package_id,
            "package_version": self.package_version,
            "revision": self.revision,
            "identity_digest": self.identity_digest,
            "bound_at": self.bound_at,
            "status": self.status.value,
            "abort_reason": self.abort_reason,
            "aborted_at": self.aborted_at,
            "campaign_prospective_digest_at_bind": self.campaign_prospective_digest_at_bind,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "PolicyRevisionBinding":
        return cls(
            binding_id=str(data["binding_id"]),
            execution_id=str(data["execution_id"]),
            lease_id=data.get("lease_id"),
            program_id=str(data["program_id"]),
            package_id=str(data["package_id"]),
            package_version=str(data["package_version"]),
            revision=int(data["revision"]),
            identity_digest=str(data["identity_digest"]),
            bound_at=str(data["bound_at"]),
            status=BindingStatus(data.get("status", BindingStatus.BOUND.value)),
            abort_reason=data.get("abort_reason"),
            aborted_at=data.get("aborted_at"),
            campaign_prospective_digest_at_bind=data.get("campaign_prospective_digest_at_bind"),
            metadata=dict(data.get("metadata") or {}),
        )


# ---------------------------------------------------------------------------
# Registry (process-scoped, thread-safe, revision-preserving)
# ---------------------------------------------------------------------------

class PolicyRevisionBindingRegistry:
    """In-memory durable registry of execution → policy revision bindings.

    Bindings are append-only with respect to identity: an execution may be
    bound exactly once while BOUND. Status transitions to DRIFT_DETECTED /
    ABORTED / COMPLETED are allowed; rebinding to a different digest is not.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._by_execution: Dict[str, PolicyRevisionBinding] = {}
        self._history: List[PolicyRevisionBinding] = []  # all transitions

    def bind(
        self,
        *,
        execution_id: str,
        program_id: str,
        loaded_package: LoadedPolicyPackage,
        lease_id: Optional[str] = None,
        campaign_prospective_digest: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        binding_id: Optional[str] = None,
        bound_at: Optional[str] = None,
        allow_rebind_if_aborted: bool = False,
    ) -> PolicyRevisionBinding:
        """Create an immutable binding of the given execution to the package revision.

        Raises BindingAlreadyExistsError if a live (BOUND) binding already exists.
        """
        with self._lock:
            existing = self._by_execution.get(execution_id)
            if existing is not None:
                if existing.status == BindingStatus.BOUND:
                    raise BindingAlreadyExistsError(
                        execution_id, existing.identity_digest
                    )
                if existing.status == BindingStatus.ABORTED and not allow_rebind_if_aborted:
                    raise BindingAbortedError(
                        execution_id, existing.abort_reason or "prior abort"
                    )
                # COMPLETED or DRIFT_DETECTED without explicit rebind permission → refuse
                if existing.status in (
                    BindingStatus.COMPLETED,
                    BindingStatus.DRIFT_DETECTED,
                ) and not allow_rebind_if_aborted:
                    raise BindingAlreadyExistsError(
                        execution_id, existing.identity_digest
                    )

            bid = binding_id or f"prb-{execution_id}-{loaded_package.identity_digest[:12]}"
            ts = bound_at or utc_now_rfc3339()
            record = PolicyRevisionBinding(
                binding_id=bid,
                execution_id=execution_id,
                lease_id=lease_id,
                program_id=program_id,
                package_id=loaded_package.manifest.package_id,
                package_version=loaded_package.manifest.version,
                revision=loaded_package.revision,
                identity_digest=loaded_package.identity_digest,
                bound_at=ts,
                status=BindingStatus.BOUND,
                campaign_prospective_digest_at_bind=campaign_prospective_digest,
                metadata=dict(metadata or {}),
            )
            self._by_execution[execution_id] = record
            self._history.append(record)
            logger.info(
                "Bound execution %s to policy %s@%s rev=%s digest=%s",
                execution_id,
                record.package_id,
                record.package_version,
                record.revision,
                record.identity_digest[:12],
            )
            return record

    def get(self, execution_id: str) -> PolicyRevisionBinding:
        with self._lock:
            rec = self._by_execution.get(execution_id)
            if rec is None:
                raise BindingNotFoundError(execution_id)
            return rec

    def get_optional(self, execution_id: str) -> Optional[PolicyRevisionBinding]:
        with self._lock:
            return self._by_execution.get(execution_id)

    def list_bindings(
        self,
        *,
        program_id: Optional[str] = None,
        status: Optional[BindingStatus] = None,
    ) -> List[PolicyRevisionBinding]:
        with self._lock:
            out = list(self._by_execution.values())
            if program_id is not None:
                out = [b for b in out if b.program_id == program_id]
            if status is not None:
                out = [b for b in out if b.status == status]
            return out

    def history(self, execution_id: Optional[str] = None) -> List[PolicyRevisionBinding]:
        with self._lock:
            if execution_id is None:
                return list(self._history)
            return [h for h in self._history if h.execution_id == execution_id]

    def mark_drift(
        self,
        execution_id: str,
        *,
        reason: str,
        observed_digest: Optional[str] = None,
    ) -> PolicyRevisionBinding:
        """Transition BOUND → DRIFT_DETECTED (does not yet abort)."""
        with self._lock:
            rec = self.get(execution_id)
            if rec.status == BindingStatus.ABORTED:
                raise BindingAbortedError(execution_id, rec.abort_reason or "")
            if rec.status == BindingStatus.COMPLETED:
                raise PolicyRevisionBindingError(
                    f"Cannot mark drift on COMPLETED binding for {execution_id}",
                    reason_code="INVALID_STATUS_TRANSITION",
                    details={"execution_id": execution_id, "status": rec.status.value},
                )
            updated = PolicyRevisionBinding(
                binding_id=rec.binding_id,
                execution_id=rec.execution_id,
                lease_id=rec.lease_id,
                program_id=rec.program_id,
                package_id=rec.package_id,
                package_version=rec.package_version,
                revision=rec.revision,
                identity_digest=rec.identity_digest,
                bound_at=rec.bound_at,
                status=BindingStatus.DRIFT_DETECTED,
                abort_reason=reason,
                aborted_at=None,
                campaign_prospective_digest_at_bind=rec.campaign_prospective_digest_at_bind,
                metadata={
                    **rec.metadata,
                    "observed_digest": observed_digest,
                    "drift_detected_at": utc_now_rfc3339(),
                },
            )
            self._by_execution[execution_id] = updated
            self._history.append(updated)
            return updated

    def abort(
        self,
        execution_id: str,
        *,
        reason: str,
        observed_digest: Optional[str] = None,
    ) -> PolicyRevisionBinding:
        """Transition to ABORTED (fail-closed). Idempotent if already ABORTED."""
        with self._lock:
            rec = self.get(execution_id)
            if rec.status == BindingStatus.ABORTED:
                return rec
            ts = utc_now_rfc3339()
            updated = PolicyRevisionBinding(
                binding_id=rec.binding_id,
                execution_id=rec.execution_id,
                lease_id=rec.lease_id,
                program_id=rec.program_id,
                package_id=rec.package_id,
                package_version=rec.package_version,
                revision=rec.revision,
                identity_digest=rec.identity_digest,
                bound_at=rec.bound_at,
                status=BindingStatus.ABORTED,
                abort_reason=reason,
                aborted_at=ts,
                campaign_prospective_digest_at_bind=rec.campaign_prospective_digest_at_bind,
                metadata={
                    **rec.metadata,
                    "observed_digest": observed_digest,
                    "aborted_at": ts,
                },
            )
            self._by_execution[execution_id] = updated
            self._history.append(updated)
            logger.warning(
                "Aborted execution %s due to policy drift/stale snapshot: %s",
                execution_id,
                reason,
            )
            return updated

    def complete(self, execution_id: str) -> PolicyRevisionBinding:
        """Mark a successful terminal binding (audit retention)."""
        with self._lock:
            rec = self.get(execution_id)
            if rec.status == BindingStatus.ABORTED:
                raise BindingAbortedError(execution_id, rec.abort_reason or "")
            updated = PolicyRevisionBinding(
                binding_id=rec.binding_id,
                execution_id=rec.execution_id,
                lease_id=rec.lease_id,
                program_id=rec.program_id,
                package_id=rec.package_id,
                package_version=rec.package_version,
                revision=rec.revision,
                identity_digest=rec.identity_digest,
                bound_at=rec.bound_at,
                status=BindingStatus.COMPLETED,
                abort_reason=None,
                aborted_at=None,
                campaign_prospective_digest_at_bind=rec.campaign_prospective_digest_at_bind,
                metadata={**rec.metadata, "completed_at": utc_now_rfc3339()},
            )
            self._by_execution[execution_id] = updated
            self._history.append(updated)
            return updated

    def clear(self) -> None:
        """Test helper: reset registry."""
        with self._lock:
            self._by_execution.clear()
            self._history.clear()


# Module-level default registry
_default_binding_registry: Optional[PolicyRevisionBindingRegistry] = None


def get_policy_revision_binding_registry() -> PolicyRevisionBindingRegistry:
    global _default_binding_registry
    if _default_binding_registry is None:
        _default_binding_registry = PolicyRevisionBindingRegistry()
    return _default_binding_registry


def reset_policy_revision_binding_registry() -> None:
    """Test helper: clear the default binding registry."""
    global _default_binding_registry
    _default_binding_registry = PolicyRevisionBindingRegistry()


# ---------------------------------------------------------------------------
# Binding operations (public API)
# ---------------------------------------------------------------------------

def bind_policy_revision_to_execution(
    *,
    execution_id: str,
    program_id: str,
    package_id: str,
    package_version: Optional[str] = None,
    lease_id: Optional[str] = None,
    registry: Optional[PolicyPackageRegistry] = None,
    binding_registry: Optional[PolicyRevisionBindingRegistry] = None,
    campaign_prospective_digest: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> PolicyRevisionBinding:
    """Resolve the named policy package and bind its immutable revision to the execution.

    This is the canonical entry point at lease acquisition / dispatch creation.
    """
    pkg_reg = registry or get_policy_package_registry()
    bind_reg = binding_registry or get_policy_revision_binding_registry()
    try:
        loaded = pkg_reg.get(package_id, package_version)
    except PolicyPackageNotFoundError as e:
        raise StalePolicySnapshotError(
            execution_id=execution_id,
            package_id=package_id,
            version=package_version,
            revision=None,
            reason=str(e),
        ) from e

    return bind_reg.bind(
        execution_id=execution_id,
        program_id=program_id,
        loaded_package=loaded,
        lease_id=lease_id,
        campaign_prospective_digest=campaign_prospective_digest,
        metadata=metadata,
    )


def bind_loaded_package_to_execution(
    *,
    execution_id: str,
    program_id: str,
    loaded_package: LoadedPolicyPackage,
    lease_id: Optional[str] = None,
    binding_registry: Optional[PolicyRevisionBindingRegistry] = None,
    campaign_prospective_digest: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> PolicyRevisionBinding:
    """Bind an already-loaded package instance to the execution (no registry lookup)."""
    bind_reg = binding_registry or get_policy_revision_binding_registry()
    return bind_reg.bind(
        execution_id=execution_id,
        program_id=program_id,
        loaded_package=loaded_package,
        lease_id=lease_id,
        campaign_prospective_digest=campaign_prospective_digest,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Lease / Dispatch payload attachment
# ---------------------------------------------------------------------------

def attach_binding_to_lease_payload(
    lease_payload: Dict[str, Any],
    binding: PolicyRevisionBinding,
) -> Dict[str, Any]:
    """Inject the policy revision binding into an execution lease envelope.

    Returns a new dict; does not mutate the original.
    """
    out = dict(lease_payload)
    out[LEASE_POLICY_BINDING_KEY] = binding.to_dict()
    # Also surface the digest at the top level for fast CAS / CAS-friendly checks
    out["bound_policy_identity_digest"] = binding.identity_digest
    out["bound_policy_package_id"] = binding.package_id
    out["bound_policy_revision"] = binding.revision
    return out


def attach_binding_to_dispatch_payload(
    dispatch_payload: Dict[str, Any],
    binding: PolicyRevisionBinding,
) -> Dict[str, Any]:
    """Inject the policy revision binding into a workflow dispatch payload.

    Returns a new dict; does not mutate the original.
    """
    out = dict(dispatch_payload)
    out[DISPATCH_POLICY_BINDING_KEY] = binding.to_dict()
    out["bound_policy_identity_digest"] = binding.identity_digest
    out["bound_policy_package_id"] = binding.package_id
    out["bound_policy_revision"] = binding.revision
    return out


def extract_binding_from_payload(
    payload: Mapping[str, Any],
) -> Optional[PolicyRevisionBinding]:
    """Recover a PolicyRevisionBinding from a lease or dispatch payload if present."""
    raw = payload.get(LEASE_POLICY_BINDING_KEY) or payload.get(DISPATCH_POLICY_BINDING_KEY)
    if raw is None:
        return None
    if isinstance(raw, PolicyRevisionBinding):
        return raw
    if isinstance(raw, Mapping):
        return PolicyRevisionBinding.from_dict(raw)
    return None


# ---------------------------------------------------------------------------
# Drift detection & abort
# ---------------------------------------------------------------------------

def resolve_bound_package(
    binding: PolicyRevisionBinding,
    *,
    registry: Optional[PolicyPackageRegistry] = None,
) -> LoadedPolicyPackage:
    """Re-resolve the exact package revision that was bound.

    Fails closed if the revision is missing or the digest no longer matches.
    """
    pkg_reg = registry or get_policy_package_registry()
    try:
        loaded = pkg_reg.get(binding.package_id, binding.package_version)
    except PolicyPackageNotFoundError as e:
        raise StalePolicySnapshotError(
            execution_id=binding.execution_id,
            package_id=binding.package_id,
            version=binding.package_version,
            revision=binding.revision,
            reason=str(e),
        ) from e

    if loaded.identity_digest != binding.identity_digest:
        raise PolicyDriftDetectedError(
            execution_id=binding.execution_id,
            bound_digest=binding.identity_digest,
            observed_digest=loaded.identity_digest,
            reason=(
                f"Registry package {binding.package_id}@{binding.package_version} "
                f"now has digest {loaded.identity_digest[:16]}…; bound digest differs"
            ),
        )
    if loaded.revision != binding.revision:
        # Same version string but revision counter diverged — treat as drift
        raise PolicyDriftDetectedError(
            execution_id=binding.execution_id,
            bound_digest=binding.identity_digest,
            observed_digest=loaded.identity_digest,
            reason=(
                f"Revision counter mismatch: bound rev={binding.revision}, "
                f"registry rev={loaded.revision}"
            ),
        )
    return loaded


def check_binding_integrity(
    execution_id: str,
    *,
    binding_registry: Optional[PolicyRevisionBindingRegistry] = None,
    package_registry: Optional[PolicyPackageRegistry] = None,
    prospective_campaign_digest: Optional[str] = None,
) -> PolicyRevisionBinding:
    """Verify that the binding is still valid and the bound package is immutable.

    - Missing binding → BindingNotFoundError
    - Already ABORTED → BindingAbortedError
    - Package missing / digest mismatch → raises Stale/Drift (does not auto-abort)
    - Optional: if prospective_campaign_digest is supplied and differs from the
      bound digest, this is *not* drift for the active execution (prospective
      only). The function records the contrast in metadata for audit but does
      not fail.

    Returns the current binding on success.
    """
    bind_reg = binding_registry or get_policy_revision_binding_registry()
    binding = bind_reg.get(execution_id)

    if binding.status == BindingStatus.ABORTED:
        raise BindingAbortedError(execution_id, binding.abort_reason or "prior abort")

    # Re-resolve and enforce digest equality
    resolve_bound_package(binding, registry=package_registry)

    # Prospective contrast is informational only
    if (
        prospective_campaign_digest is not None
        and prospective_campaign_digest != binding.identity_digest
    ):
        logger.info(
            "Prospective campaign policy digest %s differs from bound %s for "
            "execution %s (expected; prospective-only semantics)",
            prospective_campaign_digest[:12],
            binding.identity_digest[:12],
            execution_id,
        )

    return binding


def detect_and_abort_on_drift(
    execution_id: str,
    *,
    binding_registry: Optional[PolicyRevisionBindingRegistry] = None,
    package_registry: Optional[PolicyPackageRegistry] = None,
    force_observed_digest: Optional[str] = None,
) -> PolicyRevisionBinding:
    """Check integrity; on drift or stale snapshot, mark DRIFT then ABORT.

    Returns the (possibly aborted) binding.
    Raises BindingNotFoundError if no binding exists.
    """
    bind_reg = binding_registry or get_policy_revision_binding_registry()
    binding = bind_reg.get(execution_id)

    if binding.status == BindingStatus.ABORTED:
        return binding

    try:
        if force_observed_digest is not None:
            if force_observed_digest != binding.identity_digest:
                raise PolicyDriftDetectedError(
                    execution_id=execution_id,
                    bound_digest=binding.identity_digest,
                    observed_digest=force_observed_digest,
                    reason="Forced observed digest mismatch (test / external signal)",
                )
        else:
            resolve_bound_package(binding, registry=package_registry)
        return binding
    except (PolicyDriftDetectedError, StalePolicySnapshotError) as exc:
        reason = str(exc)
        observed = getattr(exc, "observed_digest", None)
        bind_reg.mark_drift(
            execution_id,
            reason=reason,
            observed_digest=observed,
        )
        return bind_reg.abort(
            execution_id,
            reason=reason,
            observed_digest=observed,
        )


def require_live_binding(
    execution_id: str,
    *,
    binding_registry: Optional[PolicyRevisionBindingRegistry] = None,
    package_registry: Optional[PolicyPackageRegistry] = None,
) -> PolicyRevisionBinding:
    """Fail-closed gate used by dispatch / authorization paths.

    Ensures a BOUND binding exists, the package is still resolvable with the
    exact digest, and the binding has not been aborted.
    """
    bind_reg = binding_registry or get_policy_revision_binding_registry()
    binding = check_binding_integrity(
        execution_id,
        binding_registry=bind_reg,
        package_registry=package_registry,
    )
    if binding.status != BindingStatus.BOUND:
        raise PolicyRevisionBindingError(
            f"Execution '{execution_id}' binding status is {binding.status.value}; "
            f"live authorization requires BOUND",
            reason_code="BINDING_NOT_LIVE",
            details={
                "execution_id": execution_id,
                "status": binding.status.value,
                "abort_reason": binding.abort_reason,
            },
        )
    return binding


# ---------------------------------------------------------------------------
# Helpers for contrastive / prospective scenarios
# ---------------------------------------------------------------------------

def contrast_bound_vs_prospective(
    execution_id: str,
    prospective_digest: str,
    *,
    binding_registry: Optional[PolicyRevisionBindingRegistry] = None,
) -> Dict[str, Any]:
    """Return an audit record showing that the active execution remains on its
    bound revision while the campaign prospective digest has moved.

    This is the key contrastive proof required by CA-M028 / Q27.
    """
    bind_reg = binding_registry or get_policy_revision_binding_registry()
    binding = bind_reg.get(execution_id)
    return {
        "execution_id": execution_id,
        "bound_identity_digest": binding.identity_digest,
        "bound_package_id": binding.package_id,
        "bound_package_version": binding.package_version,
        "bound_revision": binding.revision,
        "bound_status": binding.status.value,
        "prospective_campaign_digest": prospective_digest,
        "digests_differ": binding.identity_digest != prospective_digest,
        "prospective_only": True,
        "evaluated_at": utc_now_rfc3339(),
    }


def binding_digest_for_payload(binding: PolicyRevisionBinding) -> str:
    """Canonical digest of the binding record itself (for receipt chaining)."""
    body = {
        "binding_id": binding.binding_id,
        "execution_id": binding.execution_id,
        "package_id": binding.package_id,
        "package_version": binding.package_version,
        "revision": binding.revision,
        "identity_digest": binding.identity_digest,
        "bound_at": binding.bound_at,
    }
    return canonical_sha256(canonical_json_text(body))
