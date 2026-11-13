from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(913);y,x=np.mgrid[0:512,0:512]/512
warp=.012*np.sin(x*19)+.006*np.sin(x*51+y*7)
phase=(y+warp)*8
band=(np.sin(phase*np.pi*2)+.22*np.sin(phase*np.pi*4)>.45).astype(float)
noise=rng.normal(0,3,x.shape)
orange=np.array([175,91,43]);dark=np.array([57,53,45]);col=orange[None,None,:]*(1-band[:,:,None])+dark[None,None,:]*band[:,:,None]
col+=noise[:,:,None]+7*np.sin(y*93+x*17)[:,:,None]
Image.fromarray(np.uint8(np.clip(col,0,255))).save(R/'sandstone-color.png',optimize=True)
rough=np.clip(192+band*30+noise*2,0,255).astype('uint8');Image.fromarray(rough).save(R/'sandstone-roughness.png',optimize=True)
height=rng.normal(0,1,x.shape);dy,dx=np.gradient(height);n=np.dstack((-dx*.08,-dy*.08,np.ones_like(x)));n/=np.linalg.norm(n,axis=2)[:,:,None]
Image.fromarray(np.uint8((n*.5+.5)*255)).save(R/'sandstone-normal.png',optimize=True)
print('MAPS PASS: three 512x512 generated stone maps')
