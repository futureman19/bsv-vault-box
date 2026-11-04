"""Canonical bounded verification entrypoint; no authoring, network or external writes."""
from pathlib import Path
import subprocess,sys,json,os,hashlib
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER_EXE','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
node='C:/Program Files/nodejs/node.exe' if Path('C:/Program Files/nodejs/node.exe').exists() else 'node'
checks=[('build',[sys.executable,str(R/'build.py')]),('motion',[node,str(R/'tests.mjs')])]
for n in ['source','theme','parity']:checks.append((n,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/f'verify_{n}.py')]))
for n in ['browser','extended']:checks.append((n,[sys.executable,str(R/f'verify_{n}.py')]))
results=[]
for name,command in checks:
 with (R/(name+'-output.txt')).open('w') as log:
  completed=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
 results.append({'check':name,'exit_code':completed.returncode,'status':'PASS' if completed.returncode==0 else 'FAIL'})
 print(name,results[-1]['status'],flush=True)
 assert completed.returncode==0,(name,completed.returncode)
report={'status':'PASS','checks':results,'html_bytes':(R/'palau-v1.html').stat().st_size,'glb_bytes':(R/'palau.glb').stat().st_size,'html_sha256':hashlib.sha256((R/'palau-v1.html').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((R/'palau.glb').read_bytes()).hexdigest()}
(R/'acceptance-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
