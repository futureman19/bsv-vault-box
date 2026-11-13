from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(621);y,x=np.mgrid[:256,:256];grain=rng.normal(0,3,(256,256));v=224+7*np.sin(y*.12+np.sin(x*.04))+grain
c=np.stack([v+3,v+2,v],axis=-1);Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'salt-color.png')
r=np.clip(175+grain*3+8*np.sin(y*.12),130,220).astype('uint8');Image.fromarray(r).save(R/'salt-roughness.png')
n=np.stack([128+grain*.6,128+np.roll(grain,1,0)*.6,np.full_like(grain,254)],axis=-1);Image.fromarray(np.uint8(np.clip(n,0,255))).save(R/'salt-normal.png')
