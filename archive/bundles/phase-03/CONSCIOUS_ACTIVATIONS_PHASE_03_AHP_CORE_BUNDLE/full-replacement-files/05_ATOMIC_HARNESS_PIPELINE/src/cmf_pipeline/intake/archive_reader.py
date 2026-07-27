from __future__ import annotations

import stat
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from ca_contracts import bytes_sha256

from ..domain.errors import PipelineValidationError


@dataclass(frozen=True, slots=True)
class ArchiveMember:
    path: str
    byte_length: int
    sha256: str
    content: bytes


class PortableHarnessPackageReader:
    def __init__(self, *, max_members: int = 128, max_member_bytes: int = 8 * 1024 * 1024, max_total_bytes: int = 32 * 1024 * 1024):
        self.max_members = max_members
        self.max_member_bytes = max_member_bytes
        self.max_total_bytes = max_total_bytes

    def read(self, path: str | Path) -> tuple[str, tuple[ArchiveMember, ...]]:
        archive_path = Path(path)
        if not archive_path.is_file():
            raise PipelineValidationError(f"harness package not found: {archive_path}")
        package_bytes = archive_path.read_bytes()
        package_sha = bytes_sha256(package_bytes)
        members: list[ArchiveMember] = []
        seen: set[str] = set()
        total = 0
        try:
            with zipfile.ZipFile(archive_path) as archive:
                infos = archive.infolist()
                if len(infos) > self.max_members:
                    raise PipelineValidationError("harness package has too many members")
                for info in infos:
                    if info.is_dir():
                        continue
                    raw = info.filename.replace("\\", "/")
                    pure = PurePosixPath(raw)
                    if raw.startswith("/") or ".." in pure.parts or any(part in {"", "."} for part in pure.parts):
                        raise PipelineValidationError(f"unsafe harness member path: {raw}")
                    if raw in seen:
                        raise PipelineValidationError(f"duplicate harness member: {raw}")
                    seen.add(raw)
                    mode = info.external_attr >> 16
                    if mode and stat.S_ISLNK(mode):
                        raise PipelineValidationError(f"symbolic-link member is forbidden: {raw}")
                    if info.file_size > self.max_member_bytes:
                        raise PipelineValidationError(f"harness member exceeds size limit: {raw}")
                    total += info.file_size
                    if total > self.max_total_bytes:
                        raise PipelineValidationError("harness package exceeds total uncompressed size limit")
                    content = archive.read(info)
                    if len(content) != info.file_size:
                        raise PipelineValidationError(f"harness member byte count mismatch: {raw}")
                    members.append(ArchiveMember(raw, len(content), bytes_sha256(content), content))
        except zipfile.BadZipFile as exc:
            raise PipelineValidationError("invalid harness ZIP package") from exc
        return package_sha, tuple(sorted(members, key=lambda item: item.path))
