from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(722);y,x=np.mgrid[0:256,0:256]/256
v=.91+.07*np.sin(x*24+y*11)+.06*np.cos(y*37-x*15)+rng.normal(0,.045,x.shape)
for name,color in [('stone-color',(119,112,91)),('stone-detail',(83,80,67)),('granite',(91,87,70))]:
 Image.fromarray(np.uint8(np.clip(np.stack([c*v for c in color],-1),0,255))).save(R/(name+'.png'))
Image.fromarray(np.uint8(np.clip(180+v*35,0,255))).save(R/'stone-roughness.png')
print('PASS compact mineral maps generated')
