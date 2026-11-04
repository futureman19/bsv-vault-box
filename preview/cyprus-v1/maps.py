from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:512,:512];rng=np.random.default_rng(255)
a=np.sin(x*np.pi/4);b=np.sin(y*np.pi/4)
h=.5+.18*a+.18*b+.10*a*b
noise=rng.normal(0,1.7,(512,512));shade=(h-.5)*25+noise
color=np.clip(np.array([115,78,47])[None,None,:]+shade[:,:,None],0,255).astype('uint8')
Image.fromarray(color).save(R/'linen-color.png')
rough=np.clip(195+(h-.5)*35,0,255).astype('uint8');Image.fromarray(rough).convert('RGB').save(R/'linen-roughness.png')
gy,gx=np.gradient(h);normal=np.stack([-gx*.7,-gy*.7,np.ones_like(h)],axis=-1);normal/=np.linalg.norm(normal,axis=-1)[:,:,None];Image.fromarray(((normal*.5+.5)*255).astype('uint8')).save(R/'linen-normal.png')
print('MAPS PASS 512x512 procedural woven color / roughness / normal')
