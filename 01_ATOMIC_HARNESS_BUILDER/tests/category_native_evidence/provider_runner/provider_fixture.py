from __future__ import annotations

import json
import sys
from time import sleep


def main() -> int:
    mode = sys.argv[1]
    if mode == "version":
        sys.stdout.write("provider-fixture/1.0.0")
        return 0
    if mode == "echo-json":
        value = json.loads(sys.stdin.buffer.read())
        sys.stdout.write(json.dumps(value, sort_keys=True, separators=(",", ":")))
        return 0
    if mode == "sleep":
        sleep(5)
        return 0
    if mode == "invalid-json":
        sys.stdout.write("not-json")
        return 0
    if mode == "fail":
        sys.stderr.write("governed fixture failure")
        return 17
    return 64


if __name__ == "__main__":
    raise SystemExit(main())
