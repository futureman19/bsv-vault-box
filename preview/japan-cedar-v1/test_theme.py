from pathlib import Path
import json,struct
R=Path(__file__).resolve().parent
raw=(R/'japan.glb').read_bytes();n=struct.unpack_from('<I',raw,12)[0];d=json.loads(raw[20:20+n]);names=[x.get('name','') for x in d['nodes']]
for prefix in ['Cedar / front','Finger /','Cedar tree / trunk','Cedar tree / foliage','Terrain / granite','Terrain / moss','Granite foot','Side ring','Medallion','Lid_Hinge','Latch_Pivot']:
 assert any(x.startswith(prefix.replace(' ','_').replace('/','')) or x.startswith(prefix) for x in names),prefix
assert not any(any(b in x.lower() for b in ['glacier','basalt','river','iceland']) for x in names)
assert len(d.get('images',[]))>=3
assert (R/'japan-cedar-v1.html').stat().st_size<5_000_000
(R/'theme-check.json').write_text(json.dumps({'required_features':True,'portable_images':len(d['images']),'no_old_theme_nodes':True},indent=2))
print('THEME PASS')
