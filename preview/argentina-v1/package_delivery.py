from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','argentina-v1-source.zip','package-log.txt','git-evidence.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and 'node_modules' not in p.parts and '__pycache__' not in p.parts and not p.name.endswith('.blend1'))
def sha(b):return hashlib.sha256(b).hexdigest()
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
required={'argentina.blend','argentina.glb','argentina-v1.html','design-brief.md','README.md','poster.png','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json'}
assert required<=inventory.keys()
assert inventory['argentina-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
zpath=R/'argentina-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inventory)|{'inventory.json'}
 for name,meta in inventory.items():assert sha(z.read(name))==meta['sha256']
r={'status':'PASS','html_bytes':inventory['argentina-v1.html']['bytes'],'glb_bytes':inventory['argentina.glb']['bytes'],'inventory_files':len(inventory),'archive_bytes':zpath.stat().st_size,'archive_sha256':sha(zpath.read_bytes()),'required_artifacts_present':True,'archive_readback_hashes_match':True,'excludes':'dependencies, caches, blend backups, self-referential manifests/logs'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
