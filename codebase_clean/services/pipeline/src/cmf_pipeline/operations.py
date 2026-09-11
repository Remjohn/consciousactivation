from __future__ import annotations

import shutil
import sqlite3
import subprocess
import time
from contextlib import closing
from pathlib import Path
from typing import Any, Callable, Mapping

from ca_contracts import bytes_sha256, canonical_sha256

from .domain.errors import PipelineValidationError


class PipelineOperationsService:
    def __init__(self, repository): self.repository=repository

    def backup(self, destination: str|Path) -> dict[str,Any]:
        self.repository.initialize(); target=Path(destination); target.parent.mkdir(parents=True,exist_ok=True)
        with closing(sqlite3.connect(self.repository.path)) as source, closing(sqlite3.connect(target)) as dest:
            source.backup(dest)
        with target.open('rb') as f: digest=bytes_sha256(f.read())
        with closing(sqlite3.connect(target)) as conn:
            integrity=str(conn.execute('PRAGMA integrity_check').fetchone()[0]); tables=int(conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'").fetchone()[0])
        if integrity!='ok': raise PipelineValidationError('backup integrity check failed')
        return {'backup_id':f"pipeline-backup:{digest}",'logical_uri':'backups/pipeline.sqlite3','sha256':digest,'bytes':target.stat().st_size,'integrity':integrity,'table_count':tables,'source_database_sha256':bytes_sha256(self.repository.path.read_bytes())}

    def restore_rehearsal(self, backup_path: str|Path, restore_path: str|Path) -> dict[str,Any]:
        source=Path(backup_path);target=Path(restore_path);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        with closing(sqlite3.connect(target)) as conn:
            integrity=str(conn.execute('PRAGMA integrity_check').fetchone()[0]);counts={row[0]:int(conn.execute(f'SELECT COUNT(*) FROM "{row[0]}"').fetchone()[0]) for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")}
        if integrity!='ok': raise PipelineValidationError('restored database failed integrity check')
        receipt={'rehearsal_id':f"restore-rehearsal:{canonical_sha256({'backup_sha':bytes_sha256(source.read_bytes()),'counts':counts})}",'backup_sha256':bytes_sha256(source.read_bytes()),'restored_sha256':bytes_sha256(target.read_bytes()),'integrity':integrity,'table_counts':counts,'result':'PASS'}
        receipt['receipt_sha256']=canonical_sha256(receipt);return receipt

    @staticmethod
    def preflight(commands: Mapping[str,list[str]]) -> dict[str,Any]:
        results=[]
        for component,command in sorted(commands.items()):
            started=time.perf_counter_ns()
            try:
                proc=subprocess.run(command,text=True,capture_output=True,timeout=20)
                status='PASS' if proc.returncode==0 else 'FAIL'
                output=(proc.stdout or proc.stderr).strip().splitlines()[:4]
            except (FileNotFoundError,subprocess.TimeoutExpired) as exc:
                status='UNAVAILABLE';output=[str(exc)]
            results.append({'component_id':component,'command':command,'status':status,'elapsed_micros':(time.perf_counter_ns()-started)//1000,'output_lines':output})
        return {'preflight_id':f"environment-preflight:{canonical_sha256(results)}",'results':results,'production_authorized':False}

    @staticmethod
    def benchmark(name: str, callback: Callable[[],Any], *, iterations:int=3) -> dict[str,Any]:
        if iterations<1: raise PipelineValidationError('iterations must be >= 1')
        samples=[];result_sha=''
        for _ in range(iterations):
            started=time.perf_counter_ns();result=callback();samples.append((time.perf_counter_ns()-started)//1000);result_sha=canonical_sha256(result)
        samples.sort()
        return {'benchmark_id':f"benchmark:{canonical_sha256({'name':name,'samples':samples,'result':result_sha})}",'name':name,'iterations':iterations,'samples_micros':samples,'minimum_micros':samples[0],'median_micros':samples[len(samples)//2],'maximum_micros':samples[-1],'result_sha256':result_sha,'sla_claimed':False}
