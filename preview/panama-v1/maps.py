from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(159);y,x=np.mgrid[0:384,0:384]/384
f=np.sin(x*19+np.sin(y*14)*2)+.6*np.sin(y*31+x*8)+.3*np.sin(x*83+y*61)
v=1+.19*f+rng.normal(0,.022,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([35*v,91*v,69*v],-1),0,255))).save(R/'jade-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(135+f*20,70,200))).save(R/'jade-roughness.png',optimize=True)
v=1+.10*np.sin(x*31+y*21)+rng.normal(0,.055,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([124*v,105*v,71*v],-1),0,255))).save(R/'sediment.png',optimize=True)
n=rng.normal(0,1,(256,256));s=np.clip(63+n*15,20,110)
Image.fromarray(np.uint8(np.stack([s*.8,s,s*.9],-1))).save(R/'granite.png',optimize=True)
print('MAPS PASS')
