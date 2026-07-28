from __future__ import annotations

from pydantic import BaseModel


class RefModel(BaseModel):
    """{object_id, version, sha256} -- the AIR/Pipeline immutable-ref shape.

    STAND-IN NOTICE: this file is nominally TS-APP-API-003's output
    (`api/schemas/interviews.py`), which TS-APP-API-007 declares it reuses
    unchanged. As of this implementation, TS-APP-API-003 has not actually
    been built in this codebase -- `api/schemas/` did not exist, and
    `api/main.py` only has a commented-out placeholder for the interviews
    router. Rather than block TS-APP-API-007 on an unrelated spec, this file
    supplies only the `RefModel` shape TS-APP-API-007 needs. When
    TS-APP-API-003 is actually implemented, it should own this file in full
    (interview-specific request/response models etc.); if it defines
    `RefModel` identically (which the shape leaves little room not to), no
    change is needed here.
    """

    object_id: str
    version: str
    sha256: str
