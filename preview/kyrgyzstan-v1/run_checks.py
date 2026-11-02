"""Rebuild offline viewer and independently recheck all acceptance gates.
Run author.py separately to regenerate the packed source/model/poster.
"""
from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parent
blender=os.environ.get('BLENDER_EXE','C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe')
commands=[('build',[sys.executable,str(R/'build.py')]),('motion',['node','--test',str(R/'tests.mjs')])]
for name in ['source','parity','theme']:
 commands.append((name,[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/('verify_'+name+'.py'))]))
for name in ['browser','extended']:
 commands.append((name,[sys.executable,str(R/('verify_'+name+'.py'))]))
results=[]
for name,cmd in commands:
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/(name+'-output.txt')).write_bytes(p.stdout)
 print(name.upper(), 'PASS' if p.returncode==0 else 'FAIL',flush=True)
 results.append({'gate':name,'exit_code':p.returncode})
 if p.returncode:
  print(p.stdout.decode(errors='replace'));sys.exit(p.returncode)
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','gates':results},indent=2))
print('ALL ACCEPTANCE CHECKS PASS',flush=True)
