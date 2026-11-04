from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'design-brief.md','README.md','azerbaijan.blend','azerbaijan.glb','azerbaijan-v1.html','poster.png','poster.jpg','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt'}
assert all((R/n).is_file() for n in required)
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3 and all(not x['errors'] and not x['external_requests'] for x in b[:2]) and b[2]['fallback']
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert (R/'azerbaijan-v1.html').stat().st_size<5000000
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip'] and p.name not in ['inventory.json','delivery-check.json','pack-output.txt','git-verification.json'])
assert required<={p.relative_to(R).as_posix() for p in files}
sha=lambda data:hashlib.sha256(data).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'azerbaijan-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files};assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':(R/'azerbaijan-v1.html').stat().st_size,'GLB_BYTES':(R/'azerbaijan.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_entries':len(inv),'archive_entries':len(files),'required_artifacts_present':True,'archive_exact_readback':True,'checks_passed':['source','parity','theme','motion','desktop_file','mobile_file','corrupt_GLB_fallback','noJS_fallback','texture_channels','size','SHA256_inventory','archive_readback']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
