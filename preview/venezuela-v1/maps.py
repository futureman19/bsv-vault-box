from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(701);y,x=np.mgrid[0:512,0:512]/512
# Multiscale weathering interrupts strata; no continuous wood-like pinstripes.
coarse=np.asarray(Image.fromarray(np.uint8(rng.uniform(0,255,(24,24)))).resize((512,512),Image.Resampling.BICUBIC))/255
medium=np.asarray(Image.fromarray(np.uint8(rng.uniform(0,255,(80,80)))).resize((512,512),Image.Resampling.BICUBIC))/255
phase=y*8+.7*coarse+.22*np.sin(x*13)
vein=np.exp(-((np.sin(phase*3.14159))/.10)**2)*(coarse>.45)
v=.72+.48*coarse+.20*(medium-.5)-.17*vein+rng.normal(0,.045,x.shape)
c=np.stack([150*v,85*v,58*v],-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'stone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(190+vein*35+rng.normal(0,5,x.shape),0,255))).save(R/'stone-roughness.png',optimize=True)
v=.8+.2*np.sin(x*21)*np.cos(y*19)+rng.normal(0,.07,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([72*v,94*v,39*v],-1),0,255))).resize((256,256)).save(R/'summit.png',optimize=True)
print('MAPS PASS')
