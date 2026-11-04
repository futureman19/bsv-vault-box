"""Hermes canonical bounded validation; does not regenerate the authored model."""
from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
node='C:/Program Files/nodejs/node.exe' if os.name=='nt' else 'node'
commands=[('build',[sys.executable,'build.py']),('motion',[node,'--test','tests.mjs'])]
commands += [(n,[blender,'--background','--factory-startup','--python-exit-code','1','--python','verify_'+n+'.py']) for n in ['source','parity','theme']]
commands += [(n,[sys.executable,'verify_'+n+'.py']) for n in ['browser','extended']]
results=[]
for name,cmd in commands:
 p=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf8',errors='replace')
 (R/('hermes-'+name+'-output.txt')).write_text(p.stdout+p.stderr,encoding='utf8')
 print(name.upper(), 'PASS' if p.returncode==0 else 'FAIL',flush=True)
 results.append(dict(check=name,exit_code=p.returncode,owner='hermes',command=cmd))
 if p.returncode:print((p.stdout+p.stderr)[-5000:]);sys.exit(p.returncode)
(R/'acceptance-check.json').write_text(json.dumps(dict(status='PASS',checks=results),indent=2))
print('HTML_BYTES',(R/'fiji-v1.html').stat().st_size,'GLB_BYTES',(R/'fiji.glb').stat().st_size)
