"""Distribution-relative paths shared by source and released validators."""

from pathlib import Path


DISTRIBUTION_ROOT = Path(__file__).resolve().parents[2]
ROOT = DISTRIBUTION_ROOT
LAYOUT = "SOURCE" if DISTRIBUTION_ROOT.name == "packages" else "RELEASE"
WORKSPACE_ROOT = DISTRIBUTION_ROOT.parent if LAYOUT == "SOURCE" else DISTRIBUTION_ROOT
CONTRACTS_ROOT = DISTRIBUTION_ROOT / "contracts"
FIXTURES_ROOT = DISTRIBUTION_ROOT / "fixtures"
COMPATIBILITY_ROOT = DISTRIBUTION_ROOT / "compatibility"
PROTOCOL_ROOT = DISTRIBUTION_ROOT / "protocol"


def distribution_path(relative_path: str) -> Path:
    """Resolve a canonical distribution-relative path without checkout assumptions."""

    path = Path(relative_path)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Unsafe distribution path: {relative_path}")
    return DISTRIBUTION_ROOT / path
