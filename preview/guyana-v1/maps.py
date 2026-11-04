from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent; (R/'maps').mkdir(exist_ok=True)
rng=np.random.default_rng(741); y,x=np.mgrid[0:256,0:512];n=rng.normal(0,1,x.shape)
def noise(w,h):
 a=Image.fromarray(rng.integers(0,256,(h,w),dtype='uint8'));return np.asarray(a.resize((512,256),Image.Resampling.BICUBIC)).astype(float)/255-.5
coarse=noise(24,12);medium=noise(90,45)
w=y+coarse*34+5*np.sin(x/37+y/42);strata=np.sin(w*.17)
f=coarse*47+medium*25+strata*3+n*3
# Mineral pores and scattered warm grains break the former wood-like waves.
f-=np.where(rng.random(x.shape)<.025,rng.uniform(6,24,x.shape),0)
c=np.clip(np.array([128,94,61])[None,None,:]+f[:,:,None]*np.array([1,.86,.65]),0,255).astype('uint8')
Image.fromarray(c).save(R/'maps/sandstone-color.png'); rough=np.clip(190+strata*12+n*3,0,255).astype('uint8');Image.fromarray(rough).save(R/'maps/sandstone-roughness.png')
dy,dx=np.gradient(f/255); normal=np.stack([-dx*.7,-dy*.7,np.ones_like(dx)],axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True);Image.fromarray(((normal*.5+.5)*255).astype('uint8')).save(R/'maps/sandstone-normal.png')
print('MAPS_PASS 512x256 procedural sandstone color roughness normal')
