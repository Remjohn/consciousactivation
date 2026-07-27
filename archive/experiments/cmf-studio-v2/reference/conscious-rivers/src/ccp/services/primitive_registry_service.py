"""
CCP FR-ERA3-06 - Primitive Registry Query Service.

Loads experience and meaning primitives from YAML, warms an in-process cache,
optionally mirrors entries into Redis, exposes deterministic conflict
resolution, and supports targeted primitive invalidation for hot reload.
"""

from __future__ import annotations

import json
import os
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

import yaml

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.primitive_registry_models import (
    CACHE_KEY_PREFIX_EXP,
    CACHE_KEY_PREFIX_MNG,
    EXPERIENCE_PLANE,
    FAMILY_SORT_ORDER,
    MEANING_PLANE,
    REGISTRY_AGENT_NAME,
    CacheHealthStatus,
    CacheWarmStats,
    ConflictEntry,
    ConflictPrecedenceReason,
    ConflictResolutionResult,
    ExperiencePrimitiveRecord,
    MeaningPrimitiveRecord,
    PrimitiveFamilyQueryResponse,
    PrimitiveInvalidationResponse,
    PrimitiveLookupResult,
    PrimitivePlane,
    PrimitivePlaneQueryResponse,
    PrimitiveQueryRequest,
    PrimitiveQueryResponse,
    PrimitiveRecord,
)


try:
    import redis  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    redis = None


INVALIDATION_CHANNEL = "primitive_registry_invalidation"
REPO_ROOT = Path(__file__).resolve().parents[3]
PRIMITIVES_ROOT = REPO_ROOT / "src" / "ccp" / "harness" / "primitives"

EXPERIENCE_FAMILY_CODE_MAP = {
    "trigger_timing": "TRG",
    "friction_ability": "FRC",
    "trust_resonance_signaling": "TRS",
    "feedback_scoring": "FBK",
    "progression_replay": "PRG",
    "social_referral": "SOC",
    "social_economy": "SOC",
    "safe_failure_recovery": "SAF",
    "personalization_identity": "PER",
}


@dataclass(slots=True)
class LoadedPrimitive:
    record: PrimitiveRecord
    plane: PrimitivePlane
    source_path: Path


class YAMLRegistryLoader:
    """Load primitive YAMLs from disk and coerce them into typed records."""

    def __init__(self, primitives_root: Path | None = None) -> None:
        self.primitives_root = primitives_root or PRIMITIVES_ROOT
        self.yaml_reads = 0
        self.stale_keys = 0
        self.source_index: dict[str, Path] = {}
        self.plane_index: dict[str, PrimitivePlane] = {}

    def load_all(self) -> tuple[dict[str, LoadedPrimitive], CacheWarmStats]:
        records: dict[str, LoadedPrimitive] = {}
        self.yaml_reads = 0
        self.stale_keys = 0
        self.source_index = {}
        self.plane_index = {}

        experience_count = 0
        meaning_count = 0
        for path in sorted((self.primitives_root / EXPERIENCE_PLANE).rglob("*.yaml")):
            loaded = self._load_yaml_path(path)
            if loaded is None:
                continue
            primitive_id = _primitive_id(loaded.record)
            records[primitive_id] = loaded
            self.source_index[primitive_id] = path
            self.plane_index[primitive_id] = loaded.plane
            experience_count += 1

        for path in sorted((self.primitives_root / MEANING_PLANE).rglob("*.yaml")):
            loaded = self._load_yaml_path(path)
            if loaded is None:
                continue
            primitive_id = _primitive_id(loaded.record)
            records[primitive_id] = loaded
            self.source_index[primitive_id] = path
            self.plane_index[primitive_id] = loaded.plane
            meaning_count += 1

        stats = CacheWarmStats(
            experience_count=experience_count,
            meaning_count=meaning_count,
            stale_keys=self.stale_keys,
            yaml_reads=self.yaml_reads,
        )
        return records, stats

    def load_single(self, primitive_id: str) -> LoadedPrimitive | None:
        path = self.source_index.get(primitive_id)
        if path is None or not path.exists():
            return None
        loaded = self._load_yaml_path(path)
        if loaded is None:
            return None
        self.source_index[primitive_id] = path
        self.plane_index[primitive_id] = loaded.plane
        return loaded

    def _load_yaml_path(self, path: Path) -> LoadedPrimitive | None:
        try:
            self.yaml_reads += 1
            payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if "experience_primitive_id" in payload:
                record = ExperiencePrimitiveRecord.model_validate(payload)
                return LoadedPrimitive(record=record, plane=PrimitivePlane.EXPERIENCE, source_path=path)
            if "primitive_id" in payload:
                record = MeaningPrimitiveRecord.model_validate(payload)
                return LoadedPrimitive(record=record, plane=PrimitivePlane.MEANING, source_path=path)
        except Exception:
            self.stale_keys += 1
        return None


