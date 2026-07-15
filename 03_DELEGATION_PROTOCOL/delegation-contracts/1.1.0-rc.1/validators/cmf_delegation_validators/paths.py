"""Repository paths shared by local contract validators."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONTRACTS_ROOT = ROOT / "packages" / "contracts"
FIXTURES_ROOT = ROOT / "packages" / "fixtures"
COMPATIBILITY_ROOT = ROOT / "packages" / "compatibility"

