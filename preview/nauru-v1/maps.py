from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(674);n=384
# Isotropic multiscale limestone pores, not inherited woodgrain.
a=np.asarray(Image.fromarray(rng.integers(0,256,(48,48),dtype=np.uint8)).resize((n,n),Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(3)),dtype=float)/255
b=rng.normal(0,1,(n,n));pores=rng.random((n,n))<.035
v=.86+.18*a+.014*b-.17*pores
color=np.clip(np.stack([205*v,196*v,171*v],-1),0,255).astype('uint8')
Image.fromarray(color).save(R/'limestone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(180+35*a+25*pores,0,255))).save(R/'limestone-roughness.png',optimize=True)
dy,dx=np.gradient(v);normal=np.stack([-dx*.6,-dy*.6,np.ones_like(dx)],-1);normal/=np.linalg.norm(normal,axis=-1)[...,None]
Image.fromarray(np.uint8(np.clip((normal*.5+.5)*255,0,255))).save(R/'limestone-normal.png',optimize=True)
print('PASS: three procedural limestone maps 384 x 384')
