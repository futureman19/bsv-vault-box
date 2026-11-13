"""Gate aggregation, exact inventory and source ZIP readback (no external writes)."""
from pathlib import Path
import json,hashlib,zipfile,subprocess
R=Path(__file__).resolve().parent
def load(n):return json.loads((R/n).read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
s=load('source-check.json');p=load('parity-check.json');t=load('theme-check.json');b=load('browser-check.json');e=load('extended-check.json')
checks={
 'source':s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions'] and s['moving_meshes']==59 and s['static_meshes']==113,
 'hinge_attachment':len(load('hinge-attachment-check.json')['intersecting_attachment_pairs'])==10,
 'parity':p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5,
 'theme':t['status']=='PASS' and t['negative_control']['detached_leaf_rejected'],
 'browser':len(b)==3 and all(x['offline_file'] and not x['errors'] and not x['external_requests'] and x['open_close'] and x['reset_mid_motion'] and x['reduced_motion'] and not x['overflow'] and x['asset']['nonfinite']==0 and x['asset']['degenerate']==0 for x in b[:2]) and b[2]['fallback'],
 'extended':e['status']=='PASS' and e['nojs_poster'] and set(e['reduced_motion_samples'])<={0,1},
 'size':(R/'mexico-v1.html').stat().st_size<5000000,
 'motion':'PASS motion:' in (R/'motion-output.txt').read_text(),
}
assert all(checks.values()),checks
out={'status':'PASS','checks':{k:'PASS' for k in checks},'HTML_BYTES':(R/'mexico-v1.html').stat().st_size,'GLB_BYTES':(R/'mexico.glb').stat().st_size}
(R/'acceptance-check.json').write_text(json.dumps(out,indent=2))
exclude={'inventory.json','delivery-check.json','mexico-v1-source.zip','package-output.txt','git-evidence.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in exclude and not {'node_modules','__pycache__'}&set(p.relative_to(R).parts) and p.suffix!='.blend1')
required={'mexico-v1.html','mexico.glb','mexico.blend','mechanism.blend','design-brief.md','README.md','poster.png','source-check.json','parity-check.json','browser-check.json','theme-check.json','acceptance-check.json'}
inv={str(p.relative_to(R)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in files};assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'mexico-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for name,record in inv.items():
  data=z.read(name);assert len(data)==record['bytes'] and digest(data)==record['sha256'],name
result={'status':'PASS','HTML_bytes':out['HTML_BYTES'],'GLB_bytes':out['GLB_BYTES'],'ZIP_bytes':zpath.stat().st_size,'ZIP_sha256':digest(zpath.read_bytes()),'inventory_entries':len(inv),'archive_readback_verified':True,'required_artifacts_verified':sorted(required),'all_payload_sha256_verified':True,'inventory_scope':'Every delivery file except inventory itself, delivery-check envelope, ZIP and mutable execution logs git-evidence/package-output; no recursive hashes.'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2))
for k in checks:print(k.upper()+' PASS')
print('HTML_BYTES',out['HTML_BYTES'],'GLB_BYTES',out['GLB_BYTES']);print('DELIVERY PASS',json.dumps(result))
