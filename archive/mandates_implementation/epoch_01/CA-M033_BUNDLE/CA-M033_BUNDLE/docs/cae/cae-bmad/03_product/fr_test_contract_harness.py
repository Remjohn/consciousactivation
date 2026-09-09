"""Canonical functional-requirement verification gate for CA-M033.

This module is intentionally dependency-light so the canonical FR contract can
be checked without importing the CAE runtime. The verification boundary is the
repository's real pytest discovery/execution path.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, Mapping, Sequence


FR_ROW_RE = re.compile(
    r"^\| `(?P<id>FR-\d{3})` \| (?P<title>.*?) \| `(?P<stage>.*?)` \| "
    r"`(?P<invariant>.*?)` \| \[(?P<surface>.*?)\]\((?P<url>.*?)\) \| "
    r"`(?P<status>SPECIFIED|IMPLEMENTED|VERIFIED)` \|$"
)
FR_DETAIL_RE = re.compile(r"^### `(FR-\d{3})`:.*$", re.MULTILINE)
DETAIL_STATUS_RE = re.compile(
    r"^\- \*\*Lifecycle Status:\*\* `(SPECIFIED|IMPLEMENTED|VERIFIED)`$",
    re.MULTILINE,
)
REGISTRY_ROW_RE = re.compile(
    r"^\| `(?P<id>FR-\d{3})` \| `(?P<positive>[^`]+)` \| "
    r"`(?P<negative>[^`]+)` \| `(?P<evidence>[^`]+)` \|$",
    re.MULTILINE,
)
EXPECTED_FR_IDS = tuple(f"FR-{index:03d}" for index in range(1, 58))


class LifecycleStatus(str, Enum):
    SPECIFIED = "SPECIFIED"
    IMPLEMENTED = "IMPLEMENTED"
    VERIFIED = "VERIFIED"


class ContractValidationError(ValueError):
    """Raised when the canonical FR document violates the CA-M033 contract."""


@dataclass(frozen=True)
class FunctionalRequirement:
    requirement_id: str
    title: str
    stage: str
    invariant: str
    implementation_surface: str
    status: LifecycleStatus


@dataclass(frozen=True)
class VerificationLocators:
    positive: str
    negative: str
    evidence_class: str = "EXECUTABLE"


@dataclass(frozen=True)
class TestRun:
    locator: str
    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True)
class VerificationDecision:
    requirement_id: str
    prior_status: LifecycleStatus
    final_status: LifecycleStatus
    allowed: bool
    reason: str
    discovery_runs: tuple[TestRun, ...] = ()
    execution_runs: tuple[TestRun, ...] = ()


def _normalise_repo_path(value: Path | str) -> Path:
    path = Path(value).expanduser().resolve()
    return path


def parse_functional_requirements(path: Path | str) -> tuple[FunctionalRequirement, ...]:
    """Parse and structurally validate the canonical FR matrix and detail blocks."""
    contract_path = _normalise_repo_path(path)
    text = contract_path.read_text(encoding="utf-8")

    rows = []
    for line in text.splitlines():
        match = FR_ROW_RE.match(line)
        if match:
            rows.append(
                FunctionalRequirement(
                    requirement_id=match.group("id"),
                    title=match.group("title").strip(),
                    stage=match.group("stage").strip(),
                    invariant=match.group("invariant").strip(),
                    implementation_surface=match.group("surface").strip(),
                    status=LifecycleStatus(match.group("status")),
                )
            )

    ids = tuple(requirement.requirement_id for requirement in rows)
    if ids != EXPECTED_FR_IDS:
        raise ContractValidationError(
            "Canonical FR matrix must contain exactly FR-001 through FR-057 "
            f"in order; found {ids!r}"
        )

    if any(
        not requirement.title
        or not requirement.stage
        or not requirement.invariant
        or not requirement.implementation_surface
        for requirement in rows
    ):
        raise ContractValidationError(
            "Every FR must have a title, stage/subsystem, invariant, and "
            "implementation surface."
        )

    detail_matches = list(FR_DETAIL_RE.finditer(text))
    if tuple(match.group(1) for match in detail_matches) != EXPECTED_FR_IDS:
        raise ContractValidationError(
            "Detailed FR sections must contain exactly FR-001 through FR-057 in order."
        )

    detail_statuses: dict[str, LifecycleStatus] = {}
    for index, match in enumerate(detail_matches):
        start = match.end()
        end = detail_matches[index + 1].start() if index + 1 < len(detail_matches) else len(text)
        section = text[start:end]
        status_matches = DETAIL_STATUS_RE.findall(section)
        if len(status_matches) != 1:
            raise ContractValidationError(
                f"{match.group(1)} must contain exactly one Lifecycle Status field."
            )
        detail_statuses[match.group(1)] = LifecycleStatus(status_matches[0])

    for requirement in rows:
        detail_status = detail_statuses[requirement.requirement_id]
        if detail_status != requirement.status:
            raise ContractValidationError(
                f"{requirement.requirement_id} status mismatch between the master "
                f"table ({requirement.status.value}) and detailed section "
                f"({detail_status.value})."
            )

    return tuple(rows)


def parse_verification_registry(path: Path | str) -> Mapping[str, VerificationLocators]:
    """Read the canonical positive/negative acceptance-test registry from the FR doc."""
    contract_path = _normalise_repo_path(path)
    text = contract_path.read_text(encoding="utf-8")
    registry: dict[str, VerificationLocators] = {}
    for match in REGISTRY_ROW_RE.finditer(text):
        registry[match.group("id")] = VerificationLocators(
            positive=match.group("positive").strip(),
            negative=match.group("negative").strip(),
            evidence_class=match.group("evidence").strip(),
        )
    return registry


def validate_contract_document(path: Path | str) -> tuple[FunctionalRequirement, ...]:
    """Fail closed on malformed lifecycle state or any unsupported VERIFIED claim."""
    requirements = parse_functional_requirements(path)
    registry = parse_verification_registry(path)

    requirement_ids = {requirement.requirement_id for requirement in requirements}
    unknown_registry_ids = set(registry) - requirement_ids
    if unknown_registry_ids:
        raise ContractValidationError(
            f"Verification registry contains unknown FR IDs: {sorted(unknown_registry_ids)}"
        )

    for requirement in requirements:
        if requirement.status == LifecycleStatus.VERIFIED:
            locators = registry.get(requirement.requirement_id)
            if locators is None:
                raise ContractValidationError(
                    f"{requirement.requirement_id} cannot be VERIFIED without both "
                    "registered positive and negative acceptance-test locators."
                )
            if not locators.positive or not locators.negative:
                raise ContractValidationError(
                    f"{requirement.requirement_id} VERIFIED status requires non-empty "
                    "positive and negative locators."
                )
            if locators.evidence_class != "EXECUTABLE":
                raise ContractValidationError(
                    f"{requirement.requirement_id} VERIFIED status requires EXECUTABLE evidence."
                )

    return requirements


def _run_pytest(
    locator: str,
    *,
    cwd: Path,
    collect_only: bool,
) -> TestRun:
    command = [sys.executable, "-m", "pytest"]
    if collect_only:
        command.extend(["--collect-only", "-q"])
    else:
        command.extend(["-q"])
    command.append(locator)

    completed = subprocess.run(
        command,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    return TestRun(
        locator=locator,
        command=tuple(command),
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def discover_locator(locator: str, *, cwd: Path | str) -> TestRun:
    """Use real pytest collection to prove an acceptance locator exists."""
    return _run_pytest(locator, cwd=_normalise_repo_path(cwd), collect_only=True)


def execute_locator(locator: str, *, cwd: Path | str) -> TestRun:
    """Use real pytest execution to prove an acceptance locator passes."""
    return _run_pytest(locator, cwd=_normalise_repo_path(cwd), collect_only=False)


def _blocked(
    requirement: FunctionalRequirement,
    reason: str,
    *,
    discovery_runs: Sequence[TestRun] = (),
    execution_runs: Sequence[TestRun] = (),
) -> VerificationDecision:
    return VerificationDecision(
        requirement_id=requirement.requirement_id,
        prior_status=requirement.status,
        final_status=requirement.status,
        allowed=False,
        reason=reason,
        discovery_runs=tuple(discovery_runs),
        execution_runs=tuple(execution_runs),
    )


def verify_requirement(
    requirement: FunctionalRequirement,
    locators: VerificationLocators | None,
    *,
    cwd: Path | str,
) -> VerificationDecision:
    """Run the full fail-closed gate for one requirement.

    A requirement may move to VERIFIED only from IMPLEMENTED, and only when
    both positive and negative locators are discovered and pass. Existing
    VERIFIED requirements are revalidated but never silently downgraded.
    """
    if requirement.status is LifecycleStatus.SPECIFIED:
        return _blocked(
            requirement,
            "SPECIFIED requirements cannot skip the IMPLEMENTED lifecycle state.",
        )
    if requirement.status not in (
        LifecycleStatus.IMPLEMENTED,
        LifecycleStatus.VERIFIED,
    ):
        return _blocked(
            requirement,
            f"Unsupported source lifecycle state: {requirement.status.value}.",
        )

    if locators is None:
        return _blocked(
            requirement,
            "Missing positive/negative acceptance-test registration.",
        )
    if not locators.positive or not locators.negative:
        return _blocked(
            requirement,
            "Both positive and negative acceptance-test locators are required.",
        )

    locators_to_check = (locators.positive, locators.negative)
    discovery_runs = tuple(
        discover_locator(locator, cwd=cwd) for locator in locators_to_check
    )
    failed_discovery = next((run for run in discovery_runs if not run.passed), None)
    if failed_discovery is not None:
        return _blocked(
            requirement,
            f"Acceptance-test discovery failed for {failed_discovery.locator}.",
            discovery_runs=discovery_runs,
        )

    execution_runs = tuple(
        execute_locator(locator, cwd=cwd) for locator in locators_to_check
    )
    failed_execution = next((run for run in execution_runs if not run.passed), None)
    if failed_execution is not None:
        return _blocked(
            requirement,
            f"Acceptance-test execution failed for {failed_execution.locator}.",
            discovery_runs=discovery_runs,
            execution_runs=execution_runs,
        )

    return VerificationDecision(
        requirement_id=requirement.requirement_id,
        prior_status=requirement.status,
        final_status=LifecycleStatus.VERIFIED,
        allowed=True,
        reason="Both positive and negative acceptance tests were discovered and passed.",
        discovery_runs=discovery_runs,
        execution_runs=execution_runs,
    )


def validate_verified_evidence(
    path: Path | str,
    *,
    cwd: Path | str,
) -> tuple[VerificationDecision, ...]:
    """Validate every VERIFIED claim in the canonical document against pytest."""
    requirements = validate_contract_document(path)
    registry = parse_verification_registry(path)
    decisions = []
    for requirement in requirements:
        if requirement.status != LifecycleStatus.VERIFIED:
            continue
        decision = verify_requirement(
            requirement,
            registry[requirement.requirement_id],
            cwd=cwd,
        )
        if not decision.allowed:
            raise ContractValidationError(
                f"{requirement.requirement_id} VERIFIED claim rejected: {decision.reason}"
            )
        decisions.append(decision)
    return tuple(decisions)


def format_decision(decision: VerificationDecision) -> str:
    return (
        f"{decision.requirement_id}: "
        f"{decision.prior_status.value} -> {decision.final_status.value}; "
        f"{'ALLOWED' if decision.allowed else 'BLOCKED'}; {decision.reason}"
    )


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CA-M033 canonical FR verification gate.")
    parser.add_argument(
        "command",
        choices=("validate", "verify"),
        help="validate document structure or execute all VERIFIED evidence",
    )
    parser.add_argument(
        "--contract",
        default="docs/cae/cae-bmad/03_product/FUNCTIONAL_REQUIREMENTS.md",
        help="repository-relative path to the canonical FR contract",
    )
    parser.add_argument(
        "--cwd",
        default=".",
        help="repository root used for pytest discovery/execution",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        if args.command == "validate":
            requirements = validate_contract_document(args.contract)
            verified = sum(
                requirement.status == LifecycleStatus.VERIFIED
                for requirement in requirements
            )
            print(
                f"CA-M033 contract valid: {len(requirements)} FRs parsed; "
                f"{verified} VERIFIED claim(s) registry-backed."
            )
            return 0

        decisions = validate_verified_evidence(
            args.contract,
            cwd=args.cwd,
        )
        for decision in decisions:
            print(format_decision(decision))
        print(f"CA-M033 verified evidence valid: {len(decisions)} VERIFIED FR(s).")
        return 0
    except (ContractValidationError, OSError) as exc:
        print(f"CA-M033 contract gate BLOCKED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
