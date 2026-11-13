from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(105)
y,x=np.mgrid[:256,:256];grain=rng.normal(0,7,(256,256));broad=5*np.sin(x*.043)*np.cos(y*.051)
a=np.clip(68+grain+broad,30,110)
Image.fromarray(np.uint8(np.stack([a*.85,a,a*.98],axis=-1))).save(R/'basalt-color.png')
r=np.uint8(np.clip(175+grain*2+broad,110,230));Image.fromarray(r).convert('RGB').save(R/'basalt-roughness.png')
b=np.clip(172+grain*.9+broad,130,220);Image.fromarray(np.uint8(np.stack([b,b*1.02,b*.92],axis=-1))).save(R/'pale-color.png')
print('MAPS PASS')
