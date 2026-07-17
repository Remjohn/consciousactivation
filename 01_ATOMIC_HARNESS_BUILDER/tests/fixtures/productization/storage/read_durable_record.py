from __future__ import annotations

import json
from pathlib import Path
import sys

from cmf_builder.adapters.sqlite_productization_repository import (
    SQLiteProductizationRepository,
)


repository = SQLiteProductizationRepository(Path(sys.argv[1]))
repository.initialize()
record = repository.get_record(sys.argv[2], sys.argv[3])
receipt = repository.get_command_receipt(sys.argv[4])
print(
    json.dumps(
        {
            "record_hash": record.payload_hash if record else None,
            "record_version": record.version if record else None,
            "receipt_hash": receipt.result_hash if receipt else None,
            "integrity_issues": repository.verify_integrity(),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
)

