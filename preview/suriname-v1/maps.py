from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1017);n=rng.normal(0,1,(256,256));y,x=np.mgrid[:256,:256];v=8*np.sin(x/19+y/28)+5*np.cos(y/7)+n*9
for name,base in [('stone-color',(78,80,72)),('summit-color',(143,141,124))]:
 a=np.clip(np.array(base)[None,None,:]+v[:,:,None],0,255).astype('uint8');Image.fromarray(a).save(R/(name+'.png'))
a=np.clip(184+n*12,130,225).astype('uint8');Image.fromarray(a).save(R/'stone-roughness.png')
dy,dx=np.gradient(n);a=np.stack([128-dx*3,128-dy*3,np.full_like(n,254)],2);Image.fromarray(np.clip(a,0,255).astype('uint8')).save(R/'stone-normal.png')
print('MAPS PASS')
