from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(241);n=512
y,x=np.mgrid[0:n,0:n];grain=np.sin(y*.70+np.sin(x*.025)*1.5)+.5*np.sin(y*2.1+x*.008);noise=rng.normal(0,1,(n,n));v=grain*4+noise*1.5
rgb=np.stack([76+v*1.5,49+v,34+v*.7],axis=-1)
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'timber-color.png')
Image.fromarray(np.uint8(np.clip(155+v*3,0,255))).save(R/'timber-roughness.png')
Image.fromarray(np.uint8(np.clip(rgb*.78,0,255))).save(R/'timber-end.png')
normal=np.stack([np.full_like(v,128),128+np.gradient(v,axis=0)*.6,np.full_like(v,254)],axis=-1)
Image.fromarray(np.uint8(np.clip(normal,0,255))).save(R/'timber-normal.png')
v=rng.normal(0,18,(256,256));Image.fromarray(np.uint8(np.clip(np.stack([78+v,75+v,70+v],-1),0,255))).save(R/'granite.png')
print('MAPS PASS')
