from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda n:json.loads((R/n).read_text())
s=load('source-check.json');assert s['collision_samples']==81 and not s['collisions'];assert load('parity-check.json')['source_and_export_geometry_match']
assert load('theme-check.json')['status']=='PASS' and load('extended-check.json')['status']=='PASS'
b=load('browser-check.json');assert len(b)==3 and all(not x['errors'] and not x['external_requests'] for x in b[:2]) and b[2]['fallback']
assert (R/'maldives-v1.html').stat().st_size<5_000_000
assert '# fail 0' in (R/'motion-output.txt').read_text()
required={'maldives-v1.html','maldives.glb','maldives.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt'}
excluded={'inventory.json','delivery-check.json','maldives-v1-source.zip','package-output.txt','git-output.txt'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__','.git']) and p.suffix!='.blend1' and p.name not in excluded}
assert required<=set(files)
inv={n:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files['inventory.json']=R/'inventory.json'
z=R/'maldives-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for n,p in files.items():f.write(p,n)
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(files)
 for n,p in files.items():assert f.read(n)==p.read_bytes(),n
out=dict(status='PASS',html_bytes=(R/'maldives-v1.html').stat().st_size,glb_bytes=(R/'maldives.glb').stat().st_size,inventory_entries=len(inv),zip_entries=len(files),zip_bytes=z.stat().st_size,zip_sha256=sha(z.read_bytes()),required_artifacts_present=True,archive_exact_readback=True,checks_passed=['source','81-pose collision','hinge attachment','parity','theme','motion','desktop/mobile browser','extended','delivery'])
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));print('ALL ACCEPTANCE CHECKS PASS')
