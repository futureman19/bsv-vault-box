from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1160);y,x=np.mgrid[:256,:256];noise=rng.normal(0,1,(256,256));v=105+noise*17+8*np.sin(x*.11+y*.06)
color=np.stack([v+4,v+3,v],axis=-1).clip(0,255).astype('uint8')
Image.fromarray(color).save(R/'stone-color.png')
Image.fromarray((190+noise*12).clip(0,255).astype('uint8')).save(R/'stone-roughness.png')
v=61+4*np.sin(y*.3+x*.015)+noise*3
Image.fromarray(np.stack([v-8,v,v+8],axis=-1).clip(0,255).astype('uint8')).save(R/'slate-color.png')
print('MAPS PASS')
