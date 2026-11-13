from pathlib import Path
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent/'maps';R.mkdir(exist_ok=True)
rng=np.random.default_rng(815);y,x=np.mgrid[0:256,0:256]/256
v=.95+.05*np.sin(x*39+np.sin(y*23))+.035*np.cos(y*47+x*13)+rng.normal(0,.025,x.shape)
for name,c in [('limestone-color',(202,181,143)),('dune-color',(174,97,55))]:
 Image.fromarray(np.uint8(np.clip(np.array(c)*v[:,:,None],0,255))).save(R/(name+'.png'),optimize=True)
Image.fromarray(np.uint8(np.clip(190+22*np.sin(x*39+y*28)+rng.normal(0,7,x.shape),0,255))).save(R/'limestone-roughness.png',optimize=True)
print('MAPS PASS')
