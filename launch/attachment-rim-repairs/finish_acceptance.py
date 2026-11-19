"""Additive final comparisons and isolated original motion suites; no asset authoring."""
from pathlib import Path
import json,hashlib,shutil,subprocess
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'launch/attachment-rim-repairs/finish';O=D/'acceptance';O.mkdir(exist_ok=True)
rows=json.loads((D/'progress.json').read_text())['records'];reports=[]
node=shutil.which('node.exe') or shutil.which('node')
for row in rows:
 s=row['id'];root=(R/row['candidate']).parent;out=O/s;out.mkdir(exist_ok=True)
 before=D/s/'before';after=root if s!='iceland' else D/s/'original'
 boards=[]
 for mode in ['desktop','mobile']:
  for state in ['closed','open']:
   name=f'{mode}-{state}.png';paths=[before/name,after/name];labels=['Immutable original','Final candidate' if s!='iceland' else 'Unchanged current candidate']
   if s=='panama':paths=[before/name,root/'pass1'/name,after/name];labels=['Original camera','Pass 1: same-camera rim repair','Final: raised camera (pass 2)']
   images=[Image.open(p).convert('RGB') for p in paths];assert len({im.size for im in images})==1
   w,h=images[0].size;board=Image.new('RGB',(w*len(images),h+50),'#eee8df');draw=ImageDraw.Draw(board)
   for i,(im,label) in enumerate(zip(images,labels)):board.paste(im,(i*w,50));draw.text((i*w+12,12),s+' | '+label,fill='black')
   dest=out/f'comparison-{mode}-{state}.jpg';assert not dest.exists();board.save(dest,quality=92);boards.append(str(dest.relative_to(R)))
 motion=out/'motion';motion.mkdir();shutil.copyfile(root/'motion.mjs',motion/'motion.mjs')
 suites=[p for p in [root/'tests.mjs',root/'test_motion.mjs'] if p.exists()]
 reused=not suites
 if reused:suites=[R/'preview/afghanistan-repair-v2/tests.mjs']
 checks=[]
 for suite in suites:
  shutil.copyfile(suite,motion/suite.name)
  proc=subprocess.run([node,'--test','--test-reporter=tap',suite.name],cwd=motion,capture_output=True,text=True)
  (out/(suite.stem+'-output.txt')).write_text(proc.stdout+proc.stderr)
  assert proc.returncode==0 and '# fail 0' in proc.stdout,(s,proc.stdout,proc.stderr)
  checks.append({'suite':str(suite.relative_to(R)),'reused_contract_not_original_suite':reused,'exit_code':proc.returncode})
 reports.append({'id':s,'boards':boards,'motion_checks':checks,'viewer_bytes':(R/row['candidate']).stat().st_size,'viewer_sha256':hashlib.sha256((R/row['candidate']).read_bytes()).hexdigest()})
(O/'checks.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports,indent=2))
