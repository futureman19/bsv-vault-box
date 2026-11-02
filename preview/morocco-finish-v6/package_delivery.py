from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,shutil
from glb_tools import load,view
R=Path(__file__).resolve().parent
D=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-morocco-finish-v6');D.mkdir(parents=True,exist_ok=True)
# Expose every packed original texture as editable source alongside the new maps.
j,b=load(R/'baseline/morocco.glb')
for im in j['images']:
 name=im['name'];name=name if name.endswith(('.png','.jpg')) else name+('.png' if im['mimeType']=='image/png' else '.jpg');(R/'maps'/name).write_bytes(view(j,b,im['bufferView']))
visual={'status':'partial visual acceptance; not user-approved','body':'approved strata preserved; modest darkening, not crushed','edge':'lighter warm grain; stronger/coarser than reference, top unchanged','ceramic':'continuous carrier fixed fragmentation; rendered pattern still too pale/open, weaker interlock and imperfect corners','correction_count':1,'further_iterations':False,'non_target':'hardware, ridge, dimensions, choreography unchanged'}
(R/'visual-review.json').write_text(json.dumps(visual,indent=2))
required={'morocco-finish-v6.html','morocco.glb','morocco.blend','poster.jpg','poster.png','author.py','materials.py','finalize_glb.py','glb_tools.py','build.py','viewer.js','viewer.bundle.js','motion.mjs','template.html','package.json','THREE-LICENSE.txt','README.md','baseline/morocco.glb','baseline/morocco.blend','references/primary.png','maps/cedar-edge.jpg','maps/ceramic-atlas.png','maps/tile-repeat.png','maps/reference-color.png','maps/reference-normal.png','maps/reference-orm.png','reference-comparison.jpg','lid-comparison.jpg','finish-check.json','browser-check.json','source-check.json','parity-check.json','source-preservation-check.json','fallback-check.json','extended-check.json','visual-review.json'}
allowed={'.html','.glb','.blend','.py','.json','.jpg','.png','.js','.mjs','.txt','.md'}
files=[]
for p in R.rglob('*'):
 if not p.is_file() or p.suffix not in allowed:continue
 rel=p.relative_to(R).as_posix()
 if any(x in p.parts for x in ['node_modules','__pycache__']):continue
 if rel in ['inventory.json','delivery-check.json','delivery-open-check.json','target-export.glb']:continue
 if rel.startswith('pre-correction/') and p.suffix in {'.html','.glb'}:continue
 files.append(p)
paths={p.relative_to(R).as_posix() for p in files};assert required<=paths,required-paths
for rel in paths:assert not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts
records={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
manifest={'required_files':sorted(required),'files':records,'exclusions':['node_modules','__pycache__','blend backups','pre-correction HTML/GLB','intermediate target export'],'final_html_bytes':(R/'morocco-finish-v6.html').stat().st_size,'final_glb_bytes':(R/'morocco.glb').stat().st_size}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
zpath=R/'morocco-finish-v6-source.zip'
with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert required<=set(z.namelist());assert z.testzip() is None
 for rel,r in records.items():assert hashlib.sha256(z.read(rel)).hexdigest()==r['sha256']
# Deliver full safe editable inventory, plus ZIP; compare every copied byte.
checks={}
for p in files+[zpath]:
 dest=D/p.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);ha=hashlib.sha256(p.read_bytes()).hexdigest();assert hashlib.sha256(dest.read_bytes()).hexdigest()==ha;checks[dest.relative_to(D).as_posix()]={'bytes':dest.stat().st_size,'sha256':ha}
result={'delivery':str(D),'copy_readback':True,'zip_readback':True,'required_inventory_verified':True,'copied_files':len(checks),'html_bytes':(D/'morocco-finish-v6.html').stat().st_size,'glb_bytes':(D/'morocco.glb').stat().st_size,'source_zip_bytes':(D/zpath.name).stat().st_size,'files':checks}
for folder in [R,D]:(folder/'delivery-check.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2))
