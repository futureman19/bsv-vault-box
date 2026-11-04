from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
excluded={'inventory.json','delivery-check.json','nepal-v1-source.zip','package-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and not p.name.endswith('.blend1'))
required={'nepal.blend','nepal.glb','nepal-v1.html','poster.png','poster.jpg','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json'}
assert required.issubset({p.relative_to(R).as_posix() for p in files})
assert (R/'nepal-v1.html').stat().st_size<5000000
assert json.loads((R/'source-check.json').read_text())['collisions']==[]
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert json.loads((R/'theme-negative.json').read_text())['status']=='FAIL'
assert '# fail 0' in (R/'motion-output.txt').read_text()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'nepal-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for name,v in inv.items():assert len(z.read(name))==v['bytes'] and sha(z.read(name))==v['sha256'],name
result={'status':'PASS','html_bytes':(R/'nepal-v1.html').stat().st_size,'glb_bytes':(R/'nepal.glb').stat().st_size,'inventory_files':len(inv),'archive_bytes':zpath.stat().st_size,'archive_sha256':sha(zpath.read_bytes()),'required_artifacts_verified':sorted(required),'archive_readback':'every entry exact hash and byte count','exclusions':'dependencies, backups, caches; envelope manifests excluded from own inventory'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
