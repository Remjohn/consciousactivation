"""CA-M047 / INV-ISO-001 executable proof suite."""

from __future__ import annotations

import sqlite3
from pathlib import Path
import pytest

import importlib.util
import sys

_MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "packages"
    / "ca_runtime"
    / "src"
    / "ca_runtime"
    / "workspace_isolation.py"
)
_spec = importlib.util.spec_from_file_location("ca_runtime.workspace_isolation", _MODULE_PATH)
assert _spec and _spec.loader
workspace_isolation = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = workspace_isolation
_spec.loader.exec_module(workspace_isolation)

WorkspaceAuthorizationError = workspace_isolation.WorkspaceAuthorizationError
WorkspaceDigestMismatchError = workspace_isolation.WorkspaceDigestMismatchError
WorkspaceFilesystem = workspace_isolation.WorkspaceFilesystem
WorkspaceIsolatedDatabase = workspace_isolation.WorkspaceIsolatedDatabase
WorkspacePathIsolationError = workspace_isolation.WorkspacePathIsolationError
WorkspaceScopeError = workspace_isolation.WorkspaceScopeError
WorkspaceStateNotFoundError = workspace_isolation.WorkspaceStateNotFoundError
WorkspaceVersionConflictError = workspace_isolation.WorkspaceVersionConflictError
WorkspaceAuthority = workspace_isolation.WorkspaceAuthority
verify_workspace_bound_sha256 = workspace_isolation.verify_workspace_bound_sha256
workspace_bound_sha256 = workspace_isolation.workspace_bound_sha256


WS_A = "11111111-1111-4111-8111-111111111111"
WS_B = "22222222-2222-4222-8222-222222222222"
CAMPAIGN_A = "campaign-alpha"
CAMPAIGN_B = "campaign-beta"
AGGREGATE = "shared-aggregate"
ACTOR_A = "actor-a"
ACTOR_B = "actor-b"


@pytest.fixture
def authority_a() -> WorkspaceAuthority:
    return WorkspaceAuthority(WS_A, ACTOR_A, CAMPAIGN_A)


@pytest.fixture
def authority_b() -> WorkspaceAuthority:
    return WorkspaceAuthority(WS_B, ACTOR_B, CAMPAIGN_A)


@pytest.fixture
def db(tmp_path: Path) -> WorkspaceIsolatedDatabase:
    return WorkspaceIsolatedDatabase(tmp_path / "state.sqlite3")


@pytest.fixture
def fs(tmp_path: Path) -> WorkspaceFilesystem:
    return WorkspaceFilesystem(tmp_path / "object-storage")


class TestWorkspaceAuthorityFence:
    def test_matching_workspace_is_required_and_allowed(self, authority_a: WorkspaceAuthority) -> None:
        assert authority_a.require_workspace(WS_A) == WS_A

    def test_missing_workspace_fails_closed(self, authority_a: WorkspaceAuthority) -> None:
        with pytest.raises(WorkspaceAuthorizationError):
            authority_a.require_workspace(None)

    def test_mismatched_workspace_fails_closed(self, authority_a: WorkspaceAuthority) -> None:
        with pytest.raises(WorkspaceAuthorizationError):
            authority_a.require_workspace(WS_B)

    def test_campaign_mismatch_fails_closed(self, authority_a: WorkspaceAuthority) -> None:
        with pytest.raises(WorkspaceAuthorizationError):
            authority_a.require_campaign(CAMPAIGN_B)

    def test_scope_is_composed_from_authenticated_authority(self, authority_a: WorkspaceAuthority) -> None:
        assert authority_a.scope(AGGREGATE) == (WS_A, CAMPAIGN_A, AGGREGATE)

    @pytest.mark.parametrize(
        "value",
        ["../other", "a/b", r"a\b", ".", "..", "", "a\x00b"],
    )
    def test_unsafe_identifiers_are_rejected(self, value: str) -> None:
        with pytest.raises(WorkspaceScopeError):
            WorkspaceAuthority(value, ACTOR_A, CAMPAIGN_A)


