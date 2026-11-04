from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent;D=R/'maps';D.mkdir(exist_ok=True)
rng=np.random.default_rng(1293);y,x=np.mgrid[0:512,0:512]/512
warp=y+.016*np.sin(x*17+y*5)+.009*np.sin(x*37-y*7)
band=np.sin(warp*85)+.38*np.sin(warp*193+x*5)
noise=rng.normal(0,1,(512,512));v=band*9+noise*2.7
rgb=np.stack([183+v*1.2,122+v,76+v*.8],-1)
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(D/'sandstone-color.png')
Image.fromarray(np.uint8(np.clip(191+band*12+noise*5,0,255))).save(D/'sandstone-roughness.png')
Image.fromarray(np.uint8(np.clip(rgb*.72,0,255))).save(D/'sandstone-dark.png')
print('MAPS PASS')
