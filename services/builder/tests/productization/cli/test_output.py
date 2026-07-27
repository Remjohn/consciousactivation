from __future__ import annotations

import io
import unittest
from pathlib import Path

from cmf_builder.application.productization_contracts import ProductizationCommandResult
from cmf_builder.cli.commands import run_cli
from cmf_builder.cli.output import canonical_json, render_result


FIXTURE_ROOT = Path(__file__).parents[2] / "fixtures" / "productization" / "cli"


class FixedService:
    def __init__(self, result: ProductizationCommandResult) -> None:
        self.result = result

    def execute(self, request: object) -> ProductizationCommandResult:
        return self.result


class ProductizationCLIOutputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = ProductizationCommandResult(
            command="inspect",
            status="PASS",
            artifact_id="definition_123",
            artifact_hash="sha256:abc123",
            receipt_id="receipt_123",
            payload={
                "production_ready": False,
                "mode": "generic",
                "sections": ("input", "output"),
            },
        )

    def test_json_output_is_sorted_compact_utf8_and_terminal_lf(self) -> None:
        observed = render_result(self.result, output_format="json")
        expected = (FIXTURE_ROOT / "inspect_result.json.txt").read_text(
            encoding="utf-8"
        )
        self.assertEqual(observed, expected)
        self.assertTrue(observed.endswith("\n"))
        self.assertNotIn(": ", observed)
        self.assertEqual(canonical_json({"é": "✓"}), '{"é":"✓"}\n')

    def test_human_output_has_fixed_field_and_sorted_payload_order(self) -> None:
        observed = render_result(self.result, output_format="human")
        expected = (FIXTURE_ROOT / "inspect_result.human.txt").read_text(
            encoding="utf-8"
        )
        self.assertEqual(observed, expected)

    def test_fresh_invocations_are_byte_identical(self) -> None:
        first_out, second_out = io.StringIO(), io.StringIO()
        first_err, second_err = io.StringIO(), io.StringIO()
        service = FixedService(self.result)
        argv = (
            "--format",
            "json",
            "inspect",
            "--artifact-id",
            "definition_123",
        )
        self.assertEqual(run_cli(service, argv, stdout=first_out, stderr=first_err), 0)
        self.assertEqual(run_cli(service, argv, stdout=second_out, stderr=second_err), 0)
        self.assertEqual(first_out.getvalue().encode(), second_out.getvalue().encode())
        self.assertEqual(first_err.getvalue(), second_err.getvalue())
