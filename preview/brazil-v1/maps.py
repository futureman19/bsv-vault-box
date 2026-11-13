from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(831);y,x=np.mgrid[0:512,0:512]/512
phase=y*93+.8*np.sin(x*7+y*4)+.3*np.sin(x*19+y*11)
grain=(.5+.5*np.sin(phase*6.283))**12
v=.86-.23*grain+.06*np.sin(y*18+x*3)+rng.normal(0,.014,x.shape)
wood=np.stack([149*v,100*v,69*v],-1)
Image.fromarray(np.uint8(np.clip(wood,0,255))).save(R/'earthwood-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(wood*.74,0,255))).resize((256,256)).save(R/'earthwood-end.png',optimize=True)
Image.fromarray(np.uint8(np.clip(145+grain*42,0,255))).save(R/'earthwood-roughness.png',optimize=True)
dy,dx=np.gradient(v);n=np.stack([-dx*.5,-dy*.5,np.ones_like(v)],-1);n/=np.linalg.norm(n,axis=-1)[...,None]
Image.fromarray(np.uint8(np.clip((n*.5+.5)*255,0,255))).save(R/'earthwood-normal.png',optimize=True)
noise=rng.normal(0,1,(256,256));speck=np.clip(104+noise*24,38,177)
Image.fromarray(np.uint8(np.stack([speck*1.03,speck*1.02,speck],-1))).save(R/'granite.png',optimize=True)
print('PASS procedural maps')
