"""Deterministic generated sandstone maps; no photographic inputs."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1377);h,w=256,512
y,x=np.mgrid[0:h,0:w];u=x/w;v=y/h
warp=v+.024*np.sin(2*np.pi*u)+.012*np.sin(6*np.pi*u+3*v)+.005*np.sin(18*np.pi*u+9*v)
bands=np.sin(warp*38)+.38*np.sin(warp*93+1.2)+.15*np.sin(warp*173)
wisps=np.clip((np.sin(warp*69+np.sin(u*12.566)*.4)-.85)*4,0,1)
grain=rng.normal(0,1.9,(h,w))
color=np.stack([166+bands*17+wisps*26+grain,88+bands*12+wisps*37+grain,57+bands*7+wisps*27+grain],axis=-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'sandstone-color.png')
rough=np.uint8(np.clip(181+bands*8+grain*2,0,255));Image.fromarray(rough).save(R/'sandstone-roughness.png')
# A separate darker lid atlas deliberately differs from the body.
Image.fromarray(np.uint8(np.clip(color*np.array([.67,.61,.58]),0,255))).save(R/'lid-color.png')
print('MAPS PASS 3 generated maps, 512x256')
