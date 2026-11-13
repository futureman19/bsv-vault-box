from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1106);y,x=np.mgrid[0:512,0:512]/512
p=np.array([[169,84,63],[204,151,79],[221,196,154],[100,107,98],[139,89,77],[174,147,112]])
f=(y*7+x*1.5+.17*np.sin(x*13)+.055*np.sin(x*41+y*9))%6
i=np.floor(f).astype(int);t=np.clip((f%1-.78)/.22,0,1)[...,None]
a=p[i]*(1-t)+p[(i+1)%6]*t+rng.normal(0,2.4,(512,512,1))
Image.fromarray(np.uint8(a.clip(0,255))).save(R/'strata-color.png')
r=180+20*np.sin(f*4)+rng.normal(0,3,(512,512))
Image.fromarray(np.uint8(r.clip(0,255))).save(R/'strata-roughness.png')
g=rng.normal(0,12,(256,256,1))+np.array([80,70,62]);Image.fromarray(np.uint8(g.clip(0,255))).save(R/'feet-color.png')
print('MAPS PASS')
