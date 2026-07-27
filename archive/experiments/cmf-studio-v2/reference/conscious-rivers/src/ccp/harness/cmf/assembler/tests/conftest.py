"""pytest configuration — adds cmf-assembler package to sys.path for imports."""

import sys
from pathlib import Path

# Add the cmf-assembler package root to sys.path so tests can import modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
