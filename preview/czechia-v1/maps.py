from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(431);y,x=np.mgrid[:256,:256];n=rng.normal(0,1,(256,256));f=3*np.sin(x*.13)*np.cos(y*.09)+n*1.2
for name,base,scale in [('cobalt',[20,55,110],1),('roughness',[57,57,57],1.5),('stone',[65,80,95],3)]:
 a=np.clip(np.array(base)[None,None,:]+f[:,:,None]*scale,0,255).astype('uint8');Image.fromarray(a).save(R/(name+'.png'))
