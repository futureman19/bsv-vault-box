from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(117);y,x=np.mgrid[:256,:256]/256
h=np.zeros_like(x)
for i in range(180):
 cx,cy=rng.random(2);rad=rng.uniform(.012,.038)
 h-=rng.uniform(.4,1)*np.exp(-((x-cx)**2+(y-cy)**2)/(2*rad*rad))
h=(h-h.min())/(h.max()-h.min());v=.72+.28*h+rng.normal(0,.009,h.shape)
Image.fromarray(np.uint8(np.clip(np.stack([169*v,94*v,57*v],-1),0,255))).save(R/'copper-color.png')
Image.fromarray(np.uint8(105+65*(1-h))).save(R/'copper-roughness.png')
dy,dx=np.gradient(h);n=np.stack([-dx*3,-dy*3,np.ones_like(h)],-1);n/=np.linalg.norm(n,axis=-1)[...,None]
Image.fromarray(np.uint8((n*.5+.5)*255)).save(R/'copper-normal.png')
print('PASS: three procedural 256px copper maps')
