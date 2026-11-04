from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
s=load('source-check.json');assert not s['collisions'] and s['collision_samples']==81
print('PASS source-check: 81 poses, zero unintended collisions')
p=load('parity-check.json');assert max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
print('PASS parity-check')
for n in ['theme-check.json','motion-check.json','extended-check.json','delivery-check.json']:
 assert load(n)['PASS'];print('PASS '+n)
b=load('browser-check.json');assert len(b)==3
for c in b[:2]:assert c['offline_file'] and not c['errors'] and not c['external_requests'] and c['reduced_motion'] and c['open_close']
assert b[2]['fallback'];print('PASS browser-check: desktop/mobile file:// and corrupt GLB fallback')
for n,item in load('inventory.json').items():
 data=(R/n).read_bytes();assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],n
print('PASS SHA-256 inventory')
d=load('delivery-check.json');print('HTML_BYTES',d['HTML_BYTES'],'GLB_BYTES',d['GLB_BYTES']);print('ALL ACCEPTANCE CHECKS PASS')
