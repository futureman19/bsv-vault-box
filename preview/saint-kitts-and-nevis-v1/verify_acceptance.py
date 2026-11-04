"""Fail-closed aggregate gate; run after individual verifiers and packaging."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
s=load('source-check.json');assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions'];assert s['moving_meshes']==19 and s['static_meshes']==36
assert len(load('hinge-attachment-check.json')['intersecting_attachment_pairs'])==10
p=load('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
t=load('theme-check.json');assert t['status']=='PASS' and t['detached_ornament_negative_control_rejected']
e=load('extended-check.json');assert e['status']=='PASS' and e['noJS_poster'] and e['poster_source_render_nonblank']
b=load('browser-check.json');assert [x['case'] for x in b]==['desktop','mobile','corrupted GLB']
for x in b[:2]:
 assert all(x[k] for k in ['offline_file','rotation','open_close','reset_mid_motion','reduced_motion'])
 assert not x['errors'] and not x['external_requests'] and not x['overflow']
 assert x['asset']['degenerate']==0 and x['asset']['nonfinite']==0
 assert x['asset']['bytes']==(R/'saint-kitts-and-nevis.glb').stat().st_size
assert b[1]['touch_rotation'] and b[2]['fallback'] and b[2]['caught_loader_errors']
assert 'MOTION PASS:' in (R/'motion-output.txt').read_text()
d=load('delivery-check.json');assert d['status']=='PASS' and d['archive_readback_verified'] and d['HTML_BYTES']<5000000
for name,m in load('inventory.json').items():
 data=(R/name).read_bytes();assert len(data)==m['bytes'] and hashlib.sha256(data).hexdigest()==m['sha256'],name
print('SOURCE PASS: 81 poses, 19 moving, 36 static, 0 unintended collisions, 10 attachment pairs')
print('PARITY PASS: maximum error',max(p['source_to_glb_max'],p['glb_to_source_max']))
print('THEME PASS: two attached islands, crater/cone/channel, original pivots, detached negative rejected')
print('BROWSER PASS: desktop + mobile file://, controls, reduced motion, offline, corrupt GLB + no-JS')
print('MAPS AND POSTER PASS: portable decoded variation and nonblank source render')
print('DELIVERY PASS: exact SHA-256 inventory and ZIP readback')
print('HTML_BYTES',d['HTML_BYTES'],'GLB_BYTES',d['GLB_BYTES'])
