"""CA-M033 acceptance and countercase tests for the canonical FR contract gate."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from textwrap import dedent

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HARNESS_DIR = REPO_ROOT / "docs" / "cae" / "cae-bmad" / "03_product"
sys.path.insert(0, str(HARNESS_DIR))

import fr_test_contract_harness as harness  # noqa: E402


CONTRACT_PATH = HARNESS_DIR / "FUNCTIONAL_REQUIREMENTS.md"
FR033_POSITIVE = (
    "tests/cae/test_m033_canonical_fr_test_contract_harness.py"
    "::test_m033_positive_verified_path"
)
FR033_NEGATIVE = (
    "tests/cae/test_m033_canonical_fr_test_contract_harness.py"
    "::test_m033_negative_verified_path"
)


def _write_pytest_fixture(directory: Path, *, positive_passes: bool = True) -> Path:
    test_path = directory / "test_boundary.py"
    positive_body = (
        "assert (tmp_path / 'observed.txt').write_text('observed', encoding='utf-8') == 8\n"
        "assert (tmp_path / 'observed.txt').read_text(encoding='utf-8') == 'observed'\n"
        if positive_passes
        else "assert False, 'intentional positive acceptance failure'\n"
    )
    rendered_positive = "\n".join(
        "    " + line for line in positive_body.splitlines()
    )
    test_path.write_text(
        dedent(
            f"""
            import pytest

            def test_positive_boundary(tmp_path):
{rendered_positive}

            def test_negative_boundary():
                with pytest.raises(ValueError, match="blocked"):
                    raise ValueError("blocked")
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    return test_path


def _write_contract_variant(source: str, destination: Path, *, remove_registry: bool) -> None:
    mutated = source
    if remove_registry:
        mutated = re.sub(
            r"^\| `FR-033` \| `tests/cae/test_m033_canonical_fr_test_contract_harness\.py::test_m033_positive_verified_path` \| "
            r"`tests/cae/test_m033_canonical_fr_test_contract_harness\.py::test_m033_negative_verified_path` \| "
            r"`EXECUTABLE` \|\n",
            "",
            mutated,
            flags=re.MULTILINE,
        )
    destination.write_text(mutated, encoding="utf-8")


def test_m033_contract_matrix_is_complete_and_status_consistent() -> None:
    requirements = harness.parse_functional_requirements(CONTRACT_PATH)
    assert len(requirements) == 57
    assert [requirement.requirement_id for requirement in requirements] == [
        f"FR-{index:03d}" for index in range(1, 58)
    ]

    verified = [
        requirement.requirement_id
        for requirement in requirements
        if requirement.status is harness.LifecycleStatus.VERIFIED
    ]
    implemented = [
        requirement.requirement_id
        for requirement in requirements
        if requirement.status is harness.LifecycleStatus.IMPLEMENTED
    ]
    assert verified == ["FR-033"]
    assert len(implemented) == 56


def test_m033_registry_locators_are_real_pytest_nodes() -> None:
    registry = harness.parse_verification_registry(CONTRACT_PATH)
    assert registry["FR-033"].positive == FR033_POSITIVE
    assert registry["FR-033"].negative == FR033_NEGATIVE

    positive = harness.discover_locator(FR033_POSITIVE, cwd=REPO_ROOT)
    negative = harness.discover_locator(FR033_NEGATIVE, cwd=REPO_ROOT)

    assert positive.passed, positive.stderr or positive.stdout
    assert negative.passed, negative.stderr or negative.stdout


def test_m033_canonical_document_rejects_unregistered_verified_claim(tmp_path: Path) -> None:
    source = CONTRACT_PATH.read_text(encoding="utf-8")
    variant = tmp_path / "FUNCTIONAL_REQUIREMENTS.md"
    _write_contract_variant(source, variant, remove_registry=True)

    with pytest.raises(
        harness.ContractValidationError,
        match=r"FR-033 cannot be VERIFIED",
    ):
        harness.validate_contract_document(variant)


