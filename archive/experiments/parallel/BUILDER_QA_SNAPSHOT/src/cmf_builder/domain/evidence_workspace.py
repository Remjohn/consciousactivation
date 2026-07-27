from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Mapping


class EvidenceWorkspaceError(Exception):
    code = "EvidenceWorkspaceError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class SourceProfileInvalid(EvidenceWorkspaceError):
    code = "SourceProfileInvalid"


class SourcePathRejected(EvidenceWorkspaceError):
    code = "SourcePathRejected"


class SourceHashMismatch(EvidenceWorkspaceError):
    code = "SourceHashMismatch"


class AuthorityMetadataIncomplete(EvidenceWorkspaceError):
    code = "AuthorityMetadataIncomplete"


class RequiredRoleMissing(EvidenceWorkspaceError):
    code = "RequiredRoleMissing"


class UnsupportedSourceKind(EvidenceWorkspaceError):
    code = "UnsupportedSourceKind"


class UnsupportedMediaType(EvidenceWorkspaceError):
    code = "UnsupportedMediaType"


class ArchiveSafetyRejected(EvidenceWorkspaceError):
    code = "ArchiveSafetyRejected"


class ResourceLimitExceeded(EvidenceWorkspaceError):
    code = "ResourceLimitExceeded"


class SourceMutationDetected(EvidenceWorkspaceError):
    code = "SourceMutationDetected"


@dataclass(frozen=True, slots=True)
class TargetCandidate:
    uri: str
    source_kind: str
    sha256: str
    role: str
    precedence: int


@dataclass(frozen=True, slots=True)
class AuthorityPolicy:
    owner: str
    authority_kind: str
    usage_authority: str
    license: str
    privacy_class: str
    consent_policy_required: bool


@dataclass(frozen=True, slots=True)
class SafetyLimits:
    max_directory_depth: int
    max_file_count: int
    max_total_uncompressed_bytes: int
    max_single_file_bytes: int
    max_zip_decompression_ratio: int
    max_nested_archive_depth: int
    reject_symlinks: bool
    reject_casefold_collisions: bool
    reject_absolute_or_parent_paths: bool
    extract_archives: bool
    network_access: bool


