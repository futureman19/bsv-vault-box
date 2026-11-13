from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(573);y,x=np.mgrid[0:256,0:512];u=x/512;v=y/256
h=np.sin(v*95+3*np.sin(u*13)+np.sin(u*31))*.004+np.sin(u*22+np.sin(v*19))*np.sin(v*27)*.009+rng.normal(0,.014,u.shape)
c=np.array([.71,.46,.22])[None,None,:]+h[:,:,None]
Image.fromarray(np.uint8(np.clip(c,0,1)*255)).save(R/'sand-color.png')
Image.fromarray(np.uint8(np.clip(.78+h*2,0,1)*255)).save(R/'sand-roughness.png')
gy,gx=np.gradient(h);normal=np.stack((-gx*2,-gy*2,np.ones_like(h)),axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
Image.fromarray(np.uint8((normal*.5+.5)*255)).save(R/'sand-normal.png')
c=np.array([.24,.18,.12])[None,None,:]+rng.normal(0,.035,(256,256,1))
Image.fromarray(np.uint8(np.clip(c,0,1)*255)).save(R/'rock-color.png')
print('MAPS PASS')
