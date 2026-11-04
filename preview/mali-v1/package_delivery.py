from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','mali-v1-source.zip','packaging-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in {'node_modules','__pycache__'} for x in p.relative_to(R).parts) and p.name not in excluded and p.suffix!='.blend1')
required={'mali.blend','mali.glb','mali-v1.html','poster.png','poster.jpg','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-source-check.json','author.py','maps.py','build.py','run_checks.py','THREE-LICENSE.txt'}
names={p.relative_to(R).as_posix() for p in files};assert required<=names,required-names
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert inventory['mali-v1.html']['bytes']<5_000_000
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
with zipfile.ZipFile(R/'mali-v1-source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(R/'mali-v1-source.zip') as z:
 assert set(z.namelist())==names|{'inventory.json'}
 for n,item in inventory.items():assert hashlib.sha256(z.read(n)).hexdigest()==item['sha256']
out={'status':'PASS','html_bytes':inventory['mali-v1.html']['bytes'],'glb_bytes':inventory['mali.glb']['bytes'],'inventory_count':len(files),'required_artifacts':sorted(required),'archive_readback_verified':True,'archive_bytes':(R/'mali-v1-source.zip').stat().st_size,'archive_sha256':hashlib.sha256((R/'mali-v1-source.zip').read_bytes()).hexdigest(),'inventory_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest()}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
