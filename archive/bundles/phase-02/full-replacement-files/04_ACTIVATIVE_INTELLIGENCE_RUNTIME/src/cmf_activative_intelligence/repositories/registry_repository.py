from __future__ import annotations

import csv
import json
import re
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, Iterable, Iterator

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339

from .air_repository import AirRepository, AirRepositoryError

PRIMITIVE_REGISTRY_ID = "air-primitive-registry"
PRIMITIVE_REGISTRY_VERSION = "v2.1-snapshot"
ARCHETYPE_REGISTRY_ID = "air-archetype-evidence-registry"
ARCHETYPE_REGISTRY_VERSION = "v2.1-snapshot"
EXPECTED_PRIMITIVE_COUNT = 243
EXPECTED_ARCHETYPE_COUNT = 96


@dataclass(frozen=True, slots=True)
class PrimitiveRecord:
    primitive_id: str
    canonical_name: str
    plane: str
    family: str
    core_move: str
    source_relative_path: str
    source_sha256: str
    active_feature_ids: tuple[str, ...]
    synergizes_with: tuple[str, ...]
    conflicts_with: tuple[str, ...]
    suppression_conditions: tuple[str, ...]
    misuse_modes: tuple[str, ...]
    registry_version: str

    def immutable_ref(self) -> dict[str, str]:
        return {
            "object_id": self.primitive_id,
            "version": self.registry_version,
            "sha256": self.source_sha256,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "primitive_id": self.primitive_id,
            "canonical_name": self.canonical_name,
            "plane": self.plane,
            "family": self.family,
            "core_move": self.core_move,
            "source_relative_path": self.source_relative_path,
            "source_sha256": self.source_sha256,
            "active_feature_ids": list(self.active_feature_ids),
            "synergizes_with": list(self.synergizes_with),
            "conflicts_with": list(self.conflicts_with),
            "suppression_conditions": list(self.suppression_conditions),
            "misuse_modes": list(self.misuse_modes),
            "registry_version": self.registry_version,
        }


@dataclass(frozen=True, slots=True)
class ArchetypeEvidenceRecord:
    archetype_prompt_id: str
    family: str
    title: str
    filename: str
    source_relative_path: str
    source_sha256: str
    evidence_status: str
    registry_version: str

    def immutable_ref(self) -> dict[str, str]:
        return {
            "object_id": self.archetype_prompt_id,
            "version": self.registry_version,
            "sha256": self.source_sha256,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "archetype_prompt_id": self.archetype_prompt_id,
            "family": self.family,
            "title": self.title,
            "filename": self.filename,
            "source_relative_path": self.source_relative_path,
            "source_sha256": self.source_sha256,
            "evidence_status": self.evidence_status,
            "registry_version": self.registry_version,
        }


