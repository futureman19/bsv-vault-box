from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(421); n=256
small=Image.fromarray(rng.integers(0,255,(32,32),dtype=np.uint8)).resize((n,n),Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(2))
f=(np.asarray(small,dtype=float)-128)/128;grain=rng.normal(0,1.8,(n,n));v=f*12+grain
color=np.clip(np.array([204,190,162])[None,None,:]+v[:,:,None],0,255).astype('uint8');Image.fromarray(color).save(R/'stone-color.png')
rough=np.clip(190+f*20+grain,0,255).astype('uint8');Image.fromarray(rough).convert('RGB').save(R/'stone-roughness.png')
gy,gx=np.gradient(v);normal=np.stack([128-gx*.6,128-gy*.6,np.full_like(v,254)],axis=2);Image.fromarray(np.clip(normal,0,255).astype('uint8')).save(R/'stone-normal.png')
print('MAPS_PASS')
