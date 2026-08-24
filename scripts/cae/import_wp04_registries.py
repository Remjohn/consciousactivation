"""Inventory, validate, and import inherited CAE registry inputs into staging.

The importer never mutates an existing snapshot. It imports the supplied SDA
and SFL ZIP bytes plus the AIR Primitive source snapshot as three distinct
sources, retaining raw source text, paths, hashes, versions, references, and
integrity findings. A failed internal reference quarantines only the affected
record; no missing registry entry is synthesized.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import uuid
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit

import psycopg
import yaml
from psycopg.types.json import Jsonb


ROOT = Path(__file__).resolve().parents[2]
ENVIRONMENT_VARIABLE = "CAE_SUPABASE_DATABASE_URL"
PROJECT_REF = "evnxdssbxxrsesftdvgx"
IMPORTER_VERSION = "cae-wp04-registry-importer/1.0.0"
SDA_ARCHIVE = ROOT / "Conscious Activation Engine Brownfield" / "sda.zip"
SFL_ARCHIVE = ROOT / "Conscious Activation Engine Brownfield" / "sfl.zip"
AIR_DATA_ROOT = ROOT / "services" / "air" / "src" / "cmf_activative_intelligence" / "data"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def stable_id(prefix: str, *parts: str) -> str:
    return f"{prefix}:{canonical_hash(list(parts))[:32]}"


def load_local_environment() -> None:
    for line in (ROOT / ".env").read_text(encoding="utf-8-sig").splitlines():
        key, separator, value = line.partition("=")
        if separator and key and not key.lstrip().startswith("#"):
            os.environ.setdefault(key.strip(), value.strip())


def connection_url() -> str:
    url = os.environ.get(ENVIRONMENT_VARIABLE, "")
    parsed = urlsplit(url)
    if not (
        parsed.hostname
        and parsed.hostname.endswith(".pooler.supabase.com")
        and parsed.port == 5432
        and parsed.username == f"postgres.{PROJECT_REF}"
    ):
        raise RuntimeError("connection is not the approved CAE staging session pooler")
    return url


@dataclass(slots=True)
class Item:
    registry_kind: str
    snapshot_id: str
    registry_id: str
    registry_source_version: str
    source_id: str
    source_record_version: str | None
    source_path: str
    source_hash: str
    raw_text: str
    payload: dict[str, Any]
    record_kind: str
    status: str = "IMPORTED"
    validation_status: str = "VALID"
    crosswalk_status: str = "NOT_APPLICABLE"
    known_gaps: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def item_id(self) -> str:
        return stable_id("cae:registry-item", self.snapshot_id, self.source_id, self.source_path, self.source_hash)


@dataclass(frozen=True, slots=True)
class Reference:
    source_item_id: str
    relation_type: str
    target_kind: str | None
    target_id: str
    status: str
    rationale: str | None
    detail: dict[str, Any]


@dataclass(frozen=True, slots=True)
class Issue:
    snapshot_id: str
    item_id: str | None
    code: str
    severity: str
    status: str
    detail: dict[str, Any]
    source_hash: str | None


@dataclass(slots=True)
class Snapshot:
    snapshot_id: str
    registry_id: str
    registry_kind: str
    source_version: str
    source_locator: str
    source_archive_sha256: str
    source_manifest_sha256: str
    items: list[Item]


def scalar_id(payload: dict[str, Any]) -> str | None:
    for key in ("artifact_id", "case_id", "suite_id"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def expected_count_check(manifest: dict[str, Any], entries: Iterable[str], root: str) -> list[tuple[str, int, int]]:
    expected = manifest.get("expected_counts", {})
    if not isinstance(expected, dict):
        return []
    results: list[tuple[str, int, int]] = []
    paths = tuple(entries)
    directory_map = {
        "existential_invariants": "ontology/existential_invariants/",
        "representation_geometries": "ontology/representation_geometries/",
        "archetypal_geometries": "grammar/archetypal_geometries/",
        "species_composition": "grammar/species_composition/",
        "primitive_to_invariant": "crosswalks/primitive_to_invariant/",
        "archetype_to_geometry": "crosswalks/archetype_to_geometry/",
        "families": "families/",
        "functions": "functions/",
        "compression_rules": "compression_rules/",
        "primitive_to_function_family_crosswalks": "crosswalks/primitive_to_function_family/",
        "representation_geometry_crosswalks": "crosswalks/representation_geometry_to_function_profile/",
        "archetype_profile_crosswalks": "crosswalks/archetype_to_function_profile/",
        "surface_constraint_profiles": "crosswalks/surface_to_constraint_profile/",
    }
    for label, wanted in expected.items():
        directory = directory_map.get(str(label))
        if directory is None or not isinstance(wanted, int):
            continue
        observed = sum(1 for path in paths if path.startswith(f"{root}/{directory}") and path.endswith(".yaml"))
        results.append((str(label), wanted, observed))
    return results


def read_zip_snapshot(archive_path: Path, *, root: str, registry_id: str, registry_kind: str) -> tuple[Snapshot, list[Issue]]:
    archive_hash = sha256_file(archive_path)
    with zipfile.ZipFile(archive_path) as archive:
        names = sorted(name for name in archive.namelist() if name.endswith(".yaml"))
        manifest_name = f"{root}/registry_manifest.yaml"
        manifest_raw = archive.read(manifest_name)
        manifest = yaml.safe_load(manifest_raw) or {}
        if not isinstance(manifest, dict):
            raise ValueError(f"{archive_path.name} registry manifest is not a mapping")
        version = str(manifest.get("manifest_version") or manifest.get("version") or "UNSPECIFIED_IN_SOURCE")
        snapshot_id = stable_id("cae:registry-snapshot", registry_id, version, archive_hash)
        manifest_hash = canonical_hash({"archive_sha256": archive_hash, "manifest": manifest, "paths": names})
        items: list[Item] = []
        issues: list[Issue] = []
        count_results = expected_count_check(manifest, names, root)
        for label, expected, observed in count_results:
            if expected != observed:
                issues.append(Issue(snapshot_id, None, "MANIFEST_COUNT_MISMATCH", "BLOCKING", "QUARANTINED", {"label": label, "expected": expected, "observed": observed}, None))
        for name in names:
            if name in {manifest_name, f"{root}/failure_corpus/manifest.yaml"}:
                continue
            raw_bytes = archive.read(name)
            raw_text = raw_bytes.decode("utf-8")
            payload = yaml.safe_load(raw_text)
            if not isinstance(payload, dict):
                issues.append(Issue(snapshot_id, None, "MALFORMED_YAML_RECORD", "BLOCKING", "QUARANTINED", {"source_path": name}, sha256_bytes(raw_bytes)))
                continue
            source_id = scalar_id(payload)
            if source_id is None:
                issues.append(Issue(snapshot_id, None, "MISSING_SOURCE_ID", "BLOCKING", "QUARANTINED", {"source_path": name}, sha256_bytes(raw_bytes)))
                continue
            record_version = payload.get("version")
            if record_version is not None and not isinstance(record_version, (str, int, float)):
                record_version = None
            record_kind = str(payload.get("registry_kind") or payload.get("artifact_class") or "failure_asset")
            item = Item(registry_kind, snapshot_id, registry_id, version, source_id, None if record_version is None else str(record_version), name, sha256_bytes(raw_bytes), raw_text, payload, record_kind)
            if item.source_record_version is None:
                item.notes.append("Record has no explicit version; immutable source identity inherits the registry manifest version.")
            items.append(item)
    return Snapshot(snapshot_id, registry_id, registry_kind, version, archive_path.relative_to(ROOT).as_posix(), archive_hash, manifest_hash, items), issues


def read_primitive_snapshot() -> tuple[Snapshot, list[Issue]]:
    inventory = AIR_DATA_ROOT / "governance" / "PRIMITIVE_INVENTORY.csv"
    rows = list(csv.DictReader(inventory.read_text(encoding="utf-8").splitlines()))
    version = "v2.1-snapshot"
    item_inputs: list[tuple[dict[str, str], Path, bytes]] = []
    for row in rows:
        source = AIR_DATA_ROOT / row["snapshot_path"]
        item_inputs.append((row, source, source.read_bytes()))
    source_set_hash = canonical_hash({"inventory_sha256": sha256_file(inventory), "items": [{"id": row["primitive_id"], "sha256": sha256_bytes(raw)} for row, _, raw in item_inputs]})
    snapshot_id = stable_id("cae:registry-snapshot", "air-primitive-registry", version, source_set_hash)
    items: list[Item] = []
    issues: list[Issue] = []
    for row, source, raw in item_inputs:
        source_id = row["primitive_id"].strip()
        if sha256_bytes(raw) != row["sha256"]:
            issues.append(Issue(snapshot_id, None, "SOURCE_HASH_MISMATCH", "BLOCKING", "QUARANTINED", {"source_id": source_id, "source_path": row["snapshot_path"]}, sha256_bytes(raw)))
            continue
        raw_text = raw.decode("utf-8")
        parsed = yaml.safe_load(raw_text)
        payload = parsed if isinstance(parsed, dict) else {"raw_source": raw_text}
        payload = {"inventory": row, "document": payload}
        items.append(Item("PRIMITIVE", snapshot_id, "air-primitive-registry", version, source_id, version, row["snapshot_path"].replace("\\", "/"), sha256_bytes(raw), raw_text, payload, "primitive"))
    return Snapshot(snapshot_id, "air-primitive-registry", "PRIMITIVE", version, inventory.relative_to(ROOT).as_posix(), source_set_hash, canonical_hash({"inventory_sha256": sha256_file(inventory), "row_count": len(rows)}), items), issues


def target_kind_for_key(key: str, value: str) -> str | None:
    lower = key.lower()
    if "primitive" in lower and (lower.endswith("id") or lower.endswith("ids")):
        return "PRIMITIVE"
    if "family" in lower and (lower.endswith("id") or lower.endswith("ids")):
        return "SFL"
    if "function" in lower and (lower.endswith("id") or lower.endswith("ids")):
        return "SFL"
    if "geometry" in lower and (lower.endswith("id") or lower.endswith("ids")):
        return "SDA"
    if "invariant" in lower and (lower.endswith("id") or lower.endswith("ids")) and value.startswith("SDA-"):
        return "SDA"
    if "mutation_suite" in lower and (lower.endswith("id") or lower.endswith("ids")):
        return "SFL"
    if key == "target_id":
        return "SDA" if value.startswith("SDA-") else None
    return None


def references_from_payload(item: Item, payload: Any, *, path: str = "") -> Iterable[tuple[str, str, str | None, str | None, dict[str, Any]]]:
    if item.registry_kind == "PRIMITIVE":
        # Primitive YAML is retained as source evidence. Its embedded identity
        # fields are not a declared crosswalk, so they must not be classified
        # as references to themselves.
        return
    if isinstance(payload, dict):
        rationale = payload.get("rationale") if isinstance(payload.get("rationale"), str) else None
        for key, value in payload.items():
            if key in {"artifact_id", "case_id", "suite_id"}:
                continue
            next_path = f"{path}.{key}" if path else key
            if isinstance(value, str):
                kind = target_kind_for_key(key, value)
                if kind:
                    yield (key.upper(), value, kind, rationale, {"payload_path": next_path})
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    if isinstance(child, str):
                        kind = target_kind_for_key(key, child)
                        if kind:
                            yield (key.upper(), child, kind, rationale, {"payload_path": f"{next_path}[{index}]"})
                    else:
                        yield from references_from_payload(item, child, path=f"{next_path}[{index}]")
            else:
                yield from references_from_payload(item, value, path=next_path)


def validate(snapshots: list[Snapshot], initial_issues: list[Issue]) -> tuple[list[Reference], list[Issue]]:
    issues = list(initial_issues)
    lookup: dict[str, dict[str, list[Item]]] = {}
    for snapshot in snapshots:
        for item in snapshot.items:
            lookup.setdefault(snapshot.registry_kind, {}).setdefault(item.source_id, []).append(item)
    references: list[Reference] = []
    for snapshot in snapshots:
        for item in snapshot.items:
            same_id = lookup[snapshot.registry_kind][item.source_id]
            if len(same_id) > 1:
                item.status = item.validation_status = "QUARANTINED"
                item.known_gaps.append({"code": "DUPLICATE_SOURCE_ID"})
                issues.append(Issue(snapshot.snapshot_id, item.item_id, "DUPLICATE_SOURCE_ID", "BLOCKING", "QUARANTINED", {"source_id": item.source_id, "source_path": item.source_path}, item.source_hash))
            if item.source_record_version is None:
                issues.append(Issue(snapshot.snapshot_id, item.item_id, "MISSING_RECORD_VERSION", "REVIEW", "OPEN", {"source_id": item.source_id, "inherited_registry_version": item.registry_source_version}, item.source_hash))
            refs = list(references_from_payload(item, item.payload))
            if refs:
                item.crosswalk_status = "VALID"
            for relation_type, target_id, target_kind, rationale, detail in refs:
                assert target_kind is not None
                targets = lookup.get(target_kind, {}).get(target_id, [])
                if len(targets) == 1:
                    status = "RESOLVED"
                else:
                    status = "UNRESOLVED_INTERNAL"
                    item.status = item.validation_status = "QUARANTINED"
                    item.crosswalk_status = "UNRESOLVED"
                    issue_code = "REGISTRY_REFERENCE_MISSING" if not targets else "REGISTRY_REFERENCE_AMBIGUOUS"
                    gap = {"code": issue_code, "target_registry_kind": target_kind, "target_id": target_id, **detail}
                    item.known_gaps.append(gap)
                    issues.append(Issue(snapshot.snapshot_id, item.item_id, issue_code, "BLOCKING", "QUARANTINED", gap, item.source_hash))
                references.append(Reference(item.item_id, relation_type, target_kind, target_id, status, rationale, detail))
    return references, issues


def plans() -> tuple[list[Snapshot], list[Reference], list[Issue], str]:
    sda, sda_issues = read_zip_snapshot(SDA_ARCHIVE, root="sda", registry_id="sda-registry", registry_kind="SDA")
    sfl, sfl_issues = read_zip_snapshot(SFL_ARCHIVE, root="sfl", registry_id="sfl-registry", registry_kind="SFL")
    primitives, primitive_issues = read_primitive_snapshot()
    snapshots = [sda, sfl, primitives]
    references, issues = validate(snapshots, [*sda_issues, *sfl_issues, *primitive_issues])
    source_set_hash = canonical_hash({"snapshots": [{"registry_id": snapshot.registry_id, "source_archive_sha256": snapshot.source_archive_sha256, "source_manifest_sha256": snapshot.source_manifest_sha256} for snapshot in snapshots]})
    return snapshots, references, issues, source_set_hash


def print_summary(snapshots: list[Snapshot], references: list[Reference], issues: list[Issue], source_set_hash: str) -> None:
    print(f"source_set_sha256={source_set_hash}")
    for snapshot in snapshots:
        quarantined = sum(item.status == "QUARANTINED" for item in snapshot.items)
        print(f"{snapshot.registry_kind.lower()}_items={len(snapshot.items)}")
        print(f"{snapshot.registry_kind.lower()}_quarantined={quarantined}")
    print(f"references_total={len(references)}")
    print(f"references_unresolved_internal={sum(reference.status == 'UNRESOLVED_INTERNAL' for reference in references)}")
    codes: dict[str, int] = {}
    for issue in issues:
        codes[issue.code] = codes.get(issue.code, 0) + 1
    for code in sorted(codes):
        print(f"issue_{code.lower()}={codes[code]}")


def apply_import(snapshots: list[Snapshot], references: list[Reference], issues: list[Issue], source_set_hash: str) -> None:
    run_id = stable_id("cae:registry-import-run", IMPORTER_VERSION, source_set_hash)
    outcome = "QUARANTINED" if any(issue.severity == "BLOCKING" for issue in issues) else "IMPORTED"
    with psycopg.connect(connection_url(), connect_timeout=10) as connection:
        with connection.transaction():
            with connection.cursor() as cursor:
                cursor.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", (run_id,))
                cursor.execute("SELECT 1 FROM cae.registry_import_run WHERE registry_import_run_id = %s", (run_id,))
                if cursor.fetchone() is not None:
                    print("import_status=ALREADY_APPLIED")
                    return
                cursor.execute("SELECT count(*) FROM cae.registry_snapshot")
                if int(cursor.fetchone()[0]) != 0:
                    raise RuntimeError("registry snapshots already exist; immutable import refuses a mixed source set")
                cursor.execute(
                    "INSERT INTO cae.registry_import_run(registry_import_run_id, importer_version, source_set_sha256, source_summary, outcome) VALUES (%s, %s, %s, %s, %s)",
                    (run_id, IMPORTER_VERSION, source_set_hash, Jsonb({"registry_count": len(snapshots), "issue_count": len(issues)}), outcome),
                )
                for snapshot in snapshots:
                    status = "QUARANTINED" if any(issue.snapshot_id == snapshot.snapshot_id and issue.severity == "BLOCKING" for issue in issues) else "VALID"
                    cursor.execute(
                        """INSERT INTO cae.registry_snapshot(registry_snapshot_id, registry_id, registry_kind, source_version, source_locator, source_archive_sha256, source_manifest_sha256, item_count, validation_status, imported_by_run_id)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (snapshot.snapshot_id, snapshot.registry_id, snapshot.registry_kind, snapshot.source_version, snapshot.source_locator, snapshot.source_archive_sha256, snapshot.source_manifest_sha256, len(snapshot.items), status, run_id),
                    )
                for snapshot in snapshots:
                    for item in snapshot.items:
                        cursor.execute(
                            """INSERT INTO cae.registry_item(registry_item_id, registry_snapshot_id, source_registry, source_id, registry_source_version, source_record_version, source_path, source_hash, canonical_id, record_kind, source_raw_text, payload, migration_status, lineage_preserved, validation_status, crosswalk_status, known_gaps, migration_notes, imported_by_run_id)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, true, %s, %s, %s, %s, %s)""",
                            (item.item_id, item.snapshot_id, item.registry_id, item.source_id, item.registry_source_version, item.source_record_version, item.source_path, item.source_hash, item.source_id, item.record_kind, item.raw_text, Jsonb(item.payload), item.status, item.validation_status, item.crosswalk_status, Jsonb(item.known_gaps), " ".join(item.notes), run_id),
                        )
                for reference in references:
                    cursor.execute(
                        """INSERT INTO cae.registry_reference(registry_reference_id, source_registry_item_id, relation_type, target_registry_kind, target_id, target_snapshot_id, validation_status, rationale, detail, imported_by_run_id)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (stable_id("cae:registry-reference", reference.source_item_id, reference.relation_type, reference.target_id, canonical_hash(reference.detail)), reference.source_item_id, reference.relation_type, reference.target_kind, reference.target_id, next((snapshot.snapshot_id for snapshot in snapshots if snapshot.registry_kind == reference.target_kind), None), reference.status, reference.rationale, Jsonb(reference.detail), run_id),
                    )
                for issue in issues:
                    cursor.execute(
                        """INSERT INTO cae.registry_integrity_issue(registry_integrity_issue_id, registry_snapshot_id, registry_item_id, issue_code, severity, status, detail, source_hash, imported_by_run_id)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (stable_id("cae:registry-issue", issue.snapshot_id, issue.item_id or "", issue.code, canonical_hash(issue.detail)), issue.snapshot_id, issue.item_id, issue.code, issue.severity, issue.status, Jsonb(issue.detail), issue.source_hash, run_id),
                    )
    print(f"import_status={outcome}")
    print(f"registry_import_run_id={run_id}")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    arguments = parser.parse_args()
    try:
        snapshots, references, issues, source_set_hash = plans()
        print_summary(snapshots, references, issues, source_set_hash)
        if arguments.apply:
            load_local_environment()
            apply_import(snapshots, references, issues, source_set_hash)
        return 0
    except (OSError, RuntimeError, ValueError, zipfile.BadZipFile, yaml.YAMLError, psycopg.Error) as error:
        print("import_status=FAILED")
        print(f"failure_type={type(error).__name__}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