def _sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _strip_yaml_scalar(value: str) -> str:
    value = value.split("#", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value.strip()


def _extract_yaml_list(text: str, key: str) -> tuple[str, ...]:
    lines = text.splitlines()
    values: list[str] = []
    active = False
    base_indent = 0
    for line in lines:
        if not active:
            match = re.match(rf"^(\s*){re.escape(key)}\s*:\s*(.*)$", line)
            if not match:
                continue
            active = True
            base_indent = len(match.group(1))
            inline = match.group(2).strip()
            if inline.startswith("[") and inline.endswith("]"):
                raw = inline[1:-1].strip()
                if raw:
                    values.extend(
                        _strip_yaml_scalar(item)
                        for item in raw.split(",")
                        if _strip_yaml_scalar(item)
                    )
                return tuple(values)
            if inline not in {"", "[]"}:
                scalar = _strip_yaml_scalar(inline)
                if scalar:
                    values.append(scalar)
                return tuple(values)
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if indent <= base_indent and not stripped.startswith("-"):
            break
        if stripped.startswith("-"):
            item = _strip_yaml_scalar(stripped[1:].strip())
            if item:
                values.append(item)
    return tuple(values)


def default_data_root() -> Path:
    return Path(resources.files("cmf_activative_intelligence").joinpath("data"))


class RegistryRepository:
    def __init__(self, repository: AirRepository):
        self.repository = repository

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        with self.repository._connect() as connection:
            yield connection

    def import_all(
        self,
        *,
        data_root: Path | None = None,
        now: str | None = None,
    ) -> dict[str, Any]:
        root = data_root or default_data_root()
        timestamp = now or utc_now_rfc3339()
        self.repository.initialize(now=timestamp)
        primitive_result = self.import_primitives(root=root, now=timestamp)
        archetype_result = self.import_archetypes(root=root, now=timestamp)
        return {
            "primitive_registry": primitive_result,
            "archetype_registry": archetype_result,
        }

    def import_primitives(self, *, root: Path, now: str) -> dict[str, Any]:
        inventory = root / "governance" / "PRIMITIVE_INVENTORY.csv"
        if not inventory.is_file():
            raise AirRepositoryError(f"Primitive inventory missing: {inventory}")
        rows = list(csv.DictReader(inventory.read_text(encoding="utf-8").splitlines()))
        if len(rows) != EXPECTED_PRIMITIVE_COUNT:
            raise AirRepositoryError(
                f"Primitive inventory count {len(rows)} != {EXPECTED_PRIMITIVE_COUNT}"
            )
        ids = [row["primitive_id"] for row in rows]
        unique_id_count = len(set(ids))
        duplicate_id_count = len(ids) - unique_id_count

        prepared: list[tuple[Any, ...]] = []
        manifest_items: list[dict[str, str]] = []
        for row in rows:
            relative = row["snapshot_path"].replace("\\", "/")
            source = root / relative
            if not source.is_file():
                raise AirRepositoryError(
                    f"Primitive source missing for {row['primitive_id']}: {relative}"
                )
            observed = _sha256(source)
            if observed != row["sha256"]:
                raise AirRepositoryError(
                    f"Primitive source hash mismatch for {row['primitive_id']}"
                )
            text = source.read_text(encoding="utf-8")
            active_features = tuple(
                item for item in row.get("active_feature_ids", "").split("|") if item
            )
            prepared.append(
                (
                    row["primitive_id"],
                    row["canonical_name"].strip(),
                    row["plane"],
                    row["family"],
                    row["core_move"].strip(),
                    relative,
                    observed,
                    canonical_json_text(list(active_features)),
                    canonical_json_text(list(_extract_yaml_list(text, "synergizes_with"))),
                    canonical_json_text(list(_extract_yaml_list(text, "conflicts_with"))),
                    canonical_json_text(list(_extract_yaml_list(text, "suppression_conditions"))),
                    canonical_json_text(list(_extract_yaml_list(text, "misuse_modes"))),
                    text,
                    PRIMITIVE_REGISTRY_VERSION,
                )
            )
            manifest_items.append(
                {
                    "primitive_id": row["primitive_id"],
                    "source_sha256": observed,
                }
            )

        manifest_sha = canonical_sha256(
            {
                "registry_id": PRIMITIVE_REGISTRY_ID,
                "version": PRIMITIVE_REGISTRY_VERSION,
                "inventory_sha256": _sha256(inventory),
                "items": manifest_items,
            }
        )
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                connection.execute("DELETE FROM air_primitives")
                connection.executemany(
                    """
                    INSERT INTO air_primitives(
                        primitive_id, canonical_name, plane, family, core_move,
                        source_relative_path, source_sha256,
                        active_feature_ids_json, synergizes_with_json,
                        conflicts_with_json, suppression_conditions_json,
                        misuse_modes_json, source_text, registry_version
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    prepared,
                )
                connection.execute(
                    """
                    INSERT INTO air_registry_snapshots(
                        registry_id, registry_version, registry_kind,
                        source_manifest_sha256, item_count, imported_at_utc
                    ) VALUES(?, ?, 'primitive', ?, ?, ?)
                    ON CONFLICT(registry_id, registry_version)
                    DO UPDATE SET
                        source_manifest_sha256 = excluded.source_manifest_sha256,
                        item_count = excluded.item_count,
                        imported_at_utc = excluded.imported_at_utc
                    """,
                    (
                        PRIMITIVE_REGISTRY_ID,
                        PRIMITIVE_REGISTRY_VERSION,
                        manifest_sha,
                        len(prepared),
                        now,
                    ),
                )
            except Exception:
                connection.execute("ROLLBACK")
                raise
            else:
                connection.execute("COMMIT")
        return {
            "registry_id": PRIMITIVE_REGISTRY_ID,
            "registry_version": PRIMITIVE_REGISTRY_VERSION,
            "item_count": len(prepared),
            "unique_primitive_id_count": unique_id_count,
            "duplicate_primitive_id_count": duplicate_id_count,
            "source_manifest_sha256": manifest_sha,
        }

    def import_archetypes(self, *, root: Path, now: str) -> dict[str, Any]:
        inventory = root / "governance" / "ARCHETYPE_PROMPT_INVENTORY.csv"
        if not inventory.is_file():
            raise AirRepositoryError(f"Archetype inventory missing: {inventory}")
        rows = list(csv.DictReader(inventory.read_text(encoding="utf-8").splitlines()))
        if len(rows) != EXPECTED_ARCHETYPE_COUNT:
            raise AirRepositoryError(
                f"Archetype inventory count {len(rows)} != {EXPECTED_ARCHETYPE_COUNT}"
            )
        ids = [row["archetype_prompt_id"] for row in rows]
        if len(ids) != len(set(ids)):
            raise AirRepositoryError("Archetype inventory has duplicate IDs")

        prepared: list[tuple[Any, ...]] = []
        manifest_items: list[dict[str, str]] = []
        for row in rows:
            relative = row["snapshot_path"].replace("\\", "/")
            source = root / relative
            if not source.is_file():
                raise AirRepositoryError(
                    f"Archetype source missing for {row['archetype_prompt_id']}: {relative}"
                )
            observed = _sha256(source)
            if observed != row["sha256"]:
                raise AirRepositoryError(
                    f"Archetype source hash mismatch for {row['archetype_prompt_id']}"
                )
            prepared.append(
                (
                    row["archetype_prompt_id"],
                    row["family"],
                    row["title"].strip(),
                    row["filename"],
                    relative,
                    observed,
                    row["status"],
                    source.read_text(encoding="utf-8"),
                    ARCHETYPE_REGISTRY_VERSION,
                )
            )
            manifest_items.append(
                {
                    "archetype_prompt_id": row["archetype_prompt_id"],
                    "source_sha256": observed,
                }
            )

        manifest_sha = canonical_sha256(
            {
                "registry_id": ARCHETYPE_REGISTRY_ID,
                "version": ARCHETYPE_REGISTRY_VERSION,
                "inventory_sha256": _sha256(inventory),
                "items": manifest_items,
            }
        )
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                connection.execute("DELETE FROM air_archetypes")
                connection.executemany(
                    """
                    INSERT INTO air_archetypes(
                        archetype_prompt_id, family, title, filename,
                        source_relative_path, source_sha256, evidence_status,
                        source_text, registry_version
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    prepared,
                )
                connection.execute(
                    """
                    INSERT INTO air_registry_snapshots(
                        registry_id, registry_version, registry_kind,
                        source_manifest_sha256, item_count, imported_at_utc
                    ) VALUES(?, ?, 'archetype_evidence', ?, ?, ?)
                    ON CONFLICT(registry_id, registry_version)
                    DO UPDATE SET
                        source_manifest_sha256 = excluded.source_manifest_sha256,
                        item_count = excluded.item_count,
                        imported_at_utc = excluded.imported_at_utc
                    """,
                    (
                        ARCHETYPE_REGISTRY_ID,
                        ARCHETYPE_REGISTRY_VERSION,
                        manifest_sha,
                        len(prepared),
                        now,
                    ),
                )
            except Exception:
                connection.execute("ROLLBACK")
                raise
            else:
                connection.execute("COMMIT")
        return {
            "registry_id": ARCHETYPE_REGISTRY_ID,
            "registry_version": ARCHETYPE_REGISTRY_VERSION,
            "item_count": len(prepared),
            "source_manifest_sha256": manifest_sha,
        }

    def _primitive_from_row(self, row: sqlite3.Row) -> PrimitiveRecord:
        return PrimitiveRecord(
            primitive_id=str(row["primitive_id"]),
            canonical_name=str(row["canonical_name"]),
            plane=str(row["plane"]),
            family=str(row["family"]),
            core_move=str(row["core_move"]),
            source_relative_path=str(row["source_relative_path"]),
            source_sha256=str(row["source_sha256"]),
            active_feature_ids=tuple(json.loads(row["active_feature_ids_json"])),
            synergizes_with=tuple(json.loads(row["synergizes_with_json"])),
            conflicts_with=tuple(json.loads(row["conflicts_with_json"])),
            suppression_conditions=tuple(json.loads(row["suppression_conditions_json"])),
            misuse_modes=tuple(json.loads(row["misuse_modes_json"])),
            registry_version=str(row["registry_version"]),
        )

    def get_primitive(
        self, primitive_id: str, *, source_sha256: str | None = None
    ) -> PrimitiveRecord:
        self.repository.initialize()
        with self._connect() as connection:
            if source_sha256 is None:
                rows = connection.execute(
                    "SELECT * FROM air_primitives WHERE primitive_id = ? ORDER BY source_sha256",
                    (primitive_id,),
                ).fetchall()
            else:
                rows = connection.execute(
                    "SELECT * FROM air_primitives WHERE primitive_id = ? AND source_sha256 = ?",
                    (primitive_id, source_sha256),
                ).fetchall()
        if not rows:
            suffix = f" with source hash {source_sha256}" if source_sha256 else ""
            raise AirRepositoryError(f"unknown Primitive ID: {primitive_id}{suffix}")
        if len(rows) > 1:
            hashes = [str(row["source_sha256"]) for row in rows]
            raise AirRepositoryError(
                f"ambiguous Primitive ID {primitive_id}; supply source_sha256 from {hashes}"
            )
        return self._primitive_from_row(rows[0])

    def query_primitives(
        self,
        query: str,
        *,
        family: str | None = None,
        plane: str | None = None,
        active_feature_id: str | None = None,
        limit: int = 10,
    ) -> tuple[PrimitiveRecord, ...]:
        self.repository.initialize()
        terms = [term.casefold() for term in re.findall(r"[A-Za-z0-9_-]+", query)]
        with self._connect() as connection:
            clauses = []
            parameters: list[Any] = []
            if family:
                clauses.append("family = ?")
                parameters.append(family)
            if plane:
                clauses.append("plane = ?")
                parameters.append(plane)
            sql = "SELECT * FROM air_primitives"
            if clauses:
                sql += " WHERE " + " AND ".join(clauses)
            rows = connection.execute(sql, parameters).fetchall()

        scored: list[tuple[int, str, PrimitiveRecord]] = []
        for row in rows:
            record = self._primitive_from_row(row)
            if active_feature_id and active_feature_id not in record.active_feature_ids:
                continue
            haystack = " ".join(
                (
                    record.primitive_id,
                    record.canonical_name,
                    record.family,
                    record.core_move,
                    " ".join(record.misuse_modes),
                )
            ).casefold()
            score = 0
            if query.casefold() == record.primitive_id.casefold():
                score += 1000
            for term in terms:
                if term == record.primitive_id.casefold():
                    score += 200
                if term in record.canonical_name.casefold():
                    score += 40
                if term == record.family.casefold():
                    score += 25
                if term in haystack:
                    score += 5
            if not terms or score:
                scored.append((score, record.primitive_id, record))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return tuple(item[2] for item in scored[: max(1, min(limit, 100))])

    def _archetype_from_row(self, row: sqlite3.Row) -> ArchetypeEvidenceRecord:
        return ArchetypeEvidenceRecord(
            archetype_prompt_id=str(row["archetype_prompt_id"]),
            family=str(row["family"]),
            title=str(row["title"]),
            filename=str(row["filename"]),
            source_relative_path=str(row["source_relative_path"]),
            source_sha256=str(row["source_sha256"]),
            evidence_status=str(row["evidence_status"]),
            registry_version=str(row["registry_version"]),
        )

    def get_archetype(self, archetype_prompt_id: str) -> ArchetypeEvidenceRecord:
        self.repository.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM air_archetypes WHERE archetype_prompt_id = ?",
                (archetype_prompt_id,),
            ).fetchone()
        if row is None:
            raise AirRepositoryError(
                f"unknown archetype evidence ID: {archetype_prompt_id}"
            )
        return self._archetype_from_row(row)

    def query_archetypes(
        self,
        query: str,
        *,
        family: str | None = None,
        limit: int = 10,
    ) -> tuple[ArchetypeEvidenceRecord, ...]:
        self.repository.initialize()
        terms = [term.casefold() for term in re.findall(r"[A-Za-z0-9_-]+", query)]
        with self._connect() as connection:
            if family:
                rows = connection.execute(
                    "SELECT * FROM air_archetypes WHERE family = ?",
                    (family,),
                ).fetchall()
            else:
                rows = connection.execute("SELECT * FROM air_archetypes").fetchall()
        scored: list[tuple[int, str, ArchetypeEvidenceRecord]] = []
        for row in rows:
            record = self._archetype_from_row(row)
            haystack = " ".join(
                (
                    record.archetype_prompt_id,
                    record.title,
                    record.filename,
                    record.family,
                )
            ).casefold()
            score = 1000 if query.casefold() == record.archetype_prompt_id.casefold() else 0
            score += sum(20 if term in record.title.casefold() else 5 if term in haystack else 0 for term in terms)
            if not terms or score:
                scored.append((score, record.archetype_prompt_id, record))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return tuple(item[2] for item in scored[: max(1, min(limit, 100))])

    def status(self) -> dict[str, Any]:
        self.repository.initialize()
        with self._connect() as connection:
            snapshots = connection.execute(
                """
                SELECT *
                FROM air_registry_snapshots
                ORDER BY registry_kind, registry_version
                """
            ).fetchall()
        return {
            "snapshots": [dict(row) for row in snapshots],
            "primitive_count": self.repository.health()["primitive_count"],
            "archetype_count": self.repository.health()["archetype_count"],
            "historical_archetypes_are_current_authority": False,
        }
