from __future__ import annotations
import os
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    ca_data_root: Path
    ca_media_root: Path
    ca_delegation_root: Path
    ca_studio_rpc_entrypoint: Path
    gateway_version: str = "0.1.0"
    ws_poll_interval_ms: int = 750


def load_config() -> AppConfig:
    data_root = Path(os.environ.get("CA_DATA_ROOT", "/state"))
    return AppConfig(
        ca_data_root=data_root,
        ca_media_root=Path(os.environ.get("CA_MEDIA_ROOT", str(data_root / "media"))),
        ca_delegation_root=Path(
            os.environ.get(
                "CA_DELEGATION_ROOT",
                # default: the rc4 delegation release bundle. The
                # ca_delegation_rc4 *package* (packages/ca_delegation_rc4) only
                # ships the loader code -- the RELEASE_RECEIPT.json + contracts/
                # it expects at runtime live in the published release under
                # services/delegation/delegation-contracts/1.1.0-rc.4/.
                str(
                    Path(__file__).parent.parent
                    / "services"
                    / "delegation"
                    / "delegation-contracts"
                    / "1.1.0-rc.4"
                ),
            )
        ),
        ca_studio_rpc_entrypoint=Path(
            os.environ.get(
                "CA_STUDIO_RPC_ENTRYPOINT",
                str(
                    Path(__file__).parent.parent
                    / "services"
                    / "studio"
                    / "dist"
                    / "rpc.js"
                ),
            )
        ),
        ws_poll_interval_ms=int(os.environ.get("WS_POLL_INTERVAL_MS", "750")),
    )
