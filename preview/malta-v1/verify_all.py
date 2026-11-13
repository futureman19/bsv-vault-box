from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
commands=[('build',[sys.executable,'build.py']),('motion',['node','--test','tests.mjs'])]
for n in ['source','parity','theme_source']:commands.append((n,[blender,'--background','--factory-startup','--python-exit-code','1','--python','verify_'+n+'.py']))
for n in ['browser','extended']:commands.append((n,[sys.executable,'verify_'+n+'.py']))
out=[]
for name,cmd in commands:
 p=subprocess.run(cmd,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(R/(name+'-verification.log')).write_bytes(p.stdout);print(name, 'PASS' if p.returncode==0 else 'FAIL',flush=True);out.append(dict(check=name,exit_code=p.returncode));
 if p.returncode:print(p.stdout.decode(errors='replace'));raise SystemExit(p.returncode)
(R/'acceptance-check.json').write_text(json.dumps(dict(status='PASS',checks=out),indent=2));print('ALL ACCEPTANCE CHECKS PASS')
