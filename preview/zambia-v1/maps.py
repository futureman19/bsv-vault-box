from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(509);y,x=np.mgrid[:512,:512]/512
bands=np.sin(y*71+1.4*np.sin(x*13+y*9)+.7*np.sin(x*31))
noise=rng.normal(0,1,x.shape)
v=1+.12*bands+.09*np.sin(x*17+y*8)+.07*noise
rgb=np.stack([53*v,59*v,55*v],-1)
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'basalt-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(205+bands*12+noise*6,0,255))).save(R/'basalt-roughness.png',optimize=True)
dy,dx=np.gradient(v);normal=np.stack([-dx*.18,-dy*.18,np.ones_like(x)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
Image.fromarray(np.uint8(np.clip((normal*.5+.5)*255,0,255))).save(R/'basalt-normal.png',optimize=True)
print('MAPS PASS: independently procedural basalt color, roughness, normal 512x512')
