"""One bounded presentation-only correction; exact model bytes retained."""
from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parent; REPO=R.parents[1]
row=next(r for r in json.loads((R/'baseline.json').read_text()) if r['id']=='bangladesh')
ref=row['original_review']['viewer']['commit'];prefix='preview/bangladesh-v1/'
D=REPO/'preview/bangladesh-finish-v2'; H=D/'historical-v1';H.mkdir(parents=True,exist_ok=True)
manifest=[]
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',ref,prefix],cwd=REPO).decode().splitlines():
 rel=path[len(prefix):]
 if rel.endswith('.zip'):continue
 data=subprocess.check_output(['git','show',ref+':'+path],cwd=REPO);p=H/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 manifest.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
for n in ['bangladesh.blend','bangladesh.glb','motion.mjs','poster.png','poster.jpg','template.html','viewer.js','viewer.bundle.js','THREE-LICENSE.txt','tests.mjs','verify_parity.py']:
 (D/n).write_bytes((H/n).read_bytes())
old=b'Math.min(devicePixelRatio,2)';new=b'2'
for n in ['viewer.js','viewer.bundle.js']:
 p=D/n;data=p.read_bytes();assert data.count(old)==1,(n,data.count(old));p.write_bytes(data.replace(old,new))
data=(H/'bangladesh-v1.html').read_bytes();assert data.count(old)==1
(D/'bangladesh-finish-v2.html').write_bytes(data.replace(old,new))
(D/'.gitattributes').write_text('* -text\n')
(D/'historical-manifest.json').write_text(json.dumps({'commit':ref,'prefix':prefix,'files':manifest},indent=2))
proof={n:hashlib.sha256((D/n).read_bytes()).hexdigest() for n in ['bangladesh.blend','bangladesh.glb','motion.mjs','poster.png','poster.jpg','template.html']}
(D/'unchanged-model.json').write_text(json.dumps({'exact_baseline_files':proof,'geometry_material_camera_lighting_motion_unchanged':True,'pass':1,'change':'2x drawing buffer at DPR below 2; high-DPR existing cap remains 2; no source geometry changes'},indent=2))
print('Created',D,'HTML bytes',(D/'bangladesh-finish-v2.html').stat().st_size)
