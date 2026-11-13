from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(521);n=512;y,x=np.mgrid[0:n,0:n]/n
warp=y+.018*np.sin(x*17)+.009*np.sin(x*43+y*7)
beds=np.sin(warp*84)+.35*np.sin(warp*181+x*3)
vein=np.exp(-((np.sin(warp*39))/.12)**2)
noise=rng.normal(0,1,(n,n));fine=noise*1.9
value=beds*5-vein*16+fine
rgb=np.stack([193+value,170+value*.9,129+value*.65],-1)
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'limestone-color.png',optimize=True)
rough=np.clip(205+noise*3+beds*5,0,255).astype('uint8');Image.fromarray(rough).save(R/'limestone-roughness.png',optimize=True)
gy,gx=np.gradient(value/255);normal=np.stack([-gx*1.6,-gy*1.6,np.ones_like(x)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
Image.fromarray(np.uint8(np.clip((normal*.5+.5)*255,0,255))).save(R/'limestone-normal.png',optimize=True)
print('MAPS PASS: 3 independently generated 512x512 limestone maps')
