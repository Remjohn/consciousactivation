from __future__ import annotations

from datetime import timedelta
from hashlib import sha256
import json
from pathlib import Path

from cmf_builder.adapters.file_evidence_workspace import FileEvidenceWorkspace
from cmf_builder.adapters.in_memory_run_repository import DeterministicUuid7IdProvider
from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.application.evidence_commands import (
    EvidenceWorkspaceCommandService,
    LockEvidenceWorkspaceCommand,
)
from cmf_builder.domain.evidence_workspace import (
    SourceProfile,
    deterministic_tree_hash,
)
from tests.stories.st_01_01_synthetic_proof import (
    NOW,
    ROOT,
    build_service as build_run_service,
    create_command as create_run_command,
)


def build_context(*, root: Path = ROOT):
    run_service, repository, observations, clock, _ = build_run_service(root=root)
    run_receipt = run_service.create_run(create_run_command())
    actors = (
        Actor("architect-1", ActorKind.HUMAN),
        Actor("code-1", ActorKind.CODE),
        Actor("agent-1", ActorKind.AGENT),
        Actor("external-1", ActorKind.EXTERNAL),
        Actor("expired-1", ActorKind.HUMAN),
    )
    grants = tuple(
        AuthorityGrant(
            actor_id=actor_id,
            actions=frozenset(Action),
            resource_id="*",
            expires_at=(
                NOW - timedelta(seconds=1)
                if actor_id == "expired-1"
                else NOW + timedelta(days=1)
            ),
        )
        for actor_id in ("architect-1", "code-1", "agent-1", "external-1", "expired-1")
    )
    authority = AuthorityService(actors=actors, grants=grants)
    workspace = FileEvidenceWorkspace(root)
    service = EvidenceWorkspaceCommandService(
        repository=repository,
        workspace=workspace,
        authority=authority,
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_000_000_000,
            seed="ST-01.02",
        ),
        clock=clock,
        observations=observations,
    )
    return service, repository, observations, workspace, run_receipt.run_id


def lock_command(
    run_id: str,
    *,
    command_id: str = "source-lock-command-1",
    actor_id: str = "architect-1",
    expected_version: int = 2,
    **changes: object,
) -> LockEvidenceWorkspaceCommand:
    values: dict[str, object] = {
        "command_id": command_id,
        "run_id": run_id,
        "actor_id": actor_id,
        "expected_version": expected_version,
        "correlation_id": "st-01-02-correlation-1",
        "causation_id": "authorized-ST-01.02",
    }
    values.update(changes)
    return LockEvidenceWorkspaceCommand(**values)


def candidate_hash(root: Path, relative: str, kind: str) -> str:
    path = root / Path(*relative.split("/"))
    if kind in {"file", "zip"}:
        return sha256(path.read_bytes()).hexdigest()
    items = tuple(
        (
            item.relative_to(path).as_posix(),
            sha256(item.read_bytes()).hexdigest(),
        )
        for item in sorted(path.rglob("*"))
        if item.is_file()
    )
    return deterministic_tree_hash(items)


def source_profile_for(
    root: Path,
    relative: str,
    kind: str,
    *,
    version: str = "1.0.0",
    expected_hash: str | None = None,
    limit_changes: dict[str, object] | None = None,
) -> SourceProfile:
    value = json.loads(
        (ROOT / "development-capsules/ST-01.02/SYNTHETIC_SOURCE_PROFILE.json").read_text(
            encoding="utf-8"
        )
    )
    value["version"] = version
    value["target_candidate"]["uri"] = f"repo://{relative}"
    value["target_candidate"]["source_kind"] = kind
    value["target_candidate"]["sha256"] = expected_hash or candidate_hash(
        root, relative, kind
    )
    if limit_changes:
        value["safety_limits"].update(limit_changes)
    content = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
    return SourceProfile.from_json_bytes(content)
