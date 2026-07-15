from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZIP_DEFLATED, ZipFile

from cmf_builder.adapters.file_evidence_workspace import FileEvidenceWorkspace
from tests.stories.st_01_01_synthetic_proof import NOW
from tests.stories.st_01_02 import source_profile_for


class SourceIdentityTests(unittest.TestCase):
    def test_ac_04_06_file_identity_and_aggregate_are_deterministic(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "fixtures/task.yaml"
            source.parent.mkdir(parents=True)
            source.write_text("task: normalize\n", encoding="utf-8")
            profile = source_profile_for(root, "fixtures/task.yaml", "file")
            workspace = FileEvidenceWorkspace(root)

            first, _ = workspace.create_lock(
                run_id="run-test", profile=profile, created_at=NOW, created_by="code-1"
            )
            second, _ = workspace.create_lock(
                run_id="run-test", profile=profile, created_at=NOW, created_by="code-1"
            )

            self.assertEqual(first, second)
            descriptor = first.ordered_descriptors[0]
            self.assertEqual(descriptor.sha256, sha256(source.read_bytes()).hexdigest())
            self.assertEqual(descriptor.content_id, f"sha256:{descriptor.sha256}")
            self.assertEqual(descriptor.canonical_uri, "repo://fixtures/task.yaml")
            self.assertNotIn(str(root), descriptor.canonical_uri)

    def test_ac_04_07_directory_preserves_distinct_provenance_for_identical_bytes(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "fixtures"
            source.mkdir()
            (source / "b.txt").write_text("same", encoding="utf-8")
            (source / "a.txt").write_text("same", encoding="utf-8")
            profile = source_profile_for(root, "fixtures", "directory")
            source_lock, _ = FileEvidenceWorkspace(root).create_lock(
                run_id="run-directory",
                profile=profile,
                created_at=NOW,
                created_by="architect-1",
            )

            first, second = source_lock.ordered_descriptors
            self.assertEqual(first.content_id, second.content_id)
            self.assertNotEqual(first.source_id, second.source_id)
            self.assertEqual((first.relative_path, second.relative_path), ("a.txt", "b.txt"))
            self.assertEqual(first.discovered_from, "directory")

    def test_ac_04_06_zip_members_are_hashed_in_place_without_extraction(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "fixtures.zip"
            with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
                bundle.writestr("task.json", '{"task":"normalize"}')
                bundle.writestr("notes.txt", "synthetic")
            entries_before = {item.name for item in root.iterdir()}
            profile = source_profile_for(root, "fixtures.zip", "zip")
            source_lock, scan = FileEvidenceWorkspace(root).create_lock(
                run_id="run-zip",
                profile=profile,
                created_at=NOW,
                created_by="code-1",
            )

            self.assertEqual(scan.archive_count, 1)
            self.assertEqual(source_lock.file_count, 2)
            self.assertEqual(
                {item.relative_path for item in source_lock.ordered_descriptors},
                {"notes.txt", "task.json"},
            )
            self.assertTrue(
                all(item.discovered_from == "zip" for item in source_lock.ordered_descriptors)
            )
            self.assertEqual(entries_before, {item.name for item in root.iterdir()})

    def test_ac_08_new_profile_version_creates_invalidation_without_rewriting_history(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "task.txt"
            source.write_text("version one", encoding="utf-8")
            workspace = FileEvidenceWorkspace(root)
            first_profile = source_profile_for(root, "task.txt", "file", version="1.0.0")
            first, _ = workspace.create_lock(
                run_id="run-versioned",
                profile=first_profile,
                created_at=NOW,
                created_by="architect-1",
            )
            first_hash = first.ordered_descriptors[0].sha256

            source.write_text("version two", encoding="utf-8")
            second_profile = source_profile_for(root, "task.txt", "file", version="1.0.1")
            second, _ = workspace.create_lock(
                run_id="run-versioned",
                profile=second_profile,
                created_at=NOW,
                created_by="architect-1",
                invalidates_lock_ref=first.lock_id,
            )

            self.assertNotEqual(first.lock_id, second.lock_id)
            self.assertEqual(second.invalidates_lock_ref, first.lock_id)
            self.assertEqual(first.ordered_descriptors[0].sha256, first_hash)
            self.assertNotEqual(first_hash, second.ordered_descriptors[0].sha256)


if __name__ == "__main__":
    unittest.main()
