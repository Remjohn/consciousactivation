from __future__ import annotations
import argparse, json, os, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from verify_bundle import safe_relative, sha256, verify

def utc_now(): return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
def git(repo,*args,check=True): return subprocess.run(["git",*args],cwd=repo,text=True,capture_output=True,check=check)
def is_git_repo(repo): return (repo/".git").exists() and shutil.which("git") is not None

def rollback_from_receipt(repo,receipt,force=False):
    for record in reversed(receipt["files"]):
        target=repo/safe_relative(record["path"])
        if record["operation"]=="create":
            if not target.exists(): continue
            observed=sha256(target)
            if observed!=record["new_sha256"] and not force: raise RuntimeError(f"applied file drifted: {record['path']}")
            target.unlink()
        else:
            old_sha=record.get("old_sha256")
            if target.exists():
                observed=sha256(target)
                if old_sha and observed==old_sha: continue
                if observed!=record["new_sha256"] and not force: raise RuntimeError(f"applied file drifted: {record['path']}")
            backup=Path(record["backup_path"])
            if not backup.is_file():
                if target.exists() and old_sha and sha256(target)==old_sha: continue
                raise RuntimeError(f"missing backup: {backup}")
            target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(backup,target)
    transient_names={"__pycache__",".pytest_cache",".mypy_cache",".ruff_cache"}
    for cache in sorted(repo.rglob("*"),key=lambda p:len(p.parts),reverse=True):
        if cache.is_dir() and (cache.name in transient_names or cache.name.endswith(".egg-info")): shutil.rmtree(cache,ignore_errors=True)
        elif cache.is_file() and cache.suffix in {".pyc",".pyo"}: cache.unlink(missing_ok=True)
    for directory in sorted((repo/safe_relative(v) for v in receipt.get("created_directories",[])),key=lambda p:len(p.parts),reverse=True):
        if directory.exists():
            try: directory.rmdir()
            except OSError:
                if force: shutil.rmtree(directory,ignore_errors=True)
                else: raise RuntimeError(f"refusing to remove non-empty created directory: {directory}")

