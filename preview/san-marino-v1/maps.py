from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(734);y,x=np.mgrid[:256,:256];n=rng.normal(0,2.8,x.shape)
v=7*np.sin(x*.045+y*.018)+4*np.sin(y*.13+np.sin(x*.07))+n
color=np.stack([184+v,177+v,161+v],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'stone-color.png')
Image.fromarray(np.uint8(np.clip(190+v,0,255))).save(R/'stone-roughness.png')
gy,gx=np.gradient(v);normal=np.stack([-gx*.002,-gy*.002,np.ones_like(v)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
Image.fromarray(np.uint8((normal*.5+.5)*255)).save(R/'stone-normal.png')
print('PASS procedural maps')
