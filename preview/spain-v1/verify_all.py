"""Run acceptance without reauthoring. Logs remain folder-local."""
from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
node=os.environ.get('NODE','C:/Program Files/nodejs/node.exe')
commands=[('build',[sys.executable,'build.py']),('motion',[node,'--test','tests.mjs'])]
commands += [(name,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+name+'.py'))]) for name in ['source','parity','theme']]
commands += [(name,[sys.executable,'verify_'+name+'.py']) for name in ['browser','extended']]
results=[]
for name,cmd in commands:
 with (R/(name+'-log.txt')).open('w',encoding='utf8') as log:result=subprocess.run(cmd,cwd=R,stdout=log,stderr=subprocess.STDOUT)
 results.append({'check':name,'exit_code':result.returncode});print(name, 'PASS' if result.returncode==0 else 'FAIL',flush=True)
 if result.returncode:raise SystemExit(result.returncode)
(R/'verification-check.json').write_text(json.dumps({'status':'PASS','commands':results},indent=2))
print('ALL ACCEPTANCE CHECKS PASS')
