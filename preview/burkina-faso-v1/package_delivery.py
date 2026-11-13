"""Hash exact delivery bytes; assert explicit artifact set and ZIP readback."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'README.md','design-brief.md','burkina-faso-v1.html','burkina-faso.glb','burkina-faso.blend','mechanism.blend','poster.png','poster.jpg','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','hinge-attachment-check.json','maps/earth-color.png','maps/earth-normal.png','maps/earth-roughness.png','author.py','build.py','maps.py','verify_source.py','verify_parity.py','verify_theme.py','verify_browser.py','verify_extended.py','motion.mjs','tests.mjs','viewer.js','viewer.bundle.js','template.html','package.json','THREE-LICENSE.txt','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','mobile-fallback.png','mobile-nojs.png','desktop-open-rear.png'}
exclude={'inventory.json','delivery-check.json','burkina-faso-source.zip'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and p.name not in exclude and not p.name.startswith('lane-') and p.suffix not in ['.blend1','.pyc'] and '__pycache__' not in p.parts and 'node_modules' not in p.parts}
assert required<=files.keys(),sorted(required-files.keys())
for f in ['source-check.json','parity-check.json','theme-check.json','extended-check.json']:assert json.loads(files[f].read_text())['status']=='PASS',f
assert all(c['status']=='PASS' for c in json.loads(files['browser-check.json'].read_text()))
html=files['burkina-faso-v1.html'].stat().st_size;glb=files['burkina-faso.glb'].stat().st_size;assert html<5_000_000
sha=lambda b:hashlib.sha256(b).hexdigest()
inv={k:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for k,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'burkina-faso-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for k,p in sorted(files.items()):z.write(p,k)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 assert required<=set(z.namelist())
 for k,v in inv.items():
  b=z.read(k);assert len(b)==v['bytes'] and sha(b)==v['sha256'],k
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
result={'status':'PASS','html_bytes':html,'glb_bytes':glb,'inventory_files':len(inv),'required_files':len(required),'all_required_present':True,'zip_readback_verified':True,'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'exclusions':['inventory and delivery reports and ZIP excluded from payload inventory to avoid circular hashes','lane diagnostics','caches','node_modules','blend backups']}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
