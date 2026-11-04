from pathlib import Path
import subprocess,sys,os
R=Path(__file__).resolve().parent
B=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
steps=[('build',[sys.executable,'build.py']),('motion',['node','tests.mjs'])]+[(n,[B,'--background','--factory-startup','--python-exit-code','1','--python','verify_'+n+'.py']) for n in ['source','parity','theme']]+[(n,[sys.executable,'verify_'+n+'.py']) for n in ['browser','extended']]
for n,cmd in steps:
 p=subprocess.run(cmd,cwd=R,capture_output=True);(R/(n+'-output.txt')).write_bytes(p.stdout+p.stderr)
 if p.returncode:print((p.stdout+p.stderr).decode(errors='replace'));raise SystemExit(p.returncode)
 print('PASS',n)
print((R/'build-output.txt').read_text())
