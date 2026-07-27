"""
CCP FR-ERA3-25 - Subliminal Function Library and Taxonomy service.

Deterministic, manifest-driven loader for the Subliminal Function Layer
canonical families, function definitions, compression rules, and
maintained crosswalk bundles.
"""

from __future__ import annotations

import hashlib
import os
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import cast

import yaml

from src.ccp.core.receipt_chain import ReceiptChain
from src.ccp.models.sda_registry_models import RETAINED_PRD02_CONTENT_ARCHETYPES
from src.ccp.models.sfl_registry_models import (
    FORBIDDEN_METRIC_KEYS,
    FORBIDDEN_SDA_OWNERSHIP_KEYS,
    RECOMMENDED_FUNCTION_FAMILY_COUNT,
    SFL_COMPRESSION_PREFIX,
    SFL_FAMILY_PREFIX,
    SFL_FUNCTION_PREFIX,
    SFL_ROOT_DIRNAME,
    SFL_XW_AR_PREFIX,
    SFL_XW_PF_PREFIX,
    SFL_XW_RG_PREFIX,
    SFL_XW_SF_PREFIX,
    ArchetypeToFunctionProfileRecord,
    FunctionFamilyCompressionRuleRecord,
    PrimitiveToFunctionFamilyCrosswalkRecord,
    RepresentationGeometryToFunctionProfileRecord,
    SFLArtifactReloadResult,
    SFLManifestHealth,
    SFLRegistryAuditReport,
    SFLRegistryIssue,
    SFLRegistryManifest,
    SFLRegistryRecord,
    SourceDocumentRef,
    SubliminalFunctionDefinitionRecord,
    SubliminalFunctionFamilyRecord,
    SurfaceConstraintProfileRecord,
)
from src.ccp.services.primitive_registry_service import PrimitiveRegistryQueryService
from src.ccp.services.sda_registry_service import SDARegistryService


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SFL_ROOT = REPO_ROOT / SFL_ROOT_DIRNAME
PRIMITIVES_ROOT = REPO_ROOT / "src" / "ccp" / "harness" / "primitives"
DEFAULT_SDA_ROOT = REPO_ROOT / "sda"

STAGE_MANIFEST_LOAD = "SFL25_MANIFEST_LOAD"
STAGE_STARTUP_WARM = "SFL25_STARTUP_WARM"
STAGE_ARTIFACT_REJECTION = "SFL25_ARTIFACT_REJECTION"
STAGE_RELOAD_SUCCESS = "SFL25_RELOAD_SUCCESS"
STAGE_RELOAD_FAILURE = "SFL25_RELOAD_FAILURE"

FORBIDDEN_DIRECTORY_NAMES: set[str] = {
    "associations",
    "association_rows",
    "raw_terms",
    "raw_associations",
    "metrics",
    "policies",
    "adversarial_assets",
    "failure_assets",
}

ALLOWED_CROSSWALK_DIRS: frozenset[str] = frozenset(
    {
        "primitive_to_function_family",
        "representation_geometry_to_function_profile",
        "archetype_to_function_profile",
        "surface_to_constraint_profile",
    }
)

RECORD_MODEL_BY_DIRNAME = {
    "families": SubliminalFunctionFamilyRecord,
    "functions": SubliminalFunctionDefinitionRecord,
    "compression_rules": FunctionFamilyCompressionRuleRecord,
    "primitive_to_function_family": PrimitiveToFunctionFamilyCrosswalkRecord,
    "representation_geometry_to_function_profile": RepresentationGeometryToFunctionProfileRecord,
    "archetype_to_function_profile": ArchetypeToFunctionProfileRecord,
    "surface_to_constraint_profile": SurfaceConstraintProfileRecord,
}


