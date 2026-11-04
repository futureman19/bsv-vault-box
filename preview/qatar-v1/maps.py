from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(701);n=256
y,x=np.mgrid[0:n,0:n];grain=rng.normal(0,1,(n,n));v=3*np.sin(x*.07+y*.023)+2*np.cos(y*.16)+grain*4
rgb=np.stack([204+v,177+v,133+v],axis=-1).clip(0,255).astype('uint8');Image.fromarray(rgb).save(R/'sand-color.png')
r=(182+grain*9).clip(0,255).astype('uint8');Image.fromarray(r).save(R/'sand-roughness.png')
gy,gx=np.gradient(grain);normal=np.stack([128+gx*4,128+gy*4,np.full_like(gx,254)],axis=-1).clip(0,255).astype('uint8');Image.fromarray(normal).save(R/'sand-normal.png')
print('MAPS PASS')
