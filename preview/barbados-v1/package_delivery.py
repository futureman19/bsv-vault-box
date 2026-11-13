from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'barbados-v1.html','barbados.glb','barbados.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','motion-check.json'}
assert all((R/n).is_file() for n in required)
assert (R/'barbados-v1.html').stat().st_size<5000000
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for n in ['theme','extended','motion']:assert json.loads((R/(n+'-check.json')).read_text())['status']=='PASS'
files=sorted(p for p in R.rglob('*') if p.is_file() and p.suffix not in {'.zip','.blend1','.pyc'} and not {'node_modules','__pycache__'}.intersection(p.relative_to(R).parts) and p.name not in {'inventory.json','delivery-check.json','package-output.txt'})
def sha(b):return hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'barbados-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert required<=set(a.namelist());assert len(a.namelist())==len(files);assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r={'status':'PASS','HTML_BYTES':(R/'barbados-v1.html').stat().st_size,'GLB_BYTES':(R/'barbados.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_entries':len(inv),'required_artifacts_included':True,'archive_readback_verified':True,'scope':'local folder; no external delivery copy'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