class SFLArtifactValidator:
    """Deterministic path, role, and ownership validator for canonical SFL artifacts."""

    def validate_artifact_path(
        self,
        path: Path,
        allowed_paths: dict[str, Path],
    ) -> SFLRegistryIssue | None:
        normalized = path.as_posix().lower()
        for forbidden_name in FORBIDDEN_DIRECTORY_NAMES:
            marker = f"/{forbidden_name}/"
            if marker in normalized or normalized.endswith(f"/{forbidden_name}.yaml"):
                return SFLRegistryIssue(
                    artifact_path=str(path),
                    error_code="FLAT_120_VIOLATION",
                    message=f"Forbidden flat-association or non-canonical directory detected: {forbidden_name}",
                )

        if not any(_is_within(path, root) for root in allowed_paths.values()):
            return SFLRegistryIssue(
                artifact_path=str(path),
                error_code="FALSE_REGISTRY_VIOLATION",
                message="YAML artifact exists outside the manifest-approved SFL directories",
            )
        return None

    def validate_payload_shape(self, path: Path, payload: dict[str, object]) -> SFLRegistryIssue | None:
        artifact_class = str(payload.get("artifact_class", "")).strip()
        allowed_classes = {
            "canonical_function_family",
            "function_definition",
            "compression_rule",
            "crosswalk",
        }
        if artifact_class and artifact_class not in allowed_classes:
            return SFLRegistryIssue(
                artifact_path=str(path),
                artifact_id=_payload_artifact_id(payload),
                error_code="UNKNOWN_ARTIFACT_CLASS",
                message=f"Unknown SFL artifact_class: {artifact_class}",
            )

        forbidden_metric_keys = sorted(FORBIDDEN_METRIC_KEYS.intersection(payload.keys()))
        if forbidden_metric_keys:
            return SFLRegistryIssue(
                artifact_path=str(path),
                artifact_id=_payload_artifact_id(payload),
                error_code="FUNCTION_METRIC_SEPARATION_VIOLATION",
                message=f"Metric fields cannot appear on canonical SFL artifacts: {', '.join(forbidden_metric_keys)}",
            )

        forbidden_sda_keys = sorted(FORBIDDEN_SDA_OWNERSHIP_KEYS.intersection(payload.keys()))
        if forbidden_sda_keys:
            return SFLRegistryIssue(
                artifact_path=str(path),
                artifact_id=_payload_artifact_id(payload),
                error_code="SDA_OWNERSHIP_VIOLATION",
                message=f"SDA-owned fields cannot appear on canonical SFL artifacts: {', '.join(forbidden_sda_keys)}",
            )

        return None

    def validate_directory_contract(
        self,
        path: Path,
        record: SFLRegistryRecord,
        allowed_paths: dict[str, Path],
    ) -> SFLRegistryIssue | None:
        expected_dirname = self._expected_dirname(record)
        expected_path = allowed_paths[expected_dirname]
        if not _is_within(path, expected_path):
            return SFLRegistryIssue(
                artifact_path=str(path),
                artifact_id=_record_artifact_id(record),
                error_code="PATH_ROLE_VIOLATION",
                message=f"Artifact role and directory disagree. Expected {expected_path.as_posix()}",
            )
        return None

    def _expected_dirname(self, record: SFLRegistryRecord) -> str:
        if isinstance(record, SubliminalFunctionFamilyRecord):
            return "families"
        if isinstance(record, SubliminalFunctionDefinitionRecord):
            return "functions"
        if isinstance(record, FunctionFamilyCompressionRuleRecord):
            return "compression_rules"
        if isinstance(record, PrimitiveToFunctionFamilyCrosswalkRecord):
            return "primitive_to_function_family"
        if isinstance(record, RepresentationGeometryToFunctionProfileRecord):
            return "representation_geometry_to_function_profile"
        if isinstance(record, ArchetypeToFunctionProfileRecord):
            return "archetype_to_function_profile"
        return "surface_to_constraint_profile"


