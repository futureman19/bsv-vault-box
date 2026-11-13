from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1386);n=384
# Multiscale, isotropic pores: original generated imagery, no photo inputs.
def soft(size):
 a=Image.fromarray(np.uint8(rng.uniform(0,255,(size,size))))
 return np.asarray(a.resize((n,n),Image.Resampling.BICUBIC),dtype=float)/255-.5
v=soft(12)*.16+soft(50)*.11+soft(190)*.06
pores=rng.random((n,n))>.982
v-=pores*.19
color=np.stack([(207*(1+v)),(201*(1+v)),(175*(1+v))],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'limestone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(192-v*90,0,255))).save(R/'limestone-roughness.png',optimize=True)
v=soft(24)*.22+soft(120)*.14
Image.fromarray(np.uint8(np.clip(np.stack([66*(1+v),112*(1+v),67*(1+v)],-1),0,255))).save(R/'forest-color.png',optimize=True)
y,x=np.mgrid[:n,:n]/n
v=.06*np.sin(x*24+y*9)+.04*np.sin(y*40-x*5)+soft(30)*.09
Image.fromarray(np.uint8(np.clip(np.stack([36+v*75,143+v*130,148+v*110],-1),0,255))).save(R/'lagoon-color.png',optimize=True)
print('PASS procedural maps')
