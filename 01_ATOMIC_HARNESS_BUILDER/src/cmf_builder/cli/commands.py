from __future__ import annotations

import sys
from typing import Sequence, TextIO

from cmf_builder.application.productization_contracts import (
    ProductizationApplicationService,
    ProductizationCommandRequest,
    ProductizationError,
)
from cmf_builder.cli.exit_codes import CLIExitCode, exit_code_for_error
from cmf_builder.cli.output import (
    render_internal_error,
    render_productization_error,
    render_result,
    render_usage_error,
)
from cmf_builder.cli.parser import CLIUsageError, ParsedCLICommand, parse_cli_args


def run_cli(
    service: ProductizationApplicationService,
    argv: Sequence[str],
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    output = stdout or sys.stdout
    errors = stderr or sys.stderr
    requested_format = _requested_output_format(argv)
    try:
        parsed = parse_cli_args(argv)
    except CLIUsageError as error:
        errors.write(render_usage_error(str(error), output_format=requested_format))
        return int(CLIExitCode.USAGE)

    try:
        result = service.execute(to_request(parsed))
        output.write(render_result(result, output_format=parsed.output_format))
        return int(CLIExitCode.SUCCESS)
    except ProductizationError as error:
        errors.write(
            render_productization_error(error, output_format=parsed.output_format)
        )
        return int(exit_code_for_error(error.code))
    except Exception:
        errors.write(render_internal_error(output_format=parsed.output_format))
        return int(CLIExitCode.INTERNAL_ERROR)


def to_request(parsed: ParsedCLICommand) -> ProductizationCommandRequest:
    return ProductizationCommandRequest(
        command=parsed.command,
        manifest_path=parsed.manifest_path,
        output_path=parsed.output_path,
        artifact_id=parsed.artifact_id,
    )


def _requested_output_format(argv: Sequence[str]) -> str:
    values = tuple(argv)
    for index, value in enumerate(values[:-1]):
        if value == "--format" and values[index + 1] in {"human", "json"}:
            return values[index + 1]
    return "human"


def main(
    service: ProductizationApplicationService,
    argv: Sequence[str] | None = None,
) -> int:
    return run_cli(service, tuple(argv) if argv is not None else tuple(sys.argv[1:]))
