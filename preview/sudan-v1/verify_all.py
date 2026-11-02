"""Bounded acceptance runner; every stage must return success, never inferred."""
from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
commands=[('build',[sys.executable,str(R/'build.py')]),('motion',['node','--test',str(R/'tests.mjs')])]
for name in ['source','parity','theme']:
 commands.append((name,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+name+'.py'))]))
for name in ['browser','extended']:commands.append((name,[sys.executable,str(R/('verify_'+name+'.py'))]))
results=[]
for name,cmd in commands:
 run=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf8',errors='replace')
 (R/(name+'-log.txt')).write_text(run.stdout+'\n'+run.stderr,encoding='utf8')
 print(name.upper(), 'PASS' if run.returncode==0 else 'FAIL',flush=True)
 if name=='build':print(run.stdout.strip(),flush=True)
 if run.returncode:
  print(run.stdout,run.stderr);raise SystemExit(run.returncode)
 results.append({'check':name,'status':'PASS','exit_code':run.returncode,'command':cmd})
(R/'acceptance-summary.json').write_text(json.dumps({'status':'PASS','checks':results,'owner':'Hermes direct execution; optional Codex lane failed auth without implementation'},indent=2),encoding='utf8')
subprocess.run([sys.executable,str(R/'package_delivery.py')],cwd=R,check=True)
print('ALL_ACCEPTANCE_CHECKS PASS',flush=True)
