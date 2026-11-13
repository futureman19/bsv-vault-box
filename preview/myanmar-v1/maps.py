from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:512,0:512];u=x%128;v=y%128
d=np.abs(u-64)+np.abs(v-64)
lines=(np.abs(d-44)<1.5)|(np.abs(d-54)<1.2)|(y%128<3)|(y%128>123)
rng=np.random.default_rng(71);noise=rng.uniform(-2,2,(512,512))
a=np.zeros((512,512,3));a[:]=[24,12,10];a[lines]=[176,44,28];a+=noise[:,:,None];Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'lacquer-color.png')
r=np.uint8(np.clip(65+noise*3+lines*14,0,255));Image.fromarray(r).save(R/'lacquer-roughness.png')
a[:]=[112,23,15];a+=noise[:,:,None];Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'lining.png')
print('MAPS PASS')
