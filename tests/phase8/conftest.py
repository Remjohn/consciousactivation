from __future__ import annotations
import sys
from pathlib import Path
import pytest
from _support import delegation_root

@pytest.fixture
def rc4_root(): return delegation_root()

@pytest.fixture
def fake_provider_script(tmp_path:Path)->Path:
    path=tmp_path/'fake_provider.py'
    path.write_text('''from __future__ import annotations\nimport json,sys\nfrom pathlib import Path\nrequest=Path(sys.argv[1]); response=Path(sys.argv[2]); data=json.loads(request.read_text())\nresponse.write_text(json.dumps({"provider_id":"FAKE_PROVIDER","request_sha256":__import__("hashlib").sha256(json.dumps(data,sort_keys=True,separators=(",",":")).encode()).hexdigest(),"outputs":[]},sort_keys=True))\n''')
    return path
