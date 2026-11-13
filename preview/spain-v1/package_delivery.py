from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','verify-all-log.txt','package-log.txt'}
def digest(b):return hashlib.sha256(b).hexdigest()
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and p.suffix not in ['.zip','.blend1'])
required={'spain-v1.html','spain.glb','spain.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','verification-check.json','maps/clay-color.png','maps/ceramic-pattern.png','maps/glaze-roughness.png','maps/ivory-color.png','.gitattributes','THREE-LICENSE.txt'}
records={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files}
assert required<=set(records),required-set(records)
assert records['spain-v1.html']['bytes']<5_000_000
assert json.loads((R/'verification-check.json').read_text())['status']=='PASS'
(R/'inventory.json').write_text(json.dumps(records,indent=2),encoding='utf8')
zpath=R/'spain-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(records)|{'inventory.json'}
 for n,record in records.items():
  data=z.read(n);assert len(data)==record['bytes'] and digest(data)==record['sha256'],n
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
result={'status':'PASS','html_bytes':records['spain-v1.html']['bytes'],'glb_bytes':records['spain.glb']['bytes'],'inventory_files':len(records),'required_artifacts_present':True,'archive_readback_all_hashes_match':True,'archive_bytes':zpath.stat().st_size,'archive_sha256':digest(zpath.read_bytes()),'inventory_sha256':digest((R/'inventory.json').read_bytes()),'excludes':['node_modules','__pycache__','blend backups','self-referential inventory/delivery/archive','active orchestration logs']}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
