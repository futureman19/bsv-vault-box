from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:512,0:512];rng=np.random.default_rng(889)
a=(x//32+y//32)%2;u=np.where(a==0,x,y)%32
v=.89+.11*np.sin(np.pi*u/32)-.13*(u<3)+rng.normal(0,.008,x.shape)
color=np.stack([210*v,166*v,85*v],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'cedar-color.png')
Image.fromarray(np.uint8(np.clip(152+u*1.3,0,255))).save(R/'cedar-roughness.png')
v=.82+.12*np.sin(y*.25+.5*np.sin(x*.02))+rng.normal(0,.015,x.shape)
Image.fromarray(np.uint8(np.stack([90*v,51*v,25*v],-1))).resize((256,256)).save(R/'cedar-end.png')
n=np.clip(90+rng.normal(0,12,(256,256)),0,255).astype('uint8');Image.fromarray(n).save(R/'granite.png')
print('PASS: procedural straw color/roughness and timber maps')
