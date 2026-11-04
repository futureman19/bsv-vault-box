from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(934);y,x=np.mgrid[0:256,0:512]
w=y+.9*np.sin(x/26)+1.8*np.sin(x/69+y/38)
v=.92+.028*np.sin(w/12)+.025*np.sin(w/3.1)+.075*np.sin(x/16+y/19)*np.sin(x/41-y/23)+rng.normal(0,.065,x.shape)
vein=np.exp(-((np.sin(x/31+y/24+.7*np.sin(y/27)))/.08)**2)
v-=.13*vein
c=np.stack([118*v,107*v,93*v],-1)
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'stone-color.png')
Image.fromarray(np.uint8(np.clip(178+23*np.sin(w/11)+rng.normal(0,5,x.shape),0,255))).save(R/'stone-roughness.png')
Image.fromarray(np.uint8(np.clip(c*.59,0,255))).resize((256,128)).save(R/'stone-dark.png')
print('PASS procedural stone maps')
