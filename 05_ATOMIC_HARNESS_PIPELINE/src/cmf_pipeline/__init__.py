"""Deterministic development core for the Atomic Harness Pipeline."""

PRODUCT_ID = "atomic-harness-pipeline"
PRODUCT_VERSION = "0.2.0-dev.1"
PACKAGE_VERSION = "0.2.0.dev1"
__version__ = PACKAGE_VERSION

from .application import PipelineApplication

__all__ = ["PipelineApplication", "PRODUCT_ID", "PRODUCT_VERSION", "PACKAGE_VERSION"]
