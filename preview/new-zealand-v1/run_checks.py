"""Bounded independent acceptance. Author separately before invoking."""
from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parent
B='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
commands=[('build',[sys.executable,'build.py']),('motion',['node','--test','tests.mjs'])]+[(n,[B,'--background','--factory-startup','--python-exit-code','1','--python','verify_'+n+'.py']) for n in ['source','parity','theme','pivots']]+[(n,[sys.executable,'verify_'+n+'.py']) for n in ['browser','extended']]
results=[]
for name,command in commands:
 p=subprocess.run(command,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/(name+'-output.txt')).write_bytes(p.stdout)
 print(name.upper(), 'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if p.returncode:print(p.stdout.decode('utf8',errors='replace'));raise SystemExit(p.returncode)
 results.append({'check':name,'status':'PASS','exit_code':p.returncode})
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks':results},indent=2))
print('HTML_BYTES', (R/'new-zealand-v1.html').stat().st_size,'GLB_BYTES',(R/'new-zealand.glb').stat().st_size)
