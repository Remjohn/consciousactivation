from __future__ import annotations

from ca_runtime.cli import product_status
from . import PRODUCT_ID, PRODUCT_VERSION


def status() -> dict[str, object]:
    return product_status(PRODUCT_ID, PRODUCT_VERSION)
