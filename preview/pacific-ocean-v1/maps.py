from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:512,0:512]/512
rng=np.random.default_rng(2601)
a=np.sin(16*x+5*np.sin(8*y)+2*np.cos(13*x-9*y))*.5+.5
b=np.sin(42*y+4*np.sin(12*x))*.5+.5
noise=rng.random(x.shape)
f=.65*a+.25*b+.10*noise
c=np.stack([12+16*f,46+54*f,67+48*f],axis=-1)
Image.fromarray(c.astype('uint8')).save(R/'ocean-color.png')
Image.fromarray((65+35*f).astype('uint8')).save(R/'ocean-roughness.png')
v=(25+35*rng.random((256,256))).astype('uint8');Image.fromarray(np.stack([v,v+3,v+6],axis=-1)).save(R/'basalt.png')
print('MAPS PASS: deterministic authored ocean color/roughness and basalt')
