from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
skip={'node_modules','__pycache__'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in skip for x in p.relative_to(R).parts) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json'])
required={'china-v1.html','china.glb','china.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-output.txt'}
assert required <= {p.relative_to(R).as_posix() for p in files}
assert (R/'china-v1.html').stat().st_size<5000000
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert '# fail 0' in (R/'motion-output.txt').read_text()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'china-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for name,item in inv.items():
  b=z.read(name);assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
out=dict(status='PASS',html_bytes=(R/'china-v1.html').stat().st_size,glb_bytes=(R/'china.glb').stat().st_size,archive_bytes=zpath.stat().st_size,archive_sha256=hashlib.sha256(zpath.read_bytes()).hexdigest(),inventoried_files=len(inv),required_artifacts_verified=sorted(required),zip_readback=True)
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