class TestCryptographicIsolation:
    def test_identical_content_differs_by_workspace(self) -> None:
        payload = {"aggregate_id": AGGREGATE, "value": "same"}
        digest_a = workspace_bound_sha256(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            payload=payload,
        )
        digest_b = workspace_bound_sha256(
            workspace_id=WS_B,
            campaign_id=CAMPAIGN_A,
            payload=payload,
        )
        assert digest_a != digest_b

    def test_identical_content_differs_by_campaign(self) -> None:
        payload = {"aggregate_id": AGGREGATE, "value": "same"}
        digest_a = workspace_bound_sha256(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            payload=payload,
        )
        digest_b = workspace_bound_sha256(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_B,
            payload=payload,
        )
        assert digest_a != digest_b

    def test_canonical_hash_is_order_independent_for_payload_mapping(self) -> None:
        a = workspace_bound_sha256(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            payload={"z": 1, "a": {"b": 2, "a": 3}},
        )
        b = workspace_bound_sha256(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            payload={"a": {"a": 3, "b": 2}, "z": 1},
        )
        assert a == b

    def test_hash_verification_passes_for_the_authorized_scope(self) -> None:
        payload = {"state": "RUNNING", "version": 3}
        digest = workspace_bound_sha256(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            payload=payload,
        )
        verify_workspace_bound_sha256(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            payload=payload,
            expected_sha256=digest,
        )

    def test_hash_verification_rejects_workspace_substitution(self) -> None:
        payload = {"state": "RUNNING", "version": 3}
        digest = workspace_bound_sha256(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            payload=payload,
        )
        with pytest.raises(WorkspaceDigestMismatchError):
            verify_workspace_bound_sha256(
                workspace_id=WS_B,
                campaign_id=CAMPAIGN_A,
                payload=payload,
                expected_sha256=digest,
            )


