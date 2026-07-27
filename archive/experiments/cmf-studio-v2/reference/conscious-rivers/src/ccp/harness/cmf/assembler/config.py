"""
FR-VID-02 Configuration — RunningHub API Configuration (DEP-VID-009)

All secrets and configuration are loaded from environment variables.
No API keys or credentials appear in source code.
FR-VID-02 §3 TD5, §4 Stage 2 Step 1, Build Prompt Anti-Pattern 8.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RunningHubConfig:
    """RunningHub API configuration loaded from environment variables (DEP-VID-009)."""

    api_key: str
    proxy_url: str
    proxy_plus_url: str
    default_model: str
    vram_tier: str
    max_concurrent_t2i: int
    job_timeout_sec: int
    retry_max: int
    output_width: int
    output_height: int
    asset_storage_base: str
    receipt_output_dir: str

    @classmethod
    def from_env(cls) -> "RunningHubConfig":
        """Load configuration from environment variables. Raises KeyError if required vars missing."""
        api_key = os.environ["RUNNINGHUB_API_KEY"]
        base_url = os.environ.get("RUNNINGHUB_BASE_URL", "https://www.runninghub.ai")
        vram_tier = os.environ.get("RUNNINGHUB_VRAM_TIER", "48GB")
        default_model = os.environ.get("CMF_T2I_MODEL", "flux-dev-fp8")

        proxy_url = f"{base_url}/proxy/{api_key}"
        proxy_plus_url = f"{base_url}/proxy-plus/{api_key}"

        return cls(
            api_key=api_key,
            proxy_url=proxy_url,
            proxy_plus_url=proxy_plus_url,
            default_model=default_model,
            vram_tier=vram_tier,
            max_concurrent_t2i=int(os.environ.get("CMF_T2I_MAX_CONCURRENT", "12")),
            job_timeout_sec=int(os.environ.get("CMF_T2I_JOB_TIMEOUT", "120")),
            retry_max=int(os.environ.get("CMF_T2I_RETRY_MAX", "3")),
            output_width=int(os.environ.get("CMF_OUTPUT_WIDTH", "1080")),
            output_height=int(os.environ.get("CMF_OUTPUT_HEIGHT", "1920")),
            asset_storage_base=os.environ.get("CMF_ASSET_STORAGE", "./assets"),
            receipt_output_dir=os.environ.get("CMF_RECEIPT_DIR", "./receipts"),
        )

    @property
    def active_proxy_url(self) -> str:
        """Return the active proxy URL based on VRAM tier preference.
        FR-VID-02 §3 TD4: 48GB preferred, 24GB fallback."""
        if self.vram_tier == "48GB":
            return self.proxy_plus_url
        return self.proxy_url