@dataclass(frozen=True, slots=True)
class SourceProfile:
    profile_id: str
    version: str
    status: str
    target_profile_ref: str
    category_binding: str
    production_eligible: bool
    certified: bool
    target_candidate: TargetCandidate
    required_roles: tuple[str, ...]
    recommended_roles: tuple[str, ...]
    optional_roles: tuple[str, ...]
    prohibited_roles: tuple[str, ...]
    allowed_source_kinds: tuple[str, ...]
    allowed_media_types: tuple[str, ...]
    prohibited_extensions: tuple[str, ...]
    authority_policy: AuthorityPolicy
    safety_limits: SafetyLimits
    amendment_rule: str
    profile_sha256: str

    @property
    def ref(self) -> str:
        return f"{self.profile_id}@{self.version}"

    @classmethod
    def from_json_bytes(
        cls, content: bytes, *, observed_sha256: str | None = None
    ) -> "SourceProfile":
        digest = sha256(content).hexdigest()
        if observed_sha256 is not None and digest != observed_sha256:
            raise SourceHashMismatch(
                "Source-profile bytes do not match the governed hash.",
                expected_sha256=observed_sha256,
                observed_sha256=digest,
            )
        try:
            value = json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise SourceProfileInvalid("Source profile is not valid UTF-8 JSON.") from error
        if not isinstance(value, dict):
            raise SourceProfileInvalid("Source profile must be a JSON object.")
        try:
            candidate = value["target_candidate"]
            authority = value["authority_policy"]
            limits = value["safety_limits"]
            profile = cls(
                profile_id=_required_text(value, "profile_id"),
                version=_required_text(value, "version"),
                status=_required_text(value, "status"),
                target_profile_ref=_required_text(value, "target_profile_ref"),
                category_binding=_required_text(value, "category_binding"),
                production_eligible=_required_bool(value, "production_eligible"),
                certified=_required_bool(value, "certified"),
                target_candidate=TargetCandidate(
                    uri=_required_text(candidate, "uri"),
                    source_kind=_required_text(candidate, "source_kind"),
                    sha256=_required_hash(candidate, "sha256"),
                    role=_required_text(candidate, "role"),
                    precedence=_required_positive_int(candidate, "precedence"),
                ),
                required_roles=_required_text_tuple(value, "required_roles"),
                recommended_roles=_required_text_tuple(value, "recommended_roles"),
                optional_roles=_required_text_tuple(value, "optional_roles"),
                prohibited_roles=_required_text_tuple(value, "prohibited_roles"),
                allowed_source_kinds=_required_text_tuple(value, "allowed_source_kinds"),
                allowed_media_types=_required_text_tuple(value, "allowed_media_types"),
                prohibited_extensions=tuple(
                    item.casefold()
                    for item in _required_text_tuple(value, "prohibited_extensions")
                ),
                authority_policy=AuthorityPolicy(
                    owner=_required_text(authority, "owner"),
                    authority_kind=_required_text(authority, "authority_kind"),
                    usage_authority=_required_text(authority, "usage_authority"),
                    license=_required_text(authority, "license"),
                    privacy_class=_required_text(authority, "privacy_class"),
                    consent_policy_required=_required_bool(
                        authority, "consent_policy_required"
                    ),
                ),
                safety_limits=SafetyLimits(
                    max_directory_depth=_required_nonnegative_int(
                        limits, "max_directory_depth"
                    ),
                    max_file_count=_required_positive_int(limits, "max_file_count"),
                    max_total_uncompressed_bytes=_required_positive_int(
                        limits, "max_total_uncompressed_bytes"
                    ),
                    max_single_file_bytes=_required_positive_int(
                        limits, "max_single_file_bytes"
                    ),
                    max_zip_decompression_ratio=_required_positive_int(
                        limits, "max_zip_decompression_ratio"
                    ),
                    max_nested_archive_depth=_required_nonnegative_int(
                        limits, "max_nested_archive_depth"
                    ),
                    reject_symlinks=_required_bool(limits, "reject_symlinks"),
                    reject_casefold_collisions=_required_bool(
                        limits, "reject_casefold_collisions"
                    ),
                    reject_absolute_or_parent_paths=_required_bool(
                        limits, "reject_absolute_or_parent_paths"
                    ),
                    extract_archives=_required_bool(limits, "extract_archives"),
                    network_access=_required_bool(limits, "network_access"),
                ),
                amendment_rule=_required_text(value, "amendment_rule"),
                profile_sha256=digest,
            )
        except (KeyError, TypeError) as error:
            raise SourceProfileInvalid(
                "Source profile is missing a required contract object.",
                missing_field=str(error),
            ) from error
        profile.validate()
        return profile

    def validate(self) -> None:
        if self.target_candidate.source_kind not in self.allowed_source_kinds:
            raise UnsupportedSourceKind(
                "Target candidate kind is not allowed by its source profile.",
                source_kind=self.target_candidate.source_kind,
            )
        if self.target_candidate.role not in self.required_roles:
            raise RequiredRoleMissing(
                "The exact target candidate does not satisfy a required role.",
                role=self.target_candidate.role,
                required_roles=self.required_roles,
            )
        if self.target_candidate.role in self.prohibited_roles:
            raise SourceProfileInvalid(
                "The exact target candidate uses a prohibited role.",
                role=self.target_candidate.role,
            )
        authority_values = (
            self.authority_policy.owner,
            self.authority_policy.authority_kind,
            self.authority_policy.usage_authority,
            self.authority_policy.license,
            self.authority_policy.privacy_class,
        )
        if not all(value.strip() for value in authority_values):
            raise AuthorityMetadataIncomplete(
                "Source authority, license, and privacy metadata are required."
            )
        if self.safety_limits.extract_archives or self.safety_limits.network_access:
            raise SourceProfileInvalid(
                "The bounded Builder Core source profile must disable extraction and network access."
            )


@dataclass(frozen=True, slots=True)
class SourceDescriptor:
    source_id: str
    canonical_uri: str
    relative_path: str
    source_kind: str
    role: str
    precedence: int
    authority: str
    license: str
    privacy_class: str
    media_type: str
    size_bytes: int
    observed_mtime: str | None
    sha256: str
    discovered_from: str

    @property
    def content_id(self) -> str:
        return f"sha256:{self.sha256}"

    def identity_payload(self) -> dict[str, object]:
        return {
            "source_id": self.source_id,
            "canonical_uri": self.canonical_uri,
            "relative_path": self.relative_path,
            "source_kind": self.source_kind,
            "role": self.role,
            "precedence": self.precedence,
            "authority": self.authority,
            "license": self.license,
            "privacy_class": self.privacy_class,
            "media_type": self.media_type,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
            "discovered_from": self.discovered_from,
        }


