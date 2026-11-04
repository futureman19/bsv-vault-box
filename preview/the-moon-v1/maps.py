from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
R=Path(__file__).resolve().parent;(R/'maps').mkdir(exist_ok=True)
rng=np.random.default_rng(201);n=256
base=np.zeros((n,n))
for k,weight in [(8,10),(32,9),(128,5),(256,4)]:
 a=Image.fromarray(rng.integers(0,256,(k,k),dtype=np.uint8)).resize((n,n),Image.Resampling.BICUBIC)
 base+=(np.asarray(a).astype(float)-128)*weight/64
for name,offset in [('regolith',137),('highland',173)]:
 a=np.stack([base+offset,base+offset,base+offset-3],axis=-1)
 Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'maps'/f'{name}-color.png')
Image.fromarray(np.uint8(np.clip(218+base,170,250))).convert('RGB').save(R/'maps/regolith-roughness.png')
# Smooth terrain-local mare boundary avoids material-per-face stair stepping.
y,x=np.mgrid[0:512,0:512];wx=-1.58+3.16*x/511;wy=.94-1.88*y/511
d=np.sqrt(((wx+.68)/.40)**2+((wy+.22)/.39)**2)
blend=np.clip((d-.94)/.09,0,1)
noise=np.asarray(Image.fromarray(np.uint8(np.clip(base+128,0,255))).resize((512,512))).astype(float)-128
light=164+noise;dark=66+noise*.4
v=dark*(1-blend)+light*blend
for cx,cy,r in [(.65,.43,.255),(.85,-.55,.19)]:
 d2=np.sqrt((wx-cx)**2+(wy-cy)**2)/r
 weight=np.clip((.78-d2)/.24,0,1)
 v=v*(1-weight)+(100+noise*.4)*weight
Image.fromarray(np.uint8(np.clip(np.stack([v,v,v-2],axis=-1),0,255))).save(R/'maps/terrain-color.png')
print('MAPS PASS')
