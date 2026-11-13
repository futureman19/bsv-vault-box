from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:512,:512];rng=np.random.default_rng(2026)
weave=4*np.sin(x*np.pi/2)+3*np.cos(y*np.pi/2)+rng.normal(0,1.5,(512,512))
a=np.empty((512,512,3));a[:]=[119,31,43];a+=weave[:,:,None]
# Thin recurring geometric bands on textile cladding, not wood grain.
stripe=(np.abs((y%128)-64)<3);a[stripe]=[181,140,95]
Image.fromarray(np.clip(a,0,255).astype('uint8')).save(R/'weave-color.png')
Image.fromarray(np.clip(205+weave*2,0,255).astype('uint8')).save(R/'weave-roughness.png')
for name,c in [('edge.png',[72,17,28]),('foot.png',[43,40,38])]:
 b=np.zeros((256,256,3))+c+ rng.normal(0,3,(256,256,1));Image.fromarray(np.clip(b,0,255).astype('uint8')).save(R/name)
print('MAPS PASS')
