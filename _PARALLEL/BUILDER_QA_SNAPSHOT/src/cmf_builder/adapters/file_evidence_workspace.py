from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import os
from pathlib import Path, PurePosixPath
import stat
from zipfile import BadZipFile, ZipFile, ZipInfo

from cmf_builder.domain.evidence_workspace import (
    ArchiveSafetyRejected,
    EvidenceWorkspaceError,
    ResourceLimitExceeded,
    SourceDescriptor,
    SourceHashMismatch,
    SourceLock,
    SourceMutationDetected,
    SourcePathRejected,
    SourceProfile,
    UnsupportedMediaType,
    UnsupportedSourceKind,
    WorkspaceDiagnostic,
    deterministic_tree_hash,
    stable_source_id,
)


_MEDIA_TYPES = {
    ".json": "application/json",
    ".md": "text/plain",
    ".txt": "text/plain",
    ".yaml": "application/yaml",
    ".yml": "application/yaml",
    ".zip": "application/zip",
}


@dataclass(frozen=True, slots=True)
class WorkspaceScan:
    descriptors: tuple[SourceDescriptor, ...]
    candidate_sha256: str
    diagnostics: tuple[WorkspaceDiagnostic, ...]
    archive_count: int


class FileEvidenceWorkspace:
    """Read-only, repository-confined evidence inspection for ST-01.02."""

    def __init__(self, repository_root: Path) -> None:
        self._root = repository_root.resolve(strict=True)

    @property
    def repository_root(self) -> Path:
        return self._root

    def load_profile(self, relative_path: str, expected_sha256: str) -> SourceProfile:
        path = self._resolve_repo_path(relative_path)
        content = self._read_unchanged(path)
        return SourceProfile.from_json_bytes(
            content, observed_sha256=expected_sha256
        )

    def diagnose(self, profile: SourceProfile) -> WorkspaceScan:
        candidate = profile.target_candidate
        path = self._resolve_repo_uri(candidate.uri)
        if not path.exists():
            raise SourcePathRejected(
                "The configured target candidate does not exist.",
                candidate_uri=candidate.uri,
            )
        self._reject_link(path, relative=candidate.uri)
        observed_kind = self._observed_kind(path)
        if observed_kind != candidate.source_kind:
            raise UnsupportedSourceKind(
                "The configured target candidate kind does not match the source profile.",
                configured_kind=candidate.source_kind,
                observed_kind=observed_kind,
            )
        if observed_kind not in profile.allowed_source_kinds:
            raise UnsupportedSourceKind(
                "The configured target candidate kind is not permitted.",
                source_kind=observed_kind,
            )

        if observed_kind == "file":
            content = self._read_unchanged(path)
            self._check_budgets(profile, 1, len(content), len(content))
            candidate_hash = sha256(content).hexdigest()
            self._verify_candidate_hash(profile, candidate_hash)
            descriptors = (
                self._descriptor(
                    profile,
                    canonical_uri=candidate.uri,
                    relative_path=self._repo_relative(path),
                    content=content,
                    source_kind="file",
                    discovered_from="file",
                    observed_mtime=self._mtime(path),
                ),
            )
            archive_count = 0
        elif observed_kind == "directory":
            descriptors, candidate_hash = self._scan_directory(profile, path)
            self._verify_candidate_hash(profile, candidate_hash)
            archive_count = 0
        else:
            archive_bytes = self._read_unchanged(path)
            candidate_hash = sha256(archive_bytes).hexdigest()
            self._verify_candidate_hash(profile, candidate_hash)
            descriptors = self._scan_zip(profile, path)
            archive_count = 1

        diagnostics = (
            WorkspaceDiagnostic(
                code="SourceDiagnosticAccepted",
                outcome="PASS",
                message="Configured evidence workspace is safe and hash-valid.",
                context=(
                    ("candidate_sha256", candidate_hash),
                    ("file_count", str(len(descriptors))),
                    ("total_bytes", str(sum(item.size_bytes for item in descriptors))),
                ),
            ),
        )
        return WorkspaceScan(
            descriptors=tuple(descriptors),
            candidate_sha256=candidate_hash,
            diagnostics=diagnostics,
            archive_count=archive_count,
        )

    def create_lock(
        self,
        *,
        run_id: str,
        profile: SourceProfile,
        created_at: datetime,
        created_by: str,
        invalidates_lock_ref: str | None = None,
    ) -> tuple[SourceLock, WorkspaceScan]:
        scan = self.diagnose(profile)
        lock = SourceLock.create(
            run_id=run_id,
            profile=profile,
            descriptors=scan.descriptors,
            created_at=created_at,
            created_by=created_by,
            invalidates_lock_ref=invalidates_lock_ref,
        )
        return lock, scan

    def _scan_directory(
        self, profile: SourceProfile, directory: Path
    ) -> tuple[tuple[SourceDescriptor, ...], str]:
        descriptors: list[SourceDescriptor] = []
        identities: list[tuple[str, str]] = []
        seen_casefold: dict[str, str] = {}
        total_bytes = 0

        def visit(current: Path, depth: int) -> None:
            nonlocal total_bytes
            if depth > profile.safety_limits.max_directory_depth:
                raise ResourceLimitExceeded(
                    "Directory recursion depth exceeds the source profile.",
                    depth=depth,
                    maximum=profile.safety_limits.max_directory_depth,
                )
            try:
                entries = sorted(
                    os.scandir(current), key=lambda item: (item.name.casefold(), item.name)
                )
            except OSError as error:
                raise SourcePathRejected(
                    "A configured directory cannot be inspected.",
                    path=self._repo_relative(current),
                ) from error
            for entry in entries:
                path = Path(entry.path)
                relative = path.relative_to(directory).as_posix()
                self._reject_dir_entry_link(entry, relative=relative)
                folded = relative.casefold()
                if (
                    profile.safety_limits.reject_casefold_collisions
                    and folded in seen_casefold
                    and seen_casefold[folded] != relative
                ):
                    raise SourcePathRejected(
                        "Case-fold-colliding paths are prohibited.",
                        first_path=seen_casefold[folded],
                        second_path=relative,
                    )
                seen_casefold[folded] = relative
                if entry.is_dir(follow_symlinks=False):
                    visit(path, depth + 1)
                    continue
                if not entry.is_file(follow_symlinks=False):
                    raise SourcePathRejected(
                        "Only regular files are accepted in a source directory.",
                        path=relative,
                    )
                content = self._read_unchanged(path)
                total_bytes += len(content)
                self._check_budgets(profile, len(descriptors) + 1, len(content), total_bytes)
                digest = sha256(content).hexdigest()
                identities.append((relative, digest))
                base_uri = profile.target_candidate.uri.rstrip("/")
                descriptors.append(
                    self._descriptor(
                        profile,
                        canonical_uri=f"{base_uri}/{relative}",
                        relative_path=relative,
                        content=content,
                        source_kind="file",
                        discovered_from="directory",
                        observed_mtime=self._mtime(path),
                    )
                )

        visit(directory, 0)
        if not descriptors:
            raise SourcePathRejected("An empty directory cannot satisfy a required source role.")
        return tuple(descriptors), deterministic_tree_hash(tuple(identities))

    def _scan_zip(
        self, profile: SourceProfile, archive_path: Path
    ) -> tuple[SourceDescriptor, ...]:
        descriptors: list[SourceDescriptor] = []
        seen_casefold: dict[str, str] = {}
        total_bytes = 0
        try:
            with ZipFile(archive_path, "r") as archive:
                infos = sorted(archive.infolist(), key=lambda item: item.filename)
                for info in infos:
                    if info.is_dir():
                        continue
                    member = self._validate_zip_member(profile, info, seen_casefold)
                    self._check_budgets(
                        profile,
                        len(descriptors) + 1,
                        info.file_size,
                        total_bytes + info.file_size,
                    )
                    ratio = info.file_size / max(info.compress_size, 1)
                    if ratio > profile.safety_limits.max_zip_decompression_ratio:
                        raise ResourceLimitExceeded(
                            "ZIP decompression ratio exceeds the source profile.",
                            member=member,
                            ratio=ratio,
                            maximum=profile.safety_limits.max_zip_decompression_ratio,
                        )
                    try:
                        content = archive.read(info)
                    except (BadZipFile, RuntimeError, OSError) as error:
                        raise ArchiveSafetyRejected(
                            "ZIP member bytes are malformed or unreadable.", member=member
                        ) from error
                    if len(content) != info.file_size:
                        raise ArchiveSafetyRejected(
                            "ZIP member size does not match its declaration.", member=member
                        )
                    total_bytes += len(content)
                    descriptors.append(
                        self._descriptor(
                            profile,
                            canonical_uri=(
                                f"{profile.target_candidate.uri}#{member}"
                            ),
                            relative_path=member,
                            content=content,
                            source_kind="file",
                            discovered_from="zip",
                            observed_mtime=None,
                        )
                    )
        except EvidenceWorkspaceError:
            raise
        except (BadZipFile, OSError) as error:
            raise ArchiveSafetyRejected(
                "Configured ZIP input is malformed or unreadable.",
                path=profile.target_candidate.uri,
            ) from error
        if not descriptors:
            raise ArchiveSafetyRejected("An empty ZIP cannot satisfy a required source role.")
        return tuple(descriptors)

    def _validate_zip_member(
        self,
        profile: SourceProfile,
        info: ZipInfo,
        seen_casefold: dict[str, str],
    ) -> str:
        name = info.filename
        if "\\" in name:
            raise ArchiveSafetyRejected(
                "ZIP members must use portable forward-slash paths.", member=name
            )
        member = PurePosixPath(name)
        first = member.parts[0] if member.parts else ""
        if (
            not member.parts
            or member.is_absolute()
            or ".." in member.parts
            or (len(first) > 1 and first[1] == ":")
        ):
            raise ArchiveSafetyRejected(
                "Absolute or parent-traversing ZIP members are prohibited.", member=name
            )
        normalized = member.as_posix()
        folded = normalized.casefold()
        if folded in seen_casefold:
            raise ArchiveSafetyRejected(
                "Duplicate or case-fold-colliding ZIP members are prohibited.",
                first_member=seen_casefold[folded],
                second_member=normalized,
            )
        seen_casefold[folded] = normalized
        mode = (info.external_attr >> 16) & 0xFFFF
        if stat.S_IFMT(mode) == stat.S_IFLNK:
            raise ArchiveSafetyRejected(
                "Symbolic links are prohibited in ZIP evidence.", member=normalized
            )
        suffix = PurePosixPath(normalized).suffix.casefold()
        if suffix in profile.prohibited_extensions:
            raise ArchiveSafetyRejected(
                "Executable or script ZIP members are prohibited.", member=normalized
            )
        if suffix == ".zip" and profile.safety_limits.max_nested_archive_depth == 0:
            raise ArchiveSafetyRejected(
                "Nested archives are prohibited by the source profile.", member=normalized
            )
        self._media_type(profile, suffix, path=normalized)
        return normalized

    def _descriptor(
        self,
        profile: SourceProfile,
        *,
        canonical_uri: str,
        relative_path: str,
        content: bytes,
        source_kind: str,
        discovered_from: str,
        observed_mtime: str | None,
    ) -> SourceDescriptor:
        suffix = PurePosixPath(relative_path).suffix.casefold()
        if suffix in profile.prohibited_extensions:
            raise SourcePathRejected(
                "Executable or script source files are prohibited.", path=relative_path
            )
        media_type = self._media_type(profile, suffix, path=relative_path)
        digest = sha256(content).hexdigest()
        return SourceDescriptor(
            source_id=stable_source_id(
                canonical_uri=canonical_uri,
                role=profile.target_candidate.role,
                content_hash=digest,
            ),
            canonical_uri=canonical_uri,
            relative_path=relative_path,
            source_kind=source_kind,
            role=profile.target_candidate.role,
            precedence=profile.target_candidate.precedence,
            authority=profile.authority_policy.usage_authority,
            license=profile.authority_policy.license,
            privacy_class=profile.authority_policy.privacy_class,
            media_type=media_type,
            size_bytes=len(content),
            observed_mtime=observed_mtime,
            sha256=digest,
            discovered_from=discovered_from,
        )

    @staticmethod
    def _verify_candidate_hash(profile: SourceProfile, observed: str) -> None:
        expected = profile.target_candidate.sha256
        if observed != expected:
            raise SourceHashMismatch(
                "Target candidate bytes do not match the governed source profile.",
                candidate_uri=profile.target_candidate.uri,
                expected_sha256=expected,
                observed_sha256=observed,
            )

    @staticmethod
    def _check_budgets(
        profile: SourceProfile, file_count: int, single_size: int, total_size: int
    ) -> None:
        limits = profile.safety_limits
        if file_count > limits.max_file_count:
            raise ResourceLimitExceeded(
                "Source file count exceeds the source profile.",
                observed=file_count,
                maximum=limits.max_file_count,
            )
        if single_size > limits.max_single_file_bytes:
            raise ResourceLimitExceeded(
                "A source file exceeds the single-file budget.",
                observed=single_size,
                maximum=limits.max_single_file_bytes,
            )
        if total_size > limits.max_total_uncompressed_bytes:
            raise ResourceLimitExceeded(
                "Source bytes exceed the aggregate budget.",
                observed=total_size,
                maximum=limits.max_total_uncompressed_bytes,
            )

    @staticmethod
    def _media_type(profile: SourceProfile, suffix: str, *, path: str) -> str:
        media_type = _MEDIA_TYPES.get(suffix)
        if media_type is None or media_type not in profile.allowed_media_types:
            raise UnsupportedMediaType(
                "Source media type is not permitted by the source profile.",
                path=path,
                suffix=suffix,
                media_type=media_type or "unknown",
            )
        return media_type

    @staticmethod
    def _observed_kind(path: Path) -> str:
        if path.is_dir():
            return "directory"
        if path.is_file() and path.suffix.casefold() == ".zip":
            return "zip"
        if path.is_file():
            return "file"
        raise UnsupportedSourceKind(
            "Target candidate is not a supported regular file, directory, or ZIP.",
            path=path.name,
        )

    def _resolve_repo_uri(self, uri: str) -> Path:
        if not uri.startswith("repo://"):
            raise SourcePathRejected(
                "Only portable repo:// source identities are accepted.", uri=uri
            )
        return self._resolve_repo_path(uri.removeprefix("repo://"))

    def _resolve_repo_path(self, relative_path: str) -> Path:
        portable = PurePosixPath(relative_path)
        first = portable.parts[0] if portable.parts else ""
        if (
            not portable.parts
            or portable.is_absolute()
            or ".." in portable.parts
            or (len(first) > 1 and first[1] == ":")
            or "\\" in relative_path
        ):
            raise SourcePathRejected(
                "Configured source path is absolute, non-portable, or escapes its root.",
                path=relative_path,
            )
        candidate = self._root.joinpath(*portable.parts)
        current = self._root
        for part in portable.parts:
            current = current / part
            if current.exists() and current.is_symlink():
                raise SourcePathRejected(
                    "Symbolic links are prohibited in configured source paths.",
                    path=relative_path,
                )
        resolved = candidate.resolve(strict=False)
        if resolved != self._root and self._root not in resolved.parents:
            raise SourcePathRejected(
                "Configured source path escapes the repository root.", path=relative_path
            )
        return candidate

    @staticmethod
    def _reject_link(path: Path, *, relative: str) -> None:
        try:
            metadata = path.lstat()
        except OSError as error:
            raise SourcePathRejected(
                "Configured source metadata cannot be read.", path=relative
            ) from error
        attributes = getattr(metadata, "st_file_attributes", 0)
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        if path.is_symlink() or (reparse and attributes & reparse):
            raise SourcePathRejected(
                "Links and reparse points are prohibited in configured sources.",
                path=relative,
            )

    @staticmethod
    def _reject_dir_entry_link(entry: os.DirEntry[str], *, relative: str) -> None:
        try:
            metadata = entry.stat(follow_symlinks=False)
        except OSError as error:
            raise SourcePathRejected(
                "Source entry metadata cannot be read.", path=relative
            ) from error
        attributes = getattr(metadata, "st_file_attributes", 0)
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        if entry.is_symlink() or (reparse and attributes & reparse):
            raise SourcePathRejected(
                "Links and reparse points are prohibited in source directories.",
                path=relative,
            )

    @staticmethod
    def _read_unchanged(path: Path) -> bytes:
        try:
            before = path.stat()
            content = path.read_bytes()
            after = path.stat()
        except OSError as error:
            raise SourcePathRejected(
                "Configured source bytes cannot be read.", path=path.name
            ) from error
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise SourceMutationDetected(
                "Source bytes or metadata changed during read.", path=path.name
            )
        return content

    def _repo_relative(self, path: Path) -> str:
        return path.resolve(strict=False).relative_to(self._root).as_posix()

    @staticmethod
    def _mtime(path: Path) -> str:
        value = path.stat().st_mtime
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
