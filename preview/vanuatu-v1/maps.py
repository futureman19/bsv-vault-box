from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(8301);n=256
y,x=np.mgrid[:n,:n]
noise=rng.normal(0,1,(n,n));broad=np.sin(x*.074+np.sin(y*.083))*np.cos(y*.043)*4
pits=(noise<-1.6)*12
v=np.clip(48+broad+noise*5-pits,22,82)
a=np.stack([v,v*.94,v*.86],axis=-1).astype('uint8');Image.fromarray(a).save(R/'ash-color.png')
rough=np.clip(197+noise*10+pits,160,235).astype('uint8');Image.fromarray(rough).save(R/'ash-roughness.png')
gy,gx=np.gradient(v/255);normal=np.stack([-gx*1.6,-gy*1.6,np.ones_like(gx)],axis=-1);normal/=np.linalg.norm(normal,axis=-1)[...,None];Image.fromarray(((normal*.5+.5)*255).astype('uint8')).save(R/'ash-normal.png')
print('MAPS PASS: deterministic 256px ash color / roughness / normal')
