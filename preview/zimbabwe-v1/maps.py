from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(716);y,x=np.mgrid[:256,:256]/256
v=8*np.sin(15*x+3*np.sin(y*8))+5*np.cos(y*22)+rng.normal(0,10,x.shape)
flecks=rng.random(x.shape);v[flecks<.045]-=45;v[flecks>.96]+=30
color=np.stack([155+v,143+v*.95,122+v*.85],-1)
Image.fromarray(np.uint8(np.clip(color,0,255))).save(R/'granite-color.png')
Image.fromarray(np.uint8(np.clip(195+v*.55,0,255))).save(R/'granite-roughness.png')
Image.fromarray(np.uint8(np.clip(color*.48,0,255))).resize((128,128)).save(R/'liner-color.png')
print('MAPS PASS')
