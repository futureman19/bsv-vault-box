from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(331);y,x=np.mgrid[0:256,0:256]/256
cloud=.035*np.sin(x*19+y*13)+.027*np.cos(x*33-y*17)+.019*np.sin(x*61+y*47)
pores=rng.random(x.shape)<.025
v=1+cloud+rng.normal(0,.012,x.shape)-pores*.14
rgb=np.stack([199*v,181*v,145*v],-1)
Image.fromarray(np.uint8(np.clip(rgb,0,255))).save(R/'stone-color.png',optimize=True)
Image.fromarray(np.uint8(np.clip(192+cloud*130+pores*20,0,255))).save(R/'stone-roughness.png',optimize=True)
Image.fromarray(np.uint8(np.clip(rgb*.86,0,255))).save(R/'feet-color.png',optimize=True)
print('PASS compact generated stone maps')
