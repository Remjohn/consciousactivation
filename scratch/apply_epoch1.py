import os, shutil, py_compile, sys
sys.stdout.reconfigure(encoding='utf-8')

epoch_dir = 'Mandates implementation/epoch_01'
bundles = sorted(os.listdir(epoch_dir))

copied_files = []
syntax_errors = []

for b in bundles:
    bpath = os.path.join(epoch_dir, b)
    if not os.path.isdir(bpath):
        continue
    nested = os.path.join(bpath, b)
    root_src = nested if os.path.isdir(nested) else bpath
    
    print(f'\nApplying {b} from {root_src}...')
    for root, dirs, files in os.walk(root_src):
        for f in files:
            if f == 'AGENT_HANDOFF.md' or f.endswith('.pyc') or f.endswith('.DS_Store'):
                continue
            src_file = os.path.join(root, f)
            rel_path = os.path.relpath(src_file, root_src)
            dest_file = os.path.abspath(rel_path)
            
            # Ensure parent dir exists
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            
            # Copy file
            shutil.copy2(src_file, dest_file)
            copied_files.append(rel_path.replace('\\', '/'))
            print(f'  [COPIED] {rel_path}')
            
            # Syntax check if python
            if f.endswith('.py'):
                try:
                    py_compile.compile(dest_file, doraise=True)
                except py_compile.PyCompileError as e:
                    print(f'  [SYNTAX ERROR] {rel_path}: {e}')
                    syntax_errors.append((rel_path, str(e)))

print('\n' + '='*50)
print(f'Total files copied: {len(copied_files)}')
print(f'Syntax errors: {len(syntax_errors)}')
if syntax_errors:
    print('FAILED syntax check!')
    for s in syntax_errors:
        print(' ', s)
    sys.exit(1)
else:
    print('SUCCESS: All copied python files compiled cleanly!')
