from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(1207);y,x=np.mgrid[:256,:256]/256
v=1+.055*np.sin(x*22+2*np.sin(y*13))+.035*np.cos(y*31+x*14)+rng.normal(0,.023,x.shape)
for name,base in [('stone-color.png',[193,169,128]),('foot-color.png',[128,111,83])]:
 Image.fromarray(np.uint8(np.clip(v[:,:,None]*np.array(base),0,255))).save(R/name)
Image.fromarray(np.uint8(np.clip(188+25*np.sin(x*33+y*21)+rng.normal(0,5,x.shape),0,255))).save(R/'stone-roughness.png')
print('PASS procedural maps')
