from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[0:512,0:512];rng=np.random.default_rng(541)
a=x/16;b=y/16;over=(np.floor(a)+np.floor(b))%2
u=np.where(over==0,a%1,b%1);v=np.where(over==0,b%1,a%1)
shade=.83+.17*np.sin(u*np.pi)-.22*(v<.09)-.15*(u<.07)
shade+=.018*np.sin(u*90)+rng.normal(0,.008,x.shape)
color=np.stack([202*shade,165*shade,108*shade],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'weave-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(color*.68,0,255))).resize((256,256)).save(R/'weave-edge.png',optimize=True)
Image.fromarray(np.uint8(np.clip(156+55*(1-shade),0,255))).save(R/'weave-roughness.png',optimize=True)
s=rng.normal(0,1,(256,256));v=np.clip(175+s*14,110,220)
Image.fromarray(np.uint8(np.stack([v*1.08,v,v*.78],-1))).save(R/'limestone.png',optimize=True)
print('PASS procedural pandanus-inspired maps: color, edge, roughness, limestone')
