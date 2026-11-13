"""Final acceptance of measured evidence and exact delivered payloads."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
s=load('source-check.json');assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions'];assert s['moving_meshes']==37 and s['static_meshes']==51
p=load('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
b=load('browser-check.json');assert len(b)==3
for item in b[:2]:
 assert item['offline_file'] and item['open_close'] and item['reset_mid_motion'] and item['reduced_motion'] and not item['overflow'] and not item['external_requests'] and not item['errors'];assert item['asset']['nonfinite']==item['asset']['degenerate']==0;assert item['asset']['open_projection_max_abs_ndc']<1
assert b[1]['touch_rotation'] and b[2]['fallback'] and b[2]['caught_loader_errors'] and not b[2]['unhandled_errors']
for n in ['theme-source-check.json','extended-check.json','motion-check.json','visual-check.json','delivery-check.json']:assert load(n)['status']=='PASS',n
assert load('theme-source-check.json')['detached_ornament_negative_rejected']
for n,rec in load('inventory.json').items():
 data=(R/n).read_bytes();assert len(data)==rec['bytes'] and hashlib.sha256(data).hexdigest()==rec['sha256'],n
d=load('delivery-check.json');assert d['HTML_BYTES']==(R/'kiribati-v1.html').stat().st_size<5_000_000;assert d['GLB_BYTES']==(R/'kiribati.glb').stat().st_size;assert d['zip_readback_all_hashes']
copy=load('delivery-copy-check.json');assert copy['status']=='PASS' and copy['tested_html_sha256']==d['html_sha256']
print('PASS delivery-copy-check: actual ZIP-extracted HTML offline desktop/mobile')
print('HTML_BYTES',d['HTML_BYTES'],'GLB_BYTES',d['GLB_BYTES'])
print('PASS source-check: saved source, hollow liner, 81 motion poses, zero unintended collisions')
print('PASS parity-check: source/export world-vertex error < 1e-5')
print('PASS browser-check: offline desktop/mobile, controls, reduced motion, corrupt GLB')
print('PASS theme-source-check: pivots, rim/gap/root rays, detached-ornament negative control')
print('PASS extended-check: runtime maps/ancestry/copy, real poster pixels, no-JS fallback')
print('PASS motion-check: two real Node tests and malformed-asset negative controls')
print('PASS visual-check: stylized v1, limitations disclosed')
print('PASS delivery-check: required files, exact bytes/SHA-256 and ZIP readback')