class SFLRegistryService:
    """Manifest-driven internal registry for canonical SFL artifacts."""

    def __init__(
        self,
        *,
        sfl_root: Path | None = None,
        manifest_path: Path | None = None,
        primitives_root: Path | None = None,
        sda_root: Path | None = None,
        receipt_chain: ReceiptChain | None = None,
        primitive_registry_service: PrimitiveRegistryQueryService | None = None,
        sda_registry_service: SDARegistryService | None = None,
    ) -> None:
        coach_acronym = os.getenv("COACH_ACRONYM", "SFL")
        self.receipt_chain = receipt_chain or ReceiptChain(coach_acronym=coach_acronym[:3].upper())
        self.sfl_root = sfl_root or DEFAULT_SFL_ROOT
        self.manifest_path = manifest_path or (self.sfl_root / "registry_manifest.yaml")
        self.primitives_root = primitives_root or PRIMITIVES_ROOT
        self.sda_root = sda_root or DEFAULT_SDA_ROOT

        self.validator = SFLArtifactValidator()
        self.primitive_registry_service = primitive_registry_service or PrimitiveRegistryQueryService(
            primitives_root=self.primitives_root,
            receipt_chain=self.receipt_chain,
        )
        self.sda_registry_service = sda_registry_service or SDARegistryService(
            sda_root=self.sda_root,
            manifest_path=self.sda_root / "registry_manifest.yaml",
            receipt_chain=self.receipt_chain,
        )

        self.manifest: SFLRegistryManifest | None = None
        self.manifest_health: SFLManifestHealth | None = None
        self.report = SFLRegistryAuditReport(
            ready=False,
            family_count=0,
            function_count=0,
            compression_rule_count=0,
            primitive_to_function_family_crosswalk_count=0,
            representation_geometry_crosswalk_count=0,
            archetype_profile_crosswalk_count=0,
            surface_constraint_profile_count=0,
        )

        self.families: dict[str, SubliminalFunctionFamilyRecord] = {}
        self.functions: dict[str, SubliminalFunctionDefinitionRecord] = {}
        self.compression_rules: dict[str, FunctionFamilyCompressionRuleRecord] = {}
        self.primitive_crosswalks: dict[str, PrimitiveToFunctionFamilyCrosswalkRecord] = {}
        self.geometry_crosswalks: dict[str, RepresentationGeometryToFunctionProfileRecord] = {}
        self.archetype_crosswalks: dict[str, ArchetypeToFunctionProfileRecord] = {}
        self.surface_profiles: dict[str, SurfaceConstraintProfileRecord] = {}
        self.artifact_path_index: dict[str, Path] = {}

    def warm(
        self,
        *,
        strict: bool = False,
        allow_degraded_dev_mode: bool = False,
    ) -> SFLRegistryAuditReport:
        snapshot = self._snapshot_state()
        self._clear_state()
        issues: list[SFLRegistryIssue] = []

        manifest = self._load_manifest(issues)
        self.manifest = manifest
        if manifest is None:
            report = self._build_report(issues, ready=False)
            self.report = report
            if strict and not allow_degraded_dev_mode:
                raise RuntimeError("SFL registry manifest missing")
            return report

        allowed_paths = self._resolve_allowed_paths(manifest)
        self.manifest_health = self._build_manifest_health(manifest, allowed_paths)

        issues.extend(self._scan_for_unexpected_yaml(allowed_paths))
        issues.extend(self._load_allowed_artifacts(allowed_paths))
        issues.extend(self._validate_family_compression_rules())
        issues.extend(self._validate_registry_references())
        issues.extend(self._validate_manifest_counts(manifest))

        ready = not issues
        report = self._build_report(issues, ready=ready)
        self.report = report

        if not ready:
            if snapshot is not None:
                self._restore_snapshot(snapshot)
            if strict and not allow_degraded_dev_mode:
                raise RuntimeError("SFL registry failed validation")

        self._log_receipt(
            stage_name=STAGE_STARTUP_WARM,
            artifact_path=str(self.sfl_root),
            artifact_id=None,
            status="READY" if ready else "NOT_READY",
            message=(
                f"warm complete - families={report.family_count}, "
                f"functions={report.function_count}, "
                f"compression_rules={report.compression_rule_count}, "
                f"issues={len(report.issues)}"
            ),
            error_code=None if ready else "REGISTRY_NOT_READY",
        )
        return report

    def health(self) -> SFLRegistryAuditReport:
        return self.report.model_copy(deep=True)

    def get_family(self, artifact_id: str) -> SubliminalFunctionFamilyRecord | None:
        return self.families.get(artifact_id)

    def get_function(self, artifact_id: str) -> SubliminalFunctionDefinitionRecord | None:
        return self.functions.get(artifact_id)

    def get_crosswalk_bundle(self, name: str) -> dict[str, SFLRegistryRecord]:
        normalized = name.strip().lower()
        if normalized == "primitive_to_function_family":
            return dict(self.primitive_crosswalks)
        if normalized == "representation_geometry_to_function_profile":
            return dict(self.geometry_crosswalks)
        if normalized == "archetype_to_function_profile":
            return dict(self.archetype_crosswalks)
        if normalized == "surface_to_constraint_profile":
            return dict(self.surface_profiles)
        return {}

    def reload_artifact(self, path: str | Path) -> SFLArtifactReloadResult:
        target_path = Path(path)
        if not target_path.is_absolute():
            target_path = (self.sfl_root / target_path).resolve()
        snapshot = self._snapshot_state()
        if snapshot is None:
            return SFLArtifactReloadResult(
                artifact_path=str(target_path),
                success=False,
                error_code="REGISTRY_NOT_WARMED",
                message="Cannot reload artifact before a successful warm",
                report=self.health(),
            )

        manifest = self.manifest
        if manifest is None:
            return SFLArtifactReloadResult(
                artifact_path=str(target_path),
                success=False,
                error_code="SFL_MANIFEST_MISSING",
                message="Cannot reload without a loaded manifest",
                report=self.health(),
            )

        allowed_paths = self._resolve_allowed_paths(manifest)
        path_issue = self.validator.validate_artifact_path(target_path, allowed_paths)
        if path_issue is not None:
            self._log_issue(path_issue, STAGE_RELOAD_FAILURE)
            return SFLArtifactReloadResult(
                artifact_path=str(target_path),
                success=False,
                error_code=path_issue.error_code,
                message=path_issue.message,
                report=self.health(),
            )

        try:
            payload = cast(dict[str, object], yaml.safe_load(target_path.read_text(encoding="utf-8")) or {})
        except FileNotFoundError:
            issue = SFLRegistryIssue(
                artifact_path=str(target_path),
                error_code="ARTIFACT_NOT_FOUND",
                message="Target artifact does not exist for reload",
            )
            self._log_issue(issue, STAGE_RELOAD_FAILURE)
            return SFLArtifactReloadResult(
                artifact_path=str(target_path),
                success=False,
                error_code=issue.error_code,
                message=issue.message,
                report=self.health(),
            )

        payload_issue = self.validator.validate_payload_shape(target_path, payload)
        if payload_issue is not None:
            self._restore_snapshot(snapshot)
            self._log_issue(payload_issue, STAGE_RELOAD_FAILURE)
            return SFLArtifactReloadResult(
                artifact_path=str(target_path),
                artifact_id=payload_issue.artifact_id,
                success=False,
                error_code=payload_issue.error_code,
                message=payload_issue.message,
                previous_state_restored=True,
                report=self.health(),
            )

        record, record_issue = self._build_record(target_path, payload, allowed_paths)
        if record_issue is not None or record is None:
            self._restore_snapshot(snapshot)
            issue = record_issue or SFLRegistryIssue(
                artifact_path=str(target_path),
                error_code="MODEL_VALIDATION_ERROR",
                message="Unknown artifact validation failure",
            )
            self._log_issue(issue, STAGE_RELOAD_FAILURE)
            return SFLArtifactReloadResult(
                artifact_path=str(target_path),
                artifact_id=issue.artifact_id,
                success=False,
                error_code=issue.error_code,
                message=issue.message,
                previous_state_restored=True,
                report=self.health(),
            )

        self._replace_record(record, target_path)
        issues = self._validate_family_compression_rules()
        issues.extend(self._validate_registry_references())
        if issues:
            self._restore_snapshot(snapshot)
            for issue in issues:
                self._log_issue(issue, STAGE_RELOAD_FAILURE)
            first_issue = issues[0]
            return SFLArtifactReloadResult(
                artifact_path=str(target_path),
                artifact_id=_record_artifact_id(record),
                success=False,
                error_code=first_issue.error_code,
                message=first_issue.message,
                previous_state_restored=True,
                report=self.health(),
            )

        self.report = self._build_report([], ready=True)
        self._log_receipt(
            stage_name=STAGE_RELOAD_SUCCESS,
            artifact_path=str(target_path),
            artifact_id=_record_artifact_id(record),
            status="READY",
            message=f"Reloaded artifact and preserved SFL registry stability: {_record_artifact_id(record)}",
            error_code=None,
        )
        return SFLArtifactReloadResult(
            artifact_path=str(target_path),
            artifact_id=_record_artifact_id(record),
            success=True,
            message="Artifact reloaded successfully",
            report=self.health(),
        )

    def _load_manifest(self, issues: list[SFLRegistryIssue]) -> SFLRegistryManifest | None:
        if not self.manifest_path.exists():
            issue = SFLRegistryIssue(
                artifact_path=str(self.manifest_path),
                error_code="SFL_MANIFEST_MISSING",
                message="registry_manifest.yaml is required for SFL registry warm",
            )
            issues.append(issue)
            self._log_issue(issue, STAGE_MANIFEST_LOAD)
            return None
        try:
            payload = cast(dict[str, object], yaml.safe_load(self.manifest_path.read_text(encoding="utf-8")) or {})
            manifest = SFLRegistryManifest.model_validate(payload)
        except Exception as exc:  # pragma: no cover - exercised through integration failure
            issue = SFLRegistryIssue(
                artifact_path=str(self.manifest_path),
                error_code="SFL_MANIFEST_INVALID",
                message=f"Manifest validation failed: {exc}",
            )
            issues.append(issue)
            self._log_issue(issue, STAGE_MANIFEST_LOAD)
            return None

        self._log_receipt(
            stage_name=STAGE_MANIFEST_LOAD,
            artifact_path=str(self.manifest_path),
            artifact_id=None,
            status="READY",
            message="Loaded SFL registry manifest",
            error_code=None,
        )
        return manifest

    def _resolve_allowed_paths(self, manifest: SFLRegistryManifest) -> dict[str, Path]:
        allowed_paths = {
            "families": (self.sfl_root / manifest.family_path).resolve(),
            "functions": (self.sfl_root / manifest.function_path).resolve(),
            "compression_rules": (self.sfl_root / manifest.compression_rule_path).resolve(),
        }
        for relative_path in manifest.crosswalk_paths:
            resolved = (self.sfl_root / relative_path).resolve()
            allowed_paths[resolved.name] = resolved
        return allowed_paths

    def _build_manifest_health(
        self,
        manifest: SFLRegistryManifest,
        allowed_paths: dict[str, Path],
    ) -> SFLManifestHealth:
        crosswalk_paths = [str(path) for name, path in allowed_paths.items() if name in ALLOWED_CROSSWALK_DIRS]
        return SFLManifestHealth(
            manifest_path=str(self.manifest_path),
            artifact_root=manifest.artifact_root,
            manifest_hash=_hash_file(self.manifest_path),
            family_path=str(allowed_paths["families"]),
            function_path=str(allowed_paths["functions"]),
            compression_rule_path=str(allowed_paths["compression_rules"]),
            crosswalk_paths=crosswalk_paths,
            resolved_crosswalk_paths={
                name: str(path) for name, path in allowed_paths.items() if name in ALLOWED_CROSSWALK_DIRS
            },
            expected_counts=manifest.expected_counts,
            path_exists={name: path.exists() for name, path in allowed_paths.items()},
            counts_matched=False,
        )

    def _scan_for_unexpected_yaml(self, allowed_paths: dict[str, Path]) -> list[SFLRegistryIssue]:
        issues: list[SFLRegistryIssue] = []
        for path in self.sfl_root.rglob("*.yaml"):
            if path.resolve() == self.manifest_path.resolve():
                continue
            if "failure_corpus" in path.parts:
                continue
            issue = self.validator.validate_artifact_path(path.resolve(), allowed_paths)
            if issue is not None:
                issues.append(issue)
                self._log_issue(issue, STAGE_ARTIFACT_REJECTION)
        return issues

    def _load_allowed_artifacts(self, allowed_paths: dict[str, Path]) -> list[SFLRegistryIssue]:
        issues: list[SFLRegistryIssue] = []
        for dirname, path in allowed_paths.items():
            if dirname not in RECORD_MODEL_BY_DIRNAME and dirname not in {"families", "functions", "compression_rules"}:
                continue
            if not path.exists():
                issue = SFLRegistryIssue(
                    artifact_path=str(path),
                    error_code="MANIFEST_PATH_MISSING",
                    message=f"Manifest-declared SFL directory missing: {dirname}",
                )
                issues.append(issue)
                self._log_issue(issue, STAGE_ARTIFACT_REJECTION)
                continue

            for artifact_path in sorted(path.glob("*.yaml")):
                try:
                    payload = cast(dict[str, object], yaml.safe_load(artifact_path.read_text(encoding="utf-8")) or {})
                except Exception as exc:
                    issue = SFLRegistryIssue(
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
                    issue = record_issue or SFLRegistryIssue(
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
        payload: dict[str, object],
        allowed_paths: dict[str, Path],
    ) -> tuple[SFLRegistryRecord | None, SFLRegistryIssue | None]:
        try:
            model_type = RECORD_MODEL_BY_DIRNAME[artifact_path.parent.name]
            record = model_type.model_validate(payload)
        except Exception as exc:
            return None, SFLRegistryIssue(
                artifact_path=str(artifact_path),
                artifact_id=_payload_artifact_id(payload),
                error_code=_error_code_from_exception(exc),
                message=str(exc),
            )

        path_issue = self.validator.validate_directory_contract(artifact_path.resolve(), record, allowed_paths)
        if path_issue is not None:
            return None, path_issue
        return record, None

    def _replace_record(self, record: SFLRegistryRecord, artifact_path: Path) -> None:
        artifact_id = _record_artifact_id(record)
        self.artifact_path_index[artifact_id] = artifact_path.resolve()
        if isinstance(record, SubliminalFunctionFamilyRecord):
            self.families[artifact_id] = record
        elif isinstance(record, SubliminalFunctionDefinitionRecord):
            self.functions[artifact_id] = record
        elif isinstance(record, FunctionFamilyCompressionRuleRecord):
            self.compression_rules[artifact_id] = record
        elif isinstance(record, PrimitiveToFunctionFamilyCrosswalkRecord):
            self.primitive_crosswalks[artifact_id] = record
        elif isinstance(record, RepresentationGeometryToFunctionProfileRecord):
            self.geometry_crosswalks[artifact_id] = record
        elif isinstance(record, ArchetypeToFunctionProfileRecord):
            self.archetype_crosswalks[artifact_id] = record
        else:
            self.surface_profiles[artifact_id] = cast(SurfaceConstraintProfileRecord, record)

    def _validate_family_compression_rules(self) -> list[SFLRegistryIssue]:
        issues: list[SFLRegistryIssue] = []
        rules_by_family: dict[str, list[FunctionFamilyCompressionRuleRecord]] = {}
        raw_term_owner: dict[str, str] = {}
        for rule in self.compression_rules.values():
            rules_by_family.setdefault(rule.canonical_family_id, []).append(rule)
            if len(rule.raw_terms) < 2 and not rule.duplicate_rejection_terms:
                issues.append(
                    SFLRegistryIssue(
                        artifact_path=str(self.artifact_path_index.get(rule.artifact_id, Path(rule.artifact_id))),
                        artifact_id=rule.artifact_id,
                        error_code="FLAT_120_VIOLATION",
                        message="Compression rules must compress multiple related raw terms or provide duplicate rejection terms",
                    )
                )
            for raw_term in rule.raw_terms:
                normalized = raw_term.raw_term.strip().lower()
                prior_owner = raw_term_owner.get(normalized)
                if prior_owner is not None and prior_owner != rule.canonical_family_id:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(rule.artifact_id, Path(rule.artifact_id))),
                            artifact_id=rule.artifact_id,
                            error_code="COMPRESSION_OVERLAP_VIOLATION",
                            message=f"Raw term '{normalized}' is claimed by multiple canonical families",
                        )
                    )
                raw_term_owner[normalized] = rule.canonical_family_id

        for family in self.families.values():
            family_rules = rules_by_family.get(family.artifact_id, [])
            if not family_rules:
                issues.append(
                    SFLRegistryIssue(
                        artifact_path=str(self.artifact_path_index.get(family.artifact_id, Path(family.artifact_id))),
                        artifact_id=family.artifact_id,
                        error_code="COMPRESSION_RULE_MISSING",
                        message="Every canonical family must be backed by at least one compression rule",
                    )
                )
                continue

            covered_raw_terms = {
                alias.raw_term.strip().lower()
                for rule in family_rules
                for alias in rule.raw_terms
            }
            for alias in family.related_raw_terms:
                normalized = alias.raw_term.strip().lower()
                if normalized not in covered_raw_terms:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(family.artifact_id, Path(family.artifact_id))),
                            artifact_id=family.artifact_id,
                            error_code="COMPRESSION_COVERAGE_MISSING",
                            message=f"Family raw term '{normalized}' is not covered by a compression rule",
                        )
                    )
        return issues

    def _validate_registry_references(self) -> list[SFLRegistryIssue]:
        issues: list[SFLRegistryIssue] = []
        self.primitive_registry_service.warm_registry()
        sda_report = self.sda_registry_service.warm()
        if not sda_report.ready:
            issues.append(
                SFLRegistryIssue(
                    artifact_path=str(self.sda_root),
                    error_code="SDA_INTEROP_NOT_READY",
                    message="SDA registry must be warm and ready before SFL can validate geometry references",
                )
            )
            return issues

        for function in self.functions.values():
            if function.family_id not in self.families:
                issues.append(
                    SFLRegistryIssue(
                        artifact_path=str(self.artifact_path_index.get(function.artifact_id, Path(function.artifact_id))),
                        artifact_id=function.artifact_id,
                        error_code="FUNCTION_FAMILY_REFERENCE_MISSING",
                        message=f"Function references missing family: {function.family_id}",
                    )
                )
            for primitive_ref in function.primitive_links:
                if self.primitive_registry_service.query_by_id(primitive_ref.primitive_id) is None:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(function.artifact_id, Path(function.artifact_id))),
                            artifact_id=function.artifact_id,
                            error_code="PRIMITIVE_REFERENCE_MISSING",
                            message=f"Primitive reference not found: {primitive_ref.primitive_id}",
                        )
                    )
            for geometry_ref in function.geometry_links:
                if self.sda_registry_service.get_representation_geometry(geometry_ref.geometry_id) is None and self.sda_registry_service.get_archetypal_geometry(geometry_ref.geometry_id) is None:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(function.artifact_id, Path(function.artifact_id))),
                            artifact_id=function.artifact_id,
                            error_code="GEOMETRY_REFERENCE_MISSING",
                            message=f"Geometry reference not found: {geometry_ref.geometry_id}",
                        )
                    )
            for archetype_ref in function.archetype_links:
                if archetype_ref.archetype_name not in RETAINED_PRD02_CONTENT_ARCHETYPES:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(function.artifact_id, Path(function.artifact_id))),
                            artifact_id=function.artifact_id,
                            error_code="ARCHETYPE_REFERENCE_MISSING",
                            message=f"Unknown PRD-02 content archetype: {archetype_ref.archetype_name}",
                        )
                    )

        for crosswalk in self.primitive_crosswalks.values():
            for primitive_ref in crosswalk.primitive_links:
                if self.primitive_registry_service.query_by_id(primitive_ref.primitive_id) is None:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(crosswalk.artifact_id, Path(crosswalk.artifact_id))),
                            artifact_id=crosswalk.artifact_id,
                            error_code="PRIMITIVE_REFERENCE_MISSING",
                            message=f"Primitive reference not found: {primitive_ref.primitive_id}",
                        )
                    )
            for family_id in crosswalk.target_family_ids:
                if family_id not in self.families:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(crosswalk.artifact_id, Path(crosswalk.artifact_id))),
                            artifact_id=crosswalk.artifact_id,
                            error_code="FUNCTION_FAMILY_REFERENCE_MISSING",
                            message=f"Primitive crosswalk targets missing family: {family_id}",
                        )
                    )

        for crosswalk in self.geometry_crosswalks.values():
            for geometry_ref in crosswalk.geometry_links:
                if self.sda_registry_service.get_representation_geometry(geometry_ref.geometry_id) is None:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(crosswalk.artifact_id, Path(crosswalk.artifact_id))),
                            artifact_id=crosswalk.artifact_id,
                            error_code="GEOMETRY_REFERENCE_MISSING",
                            message=f"Representation geometry reference not found: {geometry_ref.geometry_id}",
                        )
                    )
            for function_id in crosswalk.preferred_function_ids + crosswalk.discouraged_function_ids:
                if function_id not in self.functions:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(crosswalk.artifact_id, Path(crosswalk.artifact_id))),
                            artifact_id=crosswalk.artifact_id,
                            error_code="FUNCTION_REFERENCE_MISSING",
                            message=f"Geometry crosswalk targets missing function: {function_id}",
                        )
                    )

        for crosswalk in self.archetype_crosswalks.values():
            for archetype_ref in crosswalk.archetype_links:
                if archetype_ref.archetype_name not in RETAINED_PRD02_CONTENT_ARCHETYPES:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(crosswalk.artifact_id, Path(crosswalk.artifact_id))),
                            artifact_id=crosswalk.artifact_id,
                            error_code="ARCHETYPE_REFERENCE_MISSING",
                            message=f"Unknown PRD-02 content archetype: {archetype_ref.archetype_name}",
                        )
                    )
            for function_id in crosswalk.preferred_function_ids:
                if function_id not in self.functions:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(crosswalk.artifact_id, Path(crosswalk.artifact_id))),
                            artifact_id=crosswalk.artifact_id,
                            error_code="FUNCTION_REFERENCE_MISSING",
                            message=f"Archetype crosswalk targets missing function: {function_id}",
                        )
                    )
            for family_id in crosswalk.required_family_ids + crosswalk.discouraged_family_ids:
                if family_id not in self.families:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(crosswalk.artifact_id, Path(crosswalk.artifact_id))),
                            artifact_id=crosswalk.artifact_id,
                            error_code="FUNCTION_FAMILY_REFERENCE_MISSING",
                            message=f"Archetype crosswalk targets missing family: {family_id}",
                        )
                    )

        for profile in self.surface_profiles.values():
            for family_id in profile.preferred_family_ids + profile.discouraged_family_ids:
                if family_id not in self.families:
                    issues.append(
                        SFLRegistryIssue(
                            artifact_path=str(self.artifact_path_index.get(profile.artifact_id, Path(profile.artifact_id))),
                            artifact_id=profile.artifact_id,
                            error_code="FUNCTION_FAMILY_REFERENCE_MISSING",
                            message=f"Surface profile targets missing family: {family_id}",
                        )
                    )

        return issues

    def _validate_manifest_counts(self, manifest: SFLRegistryManifest) -> list[SFLRegistryIssue]:
        issues: list[SFLRegistryIssue] = []
        actual_counts = {
            "families": len(self.families),
            "functions": len(self.functions),
            "compression_rules": len(self.compression_rules),
            "primitive_to_function_family_crosswalks": len(self.primitive_crosswalks),
            "representation_geometry_crosswalks": len(self.geometry_crosswalks),
            "archetype_profile_crosswalks": len(self.archetype_crosswalks),
            "surface_constraint_profiles": len(self.surface_profiles),
        }
        for key, expected in manifest.expected_counts.model_dump().items():
            actual = actual_counts.get(key, 0)
            if actual < expected:
                issues.append(
                    SFLRegistryIssue(
                        artifact_path=str(self.manifest_path),
                        error_code="MANIFEST_COUNT_MISMATCH",
                        message=f"{key} expected at least {expected} artifact(s) but loaded {actual}",
                    )
                )

        if self.manifest_health is not None:
            self.manifest_health.counts_matched = not issues
        return issues

    def _build_report(self, issues: list[SFLRegistryIssue], *, ready: bool) -> SFLRegistryAuditReport:
        return SFLRegistryAuditReport(
            ready=ready,
            family_count=len(self.families),
            function_count=len(self.functions),
            compression_rule_count=len(self.compression_rules),
            primitive_to_function_family_crosswalk_count=len(self.primitive_crosswalks),
            representation_geometry_crosswalk_count=len(self.geometry_crosswalks),
            archetype_profile_crosswalk_count=len(self.archetype_crosswalks),
            surface_constraint_profile_count=len(self.surface_profiles),
            issues=issues,
            manifest_health=self.manifest_health,
        )

    def _snapshot_state(self) -> dict[str, object] | None:
        if not any(
            [
                self.families,
                self.functions,
                self.compression_rules,
                self.primitive_crosswalks,
                self.geometry_crosswalks,
                self.archetype_crosswalks,
                self.surface_profiles,
            ]
        ) and self.report.ready is False:
            return None
        return {
            "manifest": deepcopy(self.manifest),
            "manifest_health": deepcopy(self.manifest_health),
            "report": self.report.model_copy(deep=True),
            "families": deepcopy(self.families),
            "functions": deepcopy(self.functions),
            "compression_rules": deepcopy(self.compression_rules),
            "primitive_crosswalks": deepcopy(self.primitive_crosswalks),
            "geometry_crosswalks": deepcopy(self.geometry_crosswalks),
            "archetype_crosswalks": deepcopy(self.archetype_crosswalks),
            "surface_profiles": deepcopy(self.surface_profiles),
            "artifact_path_index": deepcopy(self.artifact_path_index),
        }

    def _restore_snapshot(self, snapshot: dict[str, object]) -> None:
        self.manifest = cast(SFLRegistryManifest | None, snapshot["manifest"])
        self.manifest_health = cast(SFLManifestHealth | None, snapshot["manifest_health"])
        self.report = cast(SFLRegistryAuditReport, snapshot["report"])
        self.families = cast(dict[str, SubliminalFunctionFamilyRecord], snapshot["families"])
        self.functions = cast(dict[str, SubliminalFunctionDefinitionRecord], snapshot["functions"])
        self.compression_rules = cast(dict[str, FunctionFamilyCompressionRuleRecord], snapshot["compression_rules"])
        self.primitive_crosswalks = cast(dict[str, PrimitiveToFunctionFamilyCrosswalkRecord], snapshot["primitive_crosswalks"])
        self.geometry_crosswalks = cast(dict[str, RepresentationGeometryToFunctionProfileRecord], snapshot["geometry_crosswalks"])
        self.archetype_crosswalks = cast(dict[str, ArchetypeToFunctionProfileRecord], snapshot["archetype_crosswalks"])
        self.surface_profiles = cast(dict[str, SurfaceConstraintProfileRecord], snapshot["surface_profiles"])
        self.artifact_path_index = cast(dict[str, Path], snapshot["artifact_path_index"])

    def _clear_state(self) -> None:
        self.families = {}
        self.functions = {}
        self.compression_rules = {}
        self.primitive_crosswalks = {}
        self.geometry_crosswalks = {}
        self.archetype_crosswalks = {}
        self.surface_profiles = {}
        self.artifact_path_index = {}
        self.manifest_health = None

    def _log_issue(self, issue: SFLRegistryIssue, stage_name: str) -> None:
        self._log_receipt(
            stage_name=stage_name,
            artifact_path=issue.artifact_path,
            artifact_id=issue.artifact_id,
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
        status: str,
        message: str,
        error_code: str | None,
    ) -> None:
        self.receipt_chain.log(
            agent_id="sfl_registry_service",
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
                "status": status,
                "error_code": error_code,
            },
        )


def _payload_artifact_id(payload: dict[str, object]) -> str | None:
    artifact_id = str(payload.get("artifact_id", "")).strip()
    return artifact_id or None


def _record_artifact_id(record: SFLRegistryRecord) -> str:
    return record.artifact_id


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _hash_file(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _error_code_from_exception(exc: Exception) -> str:
    message = str(exc)
    if "extra_forbidden" in message:
        return "MODEL_VALIDATION_ERROR"
    if "SFL-FAM-" in message or "SFL-FN-" in message or "SFL-CR-" in message:
        return "ARTIFACT_ID_PREFIX_VIOLATION"
    if "Input should be" in message:
        return "MODEL_VALIDATION_ERROR"
    return "MODEL_VALIDATION_ERROR"
