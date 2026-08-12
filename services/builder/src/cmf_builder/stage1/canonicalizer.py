import hashlib
import json

def compute_syntax_hash(slide_role: str, container_zones: list[str], primitives: list[dict], anchor_elements: list[dict]) -> str:
    """
    Computes a deterministic SHA-256 hash of the syntax components.
    
    Canonicalization rules:
    - Sort container_zones alphabetically.
    - Sort primitives by (primitive_type, zone).
    - Sort anchor_elements by label.
    """
    sorted_zones = sorted(container_zones)
    
    canonical_primitives = []
    for p in sorted(primitives, key=lambda x: (x.get("primitive_type", "") if isinstance(x, dict) else "", x.get("zone", "") if isinstance(x, dict) else "")):
        canonical_primitives.append(p)
        
    canonical_anchors = []
    for a in sorted(anchor_elements, key=lambda x: x.get("label", "") if isinstance(x, dict) else x):
        canonical_anchors.append(a)
        
    canonical_obj = {
        "anchor_elements": canonical_anchors,
        "container_zones": sorted_zones,
        "primitives": canonical_primitives,
        "slide_role": slide_role
    }
    
    json_str = json.dumps(canonical_obj, separators=(',', ':'), sort_keys=True)
    return hashlib.sha256(json_str.encode('utf-8')).hexdigest()
