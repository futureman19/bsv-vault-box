"""Bounded verification of existing authored source; does not regenerate geometry."""
from pathlib import Path
import subprocess,sys,json,os,shutil
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER_EXE','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
node='C:/Program Files/nodejs/node.exe' if Path('C:/Program Files/nodejs/node.exe').exists() else shutil.which('node')
commands=[('build',[sys.executable,str(R/'build.py')]),('motion',[node,'--test',str(R/'tests.mjs')])]
commands += [(n,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/f'verify_{n}.py')]) for n in ['source','parity','theme']]
commands += [(n,[sys.executable,str(R/f'verify_{n}.py')]) for n in ['maps','browser','extended']]
results=[]
for name,cmd in commands:
 p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=600)
 (R/f'{name}-final-log.txt').write_text(p.stdout+p.stderr,encoding='utf8')
 results.append({'check':name,'exit_code':p.returncode,'status':'PASS' if p.returncode==0 else 'FAIL'})
 (R/'acceptance.json').write_text(json.dumps(results,indent=2))
 print(name,results[-1]['status'],flush=True)
 assert p.returncode==0,(name,p.stdout[-2000:],p.stderr[-2000:])
print('HTML_BYTES',(R/'central-african-republic-v1.html').stat().st_size,'GLB_BYTES',(R/'central-african-republic.glb').stat().st_size)
