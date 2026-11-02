from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(521);y,x=np.mgrid[0:512,0:512]
u=x/32;v=y/32;fx=u%1;fy=v%1
horizontal=((np.floor(u)+np.floor(v))%2)==0
across=np.where(horizontal,fy,fx);along=np.where(horizontal,fx,fy)
height=np.sin(np.pi*np.clip((across-.04)/.92,0,1))**.35
height*=np.where((across<.04)|(across>.96),.08,1)
fiber=.035*np.sin(across*210)+.02*np.sin(across*503+along*3)
value=.68+.28*height+fiber+rng.normal(0,.008,x.shape)
color=np.stack([183*value,138*value,79*value],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'bamboo-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(160+32*(1-height),0,255))).save(R/'bamboo-roughness.png',optimize=True)
dy,dx=np.gradient(height);n=np.stack([-dx*2,-dy*2,np.ones_like(dx)],-1);n/=np.linalg.norm(n,axis=-1,keepdims=True)
Image.fromarray(np.uint8((n*.5+.5)*255)).save(R/'bamboo-normal.png',optimize=True)
y,x=np.mgrid[0:256,0:256];grain=.9+.09*np.sin(y*.8+.2*np.sin(x*.08))+rng.normal(0,.015,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([103*grain,70*grain,42*grain],-1),0,255))).save(R/'bamboo-frame.png',optimize=True)
v=155+18*np.sin(x*.07+y*.017)+rng.normal(0,8,x.shape)
Image.fromarray(np.uint8(np.clip(np.stack([v*1.04,v*1.03,v*.96],-1),0,255))).save(R/'limestone.png',optimize=True)
print('MAPS PASS: five portable maps generated')
