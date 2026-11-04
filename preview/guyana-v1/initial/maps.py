from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent; (R/'maps').mkdir(exist_ok=True)
rng=np.random.default_rng(741); y,x=np.mgrid[0:256,0:512];n=rng.normal(0,1,x.shape)
w=y+3*np.sin(x/53)+1.6*np.sin(x/17+y/21); strata=np.sin(w*.38)+.35*np.sin(w*1.7);f=strata*10+n*2
c=np.clip(np.array([121,81,59])[None,None,:]+f[:,:,None]*np.array([1,.82,.6]),0,255).astype('uint8')
Image.fromarray(c).save(R/'maps/sandstone-color.png'); rough=np.clip(190+strata*12+n*3,0,255).astype('uint8');Image.fromarray(rough).save(R/'maps/sandstone-roughness.png')
dy,dx=np.gradient(f/255); normal=np.stack([-dx*.7,-dy*.7,np.ones_like(dx)],axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True);Image.fromarray(((normal*.5+.5)*255).astype('uint8')).save(R/'maps/sandstone-normal.png')
print('MAPS_PASS 512x256 procedural sandstone color roughness normal')
