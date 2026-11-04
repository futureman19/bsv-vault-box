from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(3317921);n=256
y,x=np.mgrid[:n,:n];grain=rng.normal(0,4,(n,n))
broad=np.zeros((n,n))
for size,amplitude in [(9,7),(27,4),(71,2)]:
 raw=Image.fromarray(rng.uniform(0,255,(size,size)).astype('uint8'))
 broad+=(np.asarray(raw.resize((n,n),Image.Resampling.BICUBIC)).astype(float)/255-.5)*amplitude
v=grain+broad
color=np.clip(np.array([52,61,60])[None,None,:]+v[:,:,None],0,255).astype('uint8')
Image.fromarray(color).save(R/'volcanic-color.png')
rough=np.clip(190+v*2,100,235).astype('uint8');Image.fromarray(rough).save(R/'volcanic-roughness.png')
h=rng.normal(0,.5,(n,n));dy,dx=np.gradient(h);norm=np.stack([-dx*.12,-dy*.12,np.ones_like(h)],axis=2);norm/=np.linalg.norm(norm,axis=2)[:,:,None]
Image.fromarray(np.clip((norm*.5+.5)*255,0,255).astype('uint8')).save(R/'volcanic-normal.png')
print('MAPS PASS: independent procedural color, roughness and normal 256x256')
