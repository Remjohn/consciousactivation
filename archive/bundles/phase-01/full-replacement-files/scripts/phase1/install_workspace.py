from __future__ import annotations

import argparse
import json
import subprocess
import sys
import sysconfig
from pathlib import Path

from _paths import repo_root


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--venv", type=Path, default=Path(".venv-phase1"))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    root = repo_root()
    venv = (root / args.venv).resolve() if not args.venv.is_absolute() else args.venv
    if venv.exists() and not args.force:
        raise SystemExit(f"venv already exists: {venv}; pass --force to replace it")
    if venv.exists():
        import shutil
        shutil.rmtree(venv)

    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    python = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    script = (
        "import json,site,sysconfig;"
        "print(json.dumps({'purelib':sysconfig.get_paths()['purelib']}))"
    )
    result = subprocess.run([str(python), "-c", script], check=True, capture_output=True, text=True)
    purelib = Path(json.loads(result.stdout)["purelib"])
    source_paths = [
        root / "packages" / "ca_contracts" / "src",
        root / "packages" / "ca_runtime" / "src",
        root / "04_ACTIVATIVE_INTELLIGENCE_RUNTIME" / "src",
        root / "05_ATOMIC_HARNESS_PIPELINE" / "src",
        root / "06_INTERVIEW_EXPRESSION" / "src",
    ]
    pth = purelib / "conscious_activations_phase1.pth"
    pth.write_text("\n".join(str(path.resolve()) for path in source_paths) + "\n", encoding="utf-8")
    smoke = (
        "import ca_contracts,ca_runtime,cmf_activative_intelligence,cmf_pipeline,"
        "conscious_activations_interview_expression;"
        "print('phase1 workspace import: PASS')"
    )
    subprocess.run([str(python), "-c", smoke], check=True)
    print(json.dumps({"result": "PASS", "venv": str(venv), "python": str(python), "pth": str(pth)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
