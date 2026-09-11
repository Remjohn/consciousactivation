from __future__ import annotations

import os
from pathlib import Path


def data_root() -> Path:
    configured = os.environ.get("CA_DATA_ROOT")
    if configured:
        return Path(configured).expanduser()
    return Path(".conscious-activations") / "dev"


def default_database_path(product_id: str) -> Path:
    safe = product_id.replace("/", "-").replace("\\", "-")
    return data_root() / safe / "product.sqlite3"
