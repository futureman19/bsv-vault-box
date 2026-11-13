from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(26857649);y,x=np.mgrid[:256,:256]
pits=np.zeros((256,256))
for i in range(900):
 cx,cy=rng.uniform(0,256,2);r=rng.uniform(.5,2.7);pits+=np.exp(-((x-cx)**2+(y-cy)**2)/(r*r))*rng.uniform(.05,.25)
v=np.clip(1-pits+.035*np.sin(x*.09)*np.sin(y*.07)+rng.normal(0,.012,x.shape),.65,1.1)
Image.fromarray(np.uint8(np.clip(v[:,:,None]*np.array([215,199,161]),0,255))).save(R/'limestone-color.png')
Image.fromarray(np.uint8(np.clip(170+pits*110,0,255))).save(R/'limestone-roughness.png')
gy,gx=np.gradient(v);n=np.stack([-gx*1.2,-gy*1.2,np.ones_like(v)],-1);n/=np.linalg.norm(n,axis=-1)[:,:,None]
Image.fromarray(np.uint8((n*.5+.5)*255)).save(R/'limestone-normal.png')
print('MAPS PASS')
