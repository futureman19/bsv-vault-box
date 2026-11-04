"""Exact deliverable manifest and ZIP readback; no external storage operations."""
from pathlib import Path
import hashlib,json,zipfile,base64,re
R=Path(__file__).resolve().parent
HTML='central-african-republic-v1.html';GLB='central-african-republic.glb';ZIP='central-african-republic-v1-source.zip'
required={HTML,GLB,'central-african-republic.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','author.py','maps.py','build.py','verify_all.py','package_delivery.py','source-check.json','parity-check.json','browser-check.json','theme-check.json','maps-check.json','extended-check.json','acceptance.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','desktop-open-rear.png','mobile-nojs.png','mobile-fallback.png','THREE-LICENSE.txt','maps/timber-color.png','maps/timber-normal.png','maps/timber-roughness.png'}
excluded={'inventory.json','delivery-check.json',ZIP,'lane-prompt.txt'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and p.name not in excluded and p.suffix not in ['.blend1','.pyc'] and not any(x in p.parts for x in ['node_modules','__pycache__','.git'])}
assert required<=files.keys(), sorted(required-files.keys())
def entry(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert files[HTML].stat().st_size<5_000_000
html=files[HTML].read_text(encoding='utf8');embedded=re.search(r'<script id="asset" type="application/octet-stream">(.*?)</script>',html,re.S).group(1)
assert base64.b64decode(embedded)==files[GLB].read_bytes()
assert all(x['status']=='PASS' and x['exit_code']==0 for x in json.loads((R/'acceptance.json').read_text()))
inv={n:entry(p) for n,p in sorted(files.items())};(R/'inventory.json').write_text(json.dumps(inv,indent=2))
with zipfile.ZipFile(R/ZIP,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(R/ZIP) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for n,e in inv.items():
  b=z.read(n);assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],n
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
result={'status':'PASS','html_bytes':inv[HTML]['bytes'],'glb_bytes':inv[GLB]['bytes'],'embedded_glb_exact':True,'required_artifacts_present':sorted(required),'hashed_payload_files':len(inv),'archive_entries':len(inv)+1,'zip_readback':'all entries matched bytes and SHA-256','inventory':entry(R/'inventory.json'),'source_zip':entry(R/ZIP),'envelope_exclusions':sorted(excluded),'not_uploaded_or_minted':True}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print('delivery PASS');print('HTML_BYTES',inv[HTML]['bytes'],'GLB_BYTES',inv[GLB]['bytes']);print('ZIP_BYTES',result['source_zip']['bytes']);print('HASHED_FILES',len(inv))
