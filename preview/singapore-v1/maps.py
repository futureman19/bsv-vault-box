from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(215);y,x=np.mgrid[:256,:256]
f=np.sin(x*.13+np.sin(y*.09))*np.cos(y*.11)+rng.normal(0,.22,(256,256))
c=np.array([131,181,167])[None,None,:]+f[:,:,None]*6
Image.fromarray(np.uint8(np.clip(c,0,255))).save(R/'celadon-color.png')
r=np.uint8(np.clip(100+f*12,0,255));Image.fromarray(r).save(R/'celadon-roughness.png')
gy,gx=np.gradient(f);n=np.dstack([128-gx*5,128-gy*5,np.full_like(f,255)]);Image.fromarray(np.uint8(np.clip(n,0,255))).save(R/'celadon-normal.png')
print('MAPS PASS')
