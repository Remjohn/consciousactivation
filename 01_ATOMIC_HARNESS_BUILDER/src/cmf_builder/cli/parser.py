from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


OUTPUT_FORMATS = ("human", "json")
COMMANDS = ("ingest", "build", "inspect", "export")


class CLIUsageError(ValueError):
    """A deterministic parser error that does not terminate the host process."""


class _NonExitingArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise CLIUsageError(message)


@dataclass(frozen=True, slots=True)
class ParsedCLICommand:
    command: str
    output_format: str
    manifest_path: Path | None = None
    output_path: Path | None = None
    artifact_id: str | None = None


def build_parser() -> argparse.ArgumentParser:
    parser = _NonExitingArgumentParser(
        prog="cmf-builder",
        description="Operate the bounded category-neutral Atomic Harness Builder.",
        allow_abbrev=False,
    )
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=OUTPUT_FORMATS,
        default="human",
        help="Render deterministic human text or canonical JSON.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser(
        "ingest",
        help="Validate and durably ingest an operator manifest.",
        allow_abbrev=False,
    )
    ingest.add_argument("manifest_path", type=Path, metavar="MANIFEST")

    build = subparsers.add_parser(
        "build",
        help="Build the artifact identified by a durable ingested-manifest ID.",
        allow_abbrev=False,
    )
    build.add_argument("--artifact-id", required=True, type=_artifact_id)

    inspect = subparsers.add_parser(
        "inspect",
        help="Inspect one governed Builder artifact.",
        allow_abbrev=False,
    )
    inspect.add_argument("--artifact-id", required=True, type=_artifact_id)

    export = subparsers.add_parser(
        "export",
        help="Export one governed Builder artifact to a portable package.",
        allow_abbrev=False,
    )
    export.add_argument("--artifact-id", required=True, type=_artifact_id)
    export.add_argument("--output", dest="output_path", required=True, type=Path)

    return parser


def parse_cli_args(argv: Sequence[str]) -> ParsedCLICommand:
    namespace = build_parser().parse_args(tuple(argv))
    return ParsedCLICommand(
        command=namespace.command,
        output_format=namespace.output_format,
        manifest_path=getattr(namespace, "manifest_path", None),
        output_path=getattr(namespace, "output_path", None),
        artifact_id=getattr(namespace, "artifact_id", None),
    )


def _artifact_id(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise argparse.ArgumentTypeError("artifact ID must not be empty")
    return normalized
