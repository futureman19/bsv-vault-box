from pathlib import Path
import json
from package_repairs import archive,recover,manifest,encode,sha
R=Path(__file__).resolve().parent;REPO=R.parents[1]
OUT=R/'deliveries';OUT.mkdir(exist_ok=True)
rows=[]
for folder,stem,html in [('united-states-flag-v10','united-states','united-states-flag-v10.html'),('cabo-verde-view-v2','cabo-verde','cabo-verde-view-v2.html'),('saint-vincent-and-the-grenadines-view-v2','saint-vincent-and-the-grenadines','saint-vincent-and-the-grenadines-view-v2.html')]:
 p=REPO/'preview'/folder
 files={f.relative_to(p).as_posix():f.read_bytes() for f in p.rglob('*') if f.is_file() and not any(x in ('node_modules','__pycache__') for x in f.relative_to(p).parts) and f.suffix not in ('.zip','.blend1','.pyc') and f.name!='inventory.json'}
 required=[html,stem+'.glb',stem+'.blend','README.md','viewer.js','motion.mjs']
 assert all(n in files for n in required);assert len(files[html])<5000000
 inv=encode({'version':1,'id':stem,'required':required,'files':manifest(files)})
 (p/'inventory.json').write_bytes(inv);files['inventory.json']=inv
 z=OUT/(folder+'-source.zip');archive(files,z)
 recovered=OUT/(folder+'-recovered');check=recover(z,sha(inv),recovered)
 rows.append({'id':stem,'folder':folder,'html':html,'html_bytes':len(files[html]),'glb_bytes':len(files[stem+'.glb']),'source_zip_bytes':z.stat().st_size,'source_zip_sha256':sha(z.read_bytes()),'inventory_sha256':sha(inv),'recovery':check})
(R/'art-delivery.json').write_bytes(encode(rows));print(json.dumps(rows,indent=2))
