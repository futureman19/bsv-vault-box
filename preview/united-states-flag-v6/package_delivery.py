from pathlib import Path
import json,hashlib,zipfile,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
O=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-usa-flag-v6');O.mkdir(parents=True,exist_ok=True)
exclude={'inventory.json','delivery-check.json','branch-backup.json'}
files=[p for p in R.rglob('*') if p.is_file() and not any(s in p.parts for s in ['__pycache__','node_modules']) and p.name not in exclude and p.suffix not in ['.zip','.blend1']]
rows=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(files)]
(R/'inventory.json').write_text(json.dumps(rows,indent=2))
required={'united-states-flag-v6.html','united-states.glb','united-states.blend','poster.png','poster.jpg','README.md','author_materials.py','maps.py','view-front-left.png','view-rear-left.png','view-rear-right.png','view-front-right.png','reference-comparison.jpg','band-front-close.png','band-left-close.png','hero-fireworks.png','blender-source-no-fx.png','features-check.json','fireworks-pixels-check.json'}
assert required <= {r['path'] for r in rows}
z=R/'united-states-flag-v6-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as out:
 for p in files+[R/'inventory.json']:out.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as inp:
 assert len(inp.namelist())==len(set(inp.namelist()))
 for r in rows:
  a=inp.read(r['path']);assert len(a)==r['bytes'] and hashlib.sha256(a).hexdigest()==r['sha256']
for p in files+[R/'inventory.json',z]:
 target=O/p.relative_to(R);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);assert p.read_bytes()==target.read_bytes()
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True,viewport={'width':390,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce');p=c.new_page();requests=[];p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
 p.goto((O/'united-states-flag-v6.html').as_uri());p.wait_for_function('pilot.ready');p.locator('#open').tap();p.wait_for_function('pilot.progress===1');p.locator('#reset').tap();p.wait_for_function('pilot.progress===0');assert not requests;b.close()
artifacts={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [z,R/'united-states-flag-v6.html',R/'united-states.glb',R/'united-states.blend',R/'poster.png',R/'poster.jpg',R/'reference-comparison.jpg']}
assert artifacts['united-states-flag-v6.html']['bytes']<5_000_000
report=dict(PASS=True,inventory_entries=len(rows),zip_readback=True,required_artifact_subset=True,copied_output_hashes_match=True,delivered_html_offline_mobile_open_reset=True,external_requests=requests,artifacts=artifacts)
for path in [R/'delivery-check.json',O/'delivery-check.json']:path.write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
