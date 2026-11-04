from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
r=np.random.default_rng(196);n=r.normal(0,1,(256,256));grain=n*9
base=np.stack([119+grain,121+grain,107+grain],axis=2)
Image.fromarray(np.uint8(np.clip(base,0,255))).save(R/'stone-color.png')
Image.fromarray(np.uint8(np.clip(195+n*12,0,255))).save(R/'stone-roughness.png')
normal=np.stack([128+n*3,128+r.normal(0,3,(256,256)),np.full((256,256),254)],axis=2)
Image.fromarray(np.uint8(np.clip(normal,0,255))).save(R/'stone-normal.png')
print('MAPS PASS')