def main():
    p=argparse.ArgumentParser(); p.add_argument("--repo",type=Path,required=True); p.add_argument("--bundle",type=Path,default=Path(__file__).resolve().parents[1]); p.add_argument("--dry-run",action="store_true"); p.add_argument("--allow-dirty",action="store_true"); p.add_argument("--skip-tests",action="store_true"); p.add_argument("--keep-failed",action="store_true"); p.add_argument("--create-branch"); p.add_argument("--commit",action="store_true"); a=p.parse_args()
    repo=a.repo.resolve(); bundle=a.bundle.resolve()
    if not (repo/"CMF_PROGRAM_CONTROL").is_dir(): raise SystemExit(f"not a Conscious Activations repository: {repo}")
    vr=verify(bundle)
    if vr["result"]!="PASS": print(json.dumps(vr,indent=2)); return 2
    baseline=json.loads((bundle/"BASELINE_LOCK.json").read_text()); ops=json.loads((bundle/"FILE_OPERATIONS.json").read_text()); manifest=json.loads((bundle/"PACKAGE_MANIFEST.json").read_text()); bundle_id=manifest["bundle_id"]
    git_repo=is_git_repo(repo)
    if git_repo:
        status=git(repo,"status","--porcelain").stdout.strip()
        if status and not a.allow_dirty: raise SystemExit("git worktree is dirty; commit/stash or pass --allow-dirty")
        if a.create_branch and git(repo,"branch","--list",a.create_branch).stdout.strip(): raise SystemExit(f"branch exists: {a.create_branch}")
    failures=[]; actions=[]
    for req in baseline["required_existing_files"]:
        target=repo/safe_relative(req["path"])
        if not target.is_file(): failures.append(f"required baseline file missing: {req['path']}")
        elif sha256(target)!=req["sha256"]: failures.append(f"required baseline hash mismatch: {req['path']}")
    for op in ops["operations"]:
        target=repo/safe_relative(op["path"])
        if target.exists():
            observed=sha256(target)
            if observed==op["new_sha256"]: actions.append({**op,"action":"already_applied"}); continue
            if op["operation"]=="create": failures.append(f"create target exists with different bytes: {op['path']}"); continue
            if observed!=op["old_sha256"]: failures.append(f"replace target hash mismatch: {op['path']}"); continue
            actions.append({**op,"action":"replace"})
        else:
            if op["operation"]=="replace": failures.append(f"replace target missing: {op['path']}"); continue
            actions.append({**op,"action":"create"})
    plan={"schema_version":"ca-phase05-apply-plan/v1","bundle_id":bundle_id,"repo":str(repo),"actions":actions,"failures":failures,"result":"PASS" if not failures else "FAIL"}; print(json.dumps(plan,indent=2,sort_keys=True))
    if failures: return 2
    if a.dry_run: return 0
    if git_repo and a.create_branch: git(repo,"checkout","-b",a.create_branch)
    state=repo/".conscious-activations"/"bundle-state"/bundle_id; backups=state/"backups"; staging=repo/".conscious-activations"/"apply-staging"/bundle_id
    if state.exists(): raise SystemExit(f"bundle state exists: {state}")
    backups.mkdir(parents=True); staging.mkdir(parents=True)
    created_dirs=set(); applied=[]
    for action in actions:
        if action["action"]=="already_applied": continue
        cursor=(repo/safe_relative(action["path"])).parent
        while cursor!=repo and not cursor.exists(): created_dirs.add(cursor); cursor=cursor.parent
    try:
        for action in actions:
            if action["action"]=="already_applied": continue
            rel=safe_relative(action["path"]); src=bundle/"full-replacement-files"/rel; staged=staging/rel; staged.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,staged)
            if sha256(staged)!=action["new_sha256"]: raise RuntimeError(f"staged hash mismatch: {action['path']}")
        for action in actions:
            if action["action"]=="already_applied": continue
            rel=safe_relative(action["path"]); target=repo/rel; backup=None
            if action["action"]=="replace": backup=backups/rel; backup.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(target,backup)
            target.parent.mkdir(parents=True,exist_ok=True); os.replace(staging/rel,target)
            applied.append({"path":action["path"],"operation":action["action"],"old_sha256":action.get("old_sha256"),"new_sha256":action["new_sha256"],"backup_path":str(backup) if backup else None})
        receipt={"schema_version":"ca-phase05-apply-receipt/v1","bundle_id":bundle_id,"applied_at_utc":utc_now(),"repo":str(repo),"files":applied,"created_directories":[str(x.relative_to(repo)).replace("\\","/") for x in sorted(created_dirs,key=lambda q:(len(q.parts),str(q)))],"tests":"not_run" if a.skip_tests else "pending","result":"APPLIED_TESTS_SKIPPED" if a.skip_tests else "APPLIED_PENDING_TESTS"}
        state.mkdir(parents=True,exist_ok=True); receipt_path=state/"apply_receipt.json"; receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
        if not a.skip_tests:
            report=state/"validation_report.json"; completed=subprocess.run([sys.executable,str(repo/"scripts"/"phase5"/"validate_phase5.py"),"--report",str(report)],cwd=repo,text=True)
            if completed.returncode!=0:
                receipt["tests"]="FAIL"; receipt["result"]="APPLY_FAILED_VALIDATION"; receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
                if not a.keep_failed:
                    rollback_from_receipt(repo,receipt,force=True); receipt["result"]="ROLLED_BACK_AFTER_VALIDATION_FAILURE"; state.mkdir(parents=True,exist_ok=True); receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
                return 3
            receipt["tests"]="PASS"; receipt["result"]="APPLIED_VALIDATED"; receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
        shutil.rmtree(staging,ignore_errors=True)
        if a.commit:
            if not git_repo: raise RuntimeError("--commit requires git")
            git(repo,"add","--all"); git(repo,"commit","-m","implement Phase 5 semantic production compiler")
        print(json.dumps(receipt,indent=2,sort_keys=True)); return 0
    except Exception:
        if applied and not a.keep_failed:
            receipt={"files":applied,"created_directories":[str(x.relative_to(repo)).replace("\\","/") for x in created_dirs]}; rollback_from_receipt(repo,receipt,force=True)
        raise
if __name__=="__main__": raise SystemExit(main())
