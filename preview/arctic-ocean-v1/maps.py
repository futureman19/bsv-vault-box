from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(201);y,x=np.mgrid[0:512,0:512]/512
f=np.sin(x*28+3*np.sin(y*13)+.5*np.sin(x*71+y*19))
vein=np.exp(-((f-.83)/.08)**2);broad=.5+.5*np.sin(y*17+x*5);grain=rng.normal(0,1,(512,512))
color=np.stack([19+15*broad+34*vein+grain,61+21*broad+52*vein+grain,82+24*broad+54*vein+grain],axis=-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'ocean-color.png')
r=np.uint8(np.clip(100+30*broad+24*vein+grain,0,255));Image.fromarray(r).save(R/'ocean-roughness.png')
gy,gx=np.gradient(vein);normal=np.stack([128-gx*25,128-gy*25,np.full_like(x,254)],axis=-1);Image.fromarray(np.uint8(np.clip(normal,0,255))).save(R/'ocean-normal.png')
print('MAPS PASS: three generated 512x512 maps')
