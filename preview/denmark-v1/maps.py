from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1728);y,x=np.mgrid[0:256,0:512]
n=rng.normal(0,1,(256,512));v=3*np.sin(y*.15+1.2*np.sin(x*.025))+2*n
c=np.stack([224+v,220+v,207+v],axis=-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'chalk-color.png')
r=np.uint8(np.clip(208+v*2,0,255));Image.fromarray(r).save(R/'chalk-roughness.png')
f=np.stack([49+v*2,54+v*2,57+v*2],axis=-1);Image.fromarray(np.uint8(np.clip(f,0,255))).save(R/'flint-color.png')
print('PROCEDURAL_MAPS PASS')
