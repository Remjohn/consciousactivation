import json
from pathlib import Path
from functools import lru_cache

@lru_cache(maxsize=1)
def load_taxonomy_bindings() -> dict:
    path = Path(__file__).resolve().parents[3] / "skill-packages" / "stage1-visual-syntax-skill" / "contracts" / "taxonomy_bindings.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_canonical_primitives() -> frozenset[str]:
    data = load_taxonomy_bindings()
    return frozenset(data["primitive_registry"]["canonical"])

def get_canonical_slide_roles() -> frozenset[str]:
    data = load_taxonomy_bindings()
    return frozenset(data["slide_role_registry"]["canonical"])

def get_canonical_zones() -> frozenset[str]:
    data = load_taxonomy_bindings()
    return frozenset(data["zone_registry"]["canonical"])

def get_taxonomy_candidate_states() -> frozenset[str]:
    data = load_taxonomy_bindings()
    return frozenset(data["taxonomy_candidate_states"]["enum"])

def is_canonical_primitive(value: str) -> bool:
    return value in get_canonical_primitives()

def is_canonical_slide_role(value: str) -> bool:
    return value in get_canonical_slide_roles()

def is_canonical_zone(value: str) -> bool:
    return value in get_canonical_zones()
