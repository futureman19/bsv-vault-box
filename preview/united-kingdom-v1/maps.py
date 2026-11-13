from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(821);y,x=np.mgrid[:256,:256]/256
v=1+.10*np.sin(y*95+x*7)+.045*np.sin(y*241+x*17)+rng.normal(0,.025,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([77*v,83*v,100*v],-1),0,255))).save(R/'slate-color.png')
Image.fromarray(np.uint8(np.clip(170+28*np.sin(y*95+x*7)+rng.normal(0,3,x.shape),0,255))).save(R/'slate-roughness.png')
v=rng.normal(0,12,x.shape)+12*np.sin(x*31+y*21)
Image.fromarray(np.uint8(np.clip(np.stack([140+v,145+v,132+v],-1),0,255))).save(R/'wall-color.png')
print('MAPS PASS')