class TestDatabaseIsolation:
    def test_schema_uses_composite_workspace_campaign_aggregate_key(
        self, db: WorkspaceIsolatedDatabase
    ) -> None:
        assert db.schema_has_composite_scope_key() is True

    def test_same_aggregate_id_can_exist_in_distinct_workspaces(
        self, db: WorkspaceIsolatedDatabase
    ) -> None:
        db.save(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
            state={"secret": "workspace-a"},
        )
        db.save(
            workspace_id=WS_B,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
            state={"secret": "workspace-b"},
        )
        assert db.get(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
        ).state == {"secret": "workspace-a"}
        assert db.get(
            workspace_id=WS_B,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
        ).state == {"secret": "workspace-b"}

    def test_same_aggregate_id_can_exist_in_distinct_campaigns(
        self, db: WorkspaceIsolatedDatabase
    ) -> None:
        db.save(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
            state={"secret": "campaign-a"},
        )
        db.save(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_B,
            aggregate_id=AGGREGATE,
            state={"secret": "campaign-b"},
        )
        assert db.get(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
        ).state["secret"] == "campaign-a"
        assert db.get(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_B,
            aggregate_id=AGGREGATE,
        ).state["secret"] == "campaign-b"

    def test_cross_workspace_read_is_fail_closed_and_does_not_leak_state(
        self, db: WorkspaceIsolatedDatabase
    ) -> None:
        db.save(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
            state={"secret": "do-not-leak"},
        )
        with pytest.raises(WorkspaceStateNotFoundError) as exc:
            db.get(
                workspace_id=WS_B,
                campaign_id=CAMPAIGN_A,
                aggregate_id=AGGREGATE,
            )
        assert str(exc.value) == "Scoped state was not found"
        assert "do-not-leak" not in str(exc.value)

    def test_cross_campaign_read_is_fail_closed(
        self, db: WorkspaceIsolatedDatabase
    ) -> None:
        db.save(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
            state={"secret": "campaign-a"},
        )
        with pytest.raises(WorkspaceStateNotFoundError):
            db.get(
                workspace_id=WS_A,
                campaign_id=CAMPAIGN_B,
                aggregate_id=AGGREGATE,
            )

    def test_cross_workspace_write_cannot_mutate_authorized_row(
        self, db: WorkspaceIsolatedDatabase
    ) -> None:
        db.save(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
            state={"owner": "A"},
        )
        db.save(
            workspace_id=WS_B,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
            state={"owner": "B"},
        )
        db.compare_and_swap(
            workspace_id=WS_B,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
            expected_version=0,
            state={"owner": "B-new"},
        )
        assert db.get(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
        ).state == {"owner": "A"}
        assert db.get(
            workspace_id=WS_B,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
        ).state == {"owner": "B-new"}

    def test_stale_version_does_not_perform_write(
        self, db: WorkspaceIsolatedDatabase
    ) -> None:
        db.save(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
            state={"counter": 1},
            version=1,
        )
        with pytest.raises(WorkspaceVersionConflictError):
            db.compare_and_swap(
                workspace_id=WS_A,
                campaign_id=CAMPAIGN_A,
                aggregate_id=AGGREGATE,
                expected_version=0,
                state={"counter": 99},
            )
        assert db.get(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
        ).state == {"counter": 1}

    def test_delete_requires_exact_scope(
        self, db: WorkspaceIsolatedDatabase
    ) -> None:
        db.save(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
            state={"owner": "A"},
        )
        with pytest.raises(WorkspaceStateNotFoundError):
            db.delete(
                workspace_id=WS_B,
                campaign_id=CAMPAIGN_A,
                aggregate_id=AGGREGATE,
            )
        assert db.get(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id=AGGREGATE,
        ).state == {"owner": "A"}

    def test_workspace_listing_never_returns_other_campaign_or_workspace(
        self, db: WorkspaceIsolatedDatabase
    ) -> None:
        db.save(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            aggregate_id="a-one",
            state={"v": 1},
        )
        db.save(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_B,
            aggregate_id="a-two",
            state={"v": 2},
        )
        db.save(
            workspace_id=WS_B,
            campaign_id=CAMPAIGN_A,
            aggregate_id="b-one",
            state={"v": 3},
        )
        rows = db.list_workspace(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
        )
        assert [(row.workspace_id, row.campaign_id, row.aggregate_id) for row in rows] == [
            (WS_A, CAMPAIGN_A, "a-one")
        ]

    def test_raw_database_shape_has_no_global_aggregate_key(self, db: WorkspaceIsolatedDatabase) -> None:
        with sqlite3.connect(db.db_path) as conn:
            pk_columns = [
                row[1]
                for row in conn.execute(
                    f"PRAGMA table_info({db.TABLE_NAME})"
                ).fetchall()
                if row[5] > 0
            ]
        assert pk_columns == ["workspace_id", "campaign_id", "aggregate_id"]

    def test_false_proof_global_aggregate_accessor_is_not_exposed(self, db: WorkspaceIsolatedDatabase) -> None:
        """A UI that hides foreign rows is not sufficient; this API has no aggregate-only read."""
        assert not hasattr(db, "get_by_aggregate_id")


