from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(237);y,x=np.mgrid[0:512,0:512]/512
cloud=np.sin(x*24+2*np.sin(y*17))+np.sin(y*31+x*11)+.5*np.sin(x*91-y*74)
grains=rng.normal(0,1,x.shape)
v=cloud*4+grains*3
color=np.stack([71+v,62+v*.9,53+v*.8],-1)
# Sparse mineral flecks; independently authored, not photographed stone.
fleck=rng.random(x.shape)>.993;color[fleck]+=[25,14,5]
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'basalt-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(204+cloud*5+grains*4,0,255))).save(R/'basalt-roughness.png',optimize=True)
dy,dx=np.gradient(v);normal=np.stack([-dx*.25,-dy*.25,np.full_like(dx,24)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
Image.fromarray(np.uint8(np.clip((normal*.5+.5)*255,0,255))).save(R/'basalt-normal.png',optimize=True)
print('MAPS PASS: three generated 512x512 portable basalt maps')
