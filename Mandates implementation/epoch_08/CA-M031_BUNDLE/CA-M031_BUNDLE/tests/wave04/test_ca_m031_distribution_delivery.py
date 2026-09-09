from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

import pytest

from ca_contracts import canonical_sha256


def _load_module():
    package_src = Path(__file__).parents[2] / "packages" / "ca_runtime" / "src"
    contracts_src = Path(__file__).parents[2] / "packages" / "ca_contracts" / "src"
    for path in (str(package_src), str(contracts_src)):
        if path not in sys.path:
            sys.path.insert(0, path)

    import types

    package = types.ModuleType("ca_runtime")
    package.__path__ = [str(package_src / "ca_runtime")]
    sys.modules.setdefault("ca_runtime", package)

    release_path = package_src / "ca_runtime" / "release_manifest.py"
    release_spec = importlib.util.spec_from_file_location("ca_runtime.release_manifest", release_path)
    assert release_spec and release_spec.loader
    release_module = importlib.util.module_from_spec(release_spec)
    sys.modules[release_spec.name] = release_module
    release_spec.loader.exec_module(release_module)

    module_path = package_src / "ca_runtime" / "distribution_delivery.py"
    spec = importlib.util.spec_from_file_location("ca_runtime.distribution_delivery", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_release_manifest_module():
    return sys.modules["ca_runtime.release_manifest"]


_dist = _load_module()
_release = _load_release_manifest_module()

ExternalDistributionClient = _dist.ExternalDistributionClient
DistributionDestination = _dist.DistributionDestination
DeliveryLedger = _dist.DeliveryLedger
RetryPolicy = _dist.RetryPolicy
TransformationClass = _dist.TransformationClass
AdaptedArtifact = _dist.AdaptedArtifact
PublishResponse = _dist.PublishResponse
RetryableDeliveryError = _dist.RetryableDeliveryError
DistributionIntegrityError = _dist.DistributionIntegrityError
DistributionIdempotencyConflictError = _dist.DistributionIdempotencyConflictError
UnsupportedSemanticTransformationError = _dist.UnsupportedSemanticTransformationError
DeliveryStatus = _dist.DeliveryStatus
ReleaseManifestBuilder = _release.ReleaseManifestBuilder

RELEASE_SECRET = b"ca-m031-release-secret"
RECEIPT_SECRET = b"ca-m031-receipt-secret"


class CanonicalTestAdapter:
    adapter_id = "test.external"
    adapter_version = "1.2.0"

    def __init__(self, *, failures_before_success: int = 0, transformation: str = "CONTAINER") -> None:
        self.failures_before_success = failures_before_success
        self.transformation = transformation
        self.publish_calls = 0
        self.seen_keys: list[str] = []
        self.last_payload: tuple[AdaptedArtifact, ...] | None = None

    def adapt(self, package, *, destination):
        assert all(isinstance(artifact.source_bytes, bytes) for artifact in package.artifacts)
        return tuple(
            AdaptedArtifact(
                artifact_id=artifact.artifact_id,
                delivered_bytes=b"container-header:" + artifact.source_bytes
                if self.transformation == TransformationClass.CONTAINER.value
                else artifact.source_bytes,
                transformation_class=self.transformation,
                semantic_source_bytes=artifact.source_bytes,
                semantic_delivered_bytes=artifact.source_bytes,
            )
            for artifact in package.artifacts
        )

    def publish(self, payload, *, package, destination, idempotency_key):
        self.publish_calls += 1
        self.seen_keys.append(idempotency_key)
        self.last_payload = tuple(payload)
        if self.publish_calls <= self.failures_before_success:
            raise RetryableDeliveryError("temporary destination outage")
        return PublishResponse(
            response_id=f"remote-{self.publish_calls}",
            accepted=True,
            remote_receipt={"cdn_object": f"obj-{package.release_id}"},
        )


class SemanticRewriteAdapter(CanonicalTestAdapter):
    adapter_version = "9.9.9"

    def adapt(self, package, *, destination):
        return tuple(
            AdaptedArtifact(
                artifact_id=artifact.artifact_id,
                delivered_bytes=b"TITLE REWRITTEN",
                transformation_class="SEMANTIC_TITLE_REWRITE",
                semantic_source_bytes=artifact.source_bytes,
                semantic_delivered_bytes=b"TITLE REWRITTEN",
            )
            for artifact in package.artifacts
        )


class WrongProjectionAdapter(CanonicalTestAdapter):
    def adapt(self, package, *, destination):
        return tuple(
            AdaptedArtifact(
                artifact_id=artifact.artifact_id,
                delivered_bytes=b"container-header:" + artifact.source_bytes,
                transformation_class=TransformationClass.CONTAINER.value,
                semantic_source_bytes=b"not-the-source",
                semantic_delivered_bytes=artifact.source_bytes,
            )
            for artifact in package.artifacts
        )


def _ref(object_id: str, revision: str, payload: object) -> dict[str, str]:
    return {"object_id": object_id, "revision": revision, "sha256": canonical_sha256(payload)}


def _fixture(tmp_path: Path, *, release_id: str = "release:campaign-7:v2", release_version: str = "2.0.0",):
    artifact = tmp_path / "release-title.txt"
    artifact.write_bytes(b"sealed semantic title\n")
    builder = ReleaseManifestBuilder(RELEASE_SECRET)
    manifest = builder.build(
        release_id=release_id,
        release_version=release_version,
        release_metadata={"campaign_id": "campaign-7", "release_sequence": 2},
        artifact_paths=[
            {
                "path": artifact,
                "logical_uri": "campaign/title.txt",
                "kind": "text",
                "license_metadata": {"license": "Proprietary", "attribution": "CAE"},
                "provenance_refs": [_ref("source:interview-1", "rev-2", {"quote": "sealed"})],
            }
        ],
        source_refs=[_ref("source:interview-1", "rev-2", {"quote": "sealed"})],
        semantic_refs=[_ref("semantic:title-2", "rev-2", {"title": "sealed semantic title"})],
        composition_ref=_ref("composition:campaign-7", "rev-2", {"composition": 2}),
        authorization_refs=[
            {
                **_ref("authorization:campaign-7", "auth-2", {"decision": "GRANT"}),
                "decision": "GRANT",
                "resource_id": "release:campaign-7:v2",
                "resource_revision": "rev-2",
            }
        ],
        policy_ref=_ref("policy:release", "policy-2", {"policy": 2}),
        provenance_tree={
            "node_id": "campaign-7",
            "node_type": "campaign",
            "revision": "rev-2",
            "sha256": canonical_sha256({"campaign": 7, "release": 2}),
            "children": [],
        },
        license_metadata={"license": "Proprietary", "attribution": "CAE"},
    )
    destination = DistributionDestination(
        destination_id="cdn:primary",
        destination_type="CDN",
        endpoint="https://cdn.example.test/release",
        allowed_transformations=frozenset({TransformationClass.IDENTITY.value, TransformationClass.CONTAINER.value}),
        configuration={"region": "eu"},
    )
    return manifest, artifact, destination


def _semantic_fingerprint(kind: str, payload: bytes) -> bytes:
    assert kind == "text"
    return payload.removeprefix(b"container-header:")


def test_successful_execution_only_delivery_verifies_release_semantics_and_receipt(tmp_path: Path):
    manifest, artifact, destination = _fixture(tmp_path)
    adapter = CanonicalTestAdapter()
    client = ExternalDistributionClient(
        release_signing_secret=RELEASE_SECRET,
        receipt_signing_secret=RECEIPT_SECRET,
        retry_policy=RetryPolicy(max_attempts=3, initial_delay_seconds=0),
        sleeper=lambda _: None,
    )

    result = client.deliver(
        manifest,
        destination=destination,
        adapter=adapter,
        semantic_fingerprint=_semantic_fingerprint,
    )

    assert result.deduplicated is False
    receipt = result.receipt
    assert receipt.delivery_status is DeliveryStatus.DELIVERED
    assert receipt.release_id == manifest.release_id
    assert receipt.release_manifest_sha256 == manifest.manifest_sha256
    assert receipt.adapter_id == adapter.adapter_id
    assert receipt.adapter_version == adapter.adapter_version
    assert receipt.attempts[-1].status == "DELIVERED"
    assert receipt.artifacts[0].transformation_class == "CONTAINER"
    assert receipt.artifacts[0].semantic_source_sha256 == receipt.artifacts[0].semantic_delivered_sha256
    receipt.verify(RECEIPT_SECRET)
    assert adapter.publish_calls == 1
    assert artifact.read_bytes() == b"sealed semantic title\n"


def test_idempotent_success_does_not_republish_and_preserves_receipt(tmp_path: Path):
    manifest, _, destination = _fixture(tmp_path)
    adapter = CanonicalTestAdapter()
    client = ExternalDistributionClient(
        release_signing_secret=RELEASE_SECRET,
        receipt_signing_secret=RECEIPT_SECRET,
        retry_policy=RetryPolicy(max_attempts=2, initial_delay_seconds=0),
        sleeper=lambda _: None,
    )

    first = client.deliver(manifest, destination=destination, adapter=adapter, semantic_fingerprint=_semantic_fingerprint)
    second = client.deliver(manifest, destination=destination, adapter=adapter, semantic_fingerprint=_semantic_fingerprint)

    assert first.receipt.receipt_id == second.receipt.receipt_id
    assert second.deduplicated is True
    assert adapter.publish_calls == 1
    assert len(client.ledger.history(first.receipt.idempotency_key)) == 1


def test_exponential_backoff_retries_same_idempotency_key_and_records_attempts(tmp_path: Path):
    manifest, _, destination = _fixture(tmp_path)
    adapter = CanonicalTestAdapter(failures_before_success=2)
    observed_delays: list[float] = []
    client = ExternalDistributionClient(
        release_signing_secret=RELEASE_SECRET,
        receipt_signing_secret=RECEIPT_SECRET,
        retry_policy=RetryPolicy(max_attempts=4, initial_delay_seconds=2, multiplier=2, max_delay_seconds=10),
        sleeper=observed_delays.append,
    )

    result = client.deliver(manifest, destination=destination, adapter=adapter, semantic_fingerprint=_semantic_fingerprint)
    receipt = result.receipt

    assert receipt.delivery_status is DeliveryStatus.DELIVERED
    assert [item.status for item in receipt.attempts] == ["RETRYING", "RETRYING", "DELIVERED"]
    assert observed_delays == [2, 4]
    assert adapter.publish_calls == 3
    assert len(set(adapter.seen_keys)) == 1
    assert receipt.attempts[0].backoff_millis == 2000
    assert receipt.attempts[1].backoff_millis == 4000


def test_terminal_failure_is_signed_and_reuses_same_key_for_safe_redelivery(tmp_path: Path):
    manifest, _, destination = _fixture(tmp_path)
    first_adapter = CanonicalTestAdapter(failures_before_success=10)
    client = ExternalDistributionClient(
        release_signing_secret=RELEASE_SECRET,
        receipt_signing_secret=RECEIPT_SECRET,
        retry_policy=RetryPolicy(max_attempts=2, initial_delay_seconds=0),
        sleeper=lambda _: None,
    )

    first = client.deliver(
        manifest,
        destination=destination,
        adapter=first_adapter,
        semantic_fingerprint=_semantic_fingerprint,
    )
    assert first.receipt.delivery_status is DeliveryStatus.FAILED
    first.receipt.verify(RECEIPT_SECRET)
    assert len(client.ledger.history(first.receipt.idempotency_key)) == 1

    recovery_adapter = CanonicalTestAdapter()
    second = client.deliver(
        manifest,
        destination=destination,
        adapter=recovery_adapter,
        semantic_fingerprint=_semantic_fingerprint,
    )
    assert second.receipt.delivery_status is DeliveryStatus.DELIVERED
    assert second.receipt.idempotency_key == first.receipt.idempotency_key
    assert second.receipt.supersedes_receipt_id == first.receipt.receipt_id
    assert len(client.ledger.history(first.receipt.idempotency_key)) == 2


def test_manifest_mutation_is_rejected_before_adapter_execution(tmp_path: Path):
    manifest, artifact, destination = _fixture(tmp_path)
    adapter = CanonicalTestAdapter()
    artifact.write_bytes(b"MUTATED AFTER SEAL\n")
    client = ExternalDistributionClient(
        release_signing_secret=RELEASE_SECRET,
        receipt_signing_secret=RECEIPT_SECRET,
        retry_policy=RetryPolicy(max_attempts=1),
        sleeper=lambda _: None,
    )

    with pytest.raises(DistributionIntegrityError):
        client.deliver(manifest, destination=destination, adapter=adapter, semantic_fingerprint=_semantic_fingerprint)

    assert adapter.publish_calls == 0


def test_unsupported_semantic_transformation_fails_closed_before_publish(tmp_path: Path):
    manifest, _, destination = _fixture(tmp_path)
    adapter = SemanticRewriteAdapter()
    client = ExternalDistributionClient(
        release_signing_secret=RELEASE_SECRET,
        receipt_signing_secret=RECEIPT_SECRET,
        retry_policy=RetryPolicy(max_attempts=1),
        sleeper=lambda _: None,
    )

    with pytest.raises(UnsupportedSemanticTransformationError):
        client.deliver(manifest, destination=destination, adapter=adapter, semantic_fingerprint=_semantic_fingerprint)

    assert adapter.publish_calls == 0


def test_semantic_projection_mismatch_is_rejected_even_for_named_technical_transform(tmp_path: Path):
    manifest, _, destination = _fixture(tmp_path)
    adapter = WrongProjectionAdapter()
    client = ExternalDistributionClient(
        release_signing_secret=RELEASE_SECRET,
        receipt_signing_secret=RECEIPT_SECRET,
        retry_policy=RetryPolicy(max_attempts=1),
        sleeper=lambda _: None,
    )

    with pytest.raises(DistributionIntegrityError):
        client.deliver(manifest, destination=destination, adapter=adapter, semantic_fingerprint=_semantic_fingerprint)

    assert adapter.publish_calls == 0


def test_idempotency_key_conflict_rejects_changed_destination_configuration(tmp_path: Path):
    manifest, _, destination = _fixture(tmp_path)
    adapter = CanonicalTestAdapter()
    client = ExternalDistributionClient(
        release_signing_secret=RELEASE_SECRET,
        receipt_signing_secret=RECEIPT_SECRET,
        retry_policy=RetryPolicy(max_attempts=1),
        sleeper=lambda _: None,
    )
    first = client.deliver(manifest, destination=destination, adapter=adapter, semantic_fingerprint=_semantic_fingerprint)
    assert first.receipt.delivery_status is DeliveryStatus.DELIVERED

    conflicting_key = first.receipt.idempotency_key
    with pytest.raises(DistributionIdempotencyConflictError):
        client.ledger.assert_compatible(conflicting_key, hashlib.sha256(b"different-request").hexdigest())


def test_two_releases_under_one_campaign_get_distinct_delivery_identity(tmp_path: Path):
    destination = DistributionDestination(
        destination_id="cdn:primary",
        destination_type="CDN",
        endpoint="https://cdn.example.test/release",
        allowed_transformations=frozenset({TransformationClass.IDENTITY.value}),
        configuration={"region": "eu"},
    )

    def build_release(root: Path, release_id: str, version: str):
        root.mkdir()
        artifact = root / "release-title.txt"
        artifact.write_bytes(version.encode("utf-8"))
        builder = ReleaseManifestBuilder(RELEASE_SECRET)
        return builder.build(
            release_id=release_id,
            release_version=version,
            release_metadata={"campaign_id": "campaign-shared", "release_sequence": int(version)},
            artifact_paths=[{
                "path": artifact,
                "logical_uri": "campaign/title.txt",
                "kind": "text",
                "license_metadata": {"license": "Proprietary", "attribution": "CAE"},
                "provenance_refs": [_ref("source:interview-1", "rev-2", {"quote": version})],
            }],
            source_refs=[_ref("source:interview-1", "rev-2", {"quote": version})],
            semantic_refs=[_ref("semantic:title", version, {"title": version})],
            composition_ref=_ref("composition:campaign-shared", version, {"composition": version}),
            authorization_refs=[{
                **_ref("authorization:campaign-shared", version, {"decision": "GRANT"}),
                "decision": "GRANT",
                "resource_id": release_id,
                "resource_revision": version,
            }],
            policy_ref=_ref("policy:release", "policy-2", {"policy": 2}),
            provenance_tree={
                "node_id": "campaign-shared",
                "node_type": "campaign",
                "revision": version,
                "sha256": canonical_sha256({"campaign": "shared", "version": version}),
                "children": [],
            },
            license_metadata={"license": "Proprietary", "attribution": "CAE"},
        )

    first_manifest = build_release(tmp_path / "one", "release:campaign-shared:v1", "1")
    second_manifest = build_release(tmp_path / "two", "release:campaign-shared:v2", "2")
    client = ExternalDistributionClient(
        release_signing_secret=RELEASE_SECRET,
        receipt_signing_secret=RECEIPT_SECRET,
        retry_policy=RetryPolicy(max_attempts=1),
        sleeper=lambda _: None,
    )
    first_result = client.deliver(
        first_manifest, destination=destination, adapter=CanonicalTestAdapter(transformation="IDENTITY"), semantic_fingerprint=_semantic_fingerprint
    )
    second_result = client.deliver(
        second_manifest, destination=destination, adapter=CanonicalTestAdapter(transformation="IDENTITY"), semantic_fingerprint=_semantic_fingerprint
    )

    assert first_result.receipt.release_id != second_result.receipt.release_id
    assert first_result.receipt.release_manifest_sha256 != second_result.receipt.release_manifest_sha256
    assert first_result.receipt.idempotency_key != second_result.receipt.idempotency_key
    assert first_manifest.release_metadata["campaign_id"] == second_manifest.release_metadata["campaign_id"] == "campaign-shared"


def test_signed_receipt_detects_tampering(tmp_path: Path):
    manifest, _, destination = _fixture(tmp_path)
    client = ExternalDistributionClient(
        release_signing_secret=RELEASE_SECRET,
        receipt_signing_secret=RECEIPT_SECRET,
        retry_policy=RetryPolicy(max_attempts=1),
        sleeper=lambda _: None,
    )
    result = client.deliver(
        manifest, destination=destination, adapter=CanonicalTestAdapter(), semantic_fingerprint=_semantic_fingerprint
    )
    receipt = result.receipt
    object.__setattr__(receipt, "release_id", "release:tampered")
    with pytest.raises(DistributionIntegrityError, match="digest mismatch"):
        receipt.verify(RECEIPT_SECRET)


def test_retry_policy_caps_exponential_delay():
    policy = RetryPolicy(max_attempts=5, initial_delay_seconds=3, multiplier=2, max_delay_seconds=5)
    assert policy.delay_before_retry(1) == 3
    assert policy.delay_before_retry(2) == 5
    assert policy.delay_before_retry(4) == 5
