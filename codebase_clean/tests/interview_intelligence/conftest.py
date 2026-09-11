import sys
from pathlib import Path

# Ensure services are in Python module search path
repo_root = Path(__file__).parents[2]
services_src = [
    repo_root / "services" / "interview-intelligence" / "src",
    repo_root / "services" / "interview-composer" / "src",
    repo_root / "services" / "air" / "src",
    repo_root / "services" / "interview" / "src",
]

for src_path in services_src:
    str_path = str(src_path)
    if str_path not in sys.path:
        sys.path.insert(0, str_path)
