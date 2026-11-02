"""Original compact mineral and invented woven-stripe maps; no borrowed imagery."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(8701);n=512
y,x=np.mgrid[:n,:n];noise=rng.normal(0,1,(n,n))
cloud=np.zeros((n,n))
for size,weight in [(8,9),(24,5),(80,3)]:
 a=Image.fromarray(rng.integers(0,256,(size,size),dtype=np.uint8)).resize((n,n),Image.Resampling.BICUBIC)
 cloud+=(np.asarray(a)/128-1)*weight
vein=np.exp(-((np.sin(y*.023+x*.041+np.sin(x*.018)*.7+cloud*.07))/.07)**2)
c=np.array([47,57,64])+cloud[:,:,None]+noise[:,:,None]*2.8+vein[:,:,None]*np.array([13,12,9])
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'basalt-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(185+cloud*1.5+noise*3,0,255))).save(R/'basalt-roughness.png',optimize=True)
# Simple invented stripe arrangement, not a named/traditional blanket pattern.
c=np.zeros((n,n,3))+np.array([34,53,82]);stripe=np.minimum(y,n-1-y)
c[(stripe>100)&(stripe<125)]=[190,177,145]
c[(stripe>134)&(stripe<148)]=[139,75,47]
c[(stripe>160)&(stripe<164)]=[169,164,143]
c[(x%128<5)&(stripe>95)]=[109,124,139]
weave=((x%4<2)^(y%4<2)).astype(float)*8-4
c+=weave[:,:,None]+rng.normal(0,1,(n,n,1))*1.2
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'woven-indigo.png',optimize=True)
print('MAPS PASS',len(list(R.glob('*.png'))))
