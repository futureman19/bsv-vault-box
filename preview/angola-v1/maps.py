from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(309)
y,x=np.mgrid[0:256,0:512];u=x/512;v=y/256
warp=v+.018*np.sin(u*33)+.008*np.sin(u*83+v*9)
band=np.sin(warp*49)+.4*np.sin(warp*117)
t=np.clip(.45+.25*band+rng.normal(0,.022,x.shape),0,1)
a=np.array([90,35,15]);b=np.array([185,132,66]);rgb=a+(b-a)*t[...,None]
Image.fromarray(rgb.astype('uint8')).save(R/'earth-color.png')
rough=np.clip(195+20*band+rng.normal(0,3,x.shape),0,255).astype('uint8')
Image.fromarray(rough).save(R/'earth-roughness.png')
rock=np.clip(rgb*.72+ rng.normal(0,5,(*x.shape,1)),0,255).astype('uint8');Image.fromarray(rock).save(R/'dark-earth.png')
print('MAPS PASS 512x256 generated color/roughness/dark-earth')
