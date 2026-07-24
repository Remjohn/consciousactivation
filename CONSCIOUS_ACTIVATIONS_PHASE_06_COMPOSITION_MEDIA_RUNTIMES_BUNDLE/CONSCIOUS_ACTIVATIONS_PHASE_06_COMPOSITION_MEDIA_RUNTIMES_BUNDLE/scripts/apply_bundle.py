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
            if sha256(target)!=record["new_sha256"] and not force: raise RuntimeError(f"applied file drifted: {record['path']}")
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
    transient={"__pycache__",".pytest_cache",".mypy_cache",".ruff_cache"}
    for cache in sorted(repo.rglob("*"),key=lambda path:len(path.parts),reverse=True):
        if cache.is_dir() and (cache.name in transient or cache.name.endswith(".egg-info")): shutil.rmtree(cache,ignore_errors=True)
        elif cache.is_file() and cache.suffix in {".pyc",".pyo"}: cache.unlink(missing_ok=True)
    for directory in sorted((repo/safe_relative(value) for value in receipt.get("created_directories",[])),key=lambda path:len(path.parts),reverse=True):
        if directory.exists():
            try: directory.rmdir()
            except OSError:
                if force: shutil.rmtree(directory,ignore_errors=True)
                else: raise RuntimeError(f"refusing to remove non-empty created directory: {directory}")

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--repo",type=Path,required=True); parser.add_argument("--bundle",type=Path,default=Path(__file__).resolve().parents[1]); parser.add_argument("--dry-run",action="store_true"); parser.add_argument("--allow-dirty",action="store_true"); parser.add_argument("--skip-tests",action="store_true"); parser.add_argument("--keep-failed",action="store_true"); parser.add_argument("--create-branch"); parser.add_argument("--commit",action="store_true"); args=parser.parse_args()
    repo=args.repo.resolve(); bundle=args.bundle.resolve()
    if not (repo/"CMF_PROGRAM_CONTROL").is_dir(): raise SystemExit(f"not a Conscious Activations repository: {repo}")
    verification=verify(bundle)
    if verification["result"]!="PASS": print(json.dumps(verification,indent=2)); return 2
    baseline=json.loads((bundle/"BASELINE_LOCK.json").read_text()); operations=json.loads((bundle/"FILE_OPERATIONS.json").read_text()); manifest=json.loads((bundle/"PACKAGE_MANIFEST.json").read_text()); bundle_id=manifest["bundle_id"]
    git_repo=is_git_repo(repo)
    if git_repo:
        status=git(repo,"status","--porcelain").stdout.strip()
        if status and not args.allow_dirty: raise SystemExit("git worktree is dirty; commit/stash or pass --allow-dirty")
        if args.create_branch and git(repo,"branch","--list",args.create_branch).stdout.strip(): raise SystemExit(f"branch exists: {args.create_branch}")
    failures=[]; actions=[]
    for requirement in baseline["required_existing_files"]:
        target=repo/safe_relative(requirement["path"])
        if not target.is_file(): failures.append(f"required baseline file missing: {requirement['path']}")
        elif sha256(target)!=requirement["sha256"]: failures.append(f"required baseline hash mismatch: {requirement['path']}")
    for operation in operations["operations"]:
        target=repo/safe_relative(operation["path"])
        if target.exists():
            observed=sha256(target)
            if observed==operation["new_sha256"]: actions.append({**operation,"action":"already_applied"}); continue
            if operation["operation"]=="create": failures.append(f"create target exists with different bytes: {operation['path']}"); continue
            if observed!=operation["old_sha256"]: failures.append(f"replace target hash mismatch: {operation['path']}"); continue
            actions.append({**operation,"action":"replace"})
        else:
            if operation["operation"]=="replace": failures.append(f"replace target missing: {operation['path']}"); continue
            actions.append({**operation,"action":"create"})
    plan={"schema_version":"ca-phase06-apply-plan/v1","bundle_id":bundle_id,"repo":str(repo),"actions":actions,"failures":failures,"result":"PASS" if not failures else "FAIL"}; print(json.dumps(plan,indent=2,sort_keys=True))
    if failures: return 2
    if args.dry_run: return 0
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise SystemExit("Phase 6 requires ffmpeg and ffprobe on PATH")
    if git_repo and args.create_branch: git(repo,"checkout","-b",args.create_branch)
    state=repo/".conscious-activations"/"bundle-state"/bundle_id; backups=state/"backups"; staging=repo/".conscious-activations"/"apply-staging"/bundle_id
    if state.exists(): raise SystemExit(f"bundle state exists: {state}")
    backups.mkdir(parents=True); staging.mkdir(parents=True); created_dirs=set(); applied=[]
    for action in actions:
        if action["action"]=="already_applied": continue
        cursor=(repo/safe_relative(action["path"])).parent
        while cursor!=repo and not cursor.exists(): created_dirs.add(cursor); cursor=cursor.parent
    try:
        for action in actions:
            if action["action"]=="already_applied": continue
            relative=safe_relative(action["path"]); source=bundle/"full-replacement-files"/relative; staged=staging/relative; staged.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(source,staged)
            if sha256(staged)!=action["new_sha256"]: raise RuntimeError(f"staged hash mismatch: {action['path']}")
        for action in actions:
            if action["action"]=="already_applied": continue
            relative=safe_relative(action["path"]); target=repo/relative; backup=None
            if action["action"]=="replace": backup=backups/relative; backup.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(target,backup)
            target.parent.mkdir(parents=True,exist_ok=True); os.replace(staging/relative,target)
            applied.append({"path":action["path"],"operation":action["action"],"old_sha256":action.get("old_sha256"),"new_sha256":action["new_sha256"],"backup_path":str(backup) if backup else None})
        receipt={"schema_version":"ca-phase06-apply-receipt/v1","bundle_id":bundle_id,"applied_at_utc":utc_now(),"repo":str(repo),"files":applied,"created_directories":[str(path.relative_to(repo)).replace("\\","/") for path in sorted(created_dirs,key=lambda value:(len(value.parts),str(value)))],"tests":"not_run" if args.skip_tests else "pending","result":"APPLIED_TESTS_SKIPPED" if args.skip_tests else "APPLIED_PENDING_TESTS"}
        state.mkdir(parents=True,exist_ok=True); receipt_path=state/"apply_receipt.json"; receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
        if not args.skip_tests:
            env=dict(os.environ); env["PYTHONDONTWRITEBYTECODE"]="1"; env["PYTHONWARNINGS"]="error::ResourceWarning"
            main_report=state/"validation_report.json"; install_report=state/"clean_install_report.json"
            main_log=state/"validation.log"; install_log=state/"clean_install.log"
            # Run the isolated package-install proof before the larger concurrent
            # regression pool. This avoids pip/build-resource contention after
            # many test subprocesses have completed.
            with install_log.open("w",encoding="utf-8") as log:
                install_check=subprocess.run([sys.executable,str(repo/"scripts"/"phase6"/"validate_phase6_clean_install.py"),"--report",str(install_report)],cwd=repo,text=True,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=900)
            with main_log.open("w",encoding="utf-8") as log:
                main_check=subprocess.run([sys.executable,str(repo/"scripts"/"phase6"/"validate_phase6.py"),"--report",str(main_report)],cwd=repo,text=True,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=900)
            if main_check.returncode!=0 or install_check.returncode!=0:
                receipt["tests"]="FAIL"; receipt["result"]="APPLY_FAILED_VALIDATION"; receipt["validation_failure"]={"clean_install_returncode":install_check.returncode,"clean_install_log_tail":install_log.read_text(encoding="utf-8",errors="replace")[-4000:],"main_returncode":main_check.returncode,"main_log_tail":main_log.read_text(encoding="utf-8",errors="replace")[-4000:]}; receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
                if not args.keep_failed:
                    rollback_from_receipt(repo,receipt,force=True); receipt["result"]="ROLLED_BACK_AFTER_VALIDATION_FAILURE"; state.mkdir(parents=True,exist_ok=True); receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
                return 3
            receipt["tests"]="PASS"; receipt["result"]="APPLIED_VALIDATED"; receipt["validation_reports"]=[str(main_report),str(install_report)]; receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
        shutil.rmtree(staging,ignore_errors=True)
        if args.commit:
            if not git_repo: raise RuntimeError("--commit requires git")
            git(repo,"add","--all"); git(repo,"commit","-m","implement Phase 6 composition and media production runtimes")
        print(json.dumps(receipt,indent=2,sort_keys=True)); return 0
    except Exception:
        if applied and not args.keep_failed: rollback_from_receipt(repo,{"files":applied,"created_directories":[str(path.relative_to(repo)).replace("\\","/") for path in created_dirs]},force=True)
        raise
if __name__=="__main__": raise SystemExit(main())
