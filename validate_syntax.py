"""Quick syntax validation script for all project Python files."""
import py_compile
import os
import sys

root = os.path.dirname(os.path.abspath(__file__))
files = []
for r, d, fs in os.walk(root):
    if '.venv' in r or '.idea' in r or '__pycache__' in r:
        continue
    for f in fs:
        if f.endswith('.py') and f != 'validate_syntax.py':
            files.append(os.path.join(r, f))

ok = 0
fails = []
for p in files:
    try:
        py_compile.compile(p, doraise=True)
        ok += 1
    except py_compile.PyCompileError as e:
        fails.append(str(e))

print(f"Compiled {ok}/{len(files)} files successfully")
if fails:
    print(f"\n{len(fails)} FAILURES:")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("All files OK!")
