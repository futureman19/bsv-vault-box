from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','angola-v1-source.zip'}
def digest(b):return hashlib.sha256(b).hexdigest()
files=[p for p in R.rglob('*') if p.is_file() and not any(x in ('node_modules','__pycache__') for x in p.relative_to(R).parts) and p.name not in excluded and not p.name.endswith('.blend1') and not p.name.startswith('.hermes-tmp')]
required={'angola-v1.html','angola.glb','angola.blend','mechanism.blend','design-brief.md','README.md','poster.png','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
names={p.relative_to(R).as_posix() for p in files};assert required<=names
assert (R/'angola-v1.html').stat().st_size<5000000
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(files)}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
zpath=R/'angola-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==names|{'inventory.json'}
 for n,m in inventory.items():
  b=z.read(n);assert len(b)==m['bytes'] and digest(b)==m['sha256'],n
result={'status':'PASS','html_bytes':(R/'angola-v1.html').stat().st_size,'glb_bytes':(R/'angola.glb').stat().st_size,'inventory_files':len(inventory),'archive_entries':len(inventory)+1,'required_files_present':True,'archive_hash_readback':True,'zip_bytes':zpath.stat().st_size,'zip_sha256':digest(zpath.read_bytes()),'exclusions':['node_modules','blend1 backups','temporary files','inventory and delivery envelopes excluded from self-hashes']}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
