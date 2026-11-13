"""Original seeded plaster and straw maps, not photographs or scans."""
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1140);n=512
def field(s,blur=0):
 a=Image.fromarray(rng.integers(0,256,(s,s),dtype=np.uint8)).resize((n,n),Image.Resampling.BICUBIC)
 if blur:a=a.filter(ImageFilter.GaussianBlur(blur))
 return np.asarray(a,dtype=float)/255-.5
broad=field(16,3);grain=field(256);fine=field(512)
v=17*broad+13*grain+5*fine
rgb=np.stack([158+v,88+v*.72,49+v*.50],axis=-1)
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'earth-color.png')
Image.fromarray(np.uint8(np.clip(218+18*grain+9*broad,0,255))).save(R/'earth-roughness.png')
y,x=np.mgrid[0:n,0:n];straw=8*np.sin(x*.63+2*field(32))+12*field(128)+5*field(512)
Image.fromarray(np.uint8(np.clip(np.stack([174+straw,132+straw*.85,69+straw*.5],axis=-1),0,255))).save(R/'straw-color.png')
print('MAPS PASS',np.median(rgb,axis=(0,1)).tolist())
