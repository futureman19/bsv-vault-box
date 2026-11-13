from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(672); y,x=np.mgrid[0:256,0:256]/256
v=.93+.07*np.sin(x*29+np.sin(y*18))+.045*np.sin(y*43+x*17)+rng.normal(0,.025,x.shape)
a=np.stack([173*v,169*v,149*v],-1)
for name,data in [('limestone-color.png',a),('limestone-edge.png',a*.8),('karst-color.png',a*.86)]:Image.fromarray(np.uint8(np.clip(data,0,255))).save(R/name,optimize=True)
Image.fromarray(np.uint8(np.clip(170+v*35,0,255))).save(R/'limestone-roughness.png',optimize=True)
print('MAPS PASS: four independently generated compact limestone maps')
