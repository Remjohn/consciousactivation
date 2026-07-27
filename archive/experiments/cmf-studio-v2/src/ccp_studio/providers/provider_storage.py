from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

from ccp_studio.contracts.provider_adapters import (
    ProviderId,
    ProviderOutputAsset,
    ProviderOutputType,
)


class ProviderOutputStorage:
    def __init__(self, storage_root: str | Path = "storage/provider_outputs"):
        self.storage_root = Path(storage_root)

    def save_bytes(
        self,
        *,
        brand_id: str,
        request_id: str,
        provider_id: ProviderId,
        data: bytes,
        filename: str,
        output_type: ProviderOutputType = ProviderOutputType.IMAGE,
        mime_type: str = "image/png",
        metadata: dict | None = None,
    ) -> ProviderOutputAsset:
        safe_filename = filename.replace("/", "_").replace("\\", "_")
        directory = self.storage_root / brand_id / request_id
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / safe_filename
        path.write_bytes(data)

        sha256 = hashlib.sha256(data).hexdigest()
        meta = metadata or {}
        meta.update({"sha256": sha256, "provider_id": provider_id.value})
        (directory / f"{safe_filename}.metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

        return ProviderOutputAsset(
            request_id=request_id,
            provider_id=provider_id,
            output_type=output_type,
            uri=str(path),
            sha256=sha256,
            mime_type=mime_type,
            byte_size=len(data),
            metadata=meta,
        )

    def download_url(
        self,
        *,
        brand_id: str,
        request_id: str,
        provider_id: ProviderId,
        url: str,
        filename: str,
        output_type: ProviderOutputType = ProviderOutputType.IMAGE,
    ) -> ProviderOutputAsset:
        with urlopen(url, timeout=60) as response:
            data = response.read()
            mime_type = response.headers.get("Content-Type", "application/octet-stream")
        if "." not in filename:
            parsed = urlparse(url)
            suffix = Path(parsed.path).suffix or ".bin"
            filename = f"{filename}{suffix}"
        return self.save_bytes(
            brand_id=brand_id,
            request_id=request_id,
            provider_id=provider_id,
            data=data,
            filename=filename,
            output_type=output_type,
            mime_type=mime_type,
            metadata={"source_url_downloaded": True},
        )
