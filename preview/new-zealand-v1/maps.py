from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(644);y,x=np.mgrid[0:512,0:512]/512
phase=y*23+1.2*np.sin(x*8+y*4)+.28*np.sin(x*29-y*16)
vein=(.5+.5*np.sin(phase*6.283))**24
v=.86+.15*np.sin(y*28+x*3)+rng.normal(0,.035,x.shape)
a=np.stack([64*v+65*vein,76*v+66*vein,78*v+64*vein],-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'gneiss-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(167+vein*38+12*np.sin(y*40),0,255))).save(R/'gneiss-roughness.png',optimize=True)
s=np.clip(rng.normal(112,18,(256,256)),40,180)
Image.fromarray(np.uint8(np.stack([s*.94,s,s*.98],-1))).save(R/'rock.png',optimize=True)
dy,dx=np.gradient(v+.10*vein)
n=np.stack([-dx*.5,-dy*.5,np.ones_like(dx)],-1);n/=np.linalg.norm(n,axis=-1,keepdims=True)
Image.fromarray(np.uint8(np.clip((n*.5+.5)*255,0,255))).save(R/'gneiss-normal.png',optimize=True)
print('MAPS PASS: 512px gneiss color/roughness/normal; 256px rock')
