from __future__ import annotations
import os
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    ca_data_root: Path
    ca_media_root: Path
    ca_delegation_root: Path
    gateway_version: str = "0.1.0"


def load_config() -> AppConfig:
    data_root = Path(os.environ.get("CA_DATA_ROOT", "/state"))
    return AppConfig(
        ca_data_root=data_root,
        ca_media_root=Path(os.environ.get("CA_MEDIA_ROOT", str(data_root / "media"))),
        ca_delegation_root=Path(
            os.environ.get(
                "CA_DELEGATION_ROOT",
                # default: find ca_delegation_rc4 package data relative to repo root
                str(Path(__file__).parent.parent / "packages" / "ca_delegation_rc4"),
            )
        ),
    )
