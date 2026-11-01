"""Read-only baseline immutability, pivot and closed-envelope regression."""
from pathlib import Path
import json,hashlib,struct
R=Path(__file__).resolve().parent;B=R.parent/'iceland-pilot'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
baseline=json.loads((R/'baseline-hashes.json').read_text())
for name,digest in baseline.items():assert sha(B/name)==digest,name
assert (B/'motion.mjs').read_bytes()==(R/'motion.mjs').read_bytes()
def glb(p):
 b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];return json.loads(b[20:20+n])
a,b=glb(B/'iceland.glb'),glb(R/'iceland.glb');anchors={}
for name in ['Lid_Hinge','Latch_Pivot']:
 old=next(n for n in a['nodes'] if n.get('name')==name);new=next(n for n in b['nodes'] if n.get('name')==name)
 for k in ['matrix','translation','rotation','scale']:assert old.get(k)==new.get(k),(name,k)
 anchors[name]={k:new[k] for k in ['matrix','translation','rotation','scale'] if k in new}
x=json.loads((B/'browser-check.json').read_text())[0]['asset'];y=json.loads((R/'browser-check.json').read_text())[0]['asset']
for k in ['min','max']:assert max(abs(i-j) for i,j in zip(x['bounds'][k],y['bounds'][k]))<1e-6
out={'v1_files_unchanged':len(baseline),'motion_bytes_unchanged':True,'anchors_unchanged':anchors,'closed_bounds_match_tolerance':1e-6,'v1_model_bytes':x['bytes'],'v2_model_bytes':y['bytes'],'model_byte_multiplier':y['bytes']/x['bytes'],'v1_html_bytes':(B/'iceland-pilot.html').stat().st_size,'v2_html_bytes':(R/'iceland-realism-v2.html').stat().st_size}
(R/'preservation-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
