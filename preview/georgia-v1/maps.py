from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(709);n=256
y,x=np.mgrid[:n,:n];v=rng.normal(0,4,(n,n))+5*np.sin(x*.043+y*.024)+3*np.sin(y*.13)
# Independent weathered mineral grain, not photographic masonry.
c=np.stack([139+v,130+v,112+v],-1).clip(0,255).astype('uint8');Image.fromarray(c).save(R/'stone-color.png')
r=(200+v*.7).clip(0,255).astype('uint8');Image.fromarray(r).save(R/'stone-roughness.png')
dy,dx=np.gradient(v);norm=np.stack([-dx*.65,-dy*.65,np.full_like(v,128)],-1);norm=norm/np.linalg.norm(norm,axis=-1,keepdims=True);Image.fromarray(((norm*.5+.5)*255).astype('uint8')).save(R/'stone-normal.png')
print('MAPS PASS 256x256 procedural color/roughness/normal')
