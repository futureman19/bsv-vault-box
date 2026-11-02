"""Run after maps.py and author.py. All subprocess failures are fatal."""
from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
node=os.environ.get('NODE_EXE','C:/Program Files/nodejs/node.exe')
steps=[('build',[sys.executable,str(R/'build.py')]),('motion',[node,'--test',str(R/'tests.mjs')])]
for n in ['source','parity']:
 steps.append((n,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+n+'.py'))]))
for n in ['browser','theme']:
 steps.append((n,[sys.executable,str(R/('verify_'+n+'.py'))]))
results=[]
for name,cmd in steps:
 p=subprocess.run(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/(name+'-log.txt')).write_bytes(p.stdout)
 print(p.stdout.decode('utf8',errors='replace'));print(name.upper(), 'PASS' if p.returncode==0 else 'FAIL',flush=True)
 results.append({'check':name,'exit_code':p.returncode})
 (R/'checks.json').write_text(json.dumps(results,indent=2))
 if p.returncode:sys.exit(p.returncode)
print('ALL CHECKS PASS')
