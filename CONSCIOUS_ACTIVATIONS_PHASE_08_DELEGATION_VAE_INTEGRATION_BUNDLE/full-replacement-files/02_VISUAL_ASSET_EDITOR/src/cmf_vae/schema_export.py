from __future__ import annotations
import json, shutil
from pathlib import Path
from typing import Any

def schema_root() -> Path: return Path(__file__).resolve().parent / "schemas"
def export_schemas(destination: str|Path) -> dict[str,Any]:
    target=Path(destination); target.mkdir(parents=True,exist_ok=True); files=[]
    for path in sorted(schema_root().glob("*.json")):
        shutil.copy2(path,target/path.name); files.append(path.name)
    return {"source":str(schema_root()),"destination":str(target),"file_count":len(files),"files":files}
def schema_registry() -> dict[str,Any]: return json.loads((schema_root()/"CONTRACT_REGISTRY.json").read_text(encoding="utf-8"))
