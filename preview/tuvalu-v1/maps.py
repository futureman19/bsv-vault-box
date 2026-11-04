from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:512,:512];rng=np.random.default_rng(521)
a=x//32;b=y//32;horizontal=(a+b)%2==0
edge=np.where(horizontal,y%32,x%32)
shade=.78+.22*np.sin(np.pi*(edge+1)/33)
fibre=np.where(horizontal,np.sin(y*2.3+x*.04),np.sin(x*2.3+y*.04))*3
c=np.array([213,182,124])[None,None,:]*shade[:,:,None]+fibre[:,:,None]+rng.normal(0,1.6,(512,512,1))
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'weave-color.png')
rough=np.uint8(165+35*(1-shade)+rng.random((512,512))*16)
Image.fromarray(rough).save(R/'weave-roughness.png')
dy,dx=np.gradient(shade);normal=np.stack([-dx*2,-dy*2,np.ones_like(dx)],axis=-1);normal/=np.linalg.norm(normal,axis=-1)[:,:,None]
Image.fromarray(np.uint8((normal*.5+.5)*255)).save(R/'weave-normal.png')
print('MAPS PASS')
