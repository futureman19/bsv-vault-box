from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(6100);N=512
def noise(n):
 a=Image.fromarray(rng.integers(0,256,(n,n),dtype=np.uint8))
 return np.asarray(a.resize((N,N),Image.Resampling.BICUBIC)).astype(float)/255
coarse=noise(12);mid=noise(55);fine=noise(256)
f=.45*coarse+.3*mid+.25*fine
pore=(fine<.22)&(mid<.6)
base=np.array([38,34,30])+((f-.5)*55)[...,None]+coarse[...,None]*np.array([14,8,3]);base[pore]*=.40
Image.fromarray(np.uint8(np.clip(base,0,255))).save(R/'scoria-color.png',optimize=True)
rough=np.uint8(np.clip(195+f*42+pore*15,0,255));Image.fromarray(rough).convert('RGB').save(R/'scoria-roughness.png',optimize=True)
# Fine-scale normal perturbation derived from height, no baked illumination.
h=(mid*.3+fine*.7-pore*.4);dy,dx=np.gradient(h);n=np.stack([-dx*.35,-dy*.35,np.ones_like(h)],axis=2);n/=np.linalg.norm(n,axis=2)[...,None]
Image.fromarray(np.uint8(np.clip((n*.5+.5)*255,0,255))).save(R/'scoria-normal.png',optimize=True)
print('MAPS PASS: three independently generated 512x512 maps')
