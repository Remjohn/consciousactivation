from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

from cmf_builder.adapters.file_evidence_workspace import FileEvidenceWorkspace
from tests.stories.st_01_02 import source_profile_for


def _archive_bytes(path: Path, member: str, content: str) -> bytes:
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr(member, content)
    return path.read_bytes()


class SwappingWorkspace(FileEvidenceWorkspace):
    def __init__(self, root: Path, replacement: bytes) -> None:
        super().__init__(root)
        self._replacement = replacement
        self._swapped = False

    def _read_unchanged(self, path: Path) -> bytes:
        original = super()._read_unchanged(path)
        if path.suffix == ".zip" and not self._swapped:
            self._swapped = True
            path.write_bytes(self._replacement)
        return original


def test_zip_hash_and_members_derive_from_one_immutable_buffer() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        candidate = root / "candidate.zip"
        original = _archive_bytes(candidate, "first.txt", "archive-a")
        replacement_path = root / "replacement.zip"
        replacement = _archive_bytes(replacement_path, "second.txt", "archive-b")
        replacement_path.unlink()
        profile = source_profile_for(
            root,
            "candidate.zip",
            "zip",
            expected_hash=sha256(original).hexdigest(),
        )
        workspace = SwappingWorkspace(root, replacement)

        scan = workspace.diagnose(profile)

        assert scan.candidate_sha256 == sha256(original).hexdigest()
        assert tuple(item.relative_path for item in scan.descriptors) == ("first.txt",)
        assert scan.descriptors[0].sha256 == sha256(b"archive-a").hexdigest()
        assert candidate.read_bytes() == replacement
