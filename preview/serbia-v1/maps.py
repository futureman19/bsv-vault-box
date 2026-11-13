from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:512,:512];u=x/512;v=y/512
# Original stepped diamonds, concentric borders, subtle crossed yarn grain.
d=np.abs((u*4)%1-.5)+np.abs((v*3)%1-.5)
step=np.floor(d*10)/10
c=np.zeros((512,512,3))+[156,38,62]
c[step<.3]=[38,57,83];c[step<.2]=[233,213,167];c[step<.1]=[156,38,62]
border=(v<.07)|(v>.93);c[border]=[38,57,83];c[(v>.025)&(v<.045)]=[233,213,167];c[(v>.955)&(v<.975)]=[233,213,167]
grain=np.sin(x*np.pi/2)*3+np.cos(y*np.pi/2)*3
rng=np.random.default_rng(521);c=np.clip(c+grain[:,:,None]+rng.normal(0,1.2,(512,512,1)),0,255).astype('uint8')
Image.fromarray(c).save(R/'weave-color.png')
r=np.clip(215+grain*2,0,255).astype('uint8');Image.fromarray(r).convert('RGB').save(R/'weave-roughness.png')
n=np.zeros((512,512,3),dtype='uint8');n[:,:,0]=(128+12*np.cos(x*np.pi/2)).astype('uint8');n[:,:,1]=(128+12*np.sin(y*np.pi/2)).astype('uint8');n[:,:,2]=254;Image.fromarray(n).save(R/'weave-normal.png')
print('MAPS PASS')
