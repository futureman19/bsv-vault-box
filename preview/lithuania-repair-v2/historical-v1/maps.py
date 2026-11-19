from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(994);y,x=np.mgrid[0:512,0:512]/512
v=.5+.22*np.sin(2*np.pi*(18*y+.25*np.sin(9*x)+.1*np.sin(31*x)))+.07*rng.normal(size=x.shape)
a=np.stack([181+37*v,149+34*v,99+32*v],axis=2)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'sand-color.png')
Image.fromarray(np.uint8(np.clip(180+40*v,0,255))).save(R/'sand-roughness.png')
w=.5+.25*np.sin(16*x+3*np.sin(9*y))+.04*rng.normal(size=x.shape)
Image.fromarray(np.uint8(np.stack([28+18*w,97+42*w,103+41*w],axis=2))).resize((256,256)).save(R/'lagoon.png')
print('MAPS PASS')
