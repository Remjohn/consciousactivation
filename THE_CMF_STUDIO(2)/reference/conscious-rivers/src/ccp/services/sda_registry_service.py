"""
CCP FR-ERA3-20 - SDA Ontology and Registry service.

Deterministic, manifest-driven loader for the Semantic Discernment
Architecture ontology, structural grammar, and maintained crosswalk
bundles. The service intentionally stops at repo-backed canonical
objects and does not expose HTTP query APIs.
"""

from __future__ import annotations

import hashlib
import os
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.sda_registry_models import (
    ARG_PREFIX,
    INV_PREFIX,
    PROHIBITED_CANONICAL_CLASSES,
    RETAINED_PRD02_CONTENT_ARCHETYPES,
    RPG_PREFIX,
    SCG_PREFIX,
    XW_AG_PREFIX,
    XW_PI_PREFIX,
    ArchetypeToGeometryCrosswalkEntry,
    ArchetypalGeometryRecord,
    ExistentialInvariantRecord,
    PrimitiveToInvariantCrosswalkEntry,
    RepresentationGeometryRecord,
    SDAArtifactClass,
    SDAArtifactReloadResult,
    SDARegistryAuditReport,
    SDARegistryIssue,
    SDARegistryKind,
    SDARegistryManifest,
    SDARegistryRecord,
    SDAManifestHealth,
    SDA_ROOT_DIRNAME,
    SpeciesCompositionRule,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SDA_ROOT = REPO_ROOT / SDA_ROOT_DIRNAME
PRIMITIVES_ROOT = REPO_ROOT / "src" / "ccp" / "harness" / "primitives"

STAGE_MANIFEST_LOAD = "SDA20_MANIFEST_LOAD"
STAGE_STARTUP_WARM = "SDA20_STARTUP_WARM"
STAGE_ARTIFACT_REJECTION = "SDA20_ARTIFACT_REJECTION"
STAGE_RELOAD_SUCCESS = "SDA20_RELOAD_SUCCESS"
STAGE_RELOAD_FAILURE = "SDA20_RELOAD_FAILURE"
STAGE_CROSSWALK_ERROR = "SDA20_CROSSWALK_ERROR"

KIND_TO_BUCKET: dict[SDARegistryKind, str] = {
    SDARegistryKind.EXISTENTIAL_INVARIANT: "existential_invariants",
    SDARegistryKind.REPRESENTATION_GEOMETRY: "representation_geometries",
    SDARegistryKind.ARCHETYPAL_GEOMETRY: "archetypal_geometries",
    SDARegistryKind.SPECIES_COMPOSITION_GRAMMAR: "species_composition",
    SDARegistryKind.PRIMITIVE_TO_INVARIANT_CROSSWALK: "primitive_to_invariant",
    SDARegistryKind.ARCHETYPE_TO_GEOMETRY_CROSSWALK: "archetype_to_geometry",
}

PREFIX_TO_KIND: dict[str, SDARegistryKind] = {
    INV_PREFIX: SDARegistryKind.EXISTENTIAL_INVARIANT,
    RPG_PREFIX: SDARegistryKind.REPRESENTATION_GEOMETRY,
    ARG_PREFIX: SDARegistryKind.ARCHETYPAL_GEOMETRY,
    SCG_PREFIX: SDARegistryKind.SPECIES_COMPOSITION_GRAMMAR,
    XW_PI_PREFIX: SDARegistryKind.PRIMITIVE_TO_INVARIANT_CROSSWALK,
    XW_AG_PREFIX: SDARegistryKind.ARCHETYPE_TO_GEOMETRY_CROSSWALK,
}

FORBIDDEN_DIRECTORY_NAMES: set[str] = {
    "content_species",
    "species",
    "hard_negatives",
    "recursive_patterns",
    "contextual_invariants",
    "feedback_loops",
}

RECORD_MODEL_BY_KIND: dict[SDARegistryKind, type[SDARegistryRecord]] = {
    SDARegistryKind.EXISTENTIAL_INVARIANT: ExistentialInvariantRecord,
    SDARegistryKind.REPRESENTATION_GEOMETRY: RepresentationGeometryRecord,
    SDARegistryKind.ARCHETYPAL_GEOMETRY: ArchetypalGeometryRecord,
    SDARegistryKind.SPECIES_COMPOSITION_GRAMMAR: SpeciesCompositionRule,
    SDARegistryKind.PRIMITIVE_TO_INVARIANT_CROSSWALK: PrimitiveToInvariantCrosswalkEntry,
    SDARegistryKind.ARCHETYPE_TO_GEOMETRY_CROSSWALK: ArchetypeToGeometryCrosswalkEntry,
}

EXPECTED_COUNT_KEYS: dict[str, str] = {
    "existential_invariants": "existential_invariant_count",
    "representation_geometries": "representation_geometry_count",
    "archetypal_geometries": "archetypal_geometry_count",
    "species_composition": "species_composition_rule_count",
    "primitive_to_invariant": "primitive_to_invariant_crosswalk_count",
    "archetype_to_geometry": "archetype_to_geometry_crosswalk_count",
}


class SDAOntologyValidator:
    """Deterministic path, class, scalar, and false-registry validator."""

    def __init__(self, sda_root: Path) -> None:
        self.sda_root = sda_root

    def validate_artifact_path(
        self,
        path: Path,
        allowed_paths: dict[str, Path],
    ) -> SDARegistryIssue | None:
        normalized = path.as_posix().lower()
        for forbidden_name in FORBIDDEN_DIRECTORY_NAMES:
            marker = f"/{forbidden_name}/"
            if marker in normalized or normalized.endswith(f"/{forbidden_name}.yaml"):
                return SDARegistryIssue(
                    artifact_path=str(path),
                    error_code="FALSE_REGISTRY_VIOLATION",
                    message=f"Forbidden canonical registry directory detected: {forbidden_name}",
                )

        if not any(_is_within(path, root) for root in allowed_paths.values()):
            return SDARegistryIssue(
                artifact_path=str(path),
                error_code="FALSE_REGISTRY_VIOLATION",
                message="YAML artifact exists outside the manifest-approved SDA directories",
            )
        return None

    def validate_payload_shape(self, path: Path, payload: dict[str, Any]) -> SDARegistryIssue | None:
        registry_kind = str(payload.get("registry_kind", "")).strip()
        if registry_kind in PROHIBITED_CANONICAL_CLASSES:
            return SDARegistryIssue(
                artifact_path=str(path),
                error_code="FALSE_REGISTRY_VIOLATION",
                message=f"Prohibited registry_kind declared in canonical SDA artifact: {registry_kind}",
                registry_kind=registry_kind,
            )

        raw_class = str(payload.get("artifact_class", "")).strip()
        if raw_class and raw_class not in {member.value for member in SDAArtifactClass}:
            return SDARegistryIssue(
                artifact_path=str(path),
                error_code="UNKNOWN_ARTIFACT_CLASS",
                message=f"Unknown artifact_class: {raw_class}",
            )

        artifact_id = str(payload.get("artifact_id", "")).strip()
        inferred_kind = _infer_kind_from_artifact_id(artifact_id)
        declared_kind = None
        if registry_kind:
            try:
                declared_kind = SDARegistryKind(registry_kind)
            except ValueError:
                return SDARegistryIssue(
                    artifact_path=str(path),
                    error_code="UNKNOWN_REGISTRY_KIND",
                    message=f"Unknown registry_kind: {registry_kind}",
                    artifact_id=artifact_id or None,
                    registry_kind=registry_kind,
                )
        if inferred_kind is not None and declared_kind is not None and inferred_kind != declared_kind:
            return SDARegistryIssue(
                artifact_path=str(path),
                artifact_id=artifact_id or None,
                registry_kind=registry_kind or None,
                error_code="ARTIFACT_ID_PREFIX_VIOLATION",
                message=f"Artifact ID prefix and registry_kind disagree: {artifact_id} vs {registry_kind}",
            )
        return None

    def validate_directory_contract(
        self,
        path: Path,
        record: SDARegistryRecord,
        allowed_paths: dict[str, Path],
    ) -> SDARegistryIssue | None:
        expected_bucket = KIND_TO_BUCKET[record.registry_kind]
        expected_path = allowed_paths[expected_bucket]
        if not _is_within(path, expected_path):
            return SDARegistryIssue(
                artifact_path=str(path),
                artifact_id=record.artifact_id,
                registry_kind=record.registry_kind.value,
                error_code="PATH_KIND_VIOLATION",
                message=(
                    f"{record.registry_kind.value} must live under "
                    f"{expected_path.as_posix()}"
                ),
            )
        return None


class SDACrosswalkCompiler:
    """Validate maintained crosswalk bundles against repo and registry reality."""

    def __init__(self, primitives_root: Path) -> None:
        self.primitives_root = primitives_root

    def validate(
        self,
        primitive_crosswalks: dict[str, PrimitiveToInvariantCrosswalkEntry],
        archetype_crosswalks: dict[str, ArchetypeToGeometryCrosswalkEntry],
        invariants: dict[str, ExistentialInvariantRecord],
        geometries: dict[str, ArchetypalGeometryRecord],
    ) -> list[SDARegistryIssue]:
        issues: list[SDARegistryIssue] = []
        primitive_ids = self._load_primitive_ids()

        for record in primitive_crosswalks.values():
            if record.primitive_id not in primitive_ids:
                issues.append(
                    SDARegistryIssue(
                        artifact_path="crosswalks/primitive_to_invariant",
                        artifact_id=record.artifact_id,
                        registry_kind=record.registry_kind.value,
                        error_code="CROSSWALK_REFERENCE_MISSING",
                        message=f"Primitive reference not found: {record.primitive_id}",
                    )
                )
            for mapping in record.linked_invariants:
                if mapping.target_id not in invariants:
                    issues.append(
                        SDARegistryIssue(
                            artifact_path="crosswalks/primitive_to_invariant",
                            artifact_id=record.artifact_id,
                            registry_kind=record.registry_kind.value,
                            error_code="CROSSWALK_REFERENCE_MISSING",
                            message=f"Invariant reference not found: {mapping.target_id}",
                        )
                    )

        for record in archetype_crosswalks.values():
            if record.content_archetype not in RETAINED_PRD02_CONTENT_ARCHETYPES:
                issues.append(
                    SDARegistryIssue(
                        artifact_path="crosswalks/archetype_to_geometry",
                        artifact_id=record.artifact_id,
                        registry_kind=record.registry_kind.value,
                        error_code="ARCHETYPE_INVENTORY_VIOLATION",
                        message=f"Unknown PRD-02 content archetype: {record.content_archetype}",
                    )
                )
            for mapping in record.linked_geometries:
                if mapping.target_id not in geometries:
                    issues.append(
                        SDARegistryIssue(
                            artifact_path="crosswalks/archetype_to_geometry",
                            artifact_id=record.artifact_id,
                            registry_kind=record.registry_kind.value,
                            error_code="CROSSWALK_REFERENCE_MISSING",
                            message=f"Archetypal geometry reference not found: {mapping.target_id}",
                        )
                    )
        return issues

    def _load_primitive_ids(self) -> set[str]:
        primitive_ids: set[str] = set()
        for path in self.primitives_root.rglob("*.yaml"):
            try:
                payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            experience_id = str(payload.get("experience_primitive_id", "")).strip()
            meaning_id = str(payload.get("primitive_id", "")).strip()
            if experience_id:
                primitive_ids.add(experience_id)
            if meaning_id:
                primitive_ids.add(meaning_id)
        return primitive_ids


class SDARegistryService:
    """Manifest-driven internal registry for SDA ontology and grammar."""

    def __init__(
        self,
        *,
        sda_root: Path | None = None,
        manifest_path: Path | None = None,
        primitives_root: Path | None = None,
        receipt_chain: ReceiptChain | None = None,
    ) -> None:
        coach_acronym = os.getenv("COACH_ACRONYM", "SDA")
        self.receipt_chain = receipt_chain or ReceiptChain(coach_acronym=coach_acronym[:3].upper())
        self.sda_root = sda_root or DEFAULT_SDA_ROOT
        self.manifest_path = manifest_path or (self.sda_root / "registry_manifest.yaml")
        self.primitives_root = primitives_root or PRIMITIVES_ROOT

        self.validator = SDAOntologyValidator(self.sda_root)
        self.crosswalk_compiler = SDACrosswalkCompiler(self.primitives_root)

        self.manifest: SDARegistryManifest | None = None
        self.manifest_health: SDAManifestHealth | None = None
        self.report = SDARegistryAuditReport()

        self.existential_invariants: dict[str, ExistentialInvariantRecord] = {}
        self.representation_geometries: dict[str, RepresentationGeometryRecord] = {}
        self.archetypal_geometries: dict[str, ArchetypalGeometryRecord] = {}
        self.species_composition_rules: dict[str, SpeciesCompositionRule] = {}
        self.primitive_to_invariant_crosswalks: dict[str, PrimitiveToInvariantCrosswalkEntry] = {}
        self.archetype_to_geometry_crosswalks: dict[str, ArchetypeToGeometryCrosswalkEntry] = {}
        self.artifact_path_index: dict[str, Path] = {}
        self._issues: list[SDARegistryIssue] = []

    def warm(
        self,
        *,
        strict: bool = False,
        allow_degraded_dev_mode: bool = False,
    ) -> SDARegistryAuditReport:
        snapshot = self._snapshot_state()
        self._clear_state()
        issues: list[SDARegistryIssue] = []

        manifest = self._load_manifest(issues)
        self.manifest = manifest
        if manifest is None:
            report = self._build_report(issues, ready=False)
            self.report = report
            if strict and not allow_degraded_dev_mode:
                raise RuntimeError("SDA registry manifest missing")
            return report

        allowed_paths = self._resolve_allowed_paths(manifest)
        manifest_health = self._build_manifest_health(manifest, allowed_paths)
        self.manifest_health = manifest_health

        issues.extend(self._scan_for_unexpected_yaml(allowed_paths))
        issues.extend(self._load_allowed_artifacts(allowed_paths))
        issues.extend(self._validate_manifest_counts(manifest))
        crosswalk_issues = self.crosswalk_compiler.validate(
            self.primitive_to_invariant_crosswalks,
            self.archetype_to_geometry_crosswalks,
            self.existential_invariants,
            self.archetypal_geometries,
        )
        for issue in crosswalk_issues:
            self._log_issue(issue, STAGE_CROSSWALK_ERROR)
        issues.extend(crosswalk_issues)

        ready = not issues
        report = self._build_report(issues, ready=ready)
        self.report = report

        if not ready:
            if snapshot is not None:
                self._restore_snapshot(snapshot)
            if strict and not allow_degraded_dev_mode:
                raise RuntimeError("SDA registry failed validation")

        self._log_receipt(
            stage_name=STAGE_STARTUP_WARM,
            artifact_path=str(self.sda_root),
            artifact_id=None,
            registry_kind=None,
            status="READY" if ready else "NOT_READY",
            message=(
                f"warm complete - invariants={report.existential_invariant_count}, "
                f"rep_geometries={report.representation_geometry_count}, "
                f"archetypes={report.archetypal_geometry_count}, "
                f"crosswalk_issues={len(issues)}"
            ),
            error_code=None if ready else "REGISTRY_NOT_READY",
        )
        return report

    def health(self) -> SDARegistryAuditReport:
        return self.report.model_copy(deep=True)

    def get_invariant(self, artifact_id: str) -> ExistentialInvariantRecord | None:
        return self.existential_invariants.get(artifact_id)

    def get_representation_geometry(self, artifact_id: str) -> RepresentationGeometryRecord | None:
        return self.representation_geometries.get(artifact_id)

    def get_archetypal_geometry(self, artifact_id: str) -> ArchetypalGeometryRecord | None:
        return self.archetypal_geometries.get(artifact_id)

    def get_species_grammar(self, artifact_id: str) -> SpeciesCompositionRule | None:
        return self.species_composition_rules.get(artifact_id)

    def get_crosswalk_bundle(self, name: str) -> dict[str, SDARegistryRecord]:
        normalized = name.strip().lower()
        if normalized == "primitive_to_invariant":
            return dict(self.primitive_to_invariant_crosswalks)
        if normalized == "archetype_to_geometry":
            return dict(self.archetype_to_geometry_crosswalks)
        return {}

    def reload_artifact(self, path: str | Path) -> SDAArtifactReloadResult:
        target_path = Path(path)
        if not target_path.is_absolute():
            target_path = (self.sda_root / target_path).resolve()
        snapshot = self._snapshot_state()
        if snapshot is None:
            return SDAArtifactReloadResult(
                artifact_path=str(target_path),
                success=False,
                error_code="REGISTRY_NOT_WARMED",
                message="Cannot reload artifact before a successful warm",
                report=self.health(),
            )

        manifest = self.manifest
        if manifest is None:
            return SDAArtifactReloadResult(
                artifact_path=str(target_path),
                success=False,
                error_code="SDA_MANIFEST_MISSING",
                message="Cannot reload without a loaded manifest",
                report=self.health(),
            )

        allowed_paths = self._resolve_allowed_paths(manifest)
        path_issue = self.validator.validate_artifact_path(target_path, allowed_paths)
        if path_issue is not None:
            self._log_issue(path_issue, STAGE_RELOAD_FAILURE)
            return SDAArtifactReloadResult(
                artifact_path=str(target_path),
                success=False,
                error_code=path_issue.error_code,
                message=path_issue.message,
                report=self.health(),
            )

        try:
            payload = yaml.safe_load(target_path.read_text(encoding="utf-8")) or {}
        except FileNotFoundError:
            issue = SDARegistryIssue(
                artifact_path=str(target_path),
                error_code="ARTIFACT_NOT_FOUND",
                message="Target artifact does not exist for reload",
            )
            self._log_issue(issue, STAGE_RELOAD_FAILURE)
            return SDAArtifactReloadResult(
                artifact_path=str(target_path),
                success=False,
                error_code=issue.error_code,
                message=issue.message,
                report=self.health(),
            )

        issue = self.validator.validate_payload_shape(target_path, payload)
        if issue is not None:
            self._restore_snapshot(snapshot)
            self._log_issue(issue, STAGE_RELOAD_FAILURE)
            return SDAArtifactReloadResult(
                artifact_path=str(target_path),
                success=False,
                error_code=issue.error_code,
                message=issue.message,
                report=self.health(),
            )

        record, record_issue = self._build_record(target_path, payload, allowed_paths)
        if record_issue is not None or record is None:
            self._restore_snapshot(snapshot)
            issue = record_issue or SDARegistryIssue(
                artifact_path=str(target_path),
                error_code="MODEL_VALIDATION_ERROR",
                message="Unknown artifact validation failure",
            )
            self._log_issue(issue, STAGE_RELOAD_FAILURE)
            return SDAArtifactReloadResult(
                artifact_path=str(target_path),
                artifact_id=issue.artifact_id,
                success=False,
                error_code=issue.error_code,
                message=issue.message,
                report=self.health(),
            )

        self._replace_record(record, target_path)
        affected_crosswalks = self._revalidate_direct_crosswalks(record)
        issues = self.crosswalk_compiler.validate(
            self.primitive_to_invariant_crosswalks,
            self.archetype_to_geometry_crosswalks,
            self.existential_invariants,
            self.archetypal_geometries,
        )
        if issues:
            self._restore_snapshot(snapshot)
            for item in issues:
                self._log_issue(item, STAGE_RELOAD_FAILURE)
            return SDAArtifactReloadResult(
                artifact_path=str(target_path),
                artifact_id=record.artifact_id,
                success=False,
                error_code=issues[0].error_code,
                message=issues[0].message,
                affected_crosswalks=affected_crosswalks,
                report=self.health(),
            )

        self.report = self._build_report([], ready=True)
        self._log_receipt(
            stage_name=STAGE_RELOAD_SUCCESS,
            artifact_path=str(target_path),
            artifact_id=record.artifact_id,
            registry_kind=record.registry_kind.value,
            status="READY",
            message=f"Reloaded artifact and preserved registry stability: {record.artifact_id}",
            error_code=None,
        )
        return SDAArtifactReloadResult(
            artifact_path=str(target_path),
            artifact_id=record.artifact_id,
            success=True,
            message="Artifact reloaded successfully",
            affected_crosswalks=affected_crosswalks,
            report=self.health(),
        )

    def _load_manifest(self, issues: list[SDARegistryIssue]) -> SDARegistryManifest | None:
        if not self.manifest_path.exists():
            issue = SDARegistryIssue(
                artifact_path=str(self.manifest_path),
                error_code="SDA_MANIFEST_MISSING",
                message="registry_manifest.yaml is required for SDA registry warm",
            )
            issues.append(issue)
            self._log_issue(issue, STAGE_MANIFEST_LOAD)
            return None
        try:
            payload = yaml.safe_load(self.manifest_path.read_text(encoding="utf-8")) or {}
            manifest = SDARegistryManifest.model_validate(payload)
        except Exception as exc:
            issue = SDARegistryIssue(
                artifact_path=str(self.manifest_path),
                error_code="SDA_MANIFEST_INVALID",
                message=f"Manifest validation failed: {exc}",
            )
            issues.append(issue)
            self._log_issue(issue, STAGE_MANIFEST_LOAD)
            return None

        self._log_receipt(
            stage_name=STAGE_MANIFEST_LOAD,
            artifact_path=str(self.manifest_path),
            artifact_id=None,
            registry_kind=None,
            status="READY",
            message="Loaded registry manifest",
            error_code=None,
        )
        return manifest

    def _resolve_allowed_paths(self, manifest: SDARegistryManifest) -> dict[str, Path]:
        return {
            "existential_invariants": (self.sda_root / manifest.ontology_paths["existential_invariants"]).resolve(),
            "representation_geometries": (self.sda_root / manifest.ontology_paths["representation_geometries"]).resolve(),
            "archetypal_geometries": (self.sda_root / manifest.grammar_paths["archetypal_geometries"]).resolve(),
            "species_composition": (self.sda_root / manifest.grammar_paths["species_composition"]).resolve(),
            "primitive_to_invariant": (self.sda_root / manifest.crosswalk_paths["primitive_to_invariant"]).resolve(),
            "archetype_to_geometry": (self.sda_root / manifest.crosswalk_paths["archetype_to_geometry"]).resolve(),
        }

    def _build_manifest_health(
        self,
        manifest: SDARegistryManifest,
        allowed_paths: dict[str, Path],
    ) -> SDAManifestHealth:
        path_exists = {name: path.exists() for name, path in allowed_paths.items()}
        return SDAManifestHealth(
            manifest_path=str(self.manifest_path),
            manifest_hash=_hash_file(self.manifest_path),
            ontology_paths={k: str(v) for k, v in manifest.ontology_paths.items()},
            grammar_paths={k: str(v) for k, v in manifest.grammar_paths.items()},
            crosswalk_paths={k: str(v) for k, v in manifest.crosswalk_paths.items()},
            expected_counts=dict(manifest.expected_counts),
            path_exists=path_exists,
            counts_matched=False,
        )

    def _scan_for_unexpected_yaml(self, allowed_paths: dict[str, Path]) -> list[SDARegistryIssue]:
        issues: list[SDARegistryIssue] = []
        for canonical_parent in (self.sda_root / "ontology", self.sda_root / "grammar", self.sda_root / "crosswalks"):
            if not canonical_parent.exists():
                continue
            for path in canonical_parent.rglob("*.yaml"):
                if path.name == "registry_manifest.yaml":
                    continue
                issue = self.validator.validate_artifact_path(path.resolve(), allowed_paths)
                if issue is not None:
                    issues.append(issue)
                    self._log_issue(issue, STAGE_ARTIFACT_REJECTION)
        return issues

    def _load_allowed_artifacts(self, allowed_paths: dict[str, Path]) -> list[SDARegistryIssue]:
        issues: list[SDARegistryIssue] = []
        for bucket_name, path in allowed_paths.items():
            if not path.exists():
                issue = SDARegistryIssue(
                    artifact_path=str(path),
                    error_code="MANIFEST_PATH_MISSING",
                    message=f"Manifest-declared SDA directory missing: {bucket_name}",
                )
                issues.append(issue)
                self._log_issue(issue, STAGE_ARTIFACT_REJECTION)
                continue

            for artifact_path in sorted(path.glob("*.yaml")):
                try:
                    payload = yaml.safe_load(artifact_path.read_text(encoding="utf-8")) or {}
                except Exception as exc:
                    issue = SDARegistryIssue(
                        artifact_path=str(artifact_path),
                        error_code="YAML_PARSE_ERROR",
                        message=f"YAML parse failure: {exc}",
                    )
                    issues.append(issue)
                    self._log_issue(issue, STAGE_ARTIFACT_REJECTION)
                    continue

                payload_issue = self.validator.validate_payload_shape(artifact_path, payload)
                if payload_issue is not None:
                    issues.append(payload_issue)
                    self._log_issue(payload_issue, STAGE_ARTIFACT_REJECTION)
                    continue

                record, record_issue = self._build_record(artifact_path, payload, allowed_paths)
                if record_issue is not None or record is None:
                    issue = record_issue or SDARegistryIssue(
                        artifact_path=str(artifact_path),
                        error_code="MODEL_VALIDATION_ERROR",
                        message="Unknown record construction failure",
                    )
                    issues.append(issue)
                    self._log_issue(issue, STAGE_ARTIFACT_REJECTION)
                    continue

                self._replace_record(record, artifact_path)
        return issues

    def _build_record(
        self,
        artifact_path: Path,
        payload: dict[str, Any],
        allowed_paths: dict[str, Path],
    ) -> tuple[SDARegistryRecord | None, SDARegistryIssue | None]:
        try:
            registry_kind = SDARegistryKind(str(payload.get("registry_kind", "")).strip())
            model_type = RECORD_MODEL_BY_KIND[registry_kind]
            record = model_type.model_validate(payload)
        except Exception as exc:
            error_code = _error_code_from_exception(exc)
            artifact_id = str(payload.get("artifact_id", "")).strip() or None
            registry_kind_raw = str(payload.get("registry_kind", "")).strip() or None
            return None, SDARegistryIssue(
                artifact_path=str(artifact_path),
                artifact_id=artifact_id,
                registry_kind=registry_kind_raw,
                error_code=error_code,
                message=str(exc),
            )

        path_issue = self.validator.validate_directory_contract(artifact_path.resolve(), record, allowed_paths)
        if path_issue is not None:
            return None, path_issue
        return record, None

    def _replace_record(self, record: SDARegistryRecord, artifact_path: Path) -> None:
        self.artifact_path_index[record.artifact_id] = artifact_path.resolve()
        if isinstance(record, ExistentialInvariantRecord):
            self.existential_invariants[record.artifact_id] = record
        elif isinstance(record, RepresentationGeometryRecord):
            self.representation_geometries[record.artifact_id] = record
        elif isinstance(record, ArchetypalGeometryRecord):
            self.archetypal_geometries[record.artifact_id] = record
        elif isinstance(record, SpeciesCompositionRule):
            self.species_composition_rules[record.artifact_id] = record
        elif isinstance(record, PrimitiveToInvariantCrosswalkEntry):
            self.primitive_to_invariant_crosswalks[record.artifact_id] = record
        elif isinstance(record, ArchetypeToGeometryCrosswalkEntry):
            self.archetype_to_geometry_crosswalks[record.artifact_id] = record

    def _revalidate_direct_crosswalks(self, record: SDARegistryRecord) -> list[str]:
        affected: list[str] = []
        if isinstance(record, ExistentialInvariantRecord):
            for crosswalk in self.primitive_to_invariant_crosswalks.values():
                if any(item.target_id == record.artifact_id for item in crosswalk.linked_invariants):
                    affected.append(crosswalk.artifact_id)
        elif isinstance(record, ArchetypalGeometryRecord):
            for crosswalk in self.archetype_to_geometry_crosswalks.values():
                if any(item.target_id == record.artifact_id for item in crosswalk.linked_geometries):
                    affected.append(crosswalk.artifact_id)
        elif isinstance(record, PrimitiveToInvariantCrosswalkEntry):
            affected.append(record.artifact_id)
        elif isinstance(record, ArchetypeToGeometryCrosswalkEntry):
            affected.append(record.artifact_id)
        return sorted(set(affected))

    def _validate_manifest_counts(self, manifest: SDARegistryManifest) -> list[SDARegistryIssue]:
        issues: list[SDARegistryIssue] = []
        actual_counts = {
            "existential_invariants": len(self.existential_invariants),
            "representation_geometries": len(self.representation_geometries),
            "archetypal_geometries": len(self.archetypal_geometries),
            "species_composition": len(self.species_composition_rules),
            "primitive_to_invariant": len(self.primitive_to_invariant_crosswalks),
            "archetype_to_geometry": len(self.archetype_to_geometry_crosswalks),
        }
        for key, expected in manifest.expected_counts.items():
            actual = actual_counts.get(key, 0)
            if actual < expected:
                issues.append(
                    SDARegistryIssue(
                        artifact_path=str(self.manifest_path),
                        error_code="MANIFEST_COUNT_MISMATCH",
                        message=f"{key} expected at least {expected} artifact(s) but loaded {actual}",
                    )
                )

        if self.manifest_health is not None:
            self.manifest_health.counts_matched = not issues
        return issues

    def _build_report(self, issues: list[SDARegistryIssue], *, ready: bool) -> SDARegistryAuditReport:
        manifest_hash = _hash_file(self.manifest_path) if self.manifest_path.exists() else ""
        registry_hash = _hash_paths(self.artifact_path_index.values())
        return SDARegistryAuditReport(
            last_load_at=datetime.now(timezone.utc).isoformat(),
            manifest_hash=manifest_hash,
            registry_hash=registry_hash,
            existential_invariant_count=len(self.existential_invariants),
            representation_geometry_count=len(self.representation_geometries),
            archetypal_geometry_count=len(self.archetypal_geometries),
            species_composition_rule_count=len(self.species_composition_rules),
            primitive_to_invariant_crosswalk_count=len(self.primitive_to_invariant_crosswalks),
            archetype_to_geometry_crosswalk_count=len(self.archetype_to_geometry_crosswalks),
            issues=issues,
            manifest_health=self.manifest_health,
            ready=ready,
        )

    def _snapshot_state(self) -> dict[str, Any] | None:
        if self.report.ready is False and not any(
            [
                self.existential_invariants,
                self.representation_geometries,
                self.archetypal_geometries,
                self.species_composition_rules,
                self.primitive_to_invariant_crosswalks,
                self.archetype_to_geometry_crosswalks,
            ]
        ):
            return None
        return {
            "manifest": deepcopy(self.manifest),
            "manifest_health": deepcopy(self.manifest_health),
            "report": self.report.model_copy(deep=True),
            "existential_invariants": deepcopy(self.existential_invariants),
            "representation_geometries": deepcopy(self.representation_geometries),
            "archetypal_geometries": deepcopy(self.archetypal_geometries),
            "species_composition_rules": deepcopy(self.species_composition_rules),
            "primitive_to_invariant_crosswalks": deepcopy(self.primitive_to_invariant_crosswalks),
            "archetype_to_geometry_crosswalks": deepcopy(self.archetype_to_geometry_crosswalks),
            "artifact_path_index": deepcopy(self.artifact_path_index),
        }

    def _restore_snapshot(self, snapshot: dict[str, Any]) -> None:
        self.manifest = snapshot["manifest"]
        self.manifest_health = snapshot["manifest_health"]
        self.report = snapshot["report"]
        self.existential_invariants = snapshot["existential_invariants"]
        self.representation_geometries = snapshot["representation_geometries"]
        self.archetypal_geometries = snapshot["archetypal_geometries"]
        self.species_composition_rules = snapshot["species_composition_rules"]
        self.primitive_to_invariant_crosswalks = snapshot["primitive_to_invariant_crosswalks"]
        self.archetype_to_geometry_crosswalks = snapshot["archetype_to_geometry_crosswalks"]
        self.artifact_path_index = snapshot["artifact_path_index"]

    def _clear_state(self) -> None:
        self.existential_invariants = {}
        self.representation_geometries = {}
        self.archetypal_geometries = {}
        self.species_composition_rules = {}
        self.primitive_to_invariant_crosswalks = {}
        self.archetype_to_geometry_crosswalks = {}
        self.artifact_path_index = {}
        self.manifest_health = None

    def _log_issue(self, issue: SDARegistryIssue, stage_name: str) -> None:
        self._log_receipt(
            stage_name=stage_name,
            artifact_path=issue.artifact_path,
            artifact_id=issue.artifact_id,
            registry_kind=issue.registry_kind,
            status="REJECTED",
            message=issue.message,
            error_code=issue.error_code,
        )

    def _log_receipt(
        self,
        *,
        stage_name: str,
        artifact_path: str,
        artifact_id: str | None,
        registry_kind: str | None,
        status: str,
        message: str,
        error_code: str | None,
    ) -> None:
        self.receipt_chain.log(
            agent_id="sda_registry_service",
            action=stage_name,
            asset_id=artifact_id,
            input_summary=artifact_path,
            output_summary=message,
            decision=status,
            decision_rationale=error_code,
            metadata={
                "stage_name": stage_name,
                "artifact_path": artifact_path,
                "artifact_id": artifact_id,
                "registry_kind": registry_kind,
                "status": status,
                "error_code": error_code,
            },
        )


def _hash_file(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _hash_paths(paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted({item.resolve() for item in paths}, key=lambda item: item.as_posix()):
        digest.update(path.as_posix().encode("utf-8"))
        if path.exists():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _infer_kind_from_artifact_id(artifact_id: str) -> SDARegistryKind | None:
    for prefix, kind in PREFIX_TO_KIND.items():
        if artifact_id.startswith(prefix):
            return kind
    return None


def _error_code_from_exception(exc: Exception) -> str:
    message = str(exc)
    if "Runtime-only scalar" in message:
        return "SCALAR_LAYER_VIOLATION"
    if "must start with" in message:
        return "ARTIFACT_ID_PREFIX_VIOLATION"
    return "MODEL_VALIDATION_ERROR"
