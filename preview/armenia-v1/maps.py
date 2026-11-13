from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(624);n=256
y,x=np.mgrid[:n,:n];broad=6*np.sin(x/21+y/33)+4*np.sin(y/13-x/39);grain=rng.normal(0,4,(n,n));pores=rng.random((n,n))<.035
rgb=np.stack([177+broad+grain,111+broad+grain,94+broad+grain],axis=2);rgb[pores]-=28
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'tuff-color.png')
r=np.clip(183+grain*2+pores*26,0,255).astype('uint8');Image.fromarray(r).convert('RGB').save(R/'tuff-roughness.png')
r=np.clip(51+rng.normal(0,10,(n,n)),0,255).astype('uint8');Image.fromarray(np.stack([r,r,r],2)).save(R/'basalt-color.png')
print('MAPS PASS')
