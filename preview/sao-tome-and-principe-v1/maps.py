from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(521);y,x=np.mgrid[0:256,0:256]/256
v=1+.13*np.sin(x*35+np.sin(y*21))*.5+.10*np.cos(y*39+x*13)+rng.normal(0,.07,x.shape)
color=np.stack([74*v,80*v,69*v],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'stone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(193+25*np.sin(x*29)*np.cos(y*32)+rng.normal(0,8,x.shape),0,255))).save(R/'stone-roughness.png',optimize=True)
f=1+.15*np.sin(x*13+y*18)+.1*np.cos(y*27-x*5)+rng.normal(0,.02,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([65*f,98*f,41*f],-1),0,255))).save(R/'forest-color.png',optimize=True)
print('PASS generated 3 compact procedural maps')
