"""Canonical bounded verification runner; every PASS requires exit code zero."""
from pathlib import Path
import subprocess,json,os
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER_EXE','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
node=os.environ.get('NODE_EXE','C:/Program Files/nodejs/node.exe')
commands=[('build',['python',str(R/'build.py')])]
for name in ['verify_source','verify_parity','test_theme']:
 commands.append((name,[blender,'--background','--factory-startup','--threads','2','--python-exit-code','1','--python',str(R/(name+'.py'))]))
commands += [('motion',[node,'--test',str(R/'tests.mjs')]),('browser',['python',str(R/'verify_browser.py')]),('extended',['python',str(R/'verify_extended.py')])]
results=[]
for name,cmd in commands:
 result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace');(R/(name+'-output.txt')).write_text(result.stdout+result.stderr,encoding='utf-8')
 results.append({'check':name,'exit_code':result.returncode,'status':'PASS' if result.returncode==0 else 'FAIL'})
 if result.returncode:
  (R/'verification-check.json').write_text(json.dumps(results,indent=2));print(result.stdout,result.stderr);raise SystemExit(result.returncode)
 print(name.upper(),'PASS')
(R/'verification-check.json').write_text(json.dumps(results,indent=2));print('ALL VERIFICATION CHECKS PASS')