class RegistryCacheManager:
    """Redis-backed cache with in-process mirror and targeted invalidation."""

    def __init__(
        self,
        loader: YAMLRegistryLoader,
        receipt_chain: ReceiptChain,
        redis_url: str | None = None,
    ) -> None:
        self.loader = loader
        self.receipt_chain = receipt_chain
        self.redis_url = redis_url or os.getenv("REDIS_URL", "")
        self.redis_connected = False
        self._redis: Any = None
        self._pubsub: Any = None
        self._listener_thread: threading.Thread | None = None

        self.local_mirror: dict[str, PrimitiveRecord] = {}
        self.id_to_key: dict[str, str] = {}
        self.id_to_plane: dict[str, PrimitivePlane] = {}
        self.family_index: dict[str, set[str]] = {}
        self.plane_index: dict[PrimitivePlane, set[str]] = {
            PrimitivePlane.EXPERIENCE: set(),
            PrimitivePlane.MEANING: set(),
        }
        self.tag_index: dict[str, set[str]] = {}
        self.last_warm_stats = CacheWarmStats()

        self._connect_redis()

    def warm_cache(self) -> CacheWarmStats:
        loaded_records, stats = self.loader.load_all()
        self.local_mirror = {}
        self.id_to_key = {}
        self.id_to_plane = {}
        self.family_index = {}
        self.plane_index = {
            PrimitivePlane.EXPERIENCE: set(),
            PrimitivePlane.MEANING: set(),
        }
        self.tag_index = {}

        if self.redis_connected and self._redis is not None:
            try:
                pipeline = self._redis.pipeline()
                for primitive_id, loaded in loaded_records.items():
                    key = _cache_key(loaded.plane, primitive_id)
                    pipeline.set(key, _serialize_record(loaded.record))
                pipeline.execute()
            except Exception:
                self.redis_connected = False
                self._redis = None
                self._pubsub = None
                self.receipt_chain.log(
                    agent_id=REGISTRY_AGENT_NAME,
                    action="registry_cache_degraded",
                    input_summary="redis_pipeline_warm_failed",
                    output_summary="falling_back_to_local_mirror_only",
                    metadata={"stage_name": "REGISTRY-WARM", "warning": True},
                )

        for primitive_id, loaded in loaded_records.items():
            self._store_local(primitive_id, loaded.record, loaded.plane)

        self.last_warm_stats = stats
        self.receipt_chain.log(
            agent_id=REGISTRY_AGENT_NAME,
            action="registry_warm",
            input_summary=f"root={self.loader.primitives_root}",
            output_summary=f"experience={stats.experience_count} meaning={stats.meaning_count}",
            metadata={
                "stage_name": "REGISTRY-WARM",
                "redis_connected": self.redis_connected,
                "yaml_reads": stats.yaml_reads,
                "stale_keys": stats.stale_keys,
            },
        )
        self._ensure_pubsub_listener()
        return stats

    def get(self, primitive_id: str) -> PrimitiveLookupResult:
        key = self.id_to_key.get(primitive_id)
        if key and primitive_id in self.local_mirror:
            return PrimitiveLookupResult(
                primitive_id=primitive_id,
                record=self.local_mirror[primitive_id],
                plane=self.id_to_plane.get(primitive_id),
                cache_hit=True,
            )

        if key and self.redis_connected and self._redis is not None:
            try:
                payload = self._redis.get(key)
                if payload:
                    record = _deserialize_record(payload)
                    self.local_mirror[primitive_id] = record
                    return PrimitiveLookupResult(
                        primitive_id=primitive_id,
                        record=record,
                        plane=self.id_to_plane.get(primitive_id),
                        cache_hit=True,
                    )
            except Exception:
                self.redis_connected = False

        loaded = self.loader.load_single(primitive_id)
        if loaded is None:
            return PrimitiveLookupResult(primitive_id=primitive_id, record=None, cache_hit=False)

        self._store_record(primitive_id, loaded.record, loaded.plane)
        return PrimitiveLookupResult(
            primitive_id=primitive_id,
            record=loaded.record,
            plane=loaded.plane,
            cache_hit=False,
            reloaded_from_disk=True,
        )

    def invalidate_primitive(self, primitive_id: str) -> PrimitiveInvalidationResponse:
        plane = self.id_to_plane.get(primitive_id) or self.loader.plane_index.get(primitive_id)
        if plane is None:
            return PrimitiveInvalidationResponse(
                primitive_id=primitive_id,
                deleted_keys=0,
                broadcast_sent=False,
                redis_connected=self.redis_connected,
            )

        deleted_keys = 1
        key = _cache_key(plane, primitive_id)

        self.local_mirror.pop(primitive_id, None)
        if self.redis_connected and self._redis is not None:
            try:
                self._redis.delete(key)
            except Exception:
                self.receipt_chain.log(
                    agent_id=REGISTRY_AGENT_NAME,
                    action="registry_invalidate_failed",
                    input_summary=primitive_id,
                    output_summary="serving_existing_cache",
                    metadata={"stage_name": "INVALIDATE", "warning": True},
                )
                return PrimitiveInvalidationResponse(
                    primitive_id=primitive_id,
                    deleted_keys=0,
                    broadcast_sent=False,
                    redis_connected=self.redis_connected,
                )

        broadcast_sent = self._publish_invalidation(primitive_id, plane)
        self.receipt_chain.log(
            agent_id=REGISTRY_AGENT_NAME,
            action="registry_invalidate",
            input_summary=primitive_id,
            output_summary=f"deleted_keys={deleted_keys}",
            metadata={
                "stage_name": "INVALIDATE",
                "broadcast_sent": broadcast_sent,
                "redis_connected": self.redis_connected,
            },
        )
        return PrimitiveInvalidationResponse(
            primitive_id=primitive_id,
            deleted_keys=deleted_keys,
            broadcast_sent=broadcast_sent,
            redis_connected=self.redis_connected,
        )

    def health(self) -> CacheHealthStatus:
        warmed_at = self.last_warm_stats.warmed_at.isoformat()
        return CacheHealthStatus(
            experience_count=self.last_warm_stats.experience_count,
            meaning_count=self.last_warm_stats.meaning_count,
            total_cached=self.last_warm_stats.total_cached,
            redis_connected=self.redis_connected,
            last_warm_at=warmed_at,
            stale_keys=self.last_warm_stats.stale_keys,
            yaml_reads=self.loader.yaml_reads,
            local_mirror_size=len(self.local_mirror),
        )

    def records_for_family(self, family_code: str) -> PrimitiveFamilyQueryResponse:
        family_key = family_code.strip().lower()
        primitive_ids = sorted(self.family_index.get(family_key, set()))
        experience_records: list[ExperiencePrimitiveRecord] = []
        meaning_records: list[MeaningPrimitiveRecord] = []
        for primitive_id in primitive_ids:
            record = self.local_mirror.get(primitive_id)
            if isinstance(record, ExperiencePrimitiveRecord):
                experience_records.append(record)
            elif isinstance(record, MeaningPrimitiveRecord):
                meaning_records.append(record)
        return PrimitiveFamilyQueryResponse(
            family_code=family_code,
            experience_records=experience_records,
            meaning_records=meaning_records,
        )

    def records_for_plane(self, plane: PrimitivePlane) -> PrimitivePlaneQueryResponse:
        primitives = [
            self.local_mirror[primitive_id]
            for primitive_id in sorted(self.plane_index[plane])
            if primitive_id in self.local_mirror
        ]
        return PrimitivePlaneQueryResponse(plane=plane, primitives=primitives)

    def records_for_tag(self, tag: str) -> list[PrimitiveRecord]:
        tag_key = tag.strip().lower()
        primitive_ids = sorted(self.tag_index.get(tag_key, set()))
        return [self.local_mirror[primitive_id] for primitive_id in primitive_ids if primitive_id in self.local_mirror]

    def _connect_redis(self) -> None:
        if not self.redis_url or redis is None:
            return
        try:
            self._redis = redis.from_url(self.redis_url, decode_responses=True)
            self._redis.ping()
            self.redis_connected = True
        except Exception:
            self.redis_connected = False
            self._redis = None

    def _ensure_pubsub_listener(self) -> None:
        if not self.redis_connected or self._redis is None or self._listener_thread is not None:
            return
        try:
            self._pubsub = self._redis.pubsub(ignore_subscribe_messages=True)
            self._pubsub.subscribe(INVALIDATION_CHANNEL)
        except Exception:
            self._pubsub = None
            self.redis_connected = False
            return

        def _listener() -> None:
            while self._pubsub is not None:
                try:
                    message = self._pubsub.get_message(timeout=1.0)
                    if not message or message.get("type") != "message":
                        time.sleep(0.05)
                        continue
                    payload = json.loads(message["data"])
                    primitive_id = str(payload.get("primitive_id", "")).strip()
                    if primitive_id:
                        self.local_mirror.pop(primitive_id, None)
                except Exception:
                    time.sleep(0.1)

        self._listener_thread = threading.Thread(target=_listener, name="primitive-registry-pubsub", daemon=True)
        self._listener_thread.start()

    def _publish_invalidation(self, primitive_id: str, plane: PrimitivePlane) -> bool:
        if not self.redis_connected or self._redis is None:
            return False
        try:
            self._redis.publish(
                INVALIDATION_CHANNEL,
                json.dumps({"primitive_id": primitive_id, "plane": plane.value}),
            )
            return True
        except Exception:
            self.redis_connected = False
            return False

    def _store_record(self, primitive_id: str, record: PrimitiveRecord, plane: PrimitivePlane) -> None:
        self._store_local(primitive_id, record, plane)
        if self.redis_connected and self._redis is not None:
            try:
                self._redis.set(_cache_key(plane, primitive_id), _serialize_record(record))
            except Exception:
                self.redis_connected = False

    def _store_local(self, primitive_id: str, record: PrimitiveRecord, plane: PrimitivePlane) -> None:
        key = _cache_key(plane, primitive_id)
        self.local_mirror[primitive_id] = record
        self.id_to_key[primitive_id] = key
        self.id_to_plane[primitive_id] = plane
        self.plane_index[plane].add(primitive_id)

        family = _family_name(record).lower()
        self.family_index.setdefault(family, set()).add(primitive_id)

        for tag in _record_tags(record):
            self.tag_index.setdefault(tag, set()).add(primitive_id)


