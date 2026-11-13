from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(868)
y,x=np.mgrid[0:256,0:256]/256
h=np.sin(x*127+np.sin(y*91))*np.sin(y*153+np.sin(x*71))
v=1+.065*h+rng.normal(0,.009,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([154*v,26*v,36*v],-1),0,255))).save(R/'enamel-color.png')
Image.fromarray(np.uint8(85+18*h)).save(R/'enamel-roughness.png')
g=np.clip(35+rng.normal(0,3,(128,128)),22,48)
Image.fromarray(np.uint8(np.stack([g,g*1.05,g*1.1],-1))).save(R/'graphite.png')
print('MAPS PASS: procedural enamel colour/roughness and graphite')
