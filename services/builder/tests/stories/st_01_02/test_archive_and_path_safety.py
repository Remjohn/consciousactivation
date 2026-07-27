from __future__ import annotations

from dataclasses import replace
from hashlib import sha256
from pathlib import Path
import stat
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from cmf_builder.adapters.file_evidence_workspace import FileEvidenceWorkspace
from cmf_builder.domain.evidence_workspace import (
    ArchiveSafetyRejected,
    ResourceLimitExceeded,
    SourceHashMismatch,
    SourcePathRejected,
    UnsupportedMediaType,
    UnsupportedSourceKind,
)
from tests.stories.st_01_02 import source_profile_for


class ArchiveAndPathSafetyTests(unittest.TestCase):
    def test_ac_03_missing_traversal_wrong_hash_and_kind_fail_typed(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "task.txt"
            source.write_text("synthetic", encoding="utf-8")
            profile = source_profile_for(root, "task.txt", "file")
            workspace = FileEvidenceWorkspace(root)
            cases = (
                (
                    SourcePathRejected,
                    replace(
                        profile,
                        target_candidate=replace(
                            profile.target_candidate, uri="repo://missing.txt"
                        ),
                    ),
                ),
                (
                    SourcePathRejected,
                    replace(
                        profile,
                        target_candidate=replace(
                            profile.target_candidate, uri="repo://../outside.txt"
                        ),
                    ),
                ),
                (
                    SourceHashMismatch,
                    replace(
                        profile,
                        target_candidate=replace(
                            profile.target_candidate, sha256="0" * 64
                        ),
                    ),
                ),
                (
                    UnsupportedSourceKind,
                    replace(
                        profile,
                        target_candidate=replace(
                            profile.target_candidate, source_kind="directory"
                        ),
                    ),
                ),
            )
            for expected, candidate in cases:
                with self.subTest(expected=expected.__name__):
                    with self.assertRaises(expected):
                        workspace.diagnose(candidate)

    def test_ac_05_zip_path_link_collision_executable_and_nested_archive_rejections(self) -> None:
        cases: tuple[tuple[str, tuple[tuple[object, bytes], ...]], ...] = (
            ("traversal", (("../evil.txt", b"x"),)),
            ("absolute", (("/evil.txt", b"x"),)),
            ("backslash", ((r"..\evil.txt", b"x"),)),
            ("casefold", (("A.txt", b"x"), ("a.txt", b"y"))),
            ("executable", (("evil.exe", b"x"),)),
            ("nested", (("inner.zip", b"not-used"),)),
        )
        for name, members in cases:
            with self.subTest(case=name), TemporaryDirectory() as directory:
                root = Path(directory)
                archive = root / "unsafe.zip"
                with ZipFile(archive, "w") as bundle:
                    for member, content in members:
                        bundle.writestr(member, content)
                profile = source_profile_for(root, "unsafe.zip", "zip")
                with self.assertRaises(ArchiveSafetyRejected):
                    FileEvidenceWorkspace(root).diagnose(profile)

        with TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "symlink.zip"
            link = ZipInfo("link.txt")
            link.create_system = 3
            link.external_attr = (stat.S_IFLNK | 0o777) << 16
            with ZipFile(archive, "w") as bundle:
                bundle.writestr(link, "target.txt")
            profile = source_profile_for(root, "symlink.zip", "zip")
            with self.assertRaises(ArchiveSafetyRejected):
                FileEvidenceWorkspace(root).diagnose(profile)

    def test_ac_05_resource_limits_cover_size_count_depth_and_ratio(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "large.txt").write_text("12345", encoding="utf-8")
            profile = source_profile_for(
                root,
                "large.txt",
                "file",
                limit_changes={"max_single_file_bytes": 4},
            )
            with self.assertRaises(ResourceLimitExceeded):
                FileEvidenceWorkspace(root).diagnose(profile)

        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "many"
            source.mkdir()
            (source / "a.txt").write_text("a", encoding="utf-8")
            (source / "b.txt").write_text("b", encoding="utf-8")
            profile = source_profile_for(
                root, "many", "directory", limit_changes={"max_file_count": 1}
            )
            with self.assertRaises(ResourceLimitExceeded):
                FileEvidenceWorkspace(root).diagnose(profile)

        with TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "nested/a"
            nested.mkdir(parents=True)
            (nested / "task.txt").write_text("a", encoding="utf-8")
            profile = source_profile_for(
                root, "nested", "directory", limit_changes={"max_directory_depth": 0}
            )
            with self.assertRaises(ResourceLimitExceeded):
                FileEvidenceWorkspace(root).diagnose(profile)

        with TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "ratio.zip"
            with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
                bundle.writestr("large.txt", "0" * 5000)
            profile = source_profile_for(
                root,
                "ratio.zip",
                "zip",
                limit_changes={"max_zip_decompression_ratio": 2},
            )
            with self.assertRaises(ResourceLimitExceeded):
                FileEvidenceWorkspace(root).diagnose(profile)

    def test_ac_05_malformed_zip_is_rejected_without_extraction_or_mutation(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "malformed.zip"
            archive.write_bytes(b"not a zip")
            profile = source_profile_for(root, "malformed.zip", "zip")
            before = (
                sha256(archive.read_bytes()).hexdigest(),
                archive.stat().st_mtime_ns,
                {item.name for item in root.iterdir()},
            )
            with self.assertRaises(ArchiveSafetyRejected):
                FileEvidenceWorkspace(root).diagnose(profile)
            after = (
                sha256(archive.read_bytes()).hexdigest(),
                archive.stat().st_mtime_ns,
                {item.name for item in root.iterdir()},
            )
            self.assertEqual(before, after)

    def test_ac_03_05_executable_and_unknown_media_fail_closed(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            executable = root / "script.exe"
            executable.write_bytes(b"MZ")
            executable_profile = source_profile_for(root, "script.exe", "file")
            with self.assertRaises(SourcePathRejected):
                FileEvidenceWorkspace(root).diagnose(executable_profile)

            unknown = root / "task.bin"
            unknown.write_bytes(b"synthetic")
            unknown_profile = source_profile_for(root, "task.bin", "file")
            with self.assertRaises(UnsupportedMediaType):
                FileEvidenceWorkspace(root).diagnose(unknown_profile)


if __name__ == "__main__":
    unittest.main()