@dataclass(frozen=True, slots=True)
class SourceLock:
    lock_id: str
    run_id: str
    source_profile_ref: str
    source_profile_hash: str
    target_profile_ref: str
    target_candidate_ref: str
    ordered_descriptors: tuple[SourceDescriptor, ...]
    aggregate_hash: str
    created_at: datetime
    created_by: str
    invalidates_lock_ref: str | None

    @property
    def file_count(self) -> int:
        return len(self.ordered_descriptors)

    @property
    def total_bytes(self) -> int:
        return sum(item.size_bytes for item in self.ordered_descriptors)

    @classmethod
    def create(
        cls,
        *,
        run_id: str,
        profile: SourceProfile,
        descriptors: tuple[SourceDescriptor, ...],
        created_at: datetime,
        created_by: str,
        invalidates_lock_ref: str | None = None,
    ) -> "SourceLock":
        ordered = tuple(
            sorted(
                descriptors,
                key=lambda item: (item.precedence, item.canonical_uri, item.sha256),
            )
        )
        if not ordered:
            raise RequiredRoleMissing("A Source Lock requires at least one descriptor.")
        covered = {item.role for item in ordered}
        missing = tuple(sorted(set(profile.required_roles) - covered))
        if missing:
            raise RequiredRoleMissing(
                "The diagnosed workspace does not cover every required role.",
                missing_roles=missing,
            )
        identity = {
            "run_id": run_id,
            "source_profile_ref": profile.ref,
            "source_profile_hash": profile.profile_sha256,
            "target_profile_ref": profile.target_profile_ref,
            "target_candidate_ref": profile.target_candidate.uri,
            "ordered_descriptors": [item.identity_payload() for item in ordered],
            "invalidates_lock_ref": invalidates_lock_ref,
        }
        aggregate = sha256(_canonical_json(identity)).hexdigest()
        return cls(
            lock_id=f"source-lock_{aggregate}",
            run_id=run_id,
            source_profile_ref=profile.ref,
            source_profile_hash=profile.profile_sha256,
            target_profile_ref=profile.target_profile_ref,
            target_candidate_ref=profile.target_candidate.uri,
            ordered_descriptors=ordered,
            aggregate_hash=f"sha256:{aggregate}",
            created_at=created_at,
            created_by=created_by,
            invalidates_lock_ref=invalidates_lock_ref,
        )


@dataclass(frozen=True, slots=True)
class WorkspaceDiagnostic:
    code: str
    outcome: str
    message: str
    context: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class EvidenceWorkspaceReceipt:
    receipt_id: str
    command_id: str
    run_id: str
    source_lock_ref: str
    source_profile_ref: str
    authority_identity: str
    event_ids: tuple[str, ...]
    diagnostics: tuple[WorkspaceDiagnostic, ...]
    outcome: str
    receipt_hash: str

    @classmethod
    def create(
        cls,
        *,
        receipt_id: str,
        command_id: str,
        run_id: str,
        source_lock_ref: str,
        source_profile_ref: str,
        authority_identity: str,
        event_ids: tuple[str, ...],
        diagnostics: tuple[WorkspaceDiagnostic, ...],
        outcome: str,
    ) -> "EvidenceWorkspaceReceipt":
        payload = {
            "receipt_id": receipt_id,
            "command_id": command_id,
            "run_id": run_id,
            "source_lock_ref": source_lock_ref,
            "source_profile_ref": source_profile_ref,
            "authority_identity": authority_identity,
            "event_ids": event_ids,
            "diagnostics": tuple(
                (item.code, item.outcome, item.message, item.context)
                for item in diagnostics
            ),
            "outcome": outcome,
        }
        digest = sha256(_canonical_json(payload)).hexdigest()
        return cls(
            receipt_id=receipt_id,
            command_id=command_id,
            run_id=run_id,
            source_lock_ref=source_lock_ref,
            source_profile_ref=source_profile_ref,
            authority_identity=authority_identity,
            event_ids=event_ids,
            diagnostics=diagnostics,
            outcome=outcome,
            receipt_hash=f"sha256:{digest}",
        )


def stable_source_id(*, canonical_uri: str, role: str, content_hash: str) -> str:
    value = f"{canonical_uri}\n{role}\n{content_hash}".encode("utf-8")
    return f"source_{sha256(value).hexdigest()}"


def deterministic_tree_hash(items: tuple[tuple[str, str], ...]) -> str:
    return sha256(_canonical_json(tuple(sorted(items)))).hexdigest()


def _required_text(value: Mapping[str, object], field: str) -> str:
    item = value[field]
    if not isinstance(item, str) or not item.strip():
        raise SourceProfileInvalid("Required source-profile text is absent.", field=field)
    return item


def _required_hash(value: Mapping[str, object], field: str) -> str:
    item = _required_text(value, field)
    if len(item) != 64 or any(character not in "0123456789abcdef" for character in item):
        raise SourceProfileInvalid("A raw lowercase SHA-256 value is required.", field=field)
    return item


def _required_bool(value: Mapping[str, object], field: str) -> bool:
    item = value[field]
    if not isinstance(item, bool):
        raise SourceProfileInvalid("Required source-profile boolean is absent.", field=field)
    return item


def _required_text_tuple(value: Mapping[str, object], field: str) -> tuple[str, ...]:
    item = value[field]
    if not isinstance(item, list) or any(
        not isinstance(member, str) or not member.strip() for member in item
    ):
        raise SourceProfileInvalid("A source-profile string list is required.", field=field)
    return tuple(item)


def _required_positive_int(value: Mapping[str, object], field: str) -> int:
    item = value[field]
    if not isinstance(item, int) or isinstance(item, bool) or item <= 0:
        raise SourceProfileInvalid("A positive source-profile integer is required.", field=field)
    return item


def _required_nonnegative_int(value: Mapping[str, object], field: str) -> int:
    item = value[field]
    if not isinstance(item, int) or isinstance(item, bool) or item < 0:
        raise SourceProfileInvalid(
            "A non-negative source-profile integer is required.", field=field
        )
    return item


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
