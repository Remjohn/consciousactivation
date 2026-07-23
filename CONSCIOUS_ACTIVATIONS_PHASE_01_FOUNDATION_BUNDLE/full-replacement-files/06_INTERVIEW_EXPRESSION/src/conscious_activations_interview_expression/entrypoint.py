from __future__ import annotations

from ca_runtime.cli import run_product_cli
from . import PRODUCT_ID, PRODUCT_VERSION


def main() -> int:
    return run_product_cli(PRODUCT_ID, PRODUCT_VERSION)
