"""Fail-closed acceptance aggregation and exact inventory/archive readback."""
from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'algeria-v1.html','algeria.glb','algeria.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','hinge-attachment-check.json','author.py','maps.py','build.py','verify_source.py','verify_parity.py','verify_browser.py','verify_theme.py','viewer.js','viewer.bundle.js','motion.mjs','tests.mjs','template.html','package.json','THREE-LICENSE.txt','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','maps/sandstone-color.png','maps/sandstone-roughness.png','maps/dark-stone.png'}
assert all((R/n).is_file() for n in required)
source=json.loads((R/'source-check.json').read_text());assert source['saved_source_reopened'] and source['collision_samples']==81 and not source['collisions'] and source['moving_meshes']==24 and source['static_meshes']==90
parity=json.loads((R/'parity-check.json').read_text());assert parity['source_and_export_geometry_match'] and max(parity['source_to_glb_max'],parity['glb_to_source_max'])<1e-5
browser=json.loads((R/'browser-check.json').read_text());assert [b['case'] for b in browser]==['desktop','mobile','corrupted GLB']
for b in browser[:2]:
 assert b['offline_file'] and not b['external_requests'] and not b['errors'] and not b['overflow']
 assert all(b[k] for k in ['rotation','open_close','reset_mid_motion','reduced_motion'])
 assert b['asset']['bytes']==(R/'algeria.glb').stat().st_size and b['asset']['degenerate']==0 and b['asset']['nonfinite']==0 and b['asset']['open_projection_max_abs_ndc']<1
assert browser[1]['touch_rotation'] and browser[2]['fallback'] and browser[2]['caught_loader_errors'] and not browser[2]['unhandled_errors']
theme=json.loads((R/'theme-check.json').read_text());assert theme['status']=='PASS' and theme['missing_tower_negative_control_rejected'] and theme['noJS_poster']
assert len(json.loads((R/'hinge-attachment-check.json').read_text())['intersecting_attachment_pairs'])==10
html=R/'algeria-v1.html';assert html.stat().st_size<5_000_000
# Prove the HTML embeds current model and source-derived poster, not stale payloads.
import base64
text=html.read_text(encoding='utf8');assert base64.b64encode((R/'algeria.glb').read_bytes()).decode() in text;assert base64.b64encode((R/'poster.jpg').read_bytes()).decode() in text
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.suffix in allowed or p.name=='.gitattributes') and p.name not in {'inventory.json','delivery-check.json','lane-prompt.txt'} and (p.parent==R or p.parent.name in {'maps','initial'}))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in files};assert required<=manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json');archive=R/'algeria-v1-source.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(archive) as z:
 assert set(z.namelist())=={p.relative_to(R).as_posix() for p in files} and z.testzip() is None
 for p in files:assert z.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':(R/'algeria.glb').stat().st_size,'ZIP_BYTES':archive.stat().st_size,'zip_sha256':sha(archive),'inventory_sha256':sha(R/'inventory.json'),'archive_entries':len(files),'required_artifacts_present':True,'archive_readback_verified':True,'embedded_payload_current':True,'checks_passed':['source','motion-81-poses','hinge-attachments','source-export-parity','desktop-offline','mobile-offline','corrupt-GLB-fallback','no-JS-fallback','theme','missing-tower-negative-control','payload-budget','inventory-and-archive-readback']}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print('HTML_BYTES',report['HTML_BYTES'],'GLB_BYTES',report['GLB_BYTES']);print('ALL ACCEPTANCE CHECKS PASS');print('ZIP_BYTES',report['ZIP_BYTES'],'ENTRIES',len(files))
