from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1776);y,x=np.mgrid[0:512,0:512]/512
warp=y+.014*np.sin(x*13)+.006*np.sin(x*37+y*12)
v=.84+.12*np.sin(warp*65)+.06*np.sin(warp*187)+rng.normal(0,.018,x.shape)
color=np.stack([177*v,99*v,61*v],-1)
vein=np.sin(warp*112+np.sin(x*23))>.95
color[vein]=color[vein]*.55+np.array([219,181,128])*.45
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'strata-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(190+22*np.sin(warp*65)+rng.normal(0,3,x.shape),0,255))).save(R/'strata-roughness.png',optimize=True)
n=rng.normal(0,5,(256,256));Image.fromarray(np.uint8(np.clip(np.stack([208+n,177+n,133+n],-1),0,255))).save(R/'limestone.png',optimize=True)
print('MAPS PASS')
