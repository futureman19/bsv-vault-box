"""Original seeded coral-stone interpretation; no sourced image pixels."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1364);n=512
coarse=Image.fromarray(rng.integers(0,255,(32,32),dtype=np.uint8)).resize((n,n),Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(4))
a=np.asarray(coarse,dtype=float)/255
pores=rng.random((n,n))<.035
v=(a-.5)*25+rng.normal(0,2,(n,n))-pores*rng.uniform(12,38,(n,n))
rgb=np.clip(np.array([198,178,143])+v[:,:,None],0,255).astype('uint8')
Image.fromarray(rgb).save(R/'stone-color.png')
rough=np.clip(183+(a-.5)*36+pores*20,0,255).astype('uint8');Image.fromarray(rough).save(R/'stone-roughness.png')
h=np.asarray(Image.fromarray(np.clip(v+128,0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(.6)),float)
dy,dx=np.gradient(h/255);norm=np.stack([-dx*.5,-dy*.5,np.ones_like(dx)],axis=-1);norm/=np.linalg.norm(norm,axis=-1)[:,:,None]
Image.fromarray(np.clip((norm*.5+.5)*255,0,255).astype('uint8')).save(R/'stone-normal.png')
print('MAPS PASS: 3 original 512x512 maps')
