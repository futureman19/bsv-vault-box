from pathlib import Path
import json
R=Path(__file__).resolve().parent
def load(n):return json.loads((R/n).read_text())
s=load('source-check.json');assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions'] and s['moving_meshes']==17 and s['static_meshes']==39
p=load('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
t=load('theme-check.json');assert t['status']=='PASS' and t['detached_negative_control']=='Relief detached from lid'
b=load('browser-check.json');assert len(b)==3
for c in b[:2]:
 assert c['offline_file'] and c['open_close'] and c['reset_mid_motion'] and c['reduced_motion'] and not c['errors'] and not c['external_requests'] and not c['overflow']
 assert c['asset']['nonfinite']==0 and c['asset']['degenerate']==0 and c['asset']['open_projection_max_abs_ndc']<1
assert b[2]['fallback'] and not b[2]['unhandled_errors']
assert load('extended-check.json')['status']=='PASS'
assert (R/'argentina-v1.html').stat().st_size<5000000
checks=['source','parity','theme / negative control','81-pose motion','desktop offline','mobile touch offline','corrupt-GLB fallback','no-JS fallback','portable maps','size']
for c in checks:print(c+': PASS')
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks':checks},indent=2))
