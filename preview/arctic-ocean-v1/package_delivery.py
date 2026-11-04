from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'arctic.blend','arctic.glb','arctic-ocean-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','author.py','mechanism.blend'}
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme','extended']:assert json.loads((R/(n+'-check.json')).read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not c.get('errors',[]) and not c.get('external_requests',[]) for c in b)
assert (R/'arctic-ocean-v1.html').stat().st_size<5000000
excluded={'inventory.json','delivery-check.json','package-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in excluded)
names={p.relative_to(R).as_posix() for p in files};assert required<=names
sha=lambda data:hashlib.sha256(data).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'arctic-ocean-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert len(a.namelist())==len(files) and required<=set(a.namelist()) and a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
out=dict(status='PASS',HTML_BYTES=(R/'arctic-ocean-v1.html').stat().st_size,GLB_BYTES=(R/'arctic.glb').stat().st_size,ZIP_BYTES=z.stat().st_size,ZIP_SHA256=sha(z.read_bytes()),inventory_entries=len(inv),archive_entries=len(files),exact_inventory_readback=True,explicit_required_artifacts=True)
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
