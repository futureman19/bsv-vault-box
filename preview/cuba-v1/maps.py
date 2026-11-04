from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(840);y,x=np.mgrid[:256,:256]/256
v=.94+.07*np.sin(x*32+y*18)+.035*np.sin(x*121-y*67)+rng.normal(0,.025,x.shape)
for name,c in [('limestone',(176,169,145)),('earth',(135,62,34))]:
 a=np.clip(v[...,None]*np.array(c),0,255).astype('uint8');Image.fromarray(a).save(R/(name+'.png'))
Image.fromarray(np.uint8(np.clip(180+(v-1)*95,0,255))).save(R/'roughness.png')
print('MAPS PASS')