def test_m033_positive_verified_path(tmp_path: Path) -> None:
    test_module = _write_pytest_fixture(tmp_path)
    requirement = harness.FunctionalRequirement(
        requirement_id="FR-033",
        title="Normative Test Contract Lifecycle",
        stage="Stage 16: Verification & PRD",
        invariant="FR-PRD-001",
        implementation_surface="docs/cae/cae-bmad/03_product/fr_test_contract_harness.py",
        status=harness.LifecycleStatus.IMPLEMENTED,
    )

    positive_locator = f"{test_module}::test_positive_boundary"
    negative_locator = f"{test_module}::test_negative_boundary"

    decision = harness.verify_requirement(
        requirement,
        harness.VerificationLocators(
            positive=positive_locator,
            negative=negative_locator,
        ),
        cwd=REPO_ROOT,
    )

    assert decision.allowed is True
    assert decision.prior_status is harness.LifecycleStatus.IMPLEMENTED
    assert decision.final_status is harness.LifecycleStatus.VERIFIED
    assert all(run.passed for run in decision.discovery_runs)
    assert all(run.passed for run in decision.execution_runs)


def test_m033_negative_verified_path(tmp_path: Path) -> None:
    test_module = _write_pytest_fixture(tmp_path)
    requirement = harness.FunctionalRequirement(
        requirement_id="FR-033",
        title="Normative Test Contract Lifecycle",
        stage="Stage 16: Verification & PRD",
        invariant="FR-PRD-001",
        implementation_surface="docs/cae/cae-bmad/03_product/fr_test_contract_harness.py",
        status=harness.LifecycleStatus.IMPLEMENTED,
    )

    decision = harness.verify_requirement(
        requirement,
        harness.VerificationLocators(
            positive=f"{test_module}::test_positive_boundary",
            negative="",
        ),
        cwd=REPO_ROOT,
    )

    assert decision.allowed is False
    assert decision.final_status is harness.LifecycleStatus.IMPLEMENTED
    assert "Both positive and negative" in decision.reason


def test_m033_failing_positive_path_is_fail_closed(tmp_path: Path) -> None:
    test_module = _write_pytest_fixture(tmp_path, positive_passes=False)
    requirement = harness.FunctionalRequirement(
        requirement_id="FR-033",
        title="Normative Test Contract Lifecycle",
        stage="Stage 16: Verification & PRD",
        invariant="FR-PRD-001",
        implementation_surface="docs/cae/cae-bmad/03_product/fr_test_contract_harness.py",
        status=harness.LifecycleStatus.IMPLEMENTED,
    )

    decision = harness.verify_requirement(
        requirement,
        harness.VerificationLocators(
            positive=f"{test_module}::test_positive_boundary",
            negative=f"{test_module}::test_negative_boundary",
        ),
        cwd=REPO_ROOT,
    )

    assert decision.allowed is False
    assert decision.final_status is harness.LifecycleStatus.IMPLEMENTED
    assert "execution failed" in decision.reason
    assert any(not run.passed for run in decision.execution_runs)



def test_m033_specified_cannot_skip_implemented_lifecycle_state() -> None:
    requirement = harness.FunctionalRequirement(
        requirement_id="FR-033",
        title="Normative Test Contract Lifecycle",
        stage="Stage 16: Verification & PRD",
        invariant="FR-PRD-001",
        implementation_surface="docs/cae/cae-bmad/03_product/fr_test_contract_harness.py",
        status=harness.LifecycleStatus.SPECIFIED,
    )

    decision = harness.verify_requirement(
        requirement,
        harness.VerificationLocators(
            positive=FR033_POSITIVE,
            negative=FR033_NEGATIVE,
        ),
        cwd=REPO_ROOT,
    )

    assert decision.allowed is False
    assert decision.final_status is harness.LifecycleStatus.SPECIFIED
    assert decision.discovery_runs == ()
    assert decision.execution_runs == ()
    assert "cannot skip the IMPLEMENTED" in decision.reason

def test_m033_missing_positive_locator_is_blocked_before_execution() -> None:
    requirement = harness.FunctionalRequirement(
        requirement_id="FR-033",
        title="Normative Test Contract Lifecycle",
        stage="Stage 16: Verification & PRD",
        invariant="FR-PRD-001",
        implementation_surface="docs/cae/cae-bmad/03_product/fr_test_contract_harness.py",
        status=harness.LifecycleStatus.IMPLEMENTED,
    )

    decision = harness.verify_requirement(
        requirement,
        harness.VerificationLocators(
            positive="",
            negative=FR033_NEGATIVE,
        ),
        cwd=REPO_ROOT,
    )

    assert decision.allowed is False
    assert decision.final_status is harness.LifecycleStatus.IMPLEMENTED
    assert decision.discovery_runs == ()
    assert decision.execution_runs == ()
    assert "Both positive and negative" in decision.reason
