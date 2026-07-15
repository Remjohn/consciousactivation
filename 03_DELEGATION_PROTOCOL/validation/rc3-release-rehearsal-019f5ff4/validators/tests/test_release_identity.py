from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from cmf_delegation_validators.paths import LAYOUT, ROOT
from cmf_delegation_validators.release_identity import (
    EXPECTED_COMPATIBILITY_PROFILE_VERSION,
    EXPECTED_PACKAGE_VERSION,
    EXPECTED_PROTOCOL_VERSION,
    EXPECTED_VISUAL_ASSET_DEMAND_VERSION,
    scan_stale_package_declarations,
    validate_release_identity,
)


RC2_SEMANTIC_BOUNDARY_HASHES = {
    "contracts/examples/visual-asset-demand.example.json": "930e93d11bb511790135f669df082b1c003d4205ffa114a92cb5b74f3ff973ad",
    "contracts/schemas/visual-asset-demand.schema.json": "d23cdfd520538adc0d7769e7fefa9a9cf8af63880446efd8a8c95d5dbfb67c5e",
    "compatibility/migrations/visual-asset-demand-v1-to-v1.1.json": "3d1cdf7e1f5c2fd2b68acf0c30215e5311c8a6d9cd2375eec49c78e8cbb62e58",
    "compatibility/migrations/visual-asset-demand-v1.1-source-kind-classification.json": "92a61deae4ecfd915385d8e72d7b2d27e038ca3f7e230fffd9d9c2791cad073b",
    "fixtures/format02/scenarios/SCN-01.json": "cd295fcc3fd31f452354f9e82d2f24ab32c06e765f2a3a3e4a670972d1f6600d",
    "fixtures/format02/scenarios/SCN-02.json": "aa23d30a60fe7a6c978e0f4fb5d8f6a376b15d0c869bd301c327093006915e39",
    "fixtures/format02/scenarios/SCN-03.json": "84f7621bc61d9171da2ff3984fd2a1b0965d3ba72061151cddce3cb47d818242",
    "fixtures/format02/scenarios/SCN-04.json": "36fd326a5f9167af6143ef75c88867c925e4be5a6e0c475b16f889b9feae498f",
    "fixtures/format02/scenarios/SCN-05.json": "0e2ac3775f53fe6119549eab8b57ebedbd158afa047c860eeb228d3be7958de7",
    "fixtures/format02/scenarios/SCN-06.json": "6055c5f7620397b034a5ee2e090c49422cc5b789562bd308bd0b2dc255fe05cb",
    "fixtures/format02/scenarios/SCN-07.json": "c19ef17a74a2c243defec9106546aed50eb722cbaa6f9f83a43dc59e3139e4de",
    "fixtures/format02/scenarios/SCN-08.json": "9c2c28b2ea5b3a7fbdb4b840fede51c2edb1a21e922bce52f7ed20e61762c9fa",
    "fixtures/format02/scenarios/SCN-10.json": "0ac77c34e2dd50a96b45b35e20c37eeb5db4e53c63285bb563a15322e064140c",
}


class ReleaseIdentityTests(unittest.TestCase):
    def test_all_current_package_declarations_resolve_to_rc3(self) -> None:
        report = validate_release_identity()
        self.assertEqual(report["package_version"], EXPECTED_PACKAGE_VERSION)
        self.assertEqual(report["stale_active_declarations"], 0)

    def test_active_rc1_and_rc2_package_declarations_are_rejected(self) -> None:
        for candidate in (1, 2):
            with self.subTest(candidate=candidate), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                (root / "active.json").write_text(
                    json.dumps({"package_version": f"1.1.0-rc.{candidate}"}),
                    encoding="utf-8",
                )
                self.assertTrue(scan_stale_package_declarations(root))

    def test_explicit_historical_rejection_evidence_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "RC2_CONVERGENCE_REJECTION_REPORT.md").write_text(
                "historical_evidence: true\nRejected: " + "1.1.0" + "-rc.2\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_stale_package_declarations(root), [])

    def test_schema_protocol_and_package_versions_are_intentionally_distinct(self) -> None:
        registry = json.loads((ROOT / "contracts/registry.json").read_text(encoding="utf-8"))
        profile = json.loads((ROOT / "compatibility/profile.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["package_version"], EXPECTED_PACKAGE_VERSION)
        self.assertEqual(registry["protocol_version"], EXPECTED_PROTOCOL_VERSION)
        demand = next(item for item in registry["messages"] if item["message_type"] == "visual-asset-demand")
        self.assertEqual(demand["message_version"], EXPECTED_VISUAL_ASSET_DEMAND_VERSION)
        self.assertEqual(profile["profile_version"], EXPECTED_COMPATIBILITY_PROFILE_VERSION)
        self.assertNotEqual(EXPECTED_PACKAGE_VERSION, EXPECTED_PROTOCOL_VERSION)

    def test_rc2_vae_boundary_contracts_and_fixtures_are_byte_preserved(self) -> None:
        for relative, expected in RC2_SEMANTIC_BOUNDARY_HASHES.items():
            with self.subTest(path=relative):
                actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
                self.assertEqual(actual, expected)

    def test_scn09_changes_only_the_compatibility_manifest_identity_hash(self) -> None:
        scenario = json.loads(
            (ROOT / "fixtures/format02/scenarios/SCN-09.json").read_text(encoding="utf-8")
        )
        for message in scenario["message_sequence"]:
            if message["message_type"] == "compatibility-manifest":
                message["fixture_hash"] = "PACKAGE_IDENTITY_DEPENDENT"
        normalized = json.dumps(
            scenario,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        self.assertEqual(
            hashlib.sha256(normalized).hexdigest(),
            "a8e71962b32b679d54b5aec47e09b6424d88000c17f12447bc137800db3af090",
        )

    def test_migration_targets_remain_visual_asset_demand_v1_1(self) -> None:
        for relative in (
            "compatibility/migrations/visual-asset-demand-v1-to-v1.1.json",
            "compatibility/migrations/visual-asset-demand-v1.1-source-kind-classification.json",
        ):
            migration = json.loads((ROOT / relative).read_text(encoding="utf-8"))
            self.assertEqual(migration["target"], "visual-asset-demand@1.1")

    def test_release_layout_receipt_identity_is_checked_in_clean_room(self) -> None:
        if LAYOUT == "RELEASE":
            report = validate_release_identity()
            self.assertGreater(report["utf8_files_scanned"], 100)


if __name__ == "__main__":
    unittest.main()
