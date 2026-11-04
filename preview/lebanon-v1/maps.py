from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(850);y,x=np.mgrid[0:256,0:256]/256
phase=y*65+.4*np.sin(x*9+y*8)
grain=(.5+.5*np.sin(phase*6.283))**9
v=1-.22*grain+.06*np.sin(y*19+x*2)+rng.normal(0,.012,x.shape)
wood=np.stack([160*v,85*v,44*v],-1)
Image.fromarray(np.uint8(np.clip(wood,0,255))).save(R/'cedar-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(wood*.68,0,255))).save(R/'cedar-end.png',optimize=True)
Image.fromarray(np.uint8(145+grain*40)).save(R/'cedar-roughness.png',optimize=True)
speck=np.clip(104+rng.normal(0,24,x.shape),38,177)
Image.fromarray(np.uint8(np.stack([speck*1.03,speck*1.02,speck],-1))).save(R/'granite.png',optimize=True)
strata=np.sin(y*27+np.sin(x*13)*.7+np.sin(x*29+y*17)*.25)
pore=rng.normal(0,2.4,x.shape);v=strata*8+pore
stone=np.stack([199+v,185+v,158+v],-1)
Image.fromarray(np.uint8(np.clip(stone,0,255))).save(R/'limestone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(199+strata*12+pore*2,0,255))).save(R/'limestone-roughness.png',optimize=True)
print('PASS procedural maps: cedar and limestone; no borrowed image pixels')