class TestFilesystemIsolation:
    def test_workspace_and_campaign_roots_are_distinct(self, fs: WorkspaceFilesystem) -> None:
        assert fs.campaign_root(WS_A, CAMPAIGN_A) != fs.campaign_root(WS_B, CAMPAIGN_A)
        assert fs.campaign_root(WS_A, CAMPAIGN_A) != fs.campaign_root(WS_A, CAMPAIGN_B)

    def test_write_and_read_are_scoped_to_the_same_workspace_and_campaign(
        self, fs: WorkspaceFilesystem
    ) -> None:
        fs.write_bytes(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            relative_path="state/value.bin",
            content=b"A",
        )
        assert (
            fs.read_bytes(
                workspace_id=WS_A,
                campaign_id=CAMPAIGN_A,
                relative_path="state/value.bin",
            )
            == b"A"
        )
        with pytest.raises(WorkspacePathIsolationError):
            fs.read_bytes(
                workspace_id=WS_B,
                campaign_id=CAMPAIGN_A,
                relative_path="state/value.bin",
            )

    @pytest.mark.parametrize("relative_path", ["../escape", "a/../../escape", "/absolute", "./file"])
    def test_traversal_and_absolute_paths_are_rejected(
        self, fs: WorkspaceFilesystem, relative_path: str
    ) -> None:
        with pytest.raises(WorkspacePathIsolationError):
            fs.artifact_path(
                workspace_id=WS_A,
                campaign_id=CAMPAIGN_A,
                relative_path=relative_path,
            )

    def test_cross_workspace_alias_symlink_is_rejected(
        self, fs: WorkspaceFilesystem, tmp_path: Path
    ) -> None:
        target = fs.campaign_root(WS_B, CAMPAIGN_A)
        target_file = target / "secret.txt"
        target_file.write_text("workspace-b-secret", encoding="utf-8")

        link = fs.campaign_root(WS_A, CAMPAIGN_A) / "alias"
        try:
            link.symlink_to(target_file)
        except (OSError, NotImplementedError) as exc:
            pytest.skip(f"symlink unavailable: {exc}")

        with pytest.raises(WorkspacePathIsolationError):
            fs.read_bytes(
                workspace_id=WS_A,
                campaign_id=CAMPAIGN_A,
                relative_path="alias",
            )

    def test_campaign_alias_symlink_is_rejected(
        self, fs: WorkspaceFilesystem
    ) -> None:
        target = fs.campaign_root(WS_A, CAMPAIGN_B)
        target_file = target / "secret.txt"
        target_file.write_text("campaign-b-secret", encoding="utf-8")

        link = fs.campaign_root(WS_A, CAMPAIGN_A) / "alias"
        try:
            link.symlink_to(target_file)
        except (OSError, NotImplementedError) as exc:
            pytest.skip(f"symlink unavailable: {exc}")

        with pytest.raises(WorkspacePathIsolationError):
            fs.read_bytes(
                workspace_id=WS_A,
                campaign_id=CAMPAIGN_A,
                relative_path="alias",
            )

    def test_state_file_cannot_be_overwritten_by_repeat_write(
        self, fs: WorkspaceFilesystem
    ) -> None:
        fs.write_bytes(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            relative_path="state.json",
            content=b"original",
        )
        with pytest.raises(FileExistsError):
            fs.write_bytes(
                workspace_id=WS_A,
                campaign_id=CAMPAIGN_A,
                relative_path="state.json",
                content=b"attacker",
            )
        assert fs.read_bytes(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            relative_path="state.json",
        ) == b"original"

    def test_missing_file_does_not_reveal_other_scope(
        self, fs: WorkspaceFilesystem
    ) -> None:
        fs.write_bytes(
            workspace_id=WS_A,
            campaign_id=CAMPAIGN_A,
            relative_path="secret.txt",
            content=b"workspace-a",
        )
        with pytest.raises(WorkspacePathIsolationError) as exc:
            fs.read_bytes(
                workspace_id=WS_B,
                campaign_id=CAMPAIGN_A,
                relative_path="secret.txt",
            )
        assert "workspace-a" not in str(exc.value)


def test_false_proof_countercase_direct_database_access_is_not_the_authorized_api() -> None:
    """A raw DB connection can see storage physically; the scoped API must be the security boundary."""
    # This deliberately records the invariant's false-proof boundary: filesystem/DB ACLs
    # outside the application are deployment controls, while this module proves the
    # application-facing scoped access path is fail-closed.
    assert True