class ConflictResolver:
    """Resolve mutually incompatible primitive sets with deterministic ordering."""

    def __init__(self, record_provider: Callable[[], dict[str, PrimitiveRecord]]) -> None:
        self._record_provider = record_provider

    def resolve(
        self,
        requested_ids: list[str],
        context: str,
        primary_intent_ids: list[str] | None = None,
    ) -> ConflictResolutionResult:
        records = self._record_provider()
        ordered_ids: list[str] = []
        seen: set[str] = set()
        resolution_log: list[str] = []
        for primitive_id in requested_ids:
            if primitive_id not in seen:
                ordered_ids.append(primitive_id)
                seen.add(primitive_id)

        active = set(ordered_ids)
        removed_ids: list[str] = []
        conflicts: list[ConflictEntry] = []
        primary_intent_set = set(primary_intent_ids or [])

        for left_index, primitive_a in enumerate(ordered_ids):
            if primitive_a not in active:
                continue
            record_a = records.get(primitive_a)
            if record_a is None:
                continue
            for primitive_b in ordered_ids[left_index + 1 :]:
                if primitive_b not in active:
                    continue
                record_b = records.get(primitive_b)
                if record_b is None:
                    continue
                if not self._conflict_exists(record_a, record_b, records, resolution_log):
                    continue
                winner, loser, reason = self._compare_records(
                    primitive_a,
                    record_a,
                    primitive_b,
                    record_b,
                    context,
                    primary_intent_set,
                )
                active.discard(loser)
                if loser not in removed_ids:
                    removed_ids.append(loser)
                conflicts.append(
                    ConflictEntry(
                        primitive_a=primitive_a,
                        primitive_b=primitive_b,
                        winner=winner,
                        loser=loser,
                        reason=reason,
                    )
                )
                resolution_log.append(f"{winner} kept over {loser} via {reason.value}")

        clean_ids = [primitive_id for primitive_id in ordered_ids if primitive_id in active]
        return ConflictResolutionResult(
            clean_ids=clean_ids,
            removed_ids=removed_ids,
            conflicts=conflicts,
            resolution_log=resolution_log,
            resolution_applied=bool(conflicts),
        )

    def _conflict_exists(
        self,
        record_a: PrimitiveRecord,
        record_b: PrimitiveRecord,
        records: dict[str, PrimitiveRecord],
        resolution_log: list[str],
    ) -> bool:
        primitive_a = _primitive_id(record_a)
        primitive_b = _primitive_id(record_b)

        conflicts_a = _conflict_targets(record_a)
        conflicts_b = _conflict_targets(record_b)

        for conflict_id in conflicts_a | conflicts_b:
            if conflict_id not in records:
                resolution_log.append(f"warning: unknown conflict target {conflict_id} referenced")

        return primitive_b in conflicts_a or primitive_a in conflicts_b

    def _compare_records(
        self,
        primitive_a: str,
        record_a: PrimitiveRecord,
        primitive_b: str,
        record_b: PrimitiveRecord,
        context: str,
        primary_intent_ids: set[str],
    ) -> tuple[str, str, ConflictPrecedenceReason]:
        score_a = _context_score(record_a, context)
        score_b = _context_score(record_b, context)
        if score_a != score_b:
            if score_a > score_b:
                return primitive_a, primitive_b, ConflictPrecedenceReason.SCORING_FIT
            return primitive_b, primitive_a, ConflictPrecedenceReason.SCORING_FIT

        primary_a = primitive_a in primary_intent_ids
        primary_b = primitive_b in primary_intent_ids
        if primary_a != primary_b:
            if primary_a:
                return primitive_a, primitive_b, ConflictPrecedenceReason.PRIMARY_INTENT
            return primitive_b, primitive_a, ConflictPrecedenceReason.PRIMARY_INTENT

        family_a = _family_sort_rank(record_a)
        family_b = _family_sort_rank(record_b)
        if family_a != family_b:
            if family_a < family_b:
                return primitive_a, primitive_b, ConflictPrecedenceReason.FAMILY_ORDER
            return primitive_b, primitive_a, ConflictPrecedenceReason.FAMILY_ORDER

        if primitive_a <= primitive_b:
            return primitive_a, primitive_b, ConflictPrecedenceReason.FAMILY_ORDER
        return primitive_b, primitive_a, ConflictPrecedenceReason.FAMILY_ORDER


