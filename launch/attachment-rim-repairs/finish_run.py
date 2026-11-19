import subprocess,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'launch/attachment-rim-repairs/finish';blender='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
for row in json.loads((D/'targets.json').read_text()):
 slug=row['id']
 if slug=='iceland':continue
 root=R/'preview'/f'{slug}-repair-v2'
 steps=[('repair',[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/'launch/attachment-rim-repairs/finish_repair.py'),'--',slug]),('source',[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(root/'verify_source.py')]),('parity',[blender,'--background','--factory-startup','--python-exit-code','1','--python',str(root/'verify_parity.py')]),('build',[sys.executable,str(root/'build.py')]),('browser',[sys.executable,str(root/'verify_browser.py')])]
 for stage,cmd in steps:
  log=root/f'finish-{stage}-output.txt'
  assert not log.exists(),('Refuse overwriting evidence',log)
  with log.open('w') as f:result=subprocess.run(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT)
  print(slug,stage,result.returncode,flush=True)
  if result.returncode:sys.exit(result.returncode)
