from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
assert json.loads((R/'acceptance-check.json').read_text())['status']=='PASS'
assert (R/'guatemala-v1.html').stat().st_size<5_000_000
exclude={'inventory.json','delivery-check.json','guatemala-v1-source.zip','acceptance-run.log'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(s in p.parts for s in ['node_modules','__pycache__']) and p.name not in exclude and p.suffix not in ['.blend1','.pyc'])
required={'guatemala-v1.html','guatemala.glb','guatemala.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','acceptance-check.json','.gitattributes'}
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':H(p.read_bytes())} for p in files};assert required<=inv.keys()
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'guatemala-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for p in files+[R/'inventory.json']:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():
  b=f.read(n);assert len(b)==v['bytes'] and H(b)==v['sha256'],n
 assert f.read('guatemala-v1.html')==(R/'guatemala-v1.html').read_bytes()
out={'status':'PASS','required_artifacts_present':sorted(required),'inventory_entries':len(inv),'archive_entries':len(inv)+1,'zip_bytes':z.stat().st_size,'zip_sha256':H(z.read_bytes()),'inventory_sha256':H((R/'inventory.json').read_bytes()),'html_bytes':(R/'guatemala-v1.html').stat().st_size,'glb_bytes':(R/'guatemala.glb').stat().st_size,'archive_all_bytes_read_back':True,'html_archived_bytes_equal_browser_tested_file':True}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('DELIVERY PASS',json.dumps(out))
