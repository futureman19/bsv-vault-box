from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1713);y,x=np.mgrid[0:256,0:256]/256
# Original plaster grain, not a photograph or copied cultural motif.
grain=rng.normal(0,1,x.shape);v=1+.035*grain+.035*np.sin(x*17+y*9)+.025*np.cos(y*23-x*8)
color=np.stack([169*v,94*v,57*v],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'earth-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(209+grain*5,180,235))).save(R/'earth-roughness.png',optimize=True)
normal=np.stack([128+grain*2,128+rng.normal(0,2,x.shape),np.full(x.shape,255)],-1)
Image.fromarray(np.uint8(np.clip(normal,0,255))).save(R/'earth-normal.png',optimize=True)
print('PASS procedural maps: 3 x 256x256')
