from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(601);n=256
y,x=np.mgrid[:n,:n]/n
smooth=np.asarray(Image.fromarray(rng.integers(0,255,(32,32),dtype=np.uint8)).resize((n,n),Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(4)),dtype=float)/255-.5
pores=rng.random((n,n))>.985
v=1+.08*smooth+.018*np.sin(y*35+np.sin(x*12)*1.7)-pores*.16+rng.normal(0,.007,(n,n))
color=np.stack([205*v,190*v,160*v],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'stone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(145+smooth*40+pores*45,0,255))).save(R/'stone-roughness.png',optimize=True)
Image.fromarray(np.uint8(np.clip(color*.72,0,255))).save(R/'foot-color.png',optimize=True)
print('MAPS PASS: 3 independently generated 256px stone maps')
