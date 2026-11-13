"""Deterministic original granite maps; no photographic source pixels."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(9801);n=256
y,x=np.mgrid[:n,:n];fine=rng.normal(0,1,(n,n));broad=np.sin(x*.09+np.sin(y*.035))*np.cos(y*.065)*4
base=np.array([170,146,135]);c=base+fine[:,:,None]*10+broad[:,:,None]
fleck=rng.random((n,n));c[fleck<.065]-=48;c[fleck>.925]+=38
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'granite-color.png')
rough=np.clip(185+fine*12,140,225).astype('uint8');Image.fromarray(rough).save(R/'granite-roughness.png')
gy,gx=np.gradient(fine);norm=np.dstack((-gx*.07,-gy*.07,np.ones_like(gx)));norm/=np.linalg.norm(norm,axis=2)[:,:,None]
Image.fromarray(np.uint8(np.clip((norm*.5+.5)*255,0,255))).save(R/'granite-normal.png')
print('MAPS PASS: three deterministic 256x256 portable images')
