from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
SKIP={'inventory.json','delivery-check.json','vatican-city-v1-source.zip','delivery-output.txt','git-output.txt'}
def digest(b):return hashlib.sha256(b).hexdigest()
def validate_size(n):assert 0<n<5_000_000,'Standalone HTML budget exceeded'
html=R/'vatican-city-v1.html';glb=R/'vatican-city.glb';validate_size(html.stat().st_size)
try:validate_size(5_000_000);raise RuntimeError('size negative not rejected')
except AssertionError:pass
required={'design-brief.md','README.md','vatican-city.blend','vatican-city.glb','vatican-city-v1.html','poster.png','poster.jpg','mechanism.blend','author.py','maps.py','build.py','viewer.js','motion.mjs','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','.gitattributes','package-lock.json'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not {'node_modules','__pycache__'}.intersection(p.relative_to(R).parts) and p.name not in SKIP and not p.name.endswith(('.blend1','.pyc'))}
assert required<=files.keys(),required-files.keys()
inv={n:{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'vatican-city-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for n,p in sorted(files.items()):z.write(p,n)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for n,m in inv.items():
  b=z.read(n);assert len(b)==m['bytes'] and digest(b)==m['sha256'],n
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
out={'status':'PASS','html_bytes':html.stat().st_size,'glb_bytes':glb.stat().st_size,'html_sha256':digest(html.read_bytes()),'glb_sha256':digest(glb.read_bytes()),'inventory_entries':len(inv),'zip_bytes':zpath.stat().st_size,'zip_sha256':digest(zpath.read_bytes()),'zip_readback_all_hashes_match':True,'required_artifacts_present':sorted(required),'size_boundary_negative_rejected':True,'note':'inventory excludes itself and packaging envelopes/output logs to avoid self-reference; all files remain within this preview'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('DELIVERY PASS');print('HTML_BYTES',out['html_bytes'],'GLB_BYTES',out['glb_bytes']);print('ZIP_BYTES',out['zip_bytes'],'INVENTORY_FILES',len(inv))
