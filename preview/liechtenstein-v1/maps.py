from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(816); y,x=np.mgrid[0:256,0:512]
fine=rng.normal(0,4,x.shape); veins=np.sin(x*.024+y*.067+np.sin(y*.043)*1.8)
v=np.clip(178+fine+10*veins,140,205)
a=np.stack([v*1.02,v,v*.94],axis=-1).clip(0,255).astype('uint8')
Image.fromarray(a).save(R/'limestone-color.png')
r=np.clip(175+fine*2+14*veins,135,220).astype('uint8');Image.fromarray(r).convert('RGB').save(R/'limestone-roughness.png')
d=np.clip(v+10*np.sin(x*.08+y*.05),120,220);Image.fromarray(np.stack([d,d*.99,d*.93],axis=-1).astype('uint8')).save(R/'rock-detail.png')
print('Three procedural limestone maps written')
