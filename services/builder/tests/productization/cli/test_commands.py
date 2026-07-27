from __future__ import annotations

import io
import unittest
from pathlib import Path

from cmf_builder.application.productization_contracts import (
    ProductizationCommandRequest,
    ProductizationCommandResult,
    ProductizationError,
    ProductizationErrorCode,
)
from cmf_builder.cli.commands import run_cli
from cmf_builder.cli.exit_codes import CLIExitCode


class RecordingService:
    def __init__(
        self,
        *,
        result: ProductizationCommandResult | None = None,
        error: Exception | None = None,
    ) -> None:
        self.result = result or _result()
        self.error = error
        self.requests: list[ProductizationCommandRequest] = []

    def execute(self, request: ProductizationCommandRequest) -> ProductizationCommandResult:
        self.requests.append(request)
        if self.error is not None:
            raise self.error
        return self.result


class ProductizationCLICommandTests(unittest.TestCase):
    def test_dispatches_every_command_to_the_frozen_service_protocol(self) -> None:
        cases = (
            (
                ("ingest", "operator-task.json"),
                ProductizationCommandRequest(
                    command="ingest", manifest_path=Path("operator-task.json")
                ),
            ),
            (
                ("build", "--artifact-id", "manifest_123"),
                ProductizationCommandRequest(
                    command="build", artifact_id="manifest_123"
                ),
            ),
            (
                ("inspect", "--artifact-id", "definition_123"),
                ProductizationCommandRequest(
                    command="inspect", artifact_id="definition_123"
                ),
            ),
            (
                (
                    "export",
                    "--artifact-id",
                    "definition_123",
                    "--output",
                    "dist/harness.zip",
                ),
                ProductizationCommandRequest(
                    command="export",
                    output_path=Path("dist/harness.zip"),
                    artifact_id="definition_123",
                ),
            ),
        )
        for argv, expected in cases:
            with self.subTest(command=argv[0]):
                service = RecordingService()
                stdout, stderr = io.StringIO(), io.StringIO()
                self.assertEqual(
                    run_cli(service, argv, stdout=stdout, stderr=stderr),
                    CLIExitCode.SUCCESS,
                )
                self.assertEqual(service.requests, [expected])
                self.assertEqual(stderr.getvalue(), "")

    def test_parser_failure_does_not_call_service(self) -> None:
        service = RecordingService()
        stdout, stderr = io.StringIO(), io.StringIO()
        code = run_cli(service, ("build",), stdout=stdout, stderr=stderr)
        self.assertEqual(code, CLIExitCode.USAGE)
        self.assertEqual(service.requests, [])
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn('error_code: "CLI_USAGE"', stderr.getvalue())

    def test_unexpected_failure_is_redacted_and_maps_to_internal_error(self) -> None:
        service = RecordingService(error=RuntimeError("secret internal detail"))
        stdout, stderr = io.StringIO(), io.StringIO()
        code = run_cli(
            service,
            ("--format", "json", "inspect", "--artifact-id", "definition_123"),
            stdout=stdout,
            stderr=stderr,
        )
        self.assertEqual(code, CLIExitCode.INTERNAL_ERROR)
        self.assertEqual(stdout.getvalue(), "")
        self.assertNotIn("secret internal detail", stderr.getvalue())
        self.assertIn('"code":"INTERNAL_ERROR"', stderr.getvalue())

    def test_frozen_error_taxonomy_has_deterministic_exit_codes(self) -> None:
        expected = {
            ProductizationErrorCode.INVALID_MANIFEST: CLIExitCode.USAGE,
            ProductizationErrorCode.INVALID_ACTIVATIVE_INPUT: CLIExitCode.USAGE,
            ProductizationErrorCode.AUTHORITY_REJECTED: CLIExitCode.AUTHORITY_REJECTED,
            ProductizationErrorCode.HASH_MISMATCH: CLIExitCode.INTEGRITY_ERROR,
            ProductizationErrorCode.NOT_FOUND: CLIExitCode.NOT_FOUND,
            ProductizationErrorCode.CONFLICT: CLIExitCode.CONFLICT,
            ProductizationErrorCode.STORAGE_INTEGRITY: CLIExitCode.INTEGRITY_ERROR,
            ProductizationErrorCode.EXPORT_REJECTED: CLIExitCode.EXPORT_REJECTED,
            ProductizationErrorCode.INTERNAL_ERROR: CLIExitCode.INTERNAL_ERROR,
        }
        for error_code, exit_code in expected.items():
            with self.subTest(error_code=error_code):
                service = RecordingService(
                    error=ProductizationError(
                        error_code,
                        "governed failure",
                        field_path="manifest.task",
                        context={"z": 2, "a": 1},
                    )
                )
                stdout, stderr = io.StringIO(), io.StringIO()
                observed = run_cli(
                    service,
                    (
                        "--format",
                        "json",
                        "inspect",
                        "--artifact-id",
                        "definition_123",
                    ),
                    stdout=stdout,
                    stderr=stderr,
                )
                self.assertEqual(observed, exit_code)
                self.assertEqual(stdout.getvalue(), "")
                self.assertTrue(stderr.getvalue().endswith("\n"))


def _result() -> ProductizationCommandResult:
    return ProductizationCommandResult(
        command="inspect",
        status="PASS",
        artifact_id="definition_123",
        artifact_hash="sha256:abc123",
        receipt_id="receipt_123",
        payload={"mode": "generic", "production_ready": False},
    )
