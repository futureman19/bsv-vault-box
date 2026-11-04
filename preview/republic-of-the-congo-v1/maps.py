from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(692);y,x=np.mgrid[0:512,0:512]/512
phase=x*79+.65*np.sin(y*10+x*6)+.21*np.sin(y*23+x*17)
grain=(.5+.5*np.sin(phase*6.283))**10
v=1-.30*grain+.14*np.sin(x*22+y*4)+rng.normal(0,.025,x.shape)
wood=np.stack([67*v,47*v,31*v],-1)
Image.fromarray(np.uint8(np.clip(wood,0,255))).save(R/'forest-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(wood*.68,0,255))).resize((256,256)).save(R/'forest-end.png',optimize=True)
Image.fromarray(np.uint8(np.clip(156+grain*55,0,255))).save(R/'forest-roughness.png',optimize=True)
speck=np.clip(90+rng.normal(0,23,(256,256)),30,160)
Image.fromarray(np.uint8(np.stack([speck*1.1,speck*.96,speck*.77],-1))).save(R/'granite.png',optimize=True)
print('PASS generated forest maps')