class PrimitiveRegistryQueryService:
    """High-level query service exposing cache, lookup, and conflict APIs."""

    def __init__(
        self,
        primitives_root: Path | None = None,
        receipt_chain: ReceiptChain | None = None,
        redis_url: str | None = None,
    ) -> None:
        coach_acronym = os.getenv("COACH_ACRONYM", "UNK")
        self.receipt_chain = receipt_chain or ReceiptChain(coach_acronym=coach_acronym)
        self.loader = YAMLRegistryLoader(primitives_root)
        self.cache = RegistryCacheManager(self.loader, self.receipt_chain, redis_url=redis_url)
        self.conflict_resolver = ConflictResolver(lambda: dict(self.cache.local_mirror))

    def warm_registry(self) -> CacheWarmStats:
        return self.cache.warm_cache()

    def query_by_id(self, primitive_id: str, plane: PrimitivePlane | None = None) -> PrimitiveRecord | None:
        lookup = self.cache.get(primitive_id)
        if lookup.record is None:
            self.receipt_chain.log(
                agent_id=REGISTRY_AGENT_NAME,
                action="registry_lookup_miss",
                input_summary=primitive_id,
                output_summary="not_found",
                metadata={"stage_name": "LOOKUP"},
            )
            return None

        if plane is not None and lookup.plane != plane:
            self.receipt_chain.log(
                agent_id=REGISTRY_AGENT_NAME,
                action="registry_lookup_plane_mismatch",
                input_summary=f"{primitive_id}:{plane.value}",
                output_summary=f"actual={lookup.plane.value if lookup.plane else 'unknown'}",
                metadata={"stage_name": "LOOKUP"},
            )
            return None

        self.receipt_chain.log(
            agent_id=REGISTRY_AGENT_NAME,
            action="registry_lookup_hit",
            input_summary=primitive_id,
            output_summary=f"plane={lookup.plane.value if lookup.plane else 'unknown'}",
            metadata={
                "stage_name": "LOOKUP",
                "cache_hit": lookup.cache_hit,
                "reloaded_from_disk": lookup.reloaded_from_disk,
            },
        )
        return lookup.record

    def query_by_family(self, family_code: str) -> PrimitiveFamilyQueryResponse:
        return self.cache.records_for_family(family_code)

    def query_by_plane(self, plane: PrimitivePlane) -> PrimitivePlaneQueryResponse:
        return self.cache.records_for_plane(plane)

    def query_by_tag(self, tag: str) -> list[PrimitiveRecord]:
        return self.cache.records_for_tag(tag)

    def query_batch(self, request: PrimitiveQueryRequest) -> PrimitiveQueryResponse:
        start = time.perf_counter()
        records: list[PrimitiveRecord] = []
        cache_hit = True
        for primitive_id in request.requested_ids:
            lookup = self.cache.get(primitive_id)
            if lookup.record is None:
                cache_hit = False
                continue
            if lookup.reloaded_from_disk:
                cache_hit = False
            records.append(lookup.record)

        resolution = self.conflict_resolver.resolve(
            request.requested_ids,
            request.context,
            request.primary_intent_ids,
        )
        resolved_primitives = [
            record for record in records if _primitive_id(record) in set(resolution.clean_ids)
        ]
        latency_ms = (time.perf_counter() - start) * 1000
        if resolution.resolution_applied:
            self.receipt_chain.log(
                agent_id=REGISTRY_AGENT_NAME,
                action="registry_conflict_resolution",
                input_summary=",".join(request.requested_ids),
                output_summary=",".join(resolution.clean_ids),
                metadata={
                    "stage_name": "CONFLICT-RESOLUTION",
                    "removed_ids": resolution.removed_ids,
                    "resolution_log": resolution.resolution_log if request.include_conflicts_log else [],
                },
            )
        return PrimitiveQueryResponse(
            query_id=str(uuid4()),
            requested_ids=request.requested_ids,
            resolved_primitives=resolved_primitives,
            conflict_resolution=resolution,
            cache_hit=cache_hit,
            latency_ms=round(latency_ms, 3),
        )

    def invalidate_primitive(self, primitive_id: str) -> PrimitiveInvalidationResponse:
        return self.cache.invalidate_primitive(primitive_id)

    def health(self) -> CacheHealthStatus:
        return self.cache.health()


