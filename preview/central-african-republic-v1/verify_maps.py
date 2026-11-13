from pathlib import Path
import numpy as np,json
from PIL import Image
R=Path(__file__).resolve().parent
stats={}
for name in ['timber-color','timber-end','timber-normal','timber-roughness','granite']:
 a=np.asarray(Image.open(R/'maps'/f'{name}.png').convert('RGB'))
 assert max(a.shape[:2])<=512 and np.isfinite(a).all()
 ranges=np.ptp(a.astype(float),axis=(0,1));assert ranges.max()>0
 stats[name]={'size':list(a.shape[:2]),'ranges':ranges.tolist(),'median':np.median(a,axis=(0,1)).tolist()}
assert np.all(np.abs(np.array(stats['timber-color']['median'])-[85,48,28])<15)
r={'status':'PASS','procedural_maps':stats,'not_scans':True}
(R/'maps-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
