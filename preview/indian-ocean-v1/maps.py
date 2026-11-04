from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(188);y,x=np.mgrid[0:384,0:384]/384
p=12*y+2*np.sin(x*8+y*3)+.8*np.sin(x*19-y*10)
v=.5+.23*np.sin(p)+.14*np.cos(x*18-y*9)+rng.normal(0,.015,x.shape)
line=np.exp(-((np.sin(p*2+.3*np.cos(x*31)))/.08)**2)
c=np.stack([18+30*v+12*line,46+66*v+15*line,64+65*v+12*line],-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'ocean-color.png')
Image.fromarray(np.uint8(110+65*v)).save(R/'ocean-roughness.png')
dy,dx=np.gradient(v);normal=np.stack([-dx*1.2,-dy*1.2,np.ones_like(v)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
Image.fromarray(np.uint8((normal*.5+.5)*255)).save(R/'ocean-normal.png')
y,x=np.mgrid[0:256,0:256];s=rng.normal(0,4,x.shape)+5*np.sin(x*.08)*np.cos(y*.12)
Image.fromarray(np.uint8(np.clip(np.stack([211+s,201+s,171+s],-1),0,255))).save(R/'limestone.png')
print('PASS procedural maps')
