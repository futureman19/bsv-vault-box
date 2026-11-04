from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
y,x=np.mgrid[:512,:512];rng=np.random.default_rng(914)
# Interleaved warp/weft value modulation, original generated textile pixels.
warp=(x%8<4);weft=(y%8<4);v=np.where(warp^weft,1.,.76)+rng.normal(0,.018,(512,512))
base=np.zeros((512,512,3))+[200,182,139]
# Compact bands, independently invented geometry and no copied symbolic motifs.
border=(y<48)|(y>464)
base[border]=[37,37,31]
base[((y>18)&(y<30))|((y>482)&(y<494))]=[137,59,45]
base[((y>36)&(y<43))|((y>469)&(y<476))]=[182,146,54]
Image.fromarray(np.uint8(np.clip(base*v[:,:,None],0,255))).save(R/'weave-color.png')
r=np.uint8(np.clip(190+40*(1-v),0,255));Image.fromarray(np.repeat(r[:,:,None],3,2)).save(R/'weave-roughness.png')
g=.75+.12*np.sin(y*.6+np.sin(x*.02))+rng.normal(0,.015,(512,512));Image.fromarray(np.uint8(np.clip(g[:,:,None]*np.array([70,42,25]),0,255))).save(R/'timber.png')
print('MAPS PASS')
