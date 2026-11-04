from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(858);y,x=np.mgrid[0:256,0:256]/256
v=8*np.sin(x*33+y*19)+5*np.sin(y*81-x*13)+rng.normal(0,5,x.shape)
mineral=np.stack([105+v,110+v,99+v],-1)
Image.fromarray(np.uint8(np.clip(mineral,0,255))).save(R/'mineral-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(202+v,0,255))).save(R/'mineral-roughness.png',optimize=True)
w=12*np.sin(x*9+y*17)+7*np.sin(y*43-x*21)+rng.normal(0,3,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([109+w,126+w,49+w*.5],-1),0,255))).save(R/'grass-color.png',optimize=True)
print('MAPS PASS: three deterministic compact authored maps')
