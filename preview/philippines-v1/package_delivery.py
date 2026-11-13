from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
files=[p for p in R.rglob('*') if p.is_file() and not any(s in p.parts for s in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json']]
required={'philippines-v1.html','philippines.glb','philippines.blend','poster.png','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','README.md','motion-local-output.txt'}
assert required <= {p.name for p in files}
def sha(b):return hashlib.sha256(b).hexdigest()
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(files)}
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
zpath=R/'philippines-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inventory)|{'inventory.json'}
 for n,v in inventory.items():assert len(z.read(n))==v['bytes'] and sha(z.read(n))==v['sha256']
h=(R/'philippines-v1.html').stat().st_size;g=(R/'philippines.glb').stat().st_size
assert h<5_000_000
r=dict(status='PASS',HTML_BYTES=h,GLB_BYTES=g,ZIP_BYTES=zpath.stat().st_size,ZIP_entries=len(inventory)+1,archive_readback_verified=True,required_artifacts_verified=True,zip_sha256=sha(zpath.read_bytes()),inventory_sha256=sha((R/'inventory.json').read_bytes()))
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
