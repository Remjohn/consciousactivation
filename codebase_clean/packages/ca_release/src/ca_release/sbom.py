from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

from ca_contracts import canonical_sha256


def build_sbom(repo_root: str|Path) -> dict[str,Any]:
    root=Path(repo_root);components=[]
    for pyproject in sorted(root.rglob('pyproject.toml')):
        if any(part in {'.venv','node_modules','.conscious-activations'} for part in pyproject.parts): continue
        data=tomllib.loads(pyproject.read_text(encoding='utf-8')); project=data.get('project',{})
        if project.get('name'):
            components.append({'ecosystem':'python','name':project['name'],'version':project.get('version','UNKNOWN'),'path':pyproject.relative_to(root).as_posix(),'dependencies':sorted(project.get('dependencies',[]))})
    for package in sorted(root.rglob('package.json')):
        if 'node_modules' in package.parts: continue
        data=json.loads(package.read_text(encoding='utf-8'))
        if data.get('name'):
            deps={**data.get('dependencies',{}),**data.get('devDependencies',{})}
            components.append({'ecosystem':'node','name':data['name'],'version':data.get('version','UNKNOWN'),'path':package.relative_to(root).as_posix(),'dependencies':[f'{k}@{v}' for k,v in sorted(deps.items())]})
    components.sort(key=lambda item:(item['ecosystem'],item['name'],item['path']))
    payload={'schema_version':'ca-development-sbom/v1','component_count':len(components),'components':components,'production_authorized':False}
    payload['sbom_sha256']=canonical_sha256(payload);return payload
