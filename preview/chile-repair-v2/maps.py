from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(671);n=512
y,x=np.mgrid[0:n,0:n]/n
warp=y+.018*np.sin(x*19)+.011*np.sin(x*49+y*8)
f=.5+.2*np.sin(warp*89)+.08*np.sin(warp*211)+rng.normal(0,.035,(n,n))
base=np.array([153,91,66]);rgb=base[None,None,:]*(.72+f[:,:,None]*.50)
salt=rng.random((n,n))>.994;rgb[salt]=[210,188,148]
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'desert-color.png')
rough=np.uint8(np.clip(185+f*50,0,255));Image.fromarray(rough).save(R/'desert-roughness.png')
gy,gx=np.gradient(f);normal=np.stack([-gx*.28,-gy*.28,np.ones_like(f)],axis=2);normal/=np.linalg.norm(normal,axis=2)[:,:,None]
Image.fromarray(np.uint8((normal*.5+.5)*255)).save(R/'desert-normal.png')
print('MAPS PASS 512x512 color roughness normal')
