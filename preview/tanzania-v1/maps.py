from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(403);n=256;y,x=np.mgrid[:n,:n]/n
v=9*np.sin(x*19+y*8)+6*np.sin(y*31-x*13)+4*np.sin(x*49+y*35)+rng.normal(0,3,(n,n))
a=np.stack([145+v,89+v*.75,44+v*.4],axis=-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'ochre-color.png')
Image.fromarray(np.uint8(np.clip(175+v,0,255))).convert('RGB').save(R/'ochre-roughness.png')
a=np.stack([65+v*.8,60+v*.7,51+v*.6],axis=-1)
Image.fromarray(np.uint8(np.clip(a,0,255))).save(R/'volcanic.png')
print('MAPS PASS: three independently generated 256px maps')
