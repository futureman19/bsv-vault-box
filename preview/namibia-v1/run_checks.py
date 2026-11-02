"""Bounded independent verification of the saved asset (no model regeneration)."""
from pathlib import Path
import subprocess,sys,json,os,hashlib
R=Path(__file__).resolve().parent
BLENDER=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
commands=[('build',[sys.executable,str(R/'build.py')]),('motion',['node','--test',str(R/'tests.mjs')])]
for n in ['source','parity','theme_source']:
 commands.append((n,[BLENDER,'--background','--threads','2','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+n+'.py'))]))
commands += [('browser',[sys.executable,str(R/'verify_browser.py')]),('extended',[sys.executable,str(R/'verify_extended.py')])]
results=[]
for name,cmd in commands:
 p=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf8',errors='replace');(R/(name+'-output.txt')).write_text(p.stdout+p.stderr,encoding='utf8')
 print(name.upper(), 'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if name=='build':print(p.stdout.strip(),flush=True)
 results.append({'check':name,'exit_code':p.returncode,'command':cmd})
 if p.returncode:print(p.stdout+p.stderr);raise SystemExit(p.returncode)
negative=[BLENDER,'--background','--threads','2','--factory-startup','--python-exit-code','1','--python',str(R/'verify_theme_source.py'),'--','--negative']
p=subprocess.run(negative,cwd=R,capture_output=True,text=True,encoding='utf8',errors='replace');(R/'negative-control-output.txt').write_text(p.stdout+p.stderr,encoding='utf8')
assert p.returncode!=0 and 'Expected 3 real dune ridges' in p.stdout+p.stderr,'Negative control failed to reject missing ridge'
print('NEGATIVE CONTROL PASS: missing ridge rejected',flush=True)
results.append({'check':'negative missing ridge','expected_nonzero':True,'exit_code':p.returncode})
hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['namibia.blend','namibia.glb','namibia-v1.html']}
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks':results,'asset_sha256':hashes},indent=2),encoding='utf8')
print('ALL ACCEPTANCE CHECKS PASS')
