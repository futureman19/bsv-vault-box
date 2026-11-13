from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
r=np.random.default_rng(605);y,x=np.mgrid[:256,:256];n=r.normal(0,6,(256,256));v=n+3*np.sin(x*.13+y*.08)
c=np.stack([55+v,61+v,66+v],-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'stone-color.png')
Image.fromarray(np.uint8(np.clip(190+n*2,0,255))).save(R/'stone-roughness.png')
print('MAPS PASS')
