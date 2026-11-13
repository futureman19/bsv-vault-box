"""Bounded local verification; no blockchain or external services."""
from pathlib import Path
import subprocess, sys
R=Path(__file__).resolve().parent
blender='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
jobs=[('build',[sys.executable,str(R/'build.py')]),('motion',['C:/Program Files/nodejs/node.exe',str(R/'tests.mjs')])]
for name in ['source','parity']:
 jobs.append((name,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+name+'.py'))]))
jobs.append(('theme',[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/'test_theme.py')]))
for name in ['browser','extended']:
 jobs.append((name,[sys.executable,str(R/('verify_'+name+'.py'))]))
for name,cmd in jobs:
 p=subprocess.run(cmd,capture_output=True)
 (R/('recheck-'+name+'.txt')).write_bytes(p.stdout+p.stderr)
 print(name, 'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if p.returncode:print((p.stdout+p.stderr).decode(errors='replace'));sys.exit(p.returncode)
print('ALL CHECKS PASS')
