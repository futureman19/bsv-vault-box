from pathlib import Path
import json,struct
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent
raw=(R/'laos.glb').read_bytes();n=struct.unpack_from('<I',raw,12)[0];d=json.loads(raw[20:20+n]);nodes=d['nodes'];names=[o.get('name','') for o in nodes]
def clean(s):return s.replace(' ','_').replace('/','')
def matching(prefix):return [i for i,s in enumerate(names) if s.startswith(prefix) or s.startswith(clean(prefix))]
for prefix in ['Bamboo / woven front','Bamboo frame /','Karst / peak','Vegetation /','River /','Limestone foot','Side ring','Medallion','Lid_Hinge','Latch_Pivot']:
 assert matching(prefix),prefix
assert len(matching('Karst / peak'))==3
assert not any(any(b in x.lower() for b in ['glacier','basalt','cedar','iceland']) for x in names)
lid=names.index('Lid_Hinge');children=nodes[lid].get('children',[])
for prefix in ['Karst /','Vegetation /','River /']:assert all(i in children for i in matching(prefix)),prefix
assert len(d.get('images',[]))>=5
ranges={}
for p in (R/'maps').glob('*.png'):
 a=np.asarray(Image.open(p));assert max(a.shape[:2])<=512
 ranges[p.name]=int(a.max())-int(a.min());assert ranges[p.name]>0
c=np.asarray(Image.open(R/'maps/bamboo-color.png'));means=c.mean(axis=(0,1));assert means[0]>means[1]>means[2] and 110<means[0]<200
assert (R/'laos-v1.html').stat().st_size<5_000_000
report={'status':'PASS','karst_peaks':3,'lid_ornament_parentage':True,'portable_images':len(d['images']),'map_ranges':ranges,'bamboo_rgb_mean':means.tolist(),'no_old_theme_nodes':True}
(R/'theme-check.json').write_text(json.dumps(report,indent=2));print('THEME PASS',json.dumps(report))
