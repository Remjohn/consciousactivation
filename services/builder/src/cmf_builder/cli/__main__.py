import os
from pathlib import Path

from cmf_builder.cli.bootstrap import local_main


database = Path(
    os.environ.get("CMF_BUILDER_DB", ".cmf-builder/builder.sqlite3")
)
raise SystemExit(local_main(database_path=database))
