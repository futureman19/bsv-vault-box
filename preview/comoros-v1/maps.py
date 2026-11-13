from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(773);n=512
y,x=np.mgrid[:n,:n];grain=rng.normal(0,5,(n,n));field=4*np.sin(x*.071+np.sin(y*.033)*2)+3*np.cos(y*.057)
pore=rng.random((n,n))>.975
base=np.stack([52+field+grain,61+field+grain,60+field+grain],axis=-1);base[pore]*=.55
Image.fromarray(np.uint8(np.clip(base,0,255))).save(R/'basalt-color.png')
rough=np.clip(205+grain*2+pore*25,0,255).astype('uint8');Image.fromarray(rough).save(R/'basalt-roughness.png')
h=(field+grain-pore*15)/255;dy,dx=np.gradient(h);v=np.stack([-dx*1.2,-dy*1.2,np.ones_like(dx)],axis=-1);v/=np.linalg.norm(v,axis=-1)[...,None]
Image.fromarray(np.uint8(np.clip((v*.5+.5)*255,0,255))).save(R/'basalt-normal.png')
print('MAPS PASS: three deterministic 512px authored basalt maps')
