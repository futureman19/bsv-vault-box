from pathlib import Path
import subprocess,json,sys
R=Path(__file__).resolve().parents[2];D=R/'launch/attachment-rim-repairs/finish';blender='C:/Users/futur/AppData/Local/Programs/Blender-5.2.1/blender.exe'
for row in json.loads((D/'targets.json').read_text()):
 slug=row['id']
 if slug=='iceland':continue
 root=R/'preview'/f'{slug}-repair-v2'
 for stage in ['preservation','contacts']:
  with (root/f'finish-{stage}-output.txt').open('w') as f:
   subprocess.run([blender,'--background','--factory-startup','--python-exit-code','1','--python',str(R/'launch/attachment-rim-repairs'/f'finish_{stage}.py'),'--',slug],cwd=R,stdout=f,stderr=subprocess.STDOUT,check=True)
 print(slug,'PASS',flush=True)