_primitive_registry_service: PrimitiveRegistryQueryService | None = None


def get_primitive_registry_service() -> PrimitiveRegistryQueryService | None:
    return _primitive_registry_service


def set_primitive_registry_service(service: PrimitiveRegistryQueryService) -> None:
    global _primitive_registry_service
    _primitive_registry_service = service


def build_default_primitive_registry_service() -> PrimitiveRegistryQueryService:
    service = PrimitiveRegistryQueryService()
    set_primitive_registry_service(service)
    return service


def _primitive_id(record: PrimitiveRecord) -> str:
    if isinstance(record, ExperiencePrimitiveRecord):
        return record.experience_primitive_id
    return record.primitive_id


def _family_name(record: PrimitiveRecord) -> str:
    if isinstance(record, ExperiencePrimitiveRecord):
        return record.experience_family
    return record.family


def _record_tags(record: PrimitiveRecord) -> set[str]:
    tags = {
        _primitive_id(record).lower(),
        _family_name(record).lower(),
        record.canonical_name.lower(),
    }
    for alias in getattr(record, "aliases", []):
        tags.add(alias.lower())
    crosswalk_id = getattr(record, "crosswalk_id", "")
    if crosswalk_id:
        tags.add(crosswalk_id.lower())
    return tags


def _conflict_targets(record: PrimitiveRecord) -> set[str]:
    targets = set(getattr(record, "conflicts_with", []))
    if isinstance(record, MeaningPrimitiveRecord):
        targets.update(record.coalition_partners_antagonistic)
    return {target for target in targets if target}


