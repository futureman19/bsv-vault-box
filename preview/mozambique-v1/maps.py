from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:512,0:512]/511
rng=np.random.default_rng(412)
ripple=np.sin(y*180+4*np.sin(x*9)+2*np.sin(x*23))
grain=rng.normal(0,1.6,x.shape)
c=np.stack([218+4*ripple+grain,196+5*ripple+grain,154+6*ripple+grain],axis=-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'sand-color.png')
Image.fromarray(np.uint8(np.clip(190+8*ripple+grain,0,255))).convert('RGB').save(R/'sand-roughness.png')
channel=np.exp(-((x-(.50+.13*np.sin(y*7)))/.055)**2)
wave=np.sin(x*34+y*45)*.7
c=np.stack([40-20*channel+wave,127-55*channel+wave,134-45*channel+wave],axis=-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'water-color.png')
dy,dx=np.gradient(ripple)
n=np.stack([-dx*.18,-dy*.18,np.ones_like(x)],axis=-1);n/=np.linalg.norm(n,axis=-1,keepdims=True)
Image.fromarray(np.uint8((n*.5+.5)*255)).save(R/'sand-normal.png')
print('MAPS_PASS')
