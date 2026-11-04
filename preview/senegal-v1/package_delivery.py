from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'design-brief.md','README.md','senegal-v1.html','senegal.glb','senegal.blend','mechanism.blend','poster.png','poster.jpg','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-output.txt','author.py','maps.py','viewer.js','template.html','THREE-LICENSE.txt'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt']}
assert required<=files.keys(),required-files.keys()
assert (R/'senegal-v1.html').stat().st_size<5000000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
parity=json.loads((R/'parity-check.json').read_text());assert parity['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert len(browser)==3 and all(not a['errors'] and not a['external_requests'] and a['reduced_motion'] for a in browser[:2]) and browser[2]['fallback']
def sha(b):return hashlib.sha256(b).hexdigest()
inv={n:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'senegal-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for n,p in files.items():out.write(p,n)
 out.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as inp:
 assert set(inp.namelist())==set(files)|{'inventory.json'}
 for n,v in inv.items():
  b=inp.read(n);assert len(b)==v['bytes'] and sha(b)==v['sha256'],n
out={'status':'PASS','html_bytes':(R/'senegal-v1.html').stat().st_size,'glb_bytes':(R/'senegal.glb').stat().st_size,'payload_files':len(files),'required_files_present':True,'archive_readback_hashes_match':True,'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'checks_passed':['source','hinge-attachment','parity','theme-negative-control','motion','offline-desktop','offline-mobile','corrupt-GLB-fallback','no-JS-fallback','decoded-maps','country-copy','delivery']}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
