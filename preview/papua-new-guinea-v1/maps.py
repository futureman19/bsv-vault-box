from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
N=512;y,x=np.mgrid[0:N,0:N]/N
# Staggered elliptical loop strands, not an orthogonal basket weave.
row=np.floor(y*18);u=((x*28+row*.5)%1-.5)*2;v=((y*18)%1-.5)*2
d=np.abs(np.sqrt((u/.73)**2+(v/.91)**2)-1)
strand=np.exp(-(d/.14)**2);twist=np.sin(x*1800+y*1200)*.035
h=np.clip(strand*(.85+twist),0,1)
rng=np.random.default_rng(612);noise=rng.normal(0,1.4,(N,N))
base=np.array([185,145,87.]);c=base[None,None,:]*(.48+.52*h[:,:,None])+noise[:,:,None]
accent=(np.floor(y*18)%9==0);c[accent]*=np.array([.77,.60,.63])
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'fibre-color.png',optimize=True)
rough=np.uint8(np.clip(214-39*h+noise,0,255));Image.fromarray(rough).save(R/'fibre-roughness.png',optimize=True)
dy,dx=np.gradient(h);normal=np.stack([-dx*1.1,-dy*1.1,np.ones_like(h)],axis=2);normal/=np.linalg.norm(normal,axis=2)[:,:,None]
Image.fromarray(np.uint8((normal*.5+.5)*255)).save(R/'fibre-normal.png',optimize=True)
print('MAPS PASS',len(list(R.glob('*.png'))))
