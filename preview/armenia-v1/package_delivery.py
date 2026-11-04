from pathlib import Path
import json,hashlib,zipfile
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'armenia-v1.html','armenia.glb','armenia.blend','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','motion-output.txt','poster.png','poster.jpg','package-lock.json'}
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert (R/'armenia-v1.html').stat().st_size<5000000
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt','git-proof.txt']}
assert required<=files.keys()
inv={n:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'armenia-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as f:
 for n,p in sorted(files.items()):f.write(p,n)
 f.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(files)|{'inventory.json'}
 for n,v in inv.items():assert sha(f.read(n))==v['sha256'] and len(f.read(n))==v['bytes']
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True);c=b.new_context(offline=True);p=c.new_page();p.goto((R/'armenia-v1.html').as_uri());p.wait_for_function('pilot.ready');assert p.evaluate('pilot.asset.bytes')==(R/'armenia.glb').stat().st_size;c.close();b.close()
r={'status':'PASS','html_bytes':(R/'armenia-v1.html').stat().st_size,'glb_bytes':(R/'armenia.glb').stat().st_size,'payload_files':len(files),'required_files_present':True,'archive_readback_all_hashes':True,'final_html_offline_ready':True,'archive_bytes':z.stat().st_size,'archive_sha256':sha(z.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
