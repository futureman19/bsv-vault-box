"""Exit-checked final gates. Does not author/re-render or silently retry failures."""
from pathlib import Path
import subprocess,sys,json,os
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
commands=[('motion',['node','--test','tests.mjs']),('build',[sys.executable,'build.py'])]
commands += [(n,[blender,'--background','--factory-startup','--python-exit-code','1','--python',f'verify_{n}.py']) for n in ['source','parity','theme']]
commands += [(n,[sys.executable,f'verify_{n}.py']) for n in ['browser','extended']]
results=[]
for name,cmd in commands:
 p=subprocess.run(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf8',errors='replace',timeout=600)
 (R/(name+'-output.txt')).write_text(p.stdout,encoding='utf8')
 results.append({'gate':name,'command':cmd,'exit_code':p.returncode,'status':'PASS' if p.returncode==0 else 'FAIL'})
 (R/'acceptance-check.json').write_text(json.dumps(results,indent=2))
 print(name.upper(),results[-1]['status'],flush=True)
 if p.returncode:print(p.stdout);sys.exit(p.returncode)
print('ALL ACCEPTANCE CHECKS PASS',flush=True)
