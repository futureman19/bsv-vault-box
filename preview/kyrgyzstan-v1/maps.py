from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(693);n=256
a=rng.normal(0,1,(n,n));fine=(a+np.roll(a,1,axis=0)*.3+np.roll(a,1,axis=1)*.2)
y,x=np.mgrid[:n,:n];weave=np.sin(x*2.4+y*.6)*1.8+np.sin(y*2.7)*1.4
color=np.clip(np.array([142,37,55])+fine[:,:,None]*7+weave[:,:,None],0,255).astype('uint8')
Image.fromarray(color).save(R/'felt-color.png')
Image.fromarray(np.clip(229+fine*5,210,250).astype('uint8')).save(R/'felt-roughness.png')
gy,gx=np.gradient(fine);normal=np.dstack([128-gx*3,128-gy*3,np.full_like(gx,254)])
Image.fromarray(np.clip(normal,0,255).astype('uint8')).save(R/'felt-normal.png')
print('MAPS PASS: deterministic 256x256 independently generated felt maps')
