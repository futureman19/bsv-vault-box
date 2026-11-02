from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
node=os.environ.get('NODE','C:/Program Files/nodejs/node.exe')
commands=[[sys.executable,str(R/'build.py')],[node,'--test',str(R/'tests.mjs')]]
commands += [[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/f)] for f in ['verify_source.py','verify_parity.py','verify_theme.py']]
commands += [[sys.executable,str(R/f)] for f in ['verify_browser.py','verify_extended.py']]
result=[]
for i,cmd in enumerate(commands):
 p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf8',errors='replace');(R/('gate-'+str(i)+'.txt')).write_text(p.stdout+p.stderr,encoding='utf8');result.append(dict(command=cmd,exit_code=p.returncode));print(Path(cmd[-1]).name,'PASS' if p.returncode==0 else 'FAIL',flush=True)
 if p.returncode:print(p.stdout+p.stderr);raise SystemExit(p.returncode)
(R/'acceptance-check.json').write_text(json.dumps(dict(status='PASS',checks=result),indent=2));print('ALL ACCEPTANCE CHECKS PASS')
