from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required=['luxembourg-v1.html','luxembourg.glb','luxembourg.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','author.py','build.py','.gitattributes']
assert all((R/f).is_file() for f in required)
assert (R/'luxembourg-v1.html').stat().st_size<5_000_000
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {'desktop','mobile','corrupted GLB'}<={x['case'] for x in browser}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert set(required)<=inv.keys();(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'luxembourg-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for p in files+[R/'inventory.json']:out.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())==set(inv)|{'inventory.json'}
 for name,entry in inv.items():
  data=archive.read(name);assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
r=dict(status='PASS',html_bytes=(R/'luxembourg-v1.html').stat().st_size,glb_bytes=(R/'luxembourg.glb').stat().st_size,zip_bytes=z.stat().st_size,zip_sha256=hashlib.sha256(z.read_bytes()).hexdigest(),inventory_count=len(inv),required_artifacts_present=True,archive_readback=True)
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
