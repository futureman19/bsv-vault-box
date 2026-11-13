"""Bounded non-authoring acceptance; writes actual subprocess logs."""
from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parent
B=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
commands=[('build',[sys.executable,str(R/'build.py')]),('motion',['node','--test',str(R/'tests.mjs')])]
commands += [(s,[B,'--background','-t','2','--factory-startup','--python-exit-code','1','--python',str(R/(s+'.py'))]) for s in ['verify_theme','verify_source','verify_parity']]
commands += [(s,[sys.executable,str(R/(s+'.py'))]) for s in ['verify_browser','verify_extended']]
results=[]
for name,cmd in commands:
 p=subprocess.run(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/(name+'.log')).write_bytes(p.stdout);results.append({'check':name,'exit_code':p.returncode,'command':cmd})
 print(name, 'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if p.returncode:print(p.stdout.decode(errors='replace'));raise SystemExit(p.returncode)
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','commands':results},indent=2))
print('ALL ACCEPTANCE CHECKS PASS')
