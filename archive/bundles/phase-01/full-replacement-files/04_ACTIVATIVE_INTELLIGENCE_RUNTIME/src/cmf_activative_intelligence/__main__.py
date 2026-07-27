from ca_runtime.cli import run_product_cli
from . import PRODUCT_ID, PRODUCT_VERSION

if __name__ == "__main__":
    raise SystemExit(run_product_cli(PRODUCT_ID, PRODUCT_VERSION))
