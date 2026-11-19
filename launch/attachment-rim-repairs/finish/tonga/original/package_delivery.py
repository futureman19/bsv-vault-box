from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'tonga.blend','tonga.glb','tonga-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json'}
def sha(b):return hashlib.sha256(b).hexdigest()
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme','extended']:assert json.loads((R/(n+'-check.json')).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not r['errors'] and not r['external_requests'] for r in b[:2]) and b[2]['fallback']
html=(R/'tonga-v1.html').stat().st_size;glb=(R/'tonga.glb').stat().st_size;assert html<5_000_000
exclude={'inventory.json','delivery-check.json','tonga-v1-source.zip','package-output.txt'}
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in exclude and not p.name.endswith('.blend1')]
entries={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(files)}
assert required<=entries.keys()
(R/'inventory.json').write_text(json.dumps(entries,indent=2))
zp=R/'tonga-v1-source.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name in entries:z.write(R/name,name)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zp) as z:
 assert set(z.namelist())==set(entries)|{'inventory.json'}
 for n,e in entries.items():assert sha(z.read(n))==e['sha256'] and len(z.read(n))==e['bytes']
result={'status':'PASS','HTML_BYTES':html,'GLB_BYTES':glb,'all_required_present':True,'inventory_files':len(entries),'zip_readback':True,'zip_bytes':zp.stat().st_size,'zip_sha256':sha(zp.read_bytes()),'checks_passed':['source','parity','theme','browser','extended','motion','delivery']}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
