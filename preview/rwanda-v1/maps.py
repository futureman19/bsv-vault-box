from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(250)
for name,color in [('earth',(153,69,47)),('ivory',(231,215,184)),('wood',(75,43,25))]:
 y,x=np.mgrid[:256,:256];noise=rng.normal(0,2,(256,256))+2*np.sin(y*.8+x*.04)
 a=np.clip(np.array(color)[None,None,:]+noise[:,:,None],0,255).astype('uint8');Image.fromarray(a).save(R/(name+'.png'))
print('MAPS PASS')
