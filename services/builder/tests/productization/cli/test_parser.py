from __future__ import annotations

import unittest
from pathlib import Path

from cmf_builder.cli.parser import CLIUsageError, parse_cli_args


class ProductizationCLIParserTests(unittest.TestCase):
    def test_parses_all_frozen_commands_into_exact_request_fields(self) -> None:
        cases = (
            (
                ("ingest", "operator-task.json"),
                ("ingest", Path("operator-task.json"), None, None, "human"),
            ),
            (
                ("--format", "json", "build", "--artifact-id", "manifest_123"),
                ("build", None, None, "manifest_123", "json"),
            ),
            (
                ("inspect", "--artifact-id", "definition_123"),
                ("inspect", None, None, "definition_123", "human"),
            ),
            (
                (
                    "export",
                    "--artifact-id",
                    "definition_123",
                    "--output",
                    "dist/harness.zip",
                ),
                (
                    "export",
                    None,
                    Path("dist/harness.zip"),
                    "definition_123",
                    "human",
                ),
            ),
        )
        for argv, expected in cases:
            with self.subTest(command=argv[0]):
                parsed = parse_cli_args(argv)
                self.assertEqual(
                    (
                        parsed.command,
                        parsed.manifest_path,
                        parsed.output_path,
                        parsed.artifact_id,
                        parsed.output_format,
                    ),
                    expected,
                )

    def test_rejects_unknown_or_incomplete_commands_without_abbreviation(self) -> None:
        invalid = (
            (),
            ("ing", "operator-task.json"),
            ("ingest",),
            ("build",),
            ("build", "--artifact-id", "   "),
            ("inspect",),
            ("export", "--artifact-id", "definition_123"),
        )
        for argv in invalid:
            with self.subTest(argv=argv), self.assertRaises(CLIUsageError):
                parse_cli_args(argv)
