from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(372);y,x=np.mgrid[0:256,0:256];grain=rng.normal(0,2.7,(256,256));bands=4*np.sin(y*.16+np.sin(x*.045)*.6)+2*np.sin(y*.41+x*.007)
f=grain+bands
rgb=np.clip(np.array([174,177,164])[None,None,:]+f[:,:,None],0,255).astype('uint8')
Image.fromarray(rgb).save(R/'limestone-color.png')
Image.fromarray(np.uint8(np.clip(195+f*1.4,0,255))).save(R/'limestone-roughness.png')
gy,gx=np.gradient(f);normal=np.stack([128-gx*.55,128-gy*.55,np.full_like(f,254)],axis=-1)
Image.fromarray(np.uint8(np.clip(normal,0,255))).save(R/'limestone-normal.png')
print('MAPS PASS',rgb.mean(axis=(0,1)).tolist())
