from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:256,0:512];rng=np.random.default_rng(763)
colors=np.zeros((256,512,3))+[36,53,85]
# Original stripes, no community-specific or sacred designs.
for a,b,c in [(35,44,[168,62,72]),(47,51,[216,201,161]),(55,60,[195,154,80]),(190,199,[168,62,72]),(202,206,[216,201,161]),(210,215,[195,154,80])]:colors[a:b]=c
weave=1+.07*np.sin(x*np.pi/2)*np.cos(y*np.pi/2)+rng.normal(0,.012,x.shape)
Image.fromarray(np.uint8(np.clip(colors*weave[:,:,None],0,255))).save(R/'weave-color.png')
rough=180+20*np.sin(x*np.pi/2)*np.cos(y*np.pi/2)
Image.fromarray(np.uint8(rough)).save(R/'weave-roughness.png')
n=np.stack([128+7*np.sin(x*np.pi/2),128+7*np.sin(y*np.pi/2),np.full(x.shape,254)],-1)
Image.fromarray(np.uint8(n)).save(R/'weave-normal.png')
noise=rng.normal(0,7,(256,256));stone=np.stack([48+noise,57+noise,59+noise],-1)
Image.fromarray(np.uint8(np.clip(stone,0,255))).save(R/'stone-color.png')
print('MAPS PASS')
