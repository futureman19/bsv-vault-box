from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(228);y,x=np.mgrid[:256,:512];phase=y/256*11+.06*np.sin(x/38)+.025*np.sin(x/11)
course=np.exp(-((phase%1)/.11)**2);v=1-.12*course+.045*np.sin(y/29+x/113)+rng.normal(0,.028,x.shape)
color=np.stack([174*v,113*v,70*v],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'earth-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(202+course*20+rng.normal(0,7,x.shape),0,255))).save(R/'earth-roughness.png',optimize=True)
a=np.clip(100+rng.normal(0,16,(128,128)),45,155)
Image.fromarray(np.uint8(np.stack([a*1.25,a*.86,a*.55],-1))).save(R/'stone.png',optimize=True)
print('PASS procedural earth and stone maps')