def _context_score(record: PrimitiveRecord, context: str) -> float:
    normalized = context.strip().lower()
    score_sources: list[dict[str, float]] = []
    if isinstance(record, ExperiencePrimitiveRecord):
        score_sources = [record.experience_stage_fit, record.surface_fit]
    elif isinstance(record, MeaningPrimitiveRecord):
        score_sources = [record.phase_fit, record.surface_fit, record.goal_bias]

    for source in score_sources:
        if normalized in source:
            return float(source[normalized])
    return 0.0


def _family_sort_rank(record: PrimitiveRecord) -> int:
    if isinstance(record, ExperiencePrimitiveRecord):
        code = EXPERIENCE_FAMILY_CODE_MAP.get(record.experience_family, "")
        if code:
            return FAMILY_SORT_ORDER.get(code, 999)
    primitive_id = _primitive_id(record)
    code = primitive_id.split("-")[1] if "-" in primitive_id else ""
    return FAMILY_SORT_ORDER.get(code, 999)


def _cache_key(plane: PrimitivePlane, primitive_id: str) -> str:
    prefix = CACHE_KEY_PREFIX_EXP if plane == PrimitivePlane.EXPERIENCE else CACHE_KEY_PREFIX_MNG
    return f"{prefix}:{primitive_id}"


def _serialize_record(record: PrimitiveRecord) -> str:
    payload = {
        "plane": PrimitivePlane.EXPERIENCE.value if isinstance(record, ExperiencePrimitiveRecord) else PrimitivePlane.MEANING.value,
        "data": record.model_dump(mode="json"),
    }
    return json.dumps(payload)


def _deserialize_record(payload: str | bytes) -> PrimitiveRecord:
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    parsed = json.loads(payload)
    plane = parsed.get("plane")
    data = parsed.get("data", {})
    if plane == PrimitivePlane.EXPERIENCE.value:
        return ExperiencePrimitiveRecord.model_validate(data)
    return MeaningPrimitiveRecord.model_validate(data)
