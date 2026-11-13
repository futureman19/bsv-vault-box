from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(710);n=256
y,x=np.mgrid[:n,:n];grain=rng.normal(0,3,(n,n));fiber=2*np.sin(x*.9+y*.41)+2*np.sin(x*.13-y*1.4)
c=np.clip(np.array([211,199,169])[None,None,:]+(grain+fiber)[:,:,None],0,255).astype('uint8')
Image.fromarray(c).save(R/'felt-color.png')
r=np.clip(218+grain*2+fiber,0,255).astype('uint8');Image.fromarray(r).save(R/'felt-roughness.png')
g=np.clip(np.array([104,122,53])[None,None,:]+(grain*1.3+8*np.sin(x*.06)*np.cos(y*.04))[:,:,None],0,255).astype('uint8');Image.fromarray(g).save(R/'steppe-color.png')
print('MAPS PASS')
