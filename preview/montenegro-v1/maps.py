from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(100);y,x=np.mgrid[0:512,0:512]/512
v=5*np.sin(x*31+y*13)+4*np.sin(x*59-y*37)+rng.normal(0,2,x.shape)
crack=np.maximum(0,1-np.abs(np.sin((x*6+y*4+.08*np.sin(y*27))*np.pi))/.025)
v-=crack*36
rgb=np.stack([160+v,163+v,157+v],-1)
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'limestone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(184+v*.7,0,255))).save(R/'limestone-roughness.png',optimize=True)
noise=rng.normal(0,6,(256,256));a=np.stack([40+noise,66+noise,42+noise],-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'forest-color.png',optimize=True)
print('PASS procedural maps')
