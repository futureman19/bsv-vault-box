"""Exact payload inventory and independent ZIP readback. Writes only this directory."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'ukraine-v1.html','ukraine.glb','ukraine.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','source-check.json','parity-check.json','browser-check.json','theme-check.json','theme-source-check.json','motion-check.json','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','mobile-nojs.png','.gitattributes'}
exclude={'inventory.json','delivery-check.json','ukraine-v1-source.zip','package-output.txt','git-verification.txt'}
files=[p for p in R.rglob('*') if p.is_file() and not set(p.relative_to(R).parts)&{'node_modules','__pycache__'} and p.name not in exclude and not p.name.endswith('.blend1')]
paths={p.relative_to(R).as_posix():p for p in files};assert required<=paths.keys(),required-paths.keys()
def sha(b):return hashlib.sha256(b).hexdigest()
inv={name:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for name,p in sorted(paths.items())}
assert inv['ukraine-v1.html']['bytes']<5000000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and source['collisions']==[]
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for f in ['theme-check.json','theme-source-check.json','motion-check.json']:assert json.loads((R/f).read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert len(browser)==3
for c in browser[:2]:assert not c['errors'] and not c['external_requests'] and c['open_close'] and c['reset_mid_motion'] and c['reduced_motion'] and c['asset']['degenerate']==0
assert browser[2]['fallback']
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'ukraine-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in paths.items():z.write(p,n)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():b=z.read(n);assert len(b)==v['bytes'] and sha(b)==v['sha256'],n
result={'status':'PASS','html_bytes':inv['ukraine-v1.html']['bytes'],'glb_bytes':inv['ukraine.glb']['bytes'],'inventory_entries':len(inv),'required_artifacts_present':True,'zip_readback':True,'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'exclusions':sorted(exclude),'limits':'No hosted deployment, no physical-phone tests; archive/inventory exclude themselves to avoid circular hashing.'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
