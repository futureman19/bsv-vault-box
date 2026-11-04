"""Deterministic authored stone maps; no harvested imagery."""
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(869);n=384
y,x=np.mgrid[:n,:n];grain=rng.normal(0,1,(n,n));broad=np.sin(x*.053+np.sin(y*.03))*np.cos(y*.047)+.5*np.sin((x+y)*.11)
h=np.clip(.5+.12*broad+.11*grain,0,1)
color=np.stack([38+35*h,43+37*h,43+34*h],axis=-1);pores=rng.random((n,n))<.028;color[pores]*=.53
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'volcanic-color.png')
rough=np.uint8(np.clip(165+48*h,0,255));Image.fromarray(rough).convert('RGB').save(R/'volcanic-roughness.png')
dy,dx=np.gradient(h);normal=np.stack([-dx*.35,-dy*.35,np.ones_like(h)],axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
Image.fromarray(np.uint8((normal*.5+.5)*255)).save(R/'volcanic-normal.png')
print('MAPS PASS: three 384x384 procedural stone maps')
