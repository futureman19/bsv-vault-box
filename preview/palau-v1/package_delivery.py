from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def sha(data):return hashlib.sha256(data).hexdigest()
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']>=81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {b['case'] for b in browser}=={'desktop','mobile','corrupted GLB'}
for b in browser[:2]:
 assert not b['errors'] and not b['external_requests'] and b['open_close'] and b['reset_mid_motion'] and b['reduced_motion']
 assert b['asset']['bytes']==(R/'palau.glb').stat().st_size
 assert b['asset']['nonfinite']==b['asset']['degenerate']==0
assert browser[2]['fallback']
assert 'PASS motion' in (R/'motion-output.txt').read_text()
html=(R/'palau-v1.html').read_bytes();assert len(html)<5_000_000
required={'palau-v1.html','palau.glb','palau.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-output.txt','.gitattributes'}
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
excluded={'inventory.json','delivery-check.json','package-output.txt','git-verification.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.suffix in allowed or p.name=='.gitattributes') and p.name not in excluded and (p.parent==R or p.parent.name in {'maps','initial'}))
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required<=inventory.keys(),required-inventory.keys()
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
z=R/'palau-v1-source.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for p in files+[R/'inventory.json']:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())==set(inventory)|{'inventory.json'}
 assert archive.testzip() is None
 for name,info in inventory.items():
  raw=archive.read(name);assert len(raw)==info['bytes'] and sha(raw)==info['sha256']
report={'status':'PASS','HTML_BYTES':len(html),'GLB_BYTES':(R/'palau.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_SHA256':sha(z.read_bytes()),'inventory_entries':len(inventory),'required_artifacts_present':True,'archive_readback_verified':True,'scope':'folder-local only; no external delivery copy or hosting','html_sha256':sha(html),'glb_sha256':sha((R/'palau.glb').read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
