"""Hash exact deliverables and verify complete archive by readback."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
EXCLUDE={'inventory.json','delivery-check.json','eswatini-v1-source.zip'}
required={'eswatini-v1.html','eswatini.glb','eswatini.blend','mechanism.blend','poster.png','poster.jpg','author.py','maps.py','build.py','README.md','design-brief.md','viewer.js','viewer.bundle.js','motion.mjs','template.html','package.json','THREE-LICENSE.txt','maps/grass-color.png','maps/grass-roughness.png','maps/binding.png','source-check.json','parity-check.json','browser-check.json','theme-source-check.json','motion-check.json','extended-check.json'}
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and p.name not in EXCLUDE and not p.name.endswith(('.blend1','.pyc')) and not any(x in p.parts for x in ['node_modules','__pycache__'])}
assert required<=set(files),required-set(files)
assert (R/'eswatini-v1.html').stat().st_size<5_000_000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
parity=json.loads((R/'parity-check.json').read_text());assert parity['source_and_export_geometry_match'] and parity['source_to_glb_max']<1e-5
browser=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in browser}=={'desktop','mobile','corrupted GLB'}
for x in browser[:2]:
 assert x['asset']['bytes']==(R/'eswatini.glb').stat().st_size
 assert x['offline_file'] and not x['external_requests'] and not x['errors'] and x['reduced_motion'] and x['open_close'] and x['reset_mid_motion'] and not x['overflow']
 assert x['asset']['degenerate']==x['asset']['nonfinite']==0
for n in ['theme-source-check.json','motion-check.json','extended-check.json']:assert json.loads((R/n).read_text())['status']=='PASS'
inv={n:identity(p.read_bytes()) for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
files['inventory.json']=R/'inventory.json'
zpath=R/'eswatini-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)
 assert required<=set(z.namelist())
 for n,p in files.items():assert z.read(n)==p.read_bytes(),n
report={'status':'PASS','html':identity((R/'eswatini-v1.html').read_bytes()),'glb':identity((R/'eswatini.glb').read_bytes()),'zip':identity(zpath.read_bytes()),'archive_members':len(files),'required_artifacts':sorted(required),'exact_inventory_and_archive_readback':True,'checks':['source','parity','theme-source','motion','browser desktop/mobile/corruption','extended theme/no-JS','strict HTML budget','SHA-256 inventory','required archive contents/readback']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('DELIVERY PASS');print('HTML_BYTES',report['html']['bytes'],'GLB_BYTES',report['glb']['bytes']);print('ZIP_BYTES',report['zip']['bytes']);print('ALL ACCEPTANCE CHECKS PASS')
