"""Exact-byte local delivery inventory and ZIP, no external writes."""
from pathlib import Path
import hashlib,json,zipfile,sys
R=Path(__file__).resolve().parent
ZIP='namibia-v1-source.zip';excluded={'inventory.json','delivery-check.json',ZIP}
required={'.gitattributes','tests.mjs','package_delivery.py','design-brief.md','README.md','namibia.blend','namibia.glb','namibia-v1.html','mechanism.blend','poster.png','poster.jpg','author.py','maps.py','build.py','viewer.js','viewer.bundle.js','motion.mjs','template.html','run_checks.py','verify_source.py','verify_parity.py','verify_theme_source.py','verify_browser.py','verify_extended.py','source-check.json','parity-check.json','theme-source-check.json','browser-check.json','extended-check.json','acceptance-check.json','negative-control-output.txt','verification-output.txt','visual-check.json','THREE-LICENSE.txt','package.json','maps/sand-color.png','maps/sand-normal.png','maps/sand-roughness.png','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','desktop-open-rear.png'}
def identity(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def payload():
 return sorted(p for p in R.rglob('*') if p.is_file() and p.relative_to(R).as_posix() not in excluded and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.pyc'])
def verify():
 inv=json.loads((R/'inventory.json').read_text());names=set(inv['files']);assert required<=names,sorted(required-names)
 assert names=={p.relative_to(R).as_posix() for p in payload()},'Payload set changed'
 for n,item in inv['files'].items():assert identity((R/n).read_bytes())==item,n
 with zipfile.ZipFile(R/ZIP) as z:
  assert len(z.namelist())==len(set(z.namelist()))
  assert set(z.namelist())==names|{'inventory.json'}
  for n in z.namelist():assert z.read(n)==(R/n).read_bytes(),n
 return inv
if '--verify' not in sys.argv:
 files={p.relative_to(R).as_posix():identity(p.read_bytes()) for p in payload()};assert required<=set(files),sorted(required-set(files))
 acceptance=json.loads((R/'acceptance-check.json').read_text());assert acceptance['status']=='PASS'
 for n,h in acceptance['asset_sha256'].items():assert files[n]['sha256']==h,('Stale acceptance',n)
 assert files['namibia-v1.html']['bytes']<5_000_000
 (R/'inventory.json').write_text(json.dumps({'algorithm':'SHA-256','excluded_envelopes':sorted(excluded),'files':files},indent=2),encoding='utf8')
 with zipfile.ZipFile(R/ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n in sorted(set(files)|{'inventory.json'}):z.write(R/n,n)
 inv=verify()
 out={'status':'PASS','HTML_BYTES':files['namibia-v1.html']['bytes'],'GLB_BYTES':files['namibia.glb']['bytes'],'inventory_files':len(files),'ZIP_ENTRIES':len(files)+1,'zip':identity((R/ZIP).read_bytes()),'inventory':identity((R/'inventory.json').read_bytes()),'archive_readback_verified':True,'required_artifacts_verified':sorted(required),'tested_delivery':'namibia-v1.html (same exact in-folder file tested over file://)'}
 (R/'delivery-check.json').write_text(json.dumps(out,indent=2),encoding='utf8')
else:
 inv=verify();out=json.loads((R/'delivery-check.json').read_text());assert out['zip']==identity((R/ZIP).read_bytes());assert out['inventory']==identity((R/'inventory.json').read_bytes())
print('DELIVERY PASS',json.dumps({k:out[k] for k in ['HTML_BYTES','GLB_BYTES','inventory_files','ZIP_ENTRIES','zip']}))
